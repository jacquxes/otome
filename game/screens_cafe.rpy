## Drag and Drop screen  ###############################################################
## This screen is for the drag and drop game

default served_food = 0
default shift_tips = 0      # tips earned this shift (added to money in the labels after the game)

# These are re-rolled at the start of every round by setup_cafe_round()
default customer_table = [0.0, 0.5, 1.0]
default customer_order = [" please.", ", thank you.", " for me."]
default order_times = [1, 1, 1]

define TIP_MIN = 4          # smallest tip for serving the right dish
define TIP_MAX = 6          # biggest tip for serving the right dish
define TIP_PENALTY = 3      # tip lost for taking a dish to the wrong table

define TABLE_X = [0.22, 0.5, 0.8]   # where the three tables are (same as the drop targets)

define RIGHT_LINES = ["Thank you!", "Looks lovely.", "Just what I wanted."]
define WRONG_LINES = ["Hm? This isn't mine.", "I didn't order this...", "Wrong table, I think."]

define ORDER_COLOR = "#3b2a1a"     # dark brown for customer orders

transform order_pop(delay):
    # Same rise-and-fade as the feedback, but waits 'delay' seconds first
    alpha 0.0 yoffset 20
    pause delay
    easein 0.4 alpha 1.0 yoffset 0
    pause 1.6
    easeout 1.0 alpha 0.0 yoffset -20

transform feedback_pop:
    alpha 0.0 yoffset 20
    easein 0.2 alpha 1.0 yoffset 0
    pause 0.9
    easeout 0.4 alpha 0.0 yoffset -20

init python:

    def setup_cafe_round():
        # Call this ONCE, right before the cafe_game screen is shown.
        global customer_table, customer_order, order_times, served_food, shift_tips

        customer_table = [0.0, 0.5, 1.0]
        customer_order = [" please.", ", thank you.", " for me."]
        renpy.random.shuffle(customer_table)
        renpy.random.shuffle(customer_order)

        if tutorial_mode:
            # Kirako leaves at about 4.5s, so start after that and space them out.
            # Shuffled, so who orders first is still random.
            order_times = [5.0, 6.5, 8.0]
            renpy.random.shuffle(order_times)
        else:
            order_times = [renpy.random.randint(1, 3) for i in range(3)]

        served_food = 0
        shift_tips = 0

    def send_dish_home(dish):
        # Slide a dish back to where it started at the bottom of the screen.
        i = cafe_menu.index(dish.drag_name)
        home_x = int(customer_table[i] * (1920 - 640))
        home_y = 1080 - 315
        dish.snap(home_x, home_y, 0.2)

    def show_feedback(table, line, tip_text, color):
        tag = "cafe_feedback_" + str(table)
        renpy.show_screen("cafe_feedback", line, tip_text, color, TABLE_X[table], tag, _tag=tag)

    def dish_dropped(drags, drop):
        global served_food, shift_tips
        dish = drags[0]

        # Let go over empty space: send it back, no penalty
        if drop is None:
            send_dish_home(dish)
            return

        table = cafe_menu.index(drop.drag_name)

        if dish.drag_name == drop.drag_name:
            # Right table
            dish.snap(drop.x, drop.y)
            dish.draggable = False
            dish.set_child(im.FactorScale(dish.child, 0.2, 0.2))
            served_food += 1
            tip = renpy.random.randint(TIP_MIN, TIP_MAX)
            shift_tips += tip
            show_feedback(table, renpy.random.choice(RIGHT_LINES), "+" + str(tip), "#2e7d32")

            # Shift finished: tips can't end below zero, so money never goes down
            if served_food == 3:
                shift_tips = max(0, shift_tips)

        else:
            # Wrong table
            send_dish_home(dish)
            shift_tips -= TIP_PENALTY
            show_feedback(table, renpy.random.choice(WRONG_LINES), "-" + str(TIP_PENALTY), "#990000")

        # Redraw the screen so the tip counter and end-of-round timer update
        renpy.restart_interaction()

screen cafe_feedback(line, tip_text, color, x, tag):

    zorder 3

    vbox:
        at feedback_pop
        xalign x
        yalign 0.40
        spacing 4
        text line size 40 color color xalign 0.5 outlines [(3, "#ffffff", 0, 0)]
        if tip_text:
            text tip_text size 52 color color xalign 0.5 bold True outlines [(3, "#ffffff", 0, 0)]

    timer 1.5 action Hide(tag)

screen cafe_menu:

    zorder 2
    modal True

    # Render background
    image im.Scale("images/cafe/caferight.png", 1920, 1080)

    if tutorial_mode == True:

        # Kirako appears
        image "images/kirako/kirako happy.png" at transform:
            xpos -0.05 ypos 0.0 zoom 0.5
        
        # Display table
        image im.Scale("images/cafe/table_right.png",1920,1080)

    # Show menu image
    image "images/cafe/cafemenu.png" at transform:
        xpos 0.30 zoom 0.5

    if tutorial_mode == True:

        # Cue Kirako's instructions after she appears
        image "images/speech.png" xalign 0.20 yalign 0.5 zoom 0.5 at transform:
            alpha 0.0 yzoom -1.0 xzoom -1.0
            pause 0.6
            alpha 1.0
        hbox:
            xalign 0.21
            yalign 0.525
            box_wrap True
            xmaximum 370
            text "Choose three items for today's menu." textalign 0.5 yalign 0.5 size 40 at transform:
                alpha 0.0
                pause 0.6
                alpha 1.0

    vbox:
        xpos 0.50
        ypos 0.4
        for item in unlocked_menu:
            textbutton item.title():
                action If(
                    item in cafe_menu,
                    true=Function(cafe_menu.remove, item),
                    false=Function(cafe_menu.append, item)
                )
                sensitive (item in cafe_menu or len(cafe_menu) < 3)
                selected (item in cafe_menu)
                text_font "Staatliches-Regular.ttf"
                text_size 72
                text_selected_color "#990000"

        textbutton "Confirm":
            action [Hide("cafe_menu"), Jump("cafe_game")]
            sensitive (len(cafe_menu) == 3)
            text_font "Staatliches-Regular.ttf"
            text_size 100
            xminimum 400
            yminimum 80
            top_margin 20

screen cafe_game:

    zorder 2
    modal True

    # Render background
    image im.Scale("images/cafe/caferight.png", 1920, 1080)

    if tutorial_mode == True:

        # Kirako appears
        image "images/kirako/kirako happy.png" at transform:
            xpos -0.05 ypos 0.0 zoom 0.5
            pause 4.0
            easeout 0.5 xpos -1.0
        
        # Display table
        image im.Scale("images/cafe/table_right.png",1920,1080)

        # Cue Kirako's instructions after she appears
        image "images/speech.png" xalign 0.20 yalign 0.5 zoom 0.5 at transform:
            alpha 0.0 yzoom -1.0 xzoom -1.0
            pause 0.6
            alpha 1.0
            pause 3.5
            alpha 0.0
        hbox:
            xalign 0.21
            yalign 0.525
            box_wrap True
            xmaximum 370
            text "Please bring the food to the correct table!" textalign 0.5 yalign 0.5 size 40 at transform:
                alpha 0.0
                pause 0.6
                alpha 1.0
                pause 3.5
                alpha 0.0

    # Tip counter
    text "Tips: [shift_tips]" xalign 0.97 yalign 0.03 size 56 font "Staatliches-Regular.ttf" outlines [(3, "#ffffff", 0, 0)] color "#000000"
    
    # Display dishes randomly
    draggroup:
        # Left dish
        drag:
            align(customer_table[0], 1.0)
            drag_name cafe_menu[0]
            image im.Scale("images/cafe/"+cafe_menu[0]+".png",640,315)
            drag_raise True
            droppable False
            dragged dish_dropped
        drag:
            drag_name cafe_menu[0]
            draggable False
            droppable True
            align (0.22,0.55)
            image "images/cafe/"+cafe_menu[0]+".png" xzoom 0.1 yzoom 0.1 alpha 0.0
        # Middle dish
        drag:
            align(customer_table[1], 1.0)
            drag_name cafe_menu[1]
            drag_raise True
            droppable False
            dragged dish_dropped
            image im.Scale("images/cafe/"+cafe_menu[1]+".png",640,315)
        drag:
            drag_name cafe_menu[1]
            draggable False
            droppable True
            align (0.5,0.55) 
            image "images/cafe/"+cafe_menu[1]+".png" xzoom 0.1 yzoom 0.1 alpha 0.0
        # Right dish
        drag:
            align(customer_table[2], 1.0)
            drag_name cafe_menu[2]
            drag_raise True
            droppable False
            dragged dish_dropped
            image im.Scale("images/cafe/"+cafe_menu[2]+".png",640,315)
        drag:
            drag_name cafe_menu[2]
            draggable False
            droppable True
            align (0.8,0.55)
            image "images/cafe/"+cafe_menu[2]+".png" xzoom 0.1 yzoom 0.1 alpha 0.0

    # Customer orders (same text style as the feedback, staggered by order_times)
    # Left customer
    text cafe_menu[0] + customer_order[0]:
        at order_pop(order_times[0])
        xalign 0.25 yalign 0.25 xmaximum 350
        textalign 0.5 size 40 color ORDER_COLOR outlines [(3, "#ffffff", 0, 0)]
    # Middle customer
    text cafe_menu[1] + customer_order[1]:
        at order_pop(order_times[1])
        xalign 0.55 yalign 0.25 xmaximum 350
        textalign 0.5 size 40 color ORDER_COLOR outlines [(3, "#ffffff", 0, 0)]
    # Right customer
    text cafe_menu[2] + customer_order[2]:
        at order_pop(order_times[2])
        xalign 0.785 yalign 0.25 xmaximum 350
        textalign 0.5 size 40 color ORDER_COLOR outlines [(3, "#ffffff", 0, 0)]

    # All three served: wait a moment so the last "Thank you!" is visible, then move on
    if served_food == 3:
        timer 1.5 action Jump("re_explain_cafegame" if tutorial_mode else "after_work_cafe")
