class_name UITheme
## The look of the menus: Godot's own buttons, sliders and panels, dressed in the
## game's fonts and colours. Change a colour or size here and every menu follows.

const CREAM := Color("f0e3ca")
const INK := Color("3d3f4f")       # gui.text_color
const ACCENT := Color("990000")    # gui.accent_color
const FADED := Color("3d3f4f66")

static var _theme: Theme


static func get_theme() -> Theme:
	if _theme != null:
		return _theme
	var body: Font = load(State.asset("Quicksand_Bold.otf"))
	var display: Font = load(State.asset("Staatliches-Regular.ttf"))
	var theme := Theme.new()
	theme.default_font = body
	theme.default_font_size = 38

	theme.set_color("font_color", "Label", INK)

	# Buttons: plain text that turns red when pressed or chosen.
	theme.set_font("font", "Button", display)
	theme.set_font_size("font_size", "Button", 60)
	theme.set_color("font_color", "Button", INK)
	theme.set_color("font_hover_color", "Button", ACCENT)
	theme.set_color("font_pressed_color", "Button", ACCENT)
	theme.set_color("font_hover_pressed_color", "Button", ACCENT)
	theme.set_color("font_focus_color", "Button", INK)
	theme.set_color("font_disabled_color", "Button", FADED)
	for state in ["normal", "hover", "pressed", "disabled", "focus"]:
		theme.set_stylebox(state, "Button", _box(Color.TRANSPARENT, 0, 16, 6))

	# Panels: cream cards.
	theme.set_stylebox("panel", "PanelContainer", _box(Color(CREAM, 0.96), 24, 48, 40))

	# Sliders: a thick track and a round handle big enough for a thumb.
	theme.set_stylebox("slider", "HSlider", _box(FADED, 10, 0, 10))
	theme.set_stylebox("grabber_area", "HSlider", _box(ACCENT, 10, 0, 10))
	theme.set_stylebox("grabber_area_highlight", "HSlider", _box(ACCENT, 10, 0, 10))
	var handle := _circle(56, ACCENT)
	for icon in ["grabber", "grabber_highlight", "grabber_disabled"]:
		theme.set_icon(icon, "HSlider", handle)

	_theme = theme
	return theme


## A small pill-shaped button for on/off and pick-one settings.
static func pill(text: String) -> Button:
	var button := Button.new()
	button.text = text
	button.toggle_mode = true
	button.focus_mode = Control.FOCUS_NONE
	button.custom_minimum_size = Vector2(170, 72)
	button.add_theme_font_size_override("font_size", 40)
	button.add_theme_stylebox_override("normal", _box(Color(INK, 0.12), 36, 28, 8))
	button.add_theme_stylebox_override("hover", _box(Color(INK, 0.12), 36, 28, 8))
	button.add_theme_stylebox_override("pressed", _box(ACCENT, 36, 28, 8))
	button.add_theme_color_override("font_pressed_color", CREAM)
	button.add_theme_color_override("font_hover_pressed_color", CREAM)
	button.add_theme_color_override("font_hover_color", INK)
	return button


static func _box(color: Color, radius: int, margin_x: int, margin_y: int) -> StyleBoxFlat:
	var box := StyleBoxFlat.new()
	box.bg_color = color
	box.set_corner_radius_all(radius)
	box.content_margin_left = margin_x
	box.content_margin_right = margin_x
	box.content_margin_top = margin_y
	box.content_margin_bottom = margin_y
	return box


static func _circle(diameter: int, color: Color) -> ImageTexture:
	var image := Image.create(diameter, diameter, false, Image.FORMAT_RGBA8)
	var center := Vector2(diameter, diameter) / 2.0
	for x in diameter:
		for y in diameter:
			var edge := diameter / 2.0 - Vector2(x + 0.5, y + 0.5).distance_to(center)
			image.set_pixel(x, y, Color(color, clamp(edge, 0.0, 1.0)))
	return ImageTexture.create_from_image(image)
