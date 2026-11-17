extends Control
## Map - the four map screens from screens_maps.rpy in one scene.
## "small" shows the whole map. "large" is twice the size and can be dragged.
## Tap a place to go there. The numbers below are copied from the Ren'Py hotspots.

signal closed(action: Dictionary)

const ART := "gui/"
const SCREEN := Vector2(1920, 1080)
const WEEKDAY := "dayofweeknumber < 6"

## [x, y, width, height, label to jump to, condition ("" = always)]
const MAPS := {
	"ginza_small": {
		"art": "ginza", "large": false,
		"places": [
			[784, 539, 342, 324, "dept_store", ""],
			[81, 104, 347, 237, "imperial_theatre", "unlock_imp_th == true and " + WEEKDAY],
			[1521, 611, 277, 114, "office_bldg", "unlock_off_bldg == true and " + WEEKDAY],
			[1063, 898, 428, 136, "hospital", "unlock_hosp == true and " + WEEKDAY],
		],
		"arrow": {"art": "map/arrow_asakusa", "left": false, "jump": "asakusa_small"},
		"zoom": {"art": "zoomin", "jump": "ginza_large"},
	},
	"ginza_large": {
		"art": "ginza", "large": true,
		"places": [
			[1573, 1069, 670, 655, "dept_store", ""],
			[149, 206, 709, 465, "imperial_theatre", "unlock_imp_th == true and " + WEEKDAY],
			[3033, 1220, 554, 240, "office_bldg", "unlock_off_bldg == true and " + WEEKDAY],
			[2130, 1791, 853, 282, "hospital", "unlock_hosp == true and " + WEEKDAY],
		],
		"arrow": {"art": "map/arrow_asakusa", "left": false, "jump": "asakusa_large"},
		"zoom": {"art": "zoomout", "jump": "ginza_small"},
	},
	"asakusa_small": {
		"art": "asakusa", "large": false,
		"places": [
			[692, 799, 311, 251, "work_cafe", ""],
			# These two are copied as they are in screens_maps.rpy, where they still
			# use the large map's numbers and so sit below the bottom of the screen.
			[418, 1194, 582, 412, "doctor_movie", "(unlock_movie_th == true and dayofweeknumber < 6) or (doctor_event == true and dayofweeknumber == 7 and timeslot == 1)"],
			[109, 1572, 394, 413, "dojo", "unlock_dojo == true and " + WEEKDAY],
			[1133, 160, 581, 222, "shrine", ""],
		],
		"arrow": {"art": "map/arrow_ginza", "left": true, "jump": "ginza_small"},
		"zoom": {"art": "zoomin", "jump": "asakusa_large"},
	},
	"asakusa_large": {
		"art": "asakusa", "large": true,
		"places": [
			[1360, 1584, 653, 514, "work_cafe", ""],
			[418, 1194, 582, 412, "doctor_movie", "(unlock_movie_th == true and dayofweeknumber < 6) or (doctor_event == true and dayofweeknumber == 7 and timeslot == 1)"],
			[130, 1578, 380, 287, "dojo", "unlock_dojo == true and " + WEEKDAY],
			[2277, 285, 1156, 487, "shrine", ""],
		],
		"arrow": {"art": "map/arrow_ginza", "left": true, "jump": "ginza_large"},
		"zoom": {"art": "zoomout", "jump": "asakusa_small"},
	},
}

## Set by the story player before the screen is shown.
var screen_name := "asakusa_small"

var _content: Control                 # the map picture and its places; this is what gets dragged
var _places: Array = []               # [Rect2 on the content, label]
var _press_position := Vector2.ZERO
var _pressed := false
var _dragged := false


func _ready() -> void:
	var map: Dictionary = MAPS[screen_name]
	var size_on_screen: Vector2 = SCREEN * (2.0 if map["large"] else 1.0)
	var suffix := "_jp" if State.jp_lang == true else ""

	_content = Control.new()
	_content.size = size_on_screen
	_content.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_content)
	_content.add_child(_picture(ART + "map/%s_ground%s.png" % [map["art"], suffix], Rect2(Vector2.ZERO, size_on_screen)))

	# Each place the player can go right now gets its highlighted cut-out of the "idle" art.
	var idle: Texture2D = load(State.asset(ART + "map/%s_idle.png" % map["art"]))
	var art_scale: Vector2 = idle.get_size() / size_on_screen
	for place in map["places"]:
		var rect := Rect2(place[0], place[1], place[2], place[3])
		if place[5] != "" and not State.evaluate(place[5]):
			continue
		if not Rect2(Vector2.ZERO, size_on_screen).encloses(rect):
			push_warning("Map '%s': the place '%s' is outside the map picture, so it cannot be tapped." % [screen_name, place[4]])
			continue
		var cutout := AtlasTexture.new()
		cutout.atlas = idle
		cutout.region = Rect2(rect.position * art_scale, rect.size * art_scale)
		_content.add_child(_picture(cutout, rect))
		_places.append([rect, place[4]])

	add_child(_picture(ART + "map/%s_frame%s.png" % [map["art"], suffix], Rect2(Vector2.ZERO, SCREEN)))

	var arrow: Dictionary = map["arrow"]
	var arrow_x := 0.0 if arrow["left"] else SCREEN.x - 93.0
	_button(arrow["art"], Rect2(arrow_x, (SCREEN.y - 219.0) / 2.0, 93, 219), arrow["jump"])
	_button(map["zoom"]["art"], Rect2(SCREEN.x - 200.0, SCREEN.y - 200.0, 200, 200), map["zoom"]["jump"])

	# The Ren'Py screens hide the day display while a map is open.
	State.day_display = false


func _close(action: Dictionary) -> void:
	State.day_display = true
	closed.emit(action)


func _picture(art: Variant, rect: Rect2) -> TextureRect:
	var picture := TextureRect.new()
	picture.texture = load(State.asset(art)) if art is String else art
	picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	picture.position = rect.position
	picture.size = rect.size
	picture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return picture


func _button(art: String, rect: Rect2, jump_to: String) -> void:
	var button := TextureButton.new()
	button.texture_normal = load(State.asset(ART + art + "_idle.png"))
	button.texture_pressed = load(State.asset(ART + art + "_hover.png"))
	button.ignore_texture_size = true
	button.stretch_mode = TextureButton.STRETCH_SCALE
	button.position = rect.position
	button.size = rect.size
	button.pressed.connect(func() -> void: _close({"jump": jump_to}))
	add_child(button)


## One handler for taps and drags. A press that moves more than a few pixels is
## a drag (large maps only); a press that stays put is a tap on a place.
func _gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		if event.pressed:
			_pressed = true
			_dragged = false
			_press_position = event.position
		elif _pressed:
			_pressed = false
			if not _dragged:
				go_to_place_at(event.position)
	elif event is InputEventMouseMotion and _pressed:
		if event.position.distance_to(_press_position) > 16.0:
			_dragged = true
		if _dragged:
			var lowest: Vector2 = SCREEN - _content.size
			_content.position = (_content.position + event.relative).clamp(lowest, Vector2.ZERO)


## Go to whichever place is under this point of the screen, if any.
func go_to_place_at(screen_point: Vector2) -> void:
	var point := screen_point - _content.position
	for place in _places:
		if place[0].has_point(point):
			_close({"jump": place[1]})
			return
