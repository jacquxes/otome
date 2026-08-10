screen inventory():

    zorder 5
    dismiss action Hide("inventory")

    frame:
        xalign 0.5 yalign 0.5
        xsize 500 ysize 400
        modal True
        image "images/menu/suitcase.png" zoom 0.1 xalign 0.5 yalign 0.5
        hbox:
            xalign 0.5 yalign 0.5
            for item in inventory:
                imagebutton xalign 0.5:
                    idle im.FactorScale("images/inventory/"+item+".png",0.2,0.2)
                    hover im.FactorScale(im.MatrixColor("images/inventory/"+item+".png",im.matrix.brightness(0.2)),0.2,0.2)
                    action Function(renpy.notify, inventory[item][0])