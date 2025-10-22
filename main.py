import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, date, timedelta
import json
import os
import calendar

class SimpleCalendar:
    def __init__(self, parent):
        self.parent = parent
        self.current_date = date.today()
        self.selected_date = self.current_date
        self.setup_calendar()
    
    def setup_calendar(self):
        self.cal_frame = ttk.Frame(self.parent)
        self.cal_frame.pack(fill=tk.BOTH, expand=True)
        
        self.header_frame = ttk.Frame(self.cal_frame)
        self.header_frame.pack(fill=tk.X, pady=5)
        
        self.prev_btn = ttk.Button(self.header_frame, text="◀", 
                                 command=self.prev_month, width=3)
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.month_var = tk.StringVar()
        self.month_label = ttk.Label(self.header_frame, textvariable=self.month_var,
                                   font=("Arial", 12, "bold"))
        self.month_label.pack(side=tk.LEFT, expand=True)
        
        self.next_btn = ttk.Button(self.header_frame, text="▶", 
                                 command=self.next_month, width=3)
        self.next_btn.pack(side=tk.RIGHT, padx=5)
        
        days_frame = ttk.Frame(self.cal_frame)
        days_frame.pack(fill=tk.X)
        
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        for day in days:
            label = ttk.Label(days_frame, text=day, font=("Arial", 9, "bold"),
                            width=4, anchor=tk.CENTER)
            label.pack(side=tk.LEFT, expand=True)
        
        self.days_frame = ttk.Frame(self.cal_frame)
        self.days_frame.pack(fill=tk.BOTH, expand=True)
        
        self.update_calendar()
    
    def update_calendar(self):
        self.month_var.set(self.current_date.strftime("%B %Y"))
        
        for widget in self.days_frame.winfo_children():
            widget.destroy()
        
        first_day = self.current_date.replace(day=1)
        days_in_month = calendar.monthrange(self.current_date.year, self.current_date.month)[1]
        start_weekday = first_day.weekday()
        
        row = 0
        col = 0
        
        for i in range(start_weekday):
            frame = ttk.Frame(self.days_frame, width=40, height=40)
            frame.grid(row=row, column=col, padx=1, pady=1)
            col += 1
        
        for day in range(1, days_in_month + 1):
            current_day_date = self.current_date.replace(day=day)
            is_today = current_day_date == date.today()
            is_selected = current_day_date == self.selected_date
            
            day_btn = tk.Button(self.days_frame, text=str(day), 
                              width=4, height=2,
                              relief="solid" if is_selected else "raised",
                              bg="lightblue" if is_selected else ("yellow" if is_today else "white"),
                              command=lambda d=day: self.select_day(d))
            day_btn.grid(row=row, column=col, padx=1, pady=1)
            
            col += 1
            if col > 6:
                col = 0
                row += 1
    
    def select_day(self, day):
        self.selected_date = self.current_date.replace(day=day)
        self.update_calendar()
        if hasattr(self, 'on_date_select'):
            self.on_date_select()
    
    def prev_month(self):
        year = self.current_date.year
        month = self.current_date.month
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
        self.current_date = self.current_date.replace(year=year, month=month)
        self.update_calendar()
    
    def next_month(self):
        year = self.current_date.year
        month = self.current_date.month
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
        self.current_date = self.current_date.replace(year=year, month=month)
        self.update_calendar()
    
    def get_selected_date(self):
        return self.selected_date.strftime("%d.%m.%Y")



def main():
    root = tk.Tk()
    app = NotesCalendar(root)
    root.mainloop()

if __name__ == "__main__":
    main()
