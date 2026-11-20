# Godot backup port - steps 1 to 3, plus menus

Tested with Godot 4.5.1. Put `tools/` and `godot/` at the top of the repo, next to `game/`.

    tools/rpy_to_json.py       turns the .rpy story files into data, copies the art
    godot/
      main.tscn/.gd            the first scene: title menu -> story -> in-game menu
      ui_theme.gd              the look of the menus (fonts, colours, slider and button shapes)
      story_player.tscn/.gd    plays the story: pictures, dialogue, choices, screens
      stage_sprite.gd          places pictures the way Ren'Py does
      state.gd                 all game variables + the game rules ported from Python
                               (flags, musician conditions, cafe visits, relationship stage)
      screens/map              the four map screens (one scene, four sets of numbers)
      screens/bedroom          end-of-day room: dresser and bed
      screens/cafe_menu        choose three items for today's menu
      screens/cafe_game        carry each dish to the right table (drag and drop)
      screens/day_display      the strip at the top: time of day, days left, money
      screens/wardrobe         dress Naomi: dresses, shoes, bags, parasol (drag or tap)
      screens/wardrobe_face    dresser close-up: hats
      screens/wardrobe_makeup  blush, eyeshadow, lipstick, cold cream
      screens/wardrobe_zoom    Naomi at full size
      drag_item.gd             a picture you can drag or tap (used by the wardrobe)
      screens/menu             title menu and in-game menu (one scene, two lists of entries)
      screens/settings         volume, mute, text speed, vibration
      screens/gallery          one page per love interest, with unlockable cutscenes
      screens/about            game name and version
      screens/placeholder      stands in for any screen that is not built yet
      story/                   made by the converter (do not edit by hand)
      assets/game/             made by the converter (copies of game/ art, about 430 MB)
      tests/autoplay.tscn      plays the story by itself and prints it as text

## First run

1. From the repo root, convert the game. This also copies the art, so it takes a moment:

       python3 tools/rpy_to_json.py game godot

2. Install Godot 4.5 or newer, choose Import, pick `godot/project.godot`.
   The first import of the art takes a few minutes.
3. Press Play. The title menu opens. **Start** plays the game from the opening.
   Click or tap to advance. The round button at the top right opens the in-game menu.

To start somewhere else while testing, open `main.tscn`, select the top node and change
**Start Label** (for example `next_morning` for the day loop). To run one scene with no
menus at all, open `story_player.tscn` and press "Run Current Scene" (F6).

## After you change a script in Ren'Py

Run the converter again (same command). Then read `godot/story/report.txt`. It lists:

- story lines it could not convert
- `python:` blocks, each with the function name to add to `state.gd`
- screens the story opens (each needs a scene in `godot/screens/`)
- effects left out for now (blur, matrixcolor)
- missing pictures and sounds

## How the pieces connect

- `call screen X` in the story opens `godot/screens/X.tscn`. If there is none, the
  placeholder opens and offers the same exits the Ren'Py screen has.
- A screen ends by emitting `closed` with `{"jump": "label"}` (Ren'Py `Jump`) or `{}` (`Return`).
- Plain `define` lines (`define TIP_MIN = 4`) are read by the converter, so Godot
  screens use the same numbers: `State.TIP_MIN`. Change them in the .rpy, re-run the converter.
- A `python:` block runs the function named in report.txt, e.g. `py_reset_daily_visits_1`.
- `$ x = some_function()` calls `some_function` in `state.gd`.
- `renpy.vibrate(n)` buzzes the phone (if Vibration is on), `renpy.full_restart()` goes back to
  the title menu, `renpy.random.shuffle(x)` and `del x[...]` work as in Python.
- Tables that name functions, like `cafe_encounter_triggers`, are read from script.rpy too.

## Placing characters by hand

While playing from the Godot editor, press **F2**. The story pauses and you can:

- drag a character to move it
- use the arrow keys to nudge it 1 pixel (hold Shift for 10)
- press + or - (or scroll) to make it bigger or smaller

Press **F2** again to save and carry on. Positions go into `godot/sprite_positions.json`, one
entry per character, and replace the `config.tag_transform` values from Ren'Py. A `show ... at`
or a `show ...:` block in the script still moves a character for that one scene.
F2 does nothing in an exported game, so players never see it.

## Character sizes

As in Ren'Py, a `zoom` in the script multiplies the character's usual size:
`zoom 1.0` is the usual size, `zoom 2.0` a close-up at twice that, `zoom 0.5` a distant shot.
The usual size comes from `config.tag_transform` (or `sprite_positions.json`, see above).

`godot --headless --path godot res://tests/size_check.tscn` lists every character shown at an
unusual size, with its script line, so you can spot any that look wrong.

## How pictures are placed (same rules as Ren'Py)

- `show x` with no block: centred at the bottom, or the `config.tag_transform` spot.
- `show x:` with a block, when x is not on screen yet: anything the block leaves out starts
  at the top-left. So `xpos 1119 ypos 262` puts the picture's top-left corner there.
- `zorder` orders pictures among themselves; they always stay under the text box.
- `zpos` works with the 3D camera turned on in `label start` (closer = bigger).
- Effects: `blur`, `rotate`, `matrixcolor BrightnessMatrix(n)` and `SaturationMatrix(n)`.
- Pairs like `align (0.4, 0.85)` and `anchor (1.0, 1.0)`, and curves like `easeout_circ`.
- Pictures made of frames (`image kirako glitched:`), including `glitch("...", offset=n)`.
- `show x as copy` (a second copy under its own name), and `at atl_dizzy`, which is
  rebuilt by hand in story_player.gd (`_at_dizzy`) because it uses `choice` and `parallel`.
- Not copied: `knot` (curved paths, used once for the cherry); it moves in a straight line.
- `show screen x` puts a screen on top while the story carries on (the map tutorial uses this).

## Transitions

All the transitions in the story work, timed as in Ren'Py:
`dissolve`, `Dissolve(t)`, `fade`, `Fade(out, hold, in)`, `fadehold`, `pushleft` / `pushright`,
`Pixellate(t, steps)`, `vpunch`, `moveinleft` ... `moveoutbottom`, and
`MoveTransition(t, leave=offscreenright)`. Your own `define fadehold = Fade(...)` lines are used.
The screen-wide ones (dissolve, fade, push, pixellate) are drawn over the whole screen, so the
story waits for them; a tap skips to the end. A new `scene` hides the text box until the next
line, like Ren'Py's `window auto`.

## Menus: where everything lives

    Title menu      Start · Load* · Gallery · Settings · About
    In-game menu    Resume · Inventory* · Wardrobe · Save* · Load* · History* · Gallery · Settings · Main menu

Entries marked * have a place in the menu but show "not built yet".
To build one, make a scene and add it to `PAGES` in `screens/menu.gd`.

- Settings and gallery unlocks are saved on the device (`user://kept.json`) and survive restarts.
- `persistent.something` in the story reads and writes the same saved values.
- The gallery's text and unlock rules come from `characters` and the `gallery.button(...)`
  lines in screens.rpy, through the converter.
- `godot --path godot res://tests/menu_tour.tscn` walks through every menu by itself.
- `godot --path godot res://tests/wardrobe_tour.tscn` fills the closet and tries every wardrobe view.
- The wardrobe opens from the bedroom dresser and from the in-game menu.

## Test without clicking

    godot --path godot res://tests/autoplay.tscn -- label=next_morning choices=1,1,0,0,1 \
        route=ginza_small,imperial_theatre,imperial_theatre,end_day \
        unlock_imp_th=true money=10 'encounters={"musician":1,"merchant":0,"doctor":0,"fighter":0,"soldier":0}'

This plays one whole day (morning, map, theatre twice, bedroom, next morning) and prints it.

Screens that have an `autoplay()` function (the two cafe screens) play themselves in this
test. This one works two cafe shifts and goes to bed:

    godot --path godot res://tests/autoplay.tscn -- label=next_morning tutorial_mode=false \
        choices=0,0,0 route=end_day

## Not built yet

- Shops, shrine and inventory screens (placeholders for now). Until the shops are built,
  Naomi only owns her waitress dress and geta, so the wardrobe shelves are nearly empty in play.
- Save / load, history, skip and auto-forward
- Lipstick tint on Naomi's side picture; blur, brightness, glitch and `zpos` effects
- Transitions other than fades and move in/out (they happen instantly)
