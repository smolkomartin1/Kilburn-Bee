from tkinter import Tk, Canvas, PhotoImage
from time import sleep

def jump(event):
    global jumped
    jumped = True

def start():
    global jumped
    speed = 0
    gravity = 0.3
    while canvas.coords(bee)[1] < 700:
        if jumped == True:
            speed = -8
            jumped = False
        canvas.move(bee, 0, speed)
        canvas.update()
        sleep(0.01)
        if canvas.coords(bee)[1] > 700:
            canvas.coords(bee, 150, 700)
        canvas.coords(bee)[1] += speed
        speed += gravity




window = Tk()
window.title("Kilburn Bee")
window.geometry("500x700")
canvas = Canvas(window, width=500, height=700)
beeImage = PhotoImage(file="bee.png")
bee = canvas.create_image(150, 350, image=beeImage, anchor="s")
jumped = False




canvas.pack()
window.bind("<space>", jump)
start()
window.mainloop()
