# The script of the game goes in this file.

# Flag for language
default jp_lang = False

define naomi_cheek_rgb = {"blush_pink":[1.7,1.0,1.7],"blush_orange":[1.0,1.0,1.0]}
define naomi_eye_rgb = {"shadow_blue":[0.6,0.8,1.0],"shadow_brown":[1.0,0.8,0.9],"shadow_orange":[1.1,1.1,1.0],"shadow_pink":[1.2,0.9,1.3]}
define naomi_lip_hsv = {"stick_pink":[-12,0.75,0.11],"stick_red":[-4,1.25,-0.3],"stick_orange":[0,1.0,0],"stick_peach":[-2,0.8,0.1]}

default cheek_color_r = 1.5
default cheek_color_g = 1.5
default cheek_color_b = 1.5

default eye_color_r = 1.15
default eye_color_g = 1.2
default eye_color_b = 1.2

default lip_color_h = 14
default lip_color_s = 0.85
default lip_color_v = 0.15

init python:

    # Create the functions to make Naomi's side image makeup dynamic
    def naomi_cheek_color(st,at,cheek):
        return im.MatrixColor(cheek, im.matrix.tint(cheek_color_r,cheek_color_g,cheek_color_b)), None
    
    def naomi_eye_color(st,at,eye):
        return im.MatrixColor(eye, im.matrix.tint(eye_color_r,eye_color_g,eye_color_b)), None

    def naomi_lip_color(st,at,lip):
        return im.MatrixColor(lip, im.matrix.hue(lip_color_h)*im.matrix.saturation(lip_color_s)*im.matrix.brightness(lip_color_v)), None

    # Glitch effect - https://github.com/Gouvernathor/renpy-ChromaGlitch
    class glitch(renpy.Displayable):
        """
        `randomkey`
            Follows the rules of the random modume's seed function.
            If not set, a random seed is generated when the transform is applied,
            and stays the same afterwards.
            If you want the effect to be random for each render operation, set to None.

        `chroma`
            Boolean, whether to apply the chromatic aberration effect.

        `minbandheight`
            Minimum height of each slice.

        `offset`
            The offset of each slice will be between -offset and offset pixels.

        `nslices`
            Number of slicings to do (the number of slices will be nslices + 1).
            Setting this to 0 is not supported.
            None (the default) makes it random.
        """

        NotSet = object()

        def __init__(self, child, *, randomkey=NotSet, chroma=True, minbandheight=1, offset=30, nslices=None, **properties):
            super().__init__(**properties)
            self.child = renpy.displayable(child)
            if randomkey is self.NotSet:
                randomkey = renpy.random.random()
            self.randomkey = randomkey
            self.chroma = chroma
            self.minbandheight = minbandheight
            self.offset = offset
            self.nslices = nslices

        def render(self, width, height, st, at):
            child = self.child
            child_render = renpy.render(child, width, height, st, at)
            cwidth, cheight = child_render.get_size()
            if not (cwidth and cheight):
                return child_render
            render = renpy.Render(cwidth, cheight)
            randomobj = renpy.random.Random(self.randomkey)
            chroma = self.chroma and renpy.display.render.models
            offset = self.offset
            minbandheight = self.minbandheight
            nslices = self.nslices
            if nslices is None:
                nslices = min(int(cheight/minbandheight), randomobj.randrange(10, 21))

            theights = sorted(randomobj.randrange(int(cheight)+1) for k in range(nslices)) # y coordinates demarcating all the strips
            offt = 0 # next strip's lateral offset
            fheight = 0 # sum of the size of all the strips added this far
            while fheight<cheight:
                # theight is the height of this particular strip
                if theights:
                    theight = max(theights.pop(0)-fheight, minbandheight)
                else:
                    theight = cheight-theight

                slice_render = child_render.subsurface((0, fheight, cwidth, theight))

                if offt and chroma:
                    for color_mask, chponder in (((False, False, True, True), 1.25), ((False, True, False, True), 1.), ((True, False, False, True), .75)):
                        chroma_render = slice_render.subsurface((0, 0, cwidth, theight))
                        chroma_render.add_property("gl_color_mask", color_mask)
                        render.blit(chroma_render, (round(offt*chponder), round(fheight)))

                else:
                    render.blit(slice_render, (offt, round(fheight)))

                fheight += theight
                if offt:
                    offt = 0
                else:
                    offt = randomobj.randrange(-offset, offset+1)

            return render

        def visit(self):
            return [self.child]

# Declare main character and set up layered image to customise display
define naomi = Character("Naomi", image="naomi", color="#702b00")
define config.side_image_tag = "naomi"
define config.tag_transform["naomi"] = Transform(zoom=0.5)
layeredimage side naomi:
    ## This will be her expressions. Filename must be side_naomi_base_[expression]
    group base auto:
        zoom 0.5
        attribute happy default
    ## This is for her blush. Filename must be side_naomi_blush_[expression]
    group blush auto:
        zoom 0.5
        attribute happy default:
            DynamicDisplayable(naomi_cheek_color, cheek="images/side/side_naomi_blush_happy.png")
        attribute angry:
            DynamicDisplayable(naomi_cheek_color, cheek="images/side/side_naomi_blush_angry.png")
        attribute blush:
            DynamicDisplayable(naomi_cheek_color, cheek="images/side/side_naomi_blush_blush.png")
        attribute relieved:
            DynamicDisplayable(naomi_cheek_color, cheek="images/side/side_naomi_blush_relieved.png")
        attribute sleepy:
            DynamicDisplayable(naomi_cheek_color, cheek="images/side/side_naomi_blush_sleepy.png")
        attribute smirk:
            DynamicDisplayable(naomi_cheek_color, cheek="images/side/side_naomi_blush_smirk.png")
        attribute surprised:
            DynamicDisplayable(naomi_cheek_color, cheek="images/side/side_naomi_blush_surprised.png")
        attribute thinking:
            DynamicDisplayable(naomi_cheek_color, cheek="images/side/side_naomi_blush_thinking.png")
        attribute troubled:
            DynamicDisplayable(naomi_cheek_color, cheek="images/side/side_naomi_blush_troubled.png")
    ## This is for her eyeshadow. Filename must be side_naomi_eye_[expression]
    group eye auto:
        zoom 0.5
        attribute happy default:
            DynamicDisplayable(naomi_eye_color, eye="images/side/side_naomi_eye_happy.png")
        attribute angry:
            DynamicDisplayable(naomi_eye_color, eye="images/side/side_naomi_eye_angry.png")
        attribute blush:
            DynamicDisplayable(naomi_eye_color, eye="images/side/side_naomi_eye_blush.png")
        attribute relieved:
            DynamicDisplayable(naomi_eye_color, eye="images/side/side_naomi_eye_relieved.png")
        attribute sleepy:
            DynamicDisplayable(naomi_eye_color, eye="images/side/side_naomi_eye_sleepy.png")
        attribute smirk:
            DynamicDisplayable(naomi_eye_color, eye="images/side/side_naomi_eye_smirk.png")
        attribute surprised:
            DynamicDisplayable(naomi_eye_color, eye="images/side/side_naomi_eye_surprised.png")
        attribute thinking:
            DynamicDisplayable(naomi_eye_color, eye="images/side/side_naomi_eye_thinking.png")
        attribute troubled:
            DynamicDisplayable(naomi_eye_color, eye="images/side/side_naomi_eye_troubled.png")
    ## This is for her lipstick. Filename must be side_naomi_lip_[expression]
    group lip auto:
        zoom 0.5
        attribute happy default:
            DynamicDisplayable(naomi_lip_color, lip="images/side/side_naomi_lip_happy.png")
        attribute angry:
            DynamicDisplayable(naomi_lip_color, lip="images/side/side_naomi_lip_angry.png")
        attribute blush:
            DynamicDisplayable(naomi_lip_color, lip="images/side/side_naomi_lip_blush.png")
        attribute relieved:
            DynamicDisplayable(naomi_lip_color, lip="images/side/side_naomi_lip_relieved.png")
        attribute sleepy:
            DynamicDisplayable(naomi_lip_color, lip="images/side/side_naomi_lip_sleepy.png")
        attribute smirk:
            DynamicDisplayable(naomi_lip_color, lip="images/side/side_naomi_lip_smirk.png")
        attribute surprised:
            DynamicDisplayable(naomi_lip_color, lip="images/side/side_naomi_lip_surprised.png")
        attribute thinking:
            DynamicDisplayable(naomi_lip_color, lip="images/side/side_naomi_lip_thinking.png")
        attribute troubled:
            DynamicDisplayable(naomi_lip_color, lip="images/side/side_naomi_lip_troubled.png")
    ## Hair layer
    always:
        "side/side_naomi_[naomi_hair].png" zoom 0.5
    ## Dress layer
    always:
        "side/side_naomi_[naomi_dress].png" zoom 0.5

# Declare other characters used by this game. The color argument colorizes the
# name of the character.
define cat = Character("[cat_name]", color="#000000")
define config.tag_transform["cat"] = Transform(zoom=0.6, xalign=0.85)
define kirako = Character("[kirako_name]",image="kirako", color="#8f3d65")
define config.tag_transform["kirako"] = Transform(zoom=0.5, xalign=0.5)

define musician = Character("[musician_name]",image="musician", color="#4a5764")
define config.tag_transform["musician"] = Transform(zoom=0.5)
define merchant = Character("[merchant_name]",image="merchant", color="#151224")
define config.tag_transform["merchant"] = Transform(zoom=0.55)
define doctor = Character("[doctor_name]",image="doctor", color = "#006337")
define config.tag_transform["doctor"] = Transform(zoom=0.5)
define soldier = Character("[soldier_name]",image="soldier")
define fighter = Character("[fighter_name]",image="fighter")
define config.tag_transform["fighter"] = Transform(zoom=0.5)

define staff = Character("[dept_name]",image="staff", color="#000000")
define config.tag_transform["staff"] = Transform(zoom=0.5)
define staff_bubble = Character(None,image="staff", kind=bubble)

define miko = Character("Shrine Maiden", image="miko", color="#000000")
define miko_bubble = Character(None,image="miko", kind=bubble)

define nurse = Character("Nurse", image="nurse", color="#000000")
define config.tag_transform["nurse"] = Transform(zoom=0.6)

define ticketer = Character("Ticket Staff", color="#000000")
define customer = Character("Customer", color="#000000")
define fan = Character("Fan", color='#000000')

define stranger = Character("Stranger",image="stranger")
define config.tag_transform["stranger"] = Transform(zoom=0.5)

# ============================================
# CAFE MENU
# ============================================
default unlocked_menu = ["Pudding", "Coffee", "Cake"]
default cafe_menu = []  # today's selected specials (max 3)

default all_menu = {
    "Pudding": True,
    "Coffee": True,
    "Cake": True,
    "Katsudon": False,
    "Omurice": False,
    "Curry": False,
    "Steak": False,
}

# ============================================
# CHARACTERS
# ============================================
default unlocked_chars = ["musician", "doctor"]

default item_to_character = {
    "Pudding": "musician",
    "Cake": "doctor",
    "Steak": "merchant",
    "Katsudon": "fighter",
    "Omurice": "soldier",
    "Coffee": ["musician", "doctor", "merchant", "fighter", "soldier"],
    "Curry": ["soldier", "merchant", "fighter"],
}

# Story/key-scene progression counters
default encounters = {
    "musician": 0,
    "merchant": 0,
    "doctor": 0,
    "fighter": 0,
    "soldier": 0,
}

default location_visits = {
    "theatre": 0,
    "hospital": 0,
    "office": 0,
    "dojo": 0,
    "station": 0,
}

# Total interactions (key scenes + casual visits) - used for balancing
default total_visits = {
    "musician": 0,
    "merchant": 0,
    "doctor": 0,
    "fighter": 0,
    "soldier": 0,
}

# Tracks if a char already visited today
default visited_today = {
    "musician": False,
    "merchant": False,
    "doctor": False,
    "fighter": False,
    "soldier": False,
}

# Cafe encounters that override casual visits
# format: { char: { encounter_number: required_menu_item } }
default cafe_encounter_triggers = {
    "musician": {
        0: {"item": "Pudding", "condition": None},
        4: {"item": "Pudding", "condition": None},
        6: {"item": "Pudding", "condition": None},
        9: {"item": "Pudding", "condition": musician_9_condition},
        11: {"item": "Pudding", "condition": musician_11_condition},
    },
    "doctor": {
        0: {"item": "Cake", "condition": None}
    },
    "merchant": {
        1: {"item": "Coffee", "condition": None}
    }
    # simple item-only example:
    # "doctor": {3: {"item": "Cake", "condition": None}},
}

# Tuning
define CATCHUP_CHANCE = 0.25


# ============================================
# RELATIONSHIP STAGE
# ============================================
init python:

    def add_point(char):
        relationship_points[char] = min(relationship_points[char] + 1, 15)

    def get_stage(char):
        pts = relationship_points[char]
        if pts >= 13: return 5
        if pts >= 10: return 4
        if pts >= 6:  return 3
        if pts >= 3:  return 2
        if pts >= 1:  return 1
        return 0

    def calc_demographics():
        total = sum(get_stage(c) for c in relationship_points)
        return min(int(total * (30.0 / 25.0)), 30)

default relationship_points = {
    "musician": 0,
    "doctor":   0,
    "merchant": 0,
    "fighter":  0,
    "soldier":  0,
}


# ============================================
# STORY FLAGS
# ============================================

default story_flags = {}

init python:
    def flag(name):
        return story_flags.get(name, False)

    def set_flag(name):
        story_flags[name] = True

# Set the flags for items in the game
default item1 = False
default tutorial_mode = True
default unlock_imp_th = False
default unlock_off_bldg = False
default unlock_hosp = False
default unlock_dojo = False
default unlock_movie_th = False
default musician_affection = 0
default musician_courage = 0
default musician_job = 0
default musician_choice = 0
default musician_event = 0
default musician_dream = False
default musician_ending = False
default merchant_affection = 0
default merchant_courage = 0
default merchant_job = 0
default merchant_choice = 0
default merchant_event = False
default merchant_dream = False
default merchant_ending = False
default fighter_affection = 0
default doctor_affection = 0
default doctor_courage = 0
default doctor_job = 0
default doctor_choice = 0
default doctor_event = False
default doctor_dream = False
default doctor_ending = False

# Flags to enable events
default enable_doctor_event_1 = False
default musician_show_seen = False
default musician_ticketer_talk_seen = False
default pre_musician_event_1 = False
default pre_musician_event_2 = False
default enable_merchant_event_1 = False
default musician_5_seen = False


# ============================================
# MUSICIAN FLAGS
# ============================================

define MUSICIAN_INTRO_GAP = 1

# Condition functions for musician encounters
init python:

    def _musician_day_gate(flag_key, gap=None):
        if gap is None:
            gap = MUSICIAN_INTRO_GAP
        last_day = story_flags.get(flag_key, -9999)
        return (last_day - totaldays) >= gap

    def musician_8_gate():
        return _musician_day_gate("musician_1_day")

    def musician_8_ready():
        return relationship_points["musician"] >= 3 and not flag("musician_show_seen")

    def musician_show_today():
        return dayofweeknumber == 6 and musician_event == 1 and totaldays <= 16

    def musician_casual_paused():
        show_window = (flag("musician_show_seen") or musician_show_today()) and encounters["musician"] < 10
        return show_window or musician_tower_today()

    def musician_9_condition():
        return flag("musician_ticketer_talk_seen")

    def musician_9_blocked():
        encounters["musician"] += 1

    def musician_9_branch():
        days_since_9 = story_flags.get("musician_9_day", -9999) - totaldays
        return "musician_9a" if days_since_9 <= 2 else "musician_9b"

    def musician_11_condition():
        return totaldays >= 3

    def musician_tower_today():
        return dayofweeknumber == 7 and musician_event == 3

    musician_encounter_table = {
        1: {"label": "musician_1"},
        3: {"label": "musician_3"},
        5: {"label": "musician_5"},
        7: {"label": "musician_7"},
        8: {"condition": musician_8_ready, "label": "musician_8"},
        10: {"branch": musician_9_branch},
    }

    def get_musician_action():
        entry = musician_encounter_table.get(encounters["musician"])
        if not entry:
            return None
        if "branch" in entry:
            return entry["branch"]()
        condition = entry.get("condition")
        if condition is None or condition():
            return entry["label"]
        elif "on_blocked" in entry:
            entry["on_blocked"]()
        return None

# ============================================
# ITEMS
# ============================================

# Inventory list
default inventory = {}
default stationery = ["pen","notebook"]
#default stationery = [["Pen",15,"An exquisitely made fountain pen with a firm grip."],["Notebook",5,"A brightly illustrated notebook with creamy lined pages for a comfortable writing experience."]]
default clothes = ["dress_cute","dress_hakama","dress_modern","dress_flapper","dress_prim"]
default accessories = ["hair_band","hair_hat","hair_flower","hair_ribbon","hair_bow","hand_round","hand_evening","hand_straw","hand_parasol","shoes_koppori","shoes_zori","shoes_heels","shoes_pumps","shoes_boots"]
default accessories2 = {"hair_band":[1584,440],"hair_hat":[1565,335],"hair_flower":[1484,620],"hair_ribbon":[1342,484],"hair_bow":[1608,700]}
default cosmetics = ["shadow_blue","shadow_brown","shadow_pink","shadow_orange","blush_pink","blush_orange","stick_pink","stick_orange","stick_red","stick_peach"]
default omamori = []
default o_charisma = 1
default o_intelligence = 1
default o_job = 1
default o_love = 1
default o_money = 1
default o_strength = 1

# Wardrobe list
default wardrobe_dress = ["dress_waitress"]
default wardrobe_shoes = ["shoes_geta"]
default wardrobe_hair = {}
default wardrobe_accessories = []
default wardrobe_eye = []
default wardrobe_cheek = []
default wardrobe_lip = []
default wardrobe_parasol = []
default naomi_dress = "dress_waitress"
default naomi_shoes = "shoes_geta"
default naomi_hair = "hair_base"
default naomi_accessories_left = ""
default naomi_accessories_right = ""
default naomi_cheek = ""
default naomi_eye = ""
default naomi_lip = ""

# Define images in inventory
image merchant_namecard = "images/merchant/namecard_flat.png"
image merchant_namecard_front = "images/inventory/namecard.png"
image omamori_charisma = Transform("images/inventory/omamori_charisma.png",zoom=0.1)
image omamori_intelligence = Transform("images/inventory/omamori_intelligence.png",zoom=0.1)
image omamori_job = Transform("images/inventory/omamori_job.png",zoom=0.1)
image omamori_love = Transform("images/inventory/omamori_love.png",zoom=0.1)
image omamori_money = Transform("images/inventory/omamori_money.png",zoom=0.1)
image omamori_strength = Transform("images/inventory/omamori_strength.png",zoom=0.1)
image ticket_back_new = Transform("images/inventory/ticket_back_new.png",zoom=0.2)
image ticket_back_used = Transform("images/inventory/ticket_back_used.png",zoom=0.2)
image ticket_front_new = Transform("images/inventory/ticket_front_new.png",zoom=0.2)
image ticket_front_used = Transform("images/inventory/ticket_front_used.png",zoom=0.2)

# Define and resize bg images
image bg opening 1 = Transform("images/bg opening 1.png",zoom=0.5)
image bg opening 2 = Transform("images/bg opening 2.png",zoom=0.5)
image bg cafeleft = im.Scale("images/cafe/cafeleft.png", 1920, 1080)
image bg caferight = im.Scale("images/cafe/caferight.png", 1920, 1080)
image bg dept = im.Scale("images/bg dept.png", 1920, 1080)
image bg bedroom = im.Scale("images/bg bedroom.png",1920,1080)
image bg office = im.Scale("images/bg office.png",1920,1080)
image bg hospital = im.Scale("images/bg hospital.png",1920,1080)
image bg imperial theatre = im.Scale("images/bg imperial theatre.png",1920,1080)
image bg ryounkaku = Transform("images/bg ryounkaku.png",zoom=0.5)
image bg dancehall 1 = im.Scale("images/bg dancehall 1.png",1920,1080)
image bg dancehall 2 = im.Scale("images/bg dancehall 2.png",1920,1080)
image bg irl = im.Scale("images/bg irl.png",1920,1080)
image bg movie = im.Scale("images/bg movie.png",1920,1080)
image bg movie theatre = im.Scale("images/bg movie theatre.png",1920,1080)

# Define cutscene images, thumbnails and set flags
image merchant_cutscene_1 = im.Scale("images/merchant/merchant_cutscene_1.png",1920,1080)
default persistent.merchant_cutscene_1_unlocked = False
image merchant_cutscene_2 = im.Scale("images/merchant/merchant_cutscene_2.png",1920,1080)
default persistent.merchant_cutscene_2_unlocked = False
image merchant_cutscene_3 = im.Scale(im.Crop("images/merchant/merchant_cutscene_3.png", (0, 0, 1024, 576)),1920,1080)
image musician_cutscene_11 = im.Scale("images/musician/musician_cutscene_11.png",1920,1080)
image musician_cutscene_12 = im.Scale("images/musician/musician_cutscene_12.png",1920,1080)
default persistent.musician_cutscene_1_unlocked = False
image musician_cutscene_2 = im.Scale("images/musician/musician_cutscene_2.png",1920,1080)
default persistent.musician_cutscene_2_unlocked = False
image musician_cutscene_3 = im.Scale("images/musician/musician_cutscene_3.png",1920,1080)
image doctor_cutscene_2 = im.Scale("images/doctor/doctor_cutscene_2.png",1920,1080)
image doctor_cutscene_3 = im.Scale("images/doctor/doctor_cutscene_3.png",1920,1080)

# Define assets used in scenes
image fans = im.Scale("images/musician/fans.png",1920,1080)
image fans_less = im.Scale("images/musician/fans_less.png",1920,1080)

# Set the number of days in the game
default dayofweek = "Monday"
default dayofweeknumber = 1
default totaldays = 28

# Set day cycle
default timeslot = 2
default timeofday = "Morning"

# Set the stat values in the game
default money = 0
default strength = 0
default charisma = 0

# Transforms for double vision effect
transform atl_dizzy(x=0.5, y=1.0, xa=0.5, ya=1.0, a=1.0, t=0.4, z=1.05):
    alpha 1.0 rotate 0.0 zoom 1.0
    xpos x ypos y
    xanchor xa yanchor ya
    transform_anchor True
    choice:
        parallel:
            ease t rotate a
        parallel:
            linear t alpha 0.5 zoom z blur 5.0
        ease t xalign 0.55 rotate -a
    choice:
        parallel:
            ease t rotate -a
        parallel:
            linear t alpha 0.5 zoom z blur 5.0
        ease t xalign 0.45 rotate a 
    linear t rotate 0.0 alpha 0 zoom 1.0 xalign 0.5

# Haptics (Android only)
define persistent.haptics_enabled = True

# The game starts here.

label start:

    # Enable camera
    camera:
        perspective True
    
    # Jump to opening sequence
    $ day_display = False
    jump opening_sequence
    


# This ends the game.
return

