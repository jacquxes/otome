## Opening Sequence ##

label opening_sequence:

    scene bg opening

    show text "{color=#ffffff}I'm chasing a cat. It's getting away from me.{/color}":
        xalign 0.5 yalign 0.5
    pause
    hide text
    show text "{color=#ffffff}My lungs burn. My feet pound against the ground. I reach out and lunge forward in one last desperate grab—{/color}":
        xalign 0.5 yalign 0.5
    pause
    hide text
    show text "{color=#ffffff}Then there is nothing.{/color}":
        xalign 0.5 yalign 0.5
    pause
    # show black1 zorder 2:
    #     xalign 0.5 yalign 3.5 #full open
    #     easein 3.5 yalign 1.3 #part open
    #     pause 0.5
    #     easeout 2.5 yalign 1.0 #full close
    # show black2 zorder 2:
    #     xalign 0.5 yalign -2.5 #full open
    #     easein 3.5 yalign -0.3 #part open
    #     pause 0.5
    #     easeout 2.5 yalign 0.0 #full close
    # pause
    # hide text
    # hide black1
    # hide black_2
    # with Fade(2.0,0.5,0.5)
    
    # Start introduction to cat
    scene bg cafeleft
    play music "<from 1 to 79.5>spring.mp3" loop if_changed
    show table_left:
        xalign 1.0 yalign 1.0 zoom 0.5
    show cat neutral
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
    pause
    hide black1
    hide black2
    $ day_display = True
    ## Cat is unnamed yet
    $ cat_name = "???"
    # show black1 zorder 2:
    #     xalign 0.5 yalign 1.0 #full close
    #     easein 3.5 yalign 1.3 #part open
    #     pause 0.5
    #     easeout 2.5 yalign 3.5 #full open
    # show black2 zorder 2:
    #     xalign 0.5 yalign 0.0 #full close
    #     easein 3.5 yalign -0.3 #part open
    #     pause 0.5
    #     easeout 2.5 yalign -2.5 #full open
    # pause
    naomi sleepy "Nhh..."
    cat "Meow."
    naomi surprised "A cat?"
    naomi troubled "Where am I?"
    naomi thinking "And what was I doing before this...?"
    cat "Meow."
    naomi troubled "I don't recall anything."
    # naomi sleepy "(I'm finally here.)"
    # show cat neutral with moveinbottom
    # cat "Meow."
    # naomi surprised "Ah, you must be Miss Kirako's cat."
    # naomi happy "Hello!"
    # show cat huff
    # cat "You can't be here meow."
    # naomi surprised "Did I hear the cat speak?"
    # naomi thinking "No way, I must have misheard."
    # naomi sleepy "It was such a long journey to get here."


    ## Kirako is unnamed yet
    $ kirako_name = "???"

    ## Kirako enters and Maachan moves right
    show table_left zorder 2.0:
        xalign 1.0 yalign 1.0 zoom 0.5
    show cat eyeroll at right zorder 3.0
    show kirako angry:
        xalign 0.3
    with moveinleft
    kirako "Maachan!"
    kirako "Don't run off on your own!"
    image kirako glitched:
        glitch("kirako angry")
        pause 0.1
        glitch("kirako angry",offset=60,randomkey=None)
        pause 0.1
        glitch("kirako angry")
        pause 0.1
        "kirako angry"
    show kirako glitched:
        xalign 0.3
    naomi surprised "...Maachan?"
    show kirako happy:
        xalign 0.3 zoom 1.0
    kirako "Oh hello! You must be Hana-chan's daughter. Naomi, yes?"
    naomi troubled "Yes, that's me."
    kirako "I knew it!"
    show kirako wink:
        xalign 0.3 zoom 1.0
    kirako "You look just like your mother."
    show kirako pout:
        xalign 0.3 zoom 1.0
    kirako "Did she not mention me? We were neighbours before she got married!"
    naomi thinking "(She looks familiar, now that I think about it...)"
    show kirako happy:
        xalign 0.3 zoom 1.0
    kirako "I'm Kirako! Welcome to Cafe Diamond."
    $ kirako_name = "Kirako"
    $ cat_name = "Maachan"
    naomi happy "It's nice to meet you, Miss Kirako."
    show kirako happy:
        xalign 0.3 zoom 1.0
    kirako "I'm so glad you're here!"
    show kirako pout:
        xalign 0.3 zoom 1.0
    kirako "We might have to close at the end of the month..."
    naomi surprised "Close?"
    show kirako angry:
        xalign 0.3 zoom 1.0
    kirako "Customers have been scarce lately."
    show kirako happy:
        xalign 0.3 zoom 1.0
    kirako "But what can you do!"
    naomi troubled "..."
    show kirako wink:
        xalign 0.3 zoom 1.0
    kirako "Let's make the most of your stay here."
    show kirako happy:
        xalign 0.3 zoom 1.0
    kirako "Have fun, meet people, eat cake!"
    naomi troubled "Ah-"
    show kirako pout:
        xalign 0.3 zoom 1.0
    kirako "Oh my, look at the time! We have to open the cafe!"
    show kirako angry:
        xalign 0.3 zoom 1.0
    kirako "Follow me!"
    hide kirako with moveoutright
    naomi surprised "Eh?"
    $ timeslot -= 1
    $ renpy.random.shuffle(cafe_menu)    
    call screen cafe_menu with pushleft
    pause

label re_explain_cafegame:

    scene bg caferight
    
    # Recreate ending scene
    image order0 = "images/[cafe_menu[0]].png"
    show order0:
        xalign 0.22 yalign 0.55 xzoom 0.10 yzoom 0.1
    image order1 = "images/[cafe_menu[1]].png"
    show order1:
        xalign 0.5 yalign 0.55 xzoom 0.10 yzoom 0.1
    image order2 = "images/[cafe_menu[2]].png"
    show order2:
        xalign 0.8 yalign 0.55 xzoom 0.10 yzoom 0.1

    image cafetableright = im.Scale("images/cafe/table_right.png",1920,1080)
    show cafetableright zorder 3.0

    # Kirako pays Naomi
    naomi relieved "All done."
    show kirako happy with moveinleft
    kirako "Thank you for your help Naomi!"
    $ tips = renpy.random.randint(10, 15)
    $ money += tips
    kirako "Here you go, [tips] yen in tips today."
    show kirako wink
    kirako "Very decent for your first day!"
    naomi happy "Thank you!"
    show kirako happy
    kirako "Any questions for me?"
    naomi troubled "Ummm, actually."
    naomi thinking "I can't quite remember what was the arrangement for me to be here..."
    naomi pain "(In fact I can't remember anything.)"
    naomi troubled "Did my mother...?"
    show kirako pout
    kirako "Oh my. I don't remember so well myself, truthfully!"
    kirako "Something about living away from home, experiencing city life..."
    show kirako wink
    kirako "It's alright, you're already here."
    show kirako happy
    kirako "Just come help out whenever you feel like it."
    kirako "You can spend the rest of your time exploring the city."
    naomi surprised "But the cafe."
    naomi thinking "Is there anything I can do to help?"
    show kirako pout
    kirako "Oh darling, that's so sweet of you!"
    show kirako wink
    kirako "You don't have to worry about that."
    show kirako happy
    kirako "I'll think of a way to save the cafe."
    naomi relieved "...Alright."
    show kirako happy
    kirako "Come on, you must be tired. I'll bring you up to your room."
    # show kirako pout
    # kirako "If you need some cash, you can work a shift or two in the cafe."
    # show kirako happy
    # kirako "Talking to customers will help you find a job!"
    # naomi thinking "I see!" 
    # naomi happy "I'll do my best to find a job soon!"
    # show kirako pout
    # kirako "Oh darling, you must be so tired after the long journey."
    # show kirako happy
    # kirako "Let me bring you up to your room."
    # naomi relieved "(Finally! Some rest.)"
    hide kirako with moveoutleft
    $ timeslot -= 1
    stop music fadeout 3
    jump re_evening_time

