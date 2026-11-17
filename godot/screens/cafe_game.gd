extends Control
## Cafe game - carry each dish to the table that ordered it (`screen cafe_game`).
##
## The three orders appear above the tables for a moment and fade. Drag a dish
## from the bottom of the screen onto a table. Right table: a tip. Wrong table:
## the dish slides back and a little is taken off the tips.
##
## The numbers (TIP_MIN, TIP_MAX, TIP_PENALTY, TABLE_X, the lines customers say)
## are read from your `define` lines in screens_cafe.rpy, so change them there.
## State.setup_cafe_round() has already shuffled the round before this opens.

signal closed(action: Dictionary)

# In the scene this node has Z Index 2, so it covers the day display (Z Index 1),
# the same as `zorder 2` on the Ren'Py screen.

const SCREEN := Vector2(1920, 1080)
const DISH_SIZE := Vector2(640, 315)
const TABLE_Y := 0.55
const ORDER_X := [0.25, 0.55, 0.785]
const GOOD := Color("2e7d32")
const BAD := Color("990000")

@onready var tutorial: Control = $Tutorial
@onready var kirako: TextureRect = $Tutorial/Kirako
@onready var table: TextureRect = $Table
@onready var bubble: Control = $Bubble
@onready var tips_label: Label = $Tips
@onready var text_font: Font = $Bubble/Text.get_theme_font("font")

var _dishes: Array = []      # the three draggable dishes, in menu order
var _targets: Array = []     # Rect2 of each table's drop spot, in menu order
var _homes: Array = []       # where each dish starts
var _held: TextureRect = null


func _ready() -> void:
	var teaching: bool = State.tutorial_mode == true
	tutorial.visible = teaching
	table.visible = teaching
	bubble.visible = false
	if teaching:
		_run_tutorial()

	var menu: Array = State.cafe_menu
	for i in 3:
		var texture: Texture2D = load(State.asset("images/cafe/%s.png" % menu[i]))

		# The drop spot is the dish at one tenth of its size, on the table.
		var spot_size: Vector2 = texture.get_size() * 0.1
		_targets.append(Rect2(Vector2(State.TABLE_X[i], TABLE_Y) * (SCREEN - spot_size), spot_size))

		var dish := TextureRect.new()
		dish.texture = texture
		dish.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		dish.size = DISH_SIZE
		dish.position = Vector2(State.customer_table[i] * (SCREEN.x - DISH_SIZE.x), SCREEN.y - DISH_SIZE.y)
		dish.gui_input.connect(_on_dish_input.bind(dish))
		add_child(dish)
		_dishes.append(dish)
		_homes.append(dish.position)

		_show_order(menu[i] + State.customer_order[i], ORDER_X[i], float(State.order_times[i]))
	_update_tips()


## Kirako explains, then steps out of the way after four seconds.
func _run_tutorial() -> void:
	await get_tree().create_timer(0.6).timeout
	bubble.show()
	await get_tree().create_timer(3.4).timeout
	var leave := create_tween()
	leave.tween_property(kirako, "position:x", -SCREEN.x, 0.5).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN)
	await get_tree().create_timer(0.1).timeout
	bubble.hide()


# ---------------------------------------------------------------------------
# Dragging
# ---------------------------------------------------------------------------

func _on_dish_input(event: InputEvent, dish: TextureRect) -> void:
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		if event.pressed:
			_held = dish
			dish.move_to_front()
		elif _held == dish:
			_held = null
			_dropped(dish)
	elif event is InputEventMouseMotion and _held == dish:
		dish.position += event.relative


## The Godot version of dish_dropped() in screens_cafe.rpy.
func _dropped(dish: TextureRect) -> void:
	var dish_index := _dishes.find(dish)
	var table_index := _table_under(dish)

	# Let go over empty space: send it back, no penalty
	if table_index == -1:
		_send_home(dish)
		return

	if table_index == dish_index:
		# Right table: the dish shrinks onto the table and stays there
		dish.mouse_filter = Control.MOUSE_FILTER_IGNORE
		dish.size = DISH_SIZE * 0.2
		dish.position = _targets[table_index].position
		State.served_food += 1
		var tip := randi_range(State.TIP_MIN, State.TIP_MAX)
		State.shift_tips += tip
		_show_feedback(table_index, State.RIGHT_LINES.pick_random(), "+%d" % tip, GOOD)

		# Shift finished: tips can't end below zero, so money never goes down
		if State.served_food == 3:
			State.shift_tips = max(0, State.shift_tips)
			_finish()
	else:
		# Wrong table
		_send_home(dish)
		State.shift_tips -= State.TIP_PENALTY
		_show_feedback(table_index, State.WRONG_LINES.pick_random(), "-%d" % State.TIP_PENALTY, BAD)
	_update_tips()


## Which table the dish was let go over: the one it covers most. -1 for none.
func _table_under(dish: TextureRect) -> int:
	var dish_rect := Rect2(dish.position, dish.size)
	var best := -1
	var best_area := 0.0
	for i in _targets.size():
		var area: float = dish_rect.intersection(_targets[i]).get_area()
		if area > best_area:
			best = i
			best_area = area
	return best


func _send_home(dish: TextureRect) -> void:
	create_tween().tween_property(dish, "position", _homes[_dishes.find(dish)], 0.2)


## All three served: wait a moment so the last "Thank you!" is visible, then move on.
func _finish() -> void:
	await get_tree().create_timer(1.5).timeout
	closed.emit({"jump": "re_explain_cafegame" if State.tutorial_mode == true else "after_work_cafe"})


# ---------------------------------------------------------------------------
# Words that pop up
# ---------------------------------------------------------------------------

func _update_tips() -> void:
	tips_label.text = "Tips: %d" % State.shift_tips


## A customer's order: waits `delay` seconds, rises in, stays, fades out (transform order_pop).
func _show_order(text: String, xalign: float, delay: float) -> void:
	var label := _outlined(text, 40, State.ORDER_COLOR, 350.0)
	label.position = Vector2(xalign, 0.25) * (SCREEN - label.size)
	_pop(label, delay, 0.4, 1.6, 1.0)


## What the customer says when a dish arrives, with the tip under it (screen cafe_feedback).
func _show_feedback(table_index: int, line: String, tip_text: String, color: Color) -> void:
	var box := Control.new()
	box.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var words := _outlined(line, 40, color)
	var tip := _outlined(tip_text, 52, color)
	box.size = Vector2(max(words.size.x, tip.size.x), words.size.y + 4 + tip.size.y)
	words.position = Vector2((box.size.x - words.size.x) / 2.0, 0)
	tip.position = Vector2((box.size.x - tip.size.x) / 2.0, words.size.y + 4)
	box.add_child(words)
	box.add_child(tip)
	box.position = Vector2(State.TABLE_X[table_index], 0.40) * (SCREEN - box.size)
	_pop(box, 0.0, 0.2, 0.9, 0.4)


## Rise in, hold, drift up and fade, then remove itself.
func _pop(node: Control, delay: float, rise: float, hold: float, fade: float) -> void:
	add_child(node)
	var rest_y := node.position.y
	node.modulate.a = 0.0
	node.position.y = rest_y + 20
	var tween := create_tween()
	tween.tween_interval(delay)
	tween.tween_property(node, "modulate:a", 1.0, rise).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_SINE)
	tween.parallel().tween_property(node, "position:y", rest_y, rise).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_SINE)
	tween.tween_interval(hold)
	tween.tween_property(node, "modulate:a", 0.0, fade).set_ease(Tween.EASE_IN).set_trans(Tween.TRANS_SINE)
	tween.parallel().tween_property(node, "position:y", rest_y - 20, fade).set_ease(Tween.EASE_IN).set_trans(Tween.TRANS_SINE)
	tween.tween_callback(node.queue_free)


## Text with a white outline, sized to fit its words (wrapping at `max_width` if given).
func _outlined(text: String, font_size: int, color: Variant, max_width: float = -1.0) -> Label:
	var label := Label.new()
	label.text = text
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.add_theme_font_override("font", text_font)
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", Color(color))
	label.add_theme_color_override("font_outline_color", Color.WHITE)
	label.add_theme_constant_override("outline_size", 8)
	if max_width > 0.0:
		label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.size = text_font.get_multiline_string_size(text, HORIZONTAL_ALIGNMENT_CENTER, max_width, font_size) + Vector2(8, 0)
	return label


## Used by tests/autoplay: one wrong table first, then every dish to its own table.
func autoplay() -> void:
	await get_tree().create_timer(5.0 if State.tutorial_mode == true else 1.0).timeout
	_carry(0, 1)
	for i in 3:
		await get_tree().create_timer(0.8).timeout
		_carry(i, i)


func _carry(dish_index: int, table_index: int) -> void:
	var dish: TextureRect = _dishes[dish_index]
	dish.position = _targets[table_index].get_center() - dish.size / 2.0
	_dropped(dish)
