extends Control
## Map tutorial - Kirako shows how the map works (`screen map_tutorial` in screens_maps.rpy).
## Shown with `show screen map_tutorial`. Plays for 9 seconds, then closes itself.
## While it is up, taps do not move the story on (Ren'Py's `modal True`).

signal closed(action: Dictionary)

var modal := true

const SCREEN := Vector2(1920, 1080)
const ART := "gui/map/"


func _ready() -> void:
	State.day_display = false
	tree_exiting.connect(func() -> void: State.day_display = true)
	var jp: bool = State.jp_lang == true
	add_child(_picture(ART + ("asakusa_ground_jp.png" if jp else "asakusa_ground.png"), Rect2(Vector2.ZERO, SCREEN)))
	if not jp:
		# The shrine, highlighted, blinking a few times
		var region := Rect2(2277, 285, 1156, 487)
		var spot := Rect2(1133, 160, 578, 243.5)
		add_child(_picture(ART + "asakusa_idle.png", spot, region))
		_blink(_picture(ART + "asakusa_hover.png", spot, region), 1.0)
	add_child(_picture(ART + ("asakusa_frame_jp.png" if jp else "asakusa_frame.png"), Rect2(Vector2.ZERO, SCREEN)))

	# The arrow to Ginza, blinking after Kirako moves
	var arrow := Rect2(0, (SCREEN.y - 219) / 2.0, 93, 219)
	add_child(_picture(ART + "arrow_ginza_idle.png", arrow))
	_blink(_picture(ART + "arrow_ginza_hover.png", arrow), 5.6)

	# Kirako: facing right at first, then turns and steps left
	var kirako := _picture("images/kirako/kirako happy.png", Rect2(0.35 * SCREEN.x, 0, 810, 1080))
	kirako.flip_h = true
	add_child(kirako)
	var walk := create_tween()
	walk.tween_interval(4.0)
	walk.tween_callback(func() -> void: kirako.flip_h = false)
	walk.tween_property(kirako, "position:x", 0.1 * SCREEN.x, 1.5).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN)

	_bubble("Choose the place you want to visit!", Vector2(0.8, 0.4), Vector2(0.79, 0.39), true, 0.6, 3.5)
	_bubble("You can use the arrow to visit places in Ginza.", Vector2(0.03, 0.3), Vector2(0.045, 0.29), false, 5.6, -1)

	get_tree().create_timer(9.0).timeout.connect(func() -> void: closed.emit({}))


## Off, then on for half a second, off, on... three times (the Ren'Py pattern).
func _blink(picture: TextureRect, start: float) -> void:
	picture.modulate.a = 0.0
	add_child(picture)
	var tween := create_tween()
	tween.tween_interval(start)
	for i in 3:
		tween.tween_callback(func() -> void: picture.modulate.a = 1.0)
		tween.tween_interval(0.5)
		tween.tween_callback(func() -> void: picture.modulate.a = 0.0)
		tween.tween_interval(0.5)


## A speech bubble with words in it. It appears after `start` seconds and, if `stay` is
## not -1, disappears `stay` seconds later.
func _bubble(words: String, bubble_align: Vector2, text_align: Vector2, flipped: bool, start: float, stay: float) -> void:
	var box := Control.new()
	box.mouse_filter = Control.MOUSE_FILTER_IGNORE
	box.modulate.a = 0.0
	var size := Vector2(380, 180)
	var bubble := _picture("images/speech.png", Rect2(bubble_align * (SCREEN - size), size))
	bubble.flip_h = flipped
	box.add_child(bubble)
	var label := Label.new()
	label.text = words
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.add_theme_font_override("font", load(State.asset("Quicksand_Bold.otf")))
	label.add_theme_font_size_override("font_size", 40)
	label.add_theme_color_override("font_color", Color("3d3f4f"))
	label.size = Vector2(370, 150)
	label.position = text_align * (SCREEN - label.size)
	box.add_child(label)
	add_child(box)
	var tween := create_tween()
	tween.tween_interval(start)
	tween.tween_callback(func() -> void: box.modulate.a = 1.0)
	if stay >= 0.0:
		tween.tween_interval(stay)
		tween.tween_callback(func() -> void: box.modulate.a = 0.0)


func _picture(game_path: String, rect: Rect2, region: Variant = null) -> TextureRect:
	var picture := TextureRect.new()
	var art: Texture2D = load(State.asset(game_path))
	if region != null:
		var cut := AtlasTexture.new()
		cut.atlas = art
		cut.region = region
		art = cut
	picture.texture = art
	picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	picture.position = rect.position
	picture.size = rect.size
	picture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return picture
