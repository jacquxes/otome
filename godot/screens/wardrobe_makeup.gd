extends Control
## Wardrobe, makeup view (`screen wardrobe_makeup`).
## Drag a blush, eyeshadow or lipstick onto Naomi's face (or tap it) to put it on.
## Drag the cold cream onto her eyes, cheeks or lips to wipe that one off.
##
## Makeup she owns:  wardrobe_cheek, wardrobe_eye, wardrobe_lip
## Makeup she wears: naomi_cheek, naomi_eye, naomi_lip  ("" = none), plus the
## colour numbers used by her side picture (cheek_color_r ... lip_color_v).

signal closed(action: Dictionary)

const CLOSE_UP := Vector2(-600, -100)
const FACE := Rect2(0, 0, 940, 1080)            # anywhere on Naomi counts for putting makeup on
const CREAM_HOME := Vector2(1600, 750)

## kind -> owned list, first shelf x, gap, shelf y, y of the overlay on the full-size figure
const KINDS := {
	"eye": {"owned": "wardrobe_eye", "x": 860, "gap": 160, "y": 100, "figure_y": 312},
	"cheek": {"owned": "wardrobe_cheek", "x": 800, "gap": 290, "y": 230, "figure_y": 400},
	"lip": {"owned": "wardrobe_lip", "x": 890, "gap": 150, "y": 600, "figure_y": 640},
}
## The colours her side picture goes back to when makeup is wiped off (the defaults in script.rpy).
const BARE := {
	"cheek": {"cheek_color_r": 1.5, "cheek_color_g": 1.5, "cheek_color_b": 1.5},
	"eye": {"eye_color_r": 1.15, "eye_color_g": 1.2, "eye_color_b": 1.2},
	"lip": {"lip_color_h": 14, "lip_color_s": 0.85, "lip_color_v": 0.15},
}

var _face: Control


func _ready() -> void:
	z_index = 50
	add_child(_picture("images/bg wardrobe.png", Vector2(-300, -200)))
	add_child(_picture("images/wardrobe/bg makeup.png", Vector2(940, 0), 0.5))
	add_child(_picture("images/naomi/base_torso.png", Vector2(-600, 799)))
	var hair := DragItem.new()
	hair.set_art("images/naomi/%s.png" % State.naomi_hair, 1.0, Rect2(600, 100, 899, 899))
	hair.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(hair)
	if State.naomi_dress != "":
		add_child(_picture("images/naomi/%s.png" % State.naomi_dress, Vector2(-600, 640)))
	_face = Control.new()
	_face.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_face)

	for kind: String in KINDS:
		var info: Dictionary = KINDS[kind]
		var owned: Array = State.get(info["owned"])
		for i in owned.size():
			var item := DragItem.new()
			item.item_name = owned[i]
			item.set_art("images/item/makeup_%s%s.png" % [kind, owned[i]], 0.5)
			item.home = Vector2(info["x"] + info["gap"] * (i + 1), info["y"])
			item.position = item.home
			item.picked_up.connect(func(it: DragItem) -> void: it.z_index = 20)
			item.dropped.connect(_on_makeup_dropped.bind(kind))
			item.tapped.connect(func(it: DragItem) -> void: put_on(kind, it.item_name))
			add_child(item)

	var cream := DragItem.new()
	cream.set_art("images/wardrobe/makeup_remover.png", 0.5)
	cream.home = CREAM_HOME
	cream.position = CREAM_HOME
	cream.picked_up.connect(func(it: DragItem) -> void: it.z_index = 20)
	cream.dropped.connect(_on_cream_dropped)
	add_child(cream)

	var back := TextureButton.new()
	back.texture_normal = load(State.asset("images/back.png"))
	back.ignore_texture_size = true
	back.stretch_mode = TextureButton.STRETCH_SCALE
	back.size = Vector2(167, 167)
	back.z_index = 30
	back.pressed.connect(func() -> void: closed.emit({}))
	add_child(back)
	_refresh()


## Put a colour on. Also sets the numbers her side picture uses (wear_cheek / wear_eye / wear_lip).
func put_on(kind: String, colour: String) -> void:
	State.set("naomi_" + kind, colour)
	match kind:
		"cheek":
			var rgb: Array = State.naomi_cheek_rgb[colour]
			State.cheek_color_r = rgb[0]; State.cheek_color_g = rgb[1]; State.cheek_color_b = rgb[2]
		"eye":
			var rgb: Array = State.naomi_eye_rgb[colour]
			State.eye_color_r = rgb[0]; State.eye_color_g = rgb[1]; State.eye_color_b = rgb[2]
		"lip":
			var hsv: Array = State.naomi_lip_hsv[colour]
			State.lip_color_h = hsv[0]; State.lip_color_s = hsv[1]; State.lip_color_v = hsv[2]
	_refresh()


## Wipe one kind of makeup off (clean_cheek / clean_eye / clean_lip).
func wipe_off(kind: String) -> void:
	State.set("naomi_" + kind, "")
	for variable: String in BARE[kind]:
		State.set(variable, BARE[kind][variable])
	_refresh()


func _refresh() -> void:
	for node in _face.get_children():
		node.queue_free()
	for kind: String in KINDS:
		var colour: String = State.get("naomi_" + kind)
		if colour != "":
			_face.add_child(_picture("images/naomi/makeup_%s%s.png" % [kind, colour],
				CLOSE_UP + Vector2(0, KINDS[kind]["figure_y"])))


func _on_makeup_dropped(item: DragItem, kind: String) -> void:
	if item.rect().intersects(FACE):
		put_on(kind, item.item_name)
	item.z_index = 0
	item.go_home()


## The cold cream wipes whichever part of her face it covers most.
func _on_cream_dropped(cream: DragItem) -> void:
	var best := ""
	var best_area := 0.0
	for kind: String in KINDS:
		# Each band is the makeup picture's own strip across her face.
		var band := Rect2(0, KINDS[kind]["figure_y"] + CLOSE_UP.y, FACE.size.x, 260)
		var area: float = cream.rect().intersection(band).get_area()
		if area > best_area:
			best = kind
			best_area = area
	if best != "":
		wipe_off(best)
	cream.z_index = 0
	cream.go_home()


func _picture(game_path: String, at: Vector2, art_scale: float = 1.0) -> TextureRect:
	var picture := TextureRect.new()
	picture.texture = load(State.asset(game_path))
	picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	picture.size = picture.texture.get_size() * art_scale
	picture.position = at
	picture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return picture
