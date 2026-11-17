class_name DragItem
extends TextureRect
## A picture the player can drag with a finger, or tap. Only its painted part reacts.
## It only moves itself and reports what happened; the screen decides what a drop means.
##
##   picked_up  the first moment it is really dragged (not on a simple tap)
##   dropped    let go after a drag
##   tapped     pressed and released without moving

signal picked_up(item: DragItem)
signal dropped(item: DragItem)
signal tapped(item: DragItem)

const DRAG_START := 14.0   # pixels of movement before a press counts as a drag

var item_name := ""
var home := Vector2.ZERO   # where it rests (its shelf spot)

var _solid: BitMap          # which pixels of the picture are not see-through
static var _solid_cache: Dictionary = {}

var _held := false
var _dragging := false
var _travelled := 0.0


func _init() -> void:
	expand_mode = TextureRect.EXPAND_IGNORE_SIZE


## Show a picture from game/ at a scale, e.g. set_art("images/item/dress_cute.png", 0.5).
func set_art(game_path: String, art_scale: float = 1.0, region: Variant = null) -> void:
	var art: Texture2D = load(State.asset(game_path))
	if region != null:
		var cut := AtlasTexture.new()
		cut.atlas = art
		cut.region = region
		art = cut
	texture = art
	size = art.get_size() * art_scale
	# Remember the picture's shape, so only its painted part can be grabbed.
	var key := "%s %s" % [game_path, region]
	if not _solid_cache.has(key):
		var shape := BitMap.new()
		shape.create_from_image_alpha(art.get_image(), 0.1)
		_solid_cache[key] = shape
	_solid = _solid_cache[key]


func go_home(seconds: float = 0.15) -> void:
	create_tween().tween_property(self, "position", home, seconds)


func rect() -> Rect2:
	return Rect2(position, size)


## Touches on the see-through part of the picture pass through to whatever is behind it.
## (Clothes pictures are mostly empty space, and they overlap each other on Naomi.)
func _has_point(point: Vector2) -> bool:
	if _solid == null or size.x <= 0 or size.y <= 0:
		return false
	var shape_size := Vector2(_solid.get_size())
	var pixel := Vector2i(point / size * shape_size)
	if pixel.x < 0 or pixel.y < 0 or pixel.x >= shape_size.x or pixel.y >= shape_size.y:
		return false
	return _solid.get_bitv(pixel)


func _gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		if event.pressed:
			_held = true
			_dragging = false
			_travelled = 0.0
		elif _held:
			_held = false
			if _dragging:
				dropped.emit(self)
			else:
				tapped.emit(self)
	elif event is InputEventMouseMotion and _held:
		_travelled += event.relative.length()
		if not _dragging and _travelled > DRAG_START:
			_dragging = true
			picked_up.emit(self)
		if _dragging:
			position += event.relative
