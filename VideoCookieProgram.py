
#Video game and Cookie program

video_game = input("What video game should we play? ")
print("Ok, "+ video_game.title() + " is a fun game.\n")

cookie_type = 'Chocolate Cookies'
if (cookie_type.lower() == 'chocolate cookies'):
    print("I love chocolate cookies!")

#Enter a numberical value (For Example, 10 instead of "ten")
bake_timer = input("How many minutes does it take to bake cookies? ")
bake_timer = int(bake_timer)

waiting = True
while waiting:
    if bake_timer == 0:
        waiting = False
    else:
        print("Timer: " + str(bake_timer))
        bake_timer -= 1 #This means bake_timer = bake_timer  -1

print("\nLet's play " + video_game.tilte() + "now!")

    
