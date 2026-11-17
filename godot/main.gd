extends Control
## Main - the first scene. It shows the title menu, starts the story, and opens
## the in-game menu over it. Everything else lives inside one of those three.
##
##   title menu  ->  Start  ->  story player  ->  menu button  ->  in-game menu
##                                                     "Main menu" brings you back here

const MENU := preload("res://screens/menu.tscn")
const STORY_PLAYER := preload("res://story_player.tscn")

## Where "Start" begins. "start" is the opening; "next_morning" is handy for testing the day loop.
@export var start_label := "start"

var _player: Control
var _menu: Control


func _ready() -> void:
	show_title()


func show_title() -> void:
	_clear()
	_menu = MENU.instantiate()
	_menu.in_game = false
	_menu.start_pressed.connect(start_game)
	add_child(_menu)


func start_game() -> void:
	_clear()
	State.reset()
	_player = STORY_PLAYER.instantiate()
	_player.start_label = start_label
	_player.menu_requested.connect(open_game_menu)
	_player.finished.connect(show_title)
	add_child(_player)


func open_game_menu() -> void:
	if _menu != null:
		return
	_player.menu_open = true
	_menu = MENU.instantiate()
	_menu.in_game = true
	_menu.resume_pressed.connect(close_game_menu)
	_menu.main_menu_pressed.connect(show_title)
	add_child(_menu)


func close_game_menu() -> void:
	_menu.queue_free()
	_menu = null
	_player.menu_open = false


func _clear() -> void:
	for node in [_menu, _player]:
		if node != null:
			node.queue_free()
	_menu = null
	_player = null
