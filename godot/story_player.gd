extends Control
## Story player - reads the converted story files and plays them:
## backgrounds, pictures, dialogue, choices, and changes to game variables.
##
## It does what Ren'Py does when it runs a label. The story itself lives in
## res://story/*.json, made by tools/rpy_to_json.py from your .rpy files.
##
## How it runs: every script file is one flat list of steps. `_pc` is the
## number of the next step. That makes "where am I in the story" two small
## values (list + number), which is what save / load will need later.

signal line_shown(who: String, text: String)   ## a line of dialogue is on screen
signal menu_shown(captions: Array)             ## choices are on screen
signal screen_shown(screen_name: String, screen: Control)  ## a hand-built screen opened
signal menu_requested                          ## the menu button was tapped
signal finished                                ## the label returned with nothing left to run

const SIDE_TAG := "naomi"            # config.side_image_tag
const CHOICE_SIZE := Vector2(670, 107)
const CHOICE_CENTER_Y := 405.0
const CHOICE_TEXT_COLOR := Color("f0e3ca")
const DEFAULT_NAME_COLOR := Color("990000")  # gui.accent_color
const AT_POSITIONS := {                        # Ren'Py's built-in `at` positions
	"left": {"xalign": 0.0, "yalign": 1.0},
	"center": {"xalign": 0.5, "yalign": 1.0},
	"right": {"xalign": 1.0, "yalign": 1.0},
	"truecenter": {"xalign": 0.5, "yalign": 0.5},
}
const MOVE_IN := {"moveinleft": Vector2(-1, 0), "moveinright": Vector2(1, 0),
	"moveintop": Vector2(0, -1), "moveinbottom": Vector2(0, 1)}
const MOVE_OUT := {"moveoutleft": Vector2(-1, 0), "moveoutright": Vector2(1, 0),
	"moveouttop": Vector2(0, -1), "moveoutbottom": Vector2(0, 1)}

## The label to play when this scene starts. Leave empty to start it from code.
## "next_morning" is the top of the day loop. "start" is the very beginning of the game.
@export var start_label := "next_morning"
## Optional background to put up before the label runs (handy when testing one scene).
@export var start_background := ""
## Values the skipped part of the story would have set by now. Only used when
## starting somewhere other than "start". (The opening sets these two names.)
@export var start_values := {"kirako_name": "Kirako", "cat_name": "Maachan"}

## Ren'Py screen name -> the Godot scene that replaces it. A screen that is not
## listed here (or has no res://screens/<name>.tscn) gets the placeholder.
const SCREEN_SCENES := {
	"asakusa_small": "res://screens/map.tscn",
	"asakusa_large": "res://screens/map.tscn",
	"ginza_small": "res://screens/map.tscn",
	"ginza_large": "res://screens/map.tscn",
}
const PLACEHOLDER_SCREEN := "res://screens/placeholder.tscn"

@onready var stage: Control = $Stage
@onready var screen_layer: Control = $Screens
@onready var textbox: Control = $TextBox
@onready var name_box: Control = $TextBox/NameBox
@onready var name_label: Label = $TextBox/NameBox/Name
@onready var dialogue: RichTextLabel = $TextBox/Dialogue
@onready var side: Control = $Side
@onready var choices: VBoxContainer = $Choices
@onready var menu_button: TextureButton = $MenuButton

## Set while a menu is open over the game: taps then do not advance the story.
var menu_open := false

var characters: Dictionary = {}
var images: Dictionary = {}
var tag_transforms: Dictionary = {}
var labels: Dictionary = {}          # label name -> [list of steps, step number]

var _ops: Array = []                 # the list of steps being played
var _pc := 0                         # the next step in that list
var _calls: Array = []               # where to come back to after `call`
var _sprites: Dictionary = {}        # tag -> StageSprite
var _fresh: Array = []               # sprites shown since the last line (for `with dissolve`)
var _attrs: Dictionary = {}          # tag -> last expression used ("happy")
var _audio: Dictionary = {}          # channel -> AudioStreamPlayer
var _audio_file: Dictionary = {}     # channel -> file playing now
var _audio_range: Dictionary = {}    # channel -> [from, to, loop] for `<from 1 to 79.5>`
var _in_menu := false
var _in_screen := false
var _typing: Tween                   # the letter-by-letter reveal of the current line, if any
var _wait_id := 0
var _warned: Dictionary = {}

signal _advanced
signal _chosen(index: int)


func _ready() -> void:
	var data: Dictionary = State.load_json("res://story/game_data.json")
	characters = data.get("characters", {})
	images = data.get("images", {})
	tag_transforms = data.get("tag_transforms", {})
	_load_story_files()
	textbox.hide()
	side.hide()
	menu_button.pressed.connect(func() -> void: menu_requested.emit())
	if start_label != "":
		if start_label != "start":
			for key in start_values:
				if not State.vars.has(key):
					State.vars[key] = start_values[key]
		if start_background != "":
			_show({"t": "scene", "image": start_background})
		start.call_deferred(start_label)


func _load_story_files() -> void:
	for file in DirAccess.get_files_at("res://story"):
		if not file.ends_with(".json") or file == "game_data.json":
			continue
		var story: Dictionary = State.load_json("res://story/" + file)
		for label in story["labels"]:
			labels[label] = [story["ops"], int(story["labels"][label])]


# ---------------------------------------------------------------------------
# Running the story
# ---------------------------------------------------------------------------

## Play a label from its first line until it returns.
func start(label: String) -> void:
	if not _go_to(label):
		return
	_calls.clear()
	await _run()
	finished.emit()


func _go_to(label: String) -> bool:
	if not labels.has(label):
		push_error("Label not found in res://story: " + label)
		return false
	_ops = labels[label][0]
	_pc = labels[label][1]
	return true


func _return() -> bool:
	if _calls.is_empty():
		return false
	var back: Array = _calls.pop_back()
	_ops = back[0]
	_pc = back[1]
	return true


func _run() -> void:
	while true:
		if _pc >= _ops.size():
			if not _return():
				return
			continue
		var op: Dictionary = _ops[_pc]
		_pc += 1
		match op["t"]:
			"say":
				_show_line(op)
				await _wait_for_tap()
			"menu":
				_pc = await _menu(op)
			"show", "scene":
				_show(op)
			"hide":
				_hide(op)
			"with":
				_transition_in(_fresh, op["name"])
				_fresh.clear()
			"pause":
				if op["time"] == null:
					await _wait_for_tap()
				else:
					await _wait_for_tap(op["time"])
			"window":
				textbox.visible = op["show"]
				side.visible = op["show"] and side.get_child_count() > 0
			"set":
				State.assign(op["var"], op["keys"], op["op"], op["value"])
			"eval":
				State.evaluate(op["code"])
			"jump_if_not":
				if not State.evaluate(op["cond"]):
					_pc = int(op["to"])
			"goto":
				_pc = int(op["to"])
			"jump":
				if not _go_to(op["label"]):
					return
			"jump_expr":
				if not _go_to(str(State.evaluate(op["code"]))):
					return
			"call":
				_calls.append([_ops, _pc])
				if not _go_to(op["label"]):
					return
			"call_expr":
				_calls.append([_ops, _pc])
				if not _go_to(str(State.evaluate(op["code"]))):
					return
			"return":
				if not _return():
					return
			"play":
				_play(op)
			"stop":
				_stop(op)
			"screen":
				var action: Dictionary = await _open_screen(op["name"])
				if action.has("jump") and not _go_to(action["jump"]):
					return
			"python":
				if State.has_method(op["func"]):
					State.call(op["func"])
				else:
					push_warning("Python block not ported yet: add func %s() to state.gd (see story/report.txt)" % op["func"])
			"todo":
				push_warning("Skipped (not converted, line %s): %s" % [op.get("line", "?"), op["code"]])
			_:
				push_warning("Unknown step: " + str(op["t"]))


# ---------------------------------------------------------------------------
# Taps
# ---------------------------------------------------------------------------

func _unhandled_input(event: InputEvent) -> void:
	var tapped: bool = event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT
	if tapped or event.is_action_pressed("ui_accept"):
		advance()


## Move on to the next line (same as a tap).
func advance() -> void:
	if menu_open or _in_menu or _in_screen:
		return
	if _typing != null and _typing.is_running():
		# First tap while the line is still appearing: show all of it.
		_typing.kill()
		dialogue.visible_ratio = 1.0
		return
	_advanced.emit()


## Pick a choice by its position in the list (same as tapping it).
func choose(index: int) -> void:
	if _in_menu and not menu_open:
		_chosen.emit(index)


## Wait for a tap. With `seconds`, also carry on by itself after that long.
func _wait_for_tap(seconds: float = -1.0) -> void:
	_wait_id += 1
	var my_id := _wait_id
	if seconds >= 0.0:
		get_tree().create_timer(seconds).timeout.connect(func() -> void:
			if my_id == _wait_id:
				_advanced.emit())
	await _advanced
	_wait_id += 1


# ---------------------------------------------------------------------------
# Dialogue
# ---------------------------------------------------------------------------

func _show_line(op: Dictionary) -> void:
	_fresh.clear()
	var who: Variant = op.get("who")
	var text := _format_text(op["text"])

	if who == "extend":
		dialogue.text += text
	else:
		dialogue.text = text
		var character: Dictionary = characters.get(who, {}) if who != null else {}
		var shown_name := _format_text(character["name"]) if character.get("name") != null else ""
		name_box.visible = shown_name != ""
		name_label.text = shown_name
		var color: Variant = character.get("color")
		name_label.add_theme_color_override("font_color", Color(color) if color != null else DEFAULT_NAME_COLOR)

		# Naomi's side picture stays up whoever is speaking (config.side_image_tag),
		# wearing the last expression she was given.
		var tag: Variant = character.get("image")
		if tag != null and not op["attrs"].is_empty():
			_attrs[tag] = op["attrs"][0]
		_build_side(_attrs.get(SIDE_TAG, "happy"))

	# Text speed setting: letters per second, 0 = the whole line at once.
	var speed := float(State.settings["text_speed"])
	dialogue.visible_ratio = 1.0
	if speed > 0.0 and who != "extend":
		dialogue.visible_ratio = 0.0
		_typing = create_tween()
		_typing.tween_property(dialogue, "visible_ratio", 1.0, dialogue.get_parsed_text().length() / speed)

	textbox.show()
	side.visible = side.get_child_count() > 0
	line_shown.emit(name_label.text if name_box.visible else "", dialogue.get_parsed_text())


## Put game values into text:  "[money] yen"  ->  "10 yen".  Also handles [cafe_menu[0]].
func _fill_in(text: String) -> String:
	text = text.replace("[[", "\u0001")
	var value_re := RegEx.create_from_string("\\[((?:[^\\[\\]]|\\[[^\\[\\]]*\\])+)\\]")
	var found := value_re.search(text)
	while found:
		var code := found.get_string(1).split("!")[0]
		text = text.substr(0, found.get_start()) + str(State.evaluate(code)) + text.substr(found.get_end())
		found = value_re.search(text)
	return text.replace("\u0001", "[lb]")


## Ren'Py text -> Godot text:  [money] shows the value,  {i}..{/i} become tags.
func _format_text(text: String) -> String:
	text = _fill_in(text)

	var tag_re := RegEx.create_from_string("\\{(/?)(\\w*)(=[^}]*)?\\}")
	var out := ""
	var at := 0
	for tag in tag_re.search_all(text):
		out += text.substr(at, tag.get_start() - at)
		if tag.get_string(2) in ["i", "b", "u", "s", "color"]:
			out += "[" + tag.get_string(1) + tag.get_string(2) + tag.get_string(3) + "]"
		at = tag.get_end()
	return out + text.substr(at)


## Naomi's side picture: the same layers, in the same order, as `layeredimage side naomi`.
func _build_side(expression: String) -> void:
	_clear(side)
	var cheek := Color(State.cheek_color_r, State.cheek_color_g, State.cheek_color_b)
	var eye := Color(State.eye_color_r, State.eye_color_g, State.eye_color_b)
	var layers := [
		["base_" + expression, Color.WHITE],
		["blush_" + expression, cheek],
		["eye_" + expression, eye],
		["lip_" + expression, Color.WHITE],   # TODO lipstick hue/saturation needs a small shader
		[State.naomi_hair, Color.WHITE],
		[State.naomi_dress, Color.WHITE],
	]
	for layer in layers:
		var texture := _texture("images/side/side_naomi_%s.png" % layer[0])
		if texture == null:
			continue
		var rect := TextureRect.new()
		rect.texture = texture
		rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		rect.set_anchors_preset(Control.PRESET_FULL_RECT)
		rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
		rect.modulate = layer[1]
		side.add_child(rect)


# ---------------------------------------------------------------------------
# Choices
# ---------------------------------------------------------------------------

func _menu(op: Dictionary) -> int:
	if op["prompt"] != null:
		_show_line(op["prompt"])
	else:
		textbox.hide()
		side.hide()

	# Like Ren'Py, a choice whose `if` is false is not shown at all.
	var open: Array = []
	for choice in op["choices"]:
		if choice["cond"] == null or State.evaluate(choice["cond"]):
			open.append(choice)
	if open.is_empty():
		return _pc

	var captions: Array = []
	for i in open.size():
		var caption := _format_text(open[i]["text"])
		captions.append(caption)
		choices.add_child(_choice_button(caption, i))
	choices.size = Vector2(CHOICE_SIZE.x, 0)
	choices.reset_size()
	choices.position = Vector2(StageSprite.SCREEN.x - CHOICE_SIZE.x, CHOICE_CENTER_Y - choices.size.y / 2.0)
	choices.show()

	_in_menu = true
	menu_shown.emit(captions)
	var picked: int = await _chosen
	_in_menu = false
	choices.hide()
	_clear(choices)
	return int(open[picked]["to"])


func _choice_button(caption: String, index: int) -> Button:
	var button := Button.new()
	button.text = caption
	button.custom_minimum_size = CHOICE_SIZE
	button.alignment = HORIZONTAL_ALIGNMENT_RIGHT
	button.focus_mode = Control.FOCUS_NONE
	var box := StyleBoxTexture.new()
	box.texture = _texture("gui/button/choice_idle_background.png")
	box.content_margin_top = 30      # gui.choice_button_borders = Borders(0, 30, 20, 0)
	box.content_margin_right = 20
	for state in ["normal", "hover", "pressed"]:
		button.add_theme_stylebox_override(state, box)
	for state in ["font_color", "font_hover_color", "font_pressed_color"]:
		button.add_theme_color_override(state, CHOICE_TEXT_COLOR)
	button.add_theme_font_override("font", dialogue.get_theme_font("normal_font"))
	button.add_theme_font_size_override("font_size", 50)
	button.pressed.connect(choose.bind(index))
	return button


# ---------------------------------------------------------------------------
# Screens (`call screen map` and friends)
# ---------------------------------------------------------------------------

## Open a hand-built screen and wait until it closes.
## Every screen scene has `signal closed(action)`. The action is {"jump": "label"}
## for Ren'Py's Jump("label"), or {} for Return().
func _open_screen(screen_name: String) -> Dictionary:
	var path: String = SCREEN_SCENES.get(screen_name, "res://screens/%s.tscn" % screen_name)
	if not ResourceLoader.exists(path):
		path = PLACEHOLDER_SCREEN
	var screen: Control = load(path).instantiate()
	if "screen_name" in screen:
		screen.screen_name = screen_name
	textbox.hide()
	side.hide()
	_in_screen = true
	screen_layer.add_child(screen)
	screen_shown.emit(screen_name, screen)
	var action: Dictionary = await screen.closed
	_in_screen = false
	screen.queue_free()
	return action


# ---------------------------------------------------------------------------
# Pictures on the stage
# ---------------------------------------------------------------------------

func _show(op: Dictionary) -> void:
	if op["t"] == "scene":
		# With a fade, the old pictures stay under the new one until it has faded in.
		var keep := 0.5 if _is_fade(op.get("with", "")) else 0.0
		for old in _sprites.values():
			if keep > 0.0:
				get_tree().create_timer(keep).timeout.connect(old.queue_free)
			else:
				old.queue_free()
		_sprites.clear()
		if op.get("image") == null:
			return

	var image_name: String = op["image"]
	var tag := image_name.split(" ")[0]
	var sprite: StageSprite = _sprites.get(tag)
	var is_new := sprite == null
	if is_new:
		sprite = StageSprite.new()
		_sprites[tag] = sprite
		stage.add_child(sprite)
		_apply(sprite, tag_transforms.get(tag, {}))

	if op.has("text"):
		_set_text_picture(sprite, op["text"])
	elif sprite.image_name != image_name or images.get(image_name, {}).has("dynamic"):
		image_name = _find_image(image_name, sprite.image_name)
		var entry: Dictionary = images.get(image_name, {})
		if entry.is_empty():
			_warn_once("No picture called '%s'. Check story/report.txt." % op["image"])
		else:
			# A "dynamic" picture has a game value in its file name: images/cafe/[cafe_menu[0]].png
			sprite.texture = _texture(_fill_in(entry["path"]) if entry.has("dynamic") else entry["path"])
			sprite.image_name = image_name
			if sprite.texture != null:
				if entry.has("size"):
					sprite.base_size = Vector2(entry["size"][0], entry["size"][1])
				else:
					sprite.base_size = sprite.texture.get_size() * float(entry.get("zoom", 1.0))
			sprite.place()

	for position_name in op.get("at", []):
		if AT_POSITIONS.has(position_name):
			_apply(sprite, AT_POSITIONS[position_name])
		else:
			_warn_once("Position '%s' is not built yet (add it to AT_POSITIONS)." % position_name)

	if op.has("zorder"):
		sprite.z_index = int(op["zorder"])
	if is_new:
		_fresh.append(sprite)
	if op.has("with"):
		_transition_in([sprite], op["with"])
	if op.has("atl"):
		_run_atl(sprite, op["atl"])


## `show kirako` with no expression keeps the picture already up; otherwise it
## takes the first picture with that tag, the way Ren'Py guesses.
func _find_image(image_name: String, showing: String) -> String:
	if images.has(image_name) or image_name.contains(" "):
		return image_name
	if showing != "":
		return showing
	var names: Array = images.keys()
	names.sort()
	for candidate in names:
		if candidate.begins_with(image_name + " "):
			return candidate
	return image_name


## `show text "..."` : words on the stage, placed like any other picture.
func _set_text_picture(sprite: StageSprite, text: String) -> void:
	for child in sprite.get_children():
		child.queue_free()
	var font := dialogue.get_theme_font("normal_font")
	var label := RichTextLabel.new()
	label.bbcode_enabled = true
	label.autowrap_mode = TextServer.AUTOWRAP_OFF
	label.scroll_active = false
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.add_theme_font_override("normal_font", font)
	label.add_theme_font_size_override("normal_font_size", 50)
	label.text = _format_text(text)
	label.size = font.get_string_size(label.get_parsed_text(), HORIZONTAL_ALIGNMENT_LEFT, -1, 50) + Vector2(8, 8)
	sprite.texture = null
	sprite.add_child(label)
	sprite.image_name = "text"
	sprite.base_size = label.size
	sprite.place()


## Simple ATL: each line either sets values at once or moves to them over time.
func _run_atl(sprite: StageSprite, steps: Array) -> void:
	if sprite.running_tween != null:
		sprite.running_tween.kill()
	var tween := create_tween()
	sprite.running_tween = tween
	var added := false
	for step in steps:
		if step.has("wait"):
			tween.tween_interval(step["wait"])
			added = true
			continue
		var props := StageSprite.canonical(step["props"])
		if step["warp"] == null:
			tween.tween_callback(_apply.bind(sprite, props))
			added = true
			continue
		# Ren'Py's "easein" starts fast and slows down, which Godot calls EASE_OUT.
		var trans := Tween.TRANS_LINEAR if step["warp"] == "linear" else Tween.TRANS_SINE
		var ease := Tween.EASE_IN_OUT
		if step["warp"] == "easein":
			ease = Tween.EASE_OUT
		elif step["warp"] == "easeout":
			ease = Tween.EASE_IN
		if props.is_empty():
			tween.tween_interval(step["time"])
		var first := true
		for key in props:
			var mover := tween.tween_property(sprite, key, props[key], step["time"]) if first \
				else tween.parallel().tween_property(sprite, key, props[key], step["time"])
			mover.set_trans(trans).set_ease(ease)
			first = false
		added = true
	if not added:
		tween.kill()


func _apply(sprite: StageSprite, props: Dictionary) -> void:
	var clean := StageSprite.canonical(props)
	for key in clean:
		sprite.set(key, clean[key])


func _hide(op: Dictionary) -> void:
	var tag: String = op["image"].split(" ")[0]
	var sprite: StageSprite = _sprites.get(tag)
	if sprite == null:
		return
	_sprites.erase(tag)
	_fresh.erase(sprite)
	if sprite.running_tween != null:
		sprite.running_tween.kill()
	var how: String = op.get("with", "")
	var tween := create_tween()
	if _is_fade(how):
		tween.tween_property(sprite, "alpha", 0.0, 0.5)
	elif MOVE_OUT.has(how):
		var away: Vector2 = MOVE_OUT[how] * StageSprite.SCREEN
		tween.tween_property(sprite, "xoffset", away.x, 0.5)
		tween.parallel().tween_property(sprite, "yoffset", away.y, 0.5)
	elif how != "":
		_warn_once("Transition '%s' is not built yet, so it happens instantly." % how)
	tween.tween_callback(sprite.queue_free)


func _transition_in(sprites: Array, how: String) -> void:
	for sprite in sprites:
		if not is_instance_valid(sprite):
			continue
		if _is_fade(how):
			sprite.alpha = 0.0
			create_tween().tween_property(sprite, "alpha", 1.0, 0.5)
		elif MOVE_IN.has(how):
			var from: Vector2 = MOVE_IN[how] * StageSprite.SCREEN
			sprite.xoffset = from.x
			sprite.yoffset = from.y
			var tween := create_tween()
			tween.tween_property(sprite, "xoffset", 0.0, 0.5)
			tween.parallel().tween_property(sprite, "yoffset", 0.0, 0.5)
		elif how != "" and how != "None":
			_warn_once("Transition '%s' is not built yet, so it happens instantly." % how)


## dissolve, fade, Fade(2.0, 0.5, 2.0), Dissolve(.2), fadehold ... all become a half-second fade for now.
func _is_fade(how: String) -> bool:
	var lower := how.to_lower()
	return lower.contains("fade") or lower.contains("dissolve")


# ---------------------------------------------------------------------------
# Music and sound
# ---------------------------------------------------------------------------

func _play(op: Dictionary) -> void:
	var channel: String = op["channel"]
	if op["if_changed"] and _audio_file.get(channel) == op["file"]:
		return
	var stream: AudioStream = load(State.asset("audio/" + op["file"])) if ResourceLoader.exists(State.asset("audio/" + op["file"])) else null
	if stream == null:
		_warn_once("Audio file not found: " + op["file"])
		return
	if stream is AudioStreamMP3 or stream is AudioStreamOggVorbis:
		stream.loop = op["loop"]
	if not _audio.has(channel):
		_audio[channel] = AudioStreamPlayer.new()
		_audio[channel].bus = "Music" if channel == "music" else "Sound"   # the two volume sliders
		add_child(_audio[channel])
	var player: AudioStreamPlayer = _audio[channel]
	player.stream = stream
	player.volume_db = 0.0
	player.play(op["from"])
	_audio_file[channel] = op["file"]
	if op.has("to"):
		_audio_range[channel] = [op["from"], op["to"], op["loop"]]
	else:
		_audio_range.erase(channel)
	if op["fadein"] > 0.0:
		player.volume_db = -40.0
		create_tween().tween_property(player, "volume_db", 0.0, op["fadein"])


## `<from 1 to 79.5>` : when the end point is reached, loop back or stop.
func _process(_delta: float) -> void:
	for channel in _audio_range:
		var player: AudioStreamPlayer = _audio[channel]
		var part: Array = _audio_range[channel]
		if player.playing and player.get_playback_position() >= part[1]:
			if part[2]:
				player.seek(part[0])
			else:
				player.stop()


func _stop(op: Dictionary) -> void:
	var player: AudioStreamPlayer = _audio.get(op["channel"])
	_audio_file.erase(op["channel"])
	_audio_range.erase(op["channel"])
	if player == null:
		return
	if op["fadeout"] > 0.0:
		var tween := create_tween()
		tween.tween_property(player, "volume_db", -40.0, op["fadeout"])
		tween.tween_callback(player.stop)
	else:
		player.stop()


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

func _texture(path: String) -> Texture2D:
	var full := State.asset(path)
	if not ResourceLoader.exists(full):
		return null
	return load(full)


func _clear(node: Node) -> void:
	for child in node.get_children():
		node.remove_child(child)
		child.queue_free()


func _warn_once(message: String) -> void:
	if not _warned.has(message):
		_warned[message] = true
		push_warning(message)
