extends Node
## Plays the story by itself and prints it as text, so you can compare it with Ren'Py.
##
##   godot --path godot res://tests/autoplay.tscn -- label=musician_1 choices=0 money=10
##
##   label=NAME        which label to start from (default: next_morning)
##   choices=1,0,2     which choice to pick at each menu, in order (0 is the first shown;
##                     the last number is reused once the list runs out)
##   route=a,b,c       where to go each time a screen opens, in order: a label to jump to,
##                     or "return". When the list runs out the run stops.
##   lines=N           stop after N lines of dialogue
##   NAME=VALUE        set a game variable before starting, e.g. money=10
##   shots=FOLDER      also save a picture of the screen at every line, menu and screen
##   stage=1           also list the pictures on the stage at every line

var player: Control
var choices: Array = [0]
var route: Array = []
var max_lines := 100000
var shots := ""
var count := 0
var lines := 0
var list_stage := false


func _ready() -> void:
	player = load("res://story_player.tscn").instantiate()
	for arg in OS.get_cmdline_user_args():
		var pair := arg.split("=", true, 1)
		if pair.size() != 2:
			continue
		match pair[0]:
			"label": player.start_label = pair[1]
			"background": player.start_background = pair[1]
			"choices": choices = Array(pair[1].split(",")).map(func(c: String) -> int: return int(c))
			"route": route = Array(pair[1].split(","))
			"lines": max_lines = int(pair[1])
			"shots": shots = pair[1]
			"stage": list_stage = pair[1] == "1"
			_: State.vars[pair[0]] = State.evaluate(pair[1])
	player.line_shown.connect(_on_line)
	player.menu_shown.connect(_on_menu)
	player.screen_shown.connect(_on_screen)
	player.finished.connect(_stop.bind("the story returned"))
	add_child(player)
	_tap_through_pauses()


func _on_line(who: String, text: String) -> void:
	print("%s: %s" % [who, text] if who != "" else text)
	if list_stage:
		for c in player.stage.get_children():
			print("      [%s  at %s  size %s  zorder %d  alpha %.2f]" % [c.image_name, c.position.round(), c.size.round(), c.zorder, c.modulate.a])
	lines += 1
	await _shot()
	if lines >= max_lines:
		return _stop("reached lines=%d" % max_lines)
	player.advance()


func _on_menu(captions: Array) -> void:
	var pick: int = min(choices[0], captions.size() - 1)
	if choices.size() > 1:
		choices.pop_front()
	print("  MENU ", captions, " -> ", captions[pick])
	await _shot()
	player.choose(pick)


func _on_screen(screen_name: String, screen: Control) -> void:
	if "modal" in screen:
		# A screen shown on top of the story (show screen); it closes by itself.
		print("  OVERLAY %s" % screen_name)
		if shots != "":
			_shoot_every(screen, 2.5)
		return
	await _shot()
	if screen.has_method("autoplay"):
		print("  SCREEN %s plays itself" % screen_name)
		screen.closed.connect(func(action: Dictionary) -> void:
			print("    -> %s   [menu %s, tips %s]" % [action, State.cafe_menu, State.shift_tips]))
		if shots != "":
			_shoot_every(screen, 1.5)
		screen.autoplay()
		return
	if route.is_empty():
		return _stop("screen '%s' opened and the route list is empty" % screen_name)
	var next: String = route.pop_front()
	print("  SCREEN %s -> %s   [day %s left, weekday %s, timeslot %s]"
		% [screen_name, next, State.totaldays, State.dayofweeknumber, State.timeslot])
	screen.closed.emit({} if next == "return" else {"jump": next})


func _stop(why: String) -> void:
	print("--- stopped: %s ---" % why)
	for key in ["totaldays", "dayofweeknumber", "timeslot", "money", "tutorial_mode", "musician_event",
			"inventory", "encounters", "visited_today", "story_flags"]:
		print("  %s = %s" % [key, State.vars.get(key)])
	get_tree().quit()


# `pause` lines wait for a tap too; keep tapping so the run never stalls.
func _tap_through_pauses() -> void:
	while true:
		await get_tree().create_timer(0.6).timeout
		player.advance()


func _shot() -> void:
	if shots == "":
		await get_tree().process_frame
		return
	await get_tree().create_timer(0.7).timeout
	await RenderingServer.frame_post_draw
	count += 1
	get_viewport().get_texture().get_image().save_png("%s/%03d.png" % [shots, count])


func _shoot_every(screen: Control, seconds: float) -> void:
	while is_instance_valid(screen):
		await get_tree().create_timer(seconds).timeout
		await RenderingServer.frame_post_draw
		count += 1
		get_viewport().get_texture().get_image().save_png("%s/%03d.png" % [shots, count])
