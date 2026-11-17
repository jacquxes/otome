extends Control
## DayDisplay - the strip at the top: time of day, days left / weekday, money.
## Same job as `screen DayDisplay` in screens.rpy. It shows whenever the game
## variable `day_display` is true.

const WEEKDAYS := ["Error", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
const TIME_ICONS := {
	2: preload("res://assets/game/images/menu/morning.png"),
	1: preload("res://assets/game/images/menu/afternoon.png"),
	0: preload("res://assets/game/images/menu/evening.png"),
}

@onready var time_icon: TextureRect = $TimeIcon
@onready var day_text: Label = $DayText
@onready var money_text: Label = $MoneyText

var _shown_for := 0.0


func _process(delta: float) -> void:
	var on: bool = State.day_display == true
	if on and not visible:
		_shown_for = 0.0
	visible = on
	if not on:
		return
	_shown_for += delta

	var day_number := int(State.dayofweeknumber)
	var weekday: String = WEEKDAYS[day_number] if day_number >= 1 and day_number <= 7 else "Error"
	State.vars["dayofweek"] = weekday

	time_icon.texture = TIME_ICONS.get(int(State.timeslot))
	# Like the Ren'Py screen: "N days left" for three seconds, then the weekday.
	day_text.text = "%d days left" % State.totaldays if _shown_for < 3.0 else weekday
	money_text.text = "¥%d" % State.money
