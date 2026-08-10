label merchant_dance:

    # Pickup at cafe
    scene bg cafeleft with dissolve
    show kirako happy with moveinright
    kirako "Yujiro's here for your date."
    naomi blush "It's not a date!"
    naomi troubled "It's for work."
    show kirako wink
    kirako "Sure, dear."
    if naomi_dress == "dress_flapper":
        show kirako happy
        kirako "I see you're ready to dance all night."
    else:
        show kirako happy
        kirako "Go change into your dancing clothes."
    show kirako wink
    kirako "Have fun!"
    show kirako happy
    hide kirako with moveoutleft
    menu:
        "Change clothes":
            naomi thinking "I'll change clothes quickly."
            window hide
            show screen wardrobe
            naomi happy "I'm ready."
        "Meet Yujiro":
            naomi happy "I'm ready."
    show bg caferight
    show cafetableright zorder 3.0
    show merchant frownside_suit:
        xalign 0.5
    with pushleft
    $ merchant_name = "Yujiro"
    if naomi_dress == "dress_flapper":
        show merchant frownside_suit
        naomi troubled "Did you wait long?"
        show merchant frown_suit
        merchant "No, I just..."
        show merchant surprised_suit
        naomi troubled "...Do I look alright?"
        merchant "..."
        show merchant smile_suit
        merchant "You look beautiful."
        naomi blush "..."
        naomi relieved "Thank you."
        naomi blush "You look very dashing too."
        show merchant surprised_suit
        merchant "..."
        show merchant happy_suit
        merchant "Thanks."
        merchant "Shall we go?"
        naomi happy "Yes."
        show merchant frownside_suit:
            xzoom -1.0 zoom 1.0
    else:
        show merchant frownside_suit
        naomi troubled "Did you wait long?"
        show merchant frown
        merchant "No, I just..."
        show merchant surprised_suit
        merchant "..."
        naomi troubled "Is something wrong?"
        show merchant resigned_suit
        merchant "Nothing."
        show merchant frown_suit
        merchant "Shall we go?"
        naomi happy "Yes."
        show merchant frown_suit:
            xzoom -1.0 zoom 1.0

    # At dance hall
    hide merchant
    hide cafetableright
    hide bg caferight
    show bg dancehall 1
    show merchant frownside_suit:
        xalign 0.5
    with fade
    naomi relieved "This place is so grand..."
    show merchant happy_suit
    merchant "Do you like it?"
    merchant "There are other places like this, I'll bring you next time."
    naomi blush "(Next time?!)"
    show merchant frownside_suit
    merchant "Endo is over there." 
    naomi blush "(Right, this is work!)"
    merchant "I have to catch him before the dancing starts."
    naomi blush "(I need to calm down.)"
    naomi blush "G-go ahead without me!"
    show merchant frown_suit
    merchant "Will you be alright here alone?"
    show merchant frown_suit:
        zoom 1.0
        easein 1.0 zoom 1.3 yalign 0.3
    merchant "You look a little flushed."
    naomi blush "...I'm just a little warm."
    naomi happy "I'll be fine after a little rest."
    show merchant frown_suit:
        easeout 1.0 zoom 1.0 yalign 0.0
    merchant "Alright, don't overexert yourself."
    show merchant frownside_suit
    merchant "Wait here for me."
    hide merchant with MoveTransition(1.0,leave=offscreenright)
    naomi pain "Phew."
    naomi thinking "(I know this is work but.)"
    naomi blush "(Why is my heart beating so quickly?)"
    show stranger with moveinleft:
        xalign 0.5
    stranger "Are you alone, miss?"
    naomi surprised "Uh, me?"
    show stranger zorder 3.0:
        easeout 2.0 zoom 2.0 yalign 0.25 xalign 0.5
    stranger "Would you like to dance?"
    naomi troubled "Umm... I'm here with someone."
    show merchant scowlfront_suit with moveinleft
    merchant "Oi. Leave her alone."
    show stranger:
        zoom 2.0 yalign 0.25 xalign 0.5
        easein 1.0 zoom 1.0 yalign 0.7 xpos 0.7 blur 0.0
    show merchant frownside_suit
    stranger "I- I'm sorry!"
    hide stranger with moveoutright
    show merchant scowlfront_suit:
        zoom 1.0
        linear 1.0 xalign 0.5
    merchant "Was he bothering you?"
    naomi relieved "He was looking for someone to dance with."
    show merchant frownside_suit
    merchant "I see."
    naomi thinking "But doesn't he have a partner?"
    show merchant frown_suit
    merchant "Hm?"
    naomi thinking "You told me it's the rule of the dance hall, to come with a partner."
    show merchant surprised_suit
    merchant "..."
    show merchant scowlside_suit
    merchant "I just wanted to bring you with me."
    naomi blush "..."
    naomi relieved "You could have just said so."
    show merchant surprised_suit
    merchant "..."
    show merchant smile_suit
    merchant "I'll do that next time."
    naomi blush "(Next time?)"
    if naomi_dress == "dress_flapper":
        play music "<from 7>dance.mp3" fadein 3
        show merchant frownside_suit
        merchant "Music's starting."        
        show bg dancehall 2:
            matrixcolor BrightnessMatrix(0)
            linear 2.0 zoom 1.2 yalign 0.8 blur 5.0 matrixcolor BrightnessMatrix(-0.1)
        show merchant happy_suit:
            zoom 1.0 yanchor 0.0
            linear 2.0 zoom 2.5 yanchor 0.0 ypos -0.5 matrixcolor BrightnessMatrix(-0.05)
        merchant "Here."
        show bg dancehall 2:
            linear 2.0 zoom 1.3 yalign 0.0 blur 10.0
        show merchant happy_suit:
            linear 2.0 zoom 3.5 yalign 0.15
        naomi blush "...But I don't know how to dance."
        merchant "It's fine. Just follow my lead."
        show bg dancehall 2:
            ease 3.0 xalign 1.0 yalign 0.0
            ease 3.0 xalign 0.5 yalign 0.0
        show merchant happy_suit:
            pause 3.0
            xzoom -1.0
        naomi blush "(He's so close!)"
        hide window
        hide merchant
        show merchant_cutscene_2:
            zoom 1.1 xalign 0.0 yalign 0.8
        with Fade(2.0,0.5,2.0)
        show merchant_cutscene_2:
            ease 4.0 xalign 1.0
        pause
        naomi blush "(He smells like cedarwood...)"
        merchant "Is this... okay?"
        naomi blush "...Yes."
        merchant "Good."
        if merchant_courage > 2:
            merchant "From now on, stay by my side."
            hide merchant_cutscene_2
            $ persistent.merchant_cutscene_2_unlocked = True
            # show bg dancehall 2:
            #     zoom 1.3 xalign 0.5 yalign 0.0 blur 10.0 matrixcolor BrightnessMatrix(-0.1)
            #     ease 3.0 xalign 0.0
            # show merchant happy_suit:
            #     zoom 3.5 yalign 0.15 xalign 0.5 xzoom -1.0 matrixcolor BrightnessMatrix(-0.05)
            # with Fade(2.0,0.5,2.0)
            # merchant "Is this... okay?"
            # naomi blush "...Yes."
            # show bg dancehall 2:
            #     ease 3.0 xalign 0.5 yalign 0.0 blur 10.0
            # show merchant smile_suit:
            #     zoom 3.5 yalign 0.15 xzoom 1.0
            # merchant "Good."
            # show merchant happy_suit:
            #     zoom 3.5 yalign 0.15 xzoom 1.0
            # merchant "From now on, stay by my side."
            image merchant glitched2:
                zoom 3.5 yalign 0.15 xalign 0.5
                glitch("merchant happy_suit")
                pause 0.1
                glitch("merchant happy_suit",offset=60,randomkey=None)
                pause 0.1
                glitch("merchant happy_suit")
                pause 0.1
                "merchant happy_suit"
            stop music
            play sound "<from 4 to 7>ringing.mp3" fadeout 2
            show merchant glitched2
            show bg dancehall 2 as bg_copy at atl_dizzy
            show merchant glitched2
            if persistent.haptics_enabled:
                $ renpy.vibrate(0.5)
            naomi pain "Ngh!" with vpunch
            show bg dancehall 2:
                easeout 0.5 zoom 1.4 xalign 0.5 yalign 0.1 blur 10.0
            show merchant surprised_suit:
                zoom 3.5 yalign 0.15
                easeout 0.5 zoom 4.0 yalign 0.25
            merchant "Naomi!"
            #play music "<from 32>dance.mp3" fadein 1
            merchant "Are you alright?"
            naomi pain "I was dizzy for a moment..."
            show bg dancehall 2:
                easeout 1.0 zoom 1.4 xalign 0.5 yalign 0.0 blur 10.0
            show merchant scowlfront_suit:
                ease 1.0 yalign 0.15
            merchant "I'll take you home."
            naomi troubled "I'm alright-"
            show bg dancehall 2:
                ease 2.0 xalign 0.0 yalign 0.0 blur 10.0
            show merchant scowlside_suit:
                zoom 4.0 yalign 0.15 xzoom -1.0
            merchant "We're leaving now."
            stop music fadeout 3
            hide merchant
            $ merchant_dream = True
        else:
            hide merchant_cutscene_2
            $ persistent.merchant_cutscene_2_unlocked = True
            show bg dancehall 2:
                ease 3.0 xalign 1.0 yalign 0.0
                ease 3.0 xalign 0.5 yalign 0.0
            show merchant happy_suit:
                pause 3.0
                xzoom -1.0
            naomi blush "(If only this moment could last forever!)"
            merchant "You're getting the hang of it."
            naomi blush "..."
            stop music fadeout 3
            merchant "Come on, I'll take you home."

    else:
        show merchant scowlside_suit
        merchant "Anyway, I already spoke to Endo."
        show merchant frown_suit:
            zoom 1.0 xzoom -1.0
        merchant "Let's go."
        hide merchant
    
    # Back home
    hide bg dancehall
    show bg bedroom
    with fade
    show cat neutral with moveinbottom
    if naomi_dress == "dress_flapper":
        if merchant_courage > 2:
            cat "Back so early?"
            naomi troubled "I had a dizzy spell."
            show cat eyeroll
            cat "Huh, again."
            show cat happy
            cat "Sweet dreams."
        else:
            cat "Looks like someone had a good time."
            naomi blush "..."
            cat "Good night."
        hide cat with moveoutbottom
        naomi pain "(As if I'd be able to sleep!)"
        naomi blush "(My heart is still racing...)"
        $ merchant_ending = True
    else:
        cat "Back so early?"
        naomi troubled "We did what we had to."
        cat "Huh."
        show cat huff
        cat "Wear something appropriate next time."
        hide cat with moveoutbottom
        naomi thinking "(Would it have been different?)"
    $ merchant_event = False
    call screen bedroom

label doctor_movie:
    scene bg cafeleft with dissolve
    menu:
        naomi thinking "I need to head to the movie soon."
        "Change clothes":
            naomi thinking "I'll change clothes quickly."
            window hide
            show screen wardrobe
            naomi happy "I'm ready."
        "Head out":
            naomi happy "I'm ready."
    # At movies
    stop music fadeout 3.0
    hide cafetableright
    hide bg caferight
    show bg movie
    with fade
    show doctor indifferent:
        xalign 0.5
    naomi troubled "Sorry, did you wait long?"
    show doctor happyside
    doctor "I just arrived myself."
    if naomi_dress == "dress_prim":
        show doctor blush
        doctor "Oh... What a cute dress."
        naomi blush "Thank you."
    show doctor happyside
    doctor "Shall we?"
    naomi happy "Let's go!"
    scene bg movie theatre with Fade(2.0,0.5,2.0)
    play music "<from 604 to 615>scary.mp3"
    naomi troubled "(This movie is interesting, but...)"
    naomi pain "(The suspense is unbearable!)"
    stop music fadeout 3
    if naomi_dress == "dress_prim":
        window hide
        show doctor_cutscene_2 with Fade(2.0,0.5,2.0)
        play music "<from 630 to 640>scary.mp3"
        pause
        naomi blush "(His hand is so warm...)"
        stop music fadeout 3
        window hide
        hide doctor_cutscene_2
        show bg movie 
        with Fade(2.0,0.5,2.0)
        show doctor concerned:
            xalign 0.5
        doctor "Are you alright?"
        show doctor bummed
        doctor "I should have checked the movie first before inviting you."
        naomi relieved "I'm fine."
        naomi blush "Thanks for holding my hand."
        if doctor_courage > 2:
            show doctor thinking
            doctor "That's not it."
            naomi troubled "?"
            show doctor happyside
            doctor "I didn't hold your hand because you were scared."
            naomi blush "..."
            show doctor happy:
                zoom 1.0 xalign 0.5 yalign 0.0
                ease 2.0 zoom 1.5 yalign 0.1
            doctor "I held your hand because..."
            show doctor happy:
                zoom 1.5 yalign 0.1
            doctor "I just wanted to."
            image doctor glitched2:
                glitch("doctor happy")
                pause 0.1
                glitch("doctor happy",offset=60,randomkey=None)
                pause 0.1
                glitch("doctor happy")
                pause 0.1
                "doctor happy"
            show doctor glitched2:
                zoom 1.5 yalign 0.1
            naomi surprised "('...just wanted to..')"
            show bg movie as bg_copy at atl_dizzy
            show doctor glitched2:
                zoom 1.5 yalign 0.1
            if persistent.haptics_enabled:
                $ renpy.vibrate(0.5)
            naomi pain "Ngh!" with vpunch
            show doctor concerned:
                zoom 1.5 yalign 0.1
                easeout 0.5 zoom 2.0 yalign 0.2
            doctor "Naomi!"
            doctor "Are you alright?"
            naomi troubled "Yes..."
            show doctor concerned:
                ease 1.0 zoom 1.5 yalign 0.15
            doctor "I'll take you home."
        else:
            show doctor happyside
            doctor "If you ever feel scared, I'll be here to hold your hand again."
            naomi blush "Is that a promise?"
            show doctor happy
            doctor "As long as you'll keep me beside you."
            naomi blush "..."
            doctor "Let me walk you home."
        # Back home
        hide bg movie
        show bg bedroom
        with fade
        show cat neutral with moveinbottom
        cat "How was the movie?"
        naomi blush "Interesting."
        show cat huff
        cat "Huh."
        show cat happy
        cat "Good night."
        hide cat with moveoutbottom
        if doctor_courage > 2:
            naomi blush "(...He wanted to hold my hand.)"
            $ doctor_dream = True
        $ doctor_event = False
        $ doctor_ending = True
    else:
        hide window
        show bg movie with Fade(2.0,0.5,2.0)
        show doctor concerned
        doctor "Are you alright?"
        show doctor bummed
        doctor "I should have checked the movie first before inviting you."
        naomi relieved "I'm fine."
        show doctor happyside
        doctor "That's good."
        doctor "Thanks for spending your afternoon with me."
        naomi happy "I had fun too. Thanks for inviting me!"
        doctor "I'll see you around then."
        naomi happy "Yes, see you!"        
        # Back home
        hide bg movie
        show bg bedroom
        with fade
        show cat neutral with moveinbottom
        cat "How was the movie?"
        naomi troubled "Interesting, but a little scary."
        show cat huff
        cat "Huh."
        hide cat with moveoutbottom
        $ doctor_event = False
    if musician_event == 3:
        jump musician_tower
    else:
        scene bg cafeleft with fade
        naomi sleepy "It's been a long day. I'll head to bed."
        jump evening_time



### what we gonna do she cant dream about two guys on the same night