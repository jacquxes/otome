extends Control
## Menu - one scene for both the title menu and the in-game menu.
## The list on the left is the "place to live" for every game control. Tapping
## an entry shows its page on the right. Pages that are not built yet say so.
##
## To add a page: make a scene, then add its name to PAGES below.

signal start_pressed
signal resume_pressed
signal main_menu_pressed

## false = title menu (before the game starts), true = opened from inside the game
var in_game := false

const TITLE_ENTRIES := ["Start", "Load", "Gallery", "Settings", "About"]
const GAME_ENTRIES := ["Resume", "Inventory", "Wardrobe", "Save", "Load", "History", "Gallery", "Settings", "Main menu"]

## Entry -> the scene shown on the right. Entries without one show "not built yet".
const PAGES := {
	"Settings": "res://screens/settings.tscn",
	"About": "res://screens/about.tscn",
}
## Entries that open a full-screen scene on top of the menu. Each has `signal closed`.
const FULL_SCREENS := {
	"Gallery": "res://screens/gallery.tscn",
	"Wardrobe": "res://screens/wardrobe.tscn",
}

@onready var backdrop: TextureRect = $Backdrop
@onready var shade: ColorRect = $Shade
@onready var title: Label = $Side/Column/Title
@onready var entries: VBoxContainer = $Side/Column/Entries
@onready var page: PanelContainer = $Page
@onready var page_title: Label = $Page/Column/Title
@onready var page_body: Control = $Page/Column/Body

var _leave_asked := false


func _ready() -> void:
	theme = UITheme.get_theme()
	var game: Dictionary = State.load_json("res://story/game_data.json").get("game", {})
	title.text = "Menu" if in_game else game.get("name", "")
	title.add_theme_font_override("font", load(State.asset("Staatliches-Regular.ttf")))
	page_title.add_theme_font_override("font", load(State.asset("Staatliches-Regular.ttf")))
	backdrop.visible = not in_game     # the title menu has its own picture
	shade.visible = in_game            # the in-game menu dims the game behind it
	page.hide()
	for entry: String in (GAME_ENTRIES if in_game else TITLE_ENTRIES):
		var button := Button.new()
		button.text = entry
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		button.focus_mode = Control.FOCUS_NONE
		button.pressed.connect(_on_entry.bind(entry, button))
		entries.add_child(button)


func _on_entry(entry: String, button: Button) -> void:
	match entry:
		"Start":
			start_pressed.emit()
		"Resume":
			resume_pressed.emit()
		"Main menu":
			# Ask once before throwing away the current game (there is no save yet).
			if _leave_asked:
				main_menu_pressed.emit()
			else:
				_leave_asked = true
				button.text = "Tap again to leave"
		_:
			if FULL_SCREENS.has(entry):
				var screen: Control = load(FULL_SCREENS[entry]).instantiate()
				screen.closed.connect(func(_action: Dictionary) -> void: screen.queue_free())
				add_child(screen)
			else:
				show_page(entry)


func show_page(entry: String) -> void:
	for child in page_body.get_children():
		child.queue_free()
	page_title.text = entry
	if PAGES.has(entry):
		page_body.add_child(load(PAGES[entry]).instantiate())
	else:
		var note := Label.new()
		note.text = "%s is not built yet.\nThis is where it will live." % entry
		page_body.add_child(note)
	page.show()
