class_name StageSprite
extends TextureRect
## One picture on the stage (a background, a character, an item).
## It is placed the way Ren'Py places things, so ATL numbers carry over as they are.
##
##   xpos / ypos       where the anchor sits, as a fraction of the screen (0.5 = middle)
##   xpos_px / ypos_px the same, in pixels (Ren'Py `xpos 100`)
##   xanchor / yanchor which point of the picture sits there (0 = left/top, 1 = right/bottom)
##   zoom              size multiplier (xzoom / yzoom do one direction only)
##   `xalign 0.5` in Ren'Py simply means xpos 0.5 and xanchor 0.5.

const SCREEN := Vector2(1920, 1080)

var image_name := ""
var base_size := Vector2.ZERO
var running_tween: Tween

var xpos := 0.5: set = _set_xpos
var ypos := 1.0: set = _set_ypos
var xpos_px := 0.0: set = _set_xpos_px
var ypos_px := 0.0: set = _set_ypos_px
var xanchor := 0.5: set = _set_xanchor
var yanchor := 1.0: set = _set_yanchor
var xoffset := 0.0: set = _set_xoffset
var yoffset := 0.0: set = _set_yoffset
var zoom := 1.0: set = _set_zoom
var xzoom := 1.0: set = _set_xzoom
var yzoom := 1.0: set = _set_yzoom
var alpha := 1.0: set = _set_alpha


func _init() -> void:
	expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	stretch_mode = TextureRect.STRETCH_SCALE
	mouse_filter = Control.MOUSE_FILTER_IGNORE


func place() -> void:
	size = base_size * zoom * Vector2(xzoom, yzoom)
	position = Vector2(
		xpos * SCREEN.x + xpos_px + xoffset - xanchor * size.x,
		ypos * SCREEN.y + ypos_px + yoffset - yanchor * size.y)


func _set_xpos(v: float) -> void: xpos = v; place()
func _set_ypos(v: float) -> void: ypos = v; place()
func _set_xpos_px(v: float) -> void: xpos_px = v; place()
func _set_ypos_px(v: float) -> void: ypos_px = v; place()
func _set_xanchor(v: float) -> void: xanchor = v; place()
func _set_yanchor(v: float) -> void: yanchor = v; place()
func _set_xoffset(v: float) -> void: xoffset = v; place()
func _set_yoffset(v: float) -> void: yoffset = v; place()
func _set_zoom(v: float) -> void: zoom = v; place()
func _set_xzoom(v: float) -> void: xzoom = v; place()
func _set_yzoom(v: float) -> void: yzoom = v; place()
func _set_alpha(v: float) -> void: alpha = v; modulate.a = v


## Turn Ren'Py property names into the ones above.
static func canonical(props: Dictionary) -> Dictionary:
	var out := {}
	for key in props:
		var value: float = props[key]
		match key:
			"xalign":
				out["xpos"] = value; out["xpos_px"] = 0.0; out["xanchor"] = value
			"yalign":
				out["ypos"] = value; out["ypos_px"] = 0.0; out["yanchor"] = value
			"xpos":
				out["xpos"] = value; out["xpos_px"] = 0.0
			"ypos":
				out["ypos"] = value; out["ypos_px"] = 0.0
			"xpos_px":
				out["xpos"] = 0.0; out["xpos_px"] = value
			"ypos_px":
				out["ypos"] = 0.0; out["ypos_px"] = value
			"xanchor", "yanchor", "xoffset", "yoffset", "zoom", "xzoom", "yzoom", "alpha":
				out[key] = value
			_:
				pass  # zpos, rotate: not supported yet, safely ignored
	return out
