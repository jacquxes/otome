extends Node
## State - every game variable, with the same names as in Ren'Py.
##
## This is the Godot version of Ren'Py's "store". The starting values come from
## the `default` lines in the .rpy files (the converter copies them into
## story/game_data.json), so you never type them twice.
##
## From any script:   State.money      State.encounters["musician"]
## From story data:   conditions and `$` lines are run by evaluate() below.
##
## The game rules you wrote as Python functions (flag, set_flag, get_stage,
## musician_8_ready ...) get ported here by hand, one function each, same names.

var vars: Dictionary = {}
var _renamed: Dictionary = {}

## Kept between playthroughs and between launches (Ren'Py's `persistent`):
## gallery unlocks, vibration on/off. In the story it is `persistent.name`.
var persistent: Dictionary = {}
## The player's settings. Also kept between launches.
var settings: Dictionary = {"music_volume": 1.0, "sound_volume": 1.0, "mute": false, "text_speed": 0}

const KEPT_FILE := "user://kept.json"


func _ready() -> void:
	# Two volume channels, like Ren'Py's music and sound mixers.
	for bus_name in ["Music", "Sound"]:
		AudioServer.add_bus()
		AudioServer.set_bus_name(AudioServer.bus_count - 1, bus_name)
	_load_kept()
	apply_settings()
	reset()


## Put every variable back to its starting value (new game).
func reset() -> void:
	vars.clear()
	var data: Dictionary = load_json("res://story/game_data.json")
	_renamed = data.get("renamed", {})
	for key in data.get("defaults", {}):
		vars[key] = evaluate(data["defaults"][key])
	vars["persistent"] = persistent   # the same dictionary, so the story's changes are kept


# These two let `State.money` and `money` (inside story conditions) find the
# values stored in `vars`.
func _get(property: StringName) -> Variant:
	return vars.get(String(property))


func _set(property: StringName, value: Variant) -> bool:
	if vars.has(String(property)):
		vars[String(property)] = value
		return true
	return false


## Run one converted expression, e.g. "(money >= 10)" or "flag(\"met_hideo\")".
## Game variables are found by name in `vars`; function names are looked up in this script.
func evaluate(code: String) -> Variant:
	var expression := Expression.new()
	if expression.parse(code, PackedStringArray(vars.keys())) != OK:
		push_error("Story expression could not be read: %s (%s)" % [code, expression.get_error_text()])
		return null
	var result: Variant = expression.execute(vars.values(), self)
	if expression.has_execute_failed():
		push_error("Story expression failed: %s (%s). Either a variable in it has no value yet, or it calls a function that still needs porting into state.gd." % [code, expression.get_error_text()])
		return null
	return result


## Run one converted `$` assignment, e.g.  $ encounters["musician"] += 1
func assign(variable: String, keys: Array, op: String, value_code: String) -> void:
	var value: Variant = evaluate(value_code)
	if variable == "persistent":
		save_kept.call_deferred()
	if keys.is_empty():
		vars[variable] = _combine(vars.get(variable), op, value)
		return
	var holder: Variant = vars.get(variable)
	for i in keys.size() - 1:
		holder = holder[evaluate(keys[i])]
	var last: Variant = evaluate(keys[-1])
	var old: Variant = holder.get(last) if holder is Dictionary else holder[last]
	holder[last] = _combine(old, op, value)


func _combine(old: Variant, op: String, value: Variant) -> Variant:
	match op:
		"=": return value
		"+=": return old + value
		"-=": return old - value
		"*=": return old * value
		"/=": return old / value
		"%=": return old % value
	push_error("Unknown assignment: " + op)
	return old


# ---------------------------------------------------------------------------
# Things kept between launches
# ---------------------------------------------------------------------------

func _load_kept() -> void:
	var data: Dictionary = load_json("res://story/game_data.json")
	_renamed = data.get("renamed", {})
	for key in data.get("persistent", {}):
		persistent[key] = evaluate(data["persistent"][key])
	if not FileAccess.file_exists(KEPT_FILE):
		return
	var kept: Variant = JSON.parse_string(FileAccess.get_file_as_string(KEPT_FILE))
	if kept is Dictionary:
		persistent.merge(kept.get("persistent", {}), true)
		settings.merge(kept.get("settings", {}), true)


## Write `persistent` and `settings` to the device.
func save_kept() -> void:
	var file := FileAccess.open(KEPT_FILE, FileAccess.WRITE)
	if file != null:
		file.store_string(JSON.stringify({"persistent": persistent, "settings": settings}, "\t"))


## Change one setting, apply it and keep it.
func set_setting(setting_name: String, value: Variant) -> void:
	settings[setting_name] = value
	apply_settings()
	save_kept()


func apply_settings() -> void:
	for pair in [["Music", "music_volume"], ["Sound", "sound_volume"]]:
		var bus := AudioServer.get_bus_index(pair[0])
		AudioServer.set_bus_volume_db(bus, linear_to_db(max(float(settings[pair[1]]), 0.0001)))
		AudioServer.set_bus_mute(bus, bool(settings["mute"]) or float(settings[pair[1]]) <= 0.0)


## "images/bg shrine.png" -> the res:// path of its copy in this project.
## (A few files are copied under a corrected extension; `_renamed` knows which.)
func asset(game_path: String) -> String:
	return "res://assets/game/" + _renamed.get(game_path, game_path)


static func load_json(path: String) -> Variant:
	var text := FileAccess.get_file_as_string(path)
	if text.is_empty():
		push_error("Could not read " + path)
		return {}
	return JSON.parse_string(text)


# ---------------------------------------------------------------------------
# Game rules ported from script.rpy, same names, same order as the Python.
# Add the rest here as each route needs them.
# ---------------------------------------------------------------------------

# -- story flags --

func flag(flag_name: String) -> bool:
	return bool(vars["story_flags"].get(flag_name, false))


func set_flag(flag_name: String) -> void:
	vars["story_flags"][flag_name] = true


# -- musician conditions --

const MUSICIAN_INTRO_GAP := 1


func _musician_day_gate(flag_key: String, gap: int = MUSICIAN_INTRO_GAP) -> bool:
	var last_day: int = vars["story_flags"].get(flag_key, -9999)
	return (last_day - vars["totaldays"]) >= gap


func musician_8_gate() -> bool:
	return _musician_day_gate("musician_1_day")


func musician_8_ready() -> bool:
	return vars["relationship_points"]["musician"] >= 3 and not flag("musician_show_seen")


func musician_show_today() -> bool:
	return vars["dayofweeknumber"] == 6 and vars["musician_event"] == 1 and vars["totaldays"] <= 16


func musician_casual_paused() -> bool:
	var show_window: bool = (flag("musician_show_seen") or musician_show_today()) and vars["encounters"]["musician"] < 10
	return show_window or musician_tower_today()


func musician_9_condition() -> bool:
	return flag("musician_ticketer_talk_seen")


func musician_9_blocked() -> void:
	vars["encounters"]["musician"] += 1


func musician_9_branch() -> String:
	var days_since_9: int = vars["story_flags"].get("musician_9_day", -9999) - vars["totaldays"]
	return "musician_9a" if days_since_9 <= 2 else "musician_9b"


func musician_11_condition() -> bool:
	return vars["totaldays"] >= 3


func musician_tower_today() -> bool:
	return vars["dayofweeknumber"] == 7 and vars["musician_event"] == 3


## The Godot version of musician_encounter_table + get_musician_action().
## Returns the label to play at the theatre, or null for an ordinary visit.
func get_musician_action() -> Variant:
	match int(vars["encounters"]["musician"]):
		1: return "musician_1"
		3: return "musician_3"
		5: return "musician_5"
		7: return "musician_7"
		8: return "musician_8" if musician_8_ready() else null
		10: return musician_9_branch()
	return null


# -- phone --

## renpy.vibrate(seconds): buzz the phone, if the player has vibration on in Settings.
func vibrate(seconds: float) -> void:
	if persistent.get("haptics_enabled", true):
		Input.vibrate_handheld(int(seconds * 1000.0))


# -- relationship stage --

func add_point(character: String) -> void:
	vars["relationship_points"][character] = min(vars["relationship_points"][character] + 1, 15)


func get_stage(character: String) -> int:
	var pts: int = vars["relationship_points"][character]
	if pts >= 13: return 5
	if pts >= 10: return 4
	if pts >= 6: return 3
	if pts >= 3: return 2
	if pts >= 1: return 1
	return 0


func calc_demographics() -> int:
	var total := 0
	for character in vars["relationship_points"]:
		total += get_stage(character)
	return min(int(total * (30.0 / 25.0)), 30)


# -- cafe --

## Cafe encounters that override casual visits come from `cafe_encounter_triggers`
## in script.rpy (read by the converter): character -> encounter number ->
## {"item": menu item needed, "condition": name of a function in this file, or null}.


## Call this ONCE, right before the cafe_game screen is shown. (screens_cafe.rpy)
func setup_cafe_round() -> void:
	var customer_table: Array = [0.0, 0.5, 1.0]
	var customer_order: Array = [" please.", ", thank you.", " for me."]
	customer_table.shuffle()
	customer_order.shuffle()

	var order_times: Array
	if vars["tutorial_mode"]:
		# Kirako leaves at about 4.5s, so start after that and space them out.
		order_times = [5.0, 6.5, 8.0]
		order_times.shuffle()
	else:
		order_times = [randi_range(1, 3), randi_range(1, 3), randi_range(1, 3)]

	vars["customer_table"] = customer_table
	vars["customer_order"] = customer_order
	vars["order_times"] = order_times
	vars["served_food"] = 0
	vars["shift_tips"] = 0


## The trigger for this character's current encounter number, if its menu item
## is on today's menu and its condition passes. Otherwise null.
func _cafe_trigger(character: String) -> Variant:
	var trigger: Variant = vars["cafe_encounter_triggers"].get(character, {}).get(int(vars["encounters"][character]))
	if trigger == null:
		return null
	var item_match: bool = trigger["item"] in vars["cafe_menu"]
	var cond_match: bool = call(trigger["condition"]) if trigger["condition"] != null else true
	return trigger if item_match and cond_match else null


## Python's sorted(names, key=scores)[0] : the first name with the lowest score
## (or the highest, with reverse=True). Ties keep their original order.
func _first_by(names: Array, scores: Dictionary, highest: bool) -> String:
	var best: String = names[0]
	for candidate in names:
		if (highest and scores[candidate] > scores[best]) or (not highest and scores[candidate] < scores[best]):
			best = candidate
	return best


func _can_visit(character: String, already_picked: Array) -> bool:
	return character in vars["unlocked_chars"] and not vars["visited_today"][character] \
		and character not in already_picked


# -- python: blocks, one function each (names come from story/report.txt) --

## script_02_day_choices.rpy, label reset_daily_visits
func py_reset_daily_visits_1() -> void:
	for c in vars["visited_today"]:
		vars["visited_today"][c] = false
	vars["cafe_menu"] = []


## script_03_cafe.rpy, label check_cafe_visits: who drops by the cafe this shift.
## Sets `visiting_chars` (up to two characters), read by the story lines that follow.
func py_check_cafe_visits_1() -> void:
	var cafe_menu: Array = vars["cafe_menu"]
	var item_to_character: Dictionary = vars["item_to_character"]
	var eligible: Array = []
	var already_picked: Array = []
	var fixed_chars_today: Array = []
	var forced_char: Variant = null

	# Check for forced encounter triggers first
	for character in vars["cafe_encounter_triggers"]:
		if character not in vars["unlocked_chars"] or vars["visited_today"][character]:
			continue
		if _cafe_trigger(character) != null:
			forced_char = character
			break

	if forced_char != null:
		already_picked.append(forced_char)
		fixed_chars_today.append(forced_char)

	# Pass 1: fixed items (excluding forced)
	for item in cafe_menu:
		var mapping: Variant = item_to_character.get(item)
		if mapping == null or mapping is Array:
			continue
		if mapping == "musician" and musician_casual_paused():
			continue
		if _can_visit(mapping, already_picked):
			eligible.append(mapping)
			already_picked.append(mapping)
			fixed_chars_today.append(mapping)

	# Pass 2: randomized items (excluding forced)
	for item in cafe_menu:
		var mapping: Variant = item_to_character.get(item)
		if mapping == null or not (mapping is Array):
			continue
		var candidates: Array = []
		for c in mapping:
			if _can_visit(c, already_picked) and not (c == "musician" and musician_casual_paused()):
				candidates.append(c)
		if not candidates.is_empty():
			var chosen: String
			if randf() < vars["CATCHUP_CHANCE"]:
				chosen = _first_by(candidates, vars["total_visits"], false)
			else:
				chosen = _first_by(candidates, vars["encounters"], true)
			eligible.append(chosen)
			already_picked.append(chosen)

	# Slot selection
	var visiting_chars: Array = []
	if forced_char != null:
		visiting_chars.append(forced_char)
		if not eligible.is_empty():
			eligible.shuffle()
			visiting_chars.append(eligible[0])
	elif not eligible.is_empty():
		eligible.shuffle()
		var pool: Array = fixed_chars_today if not fixed_chars_today.is_empty() else eligible
		if randf() < vars["CATCHUP_CHANCE"]:
			visiting_chars.append(_first_by(pool, vars["total_visits"], false))
		else:
			visiting_chars.append(_first_by(pool, vars["encounters"], true))
		var remaining: Array = eligible.filter(func(c: String) -> bool: return c not in visiting_chars)
		if not remaining.is_empty():
			visiting_chars.append(remaining.pick_random())

	vars["visiting_chars"] = visiting_chars


## script_03_cafe.rpy, slot 1: is this visit a story encounter? Sets `override1`.
func py_check_cafe_visits_2() -> void:
	vars["override1"] = _cafe_override(vars["char1"])


## script_03_cafe.rpy, slot 2: the same for the second visitor. Sets `override2`.
func py_check_cafe_visits_3() -> void:
	vars["override2"] = _cafe_override(vars["char2"])


## The story label for this visit, e.g. "musician_4", or null for a casual visit.
func _cafe_override(character: String) -> Variant:
	if _cafe_trigger(character) == null:
		return null
	return character + "_" + str(int(vars["encounters"][character]))
