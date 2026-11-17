extends Control
## Cafe menu - choose three items for today's menu (`screen cafe_menu` in screens_cafe.rpy).
## Tap an item to add or remove it. Confirm lights up once three are chosen and
## starts the serving game.

signal closed(action: Dictionary)

# In the scene this node has Z Index 2, so it covers the day display (Z Index 1),
# the same as `zorder 2` on the Ren'Py screen.

const IDLE := Color("707070")          # gui.idle_color
const CHOSEN := Color("990000")        # text_selected_color
const DISABLED := Color("7070707f")    # gui.insensitive_color

@onready var tutorial: Control = $Tutorial
@onready var table: TextureRect = $Table
@onready var bubble: Control = $Bubble
@onready var items: VBoxContainer = $Items
@onready var confirm: Button = $Items/Confirm

var _buttons: Dictionary = {}  # item name -> Button


func _ready() -> void:
	# Kirako, the table and her speech bubble only appear the first time.
	var teaching: bool = State.tutorial_mode == true
	tutorial.visible = teaching
	table.visible = teaching
	bubble.visible = false
	if teaching:
		get_tree().create_timer(0.6).timeout.connect(bubble.show)

	for item: String in State.unlocked_menu:
		var button := _text_button(item.capitalize(), 72)
		button.pressed.connect(_toggle.bind(item))
		items.add_child(button)
		_buttons[item] = button
	items.move_child(confirm, -1)
	confirm.pressed.connect(func() -> void: closed.emit({"jump": "cafe_game"}))
	_refresh()


func _toggle(item: String) -> void:
	var menu: Array = State.cafe_menu
	if item in menu:
		menu.erase(item)
	elif menu.size() < 3:
		menu.append(item)
	_refresh()


func _refresh() -> void:
	var menu: Array = State.cafe_menu
	for item in _buttons:
		var button: Button = _buttons[item]
		var chosen: bool = item in menu
		button.disabled = not chosen and menu.size() >= 3
		_color(button, CHOSEN if chosen else IDLE)
	confirm.disabled = menu.size() != 3
	_color(confirm, IDLE)


func _text_button(text: String, font_size: int) -> Button:
	var button := Button.new()
	button.text = text
	button.flat = true
	button.focus_mode = Control.FOCUS_NONE
	button.alignment = HORIZONTAL_ALIGNMENT_LEFT
	button.add_theme_font_override("font", confirm.get_theme_font("font"))
	button.add_theme_font_size_override("font_size", font_size)
	return button


func _color(button: Button, color: Color) -> void:
	for state in ["font_color", "font_focus_color"]:
		button.add_theme_color_override(state, color)
	for state in ["font_hover_color", "font_pressed_color", "font_hover_pressed_color"]:
		button.add_theme_color_override(state, CHOSEN)
	button.add_theme_color_override("font_disabled_color", DISABLED)


## Used by tests/autoplay: choose the first three items and confirm.
func autoplay() -> void:
	for item: String in State.unlocked_menu.slice(0, 3):
		await get_tree().create_timer(0.3).timeout
		_toggle(item)
	await get_tree().create_timer(0.8).timeout
	closed.emit({"jump": "cafe_game"})
