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