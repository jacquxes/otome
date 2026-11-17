extends Node
## Opens the wardrobe with a full closet and tries everything, saving a picture of each step.
##   godot --path godot res://tests/wardrobe_tour.tscn -- shots=/some/folder

var shots := ""
var count := 0


func _ready() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("shots="):
			shots = arg.trim_prefix("shots=")
	# Give Naomi everything the shops sell.
	State.wardrobe_dress = ["dress_waitress", "dress_cute", "dress_hakama", "dress_modern", "dress_flapper", "dress_prim"]
	State.wardrobe_shoes = ["shoes_geta", "shoes_koppori", "shoes_zori", "shoes_heels", "shoes_pumps", "shoes_boots"]
	State.wardrobe_accessories = ["hand_round", "hand_evening", "hand_straw"]
	State.wardrobe_parasol = ["hand_parasol"]
	State.wardrobe_hair = State.accessories2.duplicate(true)
	State.wardrobe_eye = ["shadow_blue", "shadow_brown", "shadow_pink", "shadow_orange"]
	State.wardrobe_cheek = ["blush_pink", "blush_orange"]
	State.wardrobe_lip = ["stick_pink", "stick_orange", "stick_red", "stick_peach"]

	var wardrobe: Control = load("res://screens/wardrobe.tscn").instantiate()
	add_child(wardrobe)
	await _shot("wardrobe, as she starts")

	wardrobe.wear("dress", "dress_modern")
	wardrobe.wear("shoes", "shoes_boots")
	wardrobe.wear("bag", "hand_round")
	wardrobe.wear("parasol", "hand_parasol")
	await _shot("new outfit")
	print("  wearing: ", [State.naomi_dress, State.naomi_shoes, State.naomi_accessories_right, State.naomi_accessories_left])

	# Drag the dress off her and let go over empty space: it should go back to the shelf.
	var dress: DragItem = wardrobe._items["dress"]["dress_modern"]
	wardrobe._on_picked_up(dress, "dress")
	dress.position = Vector2(900, 900)
	wardrobe._on_dropped(dress, "dress")
	await _shot("dress dragged off")
	print("  dress after dragging off: '", State.naomi_dress, "'")
	# Drag another one onto her.
	var cute: DragItem = wardrobe._items["dress"]["dress_cute"]
	wardrobe._on_picked_up(cute, "dress")
	cute.position = Vector2(400, 400)
	wardrobe._on_dropped(cute, "dress")
	print("  dress after dragging one on: '", State.naomi_dress, "'")

	var bag: DragItem = wardrobe._items["bag"]["hand_round"]
	print("  bag reacts on its painted part: ", bag._has_point(bag.size * Vector2(0.68, 0.45)),
		", on its empty corner: ", bag._has_point(Vector2(5, 5)))

	wardrobe.open_view("res://screens/wardrobe_face.tscn")
	var face: Control = wardrobe.get_child(-1)
	await _shot("dresser view")
	face.wear("hair_hat")
	await _shot("hat on")
	face._open_makeup()
	var makeup: Control = face.get_child(-1)
	await _shot("makeup view")
	makeup.put_on("cheek", "blush_pink")
	makeup.put_on("eye", "shadow_blue")
	makeup.put_on("lip", "stick_red")
	await _shot("makeup on")
	print("  makeup: ", [State.naomi_cheek, State.naomi_eye, State.naomi_lip], " lip colour ", [State.lip_color_h, State.lip_color_s, State.lip_color_v])
	makeup.wipe_off("eye")
	print("  after cold cream on eyes: '", State.naomi_eye, "' eye colour ", [State.eye_color_r, State.eye_color_g, State.eye_color_b])
	makeup.closed.emit({})
	face.closed.emit({})
	await _shot("back in the wardrobe")
	wardrobe.open_view("res://screens/wardrobe_zoom.tscn")
	await _shot("full size")
	get_tree().quit()


func _shot(what: String) -> void:
	await get_tree().create_timer(0.5).timeout
	count += 1
	print("%02d %s" % [count, what])
	if shots != "":
		await RenderingServer.frame_post_draw
		get_viewport().get_texture().get_image().save_png("%s/%02d.png" % [shots, count])
