label merchant_final_irl:
    show bg office
    show merchant resigned:
        xalign 0.5
    merchant "Finally."
    naomi troubled "...Yujiro?"
    show merchant frown:
        ease 1.0 zoom 1.2 yalign 0.1
    merchant "Since I met you, I've not been myself."
    naomi troubled "What do you mean?"
    show merchant frownside:
        zoom 1.2 yalign 0.1
    merchant "Being gentle."
    show merchant frown:
        zoom 1.2 yalign 0.1
    merchant "Relying on others."
    show merchant frownside:
        zoom 1.2 yalign 0.1
    merchant "Caring..."
    show merchant surprised:
        zoom 1.2 yalign 0.1
    merchant "Caring for you."
    naomi blush "..."
    show merchant smile:
        easein 1.0 zoom 1.5 yalign 0.15
    merchant "You changed me."
    naomi troubled "I did?"
    show merchant happy:
        zoom 1.5 yalign 0.15
    merchant "With you, I've become a better person."
    show merchant smile:
        easein 1.0 zoom 2.0 yalign 0.2
    merchant "Stay by my side."
    image merchant glitched4:
        glitch("merchant smile")
        pause 0.1
        glitch("merchant smile",offset=60,randomkey=None)
        pause 0.1
        glitch("merchant smile")
        pause 0.1
        "merchant smile"
    show merchant glitched4:
        zoom 2.0 yalign 0.2
    naomi sleepy "(This scent...)"
    $ day_display = False
    show black1:
        xalign 0.5 yalign 1.0 #full close
    show black2:
        xalign 0.5 yalign 0.0 #full close
    hide window
    with Pixellate(2.0,5)
    show text "{color=#ffffff}Cedarwood...{/color}":
        xalign 0.5 yalign 0.8
    pause
    show merchant frownside zorder 2:
        xalign 0.1 zoom 1.5 yalign 0.1
    show text "{color=#ffffff}Yujiro.{/color}" zorder 3:
        xalign 0.7 yalign 0.8
    with dissolve
    pause
    show text "{color=#ffffff}He's my senior at internship.{/color}" zorder 3:
        xalign 0.5 yalign 0.8
    with dissolve
    pause
    show merchant frown zorder 2:
        zoom 1.5 yalign 0.1
    show text "{color=#ffffff}'You can start by filling in these forms.'{/color}" zorder 3:
        xalign 0.9 yalign 0.25
    with dissolve
    pause
    show text "{color=#ffffff}He was strict on himself and others.{/color}" zorder 3:
        xalign 0.5 yalign 0.8
    with dissolve
    pause
    show merchant scowlside zorder 2:
        zoom 1.5 yalign 0.1
    show text "{color=#ffffff}'Thanks for the idea.'{/color}" zorder 3:
        xalign 0.65 yalign 0.25
    with dissolve
    pause
    show text "{color=#ffffff}I respected him for his hard work.{/color}" zorder 3:
        xalign 0.5 yalign 0.8
    with dissolve
    pause
    show merchant scowlfront zorder 2:
        zoom 1.5 yalign 0.1
    show text "{color=#ffffff}'Thanks for staying back with me.'{/color}" zorder 3:
        xalign 0.95 yalign 0.4
    with dissolve
    pause
    show text "{color=#ffffff}Eventually, I gained his trust.{/color}" zorder 3:
        xalign 0.5 yalign 0.8
    with dissolve
    pause
    show merchant smile_suit zorder 2:
        zoom 1.5 yalign 0.1
    show text "{color=#ffffff}'From now on, stay by my side.'{/color}" zorder 3:
        xalign 0.7 yalign 0.4
    with dissolve
    pause
    hide merchant
    hide text
    show text "{color=#ffffff}I want to be by your side.{/color}" zorder 3:
        xalign 0.5 yalign 0.8
    with dissolve
    pause
    hide text with dissolve
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
    show merchant frownside zorder 1:
        zoom 2.5 yalign 0.0 xalign 0.1
    show text "{color=#ffffff}Yujiro...{/color}" zorder 3:
        xalign 0.5 yalign 0.8
    pause
    hide black1
    hide black2
    hide text
    show merchant surprised:
        zoom 2.5 yalign 0.0 xalign 0.1
        easein 0.5 zoom 3.0 yalign 0.05 xpos -0.15
    show text "{color=#ffffff}'Naomi!'{/color}" zorder 3:
        xalign 0.6 yalign 0.8 alpha 1.0
    pause
    show merchant surprised:
        zoom 3.0 yalign 0.05 xpos -0.15
    show text "{color=#ffffff}'You're awake.'{/color}" zorder 3:
        xalign 0.6 yalign 0.8
    pause
    show text "{color=#ffffff}Where...am I?{/color}" zorder 3:
        xalign 0.8 yalign 0.8
    pause
    show merchant resigned:
        zoom 3.0 yalign 0.05 xpos -0.15
    show text "{color=#ffffff}'The hospital.'{/color}" zorder 3:
        xalign 0.6 yalign 0.8
    pause
    show merchant frown:
        zoom 3.0 yalign 0.05 xpos -0.15
    show text "{color=#ffffff}'You've been out for two days.'{/color}" zorder 3:
        xalign 0.75 yalign 0.8
    pause
    show text "{color=#ffffff}Two days...?{/color}" zorder 3:
        xalign 0.8 yalign 0.8
    pause
    show text "{color=#ffffff}What about...work?{/color}" zorder 3:
        xalign 0.8 yalign 0.8
    pause
    show merchant scowlfront:
        zoom 3.0 yalign 0.05 xpos -0.15
    show text "{color=#ffffff}'Work? With you here?'{/color}" zorder 3:
        xalign 0.7 yalign 0.8
    pause
    show merchant frown:
        zoom 3.0 yalign 0.05 xpos -0.15
    show text "{color=#ffffff}'I told you, I need you by my side.'{/color}" zorder 3:
        xalign 0.85 yalign 0.8
    pause
    show text "{color=#ffffff}Sorry...I left you alone.{/color}" zorder 3:
        xalign 0.8 yalign 0.8
    pause
    hide text
    show merchant surprised:
        zoom 3.0 yalign 0.05 xpos -0.15
    pause
    show merchant resigned:
        zoom 3.0 yalign 0.05 xpos -0.15
    show text "{color=#ffffff}'Always worrying about others.'{/color}" zorder 3:
        xalign 0.8 yalign 0.8
    pause
    show merchant smile:
        zoom 3.0 yalign 0.05 xpos -0.15
    show text "{color=#ffffff}'Rest. I'll call for the doctor.'{/color}" zorder 3:
        xalign 0.75 yalign 0.8
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
    hide merchant
    hide text
    show merchant_cutscene_3
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

label merchant_final_not:
    show merchant resigned:
        xalign 0.5
    merchant "There you are."
    naomi troubled "Sorry, I'm late! What do you need me to do?"
    show merchant frown
    merchant "I need you to fill in these employment forms."
    show paperstack:
        xpos 0.4 ypos 0.5 zpos 0 zoom 0.5
        easein 1.0 xpos 0.4 ypos 0.55 zpos 800
    naomi happy "Sure!"
    naomi thinking "(These must be the new employment terms. I'd better take a good look before I sign.)"
    naomi thinking "Position title..."
    naomi blush "Girlfriend?"
    show merchant frownside
    merchant "..."
    merchant "I want to make this official."
    show merchant scowlfront
    merchant "You have a problem with that?"
    naomi blush "Uh, I guess not."
    show merchant happy
    merchant "Then sign those forms quickly."
    naomi smirk "What if I want to negotiate?"
    show merchant surprised
    merchant "..."
    naomi smirk "Just kidding."
    naomi relieved "You didn't have to go to all this trouble."
    naomi happy "I'll be your girlfriend, no conditions needed."
    show merchant resigned
    merchant "I didn't know how to put it in words..."
    show merchant frown
    merchant "You'll stay here with me from now on?"
    naomi happy "I will."
    show merchant smile
    merchant "That's a deal."
    merchant "I'll see you later?"
    naomi happy "Sure!"
    hide merchant with moveoutright
    naomi blush "I can't believe he asked me to be his girlfriend."
    naomi happy "Everything worked out just right."
    naomi thinking "I found a job."
    naomi blush "And met Yujiro."
    naomi happy "I'm so happy, I feel like I'm dreaming right now!"
    naomi thinking "..."
    naomi troubled "What if it's all just a dream?"
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

label doctor_final_irl:
    show clinic
    show doctor concerned:
        xalign 0.5
    doctor "I've been waiting for you."
    naomi troubled "Waiting for me?"
    show doctor happy:
        ease 1.0 zoom 1.2 yalign 0.1
    doctor "To wake up."
    doctor "You helped me to be a better person."
    naomi troubled "I did?"
    show bg clinic as bg_copy at atl_dizzy
    show doctor glitched2:
        zoom 1.2 yalign 0.1
    naomi pain "Ngh!" with vpunch
    naomi pain "(This pain again!)"
    show doctor happy:
        easein 1.0 zoom 1.5 yalign 0.2
    doctor "You were brave to tell me your thoughts."
    naomi troubled "I was brave?"
    show doctor concerned:
        zoom 1.5 yalign 0.2
    doctor "It's my turn to be brave for you."
    show bg clinic as bg_copy at atl_dizzy
    naomi pain "Ahh!" with vpunch
    doctor "Hang in there."
    image doctor glitched3:
        glitch("doctor concerned")
        pause 0.1
        glitch("doctor concerned",offset=60,randomkey=None)
        pause 0.1
        glitch("doctor concerned")
        pause 0.1
        "doctor concerned"
    show doctor glitched3:
        zoom 1.5 yalign 0.2
    naomi troubled "(A warm hand...)"
    $ day_display = False
    show black1:
        xalign 0.5 yalign 1.0 #full close
    show black2:
        xalign 0.5 yalign 0.0 #full close
    hide window
    with Pixellate(2.0,5)
    show text "{color=#ffffff}'Open your eyes, Naomi.'{/color}":
        xalign 0.5 yalign 0.8
    pause
    show text "{color=#ffffff}This voice...{/color}":
        xalign 0.5 yalign 0.8
    pause
    show doctor happy zorder 2:
        zoom 1.0 xalign 0.65 yalign 0.0
        ease 2.0 zoom 1.5 yalign 0.1
    show text "{color=#ffffff}'I held your hand because...'{/color}" zorder 3:
        xalign 0.1 yalign 0.25
    with dissolve
    pause
    show doctor happy zorder 2:
        zoom 1.5 yalign 0.1
    show text "{color=#ffffff}'I just wanted to.'{/color}" zorder 3:
        xalign 0.9 yalign 0.25
    with dissolve
    pause
    hide doctor
    show text "{color=#ffffff}So warm.{/color}" zorder 3:
        xalign 0.5 yalign 0.8
    with dissolve
    pause
    show doctor happy zorder 2:
        zoom 1.5 yalign 0.3
    show text "{color=#ffffff}'Naomi, I'm glad I met you.'{/color}" zorder 3:
        xalign 0.9 yalign 0.25
    with dissolve
    pause
    hide doctor
    show text "{color=#ffffff}I'm glad, too.{/color}" zorder 3:
        xalign 0.5 yalign 0.8
    with dissolve
    pause
    show text "{color=#ffffff}How did we meet?{/color}" zorder 3:
        xalign 0.5 yalign 0.8
    pause
    hide doctor
    hide text
    show cat neutral
    show doctor happyside zorder 2:
        xzoom -1.0
    show text "{color=#ffffff}'Maachan.'{/color}" zorder 3:
        xalign 0.35 yalign 0.25
    with dissolve
    pause
    show cat scared:
        xpos 1.0 zoom 0.7 ypos 0.1
    show text "{color=#ffffff}'Mew!'{/color}" zorder 3:
        xalign 0.5 yalign 0.8
    pause
    hide text
    show cat scared:
        xpos 1.0
        easein 0.5 xpos 2.5 ypos 0.5 zoom 2.5 blur 10.0
    show doctor bummed
    pause
    hide cat
    show text "{color=#ffffff}That's right, he's Maachan's vet.{/color}" zorder 3:
        xalign 0.7 yalign 0.8
    with dissolve
    pause
    hide doctor
    show kirako angry:
        xalign 0.6
    show cat eyeroll:
        xpos 1.1
    show text "{color=#ffffff}'Maachan! Don't run off on your own!'{/color}" zorder 3:
        xalign 0.1 yalign 0.36
    with dissolve
    pause
    hide kirako
    hide cat
    hide text
    show text "{color=#ffffff}That day, I helped Kirako bring her cat to see Shiro as usual, but.{/color}" zorder 3:
        xalign 0.5 yalign 0.8
    with dissolve
    pause
    hide text
    show cat scared:
        xpos 0.7 zoom 0.75 ypos 0.1
    pause
    show cat scared:
        easein 0.5 xpos -0.5 ypos 0.5 zoom 2.5 blur 10.0
    show text "{color=#ffffff}Maachan, no!{/color}" zorder 3:
        xalign 0.5 yalign 0.8
    play sound "crash.mp3"
    pause
    show text "{color=#ffffff}'I've got you.'{/color}" zorder 3:
        xalign 0.5 yalign 0.8
    with dissolve
    pause
    show text "{color=#ffffff}'Hang in there.'{/color}" zorder 3:
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
    show text "{color=#ffffff}Shiro.{/color}" zorder 3:
        xalign 0.5 yalign 0.8
        pause 3.5
        easeout 3 alpha 0.0
    show doctor indifferent zorder 1:
        zoom 2.0 yalign 0.0 xalign 0.1 xzoom -1.0
    pause
    hide black1
    hide black2
    hide text
    show doctor concerned:
        zoom 2.0 yalign 0.0 xalign 0.1
        easein 0.5 zoom 2.5 yalign 0.05 xpos -0.1
    show text "{color=#ffffff}'Naomi!'{/color}" zorder 3:
        xalign 0.6 yalign 0.8 alpha 1.0
    pause
    show doctor happy:
        zoom 2.5 yalign 0.05 xpos -0.1
    show text "{color=#ffffff}'You're awake.'{/color}" zorder 3:
        xalign 0.6 yalign 0.8
    pause
    show text "{color=#ffffff}...How...long?{/color}" zorder 3:
        xalign 0.6 yalign 0.8
    pause
    show doctor indifferent:
        zoom 2.5 yalign 0.05 xpos -0.1 xzoom -1.0
    show text "{color=#ffffff}'You've been out for two days.'{/color}" zorder 3:
        xalign 0.7 yalign 0.8
    pause
    show text "{color=#ffffff}Two...{/color}" zorder 3:
        xalign 0.5 yalign 0.8
    pause
    show doctor concerned:
        zoom 2.5 yalign 0.05 xpos -0.1 xzoom -1.0
    show text "{color=#ffffff}'Rest. I'll go get the doctor.'{/color}" zorder 3:
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
    hide doctor
    hide text
    show doctor_cutscene_3
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

label doctor_final_not:
    show doctor concerned:
        xalign 0.5
    doctor "I've been waiting for you, Naomi."
    naomi troubled "Sorry, I'm late! Where are the patient notes?"
    doctor "That can wait."
    show doctor indifferent
    doctor "I have something to tell you."
    naomi troubled "...(He looks serious.)"
    show doctor thinking
    doctor "I've decided that I don't want to be your doctor."
    naomi surprised "(Wait, what? Did I do something wrong?)"
    naomi troubled "Did I-"
    show doctor happy
    doctor "I want to be your boyfriend instead."
    naomi blush "!"
    show doctor blush
    doctor "Will you be my girlfriend?"
    naomi pain "You-"
    naomi relieved "You got me there."
    show doctor bummed
    doctor "Is that a no?"
    naomi angry "No!"
    doctor "No?"
    naomi relieved "What I mean is, yes! I'll be your girlfriend."
    show doctor blush
    doctor "..."
    doctor "I feel shy suddenly."
    naomi blush "Now you made me feel shy too."
    show doctor happy
    doctor "I'm glad."
    doctor "Will you stay here with me from now on?"
    naomi happy "I will."
    show doctor happyside:
        xzoom -1.0 zoom 1.0
    doctor "I need to go now."
    doctor "I'll see you later?"
    naomi happy "Sure!"
    hide doctor with moveoutright
    naomi blush "I can't believe he asked me out."
    naomi happy "Everything worked out just right."
    naomi thinking "I found a job."
    naomi blush "And met [doctor_name]."
    naomi happy "I'm so happy, I feel like I'm dreaming right now!"
    naomi thinking "..."
    naomi troubled "What if it's all just a dream?"
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

label musician_final_irl:
    $ day_display = False
    show bg imperial theatre
    show musician troubled:
        xalign 0.5
    naomi surprised "Hideo?"
    naomi troubled "Don't you have rehearsal?"
    musician "No, I'm here for you."
    naomi surprised "Me?"
    show musician shy
    musician "You helped me to be true to myself."
    show musician troubled
    musician "It's my turn to help you remember who you are."
    naomi troubled "Who I am?"
    musician "Listen."
    naomi thinking "This sound..."
    naomi surprised "It's from my dream!"
    show bg imperial theatre as bg_copy at atl_dizzy
    image musician glitched3:
        glitch("musician troubled")
        pause 0.1
        glitch("musician troubled",offset=60,randomKey=None)
        pause 0.1
        glitch("musician troubled")
        pause 0.1
        "musician troubled"
    show musician glitched3
    naomi pain "Ngh!" with vpunch
    musician "Come back, Naomi."
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

label musician_final_not:
    show bg imperial theatre
    show musician happy:
        xalign 0.5
    naomi surprised "Hideo?"
    musician "I've been waiting for you, Naomi."
    naomi troubled "Don't you have rehearsal?"
    show musician shy
    musician "That can wait."
    show musician troubled
    musician "There's something I need to tell you."
    naomi blush "..."
    show musician shy2
    musician "I..."
    musician "I really like you."
    naomi surprised "..."
    naomi blush "I feel the same way..."
    show musician surprised
    musician "You do?"
    show musician happy
    musician "I'm glad."
    musician "Will you stay here with me from now on?"
    naomi happy "I will."
    show musician shy
    musician "I need to go now."
    show musician happy
    musician "I'll see you later?"
    naomi happy "Sure!"
    hide musician with moveoutleft
    naomi blush "I can't believe he feels the same way as me."
    naomi happy "Everything worked out just right."
    naomi thinking "I found a job."
    naomi blush "And met Hideo."
    naomi happy "I'm so happy, I feel like I'm dreaming right now!"
    naomi thinking "..."
    naomi troubled "What if it's all just a dream?"
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
