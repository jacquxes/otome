## Maps ##

label ginza_large:
        
    call screen ginza_large
    pause

label ginza_small:
        
    call screen ginza_small
    pause

label asakusa_large:
        
    call screen asakusa_large
    pause

label asakusa_small:
        
    call screen asakusa_small
    pause

label reset_daily_visits:
    python:
        for c in visited_today:
            visited_today[c] = False
        cafe_menu = []
    return

## Day Change ##

## Morning Sequence ##

label next_morning:

    # Reset daily visit flags and clear today's menu
    call reset_daily_visits

    # Day change
    $ totaldays -= 1
    $ dayofweeknumber += 1
    $ timeslot = 2

    # Check for weekend
    if dayofweeknumber == 8:
        $ dayofweeknumber = 1
    elif dayofweeknumber == 6:
        jump weekend_saturday
    elif dayofweeknumber == 7:
        jump weekend_sunday

    scene bg cafeleft with fade
    play music "<from 1 to 79.5>spring.mp3" loop if_changed
    if tutorial_mode == True:
        # $ first_encounter.append("musician")
        # $ first_encounter.append("doctor")
        show table_left zorder 2.0:
            xalign 1.0 yalign 1.0 zoom 0.5
        show kirako pout with moveinright
        kirako "Bless me, I forgot to give you this yesterday."
        naomi sleepy "Good morning."
        show kirako happy
        kirako "Here's a map to help you find your way around the city."
        image map = "images/cafe/map.png"
        show map zorder 3.0:
            xpos 0.4 ypos 0.5 zpos 0 zoom 0.25
            easein 1.0 ypos 0.6 zpos 800
        kirako "Shall I show you how to use it?"
        menu:
            "Yes":
                window hide
                show screen map_tutorial
                pause
            "No":
                naomi relieved "It's alright, I'll figure it out."
        show kirako pout
        kirako "Going somewhere or working at the cafe will take up half your day, so plan your time wisely!"
        naomi happy "I'll do that! Thank you, Miss Kirako!"
        hide map with moveoutbottom
        $ inventory.update({"map":["A map of the city."]})
        show kirako happy
        kirako "Have a fun day!"
        hide kirako with moveoutright
        $ tutorial_mode = False
        menu:
            naomi thinking "What shall I do this morning?"
            "Work at the cafe":
                jump work_cafe
            "Go out":
                stop music fadeout 3
                jump asakusa_small
    if doctor_dream == True:
        $ doctor_dream = False
        show cat eyeroll
        naomi sleepy "What a strange dream."
        show cat neutral
        cat "What dream?"
        naomi troubled "I felt like I was waking from sleep."
        naomi thinking "Someone was holding my hand..."
        cat "Who?"
        naomi thinking "(That warmth...)"
        naomi blush "[doctor_name]..."
        show cat happy
        cat "You could ask him about it."
        naomi surprised "And let him know I was dreaming about him?"
        naomi blush "I'll die of embarassment!"
        show cat neutral
        cat "It might change things."
        hide cat with moveoutbottom
        naomi troubled "Change things?"
        #naomi pain "Anyway..."
    if musician_dream == True:
        $ musician_dream = False
        show cat eyeroll
        naomi sleepy "I dreamt of a song."
        show cat neutral
        cat "A song?"
        naomi troubled "Like a song that I've forgotten."
        naomi pain "Such a lonesome tune..."
        naomi thinking "(That music...)"
        naomi blush "Hideo..."
        show cat happy
        cat "Have him play it for you."
        cat "Maybe you might recall something."
        hide cat with moveoutbottom
        naomi troubled "Maybe..."
        #naomi pain "Anyway..."
    if totaldays == 0:
        show kirako pout with moveinright        
        show table_left:
            xalign 1.0 yalign 1.0 zoom 0.5
        kirako "Oh Naomi, how time flies!" 
        kirako "I can't believe it's been two weeks already."
        naomi relieved "It feels like yesterday that I arrived."
        kirako "Have you found a place to take you in?"
        menu:
            naomi happy "Yes, I'll work at..."
            "The Imperial Theatre" if musician_job >=7:
                naomi happy "The Imperial Theatre."
                show kirako happy
                kirako "A lovely place."
                show kirako wink
                kirako "I'll find you when I need to get my hands on those sold-out shows!"
                naomi happy "Most certainly!"
                naomi happy "Thank you letting me stay here. I will head over now."
                show kirako pout
                kirako "Goodbye dear!"
                jump imperial_theatre
            "The hospital" if doctor_job >=7:
                naomi happy "The hospital."
                show kirako happy
                kirako "A place for healing."
                show kirako wink
                kirako "I'll know who to look for when I'm sick."
                naomi happy "Most certainly!"
                naomi happy "Thank you letting me stay here. I will head over now."
                show kirako pout
                kirako "Goodbye dear!"
                jump hospital
            "The office" if merchant_job >=7:
                naomi happy "The office."
                show kirako happy
                kirako "A good choice."
                show kirako wink
                kirako "I heard they pay well!"
                naomi blush "It's alright I guess."
                naomi happy "Thank you letting me stay here. I will head over now."
                show kirako pout
                kirako "Goodbye dear!"
                jump office_bldg
        naomi troubled "No..."
        kirako "Oh dear. Will you be heading back home then?"
        naomi happy "Yes, I'll come by again when I can."
        show kirako happy
        kirako "You're always welcome here, remember that."
        naomi happy "Thank you, I'll be back!"
        naomi thinking "(I wonder what happened to Maachan....)"
        stop music fadeout 3
        $ day_display = False
        show black1:
            xalign 0.5 yalign 1.0 #full close
        show black2:
            xalign 0.5 yalign 0.0 #full close
        show text "{color=#ffffff}Game over.{/color}":
            xalign 0.5 yalign 0.5
        with Fade(2.0,0.5,0.5)
        pause
        return
    menu:
        naomi sleepy "It's morning. What shall I do today?"
        "Work at the cafe":
            jump work_cafe
        "Go out":
            stop music fadeout 3
            jump asakusa_small

## shorten weekend if no event, if dream provide end location as an option

label weekend_saturday:
    scene bg cafeleft with fade
    play music "<from 1 to 79.5>spring.mp3" loop if_changed
    naomi sleepy "It's Saturday."
    if musician_event == 1:
        naomi thinking "The cello performance is this afternoon."
    if merchant_event == True:
        naomi thinking "I have to go with Yujiro to the dance hall tonight."
        if "dress_flapper" in wardrobe_dress:
            naomi happy "I can wear that dress I bought."
        else:
            naomi troubled "I don't have anything appropriate to wear." 
    menu:
        naomi thinking "What should I do this morning?"
        "Visit department store":
            stop music fadeout 3.0
            call dept_store
        "Visit Asakusa Shrine":
            stop music fadeout 3.0
            call shrine
        "Work at the cafe":
            call work_cafe
    scene bg cafeleft with fade
    if musician_event == 1:
        jump musician_show
    menu:
        naomi thinking "What should I do this afternoon?"
        "Visit department store":
            stop music fadeout 3.0
            call dept_store
        "Visit Asakusa Shrine":
            stop music fadeout 3.0
            call shrine
        "Work at the cafe":
            call work_cafe
    if merchant_event == True:
        jump merchant_dance
    else:
        scene bg cafeleft with fade
        naomi sleepy "It's been a long day. I'll head to bed."
    jump evening_time

label weekend_sunday:
    scene bg cafeleft with fade
    if merchant_dream == True:
        $ merchant_dream = False
        show cat eyeroll
        naomi sleepy "I had a strange dream."
        show cat neutral
        cat "What dream?"
        naomi troubled "I felt like I was waking from a long dream."
        naomi thinking "Someone was calling my name..."
        cat "Who?"
        naomi thinking "(...Cedarwood scent.)"
        naomi blush "Yujiro."
        show cat happy
        cat "Ask him about it."
        naomi surprised "And let him know I was dreaming about him?"
        naomi blush "That's too embarassing!"
        show cat neutral
        cat "You might discover something important."
        hide cat with moveoutright
        naomi troubled "Important?"
        naomi pain "Anyway..."
    naomi sleepy "It's Sunday."
    if doctor_event == True:
        naomi thinking "I have to meet Shiro for the movie later."
        if "dress_prim" in wardrobe_dress:
            naomi happy "I can wear that green dress I bought."
        else:
            naomi troubled "I don't have anything appropriate to wear."
    if musician_event == 3:
        naomi thinking "Oh yes, Hideo's taking me somewhere in the evening."
        naomi blush "It's a date...?"
        if "dress_modern" in wardrobe_dress:
            naomi blush "The kimono with the artistic pattern reminds me of Hideo... I could wear that."
        else:
            naomi troubled "I should wear a nicer kimono... In case it's a date."
    menu:
        naomi thinking "Where should I go this morning?"
        "Visit department store":
            call dept_store
        "Visit Asakusa Shrine":
            call shrine
        "Work at the cafe":
            call work_cafe
    scene bg cafeleft with fade
    if doctor_event == True:
        jump doctor_movie
    else:
        menu:
            naomi thinking "What should I do this afternoon?"
            "Visit department store":
                call dept_store
            "Visit Asakusa Shrine":
                call shrine
            "Work at the cafe":
                call work_cafe
    scene bg cafeleft with fade
    if musician_event == 3:
        jump musician_tower
    naomi sleepy "It's been a long day. I'll head to bed."
    jump evening_time

label re_evening_time:
    scene bg bedroom with dissolve
    show kirako happy zorder 3.0 with moveinleft
    kirako "Here's your room."
    show bedroom_dresser zorder 2.0:
        zoom 0.5 xpos 1119 ypos 262 matrixcolor BrightnessMatrix(0.2)
    kirako "You can use the dresser to change or put on makeup."
    hide bedroom_dresser
    show bedroom_bed zorder 2.0:
        zoom 0.5 xalign 0.0 yalign 1.0 matrixcolor BrightnessMatrix(0.2)
    kirako "Just hop into bed when you're ready to end the day!"
    hide bedroom_bed
    naomi relieved "Got it, thank you!"
    kirako "Have a good rest."
    hide kirako with moveoutleft
    show cat eyeroll:
        xpos -0.5 ypos 0.2 zoom 2.5 blur 10.0
        easein 3.0 xalign 0.7 yalign 0.5 zoom 1.0 blur 0.0
    cat "Meow."
    naomi happy "Aww hello! It's you again."
    show cat huff:
        xalign 0.7 yalign 0.5 zoom 1.0 blur 0.0
    cat "Meow."
    naomi troubled "You know, I just can't recall anything."
    show cat neutral
    naomi relieved "But since I'm here, I'll do what I can to help Kirako."
    cat "Meow."
    naomi thinking "Hopefully along the way, I'll remember something."
    naomi sleepy "But now, it's time for bed."
    cat "Meow."
    hide cat with moveoutbottom
    naomi relieved "Goodnight to you too."
    # cat "You can't be here meow."
    # naomi surprised "It spoke?"
    # show cat neutral
    # cat "But don't worry meow."
    # show cat happy
    # cat "I'll help you meow."
    # hide cat with moveoutbottom
    # naomi troubled "(I definitely need some sleep.)"
    call screen bedroom

label evening_time:

    if merchant_event == True and dayofweeknumber == 6:
        call merchant_dance
    else:    
        scene bg bedroom with dissolve
        call screen bedroom

    # # Maachan prompt for cafe encounters
    # if totaldays > 4 and len(first_encounter) > 0:
    #     show cat neutral
    #     cat "Meow."
    #     naomi surprised "Oh!"
    #     naomi relieved "It's you."
    #     $ cat_random = renpy.random.randint(1, 3)
    #     if cat_random == 1:
    #         show cat huff
    #         cat "Kirako could use your help at the cafe meow."
    #     if cat_random == 2:
    #         show cat eyeroll
    #         cat "Aren't you short on cash yet?"
    #     if cat_random == 3:
    #         show cat huff
    #         cat "Did you forget that you're here to find a job?"
    #     show cat neutral
    #     cat "Talking to customers could land you a job meow."
    #     naomi troubled "Alright, I got it."
    #     show cat eyeroll
    #     $ cat_random = renpy.random.randint(1, 5)
    #     if cat_random == 1:
    #         cat "Sure you did."
    #     if cat_random == 2:
    #         cat "Uh huh."
    #     if cat_random == 3:
    #         cat "Good luck."
    #     if cat_random == 4:
    #         cat "'Kay."
    #     if cat_random == 5:
    #         cat "Whatever you say."
    #     hide cat with moveoutbottom
    #     naomi troubled "Kirako has been very kind to let me stay here."
    #     naomi thinking "I should start working more shifts from tomorrow."

    # # Maachan prompt for external encounters
    # if totaldays > 4 and len(second_encounter) < 3:
    #     show cat neutral
    #     cat "Meow."
    #     naomi surprised "Ah!"
    #     naomi relieved "You surprised me."
    #     show cat huff
    #     cat "You need to visit more places meow."
    #     if "fighter" not in second_encounter:
    #         show cat neutral
    #         cat "Draw your fortune at Asakusa Shrine meow."
    #     if "merchant" not in second_encounter:
    #         show cat eyeroll
    #         cat "Pick up something at the department store meow."
    #     if "soldier" not in second_encounter:
    #         show cat huff
    #         cat "Take a walk to Tokyo Station meow."
    #     naomi troubled "Alright, I got it."
    #     show cat eyeroll
    #     $ cat_random = renpy.random.randint(1, 5)
    #     if cat_random == 1:
    #         cat "Sure you did."
    #     if cat_random == 2:
    #         cat "Uh huh."
    #     if cat_random == 3:
    #         cat "Good luck."
    #     if cat_random == 4:
    #         cat "'Kay."
    #     if cat_random == 5:
    #         cat "Whatever you say."
    #     hide cat with moveoutbottom
    #     naomi thinking "Maybe this is a sign I should take a break and relax."
    #     naomi happy "I should go explore somewhere new tomorrow."

    

label end_day:
    menu:
        "End the day":
            naomi sleepy "It's been a long day. I'll head to bed now."
            if merchant_dream == True and merchant_courage > 2:
                $ day_display = False
                define fadehold = Fade (1.0,1.0,2.0)
                image black1 = "black_1.png"
                image black2 = "black_2.png"
                show black1:
                    xalign 0.5 yalign 1.0
                show black2:
                    xalign 0.5 yalign 0.0
                show text "{color=#ffffff}'Naomi... Naomi...'{/color}":
                    xalign 0.5 yalign 0.8
                with fadehold
                pause
                scene bg irl:
                    xalign 0.5 yalign 0.0 blur 20.0 matrixcolor BrightnessMatrix(0.5)
                    easein 4.8 blur 10.0 matrixcolor BrightnessMatrix(0.2)
                    pause 0.5
                    xalign 1.0 zoom 0.8 blur 15.0 matrixcolor BrightnessMatrix(0.4)
                show black1:
                    xalign 0.5 yalign 1.0 #full close
                    easein 3.5 yalign 1.3 #part open
                    pause 0.5
                    easein 2.5 yalign 1.0 #full close
                show black2:
                    xalign 0.5 yalign 0.0 #full close
                    easein 3.5 yalign -0.3 #part open
                    pause 0.5
                    easein 2.5 yalign 0.0 #full close
                show text "{color=#ffffff}Cedarwood scent...{/color}":
                    xalign 0.5 yalign 0.8
                pause
                $ day_display = True
                jump next_morning
            if doctor_dream == True and doctor_courage > 2:
                $ day_display = False
                define fadehold = Fade (1.0,1.0,2.0)
                image black1 = "black_1.png"
                image black2 = "black_2.png"
                show black1:
                    xalign 0.5 yalign 1.0
                show black2:
                    xalign 0.5 yalign 0.0
                show text "{color=#ffffff}'Naomi, I'm here...'{/color}":
                    xalign 0.5 yalign 0.8
                with fadehold
                pause
                scene bg irl:
                    xalign 0.5 yalign 0.0 blur 20.0 matrixcolor BrightnessMatrix(0.5)
                    easein 4.8 blur 10.0 matrixcolor BrightnessMatrix(0.2)
                    pause 0.5
                    xalign 1.0 zoom 0.8 blur 15.0 matrixcolor BrightnessMatrix(0.4)
                show black1:
                    xalign 0.5 yalign 1.0 #full close
                    easein 3.5 yalign 1.3 #part open
                    pause 0.5
                    easein 2.5 yalign 1.0 #full close
                show black2:
                    xalign 0.5 yalign 0.0 #full close
                    easein 3.5 yalign -0.3 #part open
                    pause 0.5
                    easein 2.5 yalign 0.0 #full close
                show text "{color=#ffffff}So warm...{/color}":
                    xalign 0.5 yalign 0.8
                pause
                show text "{color=#ffffff}The feeling of someone's hand in mine...{/color}":
                    xalign 0.5 yalign 0.8
                pause
                $ day_display = True
                jump next_morning
            if musician_dream == True and musician_courage > 2:
                $ day_display = False
                define fadehold = Fade (1.0,1.0,2.0)
                image black1 = "black_1.png"
                image black2 = "black_2.png"
                show black1:
                    xalign 0.5 yalign 1.0
                show black2:
                    xalign 0.5 yalign 0.0
                # show text "{color=#ffffff}'Naomi... Naomi...'{/color}":
                #     xalign 0.5 yalign 0.8
                with fadehold
                pause
                scene bg irl:
                    xalign 0.5 yalign 0.0 blur 20.0 matrixcolor BrightnessMatrix(0.5)
                    easein 4.8 blur 10.0 matrixcolor BrightnessMatrix(0.2)
                    pause 0.5
                    xalign 1.0 zoom 0.8 blur 15.0 matrixcolor BrightnessMatrix(0.4)
                show black1:
                    xalign 0.5 yalign 1.0 #full close
                    easein 3.5 yalign 1.3 #part open
                    pause 0.5
                    easein 2.5 yalign 1.0 #full close
                show black2:
                    xalign 0.5 yalign 0.0 #full close
                    easein 3.5 yalign -0.3 #part open
                    pause 0.5
                    easein 2.5 yalign 0.0 #full close
                show text "{color=#ffffff}This music... where have I heard it?{/color}":
                    xalign 0.5 yalign 0.8
                pause
                $ day_display = True
                jump next_morning
            else:
                jump next_morning
        "Stay up":
            call screen bedroom

label movie_theatre:
    
    scene bg movie theatre
    pause
    jump asakusa_small

label dojo:
    
    scene bg dojo
    $ timeslot -= 1
    $ strength += 1
    if strength >= 3:
        "I encounter a monster"
    elif strength >= 2:
        "I became stronger"
    elif strength >= 1:
        "I died"
    if timeslot == 1:
        jump asakusa_small
    if timeslot < 1:
        jump evening_time

label tokyo_station:

    scene bg station
    pause
    # Deduct timeslot and check if morning or afternoon
    $ timeslot -= 1
    if timeslot == 1:
        jump ginza_small
    if timeslot < 1:
        jump evening_time
