from tkinter import Tk, Canvas, PhotoImage
from time import sleep
from random import randint

def jump(event):
    global jumped
    jumped = True

def collision(pipes):
    beeCoords = canvas.coords(bee)
    print(beeCoords)
    # checks just the first pipe, if pipe distance too short than add a for loop
    pipeTop = canvas.coords(pipes[0][0])
    print(pipeTop)
    if pipeTop[2] >= beeCoords[0] >= pipeTop[0] and ((pipeTop[3] + 300) <= beeCoords[1] or beeCoords[1] <= pipeTop[3]):
        return True
    return False

def start():
    global jumped
    pipes = generatePipes(4, 600)
    speed = 0
    gravity = 0.3
    hit = False
    while canvas.coords(bee)[1] < 900 and hit == False:
        if jumped == True:
            speed = -9
            jumped = False
        canvas.move(bee, 0, speed)
        for i in range(len(pipes)):
            canvas.move(pipes[i][0], -7, 0)
            canvas.move(pipes[i][1], -7, 0)
        # If pipe out of screen then generate new one
        if canvas.coords(pipes[0][0])[2] < 0:
            pipes.pop(0)
            newPipe = generatePipes(1, canvas.coords(pipes[len(pipes) - 1][0])[2] + 500)
            pipes.append(newPipe)
        canvas.update()
        sleep(0.01)
        hit = collision(pipes)
        if canvas.coords(bee)[1] > 900:
            canvas.coords(bee, 250, 900)
        canvas.coords(bee)[1] += speed
        speed += gravity

def generatePipes(amount, distancePipes):
    genPipes = []
    if amount == 1:
        opening = randint(50, 550)
        genPipes.append(canvas.create_rectangle(distancePipes, 0, 100 + distancePipes, opening))
        genPipes.append(canvas.create_rectangle(distancePipes, opening + 300, 100 + distancePipes, 900))
    else:
        for p in range(amount):
            pair = []
            opening = randint(50, 550)
            pair.append(canvas.create_rectangle(1200 + distancePipes * p, 0, 1300 + distancePipes * p, opening))
            pair.append(canvas.create_rectangle(1200 + distancePipes * p, opening + 300, 1300 + distancePipes * p, 900))
            genPipes.append(pair)
    return genPipes


window = Tk()
window.title("Kilburn Bee")
window.geometry("1440x900")
canvas = Canvas(window, width=1440, height=900)
beeImage = PhotoImage(file="bee.png")
bee = canvas.create_image(250, 450, image=beeImage, anchor="s")
jumped = True




canvas.pack()
window.bind("<space>", jump)
start()
window.mainloop()
