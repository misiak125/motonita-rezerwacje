from .funcs import animate_gif
from tkinter import Toplevel, Label
from PIL import ImageTk, Image

def on_customer_click(event):
    top = Toplevel()
    frame_counter = 0
    top.title("GRATULACJE!")
    cat_gif = Image.open(r"src/static/cat1.gif")
    frames = []
    for i in range(cat_gif.n_frames):
        cat_gif.seek(i)  
        frame = ImageTk.PhotoImage(cat_gif.copy())  
        frames.append(frame)
    gif_label = Label(top)
    gif_label.pack()

    text_label = Label(top, text="Pogłaskałeś klienta!", 
        font=("Helvetica", 17, "bold"), bg="black", fg="white")
    text_label.place(anchor="w", x=10, y=20)

    animate_gif(gif_label, frames, frame_counter)
