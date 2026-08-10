## Shrine screen  ###############################################################
## This screen is for the shrine

screen asakusa_shrine():

    image "images/bg shrine.png":
        xalign 1.0 yalign 0.5 zoom 0.65

    image "images/shrine/miko happy.png" at transform:
        xalign 0.63 yalign 0.6 zoom 0.6 
        easein 1.5 xalign 0.9

    image "images/speech.png" at transform:
        xalign 0.56 yalign 0.2 zoom 0.5 alpha 0 
        pause 1.5
        alpha 1.0

    hbox:
        xalign 0.55
        yalign 0.2
        box_wrap True
        xmaximum 350
        text "Which charm would you like to know about?" textalign 0.5 size 40 at transform:
            yalign 0.5 alpha 0.0
            pause 1.5
            alpha 1.0

    image "images/shrine/shrine_counter.png":
        xalign 1.0 ypos 0.227 zoom 0.8

    image "images/shrine/omikuji_0.png":
        xalign 0.11 yalign 0.66 zoom 0.8

    imagebutton:
        xalign 0.0 yalign 0.15
        idle im.FactorScale("images/back.png",0.5,0.5)
        hover im.MatrixColor(im.FactorScale("images/back.png",0.5,0.5),im.matrix.brightness(0.3))
        action Jump("shrine")

    imagebutton:
        xpos 0.44 ypos 0.61
        insensitive im.Scale("images/dept/soldout.png",100,100)
        idle im.FactorScale("images/shrine/omamori_strength.png",0.18,0.18)
        hover im.MatrixColor(im.FactorScale("images/shrine/omamori_strength.png",0.18,0.18),im.matrix.brightness(0.2))
        if o_strength > 0:
            action Jump("omamori_strength")

    imagebutton:
        xpos 0.53 ypos 0.61
        insensitive "images/dept/soldout.png"
        idle im.FactorScale("images/shrine/omamori_money.png",0.18,0.18)
        hover im.MatrixColor(im.FactorScale("images/shrine/omamori_money.png",0.18,0.18),im.matrix.brightness(0.2))
        if o_money > 0:
            action Jump("omamori_money")

    imagebutton:
        xpos 0.61 ypos 0.61
        insensitive "images/dept/soldout.png"
        idle im.FactorScale("images/shrine/omamori_love.png",0.18,0.18)
        hover im.MatrixColor(im.FactorScale("images/shrine/omamori_love.png",0.18,0.18),im.matrix.brightness(0.2))
        if o_love > 0:
            action Jump("omamori_love")

    imagebutton:
        xpos 0.7 ypos 0.61
        insensitive "images/dept/soldout.png"
        idle im.FactorScale("images/shrine/omamori_charisma.png",0.18,0.18)
        hover im.MatrixColor(im.FactorScale("images/shrine/omamori_charisma.png",0.18,0.18),im.matrix.brightness(0.2))
        if o_charisma > 0:
            action Jump("omamori_charisma")

    imagebutton:
        xpos 0.78 ypos 0.61
        insensitive "images/dept/soldout.png"
        idle im.FactorScale("images/shrine/omamori_intelligence.png",0.18,0.18)
        hover im.MatrixColor(im.FactorScale("images/shrine/omamori_intelligence.png",0.18,0.18),im.matrix.brightness(0.2))
        if o_intelligence > 0:
            action Jump("omamori_intelligence")

    imagebutton:
        xpos 0.86 ypos 0.61
        insensitive "images/dept/soldout.png"
        idle im.FactorScale("images/shrine/omamori_job.png",0.18,0.18)
        hover im.MatrixColor(im.FactorScale("images/shrine/omamori_job.png",0.18,0.18),im.matrix.brightness(0.2))
        if o_job > 0:
            action Jump("omamori_job")

