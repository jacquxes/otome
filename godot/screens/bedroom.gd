extends Control
## Bedroom - shown at the end of the day (`screen bedroom` in screens.rpy).
## Dresser opens the wardrobe. Bed jumps to the `end_day` label.
##
## Every screen follows the same rule: when the player is done, emit
## `closed` with {"jump": "label"} (Ren'Py's Jump) or {} (Ren'Py's Return).

signal closed(action: Dictionary)

@onready var dresser: TextureButton = $Dresser
@onready var bed: TextureButton = $Bed


func _ready() -> void:
	bed.pressed.connect(func() -> void: closed.emit({"jump": "end_day"}))
	dresser.pressed.connect(_open_wardrobe)
	# Ren'Py brightens these on hover. A phone has no hover, so brighten while pressed.
	for button: TextureButton in [dresser, bed]:
		button.button_down.connect(func() -> void: button.modulate = Color(1.2, 1.2, 1.2))
		button.button_up.connect(func() -> void: button.modulate = Color.WHITE)


func _open_wardrobe() -> void:
	var wardrobe: Control = load("res://screens/wardrobe.tscn").instantiate()
	wardrobe.closed.connect(func(_action: Dictionary) -> void: wardrobe.queue_free())
	add_child(wardrobe)
