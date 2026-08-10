# Tutorial mode for dept store

label dept_store:
    scene bg dept
    if encounters["merchant"] == 0:
        jump merchant_0
    call screen dept_store

label dept_only:
    scene bg dept
    call screen dept_store
    pause

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

label dept_exit:
    scene bg dept
    menu:
        "Leave":
            hide screen stationery_counter
            hide screen accessories_counter
            hide screen clothes_counter
            hide screen cosmetics_counter
            hide screen dept_store
            $ timeslot -= 1
            if dayofweeknumber > 5:
                return
            else:
                if timeslot == 1:
                    jump ginza_small
                if timeslot < 1:
                    jump evening_time
        "Stay":
            hide screen stationery_counter
            hide screen accessories_counter
            hide screen clothes_counter
            hide screen cosmetics_counter
            jump dept_only

label stationery_section:
    call screen stationery_counter
    pause

label purchase_pen:
    show screen stationery_counter
    menu:
        staff_bubble "An exquisitely-made fountain pen with a firm grip."
        "Buy." if money >= 5:
            $ money -= 5
            $ inventory.append("pen")
            $ stationery.remove("pen")
            jump stationery_section
        "Don't buy.":
            jump stationery_section

label purchase_notebook:
    show screen stationery_counter
    menu:
        staff_bubble "A notebook with a beautifully illustrated cover and creamy lined pages."
        "Buy." if money >= 5:
            $ money -= 5
            $ inventory.append("notebook")
            $ stationery.remove("notebook")
            jump stationery_section
        "Don't buy.":
            jump stationery_section

label accessories_section:
    # scene counter_bg
    # show screen accessories_counter
    # pause
    call screen accessories_counter
    pause

label purchase_hair_bow:
    show screen accessories_counter
    show staff happy
    window hide
    menu:
        staff_bubble "This Western-style bow for 5 yen is very popular recently!"
        "Buy." if money >=5:
            $ money -= 5
            $ wardrobe_hair.update({"hair_bow":[1608,700]})
            $ accessories.remove("hair_bow")
            jump accessories_section
        "Don't buy.":
            jump accessories_section

label purchase_hair_hat:
    show screen accessories_counter
    menu:
        staff_bubble "This hat goes well with Western-style dresses, for 5 yen."
        "Buy." if money >=5:
            $ money -= 5
            $ wardrobe_hair.update({"hair_hat":[1565,335]})
            $ accessories.remove("hair_hat")
            jump accessories_section
        "Don't buy.":
            jump accessories_section

label purchase_hair_band:
    show screen accessories_counter
    menu:
        staff_bubble "A touch of glamour that keeps your hair in place while dancing, for 5 yen."
        "Buy." if money >=5:
            $ money -= 5
            $ wardrobe_hair.update({"hair_band":[1584,440]})
            $ accessories.remove("hair_band")
            jump accessories_section
        "Don't buy.":
            jump accessories_section

label purchase_hair_ribbon:
    show screen accessories_counter
    menu:
        staff_bubble "This velvet ribbon for 5 yen was imported from England."
        "Buy." if money >=5:
            $ money -= 5
            $ wardrobe_hair.update({"hair_ribbon":[1342,484]})
            $ accessories.remove("hair_ribbon")
            jump accessories_section
        "Don't buy.":
            jump accessories_section

label purchase_hair_flower:
    show screen accessories_counter
    menu:
        staff_bubble "A pretty silk flower to decorate your hair for 5 yen. It won't wilt!"
        "Buy." if money >=5:
            $ money -= 5
            $ wardrobe_hair.update({"hair_flower":[1484,620]})
            $ accessories.remove("hair_flower")
            jump accessories_section
        "Don't buy.":
            jump accessories_section

label purchase_hand_round:
    show screen accessories_counter
    menu:
        staff_bubble "A fashionable round leather handbag for 10 yen."
        "Buy." if money >=10:
            $ money -= 10
            $ wardrobe_accessories.append("hand_round")
            $ accessories.remove("hand_round")
            jump accessories_section
        "Don't buy.":
            jump accessories_section

label purchase_hand_evening:
    show screen accessories_counter
    menu:
        staff_bubble "An elegant evening clutch for 10 yen."
        "Buy." if money >=10:
            $ money -= 10
            $ wardrobe_accessories.append("hand_evening")
            $ accessories.remove("hand_evening")
            jump accessories_section
        "Don't buy.":
            jump accessories_section

label purchase_hand_straw:
    show screen accessories_counter
    menu:
        staff_bubble "A sturdy straw bag for 10 yen."
        "Buy." if money >=10:
            $ money -= 10
            $ wardrobe_accessories.append("hand_straw")
            $ accessories.remove("hand_straw")
            jump accessories_section
        "Don't buy.":
            jump accessories_section

label purchase_hand_parasol:
    show screen accessories_counter
    menu:
        staff_bubble "A parasol with delicate blue embroidery for 10 yen."
        "Buy." if money >=10:
            $ money -= 10
            $ wardrobe_parasol.append("hand_parasol")
            $ accessories.remove("hand_parasol")
            jump accessories_section
        "Don't buy.":
            jump accessories_section

label purchase_shoes_koppori:
    show screen accessories_counter
    menu:
        staff_bubble "Laminated wooden slippers which elevates your kimono, for 5 yen."
        "Buy." if money >=5:
            $ money -= 5
            $ wardrobe_shoes.append("shoes_koppori")
            $ accessories.remove("shoes_koppori")
            jump accessories_section
        "Don't buy.":
            jump accessories_section

label purchase_shoes_zori:
    show screen accessories_counter
    menu:
        staff_bubble "Sturdy straw slippers which last a long time, for 5 yen."
        "Buy." if money >=5:
            $ money -= 5
            $ wardrobe_shoes.append("shoes_zori")
            $ accessories.remove("shoes_zori")
            jump accessories_section
        "Don't buy.":
            jump accessories_section

label purchase_shoes_heels:
    show screen accessories_counter
    menu:
        staff_bubble "Western-style shoes for an evening out, for 5 yen."
        "Buy." if money >=5:
            $ money -= 5
            $ wardrobe_shoes.append("shoes_heels")
            $ accessories.remove("shoes_heels")
            jump accessories_section
        "Don't buy.":
            jump accessories_section

label purchase_shoes_pumps:
    show screen accessories_counter
    menu:
        staff_bubble "Shoes that can be used everyday by the modern woman, for 5 yen."
        "Buy." if money >=5:
            $ money -= 5
            $ wardrobe_shoes.append("shoes_pumps")
            $ accessories.remove("shoes_pumps")
            jump accessories_section
        "Don't buy.":
            jump accessories_section

label purchase_shoes_boots:
    show screen accessories_counter
    menu:
        staff_bubble "Sturdy Western-style boots that will protect your feet, for 5 yen."
        "Buy." if money >=5:
            $ money -= 5
            $ wardrobe_shoes.append("shoes_boots")
            $ accessories.remove("shoes_boots")
            jump accessories_section
        "Don't buy.":
            jump accessories_section

label clothes_section:
    call screen clothes_counter
    pause

label purchase_dress_cute:
    show screen clothes_counter
    menu:
        staff_bubble "A kimono with a refreshing blue print, just right for a walk in late spring, for 25 yen."
        "Buy." if money >= 25:
            $ money -= 25
            $ wardrobe_dress.append("dress_cute")
            $ clothes.remove("dress_cute")
            jump clothes_section
        "Don't buy.":
            jump clothes_section

label purchase_dress_hakama:
    show screen clothes_counter
    menu:
        staff_bubble "A hakama with a trendy print, easy to move around in, for 25 yen."
        "Buy." if money >= 25:
            $ money -= 25
            $ wardrobe_dress.append("dress_hakama")
            $ clothes.remove("dress_hakama")
            jump clothes_section
        "Don't buy.":
            jump clothes_section

label purchase_dress_modern:
    show screen clothes_counter
    menu:
        staff_bubble "A fashionable kimono with a bold and artistic print, for 25 yen."
        "Buy." if money >= 25:
            $ money -= 25
            $ wardrobe_dress.append("dress_modern")
            $ clothes.remove("dress_modern")
            jump clothes_section
        "Don't buy.":
            jump clothes_section

label purchase_dress_flapper:
    show screen clothes_counter
    menu:
        staff_bubble "A fashionable Western-style flapper dress for a night out at the dance club, for 25 yen."
        "Buy." if money >= 25:
            $ money -= 25
            $ wardrobe_dress.append("dress_flapper")
            $ clothes.remove("dress_flapper")
            jump clothes_section
        "Don't buy.":
            jump clothes_section

label purchase_dress_prim:
    show screen clothes_counter
    menu:
        staff_bubble "A modest Western-style dress for the modern girl, for 25 yen."
        "Buy." if money >= 25:
            $ money -= 25
            $ wardrobe_dress.append("dress_prim")
            $ clothes.remove("dress_prim")
            jump clothes_section
        "Don't buy.":
            jump clothes_section

label cosmetics_section:
    call screen cosmetics_counter
    pause

label purchase_shadow_blue:
    show screen cosmetics_counter
    menu:
        staff_bubble "Blue eyeshadow adds smoky depth and mystery, for 5 yen."
        "Buy." if money >= 5:
            $ money -= 5
            $ wardrobe_eye.append("shadow_blue")
            $ cosmetics.remove("shadow_blue")
            jump cosmetics_section
        "Don't buy.":
            jump cosmetics_section

label purchase_shadow_brown:
    show screen cosmetics_counter
    menu:
        staff_bubble "Brown eyeshadow lends warm and earthy tones, for 5 yen."
        "Buy." if money >= 5:
            $ money -= 5
            $ wardrobe_eye.append("shadow_brown")
            $ cosmetics.remove("shadow_brown")
            jump cosmetics_section
        "Don't buy.":
            jump cosmetics_section

label purchase_shadow_orange:
    show screen cosmetics_counter
    menu:
        staff_bubble "Orange eyeshadow lends vibrancy to the eyes, for 5 yen."
        "Buy." if money >= 5:
            $ money -= 5
            $ wardrobe_eye.append("shadow_orange")
            $ cosmetics.remove("shadow_orange")
            jump cosmetics_section
        "Don't buy.":
            jump cosmetics_section
            
label purchase_shadow_pink:
    show screen cosmetics_counter
    menu:
        staff_bubble "Pink eyeshadow adds a touch of color and femininity, for 5 yen."
        "Buy." if money >= 5:
            $ money -= 5
            $ wardrobe_eye.append("shadow_pink")
            $ cosmetics.remove("shadow_pink")
            jump cosmetics_section
        "Don't buy.":
            jump cosmetics_section

label purchase_stick_orange:
    show screen cosmetics_counter
    menu:
        staff_bubble "Orange lipstick adds a natural sun-kissed glow, for 5 yen."
        "Buy." if money >= 5:
            $ money -= 5
            $ wardrobe_lip.append("stick_orange")
            $ cosmetics.remove("stick_orange")
            jump cosmetics_section
        "Don't buy.":
            jump cosmetics_section

label purchase_stick_peach:
    show screen cosmetics_counter
    menu:
        staff_bubble "Peach lipstick creates a warm and natural look, for 5 yen."
        "Buy." if money >= 5:
            $ money -= 5
            $ wardrobe_lip.append("stick_peach")
            $ cosmetics.remove("stick_peach")
            jump cosmetics_section
        "Don't buy.":
            jump cosmetics_section

label purchase_stick_pink:
    show screen cosmetics_counter
    menu:
        staff_bubble "Pink lipstick evokes a soft and feminine feeling, for 5 yen."
        "Buy." if money >= 5:
            $ money -= 5
            $ wardrobe_lip.append("stick_pink")
            $ cosmetics.remove("stick_pink")
            jump cosmetics_section
        "Don't buy.":
            jump cosmetics_section

label purchase_stick_red:
    show screen cosmetics_counter
    menu:
        staff_bubble "Red lipstick exudes glamour and confidence, for 5 yen."
        "Buy." if money >= 5:
            $ money -= 5
            $ wardrobe_lip.append("stick_red")
            $ cosmetics.remove("stick_red")
            jump cosmetics_section
        "Don't buy.":
            jump cosmetics_section

label purchase_blush_pink:
    show screen cosmetics_counter
    menu:
        staff_bubble "Pink blush enhances the natural flush of the skin, for 5 yen."
        "Buy." if money >= 5:
            $ money -= 5
            $ wardrobe_cheek.append("blush_pink")
            $ cosmetics.remove("blush_pink")
            jump cosmetics_section
        "Don't buy.":
            jump cosmetics_section

label purchase_blush_orange:
    show screen cosmetics_counter
    menu:
        staff_bubble "Orange blush brings a natural sun-kissed appearance, for 5 yen."
        "Buy." if money >= 5:
            $ money -= 5
            $ wardrobe_cheek.append("blush_orange")
            $ cosmetics.remove("blush_orange")
            jump cosmetics_section
        "Don't buy.":
            jump cosmetics_section