extends Label
## About page: the game's name and version, read from options.rpy by the converter.


func _ready() -> void:
	var game: Dictionary = State.load_json("res://story/game_data.json").get("game", {})
	text = "%s\nVersion %s" % [game.get("name", ""), game.get("version", "")]
