label office_bldg:
    
    scene bg office:
        xalign 0.8 yalign 0.0
    
    if merchant_ending == True:
        if merchant_courage > 2:
            jump merchant_final_irl
        else:
            jump merchant_final_not
    if totaldays == 0:
        jump office_ending

    if encounters["merchant"] == 2:
        call merchant_3
    elif merchant_job == 2:
        call merchant_4
    elif merchant_job == 4 and enable_merchant_event_1 == True:
        call merchant_6
    else:
        show merchant scowlfront:
            xalign 0.5 yalign 0.0
        merchant "Here, work on this."
        show paperstack:
            xpos 0.4 ypos 0.5 zpos 0 zoom 0.5
            easein 1.0 xpos 0.4 ypos 0.55 zpos 800
        show merchant frownside
        merchant "I'll come back later."
        hide merchant with moveoutright

    show time:
        xalign 0.5 yalign 0.5
        ease 1.0 rotate 45
        ease 1.0 rotate -45
        ease 1.0 rotate 0
    naomi thinking "..."
    hide time
    hide paperstack
    $ timeslot -= 1
    naomi sleepy "I'm finally done."
    if merchant_job == 3 and totaldays > 6:
        $ enable_merchant_event_1 = True
        jump merchant_5
    show merchant frownside:
        xalign 0.5 yalign 0.0
    with moveinleft
    merchant "Done?"
    naomi relieved "Yes! Here you go."
    show paperstack:
        xpos 0.3 ypos 0.55 zpos 800
        easein 1.0 xpos 0.4 ypos 0.6 zpos 0 zoom 0.5
    $ salary = renpy.random.randint(20, 25)
    $ money += salary
    show merchant frown
    merchant "Thanks. Here's [salary] yen for today's work."
    naomi happy "Thanks!"
    if merchant_job == 7 and totaldays > 2:
        call merchant_7
    $ merchant_job += 1
    if timeslot == 1:
        menu:
            merchant "Do you want to work the afternoon too?"
            "Work the afternoon":
                naomi happy "Sure, I'll stay for the afternoon."
                jump office_bldg
            "Go out":
                naomi relieved "No, I'll head off now."
                merchant "Bye."
                jump ginza_small
    if timeslot < 1:
        naomi relieved "I'll head home now."
        merchant "Bye."
        jump evening_time

label merchant_0:
    $ encounters["merchant"] += 1
    $ unlocked_chars.append("merchant")
    scene bg dept:
        xalign 0.5 yalign 0.6 zoom 1.5
    $ dept_name = "Staff"
    $ merchant_name = "???"
    show merchant scowlside:
        xalign 0.55 yalign 1.0 zoom 0.5
    show staff cry:
        xalign 0.75 yalign 1.1 zoom 0.5
    merchant "Make sure this doesn't happen again!"
    show merchant frownside:
        xalign 0.55 yalign 1.0 zoom 0.5
    staff "I understand, sir. I apologise for troubling you."
    show merchant scowlside:
        xalign 0.55 yalign 1.0 zoom 0.5
    merchant "You- (inaudible)"
    show merchant frownside:
        xalign 0.55 yalign 1.0 zoom 0.5
    staff "*sniff* I- (inaudible)"
    naomi troubled "He's making her cry..."
    menu:
        "Intervene":
            show bg dept:
                xalign 0.5 yalign 0.6 zoom 1.5 
                easein 2.0 xalign 0.6 yalign 0.75 zoom 3.0
            show merchant scowlside:
                xalign 0.55 yalign 1.0 zoom 0.5
                easein 2.0 xalign 0.30 zoom 1.0 ypos 1.1
            show staff cry:
                xalign 0.75 yalign 1.1 zoom 0.5
                easein 2.0 xalign 0.8 ypos 1.3 zoom 1.0
            pause
            $ merchant_choice += 1
            naomi angry "Mister, please stop. You're making her cry."
            show merchant surprised:
                xalign 0.30 zoom 1.0 ypos 1.1
            merchant "..."
            show staff happy:
                xalign 0.8 ypos 1.3
            staff "Don't worry about me, miss."
            naomi angry "Just because you're a customer doesn't give you the right to treat her like this!"
            show merchant resigned:
                xalign 0.30 zoom 1.0 ypos 1.1
            merchant "..."
            show staff cry:
                xalign 0.8 ypos 1.3
            staff "I'm afraid there's a misunderstanding, miss."
            naomi thinking "You should be ashamed of yourself!"
            show merchant scowlside:
                xalign 0.30 zoom 1.0 ypos 1.1
            merchant "...We'll discuss this later."
            show merchant frownside:
                xzoom -1.0
                easeout 3.0 xpos -1.0 ypos 2.0 zoom 3.0 blur 5.0
            staff "Director!"
            $ merchant_name = "Director"
            naomi surprised "(Director?)"
            show staff happy:
                easein 1.0 xalign 0.5 zoom 1.0
            staff "Thank you for your concern, miss."
            staff "Our director is stern, but he means well."
            naomi angry "If he means well, he shouldn't be so harsh!"
            show staff cry:
                xalign 0.5 zoom 1.0
            staff "It was my fault for making him worry." 
            staff "I hope you will forgive him."
            naomi troubled "..."
            show staff happy:
                xalign 0.5 zoom 1.0
            staff "I appreciate your kindness in speaking up for me."
            staff "Please enjoy the rest of your visit."
            show staff happy:
                xzoom -1.0
            # show dept_clothes:
            #     xalign 1.785 ypos 0.098 zoom 1.0 alpha 0.75
            staff "Now if you would excuse me..."
            hide staff with moveoutright
            naomi thinking "(I guess it was the right thing to do? Oh well.)"
            hide staff
            # hide dept_clothes
            hide naomi
            show bg dept:
                easein 2.0 xalign 0.5 yalign 0.5 zoom 1.0
            pause
            jump dept_only
        "Observe":
            staff "I'm sorry I made you worry, director."
            $ merchant_name = "Director"
            show merchant resigned:
                xalign 0.55 yalign 1.0 zoom 0.5
            merchant "...Be more careful next time."
            show staff cry:
                xalign 0.75 yalign 1.1 zoom 0.5
                xzoom -1.0
                easeout 5.0 xpos 2.0
            show merchant frownside zorder 2.0:
                xalign 0.55 yalign 1.0 zoom 0.5
                xzoom -1.0
                easeout 5.0 xpos -0.8 ypos 2.0 zoom 3.0 blur 5.0
            show dept_clothes:
                xalign 1.4 yalign 2.0 zoom 0.755 alpha 0.75
            pause
            naomi surprised "(I thought he was a customer.)"
            naomi thinking "(Still, he shouldn't be so harsh with his staff...)"
            window hide
            hide dept_clothes
            hide merchant
            hide staff
            show bg dept:
                easein 2.0 xalign 0.5 yalign 0.5 zoom 1.0
            pause
            jump dept_only

label merchant_1:
    show cafetableright zorder 3.0
    $ guy_display = True
    $ encounters["merchant"] += 1
    show merchant frownside with dissolve:
        xalign 0.5
    merchant "Hm, same menu."
    naomi thinking "(Same..?)"
    show merchant scowlside
    merchant "A coffee please."
    naomi happy "One coffee. Please wait a mo-"
    if merchant_choice == 0:
        naomi angry "(It's the department store guy!)"
        show merchant frown
        menu:
            merchant "...Something the matter?"
            "It's nothing":
                naomi thinking "It's nothing, please excuse me."
                merchant "Hm."
                naomi troubled "Here's your coffee."
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
                $ add_point("merchant")
                show merchant thinkingside
                merchant "I could have handled it better."
                show merchant thinking
                merchant "..."
                show merchant resigned
                merchant "I will talk to her about it."
                naomi happy "Glad to hear that!"
                show merchant thinkingside
                merchant "Hm."
                naomi happy "Here's your coffee."
    elif merchant_choice == 1:
        merchant "Oh it's you. The meddlesome girl."
        naomi troubled "Sorry, I shouldn't have jumped to conclusions back there."
        show merchant thinkingside
        merchant "..."
        $ add_point("merchant")
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
        naomi happy "Here's your coffee."
    window hide
    image coffee = "images/cafe/Coffee.png"
    show coffee zorder 3.0:
        xalign 0.5 ypos 0.9 zpos 400 zoom 0.5
        easein 1.0 ypos 0.7 zpos 0
    pause
    merchant "Hm. Tastes the same too."
    naomi angry "What do you mean?"
    show merchant surprised
    naomi surprised "(Oops, I said that out loud.)"
    show merchant frownside
    merchant "..."
    show merchant scowlside
    merchant "Coffee, tea, a few cakes. Every cafe on this street has the same menu."
    show merchant resigned
    merchant "All vying for the same customers too."
    naomi troubled "..."
    naomi thinking "Same could be said of department stores too."
    show merchant surprised
    merchant "What do you mean?"
    naomi troubled "..."
    naomi troubled "It's just shopping. There isn't much else to stay for."
    show merchant frownside
    merchant "Hm."
    show merchant frown
    merchant "Thanks for the coffee."
    hide merchant with dissolve
    naomi troubled "Was I rude?"
    naomi angry "But he was rude first."
    naomi thinking "He wasn't wrong, though."
    naomi troubled "This cafe needs something different to stand out."
    return

# # Courage +1 if chose to confront over incident
# label merchant_1:
#     show cafetableright zorder 3.0
#     $ guy_display = True
#     $ encounters["merchant"] += 1
#     if merchant_choice == 0:        
#         show merchant frownside with dissolve:
#             xalign 0.5
#         merchant "A coffee please."
#         naomi happy "One coffee. Please wait a mo-"
#         naomi angry "(It's the department store guy!)"
#         show merchant frown
#         menu:
#             merchant "...Something the matter?"
#             "It's nothing":
#                 naomi thinking "It's nothing, please excuse me."
#                 merchant "Hm."
#                 naomi troubled "Here's your coffee."
#                 window hide
#                 image coffee = "images/cafe/Coffee.png"
#                 show coffee zorder 3.0:
#                     xalign 0.5 ypos 0.9 zpos 400 zoom 0.5
#                     easein 1.0 ypos 0.7 zpos 0
#                 pause
#                 show kirako happy with moveinleft:
#                     xalign 0.2
#                 show merchant surprised:
#                     xalign 0.5 zoom 1.0
#                     easein 0.5 xalign 0.8 zoom 1.0
#                 kirako "Yujiro, darling! How's your father doing?"
#                 show merchant frownside
#                 merchant "He's fine."
#                 kirako "Naomi, this is Yujiro. His father runs the department store down at Ginza."
#                 show kirako pout
#                 show merchant frown
#                 kirako "Yujiro dear, Naomi here is looking for work in the city."
#                 show kirako happy
#                 kirako "Be a dear and give her something to do, won't you?"
#                 show kirako pout
#                 kirako "Ah, is that the kettle boiling?"
#                 hide kirako with moveoutleft
#                 $ merchant_name = "Yujiro"
#                 show merchant frown:
#                     zoom 1.0
#                     easein 1.0 xalign 0.5
#                 merchant "..."
#                 show merchant frown
#                 merchant "Here."
#                 window hide
#                 show merchant_namecard zorder 3.0:
#                     xalign 0.5 yalign 0.5 zpos 0 zoom 0.2
#                     easein 1.0 yalign 0.6 zpos 800
#                 pause
#                 show merchant_namecard_front zorder 3.0:
#                     xalign 0.5 yalign 0.5
#                 pause
#                 hide merchant_namecard_front
#                 hide merchant_namecard with moveoutbottom
#                 show merchant frownside
#                 merchant "Come by my office if you need work."
#                 hide merchant_namecard with moveoutbottom
#                 $ inventory.update({"namecard":["Fujiya Yujiro's namecard."]})
#                 show merchant frownside:
#                     xzoom -1.0 zoom 1.0
#                 merchant "Can't promise I'll hire you, though."
#                 show merchant frown
#                 naomi thinking "(Would I want to work for this guy?)"
#                 naomi troubled "(Guess I could check it out first.)"
#                 naomi troubled "Thank you."
#                 hide merchant with moveoutleft
#                 $ guy_display = False
#             "Actually...":
#                 naomi troubled "Actually... I saw you talking to your staff at the department store."
#                 show merchant surprised
#                 naomi troubled "I couldn't help but think you were being pretty harsh to her..."
#                 show merchant thinkingside
#                 merchant "That incident."
#                 show merchant resigned
#                 merchant "I told her before not to carry too many things down the stairs!"
#                 show merchant scowlside
#                 merchant "She could have tripped and injured herself!"
#                 naomi surprised "(So he was worried for her!)"
#                 naomi thinking "Still, did you really need to make her cry?"
#                 show merchant surprised
#                 merchant "..."
#                 $ merchant_courage += 1
#                 show merchant thinkingside
#                 merchant "You're right, I could have handled it better."
#                 show merchant thinking
#                 merchant "..."
#                 show merchant resigned
#                 merchant "I will talk to her about it."
#                 naomi happy "Glad to hear that!"
#                 show merchant thinkingside
#                 merchant "Hm."
#                 show merchant thinking
#                 merchant "What's your name?"
#                 naomi surprised "Eh? Uh... Naomi?"
#                 show merchant frown
#                 merchant "Here."
#                 window hide
#                 show merchant_namecard zorder 3.0:
#                     xalign 0.5 yalign 0.5 zpos 0 zoom 0.2
#                     easein 1.0 yalign 0.6 zpos 800
#                 pause
#                 show merchant_namecard_front zorder 3.0:
#                     xalign 0.5 yalign 0.5
#                 pause
#                 hide merchant_namecard_front
#                 naomi blush "Mr Fujiya Yujiro..."
#                 hide merchant_namecard with moveoutbottom
#                 $ inventory.update({"namecard":["Fujiya Yujiro's namecard."]})
#                 $ merchant_name = "Yujiro"
#                 show merchant frown
#                 merchant "Just Yujiro will do."
#                 merchant "Come to my office."
#                 naomi surprised "Huh?"
#                 show merchant thinkingside
#                 merchant "You came from the countryside to find a job, didn't you?"
#                 naomi surprised "How did you know?"
#                 show merchant thinking
#                 merchant "It's not difficult to guess."
#                 show merchant happy
#                 merchant "You'll earn more working for me."
#                 merchant "I'll be expecting you."
#                 show merchant frownside:
#                     xzoom -1.0 zoom 1.0
#                 hide merchant with moveoutleft
#                 $ guy_display = False
#                 naomi thinking "(What was that about?)"
#                 naomi surprised "Oh no, his coffee!"
#                 show kirako happy with moveinleft
#                 kirako "Was that Yujiro?"
#                 naomi surprised "You know him?"
#                 kirako "Oh yes, his father runs the department store at Ginza."
#                 show kirako pout
#                 kirako "If he hadn't rushed off, I could have introduced you!"
#                 naomi sleepy "It's fine, really."
#                 naomi thinking "(I guess I can visit his office and see how it goes...)"
#     elif merchant_choice == 1:
#         show merchant frown with dissolve:
#             xalign 0.5
#         merchant "A coffee please."
#         show merchant frownside
#         naomi happy "One coffee. Please wait a mo-"
#         show merchant frown
#         naomi angry "You're the department store guy!"
#         show merchant thinking
#         merchant "Oh it's you. The meddlesome girl."
#         naomi troubled "Sorry, I shouldn't have jumped to conclusions back there."
#         show merchant thinkingside
#         merchant "..."
#         $ merchant_courage += 1
#         show merchant frownside
#         merchant "No, you were right. I shouldn't have lashed out at my staff."
#         show merchant frownside
#         naomi troubled "..."
#         show merchant frown
#         naomi troubled "What was that all about, anyway?"
#         show merchant resigned
#         merchant "She was carrying too many things down the stairs." 
#         show merchant scowlside
#         merchant "She could have tripped and injured herself!"
#         naomi surprised "(So he was worried for her!)"
#         naomi troubled "Still, you didn't need to be so harsh."
#         show merchant frown
#         merchant "..."
#         show merchant resigned
#         merchant "I had apologised to her for my conduct."
#         show merchant scowlside
#         merchant "Consider your meddling appreciated."
#         show merchant frownside
#         naomi thinking "(...is that his way of saying thanks?)"
#         show merchant frown
#         merchant "Hm."
#         show merchant thinking
#         merchant "What's your name?"
#         naomi troubled "Eh? Uh... Naomi?"
#         show merchant frownside
#         merchant "Here."
#         window hide
#         show merchant_namecard zorder 3.0:
#             xalign 0.5 yalign 0.5 zpos 0 zoom 0.2
#             easein 1.0 yalign 0.6 zpos 800
#         pause
#         show merchant_namecard_front zorder 3.0:
#             xalign 0.5 yalign 0.5
#         pause
#         hide merchant_namecard_front
#         naomi blush "Mr Fujiya Yujiro..."
#         hide merchant_namecard with moveoutbottom
#         $ inventory.update({"namecard":["Fujiya Yujiro's namecard."]})
#         $ merchant_name = "Yujiro"
#         show merchant frown
#         merchant "Just Yujiro will do."
#         merchant "Come to my office."
#         naomi surprised "Huh?"
#         show merchant thinkingside
#         merchant "You came from the countryside to find a job, didn't you?"
#         naomi surprised "How did you know?"
#         show merchant thinking
#         merchant "It's not difficult to guess."
#         show merchant frownside
#         merchant "Well, you'll earn more working for me."
#         show merchant frown
#         merchant "I'll be expecting you."
#         show merchant frownside:
#             xzoom -1.0 zoom 1.0
#         hide merchant with moveoutleft
#         $ guy_display = False
#         naomi troubled "(What was that about?)"
#         naomi surprised "Oh no, his coffee!"
#         show kirako happy with moveinleft
#         kirako "Was that Yujiro?"
#         naomi surprised "You know him?"
#         kirako "Oh yes, his father runs the department store at Ginza."
#         show kirako pout
#         kirako "If he hadn't rushed off, I could have introduced you!"
#         naomi sleepy "It's fine, really."
#         naomi thinking "(I guess I can visit his office and find out more...)"
#     $ unlock_off_bldg = True
#     return

# First visit to office, courage 0-1
label merchant_3:
    $ encounters["merchant"] += 1
    show merchant scowlside:
        xalign 0.65 yalign 0.23 zoom 0.3
    show staff cry:
        xalign 0.75 yalign 0.28 zoom 0.3
    image office_table = "images/merchant/office_table.png"
    show office_table:
        xalign 0.8 yalign 1.0 zoom 0.5
    naomi thinking "(Fujiya... This should be it.)"
    merchant "This is not good enough to be shown to the company president."
    naomi troubled "(Is he being harsh on his staff again?)"
    if merchant_courage < 1:
        merchant "There is no mention about what we plan to have."
        merchant "Did we not discuss this in detail?"
        show merchant frownside:
            xalign 0.65 yalign 0.23 zoom 0.3
        staff "I apologise for my oversight. I will add it in."
        show merchant resigned:
            xalign 0.65 yalign 0.23 zoom 0.3
        merchant "Please do."
        show staff cry:
            xzoom -1.0
            linear 0.75 xalign 0.85
            easeout 2.0 xpos 1.3 ypos 0.2 zoom 1.0
    else:
        merchant "There is no-"
        show merchant scowlfront:
            xalign 0.65 yalign 0.23 zoom 0.3
        merchant "..."
        show merchant resigned:
            xalign 0.65 yalign 0.23 zoom 0.3
        merchant "Sorry."
        show merchant scowlside:
            xalign 0.65 yalign 0.23 zoom 0.3
        merchant "I meant to say, the structure is good but it needs more detail."
        show merchant resigned:
            xalign 0.65 yalign 0.23 zoom 0.3
        merchant "Please adjust it."
        show staff happy:
            xalign 0.75 yalign 0.28 zoom 0.3
        staff "Yes, sir. Right away!"
        show staff happy:
            xzoom -1.0
            linear 0.75 xalign 0.85
            easeout 2.0 xpos 1.3 ypos 0.2 zoom 1.0
    show merchant frown:
        xalign 0.65 yalign 0.23 zoom 0.3
    show merchant scowlfront:
        xzoom -1.0
    merchant "You came."
    show merchant frown:
        xzoom 1.0
    show bg office:
        linear 2.0 xalign 0.8 yalign 0.0 zoom 2.0
    show office_table:
        linear 2.0 xalign 0.8 ypos 2.1 zoom 1.1
    show merchant frown:
        linear 2.0 xalign 0.5 yalign 0.5 zoom 1.0
    naomi surprised "Um."
    $ guy_display = True
    show merchant scowlside
    merchant "The company president wants to build a new store in Asakusa."
    show merchant thinkingside
    merchant "I need someone to work with me with the project."
    show merchant thinking
    merchant "Can you do it?"
    naomi thinking "(I want this job.)"
    naomi troubled "(But I'm worried he'll be harsh with me.)"
    menu:
        naomi thinking "(What should I do?)"
        "Accept the job":
            naomi happy "I'll do it."
        "Voice concerns":
            naomi thinking "I want this job, but."
            show merchant surprised
            naomi troubled "From what I've observed, you're pretty harsh on your staff."
            naomi thinking "I know you care a lot."
            naomi troubled "But if you could be more gentle..."
            show merchant thinking
            merchant "..."
            $ merchant_courage += 1
            show merchant resigned
            merchant "I see."
            show merchant thinkingside
            merchant "You're right, I can be pretty harsh."
            show merchant scowlfront
            merchant "I'll prove to you I can do better, so."
            show merchant frown
            merchant "Will you give this a chance??"
            naomi relieved "I'll do it."
    show merchant happy
    merchant "Good."
    show merchant thinkingside
    merchant "You can come to the office anytime between Mondays and Fridays."
    show merchant thinking
    merchant "I'll pay you for the day's work."
    show merchant thinkingside
    merchant "At the end of the month, if your performance was good, I'll give you a job."
    naomi relieved "Fair enough."
    window hide
    show paperstack zorder 4.0:
        xpos 0.4 ypos 0.5 zpos 0 zoom 0.5
        easein 1.0 xpos 0.4 ypos 0.55 zpos 800
    show merchant frown
    merchant "You can start by filling in these forms."
    image merchant glitched1:
        glitch("merchant frown")
        pause 0.1
        glitch("merchant frown",offset=60,randomkey=None)
        pause 0.1
        glitch("merchant frown")
        pause 0.1
        "merchant frown"
    show merchant glitched1
    naomi troubled "Filling in forms...?" 
    show merchant happy
    merchant "Call me when you're done."
    show merchant frown:
        xzoom 1.0 xalign 0.5 yalign 0.0 zoom 1.0
    hide merchant with moveoutright
    naomi surprised "Eh?"
    $ guy_display = False
    naomi angry "What a bossy guy."
    naomi sleepy "Guess I'll just get started on this."
    hide paperstack with moveoutbottom
    hide office_table
    show bg office:
        linear 2.0 xalign 0.8 yalign 0.0 zoom 1.0
    return

#Third visit to office, courage 0-1
label merchant_4:
    $ encounters["merchant"] += 1
    show merchant scowlside:
        xalign 0.65 yalign 0.23 zoom 0.3
    show staff happy:
        xalign 0.75 yalign 0.28 zoom 0.3
    image office_table = "images/merchant/office_table.png"
    show office_table:
        xalign 0.8 yalign 1.0 zoom 0.5
    merchant "-by today."
    show merchant frown:
        xalign 0.65 yalign 0.23 zoom 0.3
    merchant "..."
    show merchant resigned:
        xalign 0.65 yalign 0.23 zoom 0.3
    merchant "That's all."
    show staff happy:
        xalign 0.75 yalign 0.28 zoom 0.3
    staff "I'll work on this right away!"
    show staff happy:
        xzoom -1.0
        linear 0.75 xalign 0.85
        easeout 2.0 xpos 1.3 ypos 0.2 zoom 1.0
    show merchant frown:
        xalign 0.65 yalign 0.23 zoom 0.3
    show merchant scowlfront:
        xzoom -1.0
    merchant "Naomi, come here for a minute."
    show merchant frown:
        xzoom 1.0
    naomi troubled "Uh, okay."
    show bg office:
        linear 2.0 xalign 0.8 yalign 0.0 zoom 2.0
    show office_table:
        linear 2.0 xalign 0.8 ypos 2.1 zoom 1.1
    show merchant scowlfront:
        linear 2.0 xalign 0.5 yalign 0.5 zoom 1.0
    $ guy_display = True
    merchant "I want to discuss plans for the new department store in Asakusa."
    merchant "Do you remember places that your parents brought you to when you were a child?"
    show merchant frown
    naomi surprised "Eh?"
    naomi thinking "(How is this related to the department store?)"
    naomi troubled "Uh... I guess so."
    naomi thinking "When they were free they would take us to the park to play..."
    naomi happy "Oh! And once in a while we'd get to go to the amusement park as a treat."
    show merchant surprised
    merchant "Amusement park."
    show merchant thinking
    merchant "Tell me more about this amusement park."
    naomi surprised "(Has he not been before?)"
    naomi thinking "(I wonder what kind of childhood he had.)"
    menu:
        "Probe more":
            naomi troubled "Did your parents not bring you as a child?"
            show merchant surprised
            merchant "..."
            $ merchant_courage += 1
            naomi surprised "Sorry, I shouldn't have asked something so personal!"
            show merchant resigned
            merchant "No, it's fine."
            merchant "I was the one who asked about your childhood first."
            show merchant frown
            merchant "Well, to answer your question."
            show merchant frownside
            merchant "Taking over the business was the priority for my father."
            merchant "I rarely went out to play like other children."
            show merchant frown
            naomi troubled "..."
            show merchant resigned
            merchant "It's fine."
            show merchant frown
            merchant "Tell me about the amusement park."
            naomi relieved "Sure!"
        "Leave it":
            naomi happy "Sure!"
    naomi happy "You can get on a ride, and it will take you high into the sky, round and round, or back and forth."
    naomi relieved "I rode the Ferris Wheel with my mother and she was too scared to look down from the top!"
    show merchant happy
    merchant "Perfect."
    show merchant thinking
    merchant "I shall propose to have an amusement park in the department store."
    naomi surprised "Eh? How?"
    show merchant thinkingside
    merchant "We'll use the roof."
    show merchant scowlside
    merchant "Thanks for the idea."
    image merchant glitched3:
        glitch("merchant scowlside")
        pause 0.1
        glitch("merchant scowlside",offset=60,randomkey=None)
        pause 0.1
        glitch("merchant scowlside")
        pause 0.1
        "merchant scowlside"
    show merchant glitched3
    naomi troubled "You're welcome..."
    show paperstack:
        xpos 0.4 ypos 0.5 zpos 0 zoom 0.5
        easein 1.0 xpos 0.4 ypos 0.55 zpos 800
    show merchant frown
    merchant "We have to get started on the proposal."
    show merchant scowlside
    merchant "Call me when you're done."
    show merchant frown:
        xzoom 1.0 xalign 0.5 yalign 0.0 zoom 1.0
    hide merchant with moveoutright
    $ guy_display = False
    naomi troubled "(I'll just get started on this first.)"
    hide paperstack with moveoutbottom
    hide office_table
    show bg office:
        linear 2.0 xalign 0.8 yalign 0.0 zoom 1.0
    return

#Fourth visit to office, courage 0-1, choice Y/N
label merchant_5:
    show merchant frownside:
        xalign 0.65 yalign 0.23 zoom 0.3
    image office_table = "images/merchant/office_table.png"
    show office_table:
        xalign 0.8 yalign 1.0 zoom 0.5
    naomi sleepy "(Where's Yujiro...?)"
    naomi surprised "(Ah.)"
    naomi thinking "(He looks troubled.)"
    show bg office:
        linear 2.0 xalign 0.8 yalign 0.0 zoom 2.0
    show office_table:
        linear 2.0 xalign 0.8 ypos 2.1 zoom 1.1
    show merchant scowlfront:
        zoom 0.3
        linear 2.0 xalign 0.5 yalign 0.5 zoom 1.0
    naomi troubled "Did something happen?"
    show merchant frownside
    merchant "..."
    show merchant frown
    merchant "The old man wants the department store to be accessible by train."
    show merchant resigned
    merchant "We have to rework the proposal."
    naomi surprised "Eh?! But isn't the meeting tomorrow?"
    naomi troubled "I don't think we can finish all that today."
    show merchant thinkingside
    merchant "It's fine."
    merchant "I'll continue working on it tonight."
    menu:
        naomi troubled "(He's planning to work on it alone?)"
        "Trust him to finish":
            naomi relieved "Alright, I trust you'll be able to finish it."
            show merchant thinking
            merchant "Of course, I'll get it done."
            $ salary = renpy.random.randint(20, 25)
            $ money += salary
            show merchant frown
            merchant "Here's [salary] yen for today's work."
            naomi happy "Thanks!"
            $ merchant_job += 1
            if timeslot == 1:
                menu:
                    merchant "Do you want to work the afternoon too?"
                    "Work the afternoon":
                        naomi happy "Sure, I'll stay for the afternoon."
                        $ merchant_job -= 1
                        show merchant scowlfront
                        merchant "Here, work on this."
                        show paperstack:
                            xpos 0.4 ypos 0.5 zpos 0 zoom 0.5
                            easein 1.0 xpos 0.4 ypos 0.55 zpos 800
                        show merchant frownside
                        merchant "I'll come back later."
                        hide merchant with moveoutright
                        show time:
                            xalign 0.5 yalign 0.5
                            ease 1.0 rotate 45
                            ease 1.0 rotate -45
                            ease 1.0 rotate 0
                        naomi thinking "..."
                        hide time
                        hide paperstack
                        naomi sleepy "I'm finally done."
                        return
                    "Go out":
                        naomi relieved "No, I'll head off now."
                        merchant "Bye."
                        jump ginza_small
            if timeslot < 1:
                naomi relieved "I'll head home first."
                merchant "Bye."
                jump evening_time
        "Insist on helping":
            naomi relieved "I'll stay back to work on it with you."
            merchant "It's alright, I can manage."
            show merchant thinking
            naomi angry "But I'm helping you on this project."
            show merchant surprised
            naomi troubled "I can't let you work on it alone."
            naomi relieved "We'll finish sooner if we work on it together."
            merchant "..."
            $ merchant_job += 1
            $ merchant_courage += 1
            $ merchant_choice = 1
            show merchant resigned
            merchant "Alright, I got it."
            show merchant happy
            merchant "Let's get started."
            show paperstack:
                xpos 0.4 ypos 0.5 zpos 0 zoom 0.5
                easein 1.0 xpos 0.4 ypos 0.55 zpos 800
            naomi thinking "..."
            show time:
                xalign 0.5 yalign 0.5
                ease 1.0 rotate 45
                ease 1.0 rotate -45
                ease 1.0 rotate 0
            image merchant discussing:
                "merchant thinking"
                pause 0.3
                "merchant thinkingside"
                pause 0.3
                "merchant scowlside"
                pause 0.3
                "merchant scowlfront"
                pause 0.3
                "merchant frown"
                pause 0.3
                "merchant thinking"
                pause 0.3
                "merchant thinkingside"
                pause 0.3
                "merchant scowlside"
                pause 0.3
                "merchant scowlfront"
                pause 0.3
                "merchant frown"
            show merchant discussing:
                zoom 1.0 matrixcolor BrightnessMatrix(0.0)
                easeout 3.0 matrixcolor BrightnessMatrix(-0.1)
            show bg office:
                matrixcolor BrightnessMatrix(0.0)
                easeout 3.0 matrixcolor BrightnessMatrix(-0.2)
            show office_table:
                matrixcolor BrightnessMatrix(0.0)
                easeout 3.0 matrixcolor BrightnessMatrix(-0.2)
            naomi thinking "..."
            pause
            if timeslot > 0:
                show time:
                    xalign 0.5 yalign 0.5
                    ease 1.0 rotate 45
                    ease 1.0 rotate -45
                    ease 1.0 rotate 0
                show merchant discussing
                naomi angry "..."
                $ timeslot -= 1
            hide time
            hide paperstack
            show merchant resigned
            merchant "Let's take a break."
            naomi pain "Alright."
            show merchant frownside
            merchant "Wait here, I'll get some coffee."
            hide merchant with moveoutright
            naomi sleepy "(It's getting harder to keep my eyes open...)"
            naomi sleepy "(I'll just rest my eyes for a while...)"
            scene merchant_cutscene_1 with Fade(2.0,0.5,2.0)
            pause
            merchant "You'll catch a cold."
            naomi sleepy "(This scent... Cedarwood...)"
            hide window
            pause
            $ totaldays -= 1
            $ dayofweeknumber += 1
            $ timeslot = 2
            jump office_bldg

# Difference for choice Y/N
label merchant_6:
    if merchant_choice == 0:
        show merchant frownside:
            xalign 0.65 yalign 0.23 zoom 0.3
        image office_table = "images/merchant/office_table.png"
        show office_table:
            xalign 0.8 yalign 1.0 zoom 0.5
        naomi troubled "(I wonder how the meeting went.)"
        show bg office:
            linear 2.0 xalign 0.8 yalign 0.0 zoom 2.0
        show office_table:
            linear 2.0 xalign 0.8 ypos 2.0 zoom 1.1
        show merchant frown:
            zoom 0.3
            linear 2.0 xalign 0.5 yalign 0.0 zoom 1.0
        naomi troubled "How did the meeting go?"
        show merchant thinking
        merchant "The proposal was approved."
        naomi happy "That's great!"
        show merchant thinkingside
        merchant "But some parts still need work."
        show merchant frown
        merchant "Here."
        show paperstack:
            xpos 0.4 ypos 0.5 zpos 0 zoom 0.5
            easein 1.0 xpos 0.4 ypos 0.55 zpos 800
        show merchant scowlside
        merchant "Work on this first."
        show merchant frownside
        merchant "I'll come back later."
        hide merchant with moveoutright
        return
    if merchant_choice == 1:
        scene bg office:
            xalign 0.8 yalign 0.0
        show staff happy:
            xalign 0.6 zoom 1.5 yalign 0.1
        with Fade(2.0,0.5,2.0)
        staff "Good morning."
        naomi sleepy "Good morning..."
        naomi surprised "I'm in office?"
        show staff show:
            ease 1.0 xalign 0.4 zoom 1.5 yalign 0.1
        staff "You fell asleep here last night."
        naomi troubled "I see..."
        naomi thinking "(I smell cedarwood...)"
        naomi surprised "(This coat.)"
        naomi surprised "Yujiro?"
        show staff happy:
            ease 1.0 xalign 0.6 zoom 1.5 yalign 0.1
        staff "The director is in a meeting now."
        naomi relieved "I see."
        naomi relieved "(I'm glad we made it in time.)"
        show staff happy zorder 3.0:
            ease 1.0 xalign 0.6 zoom 2.0 yalign 0.1
        staff "Were you working late last night? He asked us not to wake you."
        naomi blush "Yes... But I must have fallen asleep at some point."
        staff "Ah, it looks like the meeting has ended."
        show merchant frownside:
            xalign 0.65 yalign 0.23 zoom 0.3
        image office_table = "images/merchant/office_table.png"
        show office_table:
            xalign 0.8 yalign 1.0 zoom 0.5
        show staff happy:
            xalign 0.6 zoom 2.0 yalign 0.1 xzoom -1.0
        staff "I'll go back to my desk."
        hide staff with moveoutright
        merchant "Naomi."
        naomi surprised "!"
        show bg office:
            linear 2.0 xalign 0.8 yalign 0.0 zoom 2.0
        show office_table:
            linear 2.0 xalign 0.8 ypos 2.1 zoom 1.1
        show merchant frown:
            linear 2.0 xalign 0.5 yalign 0.5 zoom 1.0
        merchant "Are you alright? You were really tired."
        naomi blush "I'm sorry I fell asleep!"
        show merchant scowlside
        merchant "I shouldn't have let you work late."
        naomi blush "You could have just woke me up..."
        show merchant thinking
        merchant "You were sleeping so soundly, I-"
        naomi blush "H-here, your coat!"
        show merchant surprised
        merchant "..."
        show merchant resigned
        merchant "Thanks."
        show merchant happy
        merchant "The old man was pleased with the proposal."
        naomi surprised "That's great!"
        show merchant frownside
        merchant "Naomi, I."
        show merchant scowlside
        merchant "Thanks for staying back with me."
        image merchant glitched:
            glitch("merchant scowlside")
            pause 0.1
            glitch("merchant scowlside",offset=60,randomkey=None)
            pause 0.1
            glitch("merchant scowlside")
            pause 0.1
            glitch("merchant scowlside",offset=60,randomkey=None)
            pause 0.1
            glitch("merchant scowlside")
            "merchant scowlside"
        show merchant glitched
        naomi surprised "..."
        show merchant frown
        naomi relieved "You can rely on me."
        naomi happy "Let's keep working hard together."
        show merchant smile
        merchant "Yeah."
        naomi blush "..."
        show merchant surprised
        merchant "..."
        show merchant thinkingside
        merchant "..."
        $ salary = renpy.random.randint(40,50)
        $ money += salary
        merchant "Here's [salary] yen for yesterday's work."
        $ merchant_job += 1
        show merchant frownside
        merchant "Go home and get some rest."
        naomi troubled "(Is he...)"
        naomi surprised "(Embarassed??)"
        naomi blush "(It must be my imagination!)"
        if dayofweeknumber < 6:
            menu:
                naomi "Where should I go this morning?"
                "Stay at office":
                    naomi blush "I'll stay for the morning."
                    show merchant frown
                    merchant "Are you sure? Don't push yourself."
                    naomi relieved "I'm fine."
                    naomi happy "There's work to do after the meeting."
                    merchant "...Alright."
                    show paperstack:
                        xpos 0.4 ypos 0.5 zpos 0 zoom 0.5
                        easein 1.0 xpos 0.4 ypos 0.55 zpos 800
                    show merchant frownside
                    merchant "I'll come back later."
                    hide merchant with moveoutright
                    hide office_table
                    show bg office:
                        linear 2.0 xalign 0.8 yalign 0.0 zoom 1.0
                    return
                "Go elsewhere":
                    naomi blush "Um, I'll head off then."
                    show merchant frown
                    merchant "Bye."
                    jump ginza_small
        else:
            naomi blush "Um, I'll head off then."
            show merchant frown
            merchant "Bye."
            jump weekend_saturday


label merchant_7:
    show merchant thinking
    merchant "By the way."
    naomi surprised "Yes?"
    show merchant thinkingside
    merchant "Are you free this Saturday evening?"
    naomi troubled "Yes...?"
    naomi troubled "(What is this about?)"
    merchant "Will you come with me to the dance hall?"
    naomi blush "Dance hall?"
    naomi blush "(It sounds like he's asking me out!)"
    show merchant scowlside
    merchant "There's an architect I need to talk to, but he's only in town for the dance this weekend."
    naomi troubled "(I see, it's just work.)"
    show merchant frown
    merchant "..."
    show merchant frownside
    merchant "It's the rule of the dance hall to bring a partner..."
    naomi relieved "Alright, I'll go with you."
    $ merchant_event = True
    show merchant happy
    merchant "I'll pick you up at the cafe."
    merchant "Make sure to wear something appropriate."
    naomi troubled "Got it."
    return

label office_ending:
    naomi happy "I guess this is where I'll be working from now on."
    naomi thinking "I achieved my goal of finding a job within these two weeks."
    naomi troubled "Why does it feel like I'm missing something important?"
    $ day_display = False
    show black1:
        xalign 0.5 yalign 1.0 #full close
    show black2:
        xalign 0.5 yalign 0.0 #full close
    show text "{color=#ffffff}Game over.{/color}":
        xalign 0.5 yalign 0.5
    with Fade(2.0,0.5,0.5)
    pause
    $ renpy.full_restart()