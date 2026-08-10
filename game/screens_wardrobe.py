## Wardrobe screen ###############################################################
## This screen is for the player to switch the character's outfits

default naomi_wear = ""

init python:
    
    def wear_clothes(dropped_on, dragged_clothes):
        global naomi_wear
        # if dragged_clothes[0].drag_name == dropped_on.drag_name:
        #     dragged_clothes[0].snap(dropped_on.x,dropped_on.y)
        #     dragged_clothes[0].set_child(dropped_on.child)
        #     dragged_clothes[0].draggable = False
        #     #renpy.show("thanks_speech",zorder=100)
        dragged_clothes[0].snap(dropped_on.x,dropped_on.y)
        dragged_clothes[0].set_child(im.FactorScale("images/naomi_overlay_"+dragged_clothes[0].drag_name+".png",0.25,0.25))
        dragged_clothes[0].droppable = True
        naomi_wear = "overlay_"+dragged_clothes[0].drag_name
        #overlay_apron_orange = True

    def drag_clothes(drags,drop):
        #overlay_apron_orange = False
        global overlay_apron_orange
        overlay_apron_orange = False
        drags[0].droppable = False
        drags[0].set_child("images/"+drags[0].drag_name+".png")
        drags[0].snap(0,init_ypos[drags[0].drag_name],0.0)

#    def drop_clothes(drags,drop):
#        drags[0].set_child("images/"+drags[0].drag_name+".png")
#        drags[0].snap(0,init_ypos[drags[0].drag_name],0.0)

#    def drag_placed(drags,drop):
#        if not drop:
#            drags[0].snap(0.0,y_align,1.5)

        #store.draggable = drags[0].drag_name
        #store.droppable = drop.drag_name

        #return True

default init_ypos = {}

screen wardrobe():
    modal True
    zorder 1
    image im.Scale("images/wardrobe.jpg", 1920, 1080)
    image "images/naomi_base.png" xalign 0.5 yalign 0.5 zoom 0.25
#    textbutton "Put on apron" action SetVariable("overlay_apron_orange",True)

    # ## Aprons
    # draggroup:
    #     drag:
    #         align(0.5,0.5)
    #         drag_name "base"
    #         image "images/side_naomi_base_happy.png"
    #         draggable False
    #         droppable True
    #     drag:
    #         align(1.0, 0.3)
    #         drag_name "apron_orange"
    #         image "images/naomi_overlay_apron_orange.png"
    #         draggable True
    #         droppable False
    #         dragged drag_placed
    #         drag_raise True
    #     drag:
    #         align(1.0, 0.6)
    #         drag_name "apron_purple"
    #         image "images/naomi_overlay_apron_purple.png"
    #         draggable True
    #         droppable False
    #         dragged drag_placed
    #         drag_raise True

    ## Dresses
    draggroup:
        # Body drop zone
        drag:
            drag_name "kimono"
            draggable False
            droppable True
            dropped wear_clothes
            align (0.5,0.0)
            image "images/naomi_base_torso.png" zoom 0.25
        # Draggable clothes
        python:
            y_pos = -400
        for item in wardrobe_dress:
            python:
                y_pos += 400
                init_ypos[item] = y_pos
            drag:
                drag_name item
                image "images/"+item+".png"
                droppable False
                dragged drag_clothes
                #dropped drop_clothes
                xpos 0
                ypos y_pos
                drag_raise True
        # drag:
        #     align(1.0, 0.3)
        #     drag_name "apron_orange"
        #     image "images/apron_orange.png"
        #     dragged drag_clothes
        #     drag_raise True
        # drag:
        #     align(1.0, 0.6)
        #     drag_name "apron_purple"
        #     image "images/apron_purple.png"
        #     dragged drag_clothes
        #     drag_raise True

    ## Button to close wardrobe
    imagebutton:
        xalign 0.1 yalign 0.1
        idle im.Scale("images/close_screen.png",50,50)
        hover im.Scale("images/close_screen.png",50,50)
        action Hide("wardrobe")
