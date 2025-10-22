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

class NotesCalendar:
    def __init__(self, root):
        self.root = root
        self.notes_file = "calendar_notes.json"
        self.notes = self.load_notes()
        
        self.setup_ui()
        self.update_notes_display()
    
    def load_notes(self):
        """Загрузка заметок из файла"""
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_notes(self):
        """Сохранение заметок в файл"""
        try:
            with open(self.notes_file, 'w', encoding='utf-8') as f:
                json.dump(self.notes, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить заметки: {e}")
            return False
    
    def setup_ui(self):
        """Настройка интерфейса"""
        self.root.title("Календарь с заметками")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Календарь с заметками", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 15))
        
        # Разделение на две колонки
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Левая панель - календарь
        left_frame = ttk.LabelFrame(content_frame, text="Календарь", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Создаем календарь
        self.calendar = SimpleCalendar(left_frame)
        self.calendar.on_date_select = self.on_date_select
        
        # Выбранная дата
        self.selected_date_var = tk.StringVar()
        self.selected_date_var.set(date.today().strftime("%d.%m.%Y"))
        
        date_label = ttk.Label(left_frame, textvariable=self.selected_date_var, 
                              font=("Arial", 11, "bold"), foreground="blue")
        date_label.pack(pady=10)
        
        # Кнопки для календаря
        cal_buttons_frame = ttk.Frame(left_frame)
        cal_buttons_frame.pack(pady=5)
        
        today_btn = ttk.Button(cal_buttons_frame, text="Сегодня", 
                              command=self.go_to_today)
        today_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(cal_buttons_frame, text="Очистить заметки", 
                              command=self.clear_date_notes)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Правая панель - заметки
        right_frame = ttk.LabelFrame(content_frame, text="Заметки", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Заголовок с датой для заметок
        self.notes_title_var = tk.StringVar()
        self.notes_title_var.set("Заметки на выбранную дату")
        
        notes_title = ttk.Label(right_frame, textvariable=self.notes_title_var,
                               font=("Arial", 11, "bold"))
        notes_title.pack(pady=(0, 10))
        
        # Поле для ввода заметки
        ttk.Label(right_frame, text="Новая заметка:").pack(anchor=tk.W, pady=(0, 5))
        
        self.note_text = scrolledtext.ScrolledText(right_frame, width=35, height=6,
                                                  wrap=tk.WORD, font=("Arial", 10))
        self.note_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Кнопки для заметок
        notes_buttons_frame = ttk.Frame(right_frame)
        notes_buttons_frame.pack(pady=5)
        
        save_btn = ttk.Button(notes_buttons_frame, text="Сохранить", 
                             command=self.save_note)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = ttk.
Button(notes_buttons_frame, text="🗑️ Удалить", 
                               command=self.delete_note)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Область для просмотра существующих заметок
        ttk.Label(right_frame, text="Существующие заметки:").pack(anchor=tk.W, pady=(10, 5))
        
        self.notes_listbox = tk.Listbox(right_frame, height=8, font=("Arial", 10))
        self.notes_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.notes_listbox.bind('<<ListboxSelect>>', self.on_note_select)
        
        # Статус бар
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def on_date_select(self):
        """Обработчик выбора даты в календаре"""
        selected_date = self.calendar.get_selected_date()
        self.selected_date_var.set(selected_date)
        self.notes_title_var.set(f"Заметки на {selected_date}")
        self.update_notes_display()
        self.note_text.delete(1.0, tk.END)
        self.status_var.set(f"Выбрана дата: {selected_date}")
    
    def go_to_today(self):
        """Перейти к сегодняшней дате"""
        today = date.today()
        self.calendar.current_date = today
        self.calendar.selected_date = today
        self.calendar.update_calendar()
        self.on_date_select()
    
    def get_selected_date_key(self):
        """Получить ключ для выбранной даты"""
        return self.calendar.get_selected_date()
    
    def save_note(self):
        """Сохранить новую заметку"""
        note_content = self.note_text.get(1.0, tk.END).strip()
        if not note_content:
            messagebox.showwarning("Ошибка", "Введите текст заметки!")
            return
        
        date_key = self.get_selected_date_key()
        
        if date_key not in self.notes:
            self.notes[date_key] = []
        
        # Добавляем временную метку
        timestamp = datetime.now().strftime("%H:%M")
        note_with_time = f"[{timestamp}] {note_content}"
        
        self.notes[date_key].append(note_with_time)
        
        if self.save_notes():
            self.update_notes_display()
            self.note_text.delete(1.0, tk.END)
            self.status_var.set(f"Заметка сохранена для {date_key}")
        else:
            messagebox.showerror("Ошибка", "Не удалось сохранить заметку!")
    
    def delete_note(self):
        """Удалить выбранную заметку"""
        date_key = self.get_selected_date_key()
        selected_indices = self.notes_listbox.curselection()
        
        if not selected_indices:
            messagebox.showwarning("Ошибка", "Выберите заметку для удаления!")
            return
        
        if date_key not in self.notes:
            return
        
        index = selected_indices[0]
        
        result = messagebox.askyesno("Подтверждение", 
                                   "Вы уверены, что хотите удалить выбранную заметку?")
        if result:
            deleted_note = self.notes[date_key].pop(index)
            
            # Если заметок для этой даты не осталось, удаляем дату
            if not self.notes[date_key]:
                del self.notes[date_key]
            
            if self.save_notes():
                self.update_notes_display()
                self.note_text.delete(1.0, tk.END)
                self.status_var.set("Заметка удалена")
    
    def clear_date_notes(self):
        """Очистить все заметки для выбранной даты"""
        date_key = self.get_selected_date_key()
        
        if date_key not in self.notes or not self.notes[date_key]:
            messagebox.showinfo("Информация", "Нет заметок для очистки!")
            return
        
        result = messagebox.askyesno("Подтверждение", 
                                   f"Удалить все заметки для {date_key}?")
        if result:
            del self.notes[date_key]
            if self.save_notes():
self.update_notes_display()
                self.note_text.delete(1.0, tk.END)
                self.status_var.set(f"Все заметки для {date_key} удалены")
    
    def on_note_select(self, event):
        """Обработчик выбора заметки в списке"""
        selected_indices = self.notes_listbox.curselection()
        if selected_indices:
            pass
    
    def update_notes_display(self):
        """Обновить отображение заметок для выбранной даты"""
        date_key = self.get_selected_date_key()
        self.notes_listbox.delete(0, tk.END)
        
        if date_key in self.notes:
            for note in self.notes[date_key]:
                self.notes_listbox.insert(tk.END, note)
        
        # Обновление статуса
        notes_count = len(self.notes_listbox.get(0, tk.END))
        self.status_var.set(f"Заметок на {date_key}: {notes_count}")

def main():
    root = tk.Tk()
    app = NotesCalendar(root)
    root.mainloop()

if __name__ == "__main__":
    main()
