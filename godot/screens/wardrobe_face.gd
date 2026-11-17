extends Control
## Wardrobe, dresser view (`screen wardrobe_face`): a close-up of Naomi for hats.
## Drag a hat from the dresser onto her head to wear it. Drag it off (or tap it)
## to go back to her plain hair. The makeup box opens the makeup view.
##
## Hats she owns:  wardrobe_hair  = {"hair_hat": [x, y], ...}  (where each sits on the dresser)
## Hat she wears:  naomi_hair     ("hair_base" = none)

signal closed(action: Dictionary)

const FACE_CUT := Rect2(600, 100, 899, 899)     # the part of a hair picture shown in close-up
const HEAD := Rect2(0, 0, 899, 899)             # where a hat must be let go to be worn
const CLOSE_UP := Vector2(-600, -100)           # full-size Naomi pictures are shifted by this

var _head: Control
var _hats: Dictionary = {}   # hat name -> DragItem


func _ready() -> void:
	z_index = 40
	add_child(_picture("images/bg wardrobe.png", Vector2(-300, -200)))
	add_child(_picture("images/naomi/base_torso.png", Vector2(-600, 799)))

	var makeup := TextureButton.new()
	makeup.texture_normal = load(State.asset("images/wardrobe/makeup.png"))
	makeup.position = Vector2(1049, 652)
	makeup.pressed.connect(_open_makeup)
	add_child(makeup)

	_head = Control.new()
	_head.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_head)

	var owned: Dictionary = State.wardrobe_hair
	for hat: String in owned:
		var item := DragItem.new()
		item.item_name = hat
		item.home = Vector2(owned[hat][0], owned[hat][1])
		item.picked_up.connect(_on_picked_up)
		item.dropped.connect(_on_dropped)
		item.tapped.connect(_on_tapped)
		add_child(item)
		_hats[hat] = item

	if State.naomi_dress != "":
		var dress := _picture("images/naomi/%s.png" % State.naomi_dress, Vector2(-600, 640))
		dress.z_index = 3
		add_child(dress)

	var back := TextureButton.new()
	back.texture_normal = load(State.asset("images/back.png"))
	back.ignore_texture_size = true
	back.stretch_mode = TextureButton.STRETCH_SCALE
	back.size = Vector2(167, 167)
	back.z_index = 30
	back.pressed.connect(func() -> void: closed.emit({}))
	add_child(back)
	_refresh()


func wear(hat: String) -> void:
	State.naomi_hair = hat
	_refresh()


func take_off() -> void:
	State.naomi_hair = "hair_base"
	_refresh()


func _refresh() -> void:
	for node in _head.get_children():
		node.queue_free()
	# Her hair (with the hat she wears, if any) and her makeup, in close-up
	var hair := DragItem.new()
	hair.set_art("images/naomi/%s.png" % State.naomi_hair, 1.0, FACE_CUT)
	hair.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_head.add_child(hair)
	for layer in [["cheek", State.naomi_cheek, 400], ["eye", State.naomi_eye, 312], ["lip", State.naomi_lip, 640]]:
		if layer[1] != "":
			var makeup := _picture("images/naomi/makeup_%s%s.png" % [layer[0], layer[1]], CLOSE_UP + Vector2(0, layer[2]))
			makeup.z_index = 4
			_head.add_child(makeup)

	for hat: String in _hats:
		var item: DragItem = _hats[hat]
		if hat == State.naomi_hair:
			# Worn: the hat is part of the hair picture, so its item is an invisible handle over her head.
			item.set_art("images/naomi/%s.png" % hat, 1.0, FACE_CUT)
			item.self_modulate.a = 0.0
			item.position = HEAD.position
			item.z_index = 5
		else:
			item.set_art("images/item/%s.png" % hat)
			item.self_modulate.a = 1.0
			item.position = item.home
			item.z_index = 10


func _on_picked_up(item: DragItem) -> void:
	if State.naomi_hair == item.item_name:
		# Lifted off her head: back to plain hair, and the hat follows the finger.
		State.naomi_hair = "hair_base"
		var middle := item.get_local_mouse_position() + item.position
		_refresh()
		item.position = middle - item.size / 2.0
	item.z_index = 20


func _on_dropped(item: DragItem) -> void:
	if item.rect().intersects(HEAD):
		wear(item.item_name)
	else:
		item.z_index = 10
		item.go_home()


func _on_tapped(item: DragItem) -> void:
	if State.naomi_hair == item.item_name:
		take_off()
	else:
		wear(item.item_name)


func _open_makeup() -> void:
	var view: Control = load("res://screens/wardrobe_makeup.tscn").instantiate()
	view.closed.connect(func(_action: Dictionary) -> void:
		view.queue_free()
		_refresh())
	add_child(view)


func _picture(game_path: String, at: Vector2) -> TextureRect:
	var picture := TextureRect.new()
	picture.texture = load(State.asset(game_path))
	picture.position = at
	picture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return picture
