# Screen resolution: 1440x900
from tkinter import Tk, Canvas, PhotoImage, Button, font
from time import sleep
from random import randint
from os import path

def jump(event):
    global jumped
    jumped = True

def save():
    global saving
    saving = True

def homepage():
    global homepageList
    homepageList = []
    homepageList.append(canvas.create_image(0, 0, image=blacknessImage, anchor="nw"))
    homepageList.append(canvas.create_image(720, 240, image=logoImage))
    if path.exists("savefile.txt"):
        homepageList.append(Button(window, text="Continue", image=bigbuttonImage, font=buttonFont, command=start, compound="center", fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040", highlightthickness=0, bd=0))
    else:
        homepageList.append(Button(window, text="New Game", image=bigbuttonImage, font=buttonFont, command=start, compound="center", fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040", highlightthickness=0, bd=0))
    homepageList.append(Button(window, text="Settings", image=buttonImage, font=buttonFont, compound="center", fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040", highlightthickness=0, bd=0))
    homepageList.append(Button(window, text="Leaderboard", image=buttonImage, font=buttonFont, compound="center", fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040", highlightthickness=0, bd=0))
    homepageList.append(Button(window, text="Cheat Codes", image=buttonImage, font=buttonFont, compound="center", fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040", highlightthickness=0, bd=0))
    homepageList.append(Button(window, text="Exit", image=buttonImage, font=buttonFont, command=window.destroy, compound="center", fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040", highlightthickness=0, bd=0))
    homepageList[2].place(x=720, y=520, anchor="center")
    homepageList[3].place(x=420, y=650, anchor="center")
    homepageList[4].place(x=720, y=650, anchor="center")
    homepageList[5].place(x=1020, y=650, anchor="center")
    homepageList[6].place(x=720, y=770, anchor="center")
    canvas.update()

def start():
    global homepageList, inhomepage
    for i in homepageList:
        if type(i) == Button:
            i.destroy()
        else:
            canvas.delete(i)
    del homepageList
    inhomepage = False
    game()

def pause(event):
    global paused, pauseScreen, bossed, homepageList, inhomepage
    if inhomepage != True:
        paused = not paused
        if "pauseScreen" not in globals():
            global pauseScreen
            pauseScreen = []
            pauseScreen.append(canvas.create_image(0, 0, image=blacknessImage, anchor="nw"))
            pauseScreen.append(canvas.create_text(720, 200, fill="white", font="Impact 80", text="PAUSED"))
            pauseScreen.append(canvas.create_rectangle(660, 300, 710, 400, fill="white"))
            pauseScreen.append(canvas.create_rectangle(730, 300, 780, 400, fill="white"))
            pauseScreen.append(canvas.create_text(720, 750, fill="white", font="Impact 40", text="Press ESCAPE to continue"))
            pauseScreen.append(Button(window, text="Settings", image=buttonImage, font=buttonFont, compound="center", fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040", highlightthickness=0, bd=0))
            pauseScreen.append(Button(window, text="Save", image=buttonImage, font=buttonFont, command=save, compound="center", fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040", highlightthickness=0, bd=0))
            pauseScreen.append(Button(window, text="Cheat Codes", image=buttonImage, font=buttonFont, compound="center", fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040", highlightthickness=0, bd=0))
            pauseScreen.append(Button(window, text="Exit", image=buttonImage, font=buttonFont, command=window.destroy, compound="center", fg="white", activeforeground="#fbb040", bg="#404040", activebackground="#404040", highlightthickness=0, bd=0))
            pauseScreen[5].place(x=420, y=500, anchor="center")
            pauseScreen[6].place(x=720, y=500, anchor="center")
            pauseScreen[7].place(x=1020, y=500, anchor="center")
            pauseScreen[8].place(x=720, y=620, anchor="center")
        else:
            for i in pauseScreen:
                if type(i) == Button:
                    i.destroy()
                else:
                    canvas.delete(i)
            del pauseScreen

def boss(event):
    global bossed, paused, excel, pauseScreen, homepageList, inhomepage
    if bossed == False:
        bossed = True
        if paused != True:
            pause(0)
        global excel
        excel = canvas.create_image(0, 0, image=excelImage, anchor="nw")
        window.title("Excel - Financial Report Q4 2021")
        window.iconbitmap("assets/excelIcon.ico")
        if "pauseScreen" in globals():
            for b in range(5, len(pauseScreen)):
                pauseScreen[b].place_forget()
        elif "homepageList" in globals():
            for b in range(2, len(homepageList)):
                homepageList[b].place_forget()
    else:
        bossed = False
        canvas.delete(excel)
        del excel
        window.title("Kilburn Bee")
        window.iconbitmap("assets/bee.ico")
        if "pauseScreen" in globals():
            pauseScreen[5].place(x=420, y=500, anchor="center")
            pauseScreen[6].place(x=720, y=500, anchor="center")
            pauseScreen[7].place(x=1020, y=500, anchor="center")
            pauseScreen[8].place(x=720, y=620, anchor="center")
        elif "homepageList" in globals():
            homepageList[2].place(x=720, y=520, anchor="center")
            homepageList[3].place(x=420, y=650, anchor="center")
            homepageList[4].place(x=720, y=650, anchor="center")
            homepageList[5].place(x=1020, y=650, anchor="center")
            homepageList[6].place(x=720, y=770, anchor="center")
    canvas.update()

def plusone(pipes, scoreValue):
    global scoring
    if scoring == True and canvas.coords(pipes[0][0])[0] + 160 < canvas.coords(bee)[0]:
        scoring = False
        return scoreValue + 1
    return scoreValue

def generatePipes(amount, distancePipes, sizeOpening):
    genPipes = []
    if amount == 1:
        opening = randint(50, 550)
        genPipes.append(canvas.create_image(distancePipes, opening, image=reverseObstacles[randint(0, 3)], anchor="sw"))
        genPipes.append(canvas.create_image(distancePipes, opening + sizeOpening, image=obstacles[randint(0, 3)], anchor="nw"))
    else:
        for p in range(amount):
            pair = []
            opening = randint(50, 550)
            pair.append(canvas.create_image(1200 + distancePipes * p, opening, image=reverseObstacles[randint(0, 3)], anchor="sw"))
            pair.append(canvas.create_image(1200 + distancePipes * p, opening + sizeOpening, image=obstacles[randint(0, 3)], anchor="nw"))
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
    global jumped, paused, scoring, saving, pauseScreen
    scoreValue = 0
    distanceBetweenPipes = 550
    sizePipeOpening = 300
    gravity = 0.3
    pipes = generatePipes(4, distanceBetweenPipes, sizePipeOpening)
    honeycomb = canvas.create_image(600, 70, image=honeycombImage)
    score = canvas.create_text(615, 75, fill="#fbb040", font="Impact 50", text=f"Score: {scoreValue}", anchor="nw")
    if path.exists("savefile.txt"):
        settings = []
        jumped = False
        with open("savefile.txt") as file:
            for line in file:
                settings.append(line.replace("\n", ""))
        scoreValue = int(settings[0])
        scoring = bool("" if settings[1] == "False" else settings[1])
        speed = float(settings[2])
        animation = float(settings[3])
        hit = bool("" if settings[4] == "False" else settings[4])
        dead = bool("" if settings[4] == "False" else settings[4])
        for z in range(4):
            canvas.coords(pipes[z][0], float(settings[6 + (z*2)]), float(settings[7 + (z*2)]))
            canvas.coords(pipes[z][1], float(settings[6 + (z*2)]), float(settings[7 + (z*2)]) + 300)
        canvas.itemconfigure(score, text=f"Score: {scoreValue}")
        pause(0)
    else:
        scoring = False
        speed = 0
        animation = 16
        hit = False
        dead = False
    while canvas.coords(bee)[1] < 900:
        if paused != True:
            if hit == False:
                if jumped == True:
                    speed = -9
                    jumped = False
                    animation = 0
                if animation <= 14 or animation % 2 == 0:
                    canvas.itemconfigure(bee, image=beeImages[animation // 2])
                    animation += 1
                for i in range(len(pipes)):
                    canvas.move(pipes[i][0], -7, 0)
                    canvas.move(pipes[i][1], -7, 0)
                # If pipe out of screen then generate new one
                if canvas.coords(pipes[0][0])[0] < -140:
                    canvas.delete(pipes.pop(0))
                    newPipe = generatePipes(1, canvas.coords(pipes[len(pipes) - 1][0])[0] + distanceBetweenPipes, sizePipeOpening)
                    pipes.append(newPipe)
                    canvas.tag_raise(honeycomb)
                    canvas.tag_raise(score)
                hit = collision(pipes)
                if scoring == True:
                    scoreValue = plusone(pipes, scoreValue)
                    canvas.itemconfigure(score, text=f"Score: {scoreValue}")
            elif hit == True and dead == False:
                canvas.itemconfigure(bee, image=beeDead)
                canvas.tag_raise(bee)
                dead = True
            canvas.move(bee, 0, speed)
            canvas.update()
            sleep(0.00001)
            if canvas.coords(bee)[1] > 900:
                canvas.itemconfigure(bee, image=beeDead)
                canvas.coords(bee, 250, 900)
                canvas.tag_raise(bee)
            canvas.coords(bee)[1] += speed
            speed += gravity
        else:
            if saving == True:
                with open("savefile.txt", "w") as save_file:
                    save_file.write(f"{scoreValue}\n{scoring}\n{speed}\n{animation}\n{hit}\n{dead}\n")
                    for p in pipes:
                        save_file.write(f"{canvas.coords(p[0])[0]}\n")
                        save_file.write(f"{canvas.coords(p[0])[1]}\n")
                saving = False
                pauseScreen[6].config(text="Saved!")
            canvas.update()

window = Tk()
window.title("Kilburn Bee")
window.geometry("1440x900")
canvas = Canvas(window, width=1440, height=900)

logoImage = PhotoImage(file="assets/logo.png")
beeImages = [PhotoImage(file="assets/bee0.png"), PhotoImage(file="assets/bee1.png"), PhotoImage(file="assets/bee2.png"), PhotoImage(file="assets/bee3.png"), PhotoImage(file="assets/bee4.png"), PhotoImage(file="assets/bee5.png"), PhotoImage(file="assets/bee6.png"), PhotoImage(file="assets/bee7.png")]
beeDead = PhotoImage(file="assets/dead.png")
obstacles = [PhotoImage(file="assets/obstacle0.png"), PhotoImage(file="assets/obstacle1.png"), PhotoImage(file="assets/obstacle2.png"), PhotoImage(file="assets/obstacle3.png")]
reverseObstacles = [PhotoImage(file="assets/robstacle0.png"), PhotoImage(file="assets/robstacle1.png"), PhotoImage(file="assets/robstacle2.png"), PhotoImage(file="assets/robstacle3.png")]
buttonImage = PhotoImage(file="assets/buttonImage.png")
bigbuttonImage = PhotoImage(file="assets/bigbuttonImage.png")
honeycombImage = PhotoImage(file="assets/honeycomb.png")
blacknessImage = PhotoImage(file="assets/blackness.png")
excelImage = PhotoImage(file="assets/excel.png")
kilburn = PhotoImage(file="assets/kilburn.png")
canvas.create_image(0, 0, image=kilburn, anchor="nw")
bee = canvas.create_image(250, 450, image=beeImages[7], anchor="s")
window.iconbitmap("assets/bee.ico")
buttonFont = font.Font(family="Impact", size=30)

jumped = True
inhomepage = True
paused = False
bossed = False
saving = False

canvas.pack()
window.bind("<space>", jump)
window.bind("<Escape>", pause)
window.bind("<b>", boss)
homepage()
window.mainloop()
