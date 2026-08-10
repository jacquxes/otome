
## Store screen  ###############################################################
## This screen is for the dept store front

screen dept_store:

    image im.Scale("images/bg dept.png", 1920, 1080)
    
    imagebutton:
        xpos 1226 ypos 581
        idle im.Scale("images/dept/accessories.png",394,393)
        hover im.MatrixColor(im.Scale("images/dept/accessories.png",394,393),im.matrix.brightness(0.2))
        action Jump("accessories_section")

    imagebutton:
        xalign 1.0 yalign 1.0
        idle im.Scale("images/dept/dept_clothes.png",471,569)
        hover im.MatrixColor(im.Scale("images/dept/dept_clothes.png",471,569),im.matrix.brightness(0.2))
        action Jump("clothes_section")

    imagebutton:
        xpos 832 ypos 482
        idle im.Scale("images/dept/exit.png",254,267)
        hover im.MatrixColor(im.Scale("images/dept/exit.png",254,267),im.matrix.brightness(0.2))
        action Jump("dept_exit")

    imagebutton:
        xpos 299 ypos 581
        idle im.Scale("images/dept/stationery.png",342,399)
        hover im.MatrixColor(im.Scale("images/dept/stationery.png",342,399),im.matrix.brightness(0.2))
        action Jump("stationery_section")

    imagebutton:
        xalign 0.0 yalign 1.0
        idle im.Scale("images/dept/cosmetics.png",470,430)
        hover im.MatrixColor(im.Scale("images/dept/cosmetics.png",470,430),im.matrix.brightness(0.2))
        action Jump("cosmetics_section")


## Stationery counter

screen stationery_counter:
    modal True
    
    # Toggle the day_display off
    on "show" action SetVariable("day_display", False)
    on "hide" action SetVariable("day_display", True)

    image "images/dept/counter_bg.png" zoom 0.5
    image "images/dept/counter_sign.png" xalign 0.0 yalign 0.0 zoom 0.5
    hbox:
        xalign 0.23 yalign 0.04
        text "Stationery" color '#C2BAA9' size 70
    imagebutton:
        xalign 0.0 yalign 0.0
        idle im.FactorScale("images/back.png",0.5,0.5)
        hover im.MatrixColor(im.FactorScale("images/back.png",0.5,0.5),im.matrix.brightness(0.3))
        action [Hide("stationery_counter"),Jump("dept_only")]
    image "images/dept/staff show.png" xalign 0.75 ypos -0.05 zoom 0.45
    image "images/speech.png" xalign 0.3 yalign 0.2 zoom 0.5
    hbox:
        xalign 0.3
        yalign 0.2
        box_wrap True
        xmaximum 350
        text If(len(stationery)==0,"I'm sorry, we are sold out for today.","Which item would you like to know about?") textalign 0.5 yalign 0.5 size 40
    image "images/dept/counter.png" xalign 0.5 yalign 1.0 zoom 0.5
    image "images/dept/counter_money.png" xpos 0.83 yalign 0.0 zoom 0.5 xsize 600
    hbox:
        xalign 0.95 ypos 0.05
        text "¥[money]" color '#404040'
    grid 2 2 xalign 0.5 yalign 0.8:
        imagebutton xalign 0.5:
            insensitive im.FactorScale("images/dept/soldout.png",0.5,0.5)
            idle im.Scale("images/item/pen.jpg",160,160)
            hover im.MatrixColor(im.Scale("images/item/pen.jpg",160,160),im.matrix.brightness(0.5))
            if "pen" not in inventory:
                action Jump("purchase_pen")
        imagebutton xalign 0.5:
            insensitive im.FactorScale("images/dept/soldout.png",0.5,0.5)
            idle im.Scale("images/item/notebook.jpg",160,160)
            hover im.MatrixColor(im.Scale("images/item/notebook.jpg",160,160),im.matrix.brightness(0.5))
            if "notebook" not in inventory:
                action Jump("purchase_notebook")

        text "Pen" xalign 0.5 size 40
        text "Notebook" xalign 0.5 size 40

## Accessories counter

screen accessories_counter:
    modal True

    # Toggle the day_display off
    on "show" action SetVariable("day_display", False)
    on "hide" action SetVariable("day_display", True)

    image "images/dept/counter_bg.png" zoom 0.5
    image "images/dept/counter_sign.png" xalign 0.0 yalign 0.0 zoom 0.5
    hbox:
        xalign 0.24 yalign 0.04
        text "Accessories" color '#C2BAA9' size 70
    imagebutton:
        xalign 0.0 yalign 0.0
        idle im.FactorScale("images/back.png",0.5,0.5)
        hover im.MatrixColor(im.FactorScale("images/back.png",0.5,0.5),im.matrix.brightness(0.3))
        action [Hide("accessories_counter"),Jump("dept_only")]
    image "images/dept/staff show.png" xalign 0.65 ypos -0.05 zoom 0.5
    image "images/speech.png" xalign 0.2 yalign 0.3 zoom 0.5
    hbox:
        xalign 0.21
        yalign 0.29
        box_wrap True
        xmaximum 350
        text If(len(accessories)==0,"I'm sorry, we are sold out for today.","Which item would you like to know about?") textalign 0.5 yalign 0.5 size 40
    image "images/dept/counter.png" xalign 0.5 yalign 1.0 zoom 0.5
    image "images/dept/counter_money.png" xpos 0.83 yalign 0.0 zoom 0.5 xsize 600
    hbox:
        xalign 0.95 ypos 0.05
        text "¥[money]" color '#404040'

    ## Stand for hair accessories
    image "images/dept/counter_stand.png" xalign 0.85 yalign 0.25 zoom 0.8
    if "hair_bow" not in wardrobe_hair:
        hbox:
            xalign 0.89 ypos 0.45
            imagebutton xalign 0:
                insensitive im.Scale("images/dept/soldout.png",160,160)
                idle im.FactorScale("images/item/hair_bow.png",0.8,0.8)
                hover im.FactorScale(im.MatrixColor("images/item/hair_bow.png",im.matrix.brightness(0.2)),0.8,0.8)
                action Jump("purchase_hair_bow")
    if "hair_hat" not in wardrobe_hair:
        hbox:
            xalign 0.864 ypos 0.175
            imagebutton xalign 0:
                insensitive im.Scale("images/dept/soldout.png",160,160)
                idle im.FactorScale("images/item/hair_hat.png",0.8,0.8)
                hover im.FactorScale(im.MatrixColor("images/item/hair_hat.png",im.matrix.brightness(0.2)),0.8,0.8)
                action Jump("purchase_hair_hat")
    if "hair_band" not in wardrobe_hair:
        hbox:
            xalign 0.81 ypos 0.25
            imagebutton xalign 0.5:
                insensitive im.Scale("images/dept/soldout.png",160,160)
                idle im.FactorScale("images/item/hair_band.png",0.8,0.8)
                hover im.FactorScale(im.MatrixColor("images/item/hair_band.png",im.matrix.brightness(0.2)),0.8,0.8)
                action Jump("purchase_hair_band")
    if "hair_ribbon" not in wardrobe_hair:
        vbox:
            xalign 0.72 ypos 0.27
            imagebutton xalign 0:
                insensitive im.Scale("images/dept/soldout.png",160,160)
                idle im.FactorScale("images/item/hair_ribbon.png",0.8,0.8)
                hover im.FactorScale(im.MatrixColor("images/item/hair_ribbon.png",im.matrix.brightness(0.2)),0.8,0.8)
                action Jump("purchase_hair_ribbon")
    if "hair_flower" not in wardrobe_hair:
        hbox:
            xalign 0.76 ypos 0.39
            imagebutton xalign 0:
                insensitive im.Scale("images/dept/soldout.png",160,160)
                idle im.FactorScale("images/item/hair_flower.png",0.8,0.8)
                hover im.FactorScale(im.MatrixColor("images/item/hair_flower.png",im.matrix.brightness(0.2)),0.8,0.8)
                action Jump("purchase_hair_flower")

    ## Shelf display for handbags and parasol
    hbox:
        xalign 0.5 ypos 0.57
        imagebutton xalign 1.0:
            insensitive im.FactorScale("images/dept/soldout.png",0.5,0.5)
            idle im.FactorScale("images/item/hand_round.png",0.6,0.6)
            hover im.FactorScale(im.MatrixColor("images/item/hand_round.png",im.matrix.brightness(0.2)),0.6,0.6)
            if "hand_round" not in wardrobe_accessories:
                action Jump("purchase_hand_round")
        imagebutton xalign 1.0:
            insensitive im.FactorScale("images/dept/soldout.png",0.5,0.5)
            idle im.FactorScale("images/item/hand_evening.png",0.6,0.6)
            hover im.FactorScale(im.MatrixColor("images/item/hand_evening.png",im.matrix.brightness(0.2)),0.6,0.6)
            if "hand_evening" not in wardrobe_accessories:
                action Jump("purchase_hand_evening")
        imagebutton xalign 1.0:
            insensitive im.FactorScale("images/dept/soldout.png",0.5,0.5)
            idle im.FactorScale("images/item/hand_straw.png",0.6,0.6)
            hover im.FactorScale(im.MatrixColor("images/item/hand_straw.png",im.matrix.brightness(0.2)),0.6,0.6)
            if "hand_straw" not in wardrobe_accessories:
                action Jump("purchase_hand_straw")
        if "hand_parasol" not in wardrobe_parasol:
            imagebutton ypos -0.18:
                idle im.FactorScale("images/item/hand_parasol.png",0.5,0.5)
                hover im.FactorScale(im.MatrixColor("images/item/hand_parasol.png",im.matrix.brightness(0.2)),0.5,0.5)
                action Jump("purchase_hand_parasol")
                at transform:
                    rotate 283
        else:
            image im.FactorScale("images/dept/soldout.png",0.5,0.5)

    ## Shelf display for shoes
    hbox:
        xalign 0.5 ypos 0.8
        imagebutton xalign 0.5:
            insensitive im.FactorScale("images/dept/soldout.png",0.5,0.5)
            idle im.FactorScale("images/item/shoes_koppori.png",0.7,0.7)
            hover im.FactorScale(im.MatrixColor("images/item/shoes_koppori.png",im.matrix.brightness(0.2)),0.7,0.7)
            if "shoes_koppori" not in wardrobe_shoes:
                action Jump("purchase_shoes_koppori")
        imagebutton xalign 0.5:
            insensitive im.FactorScale("images/dept/soldout.png",0.5,0.5)
            idle im.FactorScale("images/item/shoes_zori.png",0.7,0.7)
            hover im.FactorScale(im.MatrixColor("images/item/shoes_zori.png",im.matrix.brightness(0.2)),0.7,0.7)
            if "shoes_zori" not in wardrobe_shoes:
                action Jump("purchase_shoes_zori")
        imagebutton xalign 0.5:
            insensitive im.FactorScale("images/dept/soldout.png",0.5,0.5)
            idle im.FactorScale("images/item/shoes_heels.png",0.7,0.7)
            hover im.FactorScale(im.MatrixColor("images/item/shoes_heels.png",im.matrix.brightness(0.2)),0.7,0.7)
            if "shoes_heels" not in wardrobe_shoes:
                action Jump("purchase_shoes_heels")
        imagebutton xalign 0.5:
            insensitive im.FactorScale("images/dept/soldout.png",0.5,0.5)
            idle im.FactorScale("images/item/shoes_pumps.png",0.7,0.7)
            hover im.FactorScale(im.MatrixColor("images/item/shoes_pumps.png",im.matrix.brightness(0.2)),0.7,0.7)
            if "shoes_pumps" not in wardrobe_shoes:
                action Jump("purchase_shoes_pumps")
        imagebutton xalign 0.5:
            insensitive im.FactorScale("images/dept/soldout.png",0.5,0.5)
            idle im.FactorScale("images/item/shoes_boots.png",0.7,0.7)
            hover im.FactorScale(im.MatrixColor("images/item/shoes_boots.png",im.matrix.brightness(0.2)),0.7,0.7)
            if "shoes_boots" not in wardrobe_shoes:
                action Jump("purchase_shoes_boots")

screen clothes_counter:
    modal True

    # Toggle the day_display off
    on "show" action SetVariable("day_display", False)
    on "hide" action SetVariable("day_display", True)

    image "images/dept/counter_bg.png" zoom 0.5
    image "images/dept/counter_sign.png" xalign 0.0 yalign 0.0 zoom 0.5
    hbox:
        xalign 0.25 yalign 0.04
        text "Clothing" color '#C2BAA9' size 70
    imagebutton:
        xalign 0.0 yalign 0.0
        idle im.FactorScale("images/back.png",0.5,0.5)
        hover im.MatrixColor(im.FactorScale("images/back.png",0.5,0.5),im.matrix.brightness(0.3))
        action [Hide("clothes_counter"),Jump("dept_only")]
    image "images/dept/staff show.png" xalign 0.75 ypos -0.05 zoom 0.45
    image "images/speech.png" xalign 0.3 yalign 0.2 zoom 0.5
    hbox:
        xalign 0.3
        yalign 0.2
        box_wrap True
        xmaximum 350
        text If(len(clothes)==0,"I'm sorry, we are sold out for today.","Which item would you like to know about?") textalign 0.5 yalign 0.5 size 40
    image "images/dept/counter.png" xalign 0.5 yalign 1.0 zoom 0.5
    image "images/dept/counter_money.png" xpos 0.83 yalign 0.0 zoom 0.5 xsize 600
    hbox:
        xalign 0.95 ypos 0.05
        text "¥[money]" color '#404040'
    hbox:
        xalign 0.5 ypos 0.57 spacing 150
        imagebutton xalign 0.5:
            insensitive im.FactorScale("images/dept/soldout.png",0.5,0.5)
            idle im.FactorScale("images/item/dress_cute.png",0.7,0.7)
            hover im.FactorScale(im.MatrixColor("images/item/dress_cute.png",im.matrix.brightness(0.2)),0.7,0.7)
            if "dress_cute" not in wardrobe_dress:
                action Jump("purchase_dress_cute")
        imagebutton xalign 0.5:
            insensitive im.FactorScale("images/dept/soldout.png",0.5,0.5)
            idle im.FactorScale("images/item/dress_hakama.png",0.7,0.7)
            hover im.FactorScale(im.MatrixColor("images/item/dress_hakama.png",im.matrix.brightness(0.2)),0.7,0.7)
            if "dress_hakama" not in wardrobe_dress:
                action Jump("purchase_dress_hakama")
        imagebutton xalign 0.5:
            insensitive im.FactorScale("images/dept/soldout.png",0.5,0.5)
            idle im.FactorScale("images/item/dress_modern.png",0.7,0.7)
            hover im.FactorScale(im.MatrixColor("images/item/dress_modern.png",im.matrix.brightness(0.2)),0.7,0.7)
            if "dress_modern" not in wardrobe_dress:
                action Jump("purchase_dress_modern")
    hbox:
        xalign 0.5 ypos 0.8 spacing 200
        imagebutton xalign 0.5:
            insensitive im.FactorScale("images/dept/soldout.png",0.5,0.5)
            idle im.FactorScale("images/item/dress_flapper.png",0.7,0.7)
            hover im.FactorScale(im.MatrixColor("images/item/dress_flapper.png",im.matrix.brightness(0.2)),0.7,0.7)
            if "dress_flapper" not in wardrobe_dress:
                action Jump("purchase_dress_flapper")
        imagebutton xalign 0.5:
            insensitive im.FactorScale("images/dept/soldout.png",0.5,0.5)
            idle im.FactorScale("images/item/dress_prim.png",0.7,0.7)
            hover im.FactorScale(im.MatrixColor("images/item/dress_prim.png",im.matrix.brightness(0.2)),0.7,0.7)
            if "dress_prim" not in wardrobe_dress:
                action Jump("purchase_dress_prim")

screen cosmetics_counter:
    modal True

    # Toggle the day_display off
    on "show" action SetVariable("day_display", False)
    on "hide" action SetVariable("day_display", True)

    image "images/dept/counter_bg.png" zoom 0.5
    image "images/dept/counter_sign.png" xalign 0.0 yalign 0.0 zoom 0.5
    hbox:
        xalign 0.25 yalign 0.04
        text "Cosmetics" color '#C2BAA9' size 70
    imagebutton:
        xalign 0.0 yalign 0.0
        idle im.FactorScale("images/back.png",0.5,0.5)
        hover im.MatrixColor(im.FactorScale("images/back.png",0.5,0.5),im.matrix.brightness(0.3))
        action [Hide("cosmetics_counter"),Jump("dept_only")]
    image "images/dept/staff show.png" xalign 0.75 ypos -0.05 zoom 0.45
    image "images/speech.png" xalign 0.3 yalign 0.2 zoom 0.5
    hbox:
        xalign 0.3
        yalign 0.2
        box_wrap True
        xmaximum 350
        text If(len(cosmetics)==0,"I'm sorry, we are sold out for today.","Which item would you like to know about?") textalign 0.5 yalign 0.5 size 40
    image "images/dept/counter.png" xalign 0.5 yalign 1.0 zoom 0.5
    image "images/dept/counter_money.png" xpos 0.83 yalign 0.0 zoom 0.5 xsize 600
    hbox:
        xalign 0.95 ypos 0.05
        text "¥[money]" color '#404040'
    hbox:
        xalign 0.5 ypos 0.62 spacing 80
        imagebutton xalign 0.5:
            insensitive im.FactorScale("images/dept/soldout.png",0.4,0.4)
            idle im.FactorScale("images/item/makeup_eyeshadow_blue.png",0.6,0.6)
            hover im.FactorScale(im.MatrixColor("images/item/makeup_eyeshadow_blue.png",im.matrix.brightness(0.2)),0.6,0.6)
            if "shadow_blue" not in wardrobe_eye:
                action Jump("purchase_shadow_blue")
        imagebutton xalign 0.5:
            insensitive im.FactorScale("images/dept/soldout.png",0.4,0.4)
            idle im.FactorScale("images/item/makeup_eyeshadow_brown.png",0.6,0.6)
            hover im.FactorScale(im.MatrixColor("images/item/makeup_eyeshadow_brown.png",im.matrix.brightness(0.2)),0.6,0.6)
            if "shadow_brown" not in wardrobe_eye:
                action Jump("purchase_shadow_brown")
        imagebutton xalign 0.5:
            insensitive im.FactorScale("images/dept/soldout.png",0.4,0.4)
            idle im.FactorScale("images/item/makeup_eyeshadow_orange.png",0.6,0.6)
            hover im.FactorScale(im.MatrixColor("images/item/makeup_eyeshadow_orange.png",im.matrix.brightness(0.2)),0.6,0.6)
            if "shadow_orange" not in wardrobe_eye:
                action Jump("purchase_shadow_orange")
        imagebutton xalign 0.5:
            insensitive im.FactorScale("images/dept/soldout.png",0.4,0.4)
            idle im.FactorScale("images/item/makeup_eyeshadow_pink.png",0.6,0.6)
            hover im.FactorScale(im.MatrixColor("images/item/makeup_eyeshadow_pink.png",im.matrix.brightness(0.2)),0.6,0.6)
            if "shadow_pink" not in wardrobe_eye:
                action Jump("purchase_shadow_pink")
    hbox:
        xalign 0.5 ypos 0.82 spacing 80
        imagebutton xalign 0.5:
            insensitive im.FactorScale("images/dept/soldout.png",0.4,0.4)
            idle im.FactorScale("images/item/makeup_lipstick_orange.png",0.3,0.3)
            hover im.FactorScale(im.MatrixColor("images/item/makeup_lipstick_orange.png",im.matrix.brightness(0.2)),0.3,0.3)
            if "stick_orange" not in wardrobe_lip:
                action Jump("purchase_stick_orange")
        imagebutton xalign 0.5:
            insensitive im.FactorScale("images/dept/soldout.png",0.4,0.4)
            idle im.FactorScale("images/item/makeup_lipstick_peach.png",0.3,0.3)
            hover im.FactorScale(im.MatrixColor("images/item/makeup_lipstick_peach.png",im.matrix.brightness(0.2)),0.3,0.3)
            if "stick_peach" not in wardrobe_lip:
                action Jump("purchase_stick_peach")
        imagebutton xalign 0.5:
            insensitive im.FactorScale("images/dept/soldout.png",0.4,0.4)
            idle im.FactorScale("images/item/makeup_lipstick_pink.png",0.3,0.3)
            hover im.FactorScale(im.MatrixColor("images/item/makeup_lipstick_pink.png",im.matrix.brightness(0.2)),0.3,0.3)
            if "stick_pink" not in wardrobe_lip:
                action Jump("purchase_stick_pink")
        imagebutton xalign 0.5:
            insensitive im.FactorScale("images/dept/soldout.png",0.4,0.4)
            idle im.FactorScale("images/item/makeup_lipstick_red.png",0.3,0.3)
            hover im.FactorScale(im.MatrixColor("images/item/makeup_lipstick_red.png",im.matrix.brightness(0.2)),0.3,0.3)
            if "stick_red" not in wardrobe_lip:
                action Jump("purchase_stick_red")
        imagebutton xalign 0.5 yalign 1.0:
            insensitive im.FactorScale("images/dept/soldout.png",0.4,0.4)
            idle im.FactorScale("images/item/makeup_cheekblush_orange.png",0.4,0.4)
            hover im.FactorScale(im.MatrixColor("images/item/makeup_cheekblush_orange.png",im.matrix.brightness(0.2)),0.4,0.4)
            if "blush_orange" not in wardrobe_cheek:
                action Jump("purchase_blush_orange")
        imagebutton xalign 0.5 yalign 1.0:
            insensitive im.FactorScale("images/dept/soldout.png",0.4,0.4)
            idle im.FactorScale("images/item/makeup_cheekblush_pink.png",0.4,0.4)
            hover im.FactorScale(im.MatrixColor("images/item/makeup_cheekblush_pink.png",im.matrix.brightness(0.2)),0.4,0.4)
            if "blush_pink" not in wardrobe_cheek:
                action Jump("purchase_blush_pink")


## Retired script ###

    # if tutorial_mode == True:
    #     # Staff and instructions
    #     image "images/staff show.png" at transform:
    #         xalign 0.5 ypos 0.1 zoom 0.5
    #         easein 0.5 xalign 0.7
    #         pause 1.0
    #         easeout 1.0 xpos 2.0
    #     image "images/speech.png" xalign 0.45 yalign 0.3 zoom 0.5 at transform:
    #         alpha 0.0
    #         pause 0.5
    #         alpha 1.0
    #         pause 1.0
    #         alpha 0.0
    #     hbox:
    #         xalign 0.45
    #         yalign 0.29
    #         box_wrap True
    #         xmaximum 370
    #         text If("pen" and "notebook" in inventory,"Tap on the doors behind to exit!","Tap on the Stationery display case!") textalign 0.5 yalign 0.5 size 40 at transform:
    #             alpha 0.0
    #             pause 0.5
    #             alpha 1.0
    #             pause 1.0
    #             alpha 0.0