label shrine:
    scene bg shrine:
        zoom 0.5 xalign 1.0 yalign 1.0 
    show miko happy:
        xalign 0.75 yalign 0.5 zoom 0.35
    show shrine_counter:
        xalign 1.0 yalign 1.0 zoom 0.5
    if o_strength > 0:
        show omamori_strength:
            xpos 0.65 ypos 0.59
    else:
        show soldout:
            xpos 0.65 ypos 0.59 zoom 0.13
    if o_money > 0:
        show omamori_money:
            xpos 0.7 ypos 0.59
    else:
        show soldout:
            xpos 0.7 ypos 0.59 zoom 0.13
    if o_love > 0:
        show omamori_love:
            xpos 0.75 ypos 0.59
    else:
        show soldout:
            xpos 0.75 ypos 0.59 zoom 0.13
    if o_charisma > 0:
        show omamori_charisma:
            xpos 0.8 ypos 0.59
    else:
        show soldout:
            xpos 0.8 ypos 0.59 zoom 0.13
    if o_charisma > 0:
        show omamori_intelligence:
            xpos 0.85 ypos 0.59
    else:
        show soldout:
            xpos 0.85 ypos 0.59 zoom 0.13
    if o_job > 0:
        show omamori_job:
            xpos 0.9 ypos 0.59
    else:
        show soldout:
            xpos 0.9 ypos 0.59 zoom 0.13
    show omikuji_0:
        xalign 0.5 yalign 0.6 zoom 0.5
    pause
    miko "Welcome to Asakusa Shrine."
    show bg shrine:
        linear 3.0 xalign 1.0 yalign 0.5 zoom 0.65
    show miko:
        linear 3.0 xalign 0.63 yalign 0.6 zoom 0.6
    show shrine_counter:
        anchor (1.0,1.0)
        linear 3.0 xalign 1.0 ypos 1.28 zoom 0.8
    if o_strength > 0:
        show omamori_strength:
            linear 3.0 xpos 0.44 ypos 0.61 zoom 1.8
    else:
        show soldout:
            linear 3.0 xpos 0.44 ypos 0.61 zoom 0.234
    if o_money > 0:
        show omamori_money:
            linear 3.0 xpos 0.53 ypos 0.61 zoom 1.8
    else:
        show soldout:
            linear 3.0 xpos 0.53 ypos 0.61 zoom 0.234
    if o_love > 0:
        show omamori_love:
            linear 3.0 xpos 0.61 ypos 0.61 zoom 1.8
    else:
        show soldout:
            linear 3.0 xpos 0.61 ypos 0.61 zoom 0.234
    if o_charisma > 0:
        show omamori_charisma:
            linear 3.0 xpos 0.7 ypos 0.61 zoom 1.8
    else:
        show soldout:
            linear 3.0 xpos 0.7 ypos 0.61 zoom 0.234
    if o_intelligence > 0:
        show omamori_intelligence:
            linear 3.0 xpos 0.78 ypos 0.61 zoom 1.8
    else:
        show soldout:
            linear 3.0 xpos 0.78 ypos 0.61 zoom 0.234
    if o_job > 0:
        show omamori_job:
            linear 3.0 xpos 0.86 ypos 0.61 zoom 1.8
    else:
        show soldout:
            linear 3.0 xpos 0.86 ypos 0.61 zoom 0.234
    show omikuji_0:
        linear 3.0 xalign 0.11 yalign 0.66 zoom 0.8
    if encounters["fighter"] == 0:
        miko "Would you like to draw your fortune for 5 yen?"
        menu:
            "Yes (5 yen)" if money >=5:
                $ money -= 5
                $ encounters["fighter"] += 1
                naomi happy "I'll give it a go."
                show omikuji_0:
                    xalign 0.5 yalign 0.5 zoom 1.5
                miko "Here, go ahead and shake it."
                pause
                show omikuji_0:
                    rotate 45
                pause
                show omikuji_0:
                    rotate -45
                pause
                hide omikuji_0
                show omikuji_1:
                    xalign 0.5 yalign 0.5 zoom 1.5 rotate 40
                pause
                hide omikuji_1
                $ omikuji = renpy.random.choice(("omikuji_daikichi","omikuji_kyo"))
                if omikuji == "omikuji_daikichi":
                    show omikuji_daikichi
                    naomi happy "I got a good fortune!"
                    hide omikuji_daikichi
                    show miko happy
                    miko "Be sure to keep your good fortune close to you."
                    miko "See you again!"
                    call fighter_1_daikichi
                if omikuji == "omikuji_kyo":
                    show omikuji_kyo
                    naomi troubled "I got a bad one..."
                    hide omikuji_kyo
                    show miko happy
                    miko "Tie your fortune to the tree before you leave."
                    miko "Take care!"
                    call fighter_1_kyo
            "No":
                naomi relieved "Not this time, thank you!"
    else:
        miko "How can I help you?"
        menu:
            "Buy a charm":
                naomi happy "I would like to buy a charm."
                call screen asakusa_shrine
                pause
            "Draw fortune (5 yen)" if money >=5:
                $ money -= 5
                naomi happy "I would like to draw my fortune."
                show omikuji_0:
                    xalign 0.5 yalign 0.5 zoom 1.5
                miko "Here, go ahead and shake it."
                pause
                show omikuji_0:
                    rotate 45
                pause
                show omikuji_0:
                    rotate -45
                pause
                hide omikuji_0
                show omikuji_1:
                    xalign 0.5 yalign 0.5 zoom 1.5 rotate 40
                pause
                hide omikuji_1
                $ omikuji = renpy.random.choice(("omikuji_daikichi","omikuji_kyo"))
                if omikuji == "omikuji_daikichi":
                    show omikuji_daikichi
                    naomi happy "I got a good fortune!"
                    hide omikuji_daikichi
                    show miko happy
                    miko "Be sure to keep your good fortune close to you."
                    miko "See you again!"
                    if "omikuji_daikichi" not in inventory:
                        $ inventory.update({"omikuji_daikichi":["A slip of paper predicting good fortune."]})
                if omikuji == "omikuji_kyo":
                    show omikuji_kyo
                    naomi troubled "I got a bad one..."
                    hide omikuji_kyo
                    show miko happy
                    miko "Tie your fortune to the tree before you leave."
                    miko "Take care!"
            "Nothing":
                naomi happy "It's alright, thanks!"
    # Deduct timeslot and check if morning or afternoon
    show bg shrine:
        linear 3.0 zoom 0.5 xalign 1.0 yalign 1.0 
    show miko happy:
        linear 3.0 xalign 0.75 yalign 0.5 zoom 0.35
    show shrine_counter:
        linear 3.0 xalign 1.0 yalign 1.0 zoom 0.5
    if o_strength > 0:
        show omamori_strength:
            linear 3.0 xpos 0.65 ypos 0.59 zoom 1.0
    else:
        show soldout:
            linear 3.0 xpos 0.65 ypos 0.59 zoom 0.13
    if o_money > 0:
        show omamori_money:
            linear 3.0 xpos 0.7 ypos 0.59 zoom 1.0
    else:
        show soldout:
            linear 3.0 xpos 0.7 ypos 0.59 zoom 0.13
    if o_love > 0:
        show omamori_love:
            linear 3.0 xpos 0.75 ypos 0.59 zoom 1.0
    else:
        show soldout:
            linear 3.0 xpos 0.75 ypos 0.59 zoom 0.13
    if o_charisma > 0:
        show omamori_charisma:
            linear 3.0 xpos 0.8 ypos 0.59 zoom 1.0
    else:
        show soldout:
            linear 3.0 xpos 0.8 ypos 0.59 zoom 0.13
    if o_intelligence > 0:
        show omamori_intelligence:
            linear 3.0 xpos 0.85 ypos 0.59 zoom 1.0
    else:
        show soldout:
            linear 3.0 xpos 0.8 ypos 0.59 zoom 0.13
    if o_job > 0:
        show omamori_job:
            linear 3.0 xpos 0.9 ypos 0.59 zoom 1.0
    else:
        show soldout:
            linear 3.0 xpos 0.9 ypos 0.59 zoom 0.13
    show omikuji_0:
        linear 3.0 xalign 0.5 yalign 0.6 zoom 0.5
    menu:
        "Leave":
            $ timeslot -= 1
            if dayofweeknumber > 5:
                return
            else:
                if timeslot == 1:
                    jump asakusa_small
                if timeslot < 1:
                    jump evening_time
        "Stay":
            jump shrine

label fighter_1_daikichi:
    $ fighter_name = "???"
    window hide
    show bg shrine:
        linear 3.0 zoom 0.5 xalign 1.0 yalign 1.0 
    show miko happy:
        linear 3.0 xalign 0.75 yalign 0.5 zoom 0.35
    show shrine_counter:
        linear 3.0 xalign 1.0 yalign 1.0 zoom 0.5
    if o_strength > 0:
        show omamori_strength:
            linear 3.0 xpos 0.65 ypos 0.59 zoom 1.0
    if o_money > 0:
        show omamori_money:
            linear 3.0 xpos 0.7 ypos 0.59 zoom 1.0
    if o_love > 0:
        show omamori_love:
            linear 3.0 xpos 0.75 ypos 0.59 zoom 1.0
    if o_charisma > 0:
        show omamori_charisma:
            linear 3.0 xpos 0.8 ypos 0.59 zoom 1.0
    if o_intelligence > 0:
        show omamori_intelligence:
            linear 3.0 xpos 0.85 ypos 0.59 zoom 1.0
    if o_job > 0:
        show omamori_job:
            linear 3.0 xpos 0.9 ypos 0.59 zoom 1.0
    show omikuji_0:
        xalign 0.11 yalign 0.66 zoom 0.8
        linear 3.0 xalign 0.5 yalign 0.6 zoom 0.5
    show fighter bummed:
        xpos -0.7 yalign 0.5 zoom 1.75
        linear 3.0 xalign 0.4 yalign 0.5 zoom 1.0
    pause
    fighter "Ah, crap! I got a bad one."
    menu:
        "Offer yours":
            naomi relieved "Here, you can have mine instead."
            window hide
            show omikuji_daikichi:
                zoom 0.5 xalign 0.8 yalign 0.8
            pause
            show fighter surprised
            fighter "Eh? Are you serious?"
            show fighter blush
            fighter "A pretty girl is offering me her good fortune?"
            naomi blush "..."
            show fighter happy
            fighter "Thank you for the kind offer. But I can't possibly take your good fortune."
            show fighter grin
            fighter "I'll be fine, don't worry about me!"
            naomi thinking "How about this?"
            window hide
            hide omikuji_daikichi
            show fighter surprised
            show omikuji_daikichi_tear:
                zoom 0.5 xalign 0.8 yalign 0.8
            pause
            hide omikuji_daikichi_tear
            show omikuji_daikichi_half:
                xalign 0.75 yalign 0.8 zoom 0.5
            show omikuji_daikichi_half2:
                xalign 0.85 yalign 0.8 zoom 0.5
            naomi happy "Here, we can share it."
            hide omikuji_daikichi_half with moveoutbottom
            naomi relieved "Take this half."
            $ inventory.update({"omikuji_daikichi_half":["Half of an omikuji."]})
            show fighter blush
            fighter blush "..."
            show fighter grin
            fighter "I'm glad! Thank you!"
            hide omikuji_daikichi_half2
            show fighter wink
            fighter "Hopefully, the good fortune will let us meet again."
            naomi blush "..."
            show fighter grin
            fighter "See you around!"
            show fighter happy
            hide fighter with moveoutleft
        "Show sympathy":
            $ inventory.update({"omikuji_daikichi":["A slip of paper predicting good fortune."]})
            naomi troubled "That's too bad."
            naomi thinking "Is there anything I can do for you?"
            show fighter grin
            fighter "Just one of those days!"
            show fighter happy
            fighter "My fortune can't be that bad, to have a pretty girl talk to me."
            naomi blush "..."
            show fighter angry
            fighter "What?! Damn bird just crapped on me!"
            naomi surprised "What?! Are you alright?"
            show fighter grin
            fighter "Yeah don't worry about it, I'm fine!"
            show fighter wink
            fighter "See you around!"
            hide fighter with moveoutleft
    return

label fighter_1_kyo:
    $ fighter_name = "???"
    window hide
    show bg shrine:
        linear 3.0 zoom 0.5 xalign 1.0 yalign 1.0 
    show miko happy:
        linear 3.0 xalign 0.75 yalign 0.5 zoom 0.35
    show shrine_counter:
        linear 3.0 xalign 1.0 yalign 1.0 zoom 0.5
    if o_strength > 0:
        show omamori_strength:
            linear 3.0 xpos 0.65 ypos 0.59 zoom 1.0
    if o_money > 0:
        show omamori_money:
            linear 3.0 xpos 0.7 ypos 0.59 zoom 1.0
    if o_love > 0:
        show omamori_love:
            linear 3.0 xpos 0.75 ypos 0.59 zoom 1.0
    if o_charisma > 0:
        show omamori_charisma:
            linear 3.0 xpos 0.8 ypos 0.59 zoom 1.0
    if o_intelligence > 0:
        show omamori_intelligence:
            linear 3.0 xpos 0.85 ypos 0.59 zoom 1.0
    if o_job > 0:
        show omamori_job:
            linear 3.0 xpos 0.9 ypos 0.59 zoom 1.0
    show omikuji_0:
        xalign 0.11 yalign 0.66 zoom 0.8
        linear 3.0 xalign 0.5 yalign 0.6 zoom 0.5
    show fighter determined:
        xpos -0.7 yalign 0.5 zoom 1.75
        easein 3.0 xalign 0.5 yalign 0.5 zoom 1.0
    pause
    fighter "Hey, pretty girl."
    show fighter grin
    fighter "Here, take mine."
    show omikuji_daikichi:
        zoom 0.5 xalign 0.8 yalign 0.8
    naomi surprised "Eh? But..."
    show fighter wink
    fighter "And I'll take yours."
    show omikuji_kyo:
        xalign 0.5 zoom 1.0
        easein 1.0 zoom 0.2 xalign 0.5 yalign 0.8
    window hide
    pause
    hide omikuji_kyo
    show fighter grin:
        zoom 0.1 xalign 0.35 yalign 0.6 xzoom -1.0 matrixcolor BrightnessMatrix(-0.5)
    pause
    show fighter happy:
        zoom 1.0 xalign 0.5 matrixcolor BrightnessMatrix(0)
    fighter "...and there. Tied it to the tree."
    menu:
        "Accept with thanks":
            naomi blush "Thank you..."
            hide omikuji_daikichi with moveoutbottom
            $ inventory.update({"omikuji_daikichi":["A slip of paper predicting good fortune."]})
            show fighter angry
            fighter "What?! Damn bird just crapped on me!"
            naomi surprised "What?! Are you alright?"
            show fighter grin
            fighter "Yeah don't worry about it, I'm fine!"
            naomi relieved "If we meet again, please let me return the favor."
            show fighter happy
            fighter "I'll remember that!"
            show fighter wink
            fighter "See you around!"
            hide fighter with moveoutleft
            return
        "Offer half":
            naomi thinking "I have an idea..."
            window hide
            hide omikuji_daikichi
            show fighter surprised
            show omikuji_daikichi_tear:
                zoom 0.5 xalign 0.8 yalign 0.8
            pause
            hide omikuji_daikichi_tear
            show omikuji_daikichi_half:
                xalign 0.75 yalign 0.8 zoom 0.5
            show omikuji_daikichi_half2:
                xalign 0.85 yalign 0.8 zoom 0.5
            naomi happy "Here, take half."
            hide omikuji_daikichi_half with moveoutbottom
            $ inventory.update({"omikuji_daikichi_half":["Half of an omikuji."]})
            naomi happy "We can share the good fortune."
            show fighter blush
            fighter "..."
            show fighter grin
            fighter "I'm glad! Thank you!"
            hide omikuji_daikichi_half2
            show fighter wink
            fighter "Hopefully, the good fortune will let us meet again."
            naomi blush "..."
            show fighter grin
            fighter "See you around!"
            show fighter happy
            hide fighter with moveoutleft
            return

label omamori_strength:
    show miko happy:
        xalign 0.9
    menu:
        miko_bubble "A charm that will increase your strength, for 15 yen."
        "Buy." if money >= 15:
            show omamori_strength:
                zpos 0 zoom 1.0
                easein 1.0 xalign 0.5 yalign 0.6 zpos 900
            pause
            hide omamori_strength with moveoutbottom
            $ money -= 15
            $ inventory.update({"omamori_strength":["A charm that will increase strength."]})
            $ o_strength -= 1
            call screen asakusa_shrine
        "Don't buy.":
            call screen asakusa_shrine

label omamori_money:
    show miko happy:
        xalign 0.9
    menu:
        miko_bubble "A charm that will increase your luck for wealth, for 15 yen."
        "Buy." if money >= 15:
            show omamori_money:
                zpos 0 zoom 1.0
                easein 1.0 xalign 0.5 yalign 0.6 zpos 900
            pause
            hide omamori_money with moveoutbottom
            $ money -= 15
            $ inventory.update({"omamori_money":["A charm that will increase luck for wealth."]})
            $ o_money -= 1
            call screen asakusa_shrine
        "Don't buy.":
            call screen asakusa_shrine

label omamori_love:
    show miko happy:
        xalign 0.9
    menu:
        miko_bubble "A charm that will increase your luck in love, for 15 yen."
        "Buy." if money >= 15:
            show omamori_love:
                zpos 0 zoom 1.0
                easein 1.0 xalign 0.5 yalign 0.6 zpos 900
            pause
            hide omamori_love with moveoutbottom
            $ money -= 15
            $ inventory.update({"omamori_love":["A charm that will increase luck in love."]})
            $ o_love -= 1
            call screen asakusa_shrine
        "Don't buy.":
            call screen asakusa_shrine

label omamori_charisma:
    show miko happy:
        xalign 0.9
    menu:
        miko_bubble "A charm that will increase your charisma, for 15 yen."
        "Buy." if money >= 15:
            show omamori_charisma:
                zpos 0 zoom 1.0
                easein 1.0 xalign 0.5 yalign 0.6 zpos 900
            pause
            hide omamori_charisma with moveoutbottom
            $ money -= 15
            $ inventory.update({"omamori_charisma":["A charm that will increase charisma."]})
            $ o_charisma -= 1
            call screen asakusa_shrine
        "Don't buy.":
            call screen asakusa_shrine

label omamori_intelligence:
    show miko happy:
        xalign 0.9
    menu:
        miko_bubble "A charm that will increase your intelligence, for 15 yen."
        "Buy." if money >= 15:
            show omamori_intelligence:
                zpos 0 zoom 1.0
                easein 1.0 xalign 0.5 yalign 0.6 zpos 900
            pause
            hide omamori_intelligence with moveoutbottom
            $ money -= 15
            $ inventory.update({"omamori_intelligence":["A charm that will increase intelligence."]})
            $ o_intelligence -= 1
            call screen asakusa_shrine
        "Don't buy.":
            call screen asakusa_shrine

label omamori_job:
    show miko happy:
        xalign 0.9
    menu:
        miko_bubble "A charm that will increase your job performance, for 15 yen."
        "Buy." if money >= 15:
            show omamori_job:
                zpos 0 zoom 1.0
                easein 1.0 xalign 0.5 yalign 0.6 zpos 900
            pause
            hide omamori_job with moveoutbottom
            $ money -= 15
            $ inventory.update({"omamori_job":["A charm that will increase job performance."]})
            $ o_job -= 1
            call screen asakusa_shrine
        "Don't buy.":
            call screen asakusa_shrine
