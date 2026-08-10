## Drag and Drop screen  ###############################################################
## This screen is for the drag and drop game

default served_food = 0 

init python:
        
    def food_served(dropped_on, dragged_food):
        global served_food
        
        if dragged_food[0].drag_name == dropped_on.drag_name:
            dragged_food[0].snap(dropped_on.x,dropped_on.y)
            dragged_food[0].draggable = False
            dragged_food[0].set_child(im.FactorScale(dragged_food[0].child,0.2,0.2))
            served_food += 1
            if served_food == 3 and tutorial_mode == True:
                served_food = 0
                renpy.jump("re_explain_cafegame")
            elif served_food == 3:
                served_food = 0
                renpy.jump("after_work_cafe")

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
    
    default customer_table = [0.0,0.5,1.0]
    default customer_order = [" please.",", thank you."," for me."]
    
    python:
        renpy.random.shuffle(customer_table)
        renpy.random.shuffle(customer_order)

        order0_time = renpy.random.randint(1,3)
        order1_time = renpy.random.randint(1,3)
        order2_time = renpy.random.randint(1,3)

    # Render background
    image im.Scale("images/cafe/caferight.png", 1920, 1080)

    if tutorial_mode == True:

        python:
            order0_time = renpy.random.randint(4,5)
            order1_time = renpy.random.randint(4,5)
            order2_time = renpy.random.randint(4,5)
        
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
    
    # Display dishes randomly
    draggroup:
        # Left dish
        drag:
            align(customer_table[0], 1.0)
            drag_name cafe_menu[0]
            image im.Scale("images/cafe/"+cafe_menu[0]+".png",640,315)
            drag_raise True
        drag:
            drag_name cafe_menu[0]
            draggable False
            droppable True
            dropped food_served
            align (0.22,0.55)
            image "images/cafe/"+cafe_menu[0]+".png" xzoom 0.1 yzoom 0.1 alpha 0.0
        # Middle dish
        drag:
            align(customer_table[1], 1.0)
            drag_name cafe_menu[1]
            drag_raise True
            image im.Scale("images/cafe/"+cafe_menu[1]+".png",640,315)
        drag:
            drag_name cafe_menu[1]
            draggable False
            droppable True
            dropped food_served
            align (0.5,0.55) 
            image "images/cafe/"+cafe_menu[1]+".png" xzoom 0.1 yzoom 0.1 alpha 0.0
        # Right dish
        drag:
            align(customer_table[2], 1.0)
            drag_name cafe_menu[2]
            drag_raise True
            image im.Scale("images/cafe/"+cafe_menu[2]+".png",640,315)
        drag:
            drag_name cafe_menu[2]
            draggable False
            droppable True
            dropped food_served
            align (0.8,0.55)
            image "images/cafe/"+cafe_menu[2]+".png" xzoom 0.1 yzoom 0.1 alpha 0.0

    # Customer speech bubbles
    # Left customer
    image "images/speech.png" xalign 0.24 yalign 0.24 zoom 0.5 at transform:
        alpha 0.0 xzoom -1.0
        pause order0_time
        easein 2.0 alpha 1.0
        easeout 1.0 alpha 0.0
    hbox:
        xalign 0.25
        yalign 0.25
        box_wrap True
        xmaximum 350
        text cafe_menu[0] + customer_order[0] textalign 0.5 yalign 0.5 size 40 at transform:
            alpha 0.0 
            pause order0_time
            easein 2.0 alpha 1.0
            easeout 1.0 alpha 0.0
    # Middle customer
    image "images/speech.png" xalign 0.55 yalign 0.24 zoom 0.5 at transform:
            alpha 0.0 xzoom -1.0
            pause order1_time
            easein 2.0 alpha 1.0
            easeout 1.0 alpha 0.0
    hbox:
        xalign 0.55
        yalign 0.26
        box_wrap True
        xmaximum 350
        text cafe_menu[1] + customer_order[1] textalign 0.5 yalign 0.5 size 40 at transform:
            alpha 0.0
            pause order1_time
            easein 2.0 alpha 1.0
            easeout 1.0 alpha 0.0
    # Right customer
    image "images/speech.png" xalign 0.80 yalign 0.24 zoom 0.5 at transform:
            alpha 0.0 
            pause order2_time
            easein 2.0 alpha 1.0
            easeout 1.0 alpha 0.0
    hbox:
        xalign 0.785
        yalign 0.265
        box_wrap True
        xmaximum 350
        text cafe_menu[2] + customer_order[2] textalign 0.5 yalign 0.5 size 40 at transform:
            alpha 0.0
            pause order2_time
            easein 2.0 alpha 1.0
            easeout 1.0 alpha 0.0