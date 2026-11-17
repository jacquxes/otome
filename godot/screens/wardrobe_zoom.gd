extends Control
## Wardrobe, full-size view (`screen wardrobe_zoom`): Naomi at full size.
## Drag to look her up and down. Nothing can be changed here.

signal closed(action: Dictionary)

const SCREEN := Vector2(1920, 1080)
const FIGURE := Vector2(2150, 4299)

var _figure: Control
var _pressed := false


func _ready() -> void:
	z_index = 40
	var shade := ColorRect.new()
	shade.color = Color(0.16, 0.12, 0.1, 0.8)
	shade.set_anchors_preset(Control.PRESET_FULL_RECT)
	shade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(shade)

	_figure = Control.new()
	_figure.size = FIGURE
	_figure.position = Vector2((SCREEN.x - FIGURE.x) / 2.0, 0)
	_figure.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_figure)

	# The same layers, in the same order, as the Ren'Py screen. [picture, x align, y]
	# A y of -1 means "at the bottom".
	_layer("base_torso", 0.5, 899)
	if State.naomi_accessories_left == "hand_parasol":
		_layer("hand_parasol", 1.0, -1)
	_layer("base_feet", 0.5, -1)
	_layer(State.naomi_hair, 0.5, 0)
	for makeup in [["cheek", State.naomi_cheek, 400], ["eye", State.naomi_eye, 312], ["lip", State.naomi_lip, 640]]:
		if makeup[1] != "":
			_layer("makeup_%s%s" % [makeup[0], makeup[1]], 0.5, makeup[2])
	if State.naomi_shoes != "":
		_layer(State.naomi_shoes, 0.5, -1)
	if State.naomi_dress != "":
		_layer(State.naomi_dress, 0.5, 740)
	if State.naomi_accessories_right != "":
		_layer(State.naomi_accessories_right, 0.0, 2000)

	var zoom_out := TextureButton.new()
	zoom_out.texture_normal = load(State.asset("gui/zoomout_idle.png"))
	zoom_out.ignore_texture_size = true
	zoom_out.stretch_mode = TextureButton.STRETCH_SCALE
	zoom_out.position = Vector2(172, 880)
	zoom_out.size = Vector2(200, 200)
	zoom_out.pressed.connect(func() -> void: closed.emit({}))
	add_child(zoom_out)


func _layer(picture_name: String, xalign: float, y: float) -> void:
	var picture := TextureRect.new()
	picture.texture = load(State.asset("images/naomi/%s.png" % picture_name))
	picture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var art_size: Vector2 = picture.texture.get_size()
	picture.position = Vector2(xalign * (FIGURE.x - art_size.x), FIGURE.y - art_size.y if y < 0 else y)
	_figure.add_child(picture)


func _gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		_pressed = event.pressed
	elif event is InputEventMouseMotion and _pressed:
		_figure.position = (_figure.position + event.relative).clamp(SCREEN - FIGURE, Vector2.ZERO)
