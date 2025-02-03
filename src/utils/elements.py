from tkinter import Frame, Entry, Listbox, Button, LEFT, END
from PIL import Image, ImageTk

class SearchableComboBox():
    def __init__(self, options) -> None:
        self.dropdown_id = None
        self.options = options

        wrapper = Frame(root)
        wrapper.pack()

        self.entry = Entry(wrapper, width=24)
        self.entry.bind("<KeyRelease>", self.on_entry_key)
        self.entry.bind("<FocusIn>", self.show_dropdown) 
        self.entry.pack(side=LEFT)

        self.icon = ImageTk.PhotoImage(Image.open("src/static/dropdown_arrow.png").resize((16,16)))
        Button(wrapper, image=self.icon, command=self.show_dropdown).pack(side=LEFT)

        self.listbox = Listbox(root, height=5, width=30)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        for option in self.options:
            self.listbox.insert(END, option)

    def on_entry_key(self, event):
        pass

    def on_select(self, event):
        pass

    def show_dropdown(self, event=None):
        pass

    def hide_dropdown(self):
        pass