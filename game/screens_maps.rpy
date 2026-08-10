## Imagemap screen ###############################################################
##
## This screen is used to display the in-game choices in an image map.

screen ginza_large():
    # modal True

    # Toggle the day_display off
    on "show" action SetVariable("day_display", False)
    on "hide" action SetVariable("day_display", True)

    viewport:
        draggable True
        
        imagemap:
            idle "gui/map/ginza_idle.png"
            hover "gui/map/ginza_hover.png"
            if jp_lang == True:
                ground "gui/map/ginza_ground_jp.png"
            else:
                ground "gui/map/ginza_ground.png"
            
            hotspot (1573, 1069, 670, 655) action Jump("dept_store")
            if unlock_imp_th == True and dayofweeknumber < 6:
                hotspot (149, 206, 709, 465) action Jump("imperial_theatre")
            if unlock_off_bldg == True and dayofweeknumber < 6:
                hotspot (3033, 1220, 554, 240) action Jump("office_bldg")
            if unlock_hosp == True and dayofweeknumber < 6:
                hotspot (2130, 1791, 853, 282) action Jump("hospital")
            #hotspot (2553, 98, 1219, 556) action Jump("tokyo_station")
    
    # Set the frame
    if jp_lang == True:
        image im.Scale("gui/map/ginza_frame_jp.png", 1920, 1080)
    else:
        image im.Scale("gui/map/ginza_frame.png", 1920, 1080)  

    # Button to navigate to Asakusa map
    vbox:
        xalign 1.0
        yalign 0.5
        imagebutton:
            idle im.Scale("gui/map/arrow_asakusa_idle.png", 93, 219)
            hover im.Scale("gui/map/arrow_asakusa_hover.png", 93, 219)
            action Jump("asakusa_large")

    # Button to zoom out
    vbox:
        xalign 1.0
        yalign 1.0
        imagebutton:
            idle im.Scale("gui/zoomout_idle.png", 200, 200)
            hover im.Scale("gui/zoomout_hover.png", 200, 200)
            action Jump("ginza_small")

screen ginza_small():
    # modal True

    # Toggle the day_display off
    on "show" action SetVariable("day_display", False)
    on "hide" action SetVariable("day_display", True)

    imagemap:
        idle im.Scale("gui/map/ginza_idle.png", 1920, 1080)
        hover im.Scale("gui/map/ginza_hover.png", 1920, 1080)
        if jp_lang == True:
            ground im.Scale("gui/map/ginza_ground_jp.png",1920,1080)
        else:
            ground im.Scale("gui/map/ginza_ground.png", 1920, 1080)
            
        hotspot (784, 539, 342, 324) action Jump("dept_store")
        if unlock_imp_th == True and dayofweeknumber < 6:
            hotspot (81, 104, 347, 237) action Jump("imperial_theatre")
        if unlock_off_bldg == True and dayofweeknumber < 6:
            hotspot (1521, 611, 277, 114) action Jump("office_bldg")
        if unlock_hosp == True and dayofweeknumber < 6:
            hotspot (1063, 898, 428, 136) action Jump("hospital")
        #hotspot (1266, 61, 613, 260) action Jump("tokyo_station")

    # Set the frame
    if jp_lang == True:
        image im.Scale("gui/map/ginza_frame_jp.png",1920,1080)
    else:
        image im.Scale("gui/map/ginza_frame.png", 1920, 1080)

    # Button to navigate to Asakusa map
    vbox:
        xalign 1.0
        yalign 0.5
        imagebutton:
            idle im.Scale("gui/map/arrow_asakusa_idle.png", 93, 219)
            hover im.Scale("gui/map/arrow_asakusa_hover.png", 93, 219)
            action Jump("asakusa_small")
    
    # Button to zoom in
    vbox:
        xalign 1.0
        yalign 1.0
        imagebutton:
            idle im.Scale("gui/zoomin_idle.png", 200, 200)
            hover im.Scale("gui/zoomin_hover.png", 200, 200)
            action Jump("ginza_large")
    
screen asakusa_large():

    # Toggle the day_display off
    on "show" action SetVariable("day_display", False)
    on "hide" action SetVariable("day_display", True)

    # modal True
    viewport:
        draggable True
        
        imagemap:
            idle "gui/map/asakusa_idle.png"
            hover "gui/map/asakusa_hover.png"
            if jp_lang == True:
                ground "gui/map/asakusa_ground_jp.png"
            else:
                ground "gui/map/asakusa_ground.png"
            
            hotspot(1360, 1584, 653, 514) action Jump("work_cafe")
            if (unlock_movie_th == True and dayofweeknumber < 6) or (doctor_event == True and dayofweeknumber == 7 and timeslot == 1):
                hotspot(418, 1194, 582, 412) action Jump("doctor_movie")
            if unlock_dojo == True and dayofweeknumber < 6:
                hotspot(130, 1578, 380, 287) action Jump("dojo")
            hotspot(2277, 285, 1156, 487) action Jump("shrine")
            
    if jp_lang == True:
        image im.Scale("gui/map/asakusa_frame_jp.png", 1920, 1080)
    else:
        image im.Scale("gui/map/asakusa_frame.png", 1920, 1080)


    # Button to navigate to Ginza map
    vbox:
        xalign 0.0
        yalign 0.5
        imagebutton:
            idle im.Scale("gui/map/arrow_ginza_idle.png", 93, 219)
            hover im.Scale("gui/map/arrow_ginza_hover.png", 93, 219)
            action Jump("ginza_large")
    
    # Button to zoom out
    vbox:
        xalign 1.0
        yalign 1.0
        imagebutton:
            idle im.Scale("gui/zoomout_idle.png", 200, 200)
            hover im.Scale("gui/zoomout_hover.png", 200, 200)
            action Jump("asakusa_small")

screen asakusa_small():
    # modal True
    
    # Toggle the day_display off
    on "show" action SetVariable("day_display", False)
    on "hide" action SetVariable("day_display", True)

    imagemap:
        idle im.Scale("gui/map/asakusa_idle.png", 1920, 1080)
        hover im.Scale("gui/map/asakusa_hover.png", 1920, 1080)
        if jp_lang == True:
            ground im.Scale("gui/map/asakusa_ground_jp.png",1920,1080)
        else:
            ground im.Scale("gui/map/asakusa_ground.png", 1920, 1080)
        
        hotspot(692, 799, 311, 251) action Jump("work_cafe")
        if (unlock_movie_th == True and dayofweeknumber < 6) or (doctor_event == True and dayofweeknumber == 7 and timeslot == 1):
            hotspot(418, 1194, 582, 412) action Jump("doctor_movie")
        if unlock_dojo == True and dayofweeknumber < 6:
            hotspot(109, 1572, 394, 413) action Jump("dojo")
        hotspot(1133, 160, 581, 222) action Jump("shrine")

    if jp_lang == True:
        image im.Scale("gui/map/asakusa_frame_jp.png", 1920, 1080)
    else:
        image im.Scale("gui/map/asakusa_frame.png", 1920, 1080)

    # Button to navigate to Ginza map
    vbox:
        xalign 0.0
        yalign 0.5
        imagebutton:
            idle im.Scale("gui/map/arrow_ginza_idle.png", 93, 219)
            hover im.Scale("gui/map/arrow_ginza_hover.png", 93, 219)
            action Jump("ginza_small")

    # Button to zoom in
    vbox:
        xalign 1.0
        yalign 1.0
        imagebutton:
            idle im.Scale("gui/zoomin_idle.png", 200, 200)
            hover im.Scale("gui/zoomin_hover.png", 200, 200)
            action Jump("asakusa_large")

screen map_tutorial:

    modal True
    
    # Toggle the day_display off
    on "show" action SetVariable("day_display", False)
    on "hide" action SetVariable("day_display", True)

    if jp_lang == True:
        image im.Scale("gui/map/asakusa_ground_jp.png", 1920, 1080)
        image im.Scale("gui/map/asakusa_frame_jp.png", 1920, 1080)
    else:
        image im.Scale("gui/map/asakusa_ground.png", 1920, 1080)
        image "gui/map/asakusa_idle.png" at transform:
            xoffset 1133 yoffset 160 zoom 0.5 crop (2277, 285, 1156, 487)
        image "gui/map/asakusa_hover.png" at transform:
            xoffset 1133 yoffset 160 zoom 0.5 alpha 0.0 crop (2277, 285, 1156, 487)
            pause 1.0
            alpha 1.0
            pause 0.5
            alpha 0.0
            pause 0.5
            alpha 1.0
            pause 0.5
            alpha 0.0
            pause 0.5
            alpha 1.0
            pause 0.5
            alpha 0.0
        image im.Scale("gui/map/asakusa_frame.png", 1920, 1080)

    # Button to navigate to Ginza map
    image "gui/map/arrow_ginza_idle.png" at transform:
        xalign 0.0 yalign 0.5 zoom 0.5
    image "gui/map/arrow_ginza_hover.png" at transform:
        xalign 0.0 yalign 0.5 alpha 0.0 zoom 0.5
        pause 5.6
        alpha 1.0
        pause 0.5
        alpha 0.0
        pause 0.5
        alpha 1.0
        pause 0.5
        alpha 0.0
        pause 0.5
        alpha 1.0
        pause 0.5
        alpha 0.0

    # Kirako appears
    image "images/kirako/kirako happy.png" at transform:
        xpos 0.35 ypos 0.0 xzoom -1.0 zoom 0.5
        pause 4.0
        xzoom 1.0
        easeout 1.5 xpos 0.1 ypos 0.0
        pause 4.0

    # Cue Kirako's instructions after she appears - Asakusa Shrine
    image "images/speech.png" xalign 0.8 yalign 0.4 zoom 0.5 at transform:
        alpha 0.0 xzoom -1.0
        pause 0.6
        alpha 1.0
        pause 3.5
        alpha 0.0
    hbox:
        xalign 0.79
        yalign 0.39
        box_wrap True
        xmaximum 370
        text "Choose the place you want to visit!" textalign 0.5 yalign 0.5 size 40 at transform:
            alpha 0.0
            pause 0.6
            alpha 1.0
            pause 3.5
            alpha 0.0

    # Kirako's instructions on button to go to Ginza map
    image "images/speech.png" xalign 0.03 yalign 0.3 zoom 0.5 at transform:
        alpha 0.0 
        pause 5.6
        alpha 1.0
    hbox:
        xalign 0.045
        yalign 0.29
        box_wrap True
        xmaximum 370
        text "You can use the arrow to visit places in Ginza." textalign 0.5 yalign 0.5 size 40 at transform:
            alpha 0.0 
            pause 5.6
            alpha 1.0
    
    timer 9.0 action Hide("map_tutorial")