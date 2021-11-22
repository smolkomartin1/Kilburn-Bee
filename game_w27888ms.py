from tkinter import Tk, Canvas, PhotoImage
from time import sleep
from random import randint

def jump(event):
    global jumped
    jumped = True

def start():
    global jumped
    pipes = generatePipes(4, 600)
    speed = 0
    gravity = 0.3
    while canvas.coords(bee)[1] < 900:
        if jumped == True:
            speed = -9
            jumped = False
        canvas.move(bee, 0, speed)
        for i in range(len(pipes)):
            canvas.move(pipes[i][0], -7, 0)
            canvas.move(pipes[i][1], -7, 0)
        if canvas.coords(pipes[0][0])[2] < 0:
            pipes.pop(0)
            newPipe = generatePipes(1, canvas.coords(pipes[len(pipes) - 1][0])[2] + 500)
            pipes.append(newPipe)
        canvas.update()
        sleep(0.01)
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
