extends Control
## Placeholder - stands in for any Ren'Py screen that has no Godot scene yet,
## so the story can still be played from end to end.
## It lists the labels the real screen's buttons jump to (read from the .rpy
## by the converter) and lets you pick one.

signal closed(action: Dictionary)

var screen_name := ""


func _ready() -> void:
	var info: Dictionary = State.load_json("res://story/game_data.json").get("screens", {}).get(screen_name, {})
	var font: Font = load("res://assets/game/Quicksand_Bold.otf")

	var shade := ColorRect.new()
	shade.color = Color(0.1, 0.1, 0.15, 0.85)
	shade.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(shade)

	var column := VBoxContainer.new()
	column.set_anchors_preset(Control.PRESET_FULL_RECT)
	column.alignment = BoxContainer.ALIGNMENT_CENTER
	column.add_theme_constant_override("separation", 16)
	add_child(column)

	var title := Label.new()
	title.text = "Screen \"%s\" is not built yet.\nChoose how to leave it:" % screen_name
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_font_override("font", font)
	title.add_theme_font_size_override("font_size", 44)
	column.add_child(title)

	var grid := GridContainer.new()
	grid.columns = 3
	grid.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	column.add_child(grid)
	for label in info.get("jumps", []):
		grid.add_child(_exit_button("Jump: " + label, {"jump": label}, font))
	if info.get("returns", false) or info.get("jumps", []).is_empty():
		grid.add_child(_exit_button("Return", {}, font))


func _exit_button(text: String, action: Dictionary, font: Font) -> Button:
	var button := Button.new()
	button.text = text
	button.custom_minimum_size = Vector2(520, 80)
	button.add_theme_font_override("font", font)
	button.add_theme_font_size_override("font_size", 32)
	button.pressed.connect(func() -> void: closed.emit(action))
	return button
