
label cafe_game:
    call screen cafe_game
    
label work_cafe:
    scene bg cafeleft
    play music "<from 1 to 79.5>spring.mp3" loop if_changed
    naomi happy "I'll work a shift at the cafe!"
    
    # $ renpy.random.shuffle(cafe_menu)
    $ cafe_menu = []
    call screen cafe_menu with pushleft

# ============================================
# CAFE VISIT CHECK
# ============================================
label check_cafe_visits:

    python:
        eligible = []
        already_picked = set()
        fixed_chars_today = []
        forced_char = None

        # Check for forced encounter triggers first
        for char, triggers in cafe_encounter_triggers.items():
            if char not in unlocked_chars or visited_today[char]:
                continue
            trigger = triggers.get(encounters[char])
            if trigger:
                item_match = trigger["item"] in cafe_menu
                cond_match = trigger["condition"]() if trigger["condition"] else True
                if item_match and cond_match:
                    forced_char = char
                    break

        if forced_char:
            already_picked.add(forced_char)
            fixed_chars_today.append(forced_char)

        # Pass 1: fixed items (excluding forced)
        for item in cafe_menu:
            mapping = item_to_character.get(item)
            if mapping is None or isinstance(mapping, list):
                continue
            if mapping == "musician" and musician_casual_paused():
                continue
            if mapping in unlocked_chars and not visited_today[mapping] and mapping not in already_picked:
                eligible.append(mapping)
                already_picked.add(mapping)
                fixed_chars_today.append(mapping)

        # Pass 2: randomized items (excluding forced)
        for item in cafe_menu:
            mapping = item_to_character.get(item)
            if mapping is None or not isinstance(mapping, list):
                continue
            candidates = [
                c for c in mapping
                if c in unlocked_chars and not visited_today[c] and c not in already_picked
                and not (c == "musician" and musician_casual_paused())
            ]
            if candidates:
                if renpy.random.random() < CATCHUP_CHANCE:
                    candidates_sorted = sorted(candidates, key=lambda c: total_visits[c])
                else:
                    candidates_sorted = sorted(candidates, key=lambda c: encounters[c], reverse=True)
                chosen = candidates_sorted[0]
                eligible.append(chosen)
                already_picked.add(chosen)

        # Slot selection
        visiting_chars = []
        if forced_char:
            visiting_chars.append(forced_char)
            if eligible:
                renpy.random.shuffle(eligible)
                visiting_chars.append(eligible[0])
        elif eligible:
            renpy.random.shuffle(eligible)
            pool = fixed_chars_today if fixed_chars_today else eligible
            if renpy.random.random() < CATCHUP_CHANCE:
                visiting_chars.append(sorted(pool, key=lambda c: total_visits[c])[0])
            else:
                visiting_chars.append(sorted(pool, key=lambda c: encounters[c], reverse=True)[0])
            remaining = [c for c in eligible if c not in visiting_chars]
            if remaining:
                visiting_chars.append(renpy.random.choice(remaining))

    # ---- Slot 1 ----
    if len(visiting_chars) >= 1:
        $ char1 = visiting_chars[0]
        $ visited_today[char1] = True
        $ total_visits[char1] += 1

        python:
            override1 = None
            num1 = encounters[char1]
            trigger = cafe_encounter_triggers.get(char1, {}).get(num1)
            if trigger:
                item_match = trigger["item"] in cafe_menu
                cond_match = trigger["condition"]() if trigger["condition"] else True
                if item_match and cond_match:
                    override1 = char1 + "_" + str(num1)

        if override1:
            $ encounters[char1] += 1
            call expression override1
        else:
            call expression "casual_" + char1

    # ---- Slot 2 (skipped if slot 1 was a story encounter) ----
    if len(visiting_chars) >= 2 and not override1:
        $ char2 = visiting_chars[1]
        $ visited_today[char2] = True
        $ total_visits[char2] += 1

        python:
            override2 = None
            num2 = encounters[char2]
            trigger = cafe_encounter_triggers.get(char2, {}).get(num2)
            if trigger:
                item_match = trigger["item"] in cafe_menu
                cond_match = trigger["condition"]() if trigger["condition"] else True
                if item_match and cond_match:
                    override2 = char2 + "_" + str(num2)

        if override2:
            $ encounters[char2] += 1
            call expression override2
        else:
            call expression "casual_" + char2

    return

label after_work_cafe:
    scene bg caferight
    # Recreate ending scene
    image order0 = "images/cafe/[cafe_menu[0]].png"
    show order0:
        xalign 0.22 yalign 0.55 xzoom 0.1 yzoom 0.1
    image order1 = "images/cafe/[cafe_menu[1]].png"
    show order1:
        xalign 0.5 yalign 0.55 xzoom 0.1 yzoom 0.1
    image order2 = "images/cafe/[cafe_menu[2]].png"
    show order2:
        xalign 0.8 yalign 0.55 xzoom 0.1 yzoom 0.1
        
    call check_cafe_visits

    show cafetableright zorder 3.0
    show kirako happy with dissolve
    kirako "Thank you for your help Naomi!"
    $ tips = renpy.random.randint(10, 15)
    $ money += tips
    kirako "Here you go, [tips] yen in tips today."

    # Deduct timeslot and check if morning or afternoon
    $ timeslot -= 1
    if dayofweeknumber > 5:
        return
    else:
        if timeslot == 1:
            naomi happy "Thank you!"
            hide kirako with moveoutleft
            scene bg cafeleft with pushright
            menu:
                naomi thinking "What should I do this afternoon?"
                "Work in cafe":
                    jump work_cafe
                "Go out":
                    stop music fadeout 3
                    jump asakusa_small
        if timeslot < 1:
            kirako "Have a good rest, dear."
            naomi happy "You too, good night!"
            stop music fadeout 3
            jump evening_time


# ============================================
# CASUAL VISITS
# ============================================

label casual_musician:    
    show cafetableright zorder 3.0
    if encounters["musician"] == 2:
        call musician_2
    else:
        if 4 <= encounters["musician"] <= 6:
            show fans_less with dissolve
        show musician shy with dissolve:
            xalign 0.5
        naomi happy "Craving something sweet today?"
        show musician shy2
        musician "Yeah, pudding please."
        naomi happy "Coming right up!"
        window hide
        show pudding zorder 3.0:
            xalign 0.5 ypos 0.9 zpos 400 zoom 0.5
            easein 1.0 ypos 0.7 zpos 0
        pause
        naomi relieved "Here you go!"
        show musician happy
        musician "Thanks."
    if 4 <= encounters["musician"] <= 6:
        customer "Pudding, please!"
        naomi happy "Right up!"
        show musician shy
        musician "There's been more customers lately."
        naomi smirk "Yeah, the pudding's been selling out lately."
        show musician thinking
        musician "Selling out?"
        naomi smirk "Don't worry, we keep one just for you."
        show musician happy
        musician "Thanks."
    if encounters["musician"] == 9:
        naomi troubled "How was rehearsal today?"
        show musician shy
        musician "...Fine."
        naomi troubled "..."
        show musician shy2
        musician "It really was. I've been..."
        show musician shy
        musician "Back to my usual."
        naomi relieved "Alright."
        show musician happy
        musician "...Thanks for asking."
    if encounters["musician"] == 10:
        show musician shy2
        musician "...I'll be at the theatre then."
        naomi happy "See you there!"
    if encounters["musician"] == 11:
        naomi happy "How's the song coming along?"
        show musician thinking
        musician "...It's coming along."
        naomi happy "Coming along, huh."
        show musician happy
        musician "I'll keep working at it."
        naomi happy "I'm waiting."
    hide musician
    hide pudding
    hide fans_less
    with dissolve
    return

label casual_doctor:
    "Dr. Yumoto drops in on his way from the hospital."
    return

label casual_merchant:
    "Yujiro happened to be in the area."
    return


# label musician_1:
#     show cafetableright zorder 3.0
#     show musician shy with moveinleft:
#         xalign 0.5
#     $ musician_name = "???"
#     musician "..."
#     naomi surprised "(He's carrying a shamisen?)"
#     naomi troubled "(He looks unfriendly...)"
#     naomi troubled "What would you like to have?"
#     show musician shy2
#     musician "...Pudding, please."
#     naomi relieved "One Pudding à la Mode. Please wait a moment."
#     window hide
#     show musician shy
#     image pudding = "images/cafe/Pudding.png"
#     show pudding zorder 3.0:
#         xalign 0.5 ypos 0.9 zpos 400 zoom 0.5
#         easein 1.0 ypos 0.7 zpos 0
#         linear 0.1 xzoom 1.0 yzoom 0.9 ypos 0.7
#         linear 0.1 xzoom 1.0 yzoom 1.0 ypos 0.7
#     pause
#     hide pudding
#     image pudding_no = "images/cafe/pudding_no.png"
#     image pudding_cherry = "images/cafe/pudding_cherry.png"
#     show pudding_no zorder 3.0:
#         xalign 0.5 ypos 0.7 zoom 0.5
#     show pudding_cherry zorder 4.0:
#         xalign 0.46 ypos 0.75 zoom 0.5
#         easeout_circ 0.8 align (0.4, 0.85) knot (0.41, 0.83) zpos 150 zoom 0.6
#         ease 0.6 align (0.35, 0.85) knot (0.37, 0.82)
#     show musician shy2
#     pause
#     naomi surprised "..."
#     musician "..."
#     naomi blush "I'm so sorry!"
#     show musician happy
#     musician "...It's alright."
#     naomi troubled "But..."
#     show musician happy
#     musician "It's alright, everyone makes mistakes starting out."
#     image musician glitched:
#         glitch("musician happy")
#         pause 0.1
#         glitch("musician happy",offset=60,randomkey=None)
#         pause 0.1
#         glitch("musician happy")
#         pause 0.1
#         "musician happy"
#     show musician glitched
#     naomi relieved "(He's nicer than I thought.)"
#     show musician thinking
#     musician "You're new here, right?"
#     naomi blush "Uh, yes..."
#     naomi surprised "How did you know?"
#     show musician shy
#     musician "...I come here often."
#     naomi blush "(Of course he does! Why did I even ask him?)"
#     show musician shy2
#     musician "...deo"
#     naomi thinking "Mm?"
#     show musician shy
#     musician "...Hideo."
#     naomi thinking "Hideo?"
#     naomi surprised "Ah!"
#     naomi relieved "I'm Naomi."
#     naomi happy "It's nice to meet you."
#     $ musician_name = "Hideo"
#     show musician thinking
#     musician "You..."
#     show musician shy
#     musician "You have a lovely name."
#     naomi blush "Thank you..."
#     naomi troubled "Umm.. If it's not too much trouble to ask..."
#     show musician shy
#     naomi troubled "I actually came to the city to look for a job."
#     naomi relieved "If you know somewhere that is hiring, please let me know!"
#     show musician shy2
#     musician "Hmm..."
#     show musician thinking
#     musician "The Imperial Theatre might need ticketing staff."
#     musician "Perhaps I could introduce you to the theatre manager."
#     naomi surprised "Really? That would be helpful!"
#     show musician shy
#     musician "I'm there on weekdays."
#     show musician shy2
#     musician "You can come by anytime."
#     naomi happy "Thank you Hideo, I'll meet you there!"
#     show musician happy
#     musician "See you."
#     $ unlock_imp_th = True
#     $ encounters["musician"] += 1
#     hide musician
#     hide pudding
#     with moveoutleft
#     return



label doctor_0:
    show cafetableright zorder 3.0
    show cat neutral zorder 4.0 with moveinright:
        xpos 1.0
    $ doctor_name = "???"
    show doctor indifferent with moveinleft:
        xalign 0.5 xzoom -1.0
    image doctor glitched:
        glitch("doctor happyside")
        pause 0.1
        glitch("doctor happyside",offset=60,randomkey=None)
        pause 0.1
        glitch("doctor happyside")
        pause 0.1
        "doctor happyside"
    show doctor glitched:
        xzoom -1.0
    doctor "Maachan."
    show cat scared:
        xpos 1.0 zoom 0.7 ypos 0.1
    play sound "<from 1 to 2>cat_yowl.mp3"
    cat "Mew!"
    show cat scared:
        xpos 1.0
        easein 0.5 xpos 2.5 ypos 0.5 zoom 2.5 blur 10.0
    show doctor bummed
    doctor "..."
    hide cat
    show bg caferight as bg_copy at atl_dizzy
    if persistent.haptics_enabled:
        $ renpy.vibrate(0.5)
    naomi pain "Unngh!" with vpunch
    show doctor concerned
    doctor "Are you alright?"
    naomi pain "...I felt dizzy suddenly."
    naomi relieved "But I'm fine now."
    show doctor concerned:
        zoom 1.0
        ease 1.5 yalign 0.3 zoom 2.0
    doctor "You look a little pale."
    naomi blush "I feel fine!"
    show doctor concerned:
        zoom 2.0 yalign 0.3
        ease 1.5 yalign 0 zoom 1.0
    doctor "You look flushed. Are you feverish?"
    naomi blush "..."
    show doctor thinking:
        zoom 1.0 xzoom 1.0
    doctor "Please come by the hospital for a check-up."
    naomi surprised "Hospital?"
    show doctor concerned
    doctor "Yes. Near Ginza."
    show doctor indifferent
    doctor "Just tell the nurse you're here to see Dr Yumoto."
    naomi blush "...Dr Yumoto."
    $ doctor_name = "Dr Yumoto"
    naomi happy "Are you a regular customer?"
    naomi thinking "You knew Maachan..."
    show doctor happyside
    doctor "Yes, I come here often."
    show doctor bummed
    doctor "But I've yet to befriend Maachan..."
    show doctor concerned
    doctor "Are you new here?"
    naomi happy "Yes."
    naomi blush "Please be patient with me."
    show doctor happy
    doctor "Likewise."
    naomi surprised "Oh!"
    naomi troubled "I completely forgot to take your order."
    show doctor blush
    doctor "I forgot, too."
    show doctor happyside
    doctor "I'll have a cake, please."
    naomi blush "Right away."
    window hide
    image cake = "images/cafe/Cake.png"
    show cake zorder 3.0:
        xalign 0.5 ypos 0.9 zpos 400 zoom 0.5
        easein 1.0 ypos 0.7 zpos 0
    pause
    doctor "Thank you."
    show doctor happy
    doctor "Remember to come by the hospital after your shift."
    show doctor happyside
    naomi happy "Thank you!"
    $ unlock_hosp = True
    $ encounters["doctor"] += 1
    hide doctor
    hide cake
    with moveoutleft
    naomi blush "I do feel a little warm, now."
    naomi troubled "That dizzy spell came out of nowhere, too."
    naomi thinking "I should pay him a visit."
    return

# Courage +1 if chose to confront over incident
label merchant_1:
    show cafetableright zorder 3.0
    $ guy_display = True
    $ encounters["merchant"] += 1
    if merchant_choice == 0:        
        show merchant frownside with dissolve:
            xalign 0.5
        merchant "A coffee please."
        naomi happy "One coffee. Please wait a mo-"
        naomi angry "(It's the department store guy!)"
        show merchant frown
        menu:
            merchant "...Something the matter?"
            "It's nothing":
                naomi thinking "It's nothing, please excuse me."
                merchant "Hm."
                naomi troubled "Here's your coffee."
                window hide
                image coffee = "images/cafe/Coffee.png"
                show coffee zorder 3.0:
                    xalign 0.5 ypos 0.9 zpos 400 zoom 0.5
                    easein 1.0 ypos 0.7 zpos 0
                pause
                show kirako happy with moveinleft:
                    xalign 0.2
                show merchant surprised:
                    xalign 0.5 zoom 1.0
                    easein 0.5 xalign 0.8 zoom 1.0
                kirako "Yujiro, darling! How's your father doing?"
                show merchant frownside
                merchant "He's fine."
                kirako "Naomi, this is Yujiro. His father runs the department store down at Ginza."
                show kirako pout
                show merchant frown
                kirako "Yujiro dear, Naomi here is looking for work in the city."
                show kirako happy
                kirako "Be a dear and give her something to do, won't you?"
                show kirako pout
                kirako "Ah, is that the kettle boiling?"
                hide kirako with moveoutleft
                $ merchant_name = "Yujiro"
                show merchant frown:
                    zoom 1.0
                    easein 1.0 xalign 0.5
                merchant "..."
                show merchant frown
                merchant "Here."
                window hide
                show merchant_namecard zorder 3.0:
                    xalign 0.5 yalign 0.5 zpos 0 zoom 0.2
                    easein 1.0 yalign 0.6 zpos 800
                pause
                show merchant_namecard_front zorder 3.0:
                    xalign 0.5 yalign 0.5
                pause
                hide merchant_namecard_front
                hide merchant_namecard with moveoutbottom
                show merchant frownside
                merchant "Come by my office if you need work."
                hide merchant_namecard with moveoutbottom
                $ inventory.update({"namecard":["Fujiya Yujiro's namecard."]})
                show merchant frownside:
                    xzoom -1.0 zoom 1.0
                merchant "Can't promise I'll hire you, though."
                show merchant frown
                naomi thinking "(Would I want to work for this guy?)"
                naomi troubled "(Guess I could check it out first.)"
                naomi troubled "Thank you."
                hide merchant with moveoutleft
                $ guy_display = False
            "Actually...":
                naomi troubled "Actually... I saw you talking to your staff at the department store."
                show merchant surprised
                naomi troubled "I couldn't help but think you were being pretty harsh to her..."
                show merchant thinkingside
                merchant "That incident."
                show merchant resigned
                merchant "I told her before not to carry too many things down the stairs!"
                show merchant scowlside
                merchant "She could have tripped and injured herself!"
                naomi surprised "(So he was worried for her!)"
                naomi thinking "Still, did you really need to make her cry?"
                show merchant surprised
                merchant "..."
                $ merchant_courage += 1
                show merchant thinkingside
                merchant "You're right, I could have handled it better."
                show merchant thinking
                merchant "..."
                show merchant resigned
                merchant "I will talk to her about it."
                naomi happy "Glad to hear that!"
                show merchant thinkingside
                merchant "Hm."
                show merchant thinking
                merchant "What's your name?"
                naomi surprised "Eh? Uh... Naomi?"
                show merchant frown
                merchant "Here."
                window hide
                show merchant_namecard zorder 3.0:
                    xalign 0.5 yalign 0.5 zpos 0 zoom 0.2
                    easein 1.0 yalign 0.6 zpos 800
                pause
                show merchant_namecard_front zorder 3.0:
                    xalign 0.5 yalign 0.5
                pause
                hide merchant_namecard_front
                naomi blush "Mr Fujiya Yujiro..."
                hide merchant_namecard with moveoutbottom
                $ inventory.update({"namecard":["Fujiya Yujiro's namecard."]})
                $ merchant_name = "Yujiro"
                show merchant frown
                merchant "Just Yujiro will do."
                merchant "Come to my office."
                naomi surprised "Huh?"
                show merchant thinkingside
                merchant "You came from the countryside to find a job, didn't you?"
                naomi surprised "How did you know?"
                show merchant thinking
                merchant "It's not difficult to guess."
                show merchant happy
                merchant "You'll earn more working for me."
                merchant "I'll be expecting you."
                show merchant frownside:
                    xzoom -1.0 zoom 1.0
                hide merchant with moveoutleft
                $ guy_display = False
                naomi thinking "(What was that about?)"
                naomi surprised "Oh no, his coffee!"
                show kirako happy with moveinleft
                kirako "Was that Yujiro?"
                naomi surprised "You know him?"
                kirako "Oh yes, his father runs the department store at Ginza."
                show kirako pout
                kirako "If he hadn't rushed off, I could have introduced you!"
                naomi sleepy "It's fine, really."
                naomi thinking "(I guess I can visit his office and see how it goes...)"
    elif merchant_choice == 1:
        show merchant frown with dissolve:
            xalign 0.5
        merchant "A coffee please."
        show merchant frownside
        naomi happy "One coffee. Please wait a mo-"
        show merchant frown
        naomi angry "You're the department store guy!"
        show merchant thinking
        merchant "Oh it's you. The meddlesome girl."
        naomi troubled "Sorry, I shouldn't have jumped to conclusions back there."
        show merchant thinkingside
        merchant "..."
        $ merchant_courage += 1
        show merchant frownside
        merchant "No, you were right. I shouldn't have lashed out at my staff."
        show merchant frownside
        naomi troubled "..."
        show merchant frown
        naomi troubled "What was that all about, anyway?"
        show merchant resigned
        merchant "She was carrying too many things down the stairs." 
        show merchant scowlside
        merchant "She could have tripped and injured herself!"
        naomi surprised "(So he was worried for her!)"
        naomi troubled "Still, you didn't need to be so harsh."
        show merchant frown
        merchant "..."
        show merchant resigned
        merchant "I had apologised to her for my conduct."
        show merchant scowlside
        merchant "Consider your meddling appreciated."
        show merchant frownside
        naomi thinking "(...is that his way of saying thanks?)"
        show merchant frown
        merchant "Hm."
        show merchant thinking
        merchant "What's your name?"
        naomi troubled "Eh? Uh... Naomi?"
        show merchant frownside
        merchant "Here."
        window hide
        show merchant_namecard zorder 3.0:
            xalign 0.5 yalign 0.5 zpos 0 zoom 0.2
            easein 1.0 yalign 0.6 zpos 800
        pause
        show merchant_namecard_front zorder 3.0:
            xalign 0.5 yalign 0.5
        pause
        hide merchant_namecard_front
        naomi blush "Mr Fujiya Yujiro..."
        hide merchant_namecard with moveoutbottom
        $ inventory.update({"namecard":["Fujiya Yujiro's namecard."]})
        $ merchant_name = "Yujiro"
        show merchant frown
        merchant "Just Yujiro will do."
        merchant "Come to my office."
        naomi surprised "Huh?"
        show merchant thinkingside
        merchant "You came from the countryside to find a job, didn't you?"
        naomi surprised "How did you know?"
        show merchant thinking
        merchant "It's not difficult to guess."
        show merchant frownside
        merchant "Well, you'll earn more working for me."
        show merchant frown
        merchant "I'll be expecting you."
        show merchant frownside:
            xzoom -1.0 zoom 1.0
        hide merchant with moveoutleft
        $ guy_display = False
        naomi troubled "(What was that about?)"
        naomi surprised "Oh no, his coffee!"
        show kirako happy with moveinleft
        kirako "Was that Yujiro?"
        naomi surprised "You know him?"
        kirako "Oh yes, his father runs the department store at Ginza."
        show kirako pout
        kirako "If he hadn't rushed off, I could have introduced you!"
        naomi sleepy "It's fine, really."
        naomi thinking "(I guess I can visit his office and find out more...)"
    $ unlock_off_bldg = True
    return

label soldier_2:
    show cafetableright zorder 3.0
    show soldier happy with moveinleft
    pause
    hide soldier
    with moveoutleft
    return

label fighter_2:
    show cafetableright zorder 3.0
    $ fighter_name = "???"
    $ guy_display = True
    show fighter angry with moveinleft:
        xalign 0.5
    fighter "That bastard! I shall beat him once I've had my katsudon!"
    naomi surprised "!!!"
    naomi happy "You're the guy from the shrine!"
    show fighter surprised
    fighter "!!!"
    show fighter grin
    fighter "I knew we'd meet again."
    show fighter determined
    naomi blush "..."
    # naomi blush "Anyway..."
    # naomi thinking "...Beat him?"
    # show fighter angry
    # fighter "Some arrogant bastard challenged my dojo while I was out."
    # show fighter determined
    # fighter "I'm going to his dojo to show him his place!"
    # naomi troubled "I see..."
    # menu:
    #     "Treat him (5 yen)" if money >= 5:
    #         $ money -= 5
    #         naomi happy "Katsudon on the house, just for you."
    #         naomi happy "For luck!"
    #         show fighter surprised
    #         fighter "Really?"
    #         show fighter blush
    #         if "omikuji_daikichi_half" in inventory:
    #             $ fighter_affection += 2
    #         elif "omikuji_daikichi" in inventory:
    #             $ fighter_affection += 1
    #         pause
    #         show fighter determined
    #         fighter "Great! I'm gonna beat that guy this time for sure!"
    #     "Banter back":
    #         naomi happy "Indeed the good fortune came true."
    #         naomi happy "So, one katsudon for you?"
    #         show fighter grin
    #         fighter "Yes!"
    #         show fighter determined
    #         fighter "I shall defeat that guy today!"
    naomi happy "Here is your katsudon!"
    window hide
    image katsudon = "images/cafe/Katsudon.png"
    show katsudon zorder 3.0:
        xalign 0.5 ypos 0.9 zpos 400 zoom 0.5
        easein 1.0 ypos 0.7 zpos 0
    pause
    $ unlock_dojo = True
    $ guy_display = False
    hide fighter
    with moveoutleft
    return

