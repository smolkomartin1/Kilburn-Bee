from tkinter import Tk, Canvas

window = Tk()
window.title("Kilburn Bee")
window.geometry("500x700")
canvas = Canvas(window, width=500, height=700)
canvas.create_text(35, 10, text="Hello world")
canvas.pack()

window.mainloop()
