extends Node
## Plays the first 60 lines of every label (or the ones you name) and lists each
## character shown at a size other than its usual one, with the script line.
## Most of these are deliberate close-ups or distant shots; look for surprises.
##   godot --headless --path godot res://tests/size_check.tscn
##   godot --headless --path godot res://tests/size_check.tscn -- doctor_2 merchant_3
var player: Control
var lines := 0
var label := ""
var found: Dictionary = {}
var tagzoom: Dictionary = {}

func _ready() -> void:
	var data: Dictionary = State.load_json("res://story/game_data.json")
	for tag in data["tag_transforms"]:
		tagzoom[tag] = float(data["tag_transforms"][tag].get("zoom", 1.0))
	var labels: Array = []
	for file in DirAccess.get_files_at("res://story"):
		if file.begins_with("script") and file.ends_with(".json"):
			labels += State.load_json("res://story/" + file)["labels"].keys()
	labels.sort()
	var only := OS.get_cmdline_user_args()
	for l in labels:
		if only.size() > 0 and not (l in only):
			continue
		await run(l)
	print("=== Characters at an unusual size: ", found.size())
	for k in found:
		print(k, "  ", found[k])
	get_tree().quit()

func run(l: String) -> void:
	label = l
	lines = 0
	State.reset()
	State.vars["kirako_name"] = "Kirako"; State.vars["cat_name"] = "Maachan"
	State.vars["money"] = 100
	player = load("res://story_player.tscn").instantiate()
	player.start_label = ""
	player.line_shown.connect(_on_line)
	player.menu_shown.connect(func(_c: Array) -> void: player.choose.call_deferred(0))
	player.screen_shown.connect(func(_n: String, s: Control) -> void: s.closed.emit.call_deferred({}))
	add_child(player)
	var done := [false]
	player.finished.connect(func() -> void: done[0] = true)
	player.start(l)
	var t := 0.0
	while not done[0] and lines < 60 and t < 25.0:
		await get_tree().create_timer(0.05).timeout
		t += 0.05
		player._advanced.emit()
	player.queue_free()
	await get_tree().process_frame

func _on_line(_who: String, _text: String) -> void:
	lines += 1
	for tag in player._sprites:
		var s: StageSprite = player._sprites[tag]
		if tagzoom.has(tag) and absf(s.zoom * s.base_zoom - tagzoom[tag]) > 0.01 and not s.image_name.begins_with("bg"):
			var key := "%s / %s" % [label, s.image_name]
			if not found.has(key):
				found[key] = "zoom %.2f (usual %.2f), line %s" % [s.zoom * s.base_zoom, tagzoom[tag], player._ops[player._pc - 1].get("line", "?")]
