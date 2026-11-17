extends VBoxContainer
## Settings page. Every change is applied and saved straight away (State.set_setting).
## To add a setting: add a row here and a default in `State.settings`.

const TEXT_SPEEDS := [["Slow", 25], ["Medium", 50], ["Fast", 100], ["Instant", 0]]


func _ready() -> void:
	add_theme_constant_override("separation", 34)

	_slider_row("Music volume", "music_volume")
	_slider_row("Sound volume", "sound_volume")
	_switch_row("Mute all", bool(State.settings["mute"]),
		func(on: bool) -> void: State.set_setting("mute", on))

	# Text speed: pick one
	var speeds := _row("Text speed")
	var group := ButtonGroup.new()
	for speed in TEXT_SPEEDS:
		var button := UITheme.pill(speed[0])
		button.button_group = group
		button.button_pressed = int(State.settings["text_speed"]) == speed[1]
		button.pressed.connect(func() -> void: State.set_setting("text_speed", speed[1]))
		speeds.add_child(button)

	# Vibration is the story's `persistent.haptics_enabled`
	_switch_row("Vibration", bool(State.persistent.get("haptics_enabled", true)),
		func(on: bool) -> void:
			State.persistent["haptics_enabled"] = on
			State.save_kept())


func _row(title: String) -> HBoxContainer:
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 20)
	var label := Label.new()
	label.text = title
	label.custom_minimum_size = Vector2(360, 72)
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	row.add_child(label)
	add_child(row)
	return row


func _slider_row(title: String, setting: String) -> void:
	var slider := HSlider.new()
	slider.min_value = 0.0
	slider.max_value = 1.0
	slider.step = 0.05
	slider.value = float(State.settings[setting])
	slider.custom_minimum_size = Vector2(620, 72)
	slider.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	slider.value_changed.connect(func(value: float) -> void: State.set_setting(setting, value))
	_row(title).add_child(slider)


func _switch_row(title: String, on: bool, changed: Callable) -> void:
	var button := UITheme.pill("On" if on else "Off")
	button.button_pressed = on
	button.toggled.connect(func(now_on: bool) -> void:
		button.text = "On" if now_on else "Off"
		changed.call(now_on))
	_row(title).add_child(button)
