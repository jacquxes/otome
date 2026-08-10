label hospital:

    # First visit to the hospital
    if encounters["doctor"] == 1:
        call doctor_2
    
    image clinic =  Transform("images/doctor/clinic.png",zoom=0.5)

    scene clinic

    if doctor_ending == True:
        if doctor_courage > 2:
            jump doctor_final_irl
        else:
            jump doctor_final_not
    if totaldays == 0:
        jump hospital_ending

    # Third visit to the hospital
    if doctor_job == 3:
        call doctor_4

    if doctor_job == 6:
        call doctor_6

    if doctor_job == 8 and totaldays > 3:
        call doctor_7

    show doctor happyside:
        xalign 0.5 yalign 0.0 zoom 1.0
    doctor "Here are the patient notes."
    doctor "If you can't read my handwriting, look for me."
    show paperstack:
        xpos 0.4 ypos 0.5 zpos 0 zoom 0.5
        easein 1.0 xpos 0.4 ypos 0.55 zpos 800
    naomi relieved "Alright!"

    if doctor_job == 4:
        call doctor_5

    show doctor happyside:
        xzoom -1.0 zoom 1.0
    doctor "See you later."
    hide doctor with moveoutright
    show clinic:
        easein 5.0 xalign 0.28 yalign 0.58 zoom 4.0
    show time:
        xalign 0.5 yalign 0.5
        ease 1.0 rotate 45
        ease 1.0 rotate -45
        ease 1.0 rotate 0
    naomi thinking "..."
    hide time
    hide paperstack
    naomi sleepy "Somehow managed to decipher his handwriting."
    naomi happy "I'll go find nurse and give her this."
    hide bg clinic with dissolve
    show bg hospital
    with dissolve
    if doctor_job == 2:
        call doctor_3
    show nurse relieved:
        xalign 0.5 ypos 0.1 xzoom -1.0
    with moveinleft
    nurse "Done?"
    show nurse sigh
    naomi relieved "Yes! Here you go."
    show paperstack:
        xpos 0.3 ypos 0.55 zpos 800
        easein 1.0 xpos 0.4 ypos 0.7 zpos 0 zoom 0.5
    $ salary = renpy.random.randint(10, 20)
    $ money += salary
    show nurse relieved
    nurse "Here's [salary] yen for today's work."

    if doctor_job == 4:
        show nurse happy
        nurse "I'm grateful for your help, Naomi."
        nurse "Since you've been doing the paperwork, I've been less tired."
        naomi happy "Glad to be of help."
        if doctor_courage > 1:
            show nurse relieved
            nurse "Hmm, I haven't had to console Dr Yumoto's patients lately too."
            nurse "How strange."
            naomi relieved "Ahaha."
    
    # Deduct timeslot and check if morning or afternoon
    $ timeslot -= 1
    if timeslot == 1:
        nurse "Do you want to work the afternoon too?"
        menu:
            "Work the afternoon":
                naomi happy "Sure, I'll stay for the afternoon."
                nurse "Go get the notes then."
                hide nurse
                hide paperstack
                with moveoutright
                $ doctor_job += 1
                jump hospital
            "Go out":
                naomi relieved "No, I'll head off now."
                nurse "Off you go then!"
                hide nurse
                hide paperstack
                with moveoutright
                $ doctor_job += 1
                jump ginza_small
    if timeslot < 1:
        nurse "Off you go now!"
        hide nurse
        hide paperstack
        with moveoutright
        $ doctor_job += 1
        jump evening_time

# Affection GET 0-1
label doctor_2:
    scene bg hospital
    $ encounters["doctor"] += 1
    show doctor thinking:
        xalign 0.8 yalign 1.0
    show nurse angry:
        xalign 0.2 xzoom -1.0 ypos 0.1
    nurse "Dr Yumoto, you can't say that to his mother!"
    doctor "...But it's true."
    show nurse sigh
    nurse "We're already shorthanded, I don't have time for this!"
    show nurse angry:
        xalign 0.2 ypos 0.1 xzoom 1.0 zoom 1.0
    nurse "Please reflect on what you have done!"
    hide nurse with moveoutleft
    show doctor bummed
    doctor "..."
    naomi troubled "(Maybe I should come back another time..?)"
    show doctor happy
    doctor "Oh, hey! You're--"
    show doctor thinking
    doctor "Err.."
    show doctor bummed 
    doctor "Sorry, I don't know your name."
    naomi relieved "It's Naomi."
    show doctor happy
    doctor "Right, Naomi!"
    show doctor happyside:
        xzoom -1.0 zoom 1.0
    doctor "Let's go to my clinic. This way."
    hide doctor with moveoutright
    show clinic
    $ guy_display = True
    show doctor concerned:
        xalign 0.5
    doctor "Did you experience a dizzy spell again?"
    naomi troubled "No..."
    show doctor thinking
    doctor "I see."
    show doctor concerned:
        zoom 1.0 yalign 1.0
        easein 2.0 zoom 2.0 yalign 0.7
    doctor "Let me check your heartbeat first."
    show doctor thinking:
        zoom 2.0 yalign 0.7
    naomi blush "..."
    doctor "Hm. A little fast."
    show doctor thinking:
        easeout 1.5 zoom 3.0 ypos 1.2 xpos 1.1
    doctor "Checking the ears."
    naomi blush "(He's so close.)"
    show doctor concerned:
        easein 2.0 zoom 2.0 yalign 0.7 xalign 0
    doctor "Looks alright."
    show doctor thinking:
        xzoom -1.0 zoom 2.0 yalign 0.7 xalign 0
        easein 2.0 zoom 3.0 ypos 1.2 xpos -0.7
    doctor "Now this side."
    naomi blush "(I can feel his body heat.)"
    show doctor concerned:
        zoom 3.0 ypos 1.2 xpos -0.7
        easeout 2.0 zoom 1.0 yalign 0.0 xalign 0.5
    doctor "Nothing unusual."
    naomi pain "(Phew, it's over.)"
    show doctor indifferent:
        zoom 1.0 yalign 0.0 xalign 0.5
    doctor "Keep monitoring and tell me if it happens again."
    naomi relieved "Got it!"
    show doctor concerned
    menu:
        doctor "Any questions for me?"
        "What happened earlier?":
            naomi troubled "What happened earlier?"
            doctor "With the mother?"
            show doctor indifferent
            doctor "I don't know."
            show doctor thinking
            doctor "She asked if there's a chance her son might die."
            show doctor indifferent
            doctor "I said yes."
            show doctor bummed
            doctor "She started crying..."
            naomi surprised "Her son might die?!"
            show doctor indifferent
            doctor "For a young person appendicitis is usually not fatal."
            show doctor thinking
            doctor "But I can't discount the slight risk of complications in surgery."
            # show doctor concerned
            # doctor "I didn't say anything wrong, did I?"
            naomi thinking "(That's too blunt!)"
            naomi thinking "(Now I understand why the nurse was upset.)"
            # naomi thinking "She was probably feeling scared and helpless."
            # naomi troubled "'Yes' was not the right thing to say to her."
            # show doctor thinking
            # doctor "..."
            # show doctor concerned
            # doctor "What should I have said, then?"
            # naomi troubled "You could have said what you explained to me."
            # naomi relieved "That it's usually not fatal, but there is a slight risk of complications."
            # show doctor thinking
            # doctor "I see."
            # show doctor happyside
            # doctor "Thanks for helping me understand."
            $ doctor_courage += 1
            show doctor happy
            doctor "Is there anything I can help you with?"
            naomi troubled "Umm... "
            naomi troubled "I overheard the nurse saying they were shorthanded..."
                # "You didn't.":
                #     naomi thinking "I don't think so."
                #     naomi relieved "She was probably overreacting?"
                #     show doctor thinking
                #     doctor "I see."
                #     show doctor indifferent
                #     doctor "Nothing I could have done then."
                #     show doctor happy
                #     doctor "Is there anything I can help you with?"
                #     naomi troubled "Umm... "
                #     naomi troubled "I overheard the nurse saying they were shorthanded..."
        "Shorthanded?":
            naomi troubled "I overheard the nurse saying they were shorthanded..."
    show doctor thinking
    doctor "Indeed. With all the paperwork, we barely have time to look after patients."
    naomi relieved "I see."
    show doctor indifferent
    naomi thinking "Umm well, I'm actually looking for a job in the city."
    naomi relieved "If the hospital is hiring..."
    show doctor happyside
    doctor "What luck!"
    show doctor happy
    doctor "We're looking for someone to help with paperwork."
    naomi relieved "That's perfect."
    show doctor happyside:
        xzoom -1.0 zoom 1.0
    doctor "Let's go talk to nurse."
    $ guy_display = False
    $ encounters["doctor"] += 1
    hide doctor with moveoutright
    hide clinic
    show bg hospital
    show nurse relieved:
        xalign 0.2 ypos 0.1
    show doctor happyside with moveinright:
        xalign 0.8
    doctor "This young lady is willing to help with the paperwork."
    show nurse sigh:
        xalign 0.2 xzoom -1.0 ypos 0.1
    nurse "I do hope she can read your handwriting."
    show doctor happyside:
        xzoom -1.0 zoom 1.0 xalign 0.8
    doctor "Nurse will explain to you."
    doctor "I'll be in my clinic."
    naomi relieved "Thank you!"
    hide doctor with moveoutright
    show nurse relieved:
        xalign 0.2 zoom 1.0 ypos 0.1
        easein 1.0 xalign 0.5 zoom 1.0
    nurse "You'll need to refer to the doctor's notes and fill out the requests for medication and such."
    nurse "You can come to the hospital between Mondays and Fridays."
    nurse "You'll be paid for the day's work."
    nurse "At the end of the month, if your performance was good, you can become a full-time employee."
    nurse "Can you start now?"
    naomi troubled "Uh, sure?"
    naomi troubled "(They must be really short-handed!)"
    show nurse sigh
    nurse "Good."
    show nurse relieved
    nurse "Now go look for Dr Yumoto and get the notes from him."
    naomi troubled "Yes, ma'am."
    hide nurse with moveoutright
    return

label doctor_3:
    scene bg hospital
    show doctor thinking:
        xalign 0.2 yalign 1.0 xzoom -1.0
    show nurse sigh:
        xalign 0.8 ypos 0.1
    nurse "Dr Yumoto, what you said to the patient just now-"
    show doctor indifferent:
        xalign 0.2 yalign 1.0 xzoom -1.0
    doctor "Did I say something wrong?"
    show nurse angry
    nurse "He was very distraught."
    show nurse angry:
        xalign 0.8 ypos 0.1 xzoom -1.0 zoom 1.0
    nurse "Please be more gentle next time."
    hide nurse with moveoutright
    show doctor bummed
    doctor "..."
    show doctor concerned
    doctor "Oh, Naomi."
    show doctor blush:
        xalign 0.5 zoom 1.0
    doctor "Sorry you had to see that."
    menu:
        "Ask what happened":
            $ doctor_courage += 1
            naomi troubled "What happened?"
            show doctor indifferent
            doctor "A patient asked about his prognosis. I told him full recovery is unlikely."
            naomi thinking "How did he react?"
            show doctor bummed
            doctor "He was shocked."
            show doctor indifferent
            doctor "I don't understand. He wanted the truth, so I was honest with him."
            naomi troubled "He asked for the truth, but maybe he wasn't ready for it."
            show doctor concerned
            doctor "Should I have lied?"
            naomi thinking "Not lie..."
            naomi relieved "Maybe he just needed to be guided to the truth slower."
            show doctor thinking
            doctor "I see..."
            show doctor happy
            doctor "Thank you for explaining it to me."
            doctor "I'll try to be more aware next time."
            naomi relieved "I'm sure your patients will appreciate it."
            nurse "Dr Yumoto!"
            show doctor happyside:
                xzoom -1.0 zoom 1.0
            doctor "I need to go. See you."
            hide doctor with moveoutright
            return
        "Brush it off":
            naomi relieved "It's fine, workplace troubles."
            show doctor happy
            doctor "You're too kind."
            nurse "Dr Yumoto!"
            show doctor happyside:
                xzoom -1.0 zoom 1.0
            doctor "I need to go. See you."
            hide doctor with moveoutright
            return

label doctor_4:
    show doctor indifferent:
        xalign 0.5 yalign 0.0 zoom 1.0
    doctor "Naomi."
    show doctor concerned
    doctor "I need your help."
    doctor "I have bad news to deliver to a patient."
    naomi surprised "What bad news?"
    doctor "He has typhoid."
    show doctor thinking
    doctor "There's little I can do except to treat his symptoms."
    show doctor concerned
    menu:
        doctor "Should I be honest with him? Or be vague about it?"
        "Be vague":
            naomi troubled "I think it is better to be indirect."
            naomi troubled "Tell him you'll do your best to keep him comfortable."
            doctor "Isn't that avoiding reality?"
            naomi thinking "Being too direct might do more harm than good, if he's very sick."
        "Be honest":
            $ doctor_choice += 1
            if totaldays > 8:
                $ enable_doctor_event_1 = True
            naomi troubled "Just be honest with him."
            doctor "Won't that be too harsh?"
            naomi relieved "It doesn't have to be harsh. You can be clear and still compassionate."
            naomi relieved "Tell him you can't cure the illness, but you'll do your best to keep him comfortable."
    show doctor thinking
    doctor "I see."
    show doctor happy
    doctor "Thank you for your advice, Naomi."
    return

label doctor_5:
    $ guy_display = True
    naomi troubled "By the way..."
    show doctor indifferent
    doctor "Yes?"
    naomi thinking "How did it go with the patient?"
    if doctor_choice == 0:
        show doctor indifferent
        doctor "The patient?"
        show doctor concerned
        doctor "Ah!"
        show doctor thinking
        doctor "It didn't go as planned..."
        show doctor bummed
        doctor "He got frustrated, and I ended up blurting out that he's incurable."
        naomi troubled "Oh no."
        naomi thinking "Well, you did what you could."
        show doctor concerned
        doctor "Yeah."
        $ guy_display = False
    if doctor_choice == 1:
        show doctor thinking
        doctor "Ah..."
        show doctor concerned
        doctor "I told him the truth."
        show doctor indifferent
        doctor "He didn't say much."
        show doctor thinking
        doctor "I think he had guessed it himself."
        show doctor indifferent
        doctor "He thanked me and left."
        show doctor happyside
        doctor "It was right to tell him the truth gently."
        naomi happy "Good that it went alright."
        show doctor happy
        doctor "Thanks for your advice."
        if enable_doctor_event_1 == True:
            doctor "Naomi, I'm glad I met you."
            image doctor glitched:
                glitch("doctor happy")
                pause 0.1
                glitch("doctor happy",offset=60,randomkey=None)
                pause 0.1
                glitch("doctor happy")
                pause 0.1
                "doctor happy"
            show doctor glitched
            show clinic as clinic_copy at atl_dizzy
            naomi pain "Unngh!" with vpunch
            show doctor concerned
            doctor "Naomi!"
            #Replace clinic with cutscene
            scene clinic with Fade(0.2,0.5,2.0)
            pause
            naomi sleepy "(So warm...)"
            hide window
            pause
            show clinic
            show doctor concerned:
                xalign 0.5 yalign 0.4 zoom 4.0 blur 5.0 matrixcolor BrightnessMatrix(-0.3)
            with Fade(2.0,0.5,2.0)
            doctor "Are you alright?"
            naomi blush "..."
            show doctor blush:
                ease 0.5 yalign 0.2 zoom 2.0 blur 0.0 matrixcolor BrightnessMatrix(0.0)
            doctor "Sorry!"
            naomi blush "Sorry, I blacked out for a moment."
            show doctor thinking:
                yalign 0.2 zoom 2.0
            doctor "I'm not sure why I'm apologising."
            show doctor concerned:
                yalign 0.2 zoom 2.0
            doctor "Here, sit down."
            naomi happy "I'm feeling fine now!"
            naomi happy "Thank you for your concern."
            show doctor concerned:
                easein 1.0 yalign 0 zoom 1.0
            doctor "Have you been sleeping well?"
            naomi troubled "...I've been having strange dreams."
            naomi thinking "Maybe I've been working too hard."
            doctor "I'll prescribe you medication to help sleep better."
            naomi happy "Thanks, doctor!"
            show doctor thinking
            doctor "..."
            show doctor blush
            doctor "Shiro."
            $ doctor_name = "Shiro"
            naomi blush "Shiro."
            naomi relieved "Thank you, Shiro!"
    return

label doctor_6:
    naomi troubled "(He's not here.)"
    naomi troubled "(Maybe he's at the wards.)"
    hide bg clinic
    show bg hospital
    with dissolve
    doctor "Madam, I can't promise your son will wake up..."
    naomi troubled "(Oh no! Is he going to say something blunt again?)"
    define mother = Character("Mother", color="#000000")
    if doctor_courage > 1:
        doctor "...but we have observed more movement." 
        doctor "It's a good sign. Don't give up, keep talking to him!"
        mother "Thank you so much, doctor!"
        naomi relieved "(Phew.)"
    else:
        mother "Is there nothing I can do?"
        doctor "Hope for the best, be prepared for the worst."
        mother "..."
        naomi pain "..."
    naomi relieved "(I'll wait for him at his office.)"
    hide bg hospital with dissolve
    show clinic with dissolve
    show doctor happyside with moveinright:
        xalign 0.5
    doctor "Hey."
    naomi relieved "Hey."
    menu:
        "I overheard.":
            if doctor_courage > 1:
                naomi happy "I overheard you talking to the patient's mother."
                show doctor concerned
                doctor "Do you think it went alright?"
                show doctor bummed
                doctor "I thought very hard and this was the best I could come up with..."
                show doctor concerned
                naomi relieved "Yes! I think you managed to assure her."
                show doctor happy
                doctor "I'm so glad."
                show doctor blush
                doctor "It's because of you..."
                naomi surprised "Me?"
                show doctor happyside
                doctor "Nothing."
                $ doctor_courage += 1
            else:
                naomi troubled "I overheard you talking to the patient's mother."
                show doctor indifferent
                doctor "Oh?"
                naomi thinking "I think you could have been more tactful."
                show doctor concerned
                doctor "How so?"
                naomi troubled "The mother was feeling helpless."
                naomi thinking "You could have encouraged her not to give up."
                show doctor thinking
                doctor "I see..."
                show doctor indifferent
                doctor "I'll go talk to her again."
                show doctor happyside
                doctor "Thank you for pointing that out to me."
                $ doctor_courage += 1
        "Nothing.":
            naomi happy "Can I have the notes?"
    return

label doctor_7:
    show doctor happyside with moveinright:
        xalign 0.5 yalign 0.0 zoom 1.0
    doctor "Hey."
    show doctor indifferent
    doctor "I... Uh."
    naomi surprised "Yes?"
    show doctor thinking
    doctor "A patient gave me a pair of tickets to the movie this Sunday afternoon."
    naomi blush "..."
    show doctor indifferent
    doctor "If you're not busy that day, I thought perhaps..."
    if doctor_courage > 2:
        show doctor blush
    doctor "Would you come with me?"
    naomi blush "Yes!"
    naomi relieved "I mean..."
    naomi happy "I'd love to go with you."
    show doctor happy
    doctor "Great!"
    show doctor happyside
    doctor "I'll meet you there then."
    naomi happy "Sure!"
    $ doctor_event = True
    return

label hospital_ending:
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