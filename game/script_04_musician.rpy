# label imperial_theatre:

#     scene bg imperial theatre
#     if musician_ending == True:
#         if musician_courage > 2:
#             jump musician_final_irl
#         else:
#             jump musician_final_not
#     if totaldays == 0:
#         jump theatre_ending

#     if encounters["musician"] == 1:
#         call musician_2
#     elif encounters["musician"] == 4:
#         if totaldays > 3:
#             call musician_6a
#         else:
#             call musician_6b
#     if musician_job == 1:
#         # naomi thinking "(I wonder if I'll run into Hideo.)"
#         # naomi thinking "(I haven't had the chance to thank him for this job...)"
#         call musician_3
#     play music "<from 246>cello.mp3" fadein 3 if_changed
#     naomi happy "I'll work a shift now."
#     show bg imperial theatre:
#         linear 2.0 xalign 1.0 yalign 0.5 zoom 2.0
#     ticketer "Come on over here then."
#     show time:
#         xalign 0.5 yalign 0.5
#         ease 1.0 rotate 45
#         ease 1.0 rotate -45
#         ease 1.0 rotate 0
#     naomi thinking "..."
#     hide time
#     if musician_job == 1:
#         customer "Front row tickets for the Saturday afternoon performance."
#         naomi relieved "Please wait a moment."
#         naomi troubled "(This performance is pretty popular.)"
#         naomi troubled "I only have seats at the back, is that alright?"
#         customer "But I won't be able to see the handsome cellist."
#         naomi troubled "..."
#         customer "Better than nothing. I'll take it then."
#         naomi relieved "Have a good day."
#         naomi thinking "(Handsome cellist?)"
#     if musician_job > 5 and encounters["musician"] < 4 and musician_event == 2:
#         ticketer "Are you friends with the cellist?"
#         ticketer "I heard he's been skipping rehearsals."
#         naomi surprised "You mean Hideo?"
#         naomi troubled "(Come to think of it, I haven't seen him here lately...)"
#         naomi troubled "(Perhaps he might drop by the cafe instead.)"
#         $ encounters["musician"] = 3
#     hide time
#     $ timeslot -= 1
#     naomi sleepy "I've sold quite a bit today."
#     $ salary = renpy.random.randint(8, 12)
#     $ money += salary
#     ticketer "Here's [salary] yen for today's work."
#     if musician_job == 1:
#         naomi happy "Thank you!"
#         if totaldays > 9:
#             ticketer "By the way, do you want to see the Saturday afternoon performance?"
#             naomi thinking "It's really popular, isn't it?"
#             menu:
#                 ticketer "There are only a few seats at the last row, but you can have one for 10 yen."
#                 "I'll take it" if money >= 10:
#                     $ money -= 10
#                     naomi happy "I'll take it."
#                     ticketer "Here you go then."
#                     window hide
#                     show ticket_back_new:
#                         xalign 0.4 yalign 0.6 zpos 0 zoom 0.5
#                         easein 1.0 xalign 0.5 yalign 0.7 zpos 400 zoom 1.0
#                     pause
#                     hide ticket_back_new with moveoutbottom
#                     $ inventory.update({"ticket_back_new":["Ticket for a seat in the last row."]})
#                     $ musician_choice += 1
#                     $ musician_event = 1
#                 "I'll pass":
#                     naomi relieved "I'll pass. Maybe next time."
#                     ticketer "Alright."
#     if musician_job == 3 and totaldays > 8:
#         stop music fadeout 3
#         call musician_4
#     if musician_job > 7 and encounters["musician"] == 5 and pre_musician_event_2 == True:
#         stop music fadeout 3
#         call musician_7
#     # if musician_job == 8 and musician_event == 2:
#     #     call musician_5
#     $ musician_job += 1
#     # Check if morning or afternoon
#     if timeslot == 1:
#         menu:
#             ticketer "Do you want to work the afternoon too?"
#             "Work the afternoon":
#                 naomi happy "Sure, I'll stay for the afternoon."
#                 jump imperial_theatre
#             "Go out":
#                 naomi relieved "No, I'll head off now."
#                 ticketer "See you next time."
#                 stop music fadeout 5
#                 jump ginza_small
#     if timeslot < 1:
#         naomi relieved "I'll head home now."
#         ticketer "See you next time."
#         stop music fadeout 5
#         jump evening_time


label imperial_theatre:

    scene bg imperial theatre
    play music "<from 246>cello.mp3" fadein 3 if_changed

    ## Encounter 2: First time at Imperial Theatre
    if encounters["musician"] == 3:
        if not flag("musician_show_seen"):
            call musician_3
        else:
            $ encounters["musician"] += 1
    if encounters["musician"] == 2:
        call musician_2
    if encounters["musician"] == 1:
        call musician_1
    if encounters["musician"] == 7:
        $ days_since_musician_5 = story_flags.get("musician_5_day", -9999) - totaldays
        if days_since_musician_5 <= 2:
            call musician_6a
        else:
            call musician_6b

    ## Post-show disappearance
    $ days_since_show = story_flags.get("musician_show_day", -9999) - totaldays

    if days_since_show >= 4 and not flag("musician_ticketer_talk_seen"):
        ticketer "Are you friends with the cellist?"
        ticketer "I heard he's been skipping rehearsals."
        naomi surprised "You mean Hideo?"
        naomi troubled "(Come to think of it, I haven't seen him here lately...)"
        naomi troubled "(Perhaps he might drop by the cafe instead.)"
        $ set_flag("musician_ticketer_talk_seen")
        $ encounters["musician"] += 1
    elif 0 < days_since_show < 4:
        naomi troubled "(I wonder where Hideo's been. I haven't seen him around here lately.)"

    $ timeslot -= 1

    ## Check if morning or afternoon
    if timeslot == 1:
        naomi thinking "Where should I go next?"
        stop music fadeout 5
        jump ginza_small
    if timeslot < 1:
        naomi relieved "I'll head home now."
        stop music fadeout 5
        jump evening_time

label musician_0:
    show cafetableright zorder 3.0
    show musician shy with moveinleft:
        xalign 0.5
    $ musician_name = "???"
    naomi thinking "..."
    musician "..."
    naomi surprised "(Oh! A customer.)"
    # naomi surprised "(He's carrying a shamisen?)"
    # naomi troubled "(He looks a little unfriendly...)"
    naomi happy "Hi! What can I get for you?"
    show musician shy2
    musician "...Pudding, please."
    naomi relieved "One Pudding à la Mode, coming right up!"
    window hide
    show musician shy
    image pudding = "images/cafe/Pudding.png"
    show pudding zorder 3.0:
        xalign 0.5 ypos 0.9 zpos 400 zoom 0.5
        easein 1.0 ypos 0.7 zpos 0
        linear 0.1 xzoom 1.0 yzoom 0.9 ypos 0.7
        linear 0.1 xzoom 1.0 yzoom 1.0 ypos 0.7
    pause
    hide pudding
    image pudding_no = "images/cafe/pudding_no.png"
    image pudding_cherry = "images/cafe/pudding_cherry.png"
    show pudding_no zorder 3.0:
        xalign 0.5 ypos 0.7 zoom 0.5
    show pudding_cherry zorder 4.0:
        xalign 0.46 ypos 0.75 zoom 0.5
        easeout_circ 0.8 align (0.4, 0.85) knot (0.41, 0.83) zpos 150 zoom 0.6
        ease 0.6 align (0.35, 0.85) knot (0.37, 0.82)
    show musician shy2
    pause
    naomi surprised "..."
    naomi blush "I'm so sorry! The cherry—"
    show musician happy
    musician "...It's fine."
    musician "The pudding's the same either way."
    # musician "Everyone makes mistakes starting out."
    image musician glitched:
        glitch("musician happy")
        pause 0.1
        glitch("musician happy",offset=60,randomkey=None)
        pause 0.1
        glitch("musician happy")
        pause 0.1
        "musician happy"
    show musician glitched
    naomi thinking "(He's... not angry.)"
    naomi relieved "(He's nicer than he looks.)"
    show musician thinking
    musician "You're new here."
    naomi blush "Yes, just started actually."
    naomi thinking "(He knows I'm new.)"
    naomi happy "Have you been coming often?"
    show musician shy
    musician "Every now and then."
    show musician happy
    musician "When I feel like having pudding."
    show musician shy2
    musician "...But it's been quieter lately."
    naomi surprised "Is that so?"
    musician "A new cafe opens, some customers go there."
    naomi thinking "(So there's been competition from other cafes.)"
    naomi happy "You're still here, though."
    show musician shy
    musician "...The pudding's better here."
    naomi relieved "(He really likes the pudding.)"
    naomi relieved "Any ideas how we could get more customers in?"
    show musician thinking
    musician "..."
    show musician shy2
    musician "There's the theatre crowd."
    naomi surprised "Theatre crowd?"
    show musician shy
    musician "After a show, people look for somewhere to go."
    show musician thinking
    musician "...I perform at the Imperial Theatre. In Ginza."
    naomi thinking "(Ginza is a little far. But if he came here just for pudding...)"
    naomi angry "(It's worth looking into.)"
    naomi happy "Thank you for the suggestion, I'll talk to the owner."
    # naomi thinking "(Someone who comes here often. Maybe he can give me some ideas.)"
    # menu:
    #     naomi thinking "(What should I ask?)"
    #     "Ask about the shamisen":
    #         $ musician_courage += 1
    #         naomi happy "Is that a shamisen you're carrying?"
    #         show musician shy2
    #         musician "Yes."
    #         naomi happy "You're a musician then?"
    #         show musician shy
    #         musician "You could say that."
    #         naomi relieved "Do you perform somewhere?"
    #         show musician thinking
    #         musician "The Imperial Theatre."
    #         naomi surprised "(The Imperial Theatre!)"
    #         naomi thinking "(That crowd, coming here after a show...)"
    #         naomi happy "I'd love to hear you play someday."
    #         show musician shy
    #         musician "...Maybe someday."
    #     "Ask for ideas for cafe":
            # naomi relieved "Actually, I've been wondering..."
            # naomi troubled "The cafe has been a little quiet lately..."
            # naomi relieved "Any idea how we could make it better?"
            # show musician thinking
            # musician "..."
            # show musician shy2
            # musician "There's the theatre crowd."
            # naomi surprised "Theatre crowd?"
            # show musician shy
            # musician "After a show, people look for somewhere to go."
            # show musician thinking
            # musician "...I perform at the Imperial Theatre. In Ginza."
            # naomi thinking "(Ginza is a little far. But if he came here just for pudding...)"
            # naomi angry "(It's worth looking into.)"
            # naomi happy "The theatre! I hadn't thought of that."
    naomi thinking "(I should get his name at least.)"
    naomi happy "By the way, I'm Naomi. You are...?"
    show musician shy
    musician "...Hideo."
    naomi relieved "Nice to meet you, Hideo."
    $ musician_name = "Hideo"
    show musician happy
    musician "Nice meeting you too, Naomi."
    show musician shy2
    musician "So, I'll see you again?"
    naomi happy "Yes, see you next time!"
    hide musician
    hide pudding_no
    hide pudding_cherry
    with moveoutleft
    naomi thinking "(The Imperial Theatre.)"
    naomi thinking "(I should go and have a look.)"
    # $ encounters["musician"] += 1
    $ unlock_imp_th = True
    return

label musician_1:
    show fans_less
    naomi happy "So this is the Imperial Theatre... It's grand!"
    naomi thinking "I hear music from behind the doors."
    naomi happy "Could Hideo be rehearsing today?"
    naomi pain "Such a lovely music."
    naomi thinking "(I wonder what upcoming performances there are.)"
    show fans_less:
        linear 2.0 xalign 1.0 yalign 0.5 zoom 2.0
    show bg imperial theatre:
        linear 2.0 xalign 1.0 yalign 0.5 zoom 2.0
    pause
    customer "Front row tickets for the Saturday afternoon performance."
    ticketer "I only have seats at the back."
    naomi thinking "(This performance seems quite popular.)"
    customer "But I won't be able to see the handsome cellist."
    ticketer "..."
    customer "Better than nothing. I'll take it then."
    naomi thinking "(Handsome cellist? I should check this out.)"
    ticketer "Next please."
    naomi troubled "Uh..."
    ticketer "Saturday afternoon performance?"
    menu:
        ticketer "There are only a few seats at the last row, one ticket will be 10 yen."
        "I'll take it" if money >= 10:
            $ money -= 10
            naomi happy "I'll take it."
            ticketer "Here you go then."
            window hide
            show ticket_back_new:
                xalign 0.4 yalign 0.6 zpos 0 zoom 0.5
                easein 1.0 xalign 0.5 yalign 0.7 zpos 400 zoom 1.0
            pause
            hide ticket_back_new with moveoutbottom
            $ inventory.update({"ticket_back_new":["Ticket for a seat in the last row."]})
            $ musician_choice += 1
            $ musician_event = 1
        "I'll pass":
            naomi relieved "I'll pass. Maybe next time."
            ticketer "Alright."
    show fans_less:
        linear 2.0 xalign 0.5 yalign 0.5 zoom 1.0
    show bg imperial theatre:
        linear 2.0 xalign 0.5 yalign 0.5 zoom 1.0
    pause
    fan "Did you hear? Hideo was spotted at a cafe in Asakusa."
    naomi thinking "(Eh? Hideo's fan?)"
    fan "Really? Which one?"
    fan "I don't know, but I'd go just to see him!"
    naomi surprised "(Hideo's fans follow him outside the theatre.)"
    naomi thinking "(If they knew about Cafe Diamond...)"
    naomi happy "That's it."
    naomi thinking "Now I need to convince Hideo to help."
    # naomi happy "Music really draws people..."
    # naomi surprised "What if we had that in the cafe?"
    # naomi thinking "A night of music. Fans who might become patrons."
    # naomi happy "That's it."
    # naomi thinking "Now I just need to convince Hideo."
    $ encounters["musician"] += 1
    return

# label musician_2:
#     play music "<from 135 to 155>cello.mp3"
#     naomi happy "So this is the Imperial Theatre... It's grand!"
#     naomi thinking "Now where can I find Hideo?"
#     naomi surprised "Ah but."
#     naomi pain "What is this music? Such a lonesone tune, I feel my heart ache."
#     naomi thinking "It wouldn't hurt just to listen for a while."
#     stop music fadeout 3
#     show musician shy with moveinleft:
#         xalign 0.5
#     window hide
#     pause
#     musician "Hey, you came."
#     naomi happy "Hey!"
#     menu:
#         "Ask about job":
#             naomi blush "Umm... About what we discussed before..."
#             show musician shy2
#             musician "Ah, yes..."
#         "Ask about music":
#             $ musician_courage += 1
#             naomi troubled "I heard music..."
#             show musician shy
#             musician "Were you listening?"
#             show musician shy2
#             musician "It was full of mistakes... I'm still working on-"
#             naomi thinking "Everyone makes mistakes starting out."
#             show musician surprised
#             naomi smirk "Someone told me that."
#             musician "..."
#             naomi happy "Besides, I didn't think it sounded bad."
#             naomi relieved "I was moved by it."
#             show musician happy
#             musician "Thanks for telling me."
#             show musician shy
#             musician "It'll be perfect by performance day."
#             naomi relieved "That's the spirit!"
#             show musician shy2
#             musician "...Oh, yeah."
#     show musician thinking
#     musician "They're hiring staff to sell tickets on weekdays."
#     musician "If you want, you can start immediately."
#     $ encounters["musician"] += 1
#     naomi happy "Thank you so much!"
#     show musician shy2
#     musician "You're welcome."
#     show musician shy
#     musician "I've got to get back to practice."
#     naomi blush "Sorry for disturbing you!"
#     show musician shy2
#     musician "I'll see you around, then?"
#     if musician_courage > 0:
#         show musician happy
#     naomi blush "Yes, see you!"
#     hide musician with moveoutleft
#     play music "<from 246>cello.mp3"
#     naomi thinking "I guess this is the ticket counter."
#     show bg imperial theatre:
#         linear 2.0 xalign 1.0 yalign 0.5 zoom 2.0
#     naomi troubled "Hello, I'm Naomi. I heard that I could start working today?"
#     ticketer "You're the new girl, yes?" 
#     ticketer "You can work morning or afternoon shifts on weekdays and you'll be paid for your time."
#     return

label musician_2:
    play music "<from 135 to 155>cello.mp3"
    naomi thinking "Where can I find Hideo? I need to convince him to help us."
    naomi surprised "Ah but."
    naomi pain "Is this the cello? Such a lonesone tune, I feel my heart ache."
    naomi sleepy "I'll just listen for a while."
    stop music fadeout 3
    show musician shy with moveinleft:
        xalign 0.5
    window hide
    pause
    show musician shy
    musician "..."
    naomi surprised "Hideo!"
    show musician surprised
    musician "...Naomi?"
    naomi happy "I was looking for you, but I got distracted by the lovely cello music..."
    show musician shy2
    musician "You were listening?"
    naomi surprised "Was that you? I thought you played the shamisen."
    show musician shy
    musician "Well, I play the cello now."
    naomi thinking "(Handsome cellist...)"
    naomi surprised "Are you performing this Saturday?"
    show musician shy2
    musician "Yeah..."
    show musician shy
    musician "Uh, you were looking for me?"
    naomi blush "Yes, I was hoping to get your help..."
    naomi thinking "I have an idea how we could help the cafe."
    naomi happy "Music on some evenings, something to bring new crowd in."
    naomi troubled "I was wondering... Would you consider playing there sometime?"
    show musician thinking
    musician "The cello doesn't work well on its own."
    musician "It needs an orchestra to be complete."
    show musician troubled
    musician "...Sorry."
    naomi thinking "(He didn't say no, but he seems reluctant.)"
    naomi troubled "(I don't want to be too pushy, but I really hope he can help.)"
    menu:
        "Just a fan meet then?":
            naomi happy "What if it's just a fan meet then?"
            show musician thinking
            musician "..."
            musician "I don't think anyone will come."
            naomi thinking "Really?"
            naomi thinking "I overheard your fans."
            naomi smirk "They were talking about tracking you down in Asakusa."
            show musician troubled
            musician "That's..."
            naomi relieved "You don't have to decide now."
            naomi happy "Just think about it."
            show musician shy
            musician "...Alright."
        "How about shamisen?":
            $ add_point("musician")
            naomi thinking "How about the shamisen then?"
            show musician shy
            musician "..."
            naomi thinking "(Did I assume too much? Just because he carries it...)"
            naomi surprised "I'm sorry!"
            naomi troubled "You're always carrying it around, so I thought..."
            show musician shy2
            musician "No, it's fine."
            musician "...I'm just used to having it with me."
            musician "Now that I perform the cello, I don't play it so much."
            naomi thinking "(It means enough to him that he carries it with him.)" 
            naomi relieved "(Even now, when he plays the cello.)"
            naomi relieved "I'd love to hear you play the shamisen someday."
            show musician happy
            musician "...Maybe someday."
        # "Your music moved me":
        #     $ add_point("musician")
        #     naomi thinking "You know, when I heard your cello earlier."
        #     show musician troubled
        #     naomi happy "I couldn't help but stop to listen."
        #     show musician shy
        #     musician "I haven't gotten it right yet."
        #     musician "It's still raw, with errors and mistakes-"
        #     naomi relieved "I was moved by it."
        #     show musician surprised
        #     naomi happy "It wasn't perfect, but it made me feel something."
        #     naomi thinking "I think other people would, too."
        #     show musician shy2
        #     musician "You think so?"
        #     naomi happy "I stopped, didn't I?"
        #     show musician shy
        #     musician "...I'll think about it."
    show musician shy2
    musician "I've got to get back to practice now."
    naomi blush "Sorry for disturbing you!"
    show musician shy2
    musician "I'll see you around, then?"
    if get_stage("musician") >= 1:
        show musician happy
    naomi blush "Yes, see you!"
    hide musician with moveoutleft
    play music "<from 246>cello.mp3"
    naomi troubled "I don't know if I managed to convince him."
    naomi thinking "I'll just have to keep trying."
    $ encounters["musician"] += 1
    return            

# label musician_3:
#     stop music fadeout 3.0
#     $ guy_display = True
#     show musician shy2:
#         xalign 0.5
#     naomi surprised "(It's Hideo!)"
#     show musician shy
#     musician "Hey, Naomi."
#     naomi blush "Hi! I was hoping to run into you, actually."
#     naomi happy "I haven't thanked you for helping me to get this job."
#     show musician shy2
#     musician "It's no trouble at all."
#     naomi relieved "Even so, I'm grateful!"
#     naomi happy "Are you heading for rehearsal?"
#     show musician thinking
#     musician "Yeah, I've got to put in extra cello practice."
#     naomi surprised "You play the cello?"
#     show musician shy2
#     musician "Yeah."
#     menu:
#         naomi thinking "(He plays the cello but he's always carrying around a shamisen.)"
#         "Ask about shamisen":
#             naomi troubled "Why do you always carry around a shamisen then?"
#             show musician shy
#             musician "..."
#             show musician shy2
#             musician "It's my grandfather's. He taught me to play."
#             naomi relieved "That's lovely. Why the cello, then?"
#             show musician troubled
#             musician "..."
#             musician "The cello... I can join an orchestra."
#             musician "But the shamisen..."
#             naomi thinking "But you still carry it with you."
#             $ musician_courage += 1
#             show musician shy
#             musician "I..."
#             show musician shy2
#             musician "I guess I'm just used to having it with me."
#             naomi troubled "I see..."
#             naomi relieved "I'd love to hear you play the shamisen someday."
#             musician "Yeah, someday."
#         "Comment on cello":
#             naomi happy "I think it's cool you play the cello."
#             show musician shy
#             musician "Thanks."
#     musician "I've got to head to practice now."
#     naomi happy "See you!"
#     $ guy_display = False
#     hide musician with moveoutleft
#     return

label musician_3:
    stop music fadeout 3.0
    naomi troubled "(I hope I can catch Hideo again.)"
    naomi troubled "(Did he already leave?)"
    show musician shy2:
        xalign 0.5
    naomi surprised "Hideo!"
    naomi relieved "Thank goodness, I thought you already left."
    show musician shy
    musician "I'm still around."
    naomi thinking "(He looks down.)"
    naomi troubled "Is something wrong?"
    show musician shy2
    musician "No, I'm just."
    show musician troubled
    musician "What if I mess up?"
    naomi surprised "But you've been rehearsing so many times."
    show musician thinking
    musician "Yes, but with everyone watching... It's different."
    naomi troubled "(How should I encourage him?)"
    menu:
        "You'll be great":
            naomi happy "Don't worry, you sound so good during rehearsal. You'll be great."
            show musician shy2
            musician "Thanks."
        # "Encourage him":
        #     naomi happy "You know, from the ticket booth, I can hear you guys rehearsing."
        #     naomi happy "The music gets better every day."
        #     show musician happy
        #     musician "Thank you, I'm glad to hear that."
        # "Ask what's wrong":
            # naomi troubled "Is something wrong?"
            # $ musician_courage += 1
            # show musician shy2
            # musician "...I'm just."
            # show musician troubled
            # musician "What if I mess up?"
            # naomi surprised "But you've been rehearsing so many times."
            # show musician thinking
            # musician "Yes, but with everyone watching... It's different."
            # naomi troubled "I see..."
        "Focus on the music":
            $ add_point("musician")
            naomi thinking "When I overheard your music, I was so absorbed I didn't notice you approach."
            naomi happy "Once you focus on your music, the crowd will fade away too."
            musician "Focus on my music."
            show musician happy
            musician "I can do that."
            naomi relieved "(He just needed to change his perspective. Good.)"
        "Play for one person":
            $ add_point("musician")
            naomi thinking "What if you don't play for everyone?"
            show musician surprised
            naomi relieved "Just one person."
            naomi happy "Imagine you're playing for that person."
            show musician thinking
            musician "That... could work."
            naomi relieved "(He just needed to change his perspective. Good.)"
            $ set_flag("pre_musician_event_1")
    show musician shy2
    musician "Umm..."
    show musician shy
    musician "Will you come this Saturday?"
    if musician_choice == 1:
        naomi happy "Yes, of course!"
        show musician surprised
        naomi thinking "It was selling out fast, but I managed to get a seat in the back."
        naomi happy "I'll be cheering you on from behind!"
        $ musician_event = 1
    else:
        naomi troubled "I would have, but the tickets were selling out..."
        show musician shy2
        musician "I see."
        naomi troubled "I'm sorry, I..."
        show musician shy
        musician "It can't be helped, don't worry about it."
        naomi relieved "You'll do great, you've been practicing so much."
        naomi happy "I'll be cheering you on in spirit."
    show musician happy
    musician "Thanks. I'll do my best."
    musician "I'll head back to practice now."
    naomi happy "See you!"
    hide musician with moveoutleft
    naomi thinking "(I came to persuade him to play at the cafe.)"
    naomi relieved "(But, I think I'll leave that to after his performance.)"
    $ encounters["musician"] += 1
    $ set_flag("musician_3_seen")
    return

label musician_show:
    $ set_flag("musician_show_seen")
    $ story_flags["musician_show_day"] = totaldays
    scene bg cafeleft with dissolve
    naomi thinking "I'll head to the theatre now for the performance."
    # At theatre
    hide cafetableright
    hide bg caferight
    show bg imperial theatre
    show fans zorder 2
    with fade
    stop music fadeout 3.0
    naomi thinking "It's still early but there are so many people..."
    if flag("pre_musician_event_1"):
        play sound "<from 1 to 6>fangirl.mp3"
        show musician troubled zorder 1 with dissolve:
            xalign 1.0 yalign 0.6 zoom 0.4
        fan "He's here!"
        naomi thinking "What's happening?"
        play sound "<from 1 to 6>fangirl.mp3" fadeout 1.0
        show musician surprised zorder 3 with dissolve:
            xalign 0.8 yalign 1.0 zoom 0.9
        fan "Hideo, we love you!!"
        show musician surprised zorder 3 with dissolve:
            xalign 0.5 yalign 0.5 zoom 1.5
        musician "Naomi!"
        naomi surprised "Hideo?"
        show musician shy2:
            zoom 1.2
        musician "..."
        naomi blush "Wha- Shouldn't you be-"
        show musician shy:
            zoom 1.2
        musician "I, uh... I saved this seat for you."
        window hide
        show ticket_front_new zorder 4:
            xalign 0.6 yalign 0.6 zpos 0 zoom 0.5
            easein 1.0 xalign 0.5 yalign 0.7 zpos 400 zoom 1.0
        pause
        naomi troubled "I already have a-"
        show musician troubled
        musician "I want you to sit here."
        naomi blush "Um, sure! I- I can sit here instead."
        naomi surprised "(This seat is right in the centre!)"
        hide ticket_front_new with moveoutbottom
        $ inventory.update({"ticket_front_new":["Ticket for a seat in the front."]})
        show musician shy2
        play sound "<from 1 to 6>fangirl.mp3" fadeout 1.0
        fan "Hideo!!!"
        fan "Who's that girl?"
        show musician troubled
        musician "I've got to be backstage now."
        naomi blush "I'll be cheering you on!"
        show musician happy
        musician "Thanks."
        play sound "<from 1 to 6>fangirl.mp3" fadeout 1.0
        show musician shy zorder 1 with dissolve:
            xalign 1.0 yalign 0.6 zoom 0.4
        fan "Hideo! We love you!"
        hide musician with dissolve
        naomi blush "(Did he come out just to pass me this?)"
        fan "Hideo? Where did he go??"
        fan "Who's that girl he was talking to?"
        naomi thinking "(Uh oh, I'd better go look for my seat.)"
    # Cutscene
    $ day_display = False
    hide fans
    if flag("pre_musician_event_1"):
        $ inventory.update({"ticket_front_used":["A used ticket for a seat in the front row."]})
        $ del inventory["ticket_front_new"]
        show musician_cutscene_11 with Fade(2.0,0.5,0.5)
        $ persistent.musician_cutscene_1_unlocked = True
    else:
        $ inventory.update({"ticket_back_used":["A used ticket for a seat in the back row."]})
        $ del inventory["ticket_back_new"]
        show black1:
            xalign 0.5 yalign 1.0 #full close
        show black2:
            xalign 0.5 yalign 0.0 #full close
        show musician_cutscene_11:
            zoom 0.4 xalign 0.6 yalign 0.7 matrixcolor BrightnessMatrix(-0.2)
        with Fade(2.0,0.5,0.5)
    play music "<from 0 to 43.5>cello.mp3"
    pause
    naomi surprised "(Hideo?)"
    naomi surprised "(He's usually quiet, but this music.)"
    naomi thinking "(I hear his resolve, his passion.)"
    if flag("pre_musician_event_1"):
        show musician_cutscene_12
        hide window
        pause
        naomi blush "(Is he looking at me?)"
        show musician_cutscene_12 as cutscene_copy at atl_dizzy
        naomi pain "(Ah!)"
        hide musician_cutscene_12
        naomi blush "(Was it just my imagination?)"
        hide window
    else:
        hide black1
        hide black2
    show bg theatre
    show fans zorder 2
    hide musician_cutscene_11
    with Fade(2.0,0.5,2.0)
    stop music fadeout 5.0
    $ day_display = True
    naomi relieved "That was intense."
    naomi happy "I think I can understand now why he has so many fans."
    naomi blush "His face when he's engrossed in his music..."
    if flag("pre_musician_event_1"):
        play sound "<from 1 to 6>fangirl.mp3" fadeout 1.0
        show musician shy zorder 1 with dissolve:
            xalign 1.0 yalign 0.6 zoom 0.4
        fan "He's here!!"
        show musician shy2 zorder 3 with dissolve:
            xalign 0.8 yalign 1.0 zoom 0.9
        play sound "<from 1 to 6>fangirl.mp3" fadeout 1.0
        fan "Hideo, we love you!!"
        show musician happy with dissolve:
            yalign 0.5 xalign 0.5 zoom 1.2
        musician "Thanks for coming."
        naomi blush "Hideo! You did great."
        show musician thinking:
            zoom 1.2
        musician "I was less nervous than I thought."
        show musician happy:
            zoom 1.2
        musician "...Thanks to you."
        naomi surprised "Me?"
        show musician shy2:
            zoom 1.2
        musician "Yeah, I..."
        musician "I was playing just for you."
        naomi blush "(Just for me?)"
        play sound "<from 1 to 6>fangirl.mp3" fadeout 1.0
        fan "Hideo!! We love you!"
        show musician shy2:
            zoom 1.2
        musician "Let's get out of here, I'll walk you back."
        musician "Can you meet me at the back of the theatre?"
        naomi blush "Sure!"
        show musician happy zorder 3 with dissolve:
            xalign 0.8 yalign 1.0 zoom 0.9
        musician "I'll find you later."
        show musician shy zorder 1 with dissolve:
            xalign 1.0 yalign 0.6 zoom 0.4
        play sound "<from 1 to 6>fangirl.mp3" fadeout 1.0
        fan "Hideo!!"
        stop sound fadeout 1.0
        hide musician
    else:
        naomi troubled "His fans are all waiting for him to come out."
        naomi troubled "I should head off quickly."
    #### Back home
    hide fans
    hide bg dancehall
    show bg cafeleft
    with fade
    show cat neutral with moveinbottom
    cat "How was the show?"
    naomi blush "Great."
    show cat eyeroll
    cat "You're besotted."
    hide cat with moveoutbottom
    if flag("pre_musician_event_1"):
        naomi blush "(...He played just for me.)"
    $ musician_event = 2
    if merchant_event == True:
        jump merchant_dance
    else:
        scene bg cafeleft with fade
        naomi sleepy "It's been a long day. I'll head to bed."
        jump evening_time

label musician_5:
    $ set_flag("musician_5_seen")
    $ story_flags["musician_5_day"] = totaldays
    show cafetableright zorder 3.0
    show musician shy with moveinleft:
        xalign 0.5
    musician "...Puddin-."
    show musician surprised
    musician "Naomi."
    naomi relieved "One Pudding à la Mode, yes?"
    show pudding zorder 3.0:
        xalign 0.5 ypos 0.9 zpos 400 zoom 0.5
        easein 1.0 ypos 0.7 zpos 0
    pause
    naomi relieved "Here you go!"
    show musician happy
    musician "Thanks."
    show musician thinking
    musician "You're not at the theatre...?"
    naomi relieved "It's been a while since I saw you there."
    naomi happy "Thought I might run into you here..."
    naomi troubled "Is everything okay?"
    show musician shy
    musician "Yeah, I've been..."
    musician "Working on something."
    naomi happy "Something?"
    show musician shy2
    menu:
        musician "I think... I want to focus on the shamisen."
        "What about the cello?":
            naomi troubled "What about the cello?"
            naomi thinking "After you put in all that effort to master it."
            show musician thinking
            musician "I know it doesn't make sense."
            musician "But I just feel..."
            show musician troubled
            musician "The shamisen. It feels right for me."
            naomi thinking "I see."
            naomi thinking "It's not about the instrument, is it?"
            show musician surprised
            naomi relieved "You're choosing to be yourself."
            show musician happy
            musician "I guess you can say that."
            show musician surprised
            naomi thinking "You're really brave to make this choice."
            naomi happy "I'll be rooting for you."
            show musician shy
            musician "Thanks. I..."
            show musician shy2
            musician "That really means a lot to me."
            image musician glitched2:
                glitch("musician shy")
                pause 0.1
                glitch("musician shy",offset=60,randomkey=None)
                pause 0.1
                glitch("musician shy2")
                pause 0.1
                glitch("musician shy2",offset=60,randomkey=None)
                pause 0.1
                glitch("musician shy2")
                "musician shy2"
            show musician glitched2
            naomi surprised "..."
            $ add_point("musician")
        "That's cool":
            naomi happy "That's cool, I think the shamisen really suits you."
            show musician shy2
            musician "...Yeah."
            naomi happy "I'm sure you'll do great."
            musician "Thanks."
            naomi troubled "(Did I say the wrong thing?)"
    naomi thinking "Oh yes, have you told the orchestra about your decision yet?"
    naomi thinking "They're still wondering why you're skipping rehearsals."
    show musician shy
    musician "Not yet..."
    show musician troubled
    musician "But you're right, I should talk to them."
    naomi relieved "I can come with you, if it's any help."
    show musician surprised
    musician "You would?"
    naomi relieved "Of course! You don't have to do everything alone."
    show musician shy2
    musician "I need to go now, but."
    naomi happy "I'll be at the theatre then."
    show musician happy
    musician "Thanks. I'll see you there."
    hide musician
    hide pudding
    with moveoutleft
    $ encounters["musician"] += 1
    return

label musician_6a:
    show musician surprised:
        xalign 0.5
    musician "You came."
    naomi relieved "I said I would, didn't I?"
    show musician happy
    naomi troubled "You ready for this?"
    show musician shy
    musician "..."
    show musician troubled
    musician "I've been wondering."
    show musician shy
    musician "To leave the orchestra at this point."
    musician "After everything they've taught me."
    show musician troubled
    menu:
        musician "Is it really the right thing to do?"
        "Yes, you don't owe them.":
            naomi thinking "I think you don't have to feel bad for them."
            naomi happy "Look at all the fans you've brought in for them."
            naomi smirk "They couldn't have done it without you."
            show musician thinking
            musician "You're right, it wasn't just one-way."
            show musician happy
            musician "Thanks for supporting me."
        "Not right or wrong.":
            $ add_point("musician")
            naomi troubled "I think there's no easy answer to that."
            naomi troubled "The truth is the orchestra will be inconvenienced if you leave."
            naomi smirk "Ticket sales might be affected too."
            naomi thinking "But at the same time, if the orchestra are people who love music as much as you do..."
            show musician surprised
            naomi happy "I believe they would want to hear your shamisen too."
            show musician thinking
            musician "You're right."
            musician "I have to accept that my decision to leave will hurt them."
            show musician troubled
            musician "But at the same time, this is something I must do."
    naomi happy "You ready?"
    show musician troubled
    musician "Let's go."
    hide bg imperial theatre
    hide musician
    hide window
    show bg imperial theatre
    show musician happy:
        xalign 0.5
    with Fade(2.0,2.0,2.0)
    naomi relieved "That went better than expected."
    show musician thinking
    musician "Yeah, I didn't think they'd ask me to play the shamisen with them."
    show musician shy
    musician "...Thank you."
    naomi surprised "I didn't do anything."
    musician "You were there."
    show musician shy2
    musician "Naomi, I..."
    ticketer "Naomi! Are you coming?"
    show musician shy
    naomi surprised "Yeah!"
    naomi blush "I've got to go."
    naomi happy "Guess I'll be seeing you around here?"
    show musician happy
    musician "Yeah, I'll be here still."
    musician "See you."
    hide musician with moveoutleft
    $ encounters["musician"] += 1
    $ set_flag("pre_musician_event_2")
    return

label musician_6b:
    ticketer "Your cellist friend is back rehearsing with the orchestra."
    naomi troubled "He is?"
    naomi troubled "(Didn't he want to play the shamisen instead?)"
    naomi relieved "(I guess he changed his mind then.)"
    $ encounters["musician"] += 1
    return

label musician_8:
    stop music fadeout 3.0
    $ guy_display = True
    show musician shy2:
        xalign 0.5
    naomi surprised "You're still here?"
    show musician shy
    musician "Yeah..."
    show musician troubled
    musician "Been working on a song, but I can't seem to get it right."
    naomi troubled "Hmm..."
    naomi thinking "Maybe you need a change of pace?"
    naomi happy "Get a different perspective."
    show musician thinking
    musician "A different perspective..."
    show musician shy2
    musician "Are you free this Sunday evening?"
    naomi surprised "Uh... I guess?"
    show musician shy
    musician "There's somewhere I want to go." 
    show musician happy
    musician "For a different perspective."
    musician "Will you come with me?"
    naomi happy "Sure, I'd love to."
    musician "I'll pick you up at the cafe."
    naomi blush "(It sounds like he's asking me out on a date!)"
    naomi blush "Alright."
    musician "See you then."
    $ guy_display = False
    hide musician with moveoutleft
    $ musician_event = 3
    $ encounters["musician"] += 1
    return

label musician_tower:
    # Pickup at cafe
    scene bg cafeleft with dissolve
    show table_left zorder 2.0:
        xalign 1.0 yalign 1.0 zoom 0.5
    show kirako happy with moveinright
    kirako "Hideo's waiting for you, dear."
    naomi blush "I- I'll be right there."
    if naomi_dress == "dress_modern":
        show kirako wink
        kirako "Perfect dress for an evening date."
        naomi blush "..."
    else:
        show kirako angry
        kirako "You're not wearing that to a date, are you? Go change!"
        naomi blush "I'll go change."
        show kirako happy
        kirako "Good girl."
    show kirako wink
    kirako "I'll leave you both to it."
    show kirako happy
    hide kirako with moveoutleft
    hide table_left
    menu:
        "Change clothes":
            naomi thinking "I'll change clothes quickly."
            window hide
            show screen wardrobe
            naomi happy "I'm ready."
        "Meet Hideo":
            naomi happy "I'm ready."
    show bg caferight
    show cafetableright zorder 3.0
    show musician shy:
        xalign 0.5
    with pushleft
    musician "Hey..."
    if naomi_dress == "dress_modern":
        show musician surprised
        musician "..."
        naomi troubled "What's wrong?"
        show musician troubled
        musician "Your kimono..."
        naomi troubled "Should I change? I wasn't sure what to wear since you didn't say-"
        show musician thinking
        musician "It suits you."
        naomi blush "Thank you."
        if get_stage("musician") >= 2:
            naomi blush "Actually, the print reminded me of you..."
            show musician surprised
            naomi smirk "Bold and artistic."
            musician "I..."
            show musician shy
            musician "I'm not sure if that's true."
            naomi happy "You are."
    show musician shy2
    musician "Shall we go?"
    naomi happy "Yes, let's go!"
    # At Ryounkaku
    hide musician
    hide cafetableright
    hide bg caferight
    hide window
    show bg ryounkaku:
        matrixcolor SaturationMatrix(1.2)
    with fade
    pause
    naomi surprised "This view, it's amazing."
    naomi relieved "From here, it feels like the city stretches out endlessly."
    hide window
    show musician shy2 with moveinright:
        xalign 0.9 matrixcolor BrightnessMatrix(-0.1)
    pause
    musician "It feels so free up here."
    show musician happy:
        easein 0.5 xalign 0.5
    musician "Like how I feel when I play."
    naomi happy "That sounds incredible."
    naomi relieved "I wonder how that feels like."
    if naomi_dress == "dress_modern":
        #$ musician_courage += 1
        if get_stage("musician") >= 2:
            show musician shy
            musician "..."
            hide window
            pause
            naomi troubled "Hideo...?"
            musician "I'm... thinking."
            naomi troubled "About your song?"
            show musician shy2
            musician "No, I... I don't know how to say this but."
            musician "You said I'm bold and artistic, but I'm really not."
            musician "I tend to hide myself, my music..."
            musician "But somehow, when I'm with you, I can be myself."
            show musician troubled
            musician "You give me courage."
            naomi blush "..."
            show musician shy
            musician "..."
            musician "Sorry, I know this came out of nowhere."
            musician "Just forget I said all this."
            show musician surprised
            naomi troubled "No!"
            naomi happy "...I'm glad."
            naomi blush "I didn't know you felt that way."
            show musician happy
            naomi happy "Thanks for telling me."
            musician "I'll try to let you know how I feel."
            naomi blush "..."
            musician "You asked how it feels like when I play."
        show musician happy:
            zoom 1.0 yalign 0.0
            easeout 1.5 zoom 2.0 yalign 0.2
        musician "Here, try it."
        naomi surprised "Me? But I can't... I don't even know how to..."
        musician "Like this."
        hide window
        # Cutscene
        show musician_cutscene_2 with Fade(2.0,0.5,0.5)
        pause
        naomi blush "(He's so close!)"
        musician "Just strum it gently."
        naomi blush "Like this?"
        musician "You got it."
        if get_stage("musician") >= 2:
            naomi surprised "This sound..."
            show musician_cutscene_2 as cutscene_copy at atl_dizzy
            if persistent.haptics_enabled:
                $ renpy.vibrate(0.5)
            naomi pain "(Ah!)" with vpunch
            $ musician_dream = True
            hide musician_cutscene_2 with Dissolve(1.0)
            show musician surprised:
                zoom 2.0 yalign 0.2
            musician "Naomi?"
            show musician troubled:
                zoom 2.0 yalign 0.2
            naomi pain "I'm fine."
            naomi troubled "(That sound... Where have I heard it before?)"
            show musician troubled:
                zoom 2.0 yalign 0.2
                easein 1.0 zoom 1.5 yalign 0.15
            musician "You look pale."
            musician "I'll take you home."
        else:
            hide musician_cutscene_2 with Dissolve(1.0)
            show musician happy:
                zoom 2.0 yalign 0.2
            musician "I think you have the talent for this."
            naomi blush "You're joking."
            show musician shy
            musician "It's getting dark."
            show musician happy
            musician "Let's head back."
    else:
        show musician shy
        musician "It's getting dark."
        musician "Let's head back."
    # Back home
    hide bg ryounkaku
    hide musician
    show bg bedroom
    with fade
    show cat neutral with moveinbottom
    if naomi_dress == "dress_modern":
        cat "Back already?"
        if get_stage("musician") >= 2:
            naomi troubled "I had a dizzy spell."
            show cat eyeroll
            cat "Huh, again."
            show cat happy
            cat "Sweet dreams."
        else:
            naomi troubled "It was getting dark."
            show cat eyeroll
            cat "Huh."
        hide cat with moveoutbottom
        naomi blush "(He was so close...)"
    else:
        cat "Back already?"
        naomi troubled "It was getting dark."
        cat "Huh."
        show cat huff
        cat "Sometimes what you wear changes the mood."
        hide cat with moveoutbottom
        naomi thinking "(Would it have been different?)"
    $ musician_ending = True
    $ musician_event = False
    call screen bedroom

label theatre_ending:
    play music "<from 135 to 155>cello.mp3"
    naomi happy "I guess this is where I'll be working from now on."
    naomi thinking "I achieved my goal of finding a job within these two weeks."
    naomi troubled "Why does it feel like I'm missing something important?"
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
    $ renpy.full_restart()