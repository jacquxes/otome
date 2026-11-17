extends Control
## Wardrobe - dress Naomi (`screen wardrobe` in screens_wardrobe.rpy).
##
## Drag a dress, shoes, a bag or the parasol from the shelves onto Naomi to wear it.
## Drag it off her (or tap it) to put it back. Tapping a shelf item wears it too.
## The dresser opens the hat-and-makeup view; the magnifier shows Naomi full size.
##
## What she owns comes from the game:  wardrobe_dress, wardrobe_shoes,
## wardrobe_accessories, wardrobe_parasol.  What she wears is saved in:
## naomi_dress, naomi_shoes, naomi_accessories_right, naomi_accessories_left.

signal closed(action: Dictionary)

const SCREEN := Vector2(1920, 1080)
const FIGURE_X := 276.5            # Naomi's pictures are 2150 wide, shown at a quarter size, xalign 0.2
const WORN_SCALE := 0.25           # images/naomi/...
const SHELF_SCALE := 0.5           # images/item/...

## One entry per thing Naomi can wear on this screen.
##   variable  the game variable holding what she wears ("" = nothing)
##   owned     the game variable listing what she owns
##   worn_at   where the worn picture sits
##   zone      where a dragged item must be let go to be worn
##   layer     drawing order on Naomi (higher = on top)
const SLOTS := {
	"dress": {"variable": "naomi_dress", "owned": "wardrobe_dress",
		"worn_at": Vector2(FIGURE_X, 186), "zone": Rect2(FIGURE_X, 225, 537.5, 625), "layer": 6},
	"shoes": {"variable": "naomi_shoes", "owned": "wardrobe_shoes",
		"worn_at": Vector2(FIGURE_X, 850), "zone": Rect2(FIGURE_X, 850, 537.5, 225), "layer": 4},
	"bag": {"variable": "naomi_accessories_right", "owned": "wardrobe_accessories",
		"worn_at": Vector2(275, 500), "zone": Rect2(275, 500, 225, 225), "layer": 7},
	"parasol": {"variable": "naomi_accessories_left", "owned": "wardrobe_parasol",
		"worn_at": Vector2(600, 500), "zone": Rect2(600, 500, 212.5, 575), "layer": 2},
}

var _items: Dictionary = {}      # slot -> {item name -> DragItem}
var _head: Control               # hair and makeup, rebuilt when they change
var _hats: Control               # the hats sitting on the dresser


func _ready() -> void:
	z_index = 5   # above the day display and the bedroom, like `zorder 5`
	add_child(_picture("images/bg wardrobe.png", Vector2.ZERO, 0.5))

	var dresser := TextureButton.new()
	dresser.texture_normal = load(State.asset("images/wardrobe/dresser.png"))
	dresser.ignore_texture_size = true
	dresser.stretch_mode = TextureButton.STRETCH_SCALE
	dresser.position = Vector2(611, 170)
	dresser.size = Vector2(474, 745)
	dresser.pressed.connect(open_view.bind("res://screens/wardrobe_face.tscn"))
	add_child(dresser)

	_hats = Control.new()
	_hats.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_hats)
	_head = Control.new()
	_head.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_head)

	# Naomi's body, under the clothes
	var feet := _picture("images/naomi/base_feet.png", Vector2(FIGURE_X, 850), WORN_SCALE)
	feet.z_index = 3
	add_child(feet)
	var torso := _picture("images/naomi/base_torso.png", Vector2(FIGURE_X, 225), WORN_SCALE)
	torso.z_index = 5
	add_child(torso)

	for slot: String in SLOTS:
		_items[slot] = {}
		var owned: Array = State.get(SLOTS[slot]["owned"])
		for i in owned.size():
			var item := DragItem.new()
			item.item_name = owned[i]
			item.home = _shelf_spot(slot, i)
			item.picked_up.connect(_on_picked_up.bind(slot))
			item.dropped.connect(_on_dropped.bind(slot))
			item.tapped.connect(_on_tapped.bind(slot))
			add_child(item)
			_items[slot][owned[i]] = item
		_refresh(slot)
	_refresh_head()

	var back := _button("images/back.png", Rect2(0, 0, 167, 167))
	back.pressed.connect(func() -> void: closed.emit({}))
	var zoom := _button("gui/zoomin_idle.png", Rect2(172, 880, 200, 200))
	zoom.pressed.connect(open_view.bind("res://screens/wardrobe_zoom.tscn"))


## Where each owned item rests. Same counting as the Ren'Py screen:
## three across, then a second row.
func _shelf_spot(slot: String, index: int) -> Vector2:
	var count := index + 1
	match slot:
		"dress":
			return Vector2(940 + 200 * count, 295) if count < 4 else Vector2(1140 + 200 * (count - 4), 475)
		"shoes":
			return Vector2(975 + 195 * count, 640) if count < 4 else Vector2(1175 + 195 * (count - 4), 815)
		"bag":
			return Vector2(950 + 200 * count, 95)
	return Vector2(1735, 530)   # the parasol


# ---------------------------------------------------------------------------
# Wearing and taking off
# ---------------------------------------------------------------------------

## Put an item on Naomi. Whatever she wore in that slot goes back to its shelf.
func wear(slot: String, item_name: String) -> void:
	State.set(SLOTS[slot]["variable"], item_name)
	_refresh(slot)


func take_off(slot: String) -> void:
	State.set(SLOTS[slot]["variable"], "")
	_refresh(slot)


## Show every item in this slot the right way: worn on Naomi, or resting on its shelf.
func _refresh(slot: String) -> void:
	var worn_name: String = State.get(SLOTS[slot]["variable"])
	for item_name: String in _items[slot]:
		var item: DragItem = _items[slot][item_name]
		if item_name == worn_name:
			item.set_art("images/naomi/%s.png" % item_name, WORN_SCALE)
			item.position = SLOTS[slot]["worn_at"]
			item.z_index = SLOTS[slot]["layer"]
		else:
			item.set_art("images/item/%s.png" % item_name, SHELF_SCALE)
			item.position = item.home
			item.z_index = 10


func _on_picked_up(item: DragItem, slot: String) -> void:
	# Lifted off Naomi: it turns back into the shelf picture, under the finger.
	if State.get(SLOTS[slot]["variable"]) == item.item_name:
		State.set(SLOTS[slot]["variable"], "")
		var middle := item.rect().get_center()
		item.set_art("images/item/%s.png" % item.item_name, SHELF_SCALE)
		item.position = middle - item.size / 2.0
	item.z_index = 20


func _on_dropped(item: DragItem, slot: String) -> void:
	if item.rect().intersects(SLOTS[slot]["zone"]):
		wear(slot, item.item_name)
	else:
		item.z_index = 10
		item.go_home()


func _on_tapped(item: DragItem, slot: String) -> void:
	if State.get(SLOTS[slot]["variable"]) == item.item_name:
		take_off(slot)
	else:
		wear(slot, item.item_name)


# ---------------------------------------------------------------------------
# Hair and makeup (changed in the dresser view, shown here)
# ---------------------------------------------------------------------------

func _refresh_head() -> void:
	for node in _head.get_children() + _hats.get_children():
		node.queue_free()
	_head.add_child(_picture("images/naomi/%s.png" % State.naomi_hair, Vector2(FIGURE_X, 0), WORN_SCALE))
	for layer in [["cheek", State.naomi_cheek, 100], ["eye", State.naomi_eye, 78], ["lip", State.naomi_lip, 160]]:
		if layer[1] != "":
			_head.add_child(_picture("images/naomi/makeup_%s%s.png" % [layer[0], layer[1]],
				Vector2(FIGURE_X, layer[2]), WORN_SCALE))
	# Hats she owns but is not wearing sit on the dresser.
	var hats: Dictionary = State.wardrobe_hair
	for hat: String in hats:
		if hat != State.naomi_hair:
			var spot := Vector2(int(hats[hat][0]) / 2 + 150, int(hats[hat][1]) / 2 + 100)
			_hats.add_child(_picture("images/item/%s.png" % hat, spot, SHELF_SCALE))


## Open the dresser view or the full-size view on top of this one.
func open_view(scene_path: String) -> void:
	var view: Control = load(scene_path).instantiate()
	view.closed.connect(func(_action: Dictionary) -> void:
		view.queue_free()
		_refresh_head())
	add_child(view)


# ---------------------------------------------------------------------------

func _picture(game_path: String, at: Vector2, art_scale: float) -> TextureRect:
	var picture := TextureRect.new()
	picture.texture = load(State.asset(game_path))
	picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	picture.size = picture.texture.get_size() * art_scale
	picture.position = at
	picture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return picture


func _button(game_path: String, rect: Rect2) -> TextureButton:
	var button := TextureButton.new()
	button.texture_normal = load(State.asset(game_path))
	button.ignore_texture_size = true
	button.stretch_mode = TextureButton.STRETCH_SCALE
	button.position = rect.position
	button.size = rect.size
	button.z_index = 30
	add_child(button)
	return button
