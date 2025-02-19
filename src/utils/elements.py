import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar

class DateEntryWithCalendar:
    def __init__(self, parent, date_var=None, **kwargs):
        self.parent = parent
        self.date_var = date_var if date_var else tk.StringVar()
        self.root = parent.winfo_toplevel()
        
        # Create entry widget
        self.entry = ttk.Entry(parent, textvariable=self.date_var, state="readonly", **kwargs)
        self.entry.bind('<Button-1>', self.show_calendar)
        
        self.calendar_window = None
        self.click_binding_id = None
        self.configure_binding_id = None

    def show_calendar(self, event):
        if self.calendar_window and self.calendar_window.winfo_exists():
            return

        # Create top-level window
        self.calendar_window = tk.Toplevel(self.parent)
        self.calendar_window.overrideredirect(True)
        self.calendar_window.attributes('-alpha', 0.95)
        
        # Position below entry widget
        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height()
        self.calendar_window.geometry(f'+{x}+{y}')
        
        # Create calendar widget
        calendar = Calendar(
            self.calendar_window,
            selectmode='day',
            date_pattern='dd.mm.yyyy',
        )
        
        if self.date_var.get():
            try:
                calendar.selection_set(tk.datetime.datetime.strptime(self.date_var.get(), '%Y-%m-%d'))
            except:
                pass
        
        calendar.pack(padx=2, pady=2)
        
        # Bind events
        calendar.bind('<<CalendarSelected>>', lambda e: self.set_date(calendar))
        self.click_binding_id = self.root.bind('<Button-1>', self.check_click_outside)
        self.configure_binding_id = self.root.bind('<Configure>', self.handle_window_change)

    def handle_window_change(self, event):
        """Close calendar when main window is moved or resized"""
        self.close_calendar()

    def check_click_outside(self, event):
        """Close calendar if click is outside the calendar widget"""
        if not self.calendar_window:
            return
        
        x, y = event.x_root, event.y_root
        cal_geom = (
            self.calendar_window.winfo_x(),
            self.calendar_window.winfo_y(),
            self.calendar_window.winfo_x() + self.calendar_window.winfo_width(),
            self.calendar_window.winfo_y() + self.calendar_window.winfo_height()
        )
        
        if not (cal_geom[0] <= x <= cal_geom[2] and cal_geom[1] <= y <= cal_geom[3]):
            self.close_calendar()

    def set_date(self, calendar):
        self.date_var.set(calendar.get_date())
        self.close_calendar()

    def close_calendar(self):
        """Clean up bindings and window"""
        if self.calendar_window:
            # Remove event bindings
            if self.click_binding_id:
                self.root.unbind('<Button-1>', self.click_binding_id)
            if self.configure_binding_id:
                self.root.unbind('<Configure>', self.configure_binding_id)
            
            # Destroy window
            self.calendar_window.destroy()
            self.calendar_window = None

    def grid(self, **kwargs):
        self.entry.grid(**kwargs)

