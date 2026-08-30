label imperial_theatre:

    scene bg imperial theatre
    play music "<from 246>cello.mp3" fadein 3 if_changed

    $ location_visits["theatre"] += 1

    ## Post-show disappearance
    $ days_since_show = story_flags.get("musician_show_day", -9999) - totaldays

    $ musician_next = get_musician_action()
    if musician_next:
        call expression musician_next from _call_musician_encounter
    else:
        if days_since_show >= 4 and not flag("musician_ticketer_talk_seen"):
            ticketer "Are you the girl from the cellist's cafe?"
            ticketer "I heard he's been skipping rehearsals."
            naomi surprised "You mean Hideo?"
            ticketer "Yes. If you see him, tell him the orchestra is waiting for him."
            naomi happy "Sure, I'll pass on the message."
            naomi troubled "(Come to think of it, I haven't seen him here lately...)"
            naomi troubled "(Perhaps he might drop by the cafe instead.)"
            $ set_flag("musician_ticketer_talk_seen")
        elif 0 < days_since_show < 4:
            show fans_less with dissolve
            fan "The orchestra came out during their break, but I didn't see Hideo."
            fan "I waited since early this morning, but he didn't appear either."
            naomi troubled "(I wonder where Hideo's been. It looks like his fans haven't spotted him lately.)"
            hide fans_less with dissolve
        else:
            if encounters["musician"] <= 2:
                show fans_less
                naomi thinking "(Hideo's fans are staking out for him again.)"
                fan "I heard the tickets for Saturday's performance are all sold out."
                fan "As expected of Hideo-sama."
                fan "I can't wait to hear his cello solo."
                naomi thinking "(So he plays the cello.)"
                naomi troubled "(But, what's that instrument he's always carrying around?)"
                hide fans_less with dissolve
                naomi thinking "(Nothing left for me to do here.)"
            if 3 < encounters["musician"] <= 4:
                show fans_less
                fan "Someone said she saw Hideo leave the building."
                naomi thinking "(Looks like I missed him this time.)"
                naomi happy "Hideo's favourite pudding, come get yours!"
                fan "Is this from the rumoured cafe?"
                naomi happy "Yes, Hideo's a regular at the Cafe Diamond in Asakusa!"
                naomi happy "This is his favourite pudding."
                fan "I'll have one pudding, please!"
                naomi thinking "(The pudding is popular, and Hideo even more so!)"
                fan "Oh, the same flavor as Hideo-sama!"
                fan "I'll have a pudding too, please!"
                naomi troubled "I'm sorry, we are out of pudding."
                naomi happy "But you can visit us in Asakusa. You might run into Hideo himself!"
                fan "A chance to run into Hideo? Let's visit that cafe!"
                naomi happy "(Good. More business for the cafe.)"
            if encounters["musician"] > 4:
                show fans_less
                naomi happy "Pudding from the Cafe Diamond! It's Hideo's favorite pudding."
                fan "I'll have one!"
                fan "I'll pass this time."
                hide fans_less with dissolve
                naomi thinking "(Sales were a little less today.)"

    $ timeslot -= 1

    ## Check if morning or afternoon
    if timeslot == 1:
        naomi thinking "(Where should I go next?)"
        stop music fadeout 5
        jump ginza_small
    if timeslot < 1:
        naomi relieved "I'll head home now."
        stop music fadeout 5
        jump evening_time

label musician_0:
    show cafetableright zorder 3.0
    show musician shy with dissolve:
        xalign 0.5
    $ musician_name = "???"
    naomi thinking "..."
    musician "..."
    naomi surprised "(Oh! A customer.)"
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
    musician "Just every now and then."
    show musician happy
    musician "When I feel like having pudding."
    naomi happy "(He must like the pudding here.)"
    show musician shy2
    musician "...But it's been quieter lately."
    naomi surprised "Is that so?"
    musician "Yeah, well."
    musician "It's how things are."
    show musician shy
    musician "A new cafe opens, some customers go there."
    naomi thinking "(So there's been competition from other cafes.)"
    naomi happy "You're still here, though."
    show musician happy
    musician "...The pudding's better here."
    naomi relieved "(He really likes the pudding.)"
    naomi relieved "Any ideas how we could get more customers in?"
    show musician thinking
    musician "..."
    musician "More customers.. It's tough."
    naomi troubled "It's fine, you don't have t-"
    show musician shy2
    musician "Well, there's the theatre crowd."
    naomi surprised "Theatre crowd?"
    show musician shy
    musician "After a show, people look for somewhere to go."
    show musician thinking
    musician "...I perform at the Imperial Theatre. In Ginza."
    naomi thinking "(Ginza is a little far. But if he came here just for pudding...)"
    naomi angry "(It's worth looking into.)"
    naomi happy "Thank you for the suggestion, I'll talk to the owner."
    naomi thinking "(I should get his name at least.)"
    naomi happy "By the way, I'm Naomi. You are...?"
    show musician shy
    musician "...Hideo."
    naomi relieved "Nice to meet you, Hideo."
    $ musician_name = "Hideo"
    show musician happy
    musician "Nice meeting you too, Naomi."
    hide musician
    hide pudding_no
    hide pudding_cherry
    with dissolve
    naomi thinking "(The Imperial Theatre.)"
    naomi thinking "(I should go and have a look.)"
    $ story_flags["musician_0_day"] = totaldays
    $ unlock_imp_th = True
    return

label musician_1:
    show fans_less
    naomi happy "So this is the Imperial Theatre... It's grand!"
    naomi thinking "I hear music from behind the doors."
    naomi pain "Such a lovely music."
    naomi thinking "I wonder what upcoming performances there are."
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
    naomi thinking "I need a plan to get these fans to our cafe."
    $ story_flags["musician_1_day"] = totaldays
    $ encounters["musician"] += 1
    return

label musician_2:
    $ encounters["musician"] += 1
    show musician shy with dissolve:
        xalign 0.5
    naomi thinking "(How do I get Hideo's fans to Cafe Diamond?)"
    naomi surprised "Oh, sorry!"
    naomi happy "Pudding, yes?"
    window hide
    show pudding zorder 3.0:
        xalign 0.5 ypos 0.9 zpos 400 zoom 0.5
        easein 1.0 ypos 0.7 zpos 0
    pause
    show musician thinking
    musician "You're distracted."
    naomi blush "...I was thinking how to bring the theatre crowd to the cafe."
    musician "..."
    musician "How about if you brought the cafe to the theatre?"
    naomi surprised "Cafe to the theatre?"
    show musician shy
    musician "Yeah..."
    show musician thinking
    musician "Some pudding during breaks would be nice."
    naomi smirk "You just want to eat pudding, don't you?"
    show musician happy
    musician "You caught me."
    hide musician
    hide pudding
    with dissolve
    naomi thinking "(But still, it's an idea.)"
    naomi thinking "(I'll bring some pudding when I visit the theatre.)"
    return

label musician_3:
    show fans_less
    $ encounters["musician"] += 1
    naomi thinking "(Hideo's fans are here as usual.)"
    naomi thinking "(I've brought the puddings from the cafe.)"
    naomi happy "Hello! Would you like to give Hideo's favourite pudding a try?"
    fan "Hideo's favourite pudding?"
    naomi happy "Yes, Hideo's a regular at the Cafe Diamond in Asakusa!"
    naomi happy "This is his favourite pudding."
    fan "Tasting the same flavor as Hideo-sama? Give me one!"
    fan "A pudding, please!"
    fan "I'll have a pudding too, please!"
    naomi troubled "I'm sorry, we are out of pudding."
    naomi happy "But you can visit us in Asakusa. You might run into Hideo himself!"
    fan "A chance to run into Hideo? Let's visit that cafe!"
    fan "He might have gone there. Let's go now!"
    naomi happy "(Good. More business for the cafe.)"
    menu:
        naomi thinking "(I should guide these customers to the cafe, but this music...)"
        "Guide the customers":
            naomi happy "Please follow me, I will bring you to the cafe."
            fan "Lead the way!"
            scene bg caferight
            show fans_less
            show cafetableright zorder 3.0
            with dissolve
            fan "Pudding, please!"
            naomi happy "Coming right up!"
            show pudding zorder 3.0:
                xalign 0.5 ypos 0.9 zpos 400 zoom 0.5
                easein 1.0 ypos 0.7 zpos 0
            fan "The food is delicious!"
            fan "I'll come again to see if I can catch Hideo."
            naomi thinking "(Good, my strategy is working out.)"
            naomi thinking "(I'll visit the theatre again to get more fans here.)"
            naomi happy "Thank you for your patronage!"
            hide fans_less
            hide pudding
            with dissolve
            show kirako happy with dissolve
            kirako "Thank you for your help Naomi!"
            show kirako pout
            kirako "Is it just me, or was the cafe busier today?"
            $ tips = renpy.random.randint(10, 15)
            $ money += tips
            show kirako happy
            kirako "Here you go, [tips] yen in tips today."
            
            # Deduct timeslot and check if morning or afternoon
            $ timeslot -= 1
            if timeslot == 1:
                naomi happy "Thank you!"
                hide kirako with dissolve
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
        "Listen to music":    
            hide fans_less with dissolve
            naomi sleepy "(I'll just listen for a while.)"
            stop music fadeout 3
            window hide
            show musician thinking:
                xalign 0.5
            with dissolve
            pause
            musician "...Naomi?"
            naomi surprised "Hideo!"
            musician "What are you doing here?"
            naomi happy "I came to promote the cafe, like you suggested."
            show musician shy
            musician "I see. How did it go?"
            naomi happy "I think it worked! People are heading to the cafe."
            naomi thinking "I brought your favourite pudding, and it was a hit."
            naomi troubled "It sold out within minutes... Sorry."
            show musician happy
            musician "It's alright, I'm glad for the cafe."
            musician "I've got to get back to practice now."
            musician "Bring extra for me next time."
            hide musician with dissolve
            play music "<from 246>cello.mp3"
            naomi happy "We're off to a promising start."
            naomi thinking "I'll just have to keep coming with the puddings."
            $ add_point("musician")
            return


label musician_4:
    show cafetableright zorder 3.0
    show musician shy with dissolve:
        xalign 0.5
    naomi happy "Hi! The usual?"
    musician "Yes, please."
    window hide
    show pudding zorder 3.0:
        xalign 0.5 ypos 0.9 zpos 400 zoom 0.5
        easein 1.0 ypos 0.7 zpos 0
    pause
    naomi happy "I've been meaning to ask, what's that you're always carrying?"
    show musician surprised
    musician "...This?"
    show musician shy
    musician "A shamisen."
    naomi happy "Do you play that in the orchestra?"
    musician "Nah, it doesn't fit in an orchestra."
    musician "I play the cello now."
    menu:
        "Ask about cello":
            naomi thinking "I see."
            naomi happy "When did you pick up the cello?"
            musician "Just about half a year back."
            naomi surprised "Half a year?"
            naomi thinking "(Unthinkable given his level of mastery.)"
            naomi thinking "You must have worked very hard at it."
            show musician happy
            musician "Yeah, it was difficult."
        "Ask about shamisen":
            naomi thinking "Why do you carry it around then?"
            show musician shy2
            musician "...I'm just used to having it with me."
            naomi thinking "(It means enough to him that he carries it with him.)" 
            show musician surprised
            naomi relieved "I'd love to hear you play the shamisen someday."
            show musician shy
            musician "...Maybe someday."
            $ add_point("musician")
    hide musician
    hide pudding
    with dissolve
    return

label musician_5:
    stop music fadeout 3.0
    show fans_less
    $ encounters["musician"] += 1
    naomi happy "Pudding from the Cafe Diamond! It's Hideo's favorite pudding."
    fan "The pudding! I want one."
    naomi happy "Here you go! Come visit our cafe in Asakusa!"
    fan "I visited, but Hideo wasn't there."
    fan "Is this really Hideo's favorite pudding?"
    naomi troubled "(People are doubting.)"
    naomi thinking "(I need to create an opportunity for them to see Hideo at the cafe...)"
    play music "<from 135 to 155>cello.mp3"
    fan "Hush! Hideo is playing."
    naomi thinking "..."
    naomi surprised "(This music!)"
    show bg imperial theatre as theatre_copy at atl_dizzy
    if persistent.haptics_enabled:
        $ renpy.vibrate(0.5)
    naomi pain "(It makes me feel...)" with vpunch
    naomi troubled "(What was that?)"
    naomi troubled "..."
    naomi surprised "(Around me, people are stopping to listen.)"
    naomi happy "That's it!"
    naomi happy "If I can get Hideo to play at the cafe, people will come."
    naomi thinking "Now I need to convince Hideo to help."
    return


label musician_6:
    show cafetableright zorder 3.0
    show musician shy with dissolve:
        xalign 0.5
    naomi happy "Welcome back!"
    show musician shy2
    musician "Thanks. The usual, please."
    naomi happy "Coming right up!"
    window hide
    show pudding zorder 3.0:
        xalign 0.5 ypos 0.9 zpos 400 zoom 0.5
        easein 1.0 ypos 0.7 zpos 0
    pause
    naomi relieved "Here you go!"
    show musician happy
    naomi thinking "(I need his help for the cafe.)"
    menu:
        naomi thinking "(How should I ask him?)"
        "It would help the cafe":
            naomi troubled "Actually, I wanted to ask you something."
            naomi troubled "Would you consider playing here sometime? It would really bring in customers."
            show musician surprised
            musician "...Here?"
            naomi relieved "Just once, even. The theatre crowd already knows your name."
            show musician thinking
            musician "..."
            musician "The cello doesn't work well on its own."
            musician "It needs an orchestra to be complete."
        "Your music moved me":
            $ add_point("musician")
            naomi troubled "Actually, I wanted to ask you something."
            naomi troubled "I was listening to your music at rehearsal."
            naomi relieved "And it moved me, somehow."
            naomi happy "Would you play something like that here? Just for us?"
            show musician surprised
            musician "...Here?"
            naomi happy "It wouldn't have to be anything big."
            show musician thinking
            musician "..."
            musician "The cello doesn't work well on its own."
            musician "It needs an orchestra to be complete."
            show musician troubled
            musician "...Sorry."
    naomi thinking "(He didn't say no, but he seems reluctant.)"
    show musician shy2
    musician "I should head back."
    naomi happy "Thanks for stopping by."
    hide musician
    hide pudding
    with dissolve
    naomi thinking "I don't want to be pushy, but I do hope he can help."
    return

label musician_7:
    show fans_less
    $ encounters["musician"] += 1
    naomi happy "Pudding from the Cafe Diamond!"
    fan "I'll have a pudding, please."
    naomi happy "Here you go! Come visit our cafe!"
    stop music fadeout 3.0
    hide fans_less with dissolve
    naomi troubled "(There's pudding left over this time.)"
    naomi troubled "(I've got to think of something else to get people to come.)"
    show musician shy:
        xalign 0.5
    with dissolve
    pause
    musician "You're here again."
    naomi happy "There's pudding left over this time."
    show musician happy
    musician "Just what I need right now."
    naomi happy "How is your rehearsal going?"
    show musician shy
    musician "Still some parts I'm not happy with..."
    musician "How is the cafe's business?"
    naomi troubled "Better than before, but I need to keep the momentum going."
    show musician thinking
    musician "Huh."
    naomi smirk "Some music might be nice."
    show musician shy2
    musician "Not the cello."
    menu:
        naomi thinking "(How should I convince him?)"
        "Just a fan meet then?":
            naomi happy "What if it's just a fan meet then?"
            show musician thinking
            musician "..."
            musician "I don't think anyone will come."
            naomi thinking "Really?"
            naomi thinking "I overheard your fans."
            naomi smirk "They went to the cafe looking for you."
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
            musician "Now that I perform the cello, I don't play it so much."
    naomi relieved "You don't have to decide now."
    naomi happy "Just think about it."
    show musician shy
    musician "...Alright."    
    musician "I've got to head back."
    naomi happy "See you at the cafe."
    hide musician with dissolve
    play music "<from 246>cello.mp3"
    naomi troubled "I hope I wasn't too pushy."
    return

label musician_8:
    show fans_less
    naomi happy "Pudding from the Cafe Diamond!"
    fan "I'll pass, thanks."
    fan "Maybe next time."
    stop music fadeout 3.0
    hide fans_less with dissolve
    naomi troubled "(More pudding left over this time.)"
    show musician shy:
        xalign 0.5
    with dissolve
    pause
    naomi surprised "Hideo!"
    naomi relieved "Good news, there's extra pudding."
    show musician shy
    musician "...I'm not hungry right now."
    naomi angry "(He doesn't want pudding?)"
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
    $ set_flag("musician_6_seen")
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
    if flag("pre_musician_event_1"):
        show musician shy2:
            xalign 0.5
        show table_left:
            xalign 1.0 yalign 1.0 zoom 0.5
        naomi troubled "(He was quiet on the way back, like his mind was elsewhere.)"
        naomi troubled "...Hideo?"
        show musician troubled
        musician "..."
        show musician shy
        musician "...Thanks again for coming to the show."
        menu:
            naomi thinking "(Should I probe?)"
            "Leave it":
                naomi happy "Come by for celebratory pudding!"
                show musician happy
                musician "Yeah. I will."
            "Ask him":
                $ add_point("musician")
                naomi troubled "You seem distracted. Is something bothering you?"
                show musician shy2
                musician "...Just thinking."
                naomi surprised "About the show?"
                show musician shy
                musician "Not really."
                musician "..."
                naomi relieved "It's alright, you don't have to say it now."
                naomi happy "If you need someone to talk to, you know where to find me."
                show musician happy
                musician "Thanks."
    hide musician with dissolve
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

label musician_9:
    $ set_flag("musician_5_seen")
    $ story_flags["musician_9_day"] = totaldays
    show cafetableright zorder 3.0
    show musician shy with dissolve:
        xalign 0.5
    musician "...Puddin-."
    naomi relieved "One Pudding à la Mode, yes?"
    show pudding zorder 3.0:
        xalign 0.5 ypos 0.9 zpos 400 zoom 0.5
        easein 1.0 ypos 0.7 zpos 0
    pause
    naomi relieved "Here you go!"
    show musician shy2
    musician "Thanks."
    naomi relieved "It's been a while since I ran into you at the theatre."
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
            show musician shy
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
    with dissolve
    return

label musician_9a:
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
    naomi blush "..."
    show musician shy2 zorder 2
    musician "Naomi, I..."
    show fans_less with dissolve
    fan "Hideo's here!"
    show fans with dissolve
    fan "Hideo-sama! We love you!"
    show musician shy
    musician "...It's getting crowded here."
    naomi pain "(Is he not aware of his own popularity?)"
    naomi thinking "Let's head back to the cafe first."
    $ encounters["musician"] += 1
    $ set_flag("pre_musician_event_2")
    scene bg caferight
    show musician shy:
        xalign 0.5
    show cafetableright zorder 3.0
    with dissolve
    naomi happy "First, pudding to celebrate!"
    show pudding zorder 3.0:
        xalign 0.5 ypos 0.9 zpos 400 zoom 0.5
        easein 1.0 ypos 0.7 zpos 0
    show musician happy
    musician "Somehow the pudding tastes better than usual."
    naomi happy "(Good, he looks like the weight lifted off him.)"
    show musician shy
    musician "...I've been thinking."
    musician "This might be a good place for me to start."
    naomi troubled "Start?"
    show musician troubled
    musician "With the shamisen."
    musician "Perform some nights, here in the cafe."
    naomi surprised "Performing in the cafe?"
    show musician shy
    musician "If the owner allows, of course."
    naomi happy "Finally!"
    naomi relieved "All this time I've just been waiting for you to be ready."
    image musician glitched3:
        glitch("musician shy2")
        pause 0.1
        glitch("musician shy2",offset=60,randomKey=None)
        pause 0.1
        glitch("musician shy2")
        pause 0.1
        "musician shy2"
    show musician glitched3
    musician "Thank you, for waiting for me."
    show bg caferight as cutscene_copy at atl_dizzy
    if persistent.haptics_enabled:
        $ renpy.vibrate(0.5)
    naomi pain "Ah!" with vpunch
    show musician troubled
    musician "Are you alright?"
    naomi troubled "...I think so."
    show musician thinking
    musician "You'd better rest, or see the doctor."
    naomi relieved "I'll be fine after some rest."
    naomi happy "More importantly, let's set a date for your first performance."
    show musician shy
    musician "...I'm still working on a song."
    naomi surprised "An original?"
    show musician shy2
    musician "...Yes."
    naomi happy "That's amazing."
    show musician happy
    musician "You'll have to wait a little more."
    naomi happy "I'm sure it's worth the wait."
    hide musician
    hide pudding
    with dissolve
    show kirako happy with dissolve
    kirako "Thank you for your help Naomi!"
    show kirako pout
    kirako "Is it just me or business has dipped again?"
    naomi troubled "It has."
    naomi thinking "But, I have an idea."
    naomi happy "Music some nights, a different crowd. What do you think?"
    kirako "Oh darling. That sounds lovely!"
    show kirako happy
    kirako "You're still young, do what makes you happy!"
    naomi thinking "(I'll take that as a yes.)"
    $ tips = renpy.random.randint(10, 15)
    $ money += tips
    show kirako happy
    kirako "Here you go, [tips] yen in tips today."
    $ story_flags["musician_8_day"] = totaldays
    
    # Deduct timeslot and check if morning or afternoon
    $ timeslot -= 1
    if timeslot == 1:
        naomi happy "Thank you!"
        hide kirako with dissolve
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
    return

label musician_9b:
    ticketer "Your cellist friend is back rehearsing with the orchestra."
    naomi troubled "He is?"
    naomi troubled "(Didn't he want to play the shamisen instead?)"
    naomi relieved "(I guess he changed his mind then.)"
    $ encounters["musician"] += 1
    return

label musician_11:    
    show musician shy2:
        xalign 0.5
    show cafetableright zorder 3.0
    with dissolve
    naomi happy "How's the song coming along?"
    show musician thinking
    musician "Not progressing."
    naomi surprised "Eh?"
    show musician troubled
    musician "There's a part I can't seem to get right."
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
    hide musician with dissolve
    $ musician_event = 3
    return

label musician_tower:
    $ story_flags["musician_8_day"] = totaldays
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

label musician_12:
    $ set_flag("musician_cafe_show_seen")
    $ story_flags["musician_cafe_show_day"] = totaldays
    show musician shy2:
        xalign 0.85 zoom 0.6 yalign 0.6
    show fans
    show cafetableright zorder 2.0
    fan "One pudding please!"
    naomi happy "Coming right up!"
    naomi thinking "(Word got around about tonight's performance.)"
    show kirako happy with moveinleft
    kirako "Is it just me or is the cafe fuller tonight?"
    fan "One pudding please!"
    naomi happy "Coming right up!"
    hide kirako with moveoutleft
    show musician shy:
        xalign 0.85 zoom 0.6 yalign 0.6
    fan "This is different from the cello... But I like this better!"
    fan "I didn't think the shamisen could be this cool."
    fan "Hideo-sama!"
    naomi thinking "(This tune...)"
    naomi happy "(It's the one he was working on.)"
    naomi troubled "(But why do I feel like I have heard this before...?)"
    show musician troubled:
        xalign 0.85 zoom 0.6 yalign 0.6
    show bg caferight as cutscene_copy at atl_dizzy
    if persistent.haptics_enabled:
        $ renpy.vibrate(0.5)
    naomi pain "(I know this tune!)" with vpunch
    show musician surprised:
        xalign 0.85 zoom 0.6 yalign 0.6
    fan "Bravo! Hideo-sama!"
    fan "Encore!"
    naomi happy "Bravo, Hideo!"
    show musician happy:
        xalign 0.85 zoom 0.6 yalign 0.6
    musician "Thank you for listening."
    hide fans
    show musician troubled:
        xalign 0.5 zoom 1.0 yalign 0.5
    with dissolve
    musician "Was it okay?"
    naomi happy "It was more than okay."
    naomi relieved "You wrote that yourself, didn't you."
    show musician shy
    musician "..."
    if relationship_points["musician"] >= 4:
        jump musician_ending_irl
    else:
        jump musician_ending
    return

label musician_ending_irl:
    naomi happy "Hideo?"
    show bg caferight as cutscene_copy at atl_dizzy
    if persistent.haptics_enabled:
        $ renpy.vibrate(0.5)
    naomi pain "Ah!" with vpunch
    show musician shy
    musician "You helped me to be true to myself."
    show musician troubled
    musician "It's my turn to help you remember who you are."
    naomi troubled "Who I am?"
    musician "Listen."
    naomi thinking "This sound..."
    naomi surprised "It's from my dream!"
    show bg caferight as bg_copy at atl_dizzy
    image musician glitched4:
        glitch("musician troubled")
        pause 0.1
        glitch("musician troubled",offset=60,randomKey=None)
        pause 0.1
        glitch("musician troubled")
        pause 0.1
        "musician troubled"
    show musician glitched4
    naomi pain "Ngh!" with vpunch
    musician "Come back, Naomi."
    hide cafetableright
    show black1:
        xalign 0.5 yalign 1.0 #full close
    show black2:
        xalign 0.5 yalign 0.0 #full close
    hide window
    with Pixellate(2.0,5)
    show text "{color=#ffffff}'Naomi.'{/color}":
        xalign 0.5 yalign 0.8
    pause
    show text "{color=#ffffff}This music...{/color}":
        xalign 0.5 yalign 0.8
    pause
    show musician shy zorder 2
    show text "{color=#ffffff}Hideo.{/color}" zorder 3:
        xalign 0.5 yalign 0.8
    with dissolve
    pause
    hide text
    show text "{color=#ffffff}A classmate who seemed aloof, until one day.{/color}" zorder 3:
        xalign 0.5 yalign 0.8
    with dissolve
    pause
    show musician happy zorder 2:
        zoom 1.0 xalign 0.8 yalign 0.0
        ease 2.0 xalign 0.9 ypos 0.0 zoom 1.2
    show text "{color=#ffffff}'Everyone makes mistakes starting out.'{/color}" zorder 3:
        xalign 0.1 yalign 0.25
    with dissolve
    pause
    hide text
    show text "{color=#ffffff}I discovered his kindness.{/color}" zorder 3:
        xalign 0.5 yalign 0.8
    with dissolve
    pause
    hide text
    show text "{color=#ffffff}I wanted to encourage him too.{/color}" zorder 3:
        xalign 0.5 yalign 0.8
    with dissolve
    pause
    show musician shy2  zorder 2:
        zoom 1.0 xalign 0.1 yalign 0.0
        ease 2.0 xalign 0.1 ypos 0.0 zoom 1.2
    show text "{color=#ffffff}'That really means a lot to me.'{/color}" zorder 3:
        xalign 0.8 yalign 0.2
    with dissolve
    pause
    hide text
    show text "{color=#ffffff}He was often shy to say how he felt, but.{/color}" zorder 3:
        xalign 0.5 yalign 0.8
    with dissolve
    pause
    show musician troubled zorder 2:
        zoom 1.2 xalign 0.65 yalign 0.0
        ease 2.0 zoom 1.5 yalign 0.1
    show text "{color=#ffffff}'You give me courage.'{/color}" zorder 3:
        xalign 0.1 yalign 0.25
    with dissolve
    pause
    hide text
    show text "{color=#ffffff}I was happy when he told me that.{/color}" zorder 3:
        xalign 0.5 yalign 0.8
    with dissolve
    pause
    show bg irl
    show black1 zorder 2:
        xalign 0.5 yalign 1.0 #full close
        easein 3.5 yalign 1.3 #part open
        pause 0.5
        easeout 2.5 yalign 3.5 #full open
    show black2 zorder 2:
        xalign 0.5 yalign 0.0 #full close
        easein 3.5 yalign -0.3 #part open
        pause 0.5
        easeout 2.5 yalign -2.5 #full open
    show text "{color=#ffffff}Hideo.{/color}" zorder 3:
        xalign 0.5 yalign 0.8
        pause 3.5
        easeout 3 alpha 0.0
    show musician troubled zorder 1:
        zoom 2.0 yalign 0.0 xalign 0.1 xzoom -1.0
    pause
    hide black1
    hide black2
    hide text
    show musician troubled:
        zoom 2.0 yalign 0.0 xalign 0.1
        easein 0.5 zoom 2.5 yalign 0.05 xpos -0.1
    show text "{color=#000000}'Naomi?'{/color}" zorder 3:
        xalign 0.7 yalign 0.8 alpha 1.0
    pause
    show musician surprised:
        zoom 2.5 yalign 0.05 xpos -0.1
    show text "{color=#000000}'You're awake!'{/color}" zorder 3:
        xalign 0.7 yalign 0.8
    pause
    show text "{color=#000000}I was asleep?{/color}" zorder 3:
        xalign 0.9 yalign 0.8
    pause
    show musician troubled:
        zoom 2.5 yalign 0.05 xpos -0.1 xzoom -1.0
    show text "{color=#000000}'You've been unconscious for two days.'{/color}" zorder 3:
        xalign 0.8 yalign 0.8
    pause
    show text "{color=#000000}Two...{/color}" zorder 3:
        xalign 0.9 yalign 0.8
    pause
    show musician troubled:
        zoom 2.5 yalign 0.05 xpos -0.1 xzoom -1.0
    show text "{color=#000000}'Rest. I'll go get the doctor.'{/color}" zorder 3:
        xalign 0.85 yalign 0.8
    pause
    show black1 zorder 2:
        xalign 0.5 yalign 3.5 #full open
        easein 3.5 yalign 1.3 #part open
        pause 0.5
        easeout 2.5 yalign 1.0 #full close
    show black2 zorder 2:
        xalign 0.5 yalign -2.5 #full open
        easein 3.5 yalign -0.3 #part open
        pause 0.5
        easeout 2.5 yalign 0.0 #full close
    pause
    show text "{color=#ffffff}A few months later, when I had recovered enough...{/color}":
        xalign 0.5 yalign 0.5
    pause
    hide black1
    hide black2
    hide musician
    hide text
    show musician_cutscene_3
    with Fade(2.0,0.5,0.5)
    pause
    show black1:
        xalign 0.5 yalign 1.0 #full close
    show black2:
        xalign 0.5 yalign 0.0 #full close
    show text "{color=#ffffff}Thank you for playing!{/color}":
        xalign 0.5 yalign 0.5
    with Fade(2.0,0.5,0.5)
    pause
    $ renpy.full_restart()


label musician_ending:
    show musician shy2:
        xalign 0.5 zoom 1.0 yalign 0.5
        linear 0.5 xalign 0.9 zoom 1.0 yalign 0.5
    show kirako happy with moveinleft:
        xalign 0.2
    kirako "Well! I don't know what that was, but I liked it."
    kirako "We should have you back."
    show musician shy2
    musician "...Maybe."
    kirako "And since we'll still be in business."
    show kirako pout
    kirako "Naomi dear, stay with us please!"
    naomi happy "I'll be happy to."
    show kirako happy
    kirako "Lovely!"
    show kirako wink
    kirako "The night is still young, darlings!"
    hide kirako with moveoutleft
    show musician shy:
        xalign 0.9 zoom 1.0 yalign 0.5
        linear 0.5 xalign 0.5 zoom 1.0 yalign 0.5
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

