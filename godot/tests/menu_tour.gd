extends Node
## Walks through the menus by itself and saves a picture of each one.
##   godot --path godot res://tests/menu_tour.tscn -- shots=/some/folder

var shots := ""
var count := 0


func _ready() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("shots="):
			shots = arg.trim_prefix("shots=")
	var main: Control = load("res://main.tscn").instantiate()
	main.start_label = "next_morning"
	add_child(main)
	await _shot("title")

	main._menu.show_page("Settings")
	await _shot("title settings")
	State.set_setting("music_volume", 0.4)
	State.set_setting("text_speed", 50)
	main._menu.show_page("Settings")
	await _shot("settings changed")
	main._menu.show_page("Load")
	await _shot("not built page")

	main._menu._on_entry("Gallery", null)
	await _shot("gallery musician")
	var gallery: Control = main._menu.get_child(-1)
	print("unlocked: ", ["musician_1", "musician_2", "merchant_1", "merchant_2"].map(gallery.is_unlocked))
	gallery.view_cutscene("musician_1")
	await _shot("cutscene")
	gallery._next_picture()
	gallery._next_picture()
	gallery.show_character("merchant")
	await _shot("gallery merchant")
	gallery.closed.emit({})

	main.start_game()
	await get_tree().create_timer(1.0).timeout
	main._player.advance()
	await _shot("in game")
	main.open_game_menu()
	main._menu.show_page("Settings")
	await _shot("game menu")
	main._player.advance()
	print("story paused while menu open: ", main._player.menu_open)
	main.close_game_menu()
	await _shot("resumed")

	print("kept file: ", FileAccess.get_file_as_string(State.KEPT_FILE).replace("\n", " "))
	State.set_setting("music_volume", 1.0)
	State.set_setting("text_speed", 0)
	get_tree().quit()


func _shot(what: String) -> void:
	await get_tree().create_timer(0.6).timeout
	count += 1
	print("%02d %s" % [count, what])
	if shots != "":
		await RenderingServer.frame_post_draw
		get_viewport().get_texture().get_image().save_png("%s/%02d.png" % [shots, count])
