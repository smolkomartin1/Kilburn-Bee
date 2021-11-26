# Game resolution: 1440x900
# Tested on 2560x1440 with both 150% and 125% scaling
# Bee assets curtesy of cobectbhax, licensed under regular license (code:d5cd4b82-ce71-42c3-9dcf-879cd12fa689)
# Brick assets curtesy of Robert Brooks, licensed under standard license
# Screenshot of Microsoft Office 365 Excel not endorsed by Microsoft
# All other game assets are made by me, Martin Smolko and can be used freely as a part of public domain

from tkinter import Tk, Canvas, PhotoImage, Button, Entry, font
from time import sleep
from random import randint
from os import path, remove


def jump(event):
    global jumped
    jumped = True


def save():
    global saving
    saving = True


def cheat(event):
    global slowmo
    slowmo = not slowmo


def homepage():
    # creates background witt logo and all the buttons
    global homepageScreen
    homepageScreen = []
    homepageScreen.append(canvas.create_image(0, 0, image=blacknessImage, anchor="nw"))
    homepageScreen.append(canvas.create_image(720, 240, image=logoImage))
    # if there exists a save file than it is loaded
    if path.exists("savefile.txt"):
        homepageScreen.append(
            Button(window, text="Continue", image=bigbuttonImage, font=buttonFont, command=start, compound="center",
                   fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040",
                   highlightthickness=0, bd=0))
    # otherwise show option for a new session
    else:
        homepageScreen.append(
            Button(window, text="New Game", image=bigbuttonImage, font=buttonFont, command=start, compound="center",
                   fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040",
                   highlightthickness=0, bd=0))
    homepageScreen.append(
        Button(window, text="Settings", image=buttonImage, font=buttonFont, command=settings, compound="center",
               fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040", highlightthickness=0,
               bd=0))
    homepageScreen.append(
        Button(window, text="Exit", image=buttonImage, font=buttonFont, command=window.destroy, compound="center",
               fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040", highlightthickness=0,
               bd=0))
    homepageScreen[2].place(x=720, y=520, anchor="center")
    homepageScreen[3].place(x=720, y=650, anchor="center")
    homepageScreen[4].place(x=720, y=770, anchor="center")
    canvas.update()


def start():
    # responsible for starting the game and removing all elements from homepage
    # also used for restarting the game (removes all elements from leaderboard)
    global homepageScreen, leaderboardScreen, inhomepage, inleaderboard, honeycomb, score
    if "homepageScreen" in globals():
        for i in homepageScreen:
            if type(i) == Button:
                i.destroy()
            else:
                canvas.delete(i)
        del homepageScreen
    elif "leaderboardScreen" in globals():
        for i in leaderboardScreen:
            if type(i) == Button:
                i.destroy()
            else:
                canvas.delete(i)
        # removes previous score and most importantly piping (via tags, not variables)
        canvas.delete("honeycombtag")
        canvas.delete("scoretag")
        canvas.delete("piping")
        del leaderboardScreen
    # initializes bee to starting position
    inhomepage = inleaderboard = False
    canvas.coords(bee, 250, 450)
    canvas.itemconfigure(bee, image=beeImages[7])
    game()


def pause(event):
    # game cannot be paused during and of the static pages (game already at a halt + buttons overlapping)
    # also cannot be (un)paused when boss key is on (results in game over if accidentally pressed)
    global paused, pauseScreen, bossed, homepageScreen, inhomepage, inleaderboard, insettings
    if inhomepage is False and inleaderboard is False and insettings is False and "excel" not in globals():
        paused = not paused
        if "pauseScreen" not in globals():
            global pauseScreen
            pauseScreen = []
            pauseScreen.append(canvas.create_image(0, 0, image=blacknessImage, anchor="nw"))
            pauseScreen.append(canvas.create_text(720, 200, fill="white", font="Impact 80", text="PAUSED"))
            pauseScreen.append(canvas.create_rectangle(660, 300, 710, 400, fill="white"))
            pauseScreen.append(canvas.create_rectangle(730, 300, 780, 400, fill="white"))
            pauseScreen.append(canvas.create_text(720, 750, fill="white", font="Impact 40",
                                                  text=f"Press {str(bindings[1])[1:-1].upper()} to continue"))
            pauseScreen.append(
                Button(window, text="Settings", image=buttonImage, font=buttonFont, command=settings, compound="center",
                       fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040",
                       highlightthickness=0, bd=0))
            pauseScreen.append(
                Button(window, text="Save", image=buttonImage, font=buttonFont, command=save, compound="center",
                       fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040",
                       highlightthickness=0, bd=0))
            pauseScreen.append(Button(window, text="Exit", image=buttonImage, font=buttonFont, command=window.destroy,
                                      compound="center", fg="white", activeforeground="#fbb040", bg="#404040",
                                      activebackground="#404040", highlightthickness=0, bd=0))
            pauseScreen[5].place(x=570, y=500, anchor="center")
            pauseScreen[6].place(x=870, y=500, anchor="center")
            pauseScreen[7].place(x=720, y=620, anchor="center")
        # remove all elements of pause screen when unpaused
        else:
            for i in pauseScreen:
                if type(i) == Button:
                    i.destroy()
                else:
                    canvas.delete(i)
            del pauseScreen


def settings():
    # hides all elements of screens which it overlays
    global settingsScreen, homepageScreen, insettings
    insettings = True
    settingsScreen = []
    settingsScreen.append(canvas.create_image(720, 450, image=leaderboardImage))
    if "homepageScreen" in globals():
        for b in range(2, len(homepageScreen)):
            homepageScreen[b].place_forget()
        canvas.tag_lower(homepageScreen[1])
    if "leaderboardScreen" in globals():
        if "leaderboardScreen" in globals() and intopfive is True:
            leaderboardScreen[len(leaderboardScreen) - 1].place_forget()
        elif "leaderboardScreen" in globals() and intopfive is False:
            leaderboardScreen[len(leaderboardScreen) - 3].place_forget()
            leaderboardScreen[len(leaderboardScreen) - 2].place_forget()
            leaderboardScreen[len(leaderboardScreen) - 1].place_forget()
    if "pauseScreen" in globals():
        for b in range(5, len(pauseScreen)):
            pauseScreen[b].place_forget()
    # after all checks places its own elements
    settingsScreen.append(canvas.create_text(420, 150, fill="white", font="Impact 40", text="Jump:", anchor="nw"))
    settingsScreen.append(canvas.create_text(420, 290, fill="white", font="Impact 40", text="Pause:", anchor="nw"))
    settingsScreen.append(canvas.create_text(420, 430, fill="white", font="Impact 40", text="Boss key:", anchor="nw"))
    settingsScreen.append(canvas.create_text(420, 570, fill="white", font="Impact 40", text="Cheat code:", anchor="nw"))
    settingsScreen.append(
        Button(window, text=bindings[0], image=buttonImage, font=buttonFont, command=lambda: buttonColorChanger(5),
               compound="center", fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040",
               highlightthickness=0, bd=0))
    settingsScreen.append(
        Button(window, text=bindings[1], image=buttonImage, font=buttonFont, command=lambda: buttonColorChanger(6),
               compound="center", fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040",
               highlightthickness=0, bd=0))
    settingsScreen.append(
        Button(window, text=bindings[2], image=buttonImage, font=buttonFont, command=lambda: buttonColorChanger(7),
               compound="center", fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040",
               highlightthickness=0, bd=0))
    settingsScreen.append(
        Button(window, text=bindings[3], image=buttonImage, font=buttonFont, command=lambda: buttonColorChanger(8),
               compound="center", fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040",
               highlightthickness=0, bd=0))
    settingsScreen.append(
        Button(window, text="Back", image=buttonImage, font=buttonFont, command=settingsClosed, compound="center",
               fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040", highlightthickness=0,
               bd=0))
    settingsScreen[5].place(x=900, y=185, anchor="center")
    settingsScreen[6].place(x=900, y=325, anchor="center")
    settingsScreen[7].place(x=900, y=465, anchor="center")
    settingsScreen[8].place(x=900, y=605, anchor="center")
    settingsScreen[9].place(x=720, y=735, anchor="center")


def buttonColorChanger(number):
    # provides user feedback that it awaits assignment of a key
    global settingsScreen
    settingsScreen[number].config(text="Press any key", fg="#fbb040")
    for i in range(4):
        window.unbind(bindings[i])
    window.bind("<Key>", lambda x: bindingChanger(x, number))


def bindingChanger(event, number):
    # sets up new binding
    global settingsScreen, pauseScreen
    pressedKey = f"<{event.keysym}>"
    if pressedKey in bindings:
        settingsScreen[number].config(text="Already used")
    else:
        settingsScreen[number].config(text=pressedKey, fg="white")
    bindings[number - 5] = pressedKey
    # pause screen has call to action so the button needs to be changed appropiately
    if "pauseScreen" in globals():
        canvas.itemconfigure(pauseScreen[4], text=f"Press {str(bindings[1])[1:-1].upper()} to continue")
    binder(bindings)


def binder(bindings):
    # saves bindings to a local file
    window.bind(bindings[0], jump)
    window.bind(bindings[1], pause)
    window.bind(bindings[2], boss)
    window.bind(bindings[3], cheat)
    with open("bindings.txt", "w") as bindfile:
        bindfile.write(str(bindings)[1:-1])


def settingsClosed():
    # takes care of clossing the settings panel
    global settingsScreen, insettings
    insettings = False
    for i in settingsScreen:
        if type(i) == Button:
            i.destroy()
        else:
            canvas.delete(i)
    del settingsScreen
    if "homepageScreen" in globals():
        homepageScreen[2].place(x=720, y=520, anchor="center")
        homepageScreen[3].place(x=720, y=650, anchor="center")
        homepageScreen[4].place(x=720, y=770, anchor="center")
        # shows up hidden logo
        canvas.tag_raise(homepageScreen[1])
    elif "pauseScreen" in globals():
        pauseScreen[5].place(x=570, y=500, anchor="center")
        pauseScreen[6].place(x=870, y=500, anchor="center")
        pauseScreen[7].place(x=720, y=620, anchor="center")
    elif "leaderboardScreen" in globals() and intopfive is True:
        leaderboardScreen[len(leaderboardScreen) - 1].place(x=725, y=810, anchor="center")
    elif "leaderboardScreen" in globals() and intopfive is False:
        leaderboardScreen[len(leaderboardScreen) - 3].place(x=575, y=700, anchor="center")
        leaderboardScreen[len(leaderboardScreen) - 2].place(x=875, y=700, anchor="center")
        leaderboardScreen[len(leaderboardScreen) - 1].place(x=725, y=800, anchor="center")


def boss(event):
    global bossed, paused, excel, pauseScreen, homepageScreen, leaderboardScreen, settingsScreen, intopfive
    if bossed is False:
        bossed = True
        # makes sure that game is paused when boss key is pressed
        if paused is False:
            pause(0)
        global excel
        # removes buttons from screne and makes the app window change title and icon (Windows only)
        excel = canvas.create_image(0, 0, image=excelImage, anchor="nw")
        window.title("Excel - Financial Report Q4 2021")
        window.iconbitmap("assets/excelIcon.ico")
        if "settingsScreen" in globals():
            for b in range(5, len(settingsScreen)):
                settingsScreen[b].place_forget()
        elif "homepageScreen" in globals():
            for b in range(2, len(homepageScreen)):
                homepageScreen[b].place_forget()
        elif "pauseScreen" in globals():
            for b in range(5, len(pauseScreen)):
                pauseScreen[b].place_forget()
        elif "leaderboardScreen" in globals() and intopfive is True:
            leaderboardScreen[len(leaderboardScreen) - 1].place_forget()
        elif "leaderboardScreen" in globals() and intopfive is False:
            leaderboardScreen[len(leaderboardScreen) - 3].place_forget()
            leaderboardScreen[len(leaderboardScreen) - 2].place_forget()
            leaderboardScreen[len(leaderboardScreen) - 1].place_forget()
    else:
        # removes the spreadsheet and shows hidden buttons
        bossed = False
        canvas.delete(excel)
        del excel
        # changes back to the original title
        window.title("Kilburn Bee")
        window.iconbitmap("assets/bee.ico")
        if "settingsScreen" in globals():
            settingsScreen[5].place(x=900, y=185, anchor="center")
            settingsScreen[6].place(x=900, y=325, anchor="center")
            settingsScreen[7].place(x=900, y=465, anchor="center")
            settingsScreen[8].place(x=900, y=605, anchor="center")
            settingsScreen[9].place(x=720, y=735, anchor="center")
        elif "homepageScreen" in globals():
            homepageScreen[2].place(x=720, y=520, anchor="center")
            homepageScreen[3].place(x=720, y=650, anchor="center")
            homepageScreen[4].place(x=720, y=770, anchor="center")
        elif "pauseScreen" in globals():
            pauseScreen[5].place(x=570, y=500, anchor="center")
            pauseScreen[6].place(x=870, y=500, anchor="center")
            pauseScreen[7].place(x=720, y=620, anchor="center")
        elif "leaderboardScreen" in globals() and intopfive is True:
            leaderboardScreen[len(leaderboardScreen) - 1].place(x=725, y=810, anchor="center")
        elif "leaderboardScreen" in globals() and intopfive is False:
            leaderboardScreen[len(leaderboardScreen) - 3].place(x=575, y=700, anchor="center")
            leaderboardScreen[len(leaderboardScreen) - 2].place(x=875, y=700, anchor="center")
            leaderboardScreen[len(leaderboardScreen) - 1].place(x=725, y=800, anchor="center")
    canvas.update()


def leaderboard(scoreValue):
    global leaderboardScreen, intopfive, inleaderboard
    intopfive = False
    inleaderboard = True
    place = 0
    leaderboardScreen.append(canvas.create_image(725, 520, image=leaderboardImage))
    leaderboardScreen.append(canvas.create_image(725, 471, image=leaderboardWindowImage))
    leaderboardScreen.append(canvas.create_image(725, 240, image=bigbuttonImage))
    leaderboardScreen.append(canvas.create_text(725, 240, fill="white", font="Impact 45", text="Top 5"))
    for i in range(len(top5)):
        # if we haven't found a higher score or have found one
        if int(top5[i][0]) > scoreValue or intopfive is True:
            # if we found one, then we need to move the table by one person
            if intopfive is True:
                a = i - 1
            else:
                a = i
            leaderboardScreen.append(
                canvas.create_text(445, 310 + i * 65, fill="#444444", font="Impact 35", text=top5[a][1], anchor="nw"))
            if i == 0:
                leaderboardScreen.append(
                    canvas.create_text(1000, 310 + i * 65, fill="#ffd700", font="Impact 35", text=top5[a][0],
                                       anchor="ne"))
            elif i == 1:
                leaderboardScreen.append(
                    canvas.create_text(1000, 310 + i * 65, fill="#c0c0c0", font="Impact 35", text=top5[a][0],
                                       anchor="ne"))
            elif i == 2:
                leaderboardScreen.append(
                    canvas.create_text(1000, 310 + i * 65, fill="#cd7f32", font="Impact 35", text=top5[a][0],
                                       anchor="ne"))
            else:
                leaderboardScreen.append(
                    canvas.create_text(1000, 310 + i * 65, fill="#444444", font="Impact 35", text=top5[a][0],
                                       anchor="ne"))
        # if score higher then one of the top 5 scores, then text box will appear on the same position
        elif intopfive is False:
            name = Entry(window, fg="#444444", font="Impact 35", width=18, bd=0)
            leaderboardScreen.append(canvas.create_window(445, 310 + i * 65, window=name, anchor="nw"))
            place = i
            intopfive = True
    # makes sure that even if the number is not bigger, it will be put in if there are less then 5 entries
    if len(top5) < 5:
        name = Entry(window, fg="#444444", font="Impact 35", width=18, bd=0)
        place = len(top5)
        leaderboardScreen.append(canvas.create_window(445, 310 + (place * 65), window=name, anchor="nw"))
        intopfive = True
    # call to action to submit name
    if intopfive is True:
        leaderboardScreen.append(canvas.create_text(725, 700, fill="white", font="Impact 25",
                                                    text=f"Congratulation!\nYou are number {place + 1} in our leaderboard!\nPlease, type in your name (16 characters max)",
                                                    justify="center"))
        leaderboardScreen.append(Button(window, text="Submit", image=buttonImage, font=buttonFont,
                                        command=lambda: storeRecord(scoreValue, place, name), compound="center",
                                        fg="white", activeforeground="#fbb040", bg="#404040",
                                        activebackground="#404040", highlightthickness=0, bd=0))
        leaderboardScreen[len(leaderboardScreen) - 1].place(x=725, y=810, anchor="center")
    else:
        leaderboardButtons()


def storeRecord(scoreValue, place, name):
    # after submission it will be saved to a file and displayed
    global leaderboardScreen, intopfive
    intopfive = False
    nametoadd = name.get()
    # prohibits names larger than 16 characters
    if len(nametoadd) >= 16:
        top5.insert(place, [int(scoreValue), nametoadd[:16]])
    # blank name fields caused problems, so is substituted by a dash
    elif len(nametoadd) == 0:
        top5.insert(place, [int(scoreValue), "-"])
    else:
        top5.insert(place, [int(scoreValue), nametoadd])
    top5.pop(5)
    with open("leaderboard.txt", "w") as saving_savefile:
        for x in top5:
            saving_savefile.write(f"{x[0]} {x[1]}\n")
    # deletes old entries and show new ones
    name.destroy()
    canvas.delete(leaderboardScreen[len(leaderboardScreen) - 2])
    leaderboardScreen[len(leaderboardScreen) - 1].destroy()
    leaderboardScreen.append(
        canvas.create_text(445, 311 + place * 65, fill="#444444", font="Impact 35", text=top5[place][1], anchor="nw"))
    if place == 0:
        leaderboardScreen.append(
            canvas.create_text(1000, 311 + place * 65, fill="#ffd700", font="Impact 35", text=top5[place][0],
                               anchor="ne"))
    elif place == 1:
        leaderboardScreen.append(
            canvas.create_text(1000, 311 + place * 65, fill="#c0c0c0", font="Impact 35", text=top5[place][0],
                               anchor="ne"))
    elif place == 2:
        leaderboardScreen.append(
            canvas.create_text(1000, 311 + place * 65, fill="#cd7f32", font="Impact 35", text=top5[place][0],
                               anchor="ne"))
    else:
        leaderboardScreen.append(
            canvas.create_text(1000, 311 + place * 65, fill="#444444", font="Impact 35", text=top5[place][0],
                               anchor="ne"))
    leaderboardButtons()


def leaderboardButtons():
    # shows orginal after submission or if the score wasn't better than one in the top 5
    global leaderboardScreen
    leaderboardScreen.append(
        Button(window, text="New Game", image=buttonImage, font=buttonFont, command=start, compound="center",
               fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040", highlightthickness=0,
               bd=0))
    leaderboardScreen.append(
        Button(window, text="Settings", image=buttonImage, font=buttonFont, command=settings, compound="center",
               fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040", highlightthickness=0,
               bd=0))
    leaderboardScreen.append(
        Button(window, text="Exit", image=buttonImage, font=buttonFont, command=window.destroy, compound="center",
               fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040", highlightthickness=0,
               bd=0))
    leaderboardScreen[len(leaderboardScreen) - 3].place(x=575, y=700, anchor="center")
    leaderboardScreen[len(leaderboardScreen) - 2].place(x=875, y=700, anchor="center")
    leaderboardScreen[len(leaderboardScreen) - 1].place(x=725, y=800, anchor="center")


def plusone(pipes, scoreValue):
    # adds +1 to score if bee successfully overcomes the whole pipe
    global scoring
    if scoring is True and canvas.coords(pipes[0][0])[0] + 160 < canvas.coords(bee)[0]:
        scoring = False
        return scoreValue + 1
    return scoreValue


def generatePipes(amount, distancePipes, sizeOpening):
    genPipes = []
    # used for parallex effect
    if amount == 1:
        opening = randint(50, 550)
        genPipes.append(canvas.create_image(distancePipes, opening, image=reverseObstacles[randint(0, 3)], anchor="sw",
                                            tags="piping"))
        genPipes.append(
            canvas.create_image(distancePipes, opening + sizeOpening, image=obstacles[randint(0, 3)], anchor="nw",
                                tags="piping"))
    # generates pipes at start of the game
    else:
        for p in range(amount):
            pair = []
            opening = randint(50, 550)
            pair.append(canvas.create_image(1200 + distancePipes * p, opening, image=reverseObstacles[randint(0, 3)],
                                            anchor="sw", tags="piping"))
            pair.append(
                canvas.create_image(1200 + distancePipes * p, opening + sizeOpening, image=obstacles[randint(0, 3)],
                                    anchor="nw", tags="piping"))
            genPipes.append(pair)
    return genPipes


def collision(pipes):
    global scoring
    beeCoords = canvas.coords(bee)
    # checks just the first pipe, if pipe distance too short than add a for loop
    pipeTop = canvas.coords(pipes[0][0])
    if (pipeTop[0] + 160) >= beeCoords[0] >= (pipeTop[0] - 48):
        scoring = True
        if (beeCoords[1] - 80) <= pipeTop[1] or (pipeTop[1] + 300) <= beeCoords[1]:
            return True
    return False


def game():
    # the game itself occurs inside this function
    global jumped, paused, scoring, saving, pauseScreen, leaderboardScreen, slowmo
    # sets default values for every stage
    scoreValue = 0
    distanceBetweenPipes = 550
    sizePipeOpening = 300
    gravity = 0.3
    pipes = generatePipes(4, distanceBetweenPipes, sizePipeOpening)
    honeycomb = canvas.create_image(600, 70, image=honeycombImage, tags="honeycombtag")
    score = canvas.create_text(615, 75, fill="#fbb040", font="Impact 50", text=f"Score: {scoreValue}", anchor="nw",
                               tags="scoretag")
    # if there exists a save file than we load values from last saved session
    if path.exists("savefile.txt"):
        settings = []
        jumped = False
        with open("savefile.txt") as file:
            for line in file:
                settings.append(line.replace("\n", ""))
        scoreValue = int(settings[0])
        # casting string "False" as boolean will result in true (empty string is a false boolean)
        scoring = bool("" if settings[1] == "False" else settings[1])
        speed = float(settings[2])
        animation = float(settings[3])
        hit = bool("" if settings[4] == "False" else settings[4])
        dead = bool("" if settings[4] == "False" else settings[4])
        # moves the pipes to their previous locations
        for z in range(4):
            canvas.coords(pipes[z][0], float(settings[6 + (z * 2)]), float(settings[7 + (z * 2)]))
            canvas.coords(pipes[z][1], float(settings[6 + (z * 2)]), float(settings[7 + (z * 2)]) + 300)
        canvas.itemconfigure(score, text=f"Score: {scoreValue}")
        pause(0)
    # if save file is not present then we load default values
    else:
        scoring = False
        speed = 0
        animation = 15
        hit = False
        dead = False
    # the game loops forever until the bee falls to the ground
    while canvas.coords(bee)[1] < 900:
        # if paused then main body of the loop is disconnected and therefore no movement occurs
        if paused is False:
            # if bee touches the pipe then player looses control of the bee and it halts
            if hit is False:
                if jumped is True:
                    speed = -9
                    jumped = False
                    animation = 0
                # takes care of wing flapping animation
                if animation <= 14 or animation % 2 == 0:
                    canvas.itemconfigure(bee, image=beeImages[int(animation) // 2])
                    animation += 1
                for i in range(len(pipes)):
                    canvas.move(pipes[i][0], -7, 0)
                    canvas.move(pipes[i][1], -7, 0)
                # If pipe out of screen then generate new one
                if canvas.coords(pipes[0][0])[0] < -140:
                    canvas.delete(pipes.pop(0))
                    newPipe = generatePipes(1, canvas.coords(pipes[len(pipes) - 1][0])[0] + distanceBetweenPipes,
                                            sizePipeOpening)
                    pipes.append(newPipe)
                    canvas.tag_raise(honeycomb)
                    canvas.tag_raise(score)
                hit = collision(pipes)
                # if bee successfully passed through a pipe than score is updated
                if scoring is True:
                    scoreValue = plusone(pipes, scoreValue)
                    canvas.itemconfigure(score, text=f"Score: {scoreValue}")
            # if bee hit a pipe then we let it fall down
            elif hit is True and dead is False:
                canvas.itemconfigure(bee, image=beeDead)
                canvas.tag_raise(bee)
                dead = True
            canvas.move(bee, 0, speed)
            canvas.update()
            # our slow motion cheat code slows the refesh speed (without any delay the bee falls striaght down)
            if slowmo is False:
                sleep(0.011)
            else:
                sleep(0.1)
            # if bee has fallen then make it lay above the ground (it can fall through the canvas)
            if canvas.coords(bee)[1] > 900:
                canvas.itemconfigure(bee, image=beeDead)
                canvas.coords(bee, 250, 900)
                canvas.tag_raise(bee)
            # if bee is unrestricted than apply gravitional constant and continue
            canvas.coords(bee)[1] += speed
            speed += gravity
        else:
            # creates a save file (saves just upper pipe, other is calculated through size of the opening)
            if saving is True:
                with open("savefile.txt", "w") as save_file:
                    save_file.write(f"{scoreValue}\n{scoring}\n{speed}\n{animation}\n{hit}\n{dead}\n")
                    for p in pipes:
                        save_file.write(f"{canvas.coords(p[0])[0]}\n")
                        save_file.write(f"{canvas.coords(p[0])[1]}\n")
                saving = False
                pauseScreen[6].config(text="Saved!")
            canvas.update()
    # if bee has fallen then remove the savefile (to prevent save scumming)
    if path.exists("savefile.txt"):
        remove("savefile.txt")
    for a in range(len(pipes)):
        canvas.delete(pipes.pop(0))
    # makes the score show up through the black layer
    leaderboardScreen = []
    leaderboardScreen.append(canvas.create_image(0, 0, image=blacknessImage, anchor="nw"))
    canvas.tag_raise(honeycomb)
    canvas.tag_raise(score)
    leaderboard(scoreValue)

# sets up tkinter
window = Tk()
window.title("Kilburn Bee")
window.geometry("1440x900")
canvas = Canvas(window, width=1440, height=900)

# loads all the assets
logoImage = PhotoImage(file="assets/logo.png")
beeImages = [PhotoImage(file="assets/bee0.png"), PhotoImage(file="assets/bee1.png"), PhotoImage(file="assets/bee2.png"),
             PhotoImage(file="assets/bee3.png"), PhotoImage(file="assets/bee4.png"), PhotoImage(file="assets/bee5.png"),
             PhotoImage(file="assets/bee6.png"), PhotoImage(file="assets/bee7.png")]
beeDead = PhotoImage(file="assets/dead.png")
obstacles = [PhotoImage(file="assets/obstacle0.png"), PhotoImage(file="assets/obstacle1.png"),
             PhotoImage(file="assets/obstacle2.png"), PhotoImage(file="assets/obstacle3.png")]
reverseObstacles = [PhotoImage(file="assets/robstacle0.png"), PhotoImage(file="assets/robstacle1.png"),
                    PhotoImage(file="assets/robstacle2.png"), PhotoImage(file="assets/robstacle3.png")]
buttonImage = PhotoImage(file="assets/buttonImage.png")
bigbuttonImage = PhotoImage(file="assets/bigbuttonImage.png")
honeycombImage = PhotoImage(file="assets/honeycomb.png")
blacknessImage = PhotoImage(file="assets/blackness.png")
excelImage = PhotoImage(file="assets/excel.png")
kilburn = PhotoImage(file="assets/kilburn.png")
leaderboardImage = PhotoImage(file="assets/leaderboard.png")
leaderboardWindowImage = PhotoImage(file="assets/leaderboardwindow.png")
canvas.create_image(0, 0, image=kilburn, anchor="nw")
bee = canvas.create_image(250, 450, image=beeImages[7], anchor="s")
window.iconbitmap("assets/bee.ico")
buttonFont = font.Font(family="Impact", size=30)

# checks if necessary files exist and if not then it creates them
if path.exists("leaderboard.txt") is False:
    with open("leaderboard.txt", "w") as leaderboardfile2:
        for i in range(5):
            leaderboardfile2.write(str('0 -\n'))
with open("leaderboard.txt") as leaderboardfile:
    top5 = [row.strip().split() for row in leaderboardfile]
if path.exists("bindings.txt"):
    with open("bindings.txt") as bindingsfile:
        bindings = bindingsfile.readline().strip()[1:-1].split("', '")
else:
    bindings = ["<space>", "<Escape>", "<b>", "<c>"]

# boolean variables representing status of different actions
jumped = True
inhomepage = True
inleaderboard = False
insettings = False
paused = False
bossed = False
saving = False
slowmo = False

# starts the fun!
canvas.pack()
binder(bindings)
homepage()
window.mainloop()
