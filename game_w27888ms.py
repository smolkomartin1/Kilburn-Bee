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
    if (pipeTop[2] + 75) >= (beeCoords[0] + 55) >= pipeTop[0] and ((beeCoords[1] - 80) <= pipeTop[3] or (pipeTop[3] + 300) <= beeCoords[1]):
        return True
    return False

def start():
    global jumped
    speed = 0
    gravity = 0.3
    animation = 16
    distanceBetweenPipes = 600
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
            if canvas.coords(pipes[0][0])[2] < 0:
                pipes.pop(0)
                newPipe = generatePipes(1, canvas.coords(pipes[len(pipes) - 1][0])[2] + distanceBetweenPipes - 100, sizePipeOpening)
                pipes.append(newPipe)
            hit = collision(pipes)
        elif hit == True and dead == False:
            canvas.itemconfigure(bee, image=beeDead)
            dead = True
        canvas.move(bee, 0, speed)
        canvas.update()
        sleep(0.001)
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
        genPipes.append(canvas.create_rectangle(distancePipes, 0, 100 + distancePipes, opening))
        genPipes.append(canvas.create_rectangle(distancePipes, opening + sizeOpening, 100 + distancePipes, 900))
    else:
        for p in range(amount):
            pair = []
            opening = randint(50, 550)
            pair.append(canvas.create_rectangle(1200 + distancePipes * p, 0, 1300 + distancePipes * p, opening))
            pair.append(canvas.create_rectangle(1200 + distancePipes * p, opening + sizeOpening, 1300 + distancePipes * p, 900))
            genPipes.append(pair)
    return genPipes


window = Tk()
window.title("Kilburn Bee")
window.geometry("1440x900")
canvas = Canvas(window, width=1440, height=900)

beeImages = [PhotoImage(file="bee_sprites/bee0.png"), PhotoImage(file="bee_sprites/bee1.png"), PhotoImage(file="bee_sprites/bee2.png"), PhotoImage(file="bee_sprites/bee3.png"), PhotoImage(file="bee_sprites/bee4.png"), PhotoImage(file="bee_sprites/bee5.png"), PhotoImage(file="bee_sprites/bee6.png"), PhotoImage(file="bee_sprites/bee7.png")]
beeDead = PhotoImage(file="bee_sprites/dead.png")
# kilburn = PhotoImage(file="kilburn5.png")
# canvas.create_image(0, 0, image=kilburn, anchor="nw")
canvas.pack()
bee = canvas.create_image(250, 450, image=beeImages[7], anchor="s")
jumped = True

canvas.pack()
window.bind("<space>", jump)
start()
window.mainloop()
