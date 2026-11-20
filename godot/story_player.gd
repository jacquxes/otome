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
var transitions: Dictionary = {}     # your own `define fadehold = Fade(...)` lines
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
var _overlays: Dictionary = {}       # screens shown with `show screen`, by name
var _typing: Tween                   # the letter-by-letter reveal of the current line, if any
var _wait_id := 0
var _warned: Dictionary = {}

## Where each character usually stands, adjusted by hand in Godot (layout mode, F2).
## Saved in res://sprite_positions.json, e.g. {"kirako": {"xalign": 0.4, "yoffset": 20, "zoom": 0.55}}.
## These replace the config.tag_transform values from Ren'Py. A `show ... at` or a
## `show ...:` block in the script still moves a character for that scene.
const POSITIONS_FILE := "res://sprite_positions.json"
var sprite_positions: Dictionary = {}
var _layout_mode := false
var _layout_selected: StageSprite
var _layout_dragging := false
var _layout_last_mouse := Vector2.ZERO
var _layout_note: Label

signal _advanced
signal _chosen(index: int)


func _ready() -> void:
	var data: Dictionary = State.load_json("res://story/game_data.json")
	characters = data.get("characters", {})
	images = data.get("images", {})
	tag_transforms = data.get("tag_transforms", {})
	transitions = data.get("transitions", {})
	if FileAccess.file_exists(POSITIONS_FILE):
		sprite_positions = State.load_json(POSITIONS_FILE)
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
				if op.has("with"):
					_screen_transition(op["with"])    # e.g. "Unngh!" with vpunch
				await _wait_for_tap()
			"menu":
				_pc = await _menu(op)
			"show", "scene":
				_show(op)
				await _screen_transition(op.get("with", ""))
			"hide":
				_hide(op)
				await _screen_transition(op.get("with", ""))
			"with":
				_transition_in(_fresh, op["name"])
				_fresh.clear()
				await _screen_transition(op["name"])
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
			"restart":
				# renpy.full_restart(): stop the story; main.gd goes back to the title menu.
				_calls.clear()
				return
			"play":
				_play(op)
			"stop":
				_stop(op)
			"show_screen":
				_show_overlay(op["name"], op.get("with", ""))
			"hide_screen":
				_hide_overlay(op["name"])
			"screen":
				var action: Dictionary = await _open_screen(op["name"], op.get("with", ""))
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
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_F2:
		set_layout_mode(not _layout_mode)
		return
	if _layout_mode:
		_layout_input(event)
		return
	var tapped: bool = event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT
	if tapped or event.is_action_pressed("ui_accept"):
		advance()


## Move on to the next line (same as a tap).
func advance() -> void:
	if _transition != null:
		_end_transition()     # a tap skips to the end of a transition, as in Ren'Py
		return
	if menu_open or _in_menu or _in_screen or _layout_mode or _modal_overlay():
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
func _open_screen(screen_name: String, with_how: String = "") -> Dictionary:
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
	_screen_transition(with_how)     # call screen cafe_menu with pushleft
	var action: Dictionary = await screen.closed
	_in_screen = false
	screen.queue_free()
	return action


## `show screen X`: put a screen on top and carry on with the story straight away.
## Only screens that have a Godot scene are shown; the rest are skipped with a warning.
## A screen with `var modal := true` stops taps from moving the story on while it is up.
## It goes away with `hide screen X`, or by itself by emitting `closed`.
func _show_overlay(screen_name: String, with_how: String = "") -> void:
	var path: String = SCREEN_SCENES.get(screen_name, "res://screens/%s.tscn" % screen_name)
	if not ResourceLoader.exists(path):
		_warn_once("show screen %s: no Godot scene for it yet, so it is skipped." % screen_name)
		return
	_hide_overlay(screen_name)
	var screen: Control = load(path).instantiate()
	_overlays[screen_name] = screen
	if screen.has_signal("closed"):
		screen.closed.connect(func(_action: Dictionary) -> void: _hide_overlay(screen_name))
	screen_layer.add_child(screen)
	screen_shown.emit(screen_name, screen)
	_screen_transition(with_how)


func _hide_overlay(screen_name: String) -> void:
	var screen: Control = _overlays.get(screen_name)
	_overlays.erase(screen_name)
	if screen != null and is_instance_valid(screen):
		screen.queue_free()


func _modal_overlay() -> bool:
	for screen in _overlays.values():
		if is_instance_valid(screen) and screen.get("modal") == true:
			return true
	return false


# ---------------------------------------------------------------------------
# Pictures on the stage
# ---------------------------------------------------------------------------

func _show(op: Dictionary) -> void:
	if op["t"] == "scene":
		for old in _sprites.values():
			old.queue_free()
		_sprites.clear()
		# Like Ren'Py's `window auto`: the text box steps aside for a new scene
		# and comes back with the next line.
		textbox.hide()
		side.hide()
		if op.get("image") == null:
			return

	var image_name: String = op["image"]
	# `show bg cafeleft as bg_copy` puts up a second copy under its own name.
	var tag: String = op.get("tag", image_name.split(" ")[0])
	var sprite: StageSprite = _sprites.get(tag)
	var is_new := sprite == null
	if is_new:
		sprite = StageSprite.new()
		_sprites[tag] = sprite
		stage.add_child(sprite)
		if op.has("atl"):
			# Ren'Py: a picture shown with its own block does not get the usual
			# centre-bottom placement. Whatever the block leaves out starts at the
			# top-left, so `xpos 1119 ypos 262` is the picture's top-left corner.
			_apply(sprite, {"xpos": 0.0, "ypos": 0.0, "xanchor": 0.0, "yanchor": 0.0})
		_apply_usual(sprite, tag_transforms.get(tag, {}))
		_apply_usual(sprite, sprite_positions.get(tag, {}))

	if op.has("text"):
		_set_text_picture(sprite, op["text"])
	elif sprite.image_name != image_name or images.get(image_name, {}).has("dynamic"):
		image_name = _find_image(image_name, sprite.image_name)
		var entry: Dictionary = images.get(image_name, {})
		if sprite.frames_tween != null:
			sprite.frames_tween.kill()
			sprite.glitch = 0.0
		if entry.is_empty():
			_warn_once("No picture called '%s'. Check story/report.txt." % op["image"])
		elif entry.has("frames"):
			sprite.image_name = image_name
			_apply(sprite, entry.get("props", {}))
			_play_frames(sprite, entry)
		else:
			_set_picture(sprite, entry)
			sprite.image_name = image_name

	for position_name in op.get("at", []):
		if AT_POSITIONS.has(position_name):
			_apply(sprite, AT_POSITIONS[position_name])
		elif position_name == "atl_dizzy":
			_at_dizzy(sprite)
		else:
			_warn_once("Position '%s' is not built yet (add it to AT_POSITIONS)." % position_name)

	if op.has("zorder"):
		sprite.zorder = int(op["zorder"])
	_sort_stage()
	if is_new:
		_fresh.append(sprite)
	if op.has("with"):
		_transition_in([sprite], op["with"])
	if op.has("atl"):
		_run_atl(sprite, op["atl"])


## Show one picture from game_data.json on a sprite (a plain file, a resized or cropped one,
## or one with a game value in its file name like images/cafe/[cafe_menu[0]].png).
func _set_picture(sprite: StageSprite, entry: Dictionary) -> void:
	var art := _texture(_fill_in(entry["path"]) if entry.has("dynamic") else entry["path"])
	if art != null and entry.has("crop"):
		var cut := AtlasTexture.new()
		cut.atlas = art
		cut.region = Rect2(entry["crop"][0], entry["crop"][1], entry["crop"][2], entry["crop"][3])
		art = cut
	sprite.texture = art
	if art != null:
		if entry.has("size"):
			sprite.base_size = Vector2(entry["size"][0], entry["size"][1])
		else:
			sprite.base_size = art.get_size() * float(entry.get("zoom", 1.0))
	sprite.place()


## A picture made of frames (`image kirako glitched:` / `image merchant discussing:`):
## each frame is another picture, maybe glitched, shown for its time.
func _play_frames(sprite: StageSprite, entry: Dictionary) -> void:
	var frames: Array = entry["frames"]
	var tween := create_tween()
	sprite.frames_tween = tween
	var total := 0.0
	for frame in frames:
		tween.tween_callback(func() -> void:
			var picture: Dictionary = images.get(frame["image"], {})
			if picture.has("path"):
				_set_picture(sprite, picture)
			sprite.glitch = float(frame.get("glitch", 0))
			sprite.new_glitch_pattern())
		if frame["time"] > 0.0:
			tween.tween_interval(frame["time"])
			total += frame["time"]
	if entry.get("loop", false) and total > 0.0:
		tween.set_loops()


## The double-vision effect (`transform atl_dizzy` in script.rpy), rebuilt by hand
## because it uses `choice` and `parallel`. A copy of the picture sways, swells and
## blurs, then fades away.
func _at_dizzy(sprite: StageSprite, t := 0.4, angle := 1.0, grow := 1.05) -> void:
	_apply(sprite, {"alpha": 1.0, "rotate": 0.0, "zoom": 1.0, "xpos": 0.5, "ypos": 1.0, "xanchor": 0.5, "yanchor": 1.0})
	var side := 1.0 if randf() < 0.5 else -1.0      # the two `choice` blocks are mirror images
	var tween := create_tween()
	tween.tween_property(sprite, "rotate", angle * side, t).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tween.parallel().tween_property(sprite, "alpha", 0.5, t)
	tween.parallel().tween_property(sprite, "zoom", grow, t)
	tween.parallel().tween_property(sprite, "blur", 5.0, t)
	tween.tween_property(sprite, "xpos", 0.5 + 0.05 * side, t).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tween.parallel().tween_property(sprite, "xanchor", 0.5 + 0.05 * side, t).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tween.parallel().tween_property(sprite, "rotate", -angle * side, t).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tween.tween_property(sprite, "rotate", 0.0, t)
	tween.parallel().tween_property(sprite, "alpha", 0.0, t)
	tween.parallel().tween_property(sprite, "zoom", 1.0, t)
	tween.parallel().tween_property(sprite, "xpos", 0.5, t)
	tween.parallel().tween_property(sprite, "xanchor", 0.5, t)


## Put the stage pictures in drawing order: by zorder, then in the order they were shown.
## (Done by reordering, not z_index, so pictures always stay under the text box.)
func _sort_stage() -> void:
	var pictures: Array = stage.get_children().filter(func(n: Node) -> bool: return n is StageSprite)
	var by_order := pictures.duplicate()
	by_order.sort_custom(func(a: StageSprite, b: StageSprite) -> bool:
		if a.zorder != b.zorder:
			return a.zorder < b.zorder
		return pictures.find(a) < pictures.find(b))
	for i in by_order.size():
		stage.move_child(by_order[i], i)


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
			tween.tween_callback(_apply.bind(sprite, step["props"]))
			added = true
			continue
		var trans := _warp_curve(step["warp"])
		var ease := _warp_direction(step["warp"])
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


## linear, ease, easein, easeout, and the named curves: ease_circ, easein_back, easeout_quad ...
func _warp_curve(warp: String) -> Tween.TransitionType:
	if warp == "linear":
		return Tween.TRANS_LINEAR
	var curves := {"quad": Tween.TRANS_QUAD, "cubic": Tween.TRANS_CUBIC, "quart": Tween.TRANS_QUART,
		"quint": Tween.TRANS_QUINT, "expo": Tween.TRANS_EXPO, "circ": Tween.TRANS_CIRC,
		"back": Tween.TRANS_BACK, "elastic": Tween.TRANS_ELASTIC, "bounce": Tween.TRANS_BOUNCE,
		"sine": Tween.TRANS_SINE}
	return curves.get(warp.get_slice("_", 1), Tween.TRANS_SINE)


## Ren'Py's "easein" starts fast and slows down, which Godot calls EASE_OUT (and the reverse).
func _warp_direction(warp: String) -> Tween.EaseType:
	if warp.begins_with("easein"):
		return Tween.EASE_OUT
	if warp.begins_with("easeout"):
		return Tween.EASE_IN
	return Tween.EASE_IN_OUT


## A character's usual placement (config.tag_transform or sprite_positions.json).
## In Ren'Py this transform sits underneath anything the script adds, so its zoom
## is kept apart and multiplied with the script's zoom; its position can be
## replaced by the script's position.
func _apply_usual(sprite: StageSprite, props: Dictionary) -> void:
	var rest := props.duplicate()
	if rest.has("zoom"):
		sprite.base_zoom = float(rest["zoom"])
		rest.erase("zoom")
	_apply(sprite, rest)


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
	var move := _move_of(op.get("with", ""))
	if move.is_empty() or move["in"]:
		sprite.queue_free()     # gone at once; a dissolve or fade is drawn over the whole screen
		return
	var away: Vector2 = Vector2(sprite.xoffset, sprite.yoffset) + move["direction"] * StageSprite.SCREEN
	var tween := create_tween()
	tween.tween_property(sprite, "xoffset", away.x, move["time"])
	tween.parallel().tween_property(sprite, "yoffset", away.y, move["time"])
	tween.tween_callback(sprite.queue_free)


## moveinleft, moveinright ... : the new pictures slide in from off-screen.
func _transition_in(sprites: Array, how: String) -> void:
	var move := _move_of(how)
	if move.is_empty() or not move["in"]:
		return
	for sprite in sprites:
		if not is_instance_valid(sprite):
			continue
		# Slide in from off-screen and stop where the character was placed.
		var rest := Vector2(sprite.xoffset, sprite.yoffset)
		var from: Vector2 = rest + move["direction"] * StageSprite.SCREEN
		sprite.xoffset = from.x
		sprite.yoffset = from.y
		var tween := create_tween()
		tween.tween_property(sprite, "xoffset", rest.x, move["time"])
		tween.parallel().tween_property(sprite, "yoffset", rest.y, move["time"])


## moveinleft / moveoutright / MoveTransition(1.0, leave=offscreenright) ...
## -> {"in": true for enter, "direction": where off-screen, "time": seconds}, or {} for anything else.
func _move_of(how: String) -> Dictionary:
	if MOVE_IN.has(how):
		return {"in": true, "direction": MOVE_IN[how], "time": 0.5}
	if MOVE_OUT.has(how):
		return {"in": false, "direction": MOVE_OUT[how], "time": 0.5}
	var m := RegEx.create_from_string("^MoveTransition\\(\\s*([\\d.]+)\\s*,\\s*(enter|leave)\\s*=\\s*offscreen(left|right|top|bottom)\\s*\\)$").search(how)
	if m:
		var entering := m.get_string(2) == "enter"
		var direction: Vector2 = (MOVE_IN if entering else MOVE_OUT)[("movein" if entering else "moveout") + m.get_string(3)]
		return {"in": entering, "direction": direction, "time": float(m.get_string(1))}
	return {}


# ---------------------------------------------------------------------------
# Whole-screen transitions: dissolve, fade, push, pixellate, vpunch
# ---------------------------------------------------------------------------
#
# How it works, as in Ren'Py: the story changes the pictures straight away, then the
# screen as it looked before (still the last frame drawn) is laid on top and taken away:
#   dissolve / Dissolve(t)      the old screen fades out over the new one
#   fade / Fade(out, hold, in)  to black, wait, back from black   (fadehold = Fade(.5, 1, .5))
#   pushleft / pushright ...    the new screen pushes the old one off (1 second)
#   Pixellate(t, steps)         old screen turns to blocks, new one comes out of them
#   vpunch / hpunch             the screen shakes
# A tap skips to the end. The story waits for the transition, like Ren'Py's `with`.

signal _transition_done
var _transition: Tween
var _transition_layer: CanvasLayer
var _before: TextureRect           # the screen as it was
var _cover: ColorRect              # the black (or other colour) of a fade
var _blocks: ColorRect             # the pixellate effect on the live screen

const PIXELLATE_SHADER := """
shader_type canvas_item;
uniform float block = 1.0;
uniform bool use_screen = false;
uniform sampler2D screen_texture : hint_screen_texture, filter_nearest;
void fragment() {
	vec2 size = use_screen ? 1.0 / SCREEN_PIXEL_SIZE : 1.0 / TEXTURE_PIXEL_SIZE;
	vec2 uv = use_screen ? SCREEN_UV : UV;
	vec2 snapped = (floor(uv * size / block) + 0.5) * block / size;
	COLOR = use_screen ? texture(screen_texture, snapped) : texture(TEXTURE, snapped);
}
"""


## Start the transition named in the script. Returns when it is over (or skipped).
func _screen_transition(how: String) -> void:
	how = transitions.get(how.strip_edges(), how.strip_edges())   # your own `define` names first
	if how == "" or how == "None" or not _move_of(how).is_empty():
		return
	if how in ["vpunch", "hpunch"]:
		_shake(Vector2(0, 10) if how == "vpunch" else Vector2(15, 0))
		return
	var kind := _transition_kind(how)
	if kind.is_empty():
		_warn_once("Transition '%s' is not built yet, so it happens instantly." % how)
		return
	if DisplayServer.get_name() == "headless":
		return    # nothing is drawn when testing without a screen
	_end_transition()
	_make_transition_layer()
	var picture := get_viewport().get_texture().get_image()
	if picture == null or picture.is_empty():
		return
	_before.texture = ImageTexture.create_from_image(picture)
	_before.position = Vector2.ZERO
	_before.modulate.a = 1.0
	_before.material = null
	_before.show()
	var tween := create_tween()
	_transition = tween
	match kind["type"]:
		"dissolve":
			tween.tween_property(_before, "modulate:a", 0.0, kind["time"])
		"fade":
			_cover.color = kind["color"]
			_cover.color.a = 0.0
			_cover.show()
			tween.tween_property(_cover, "color:a", 1.0, kind["out"])
			tween.tween_callback(_before.hide)
			tween.tween_interval(kind["hold"])
			tween.tween_property(_cover, "color:a", 0.0, kind["in"])
		"push":
			var away: Vector2 = kind["direction"] * StageSprite.SCREEN
			position = -away
			tween.tween_property(_before, "position", away, 1.0).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
			tween.parallel().tween_property(self, "position", Vector2.ZERO, 1.0).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		"pixellate":
			var shader := Shader.new()
			shader.code = PIXELLATE_SHADER
			var on_before := ShaderMaterial.new()
			on_before.shader = shader
			_before.material = on_before
			var on_screen := ShaderMaterial.new()
			on_screen.shader = shader
			on_screen.set_shader_parameter("use_screen", true)
			_blocks.material = on_screen
			var steps: int = kind["steps"]
			var each: float = kind["time"] / 2.0 / steps
			for i in range(1, steps + 1):     # the old screen breaks into bigger and bigger blocks
				tween.tween_callback(on_before.set_shader_parameter.bind("block", pow(2.0, i)))
				tween.tween_interval(each)
			tween.tween_callback(func() -> void:
				_before.hide()
				_blocks.show())
			for i in range(steps, 0, -1):     # the new one comes back out of them
				tween.tween_callback(on_screen.set_shader_parameter.bind("block", pow(2.0, i)))
				tween.tween_interval(each)
	tween.finished.connect(_end_transition)
	await _transition_done


## dissolve, Dissolve(1.0), fade, fadehold, Fade(2.0, 0.5, 2.0[, color="#fff"]), pushleft ..., Pixellate(2.0, 5)
func _transition_kind(how: String) -> Dictionary:
	var numbers: Array = []
	for found in RegEx.create_from_string("-?\\d+(\\.\\d+)?").search_all(how.get_slice("color", 0)):
		numbers.append(float(found.get_string()))
	var name := how.get_slice("(", 0).strip_edges()
	match name:
		"dissolve":
			return {"type": "dissolve", "time": 0.5}
		"Dissolve":
			return {"type": "dissolve", "time": numbers[0] if numbers.size() > 0 else 0.5}
		"fade":
			return {"type": "fade", "out": 0.5, "hold": 0.0, "in": 0.5, "color": Color.BLACK}
		"fadehold":
			return {"type": "fade", "out": 0.5, "hold": 1.0, "in": 0.5, "color": Color.BLACK}
		"Fade":
			var colour := Color.BLACK
			var c := RegEx.create_from_string("color\\s*=\\s*[\"']([^\"']+)[\"']").search(how)
			if c:
				colour = Color(c.get_string(1))
			if numbers.size() >= 3:
				return {"type": "fade", "out": numbers[0], "hold": numbers[1], "in": numbers[2], "color": colour}
			if numbers.size() == 1:
				return {"type": "fade", "out": numbers[0], "hold": 0.0, "in": numbers[0], "color": colour}
		"pushleft", "pushright", "pushup", "pushdown":
			var direction := {"pushleft": Vector2(-1, 0), "pushright": Vector2(1, 0),
				"pushup": Vector2(0, -1), "pushdown": Vector2(0, 1)}
			return {"type": "push", "direction": direction[name]}
		"Pixellate", "pixellate":
			return {"type": "pixellate", "time": numbers[0] if numbers.size() > 0 else 1.0,
				"steps": int(numbers[1]) if numbers.size() > 1 else 5}
	return {}


func _end_transition() -> void:
	if _transition == null:
		return
	if _transition.is_valid():
		_transition.kill()
	_transition = null
	position = Vector2.ZERO
	_before.hide()
	_before.material = null
	_cover.hide()
	_blocks.hide()
	_transition_done.emit()


func _make_transition_layer() -> void:
	if _transition_layer != null:
		return
	_transition_layer = CanvasLayer.new()
	_transition_layer.layer = 2       # above the game and its menus
	add_child(_transition_layer)
	_blocks = ColorRect.new()
	_before = TextureRect.new()
	_before.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_cover = ColorRect.new()
	for node: Control in [_blocks, _before, _cover]:
		node.size = StageSprite.SCREEN
		node.mouse_filter = Control.MOUSE_FILTER_IGNORE
		node.hide()
		_transition_layer.add_child(node)


## vpunch / hpunch: shake the screen for a moment (Ren'Py: 10 pixels, about a quarter second).
func _shake(amount: Vector2) -> void:
	var tween := create_tween()
	for i in 3:
		tween.tween_property(self, "position", amount, 0.045)
		tween.tween_property(self, "position", -amount, 0.045)
	tween.tween_property(self, "position", Vector2.ZERO, 0.0)


# ---------------------------------------------------------------------------
# Layout mode (F2 while playing from the Godot editor)
# ---------------------------------------------------------------------------

## Drag characters into place by hand. The story waits while this is on.
##   drag             move a character
##   arrow keys       nudge by 1 pixel (hold Shift for 10)
##   + / -            bigger / smaller (the mouse wheel works too)
##   F2 again         save to res://sprite_positions.json and carry on with the story
## Only works when running from the editor, so players never see it.
func set_layout_mode(on: bool) -> void:
	if on and not OS.has_feature("editor"):
		return
	_layout_mode = on
	if on:
		if _layout_note == null:
			_layout_note = Label.new()
			_layout_note.position = Vector2(24, 140)
			_layout_note.z_index = 50
			_layout_note.add_theme_font_size_override("font_size", 30)
			_layout_note.add_theme_color_override("font_color", Color.WHITE)
			_layout_note.add_theme_color_override("font_outline_color", Color.BLACK)
			_layout_note.add_theme_constant_override("outline_size", 10)
			add_child(_layout_note)
		_layout_note.show()
		_layout_show_selected()
	else:
		if _layout_note != null:
			_layout_note.hide()
		_layout_dragging = false
		save_sprite_positions()


func save_sprite_positions() -> void:
	var file := FileAccess.open(POSITIONS_FILE, FileAccess.WRITE)
	if file == null:
		push_warning("Could not write %s" % POSITIONS_FILE)
		return
	file.store_string(JSON.stringify(sprite_positions, "\t", true))
	print("Saved character positions to %s:\n%s" % [POSITIONS_FILE, JSON.stringify(sprite_positions, "  ", true)])


func _layout_input(event: InputEvent) -> void:
	var mouse := stage.get_local_mouse_position()
	if event is InputEventMouseButton and event.pressed:
		match event.button_index:
			MOUSE_BUTTON_LEFT:
				_layout_selected = _sprite_at(mouse)
				_layout_dragging = _layout_selected != null
				_layout_last_mouse = mouse
			MOUSE_BUTTON_WHEEL_UP:
				_layout_zoom(1.02)
			MOUSE_BUTTON_WHEEL_DOWN:
				_layout_zoom(1.0 / 1.02)
		_layout_show_selected()
	elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		_layout_dragging = false
	elif event is InputEventMouseMotion and _layout_dragging:
		_layout_move(mouse - _layout_last_mouse)
		_layout_last_mouse = mouse
	elif event is InputEventKey and event.pressed:
		var step := 10.0 if event.shift_pressed else 1.0
		match event.keycode:
			KEY_LEFT: _layout_move(Vector2(-step, 0))
			KEY_RIGHT: _layout_move(Vector2(step, 0))
			KEY_UP: _layout_move(Vector2(0, -step))
			KEY_DOWN: _layout_move(Vector2(0, step))
			KEY_EQUAL, KEY_PLUS, KEY_KP_ADD: _layout_zoom(1.02)
			KEY_MINUS, KEY_KP_SUBTRACT: _layout_zoom(1.0 / 1.02)


## The character under this point: the one drawn on top wins.
func _sprite_at(point: Vector2) -> StageSprite:
	var found: StageSprite = null
	for sprite: StageSprite in _sprites.values():
		if not Rect2(sprite.position, sprite.size).has_point(point):
			continue
		if found == null or sprite.get_index() > found.get_index():
			found = sprite
	return found


## Left-right is kept as xalign (so it stays right on any screen); up-down as yoffset in pixels.
func _layout_move(delta: Vector2) -> void:
	var sprite := _layout_selected
	if sprite == null:
		return
	var room := StageSprite.SCREEN.x - sprite.size.x
	if absf(room) > 1.0:
		var left := sprite.position.x + delta.x - sprite.xoffset
		_apply(sprite, {"xalign": snappedf(left / room, 0.001)})
	else:
		sprite.xoffset += delta.x
	sprite.yoffset = roundf(sprite.yoffset + delta.y)
	_layout_remember(sprite)


func _layout_zoom(factor: float) -> void:
	if _layout_selected == null:
		return
	_layout_selected.base_zoom = snappedf(_layout_selected.base_zoom * factor, 0.005)
	_layout_remember(_layout_selected)


func _layout_remember(sprite: StageSprite) -> void:
	var tag := ""
	for key in _sprites:
		if _sprites[key] == sprite:
			tag = key
	var spot := {"xalign": sprite.xpos, "yoffset": sprite.yoffset, "zoom": sprite.base_zoom}
	if sprite.xoffset != 0.0:
		spot["xoffset"] = sprite.xoffset
	sprite_positions[tag] = spot
	_layout_show_selected()


func _layout_show_selected() -> void:
	if _layout_note == null:
		return
	var text := "LAYOUT MODE   drag a character · arrows nudge (Shift = 10) · +/- size · F2 save\n"
	if _layout_selected == null or not is_instance_valid(_layout_selected):
		text += "Click a character to pick it."
	else:
		text += "%s   xalign %.3f   yoffset %d   zoom %.3f" % [_layout_selected.image_name,
			_layout_selected.xpos, int(_layout_selected.yoffset), _layout_selected.base_zoom]
	_layout_note.text = text


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
	# The menu button is part of the day display in Ren'Py, so it hides with it.
	menu_button.visible = State.day_display == true
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
