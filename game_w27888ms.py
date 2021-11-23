from tkinter import Tk, Canvas, PhotoImage
from time import sleep
from random import randint

def jump(event):
    global jumped
    jumped = True

def collision(pipes):
    beeCoords = canvas.coords(bee)
    # checks just the first pipe, if pipe distance too short than add a for loop
    pipeTop = canvas.coords(pipes[0][0])
    if (pipeTop[0] + 160) >= beeCoords[0] >= (pipeTop[0] - 48) and ((beeCoords[1] - 80) <= pipeTop[1] or (pipeTop[1] + 300) <= beeCoords[1]):
        return True
    return False

def start():
    global jumped
    speed = 0
    gravity = 0.3
    animation = 16
    distanceBetweenPipes = 550
    sizePipeOpening = 300
    hit = False
    dead = False
    pipes = generatePipes(4, distanceBetweenPipes, sizePipeOpening)
    while canvas.coords(bee)[1] < 900:
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
            hit = collision(pipes)
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

window = Tk()
window.title("Kilburn Bee")
window.geometry("1440x900")
canvas = Canvas(window, width=1440, height=900)

beeImages = [PhotoImage(file="assets/bee0.png"), PhotoImage(file="assets/bee1.png"), PhotoImage(file="assets/bee2.png"), PhotoImage(file="assets/bee3.png"), PhotoImage(file="assets/bee4.png"), PhotoImage(file="assets/bee5.png"), PhotoImage(file="assets/bee6.png"), PhotoImage(file="assets/bee7.png")]
beeDead = PhotoImage(file="assets/dead.png")
obstacles = [PhotoImage(file="assets/obstacle0.png"), PhotoImage(file="assets/obstacle1.png"), PhotoImage(file="assets/obstacle2.png"), PhotoImage(file="assets/obstacle3.png")]
reverseObstacles = [PhotoImage(file="assets/robstacle0.png"), PhotoImage(file="assets/robstacle1.png"), PhotoImage(file="assets/robstacle2.png"), PhotoImage(file="assets/robstacle3.png")]
kilburn = PhotoImage(file="assets/kilburn.png")
canvas.create_image(0, 0, image=kilburn, anchor="nw")
canvas.pack()
bee = canvas.create_image(250, 450, image=beeImages[7], anchor="s")
jumped = True

canvas.pack()
window.bind("<space>", jump)
start()
window.mainloop()
