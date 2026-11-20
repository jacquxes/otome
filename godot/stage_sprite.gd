class_name StageSprite
extends TextureRect
## One picture on the stage (a background, a character, an item).
## It is placed the way Ren'Py places things, so ATL numbers carry over as they are.
##
##   xpos / ypos       where the anchor sits, as a fraction of the screen (0.5 = middle)
##   xpos_px / ypos_px the same, in pixels (Ren'Py `xpos 100`)
##   xanchor / yanchor which point of the picture sits there (0 = left/top, 1 = right/bottom)
##   zoom              size multiplier (xzoom / yzoom do one direction only),
##                     on top of base_zoom, the character's usual size
##   `xalign 0.5` in Ren'Py simply means xpos 0.5 and xanchor 0.5.

const SCREEN := Vector2(1920, 1080)

var image_name := ""
## Ren'Py's `zorder`: higher is drawn in front of the other pictures (never over the text box).
var zorder := 0
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
## The character's usual size (config.tag_transform, or F2 layout mode).
## `zoom` from the script multiplies it, like Ren'Py: zoom 1.0 = usual size, 2.0 = twice that.
var base_zoom := 1.0: set = _set_base_zoom
var xzoom := 1.0: set = _set_xzoom
var yzoom := 1.0: set = _set_yzoom
var alpha := 1.0: set = _set_alpha
## Distance toward the viewer, as with Ren'Py's `camera: perspective True` (label start).
## Positive is closer and bigger, negative further and smaller; 0 is normal size.
var zpos := 0.0: set = _set_zpos
## Picture effects, all done by one small shader (made only when an effect is on):
##   brightness  matrixcolor BrightnessMatrix(n): 0.2 lighter, -0.5 darker
##   saturation  matrixcolor SaturationMatrix(n): 1.2 stronger colours, 0 grey
##   blur        blur n: soft focus, n is about the width of the blur in screen pixels
##   glitch      glitch("picture", offset=n): torn horizontal strips, up to n pixels apart
##   rotate      degrees, clockwise, around the middle of the picture
var brightness := 0.0: set = _set_brightness
var saturation := 1.0: set = _set_saturation
var blur := 0.0: set = _set_blur
var glitch := 0.0: set = _set_glitch
var rotate := 0.0: set = _set_rotate
var frames_tween: Tween          # a flip-book picture playing its frames

const EFFECTS_SHADER := """
shader_type canvas_item;
uniform float brightness = 0.0;
uniform float saturation = 1.0;
uniform float blur = 0.0;           // in picture pixels
uniform float glitch = 0.0;         // in picture pixels
uniform float glitch_seed = 0.0;
varying vec4 tint;

void vertex() {
	tint = COLOR;   // fades (alpha) and other colouring from Godot
}

float rand(float n) {
	return fract(sin(n * 12.9898 + glitch_seed * 78.233) * 43758.5453);
}

void fragment() {
	vec2 uv = UV;
	vec2 px = TEXTURE_PIXEL_SIZE;
	vec4 c;
	if (glitch > 0.0) {
		// Cut the picture into strips and slide some of them sideways,
		// with the red and blue a little apart.
		float strip = floor(uv.y * 28.0);
		if (rand(strip) > 0.5) {
			uv.x += (rand(strip + 0.5) * 2.0 - 1.0) * glitch * px.x;
		}
		float split = glitch * 0.2 * px.x;
		vec4 g = texture(TEXTURE, uv);
		c = vec4(texture(TEXTURE, uv + vec2(split, 0.0)).r, g.g, texture(TEXTURE, uv - vec2(split, 0.0)).b, g.a);
		if (uv.x < 0.0 || uv.x > 1.0) {
			c = vec4(0.0);
		}
	} else if (blur > 0.0) {
		vec4 sum = vec4(0.0);
		float total = 0.0;
		for (int i = -3; i <= 3; i++) {
			for (int j = -3; j <= 3; j++) {
				vec2 o = vec2(float(i), float(j)) / 3.0;
				float w = exp(-dot(o, o) * 2.0);
				sum += texture(TEXTURE, uv + o * blur * px) * w;
				total += w;
			}
		}
		c = sum / total;
	} else {
		c = texture(TEXTURE, uv);
	}
	float grey = dot(c.rgb, vec3(0.2126, 0.7152, 0.0722));
	c.rgb = mix(vec3(grey), c.rgb, saturation);
	c.rgb = clamp(c.rgb + brightness, 0.0, 1.0);
	COLOR = c * tint;
}
"""
static var _shader: Shader

## Ren'Py's camera sits this far from the zpos 0 plane: (width / 2) / tan(75° / 2).
const CAMERA_Z := 1251.0


func _init() -> void:
	expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	stretch_mode = TextureRect.STRETCH_SCALE
	mouse_filter = Control.MOUSE_FILTER_IGNORE


func place() -> void:
	# A negative xzoom / yzoom (Ren'Py's way to mirror a picture) flips it instead.
	var scale := Vector2(xzoom, yzoom) * base_zoom * zoom
	flip_h = scale.x < 0.0
	flip_v = scale.y < 0.0
	size = base_size * scale.abs()
	position = Vector2(
		xpos * SCREEN.x + xpos_px + xoffset - xanchor * size.x,
		ypos * SCREEN.y + ypos_px + yoffset - yanchor * size.y)
	pivot_offset = size / 2.0
	rotation_degrees = rotate
	if material != null:
		_update_effects()
	if zpos != 0.0:
		# Seen through the camera: grows toward the viewer, around the middle of the screen.
		var depth: float = CAMERA_Z / max(CAMERA_Z - zpos, 1.0)
		position = SCREEN / 2.0 + (position - SCREEN / 2.0) * depth
		size *= depth


func _set_xpos(v: float) -> void: xpos = v; place()
func _set_ypos(v: float) -> void: ypos = v; place()
func _set_xpos_px(v: float) -> void: xpos_px = v; place()
func _set_ypos_px(v: float) -> void: ypos_px = v; place()
func _set_xanchor(v: float) -> void: xanchor = v; place()
func _set_yanchor(v: float) -> void: yanchor = v; place()
func _set_xoffset(v: float) -> void: xoffset = v; place()
func _set_yoffset(v: float) -> void: yoffset = v; place()
func _set_zoom(v: float) -> void: zoom = v; place()
func _set_base_zoom(v: float) -> void: base_zoom = v; place()
func _set_xzoom(v: float) -> void: xzoom = v; place()
func _set_yzoom(v: float) -> void: yzoom = v; place()
func _set_zpos(v: float) -> void: zpos = v; place()
func _set_brightness(v: float) -> void: brightness = v; _update_effects()
func _set_saturation(v: float) -> void: saturation = v; _update_effects()
func _set_blur(v: float) -> void: blur = v; _update_effects()
func _set_glitch(v: float) -> void: glitch = v; _update_effects()
func _set_rotate(v: float) -> void: rotate = v; place()


## A new random tear for the glitch (each glitch frame looks different).
func new_glitch_pattern() -> void:
	if material != null:
		material.set_shader_parameter("glitch_seed", randf() * 100.0)


func _update_effects() -> void:
	var plain := is_zero_approx(brightness) and is_equal_approx(saturation, 1.0) \
		and blur <= 0.0 and glitch <= 0.0
	if plain and material == null:
		return
	if material == null:
		if _shader == null:
			_shader = Shader.new()
			_shader.code = EFFECTS_SHADER
		material = ShaderMaterial.new()
		material.shader = _shader
		new_glitch_pattern()
	# Blur and glitch are given in screen pixels; the shader works in picture pixels.
	var picture_pixels := 1.0
	if texture != null and size.x > 0.0:
		picture_pixels = texture.get_size().x / size.x
	material.set_shader_parameter("brightness", brightness)
	material.set_shader_parameter("saturation", saturation)
	material.set_shader_parameter("blur", blur * picture_pixels)
	material.set_shader_parameter("glitch", glitch * picture_pixels)


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
			# Pixel positions (`xpos 100`) replace the fraction, unless both are given,
			# which happens when these values have already been through this function.
			"xpos_px":
				if not props.has("xpos"):
					out["xpos"] = 0.0
				out["xpos_px"] = value
			"ypos_px":
				if not props.has("ypos"):
					out["ypos"] = 0.0
				out["ypos_px"] = value
			"xanchor", "yanchor", "xoffset", "yoffset", "zoom", "xzoom", "yzoom", "alpha", "zpos", "brightness", "saturation", "blur", "rotate":
				out[key] = value
			_:
				pass
	return out
