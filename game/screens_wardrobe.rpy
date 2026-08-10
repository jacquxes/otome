## Wardrobe screen ###############################################################
## This screen is for the player to switch the character's outfits

init python:

    #### Dresses #######

    ## Item changes to dress when dropped on torso drop zone
    def wear_clothes(dropped_on, dragged_clothes):
        global naomi_dress
        dragged_clothes[0].snap(dropped_on.x,dropped_on.y-39)
        dragged_clothes[0].set_child(im.FactorScale("images/naomi/"+dragged_clothes[0].drag_name+".png",0.25,0.25))
        dragged_clothes[0].droppable = True
        naomi_dress = dragged_clothes[0].drag_name
        renpy.restart_interaction()
    
    ## When item is dragged onto dress image, the dropped on dress will revert to item form and return to shelf
    def dropped_clothes(dropped_on,dragged):
        dropped_on.set_child(im.FactorScale("images/item/"+dropped_on.drag_name+".png",0.5,0.5))
        dropped_on.droppable = False
        dropped_on.snap(init_dressxpos[dropped_on.drag_name],init_dressypos[dropped_on.drag_name],0.0)
        global naomi_dress
        dragged[0].snap(dropped_on.x,dropped_on.y-39)
        dragged[0].set_child(im.FactorScale("images/naomi/"+dragged[0].drag_name+".png",0.25,0.25))
        dragged[0].dragging = dragging_clothes
        dragged[0].droppable = True
        naomi_dress = dragged[0].drag_name
        renpy.restart_interaction()

    ## When dress is dragged off torso, it reverts to item form
    def dragging_clothes(dragging):
        global naomi_dress
        naomi_dress = ""
        dragging[0].dragging = dragging_clothes_roll
        dragging[0].set_child(im.FactorScale("images/item/"+dragging[0].drag_name+".png",0.5,0.5))

    ## When dress is dragged, it reverts to item form. Separate from dragging_clothes to prevent triggering variable change when item is dragged from shelf.
    def dragging_clothes_roll(dragging):
        dragging[0].set_child(im.FactorScale("images/item/"+dragging[0].drag_name+".png",0.5,0.5))

    ## When item is dragged off torso, it snaps to shelf position. Separate from drag_clothes_roll to prevent triggering variable change when item is dragged from shelf.
    def drag_clothes(drags,drop):
        drags[0].droppable = False
        drags[0].snap(init_dressxpos[drags[0].drag_name],init_dressypos[drags[0].drag_name],0.0)

    #### Shoes #######

    ## Item changes to shoes when dragged to feet drop zone
    def wear_shoes(dropped_on, dragged_shoes):
        global naomi_shoes
        dragged_shoes[0].snap(dropped_on.x,dropped_on.y)
        dragged_shoes[0].set_child(im.FactorScale("images/naomi/"+dragged_shoes[0].drag_name+".png",0.25,0.25))
        dragged_shoes[0].droppable = True
        naomi_shoes = dragged_shoes[0].drag_name
        renpy.restart_interaction()

    ## When item is dragged onto shoes image, the dropped on shoes will revert to item form and return to shelf
    def dropped_shoes(dropped_on,dragged):
        dropped_on.set_child(im.FactorScale("images/item/"+dropped_on.drag_name+".png",0.5,0.5))
        dropped_on.droppable = False
        dropped_on.snap(init_shoexpos[dropped_on.drag_name],init_shoeypos[dropped_on.drag_name],0.0)
        global naomi_shoes
        dragged[0].snap(dropped_on.x,dropped_on.y-39)
        dragged[0].set_child(im.FactorScale("images/naomi/"+dragged[0].drag_name+".png",0.25,0.25))
        dragged[0].droppable = True
        dragged[0].draggling = dragging_shoes
        naomi_shoes = dragged[0].drag_name
        renpy.restart_interaction()
    
    ## When shoes is dragged off feet, it reverts to item form
    def dragging_shoes(dragging):
        global naomi_shoes
        naomi_shoes = ""
        dragging[0].set_child(im.FactorScale("images/item/"+dragging[0].drag_name+".png",0.5,0.5))
        dragging[0].dragging = dragging_shoes_roll

    ## When shoes is dragged off feet, it reverts to item form. Separate from dragging_shoes to prevent triggering variable change when item is dragged from shelf.
    def dragging_shoes_roll(dragging):
        dragging[0].set_child(im.FactorScale("images/item/"+dragging[0].drag_name+".png",0.5,0.5))

    ## When item is dragged off feet, it snaps to shelf position. 
    def drag_shoes(drags,drop):
        drags[0].droppable = False
        drags[0].snap(init_shoexpos[drags[0].drag_name],init_shoeypos[drags[0].drag_name],0.0)

    #### Hair #######

    ## Item changes to worn when dropped on head drop zone
    def wear_hat(dropped_on,dragged_hat):
        global naomi_hair
        dragged_hat[0].snap(dropped_on.x,dropped_on.y)
        dragged_hat[0].set_child(Crop((600,100,899,899),"images/naomi/"+dragged_hat[0].drag_name+".png"))
        dragged_hat[0].droppable = True
        naomi_hair = dragged_hat[0].drag_name
        renpy.restart_interaction()

    ## When item is dragged onto hair with hat, the dropped on hat will revert to item form and return to shelf
    def dropped_hat(dropped_on,dragged):
        dropped_on.set_child("images/item/"+dropped_on.drag_name+".png")
        dropped_on.droppable = False
        dropped_on.snap(wardrobe_hair[dropped_on.drag_name][0],wardrobe_hair[dropped_on.drag_name][1],0.0)
        global naomi_hair
        dragged[0].snap(dropped_on.x,dropped_on.y)
        dragged[0].set_child(Crop((600,100,899,899),"images/naomi/"+dragged[0].drag_name+".png"))
        dragged[0].droppable = True
        dragged[0].dragging = dragging_hat
        naomi_hair = dragged[0].drag_name
        renpy.restart_interaction()

    ## Reverts hat to item and reverts hair to default when hat is dragged off
    def dragging_hat(dragging):
        dragging[0].set_child("images/item/"+dragging[0].drag_name+".png")
        global naomi_hair
        naomi_hair = "hair_base"
        renpy.restart_interaction()

    ## Snaps item to original position
    def drag_hat(drags,drop):
        drags[0].droppable = False
        drags[0].snap(wardrobe_hair[drags[0].drag_name][0],wardrobe_hair[drags[0].drag_name][1],0.0)

    #### Left Hand (parasol) #######

    ## Item changes to held parasol when dropped on left hand drop zone
    def wear_accessories_left(dropped_on, dragged_accessories):
        global naomi_accessories_left
        dragged_accessories[0].snap(dropped_on.x,dropped_on.y)
        dragged_accessories[0].set_child(im.FactorScale("images/naomi/"+dragged_accessories[0].drag_name+".png",0.25,0.25))
        naomi_accessories_left = dragged_accessories[0].drag_name
        renpy.restart_interaction()

    ## Reverts parasol to item when parasol is dragged off
    def dragging_accessories_left(dragging):
        dragging[0].set_child(im.FactorScale("images/item/"+dragging[0].drag_name+".png",0.5,0.5))
        global naomi_accessories_left
        naomi_accessories_left = ""
        dragging[0].dragging = dragging_accessories_roll_left

    ## Reverts parasol to item when parasol is dragged off
    def dragging_accessories_roll_left(dragging):
        dragging[0].set_child(im.FactorScale("images/item/"+dragging[0].drag_name+".png",0.5,0.5))

    ## When item is dragged off hand, it snaps to shelf position. Separate from drag_accessories_roll_left to prevent triggering variable change when item is dragged from shelf.
    def drag_accessories_left(drags,drop):
        drags[0].droppable = False
        drags[0].snap(1735,530,0.0)
    
    #### Right Hand (bags) #######

    ## Item changes to held bag when dropped on right hand drop zone
    def wear_accessories_right(dropped_on, dragged_accessories):
        global naomi_accessories_right
        dragged_accessories[0].snap(dropped_on.x,dropped_on.y)
        dragged_accessories[0].set_child(im.FactorScale("images/naomi/"+dragged_accessories[0].drag_name+".png",0.25,0.25))
        dragged_accessories[0].droppable = True
        naomi_accessories_right = dragged_accessories[0].drag_name
        renpy.restart_interaction()

    ## When item is dragged onto hand with bag, the dropped on bag will revert to item form and return to shelf
    def dropped_bag(dropped_on,dragged):
        dropped_on.set_child("images/item/"+dropped_on.drag_name+".png")
        dropped_on.droppable = False
        dropped_on.snap(init_accessoriesxpos[dropped_on.drag_name],95,0.0)
        global naomi_accessories_right
        dragged[0].snap(dropped_on.x,dropped_on.y)
        dragged[0].set_child(im.FactorScale("images/naomi/"+dragged[0].drag_name+".png",0.25,0.25))
        dragged[0].droppable = True
        dragged[0].dragged = drag_accessories_right
        naomi_accessories_right = dragged[0].drag_name
        renpy.restart_interaction()

    ## Reverts bag to item when bag is dragged off. 
    def dragging_accessories_right(dragging):
        global naomi_accessories_right
        naomi_accessories_right = ""
        dragging[0].set_child(im.FactorScale("images/item/"+dragging[0].drag_name+".png",0.5,0.5))
        dragging[0].dragging = dragging_accessories_roll_right
        
    ## Reverts bag to item when bag is dragged off. Separate from dragging_accessories_right to prevent triggering variable change when item is dragged from shelf.
    def dragging_accessories_roll_right(dragging):
        dragging[0].set_child(im.FactorScale("images/item/"+dragging[0].drag_name+".png",0.5,0.5))

    ## When item is dragged off hand, it snaps to shelf position. 
    def drag_accessories_right(drags,drop):
        drags[0].droppable = False
        drags[0].snap(init_accessoriesxpos[drags[0].drag_name],95,0.0)
        
    #### Cheeks #######

    ## Item changes cheek color when dragged to cheek drop zone. Reverts back to original position.
    def wear_cheek(dropped_on, dragged_cheek):
        global naomi_cheek, cheek_color_r, cheek_color_g, cheek_color_b
        naomi_cheek = dragged_cheek[0].drag_name
        cheek_color_r = naomi_cheek_rgb[dragged_cheek[0].drag_name][0]
        cheek_color_g = naomi_cheek_rgb[dragged_cheek[0].drag_name][1]
        cheek_color_b = naomi_cheek_rgb[dragged_cheek[0].drag_name][2]
        #dropped_on.set_child(im.MatrixColor("images/naomi/makeup_cheek"+dragged_cheek[0].drag_name+".png",im.matrix.opacity(0.2)))
        dragged_cheek[0].snap(init_cheekxpos[dragged_cheek[0].drag_name],230)
        renpy.restart_interaction()
    
    ## Returns item to box when dragged but not dropped
    def drag_cheek(drags,drop):
        drags[0].snap(init_cheekxpos[drags[0].drag_name],230,0.0) 

    #### Eyes #######

    ## Item changes eye color when dragged to eye drop zone. Reverts back to original position.
    def wear_eye(dropped_on, dragged_eye):
        global naomi_eye, eye_color_r, eye_color_g, eye_color_b
        naomi_eye = dragged_eye[0].drag_name
        eye_color_r = naomi_eye_rgb[dragged_eye[0].drag_name][0]
        eye_color_g = naomi_eye_rgb[dragged_eye[0].drag_name][1]
        eye_color_b = naomi_eye_rgb[dragged_eye[0].drag_name][2]
        #dropped_on.set_child("images/naomi/makeup_eye"+dragged_eye[0].drag_name+".png")
        dragged_eye[0].snap(init_eyexpos[dragged_eye[0].drag_name],100)
        renpy.restart_interaction()
    
    ## Returns item to box when dragged but not dropped
    def drag_eye(drags,drop):
        drags[0].snap(init_eyexpos[drags[0].drag_name],100,0.0) 

    #### Lips #######

    ## Item changes lip color when dragged to lips drop zone. Reverts back to original position.
    def wear_lip(dropped_on, dragged_lip):
        global naomi_lip, lip_color_h, lip_color_s, lip_color_v
        naomi_lip = dragged_lip[0].drag_name
        lip_color_h = naomi_lip_hsv[dragged_lip[0].drag_name][0]
        lip_color_s = naomi_lip_hsv[dragged_lip[0].drag_name][1]
        lip_color_v = naomi_lip_hsv[dragged_lip[0].drag_name][2]
        #dropped_on.set_child("images/naomi/makeup_lip"+dragged_lip[0].drag_name+".png")
        dragged_lip[0].snap(init_lipxpos[dragged_lip[0].drag_name],600)
        renpy.restart_interaction()
    
    ## Returns item to box when dragged but not dropped
    def drag_lip(drags,drop):
        drags[0].snap(init_lipxpos[drags[0].drag_name],600,0.0) 

    #### Cold Cream #######

    ## Item reverts to base when dragged to drop zone. Returns to original position.
    def clean_lip(dropped_on, dragged):
        global naomi_lip, lip_color_h, lip_color_s, lip_color_v
        naomi_lip = ""
        lip_color_h = 14
        lip_color_s = 0.85
        lip_color_v = 0.15
        dragged[0].snap(1600,750)
        renpy.restart_interaction()

    def clean_cheek(dropped_on, dragged):
        global naomi_cheek, cheek_color_r, cheek_color_g, cheek_color_b
        naomi_cheek = ""
        cheek_color_r = 1.5
        cheek_color_g = 1.5
        cheek_color_b = 1.5
        dragged[0].snap(1600,750)
        renpy.restart_interaction()
    
    def clean_eye(dropped_on, dragged):
        global naomi_eye, eye_color_r, eye_color_g, eye_color_b
        naomi_eye = ""
        eye_color_r = 1.15
        eye_color_g = 1.2
        eye_color_b = 1.2
        dragged[0].snap(1600,750)
        renpy.restart_interaction()
    
    ## Returns item to side when dragged but not dropped
    def drag_cream(drags,drop):
        drags[0].snap(1600,750,0.0) 

### Dictionaries to store initial x and y positions of items
default init_shoexpos = {}
default init_shoeypos = {}
default init_dressxpos = {}
default init_dressypos = {}
default init_accessoriesxpos = {}
default init_hatxpos = {}
default init_hatypos = {}
default init_lipxpos = {}
default init_cheekxpos = {}
default init_eyexpos = {}

### Main wardrobe screen
screen wardrobe():
    modal True
    zorder 5
    image im.Scale("images/bg wardrobe.png",1920,1080)
    imagebutton:
        xpos 611 ypos 170
        idle im.Scale("images/wardrobe/dresser.png",474,745)
        hover im.MatrixColor(im.Scale("images/wardrobe/dresser.png",474,745),im.matrix.brightness(0.2))
        action Show("wardrobe_face")
    
    # Insert images of hats in background
    python:
        sorted_wardrobe_hair = sorted(wardrobe_hair.keys(),reverse=True)
    for key in sorted_wardrobe_hair:
        image "images/item/"+key+".png" zoom 0.5:
            xpos wardrobe_hair[key][0]//2+150
            ypos wardrobe_hair[key][1]//2+100
            if key == naomi_hair:
                alpha 0.0
    
    image "images/naomi/"+naomi_hair+".png" xalign 0.2 yalign 0.0 zoom 0.25
    image "images/naomi/makeup_cheek"+naomi_cheek+".png" xalign 0.2 ypos 100 zoom 0.25
    image "images/naomi/makeup_eye"+naomi_eye+".png" xalign 0.2 ypos 78 zoom 0.25
    image "images/naomi/makeup_lip"+naomi_lip+".png" xalign 0.2 ypos 160 zoom 0.25
    image "images/naomi/base.png" xalign 0.2 yalign 0.0 zoom 0.25 alpha 0.0
    
    ## Parasol (hand_left)
    draggroup:
        drag:
            drag_name "hand_left"
            draggable False
            droppable True
            dropped wear_accessories_left
            xpos 600
            ypos 500
            image "images/naomi/hand_parasol.png" zoom 0.25 alpha 0.0
        if "hand_parasol" in wardrobe_parasol:
            if naomi_accessories_left == "hand_parasol":
                drag:
                    drag_name "hand_parasol"
                    image "images/naomi/hand_parasol.png" zoom 0.25
                    droppable True
                    dragging dragging_accessories_left
                    dragged drag_accessories_left
                    xpos 600
                    ypos 500
            else:
                drag:
                    drag_name "hand_parasol"
                    image "images/item/hand_parasol.png" zoom 0.5
                    droppable False
                    dragging dragging_accessories_roll_left
                    dragged drag_accessories_left
                    xpos 1735
                    ypos 530
                    drag_raise True
    ## Shoes
    draggroup:
        # Feet drop zone
        drag:
            drag_name "shoes"
            draggable False
            droppable True
            dropped wear_shoes
            xalign 0.2
            ypos 850
            image "images/naomi/base_feet.png" zoom 0.25
        # Draggable shoes
        python:
            shoe_xpos = 975
            shoe_ypos = 640
            shoe_count = 0
        for item in wardrobe_shoes:
            python:
                shoe_count += 1
                if shoe_count < 4:
                    shoe_xpos += 195
                if shoe_count == 4:
                    shoe_xpos = 1175
                    shoe_ypos = 815
                if shoe_count > 4:
                    shoe_xpos += 195
                    shoe_ypos = 815
                init_shoexpos[item] = shoe_xpos
                init_shoeypos[item] = shoe_ypos
            if item == naomi_shoes:
                drag:
                    drag_name item
                    image "images/naomi/"+item+".png" zoom 0.25
                    droppable True
                    dragging dragging_shoes
                    dragged drag_shoes
                    dropped dropped_shoes
                    xalign 0.2
                    ypos 850
            else:
                drag:
                    drag_name item
                    image "images/item/"+item+".png" zoom 0.5
                    droppable False
                    dragging dragging_shoes_roll
                    dragged drag_shoes
                    dropped dropped_shoes
                    xpos shoe_xpos
                    ypos shoe_ypos
                    drag_raise True
    ## Dresses
    draggroup:
        # Body drop zone
        drag:
            drag_name "kimono"
            draggable False
            droppable True
            dropped wear_clothes
            xalign 0.2
            ypos 225
            image "images/naomi/base_torso.png" zoom 0.25
        # Draggable clothes
        python:
            dress_xpos = 940
            dress_ypos = 295
            dress_count = 0
        for item in wardrobe_dress:
            python:
                dress_count += 1
                if dress_count < 4:
                    dress_xpos += 200
                if dress_count == 4:
                    dress_xpos = 1140
                    dress_ypos = 475
                if dress_count > 4:
                    dress_xpos += 200
                    dress_ypos = 475
                init_dressxpos[item] = dress_xpos
                init_dressypos[item] = dress_ypos
            if item == naomi_dress:
                drag:
                    drag_name item
                    image "images/naomi/"+item+".png" zoom 0.25
                    droppable True
                    dragging dragging_clothes
                    dragged drag_clothes
                    dropped dropped_clothes
                    xalign 0.2
                    ypos 185
            else:
                drag:
                    drag_name item
                    image "images/item/"+item+".png" zoom 0.5
                    droppable False
                    dragging dragging_clothes_roll
                    dragged drag_clothes
                    dropped dropped_clothes
                    xpos dress_xpos
                    ypos dress_ypos
                    drag_raise True
    ## Bags (hand_right)
    draggroup:
        drag:
            drag_name "hand_right"
            draggable False
            droppable True
            dropped wear_accessories_right
            xpos 275
            ypos 500
            image "images/naomi/hand_round.png" zoom 0.25 alpha 0.0
        # Draggable accessories
        python:
            accessories_xpos = 950
        for item in wardrobe_accessories:
            python:
                accessories_xpos += 200
                init_accessoriesxpos[item] = accessories_xpos
            if item == naomi_accessories_right:
                drag:
                    drag_name item
                    image "images/naomi/"+item+".png" zoom 0.25
                    droppable True
                    dropped dropped_bag
                    dragging dragging_accessories_right
                    dragged drag_accessories_right
                    xpos 275
                    ypos 500
            else:
                drag:
                    drag_name item
                    image im.FactorScale("images/item/"+item+".png",0.5,0.5)
                    droppable False
                    dragging dragging_accessories_roll_right
                    dragged drag_accessories_right
                    xpos accessories_xpos
                    ypos 95
                    drag_raise True

    ## Button to close wardrobe
    imagebutton:
        xalign 0 yalign 0
        idle im.FactorScale("images/back.png",0.5,0.5)
        hover im.FactorScale(im.MatrixColor("images/back.png",im.matrix.brightness(0.2)),0.5,0.5)
        action Hide("wardrobe")

    ## Button to zoom in
    imagebutton:
        xalign 0.1 yalign 1.0
        idle im.Scale("gui/zoomin_idle.png",200,200)
        hover im.Scale("gui/zoomin_hover.png",200,200)
        action Show("wardrobe_zoom")

screen wardrobe_zoom():
    modal True
    zorder 6
    image im.Scale("images/bg wardrobe.png", 1920, 1080):
        blur 3.0

    # Insert image of hats
    python:
        sorted_wardrobe_hair = sorted(wardrobe_hair.keys(),reverse=True)
    for key in sorted_wardrobe_hair:
        image "images/item/"+key+".png" zoom 0.5:
            xpos wardrobe_hair[key][0]//2+150
            ypos wardrobe_hair[key][1]//2+100
            blur 3.0
            if key == naomi_hair:
                alpha 0.0
    # Insert image of clothes
    python:
        dress_xpos = 940
        dress_ypos = 295
        dress_count = 0
    for item in wardrobe_dress:
        python:
            dress_count += 1
            if dress_count < 4:
                dress_xpos += 200
            if dress_count == 4:
                dress_xpos = 1140
                dress_ypos = 475
            if dress_count > 4:
                dress_xpos += 200
                dress_ypos = 475
        image "images/item/"+item+".png" zoom 0.5:
            xpos dress_xpos
            ypos dress_ypos
            blur 3.0
            if item == naomi_dress:
                alpha 0.0
    # Insert image of shoes
    python:
        shoe_xpos = 975
        shoe_ypos = 640
        shoe_count = 0
    for item in wardrobe_shoes:
        python:
            shoe_count += 1
            if shoe_count < 4:
                shoe_xpos += 195
            if shoe_count == 4:
                shoe_xpos = 1175
                shoe_ypos = 815
            if shoe_count > 4:
                shoe_xpos += 195
                shoe_ypos = 815
        image "images/item/"+item+".png":
            zoom 0.5
            xpos shoe_xpos
            ypos shoe_ypos
            blur 3.0
            if item == naomi_shoes:
                alpha 0.0
    # Insert image of accessories
    python:
        accessories_xpos = 950
    for item in wardrobe_accessories:
        python:
            accessories_xpos += 200
        image "images/item/"+item+".png":
            zoom 0.5
            xpos accessories_xpos
            ypos 95
            blur 3.0
            if item == naomi_accessories_left or item == naomi_accessories_right:
                alpha 0.0
    # Insert image of parasol
    if "hand_parasol" in wardrobe_parasol and naomi_accessories_left == "":
        image "images/item/hand_parasol.png":
            zoom 0.5
            xpos 1735
            ypos 530
            blur 3.0

    viewport:
        area (0,0,1920,1080)
        draggable True
        vbox:
            fixed:
                area (0,0,2150,4299)
                image "images/naomi/base_torso.png" xalign 0.5 ypos 899
                if naomi_accessories_left == "hand_parasol":
                    image "images/naomi/hand_parasol.png" xalign 1.0 yalign 1.0
                image "images/naomi/base_feet.png" xalign 0.5 yalign 1.0
                image "images/naomi/"+naomi_hair+".png" xalign 0.5 yalign 0.0
                image "images/naomi/makeup_cheek"+naomi_cheek+".png" xalign 0.5 ypos 400
                image "images/naomi/makeup_eye"+naomi_eye+".png" xalign 0.5 ypos 312
                image "images/naomi/makeup_lip"+naomi_lip+".png" xalign 0.5 ypos 640
                if naomi_shoes != "":
                    image "images/naomi/"+naomi_shoes+".png" xalign 0.5 yalign 1.0
                if naomi_dress != "":
                    image "images/naomi/"+naomi_dress+".png" xalign 0.5 ypos 740
                if naomi_accessories_right != "":
                    image "images/naomi/"+naomi_accessories_right+".png" xalign 0.0 ypos 2000
    
    ## Button to zoom out
    imagebutton:
        xalign 0.1 yalign 1.0
        idle im.Scale("gui/zoomout_idle.png",200,200)
        hover im.Scale("gui/zoomout_hover.png",200,200)
        action Hide("wardrobe_zoom")

screen wardrobe_face():
    modal True
    zorder 6
    image "images/bg wardrobe.png" xpos -300 ypos -200
    image "images/naomi/base_torso.png" xpos -600 ypos 799
    imagebutton:
        xpos 1049 ypos 652
        idle "images/wardrobe/makeup.png"
        hover im.MatrixColor("images/wardrobe/makeup.png",im.matrix.brightness(0.2))
        action Show("wardrobe_makeup")

    ## Hat
    draggroup:
        # Hair drop zone
        drag:
            drag_name "hair"
            draggable False
            droppable True
            dropped wear_hat
            xalign 0.0
            yalign 0.0
            image "images/naomi/"+naomi_hair+".png" crop (600,100,899,899) 
        python:
            sorted_wardrobe_hair = sorted(wardrobe_hair.keys(),reverse=True)
        for key in sorted_wardrobe_hair:
            if key == naomi_hair:
                drag:
                    drag_name key
                    image "images/naomi/"+key+".png" crop (600,100,899,899) 
                    droppable True
                    dragging dragging_hat
                    dragged drag_hat
                    dropped dropped_hat
                    drag_raise True
            else:
                drag:
                    drag_name key
                    image "images/item/"+key+".png"
                    droppable False
                    dragged drag_hat
                    dropped dropped_hat
                    xpos wardrobe_hair[key][0]
                    ypos wardrobe_hair[key][1]
                    drag_raise True

    image "images/naomi/makeup_cheek"+naomi_cheek+".png" xpos -600 ypos 300
    image "images/naomi/makeup_eye"+naomi_eye+".png" xpos -600 ypos 212
    image "images/naomi/makeup_lip"+naomi_lip+".png" xpos -600 ypos 540
    if naomi_dress != "":
        image "images/naomi/"+naomi_dress+".png" xpos -600 ypos 640

    ## Button to close view
    imagebutton:
        xalign 0 yalign 0
        idle im.FactorScale("images/back.png",0.5,0.5)
        hover im.FactorScale(im.MatrixColor("images/back.png",im.matrix.brightness(0.2)),0.5,0.5)
        action Hide("wardrobe_face")

screen wardrobe_makeup():
    modal True
    zorder 7
    image "images/bg wardrobe.png" xpos -300 ypos -200
    image "images/wardrobe/bg makeup.png" xalign 1.0 zoom 0.5
    image "images/naomi/base_torso.png" xpos -600 ypos 799
    image "images/naomi/"+naomi_hair+".png" xalign 0.0 yalign 0.0 crop (600,100,899,899) 
    if naomi_dress != "":
        image "images/naomi/"+naomi_dress+".png" xpos -600 ypos 640

    ## Makeup #####
    ## Cheeks
    draggroup:
        # Cheek drop zone
        drag:
            drag_name "cheek"
            draggable False
            droppable True
            dropped wear_cheek
            xpos -600
            ypos 300
            image "images/naomi/makeup_cheek.png"
            #image "images/naomi/makeup_cheek"+naomi_cheek+".png"
        python:
            cheek_xpos = 800
        for item in wardrobe_cheek:
            python:
                cheek_xpos += 290
                init_cheekxpos[item] = cheek_xpos
            drag:
                drag_name item
                image "images/item/makeup_cheek"+item+".png" zoom 0.5
                draggable True
                droppable True
                dropped wear_cheek
                dragged drag_cheek
                xpos cheek_xpos
                ypos 230
                drag_raise True
    ## Eyes
    draggroup:
        # Eyes drop zone
        drag:
            drag_name "eye"
            draggable False
            droppable True
            dropped wear_eye
            xpos -600
            ypos 212
            image "images/naomi/makeup_eye"+naomi_eye+".png"
        python:
            eye_xpos = 860
        for item in wardrobe_eye:
            python:
                eye_xpos += 160
                init_eyexpos[item] = eye_xpos
            drag:
                drag_name item
                image "images/item/makeup_eye"+item+".png" zoom 0.5
                draggable True
                droppable True
                dropped wear_eye
                dragged drag_eye
                xpos eye_xpos
                ypos 100
                drag_raise True
    ## Lips
    draggroup:
        # Lip drop zone
        drag:
            drag_name "lip"
            draggable False
            droppable True
            dropped wear_lip
            xpos -600
            ypos 540
            image "images/naomi/makeup_lip"+naomi_lip+".png"
        python:
            lip_xpos = 890
        for item in wardrobe_lip:
            python:
                lip_xpos += 150
                init_lipxpos[item] = lip_xpos
            drag:
                drag_name item
                image "images/item/makeup_lip"+item+".png" zoom 0.5
                draggable True
                droppable True
                dropped wear_lip
                dragged drag_lip
                xpos lip_xpos
                ypos 600
                drag_raise True
    ## Cold cream
    draggroup:
        # Face drop zone
        drag:
            drag_name "naomi_cheek"
            draggable False
            droppable True
            dropped clean_cheek
            xpos -600
            ypos 300
            image "images/naomi/makeup_cheek"+naomi_cheek+".png"
        drag:
            drag_name "naomi_eye"
            draggable False
            droppable True
            dropped clean_eye
            xpos -600
            ypos 212
            image "images/naomi/makeup_eye"+naomi_eye+".png" alpha 0.0
        drag:
            drag_name "naomi_lip"
            draggable False
            droppable True
            dropped clean_lip
            xpos -600
            ypos 540
            image "images/naomi/makeup_lip"+naomi_lip+".png" alpha 0.0
        drag:
            drag_name "makeup_remover"
            draggable True
            droppable False
            dragged drag_cream
            xpos 1600
            ypos 750
            image "images/wardrobe/makeup_remover.png" zoom 0.5

    ## Button to close view
    imagebutton:
        xalign 0 yalign 0
        idle im.FactorScale("images/back.png",0.5,0.5)
        hover im.FactorScale(im.MatrixColor("images/back.png",im.matrix.brightness(0.2)),0.5,0.5)
        action Hide("wardrobe_makeup")