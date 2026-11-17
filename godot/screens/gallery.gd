extends Control
## Gallery - one page per love interest: bio, quote and the cutscenes unlocked so far.
##
## Nothing about the characters is typed here. The converter reads it from screens.rpy:
##   State.characters   the `characters` table (name, bio, quote, pictures, cutscenes)
##   gallery            the gallery.button / gallery.image / gallery.condition lines
## So edit the gallery in Ren'Py and re-run the converter.

signal closed(action: Dictionary)

const SCREEN := Vector2(1920, 1080)
const ART := "gui/gallery/"
const TABS := ["merchant", "fighter", "soldier", "doctor", "musician"]   # top to bottom

var _buttons: Dictionary = {}     # cutscene name -> {"images": [...], "conditions": [...]}
var _images: Dictionary = {}      # picture name -> {"path": ...}
var _page: Control                # everything that changes with the character
var _viewer: TextureRect          # the full-screen cutscene picture
var _queue: Array = []            # pictures still to show in the viewer


func _ready() -> void:
	theme = UITheme.get_theme()
	z_index = 6
	var data: Dictionary = State.load_json("res://story/game_data.json")
	_images = data.get("images", {})
	for button in data.get("gallery", []):
		_buttons[button["name"]] = button

	add_child(_picture(ART + "gallery_bg.png", Rect2(Vector2.ZERO, SCREEN)))
	_page = Control.new()
	_page.set_anchors_preset(Control.PRESET_FULL_RECT)
	_page.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_page)

	# Side tabs. Characters without a gallery entry yet are shown faded.
	for i in TABS.size():
		var who: String = TABS[i]
		var tab := _button(ART + "gallery_tab_%s.png" % who, Rect2(-38, 192 + i * 170, 200, 160))
		if State.characters.has(who):
			tab.pressed.connect(show_character.bind(who))
		else:
			tab.modulate.a = 0.45
			tab.disabled = true
		add_child(tab)

	var back := _button("images/back.png", Rect2(0, 0, 167, 167))
	back.pressed.connect(func() -> void: closed.emit({}))
	add_child(back)

	_viewer = _picture(null, Rect2(Vector2.ZERO, SCREEN))
	_viewer.mouse_filter = Control.MOUSE_FILTER_STOP
	_viewer.gui_input.connect(_on_viewer_input)
	_viewer.hide()
	add_child(_viewer)

	show_character(State.current_char)


func show_character(who: String) -> void:
	State.current_char = who
	var c: Dictionary = State.characters[who]
	for child in _page.get_children():
		child.queue_free()

	# The character
	var portrait: Texture2D = load(State.asset(c["image"]))
	var portrait_size: Vector2 = portrait.get_size() * 0.6
	_page.add_child(_picture(portrait, Rect2(Vector2(0.5, 0.2) * (SCREEN - portrait_size), portrait_size)))

	# Bio (added after the portrait so the words always sit on top of it)
	var bio := VBoxContainer.new()
	bio.add_theme_constant_override("separation", 18)
	bio.position = Vector2(270, 290)
	bio.custom_minimum_size = Vector2(380, 0)
	# Each fact sits under its label, as in the Ren'Py screen, so it stays clear of wide sleeves.
	for line in [c["bio"], c["bio2"], "Favorite food:\n" + c["favorite"],
			"Occupation:\n" + c["occupation"], "Height:\n" + c["height"]]:
		var label := Label.new()
		label.text = line
		label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		label.custom_minimum_size = Vector2(380, 0)
		label.add_theme_font_size_override("font_size", 34)
		bio.add_child(label)
	_page.add_child(bio)

	# Name
	_page.add_child(_picture(ART + "gallery_name.png", Rect2(564, 847, 792, 188)))
	var name_label := _text(c["name"], 100, Rect2(564, 857, 792, 188))
	name_label.add_theme_font_override("font", load(State.asset("Staatliches-Regular.ttf")))
	_page.add_child(name_label)

	# Quote
	_page.add_child(_picture(ART + "gallery_quote.png", Rect2(1254, 0, 666, 434)))
	_page.add_child(_text(c["quote"], 44, Rect2(1368, 70, 420, 320)))

	# Cutscenes: a preview if unlocked, a lock if not
	_page.add_child(_picture(ART + "cutscene_frame.png", Rect2(1314, 407, 606, 673)))
	var names: Array = c["cutscenes"]
	for i in names.size():
		var unlocked := is_unlocked(names[i])
		var art: String = c["cutscene_previews"][i] if unlocked else "images/locked.png"
		var size := Vector2(461, 259) if unlocked else Vector2(225, 225)
		var spot := Vector2(1401 + (461 - size.x) / 2.0, 461 + i * 309 + (259 - size.y) / 2.0)
		var preview := _button(art, Rect2(spot, size))
		preview.disabled = not unlocked
		preview.pressed.connect(view_cutscene.bind(names[i]))
		_page.add_child(preview)


## Ren'Py's rule: a gallery button opens when all of its conditions are true.
## A button with no condition is always open.
func is_unlocked(cutscene: String) -> bool:
	for condition in _buttons.get(cutscene, {}).get("conditions", []):
		if not State.evaluate(condition):
			return false
	return _buttons.has(cutscene)


## Show a cutscene's pictures full screen, one tap each.
func view_cutscene(cutscene: String) -> void:
	_queue = _buttons[cutscene]["images"].duplicate()
	_next_picture()


func _next_picture() -> void:
	if _queue.is_empty():
		_viewer.hide()
		return
	var entry: Dictionary = _images.get(_queue.pop_front(), {})
	_viewer.texture = load(State.asset(entry.get("path", "")))
	_viewer.show()


func _on_viewer_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		_next_picture()


func _picture(art: Variant, rect: Rect2) -> TextureRect:
	var picture := TextureRect.new()
	picture.texture = load(State.asset(art)) if art is String else art
	picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	picture.position = rect.position
	picture.size = rect.size
	picture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return picture


func _button(art: String, rect: Rect2) -> TextureButton:
	var button := TextureButton.new()
	button.texture_normal = load(State.asset(art))
	button.ignore_texture_size = true
	button.stretch_mode = TextureButton.STRETCH_SCALE
	button.position = rect.position
	button.size = rect.size
	# A phone has no hover, so nudge the button while it is pressed instead.
	button.button_down.connect(func() -> void: button.position.x = rect.position.x + 15)
	button.button_up.connect(func() -> void: button.position.x = rect.position.x)
	return button


func _text(words: String, font_size: int, rect: Rect2) -> Label:
	var label := Label.new()
	label.text = words
	label.position = rect.position
	label.size = rect.size
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.add_theme_font_size_override("font_size", font_size)
	return label
