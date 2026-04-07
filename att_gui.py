import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from toc_engine import DFA, StudentDatabase
import threading
import time

BG = "#fffaf0"
CARD = "#f5f3f0"
ACCENT = "#0066cc"
TEXT = "#000000"
GOOD = "#28a745"
WARN = "#ffc107"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("STUDENT ATTENDANCE SYSTEM")
        self.root.geometry("1400x800")
        self.root.configure(bg=BG)
        
        self.db = StudentDatabase()
        self.dfa = DFA()
        
        self.db.clear_all_data()
        
        self.recording = False
        self.record_time_left = 180
        self.time_expired = False
        self.marked_present = set()
        self.marked_absent = set()
        self.timer_thread = None
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.build_layout()
    
    def build_layout(self):
        header = tk.Frame(self.root, bg=ACCENT, height=60)
        header.pack(side="top", fill="x")
        header.pack_propagate(False)
        
        title = tk.Label(header, text="STUDENT ATTENDANCE SYSTEM", font=("Arial", 18, "bold"), 
                        bg=ACCENT, fg="white")
        title.pack(pady=12)
        
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.add_frame = tk.Frame(notebook, bg=BG)
        self.attend_frame = tk.Frame(notebook, bg=BG)
        
        notebook.add(self.add_frame, text="ADD STUDENT")
        notebook.add(self.attend_frame, text="MARK ATTENDANCE")
        
        self.build_add_tab()
        self.build_attend_tab()
    
    def build_add_tab(self):
        container = tk.Frame(self.add_frame, bg=BG)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        card = tk.Frame(container, bg=CARD, relief="solid", bd=1)
        card.pack(fill="both", expand=True)
        
        title = tk.Label(card, text="Add New Student", font=("Arial", 14, "bold"), 
                        bg=CARD, fg=ACCENT)
        title.pack(padx=20, pady=(15, 5))
        
        form = tk.Frame(card, bg=CARD)
        form.pack(padx=20, pady=15, fill="both")
        
        tk.Label(form, text="Registration No:", font=("Arial", 11, "bold"), 
                bg=CARD, fg=TEXT).grid(row=0, column=0, sticky="w", pady=10)
        self.reg_entry = tk.Entry(form, font=("Arial", 12), bg="white", fg=TEXT, 
                                 insertbackground=ACCENT, width=25)
        self.reg_entry.grid(row=0, column=1, sticky="ew", padx=10)
        
        tk.Label(form, text="Student Name:", font=("Arial", 11, "bold"), 
                bg=CARD, fg=TEXT).grid(row=1, column=0, sticky="w", pady=10)
        self.name_entry = tk.Entry(form, font=("Arial", 12), bg="white", fg=TEXT, 
                                  insertbackground=ACCENT, width=25)
        self.name_entry.grid(row=1, column=1, sticky="ew", padx=10)
        
        form.columnconfigure(1, weight=1)
        
        btn_frame = tk.Frame(card, bg=CARD)
        btn_frame.pack(pady=15)
        
        add_btn = tk.Button(btn_frame, text="ADD STUDENT", command=self.add_student,
                           font=("Arial", 12, "bold"), bg=ACCENT, fg="white", padx=30, 
                           pady=12, relief="flat", cursor="hand2")
        add_btn.pack(side="left", padx=10)
        
        clear_btn = tk.Button(btn_frame, text="CLEAR", command=self.clear_add,
                             font=("Arial", 11), bg="#cccccc", fg=TEXT, padx=20, 
                             pady=12, relief="flat", cursor="hand2")
        clear_btn.pack(side="left", padx=5)
        
        tree_frame = tk.Frame(card, bg=CARD)
        tree_frame.pack(padx=20, pady=(10, 10), fill="both", expand=True)
        
        tk.Label(tree_frame, text="Registered Students:", font=("Arial", 11, "bold"), 
                bg=CARD, fg=TEXT).pack(anchor="w", pady=(0, 10))
        
        self.student_tree = ttk.Treeview(tree_frame, height=12)
        self.student_tree.pack(fill="both", expand=True)
        
        self.student_tree['columns'] = ('RegNo', 'Name', 'Date')
        self.student_tree.column('#0', width=0, stretch="no")
        self.student_tree.column('RegNo', anchor="w", width=120)
        self.student_tree.column('Name', anchor="w", width=300)
        self.student_tree.column('Date', anchor="w", width=200)
        
        self.student_tree.heading('#0', text='', anchor="w")
        self.student_tree.heading('RegNo', text='Reg No', anchor="w")
        self.student_tree.heading('Name', text='Name', anchor="w")
        self.student_tree.heading('Date', text='Date Added', anchor="w")
        
        del_frame = tk.Frame(card, bg=CARD)
        del_frame.pack(padx=20, pady=(0, 15))
        
        del_btn = tk.Button(del_frame, text="DELETE SELECTED STUDENT", 
                            command=self.delete_student,
                            font=("Arial", 11, "bold"), bg="#ff6b6b", fg="white", 
                            padx=30, pady=10, relief="flat", cursor="hand2")
        del_btn.pack()
        
        self.refresh_student_tree()
    
    def build_attend_tab(self):
        container = tk.Frame(self.attend_frame, bg=BG)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        control_frame = tk.Frame(container, bg=CARD, relief="solid", bd=1)
        control_frame.pack(side="top", fill="x", pady=(0, 15))
        
        btn_ctrl = tk.Frame(control_frame, bg=CARD)
        btn_ctrl.pack(padx=15, pady=15)
        
        start_btn = tk.Button(btn_ctrl, text="START RECORDING (3 MIN)", command=self.start_recording,
                             font=("Arial", 12, "bold"), bg=GOOD, fg="white", 
                             padx=30, pady=12, relief="flat", cursor="hand2")
        start_btn.pack(side="left", padx=10)
        
        finish_btn = tk.Button(btn_ctrl, text="FINISH", command=self.finish_recording,
                            font=("Arial", 12, "bold"), bg=WARN, fg="black", 
                            padx=30, pady=12, relief="flat", cursor="hand2")
        finish_btn.pack(side="left", padx=10)
        
        self.status_label = tk.Label(control_frame, text="Status: INACTIVE", 
                                    font=("Arial", 11, "bold"), bg=CARD, fg="#cc0000")
        self.status_label.pack(pady=(0, 10))
        
        input_frame = tk.Frame(container, bg=CARD, relief="solid", bd=1)
        input_frame.pack(side="top", fill="x", pady=(0, 15))
        
        input_form = tk.Frame(input_frame, bg=CARD)
        input_form.pack(padx=15, pady=15)
        
        tk.Label(input_form, text="Reg No:", font=("Arial", 11, "bold"), 
                bg=CARD, fg=TEXT).pack(side="left", padx=(0, 10))
        self.attend_reg = tk.Entry(input_form, font=("Arial", 12), bg="white", fg=TEXT, 
                                  insertbackground=ACCENT, width=20)
        self.attend_reg.pack(side="left", padx=(0, 20))
        
        verify_btn = tk.Button(input_form, text="VERIFY", 
                               command=self.verify_student,
                               font=("Arial", 11, "bold"), bg=GOOD, fg="white", 
                               padx=30, pady=8, relief="flat", cursor="hand2")
        verify_btn.pack(side="left", padx=5)
        
        excuse_btn = tk.Button(input_form, text="EXCUSE", 
                              command=self.mark_excuse,
                              font=("Arial", 11, "bold"), bg=WARN, fg="black", 
                              padx=30, pady=8, relief="flat", cursor="hand2")
        excuse_btn.pack(side="left", padx=5)
        
        record_frame = tk.Frame(container, bg=CARD, relief="solid", bd=1)
        record_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        tk.Label(record_frame, text="Today's Attendance:", font=("Arial", 11, "bold"), 
                bg=CARD, fg=TEXT).pack(anchor="w", padx=15, pady=(10, 5))
        
        self.attend_tree = ttk.Treeview(record_frame, height=10)
        self.attend_tree.pack(padx=15, pady=(5, 10), fill="both", expand=True)
        
        self.attend_tree['columns'] = ('RegNo', 'Name', 'Status', 'Time')
        self.attend_tree.column('#0', width=0, stretch="no")
        self.attend_tree.column('RegNo', anchor="w", width=120)
        self.attend_tree.column('Name', anchor="w", width=280)
        self.attend_tree.column('Status', anchor="center", width=100)
        self.attend_tree.column('Time', anchor="w", width=120)
        
        self.attend_tree.heading('#0', text='', anchor="w")
        self.attend_tree.heading('RegNo', text='Reg No', anchor="w")
        self.attend_tree.heading('Name', text='Name', anchor="w")
        self.attend_tree.heading('Status', text='Status', anchor="center")
        self.attend_tree.heading('Time', text='Time', anchor="w")
        
        stats_frame = tk.Frame(container, bg=CARD, relief="solid", bd=1)
        stats_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        tk.Label(stats_frame, text="Statistics:", font=("Arial", 11, "bold"), 
                bg=CARD, fg=TEXT).pack(anchor="w", padx=15, pady=(10, 5))
        
        self.stats_text = tk.Text(stats_frame, font=("Arial", 10), bg="white", fg=TEXT, 
                                height=5, width=80)
        self.stats_text.pack(padx=15, pady=(5, 15), fill="both")
        self.stats_text.config(state="disabled")
        
        self.refresh_attend_tree()
        self.refresh_stats()
    
    def add_student(self):
        reg = self.reg_entry.get().strip().upper()
        name = self.name_entry.get().strip()
        
        if not reg or not name:
            messagebox.showerror("Error", "Fill all fields")
            return
        
        success, msg = self.db.add_student(reg, name)
        if success:
            messagebox.showinfo("Success", msg)
            self.clear_add()
            self.refresh_student_tree()
        else:
            messagebox.showerror("Error", msg)
    
    def clear_add(self):
        self.reg_entry.delete(0, "end")
        self.name_entry.delete(0, "end")
    
    def delete_student(self):
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a student to delete")
            return
        
        item = selected[0]
        values = self.student_tree.item(item, 'values')
        reg_no = values[0]
        
        if not messagebox.askyesno("Confirm", f"Delete student {reg_no}?"):
            return
        
        success, msg = self.db.delete_student(reg_no)
        if success:
            messagebox.showinfo("Success", msg)
            self.refresh_student_tree()
        else:
            messagebox.showerror("Error", msg)
    
    def student_exists(self, reg_no):
        students = self.db.get_students()
        return any(s[0] == reg_no for s in students)
    
    def get_student_name(self, reg_no):
        students = self.db.get_students()
        for s in students:
            if s[0] == reg_no:
                return s[1]
        return None
    
    def start_recording(self):
        self.recording = True
        self.record_time_left = 180
        self.time_expired = False
        self.marked_present.clear()
        self.marked_absent.clear()
        self.update_status()
        self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
        self.timer_thread.start()
    
    def run_timer(self):
        while self.recording and self.record_time_left > 0:
            self.record_time_left -= 1
            mins = self.record_time_left // 60
            secs = self.record_time_left % 60
            self.root.after(0, lambda m=mins, s=secs: self.status_label.config(
                text=f"Status: RECORDING - Time Left: {m}:{s:02d}"))
            time.sleep(1)
        
        if self.recording and self.record_time_left == 0:
            self.auto_mark_absent()
    
    def auto_mark_absent(self):
        self.time_expired = True
        students = self.db.get_students()
        for reg_no, name, _ in students:
            if reg_no not in self.marked_present and reg_no not in self.marked_absent:
                self.db.mark_attendance(reg_no, "ABSENT")
                self.marked_absent.add(reg_no)
        
        self.refresh_attend_tree()
        self.refresh_stats()
        self.root.after(0, lambda: messagebox.showinfo("Recording", "3 minutes ended. Unmarked students marked ABSENT."))
    
    def finish_recording(self):
        if not self.recording:
            messagebox.showinfo("Info", "Not recording")
            return
        
        self.recording = False
        self.time_expired = False
        self.marked_present.clear()
        self.marked_absent.clear()
        self.update_status()
        messagebox.showinfo("Finished", "Recording session ended")
        self.db.export_excel("attendance.xlsx")
        messagebox.showinfo("Export", "Attendance exported to attendance.xlsx")
    
    def update_status(self):
        if self.recording:
            mins = self.record_time_left // 60
            secs = self.record_time_left % 60
            self.status_label.config(
                text=f"Status: RECORDING - Time Left: {mins}:{secs:02d}",
                fg=GOOD)
        else:
            self.status_label.config(text="Status: INACTIVE", fg="#cc0000")
    
    def verify_student(self):
        if not self.recording:
            messagebox.showerror("Error", "Start recording first")
            return
        
        reg = self.attend_reg.get().strip().upper()
        
        if not reg:
            messagebox.showerror("Error", "Enter registration number")
            return
        
        if not self.dfa.validate(reg):
            messagebox.showerror("Error", "Invalid registration number")
            return
        
        if not self.student_exists(reg):
            messagebox.showerror("Error", f"Student {reg} not registered")
            return
        
        if reg in self.marked_present or reg in self.marked_absent:
            messagebox.showerror("Error", f"Student {reg} already marked")
            return
        
        if self.time_expired:
            self.db.mark_attendance(reg, "ABSENT")
            self.marked_absent.add(reg)
            status = "ABSENT"
        else:
            self.db.mark_attendance(reg, "PRESENT")
            self.marked_present.add(reg)
            status = "PRESENT"
        
        self.attend_reg.delete(0, "end")
        self.refresh_attend_tree()
        self.refresh_stats()
        messagebox.showinfo("Success", f"{reg} marked {status}")
    
    def mark_excuse(self):
        if not self.recording:
            messagebox.showerror("Error", "Start recording first")
            return
        
        reg = self.attend_reg.get().strip().upper()
        
        if not reg:
            messagebox.showerror("Error", "Enter registration number")
            return
        
        if not self.dfa.validate(reg):
            messagebox.showerror("Error", "Invalid registration number")
            return
        
        if not self.student_exists(reg):
            messagebox.showerror("Error", f"Student {reg} not registered")
            return
        
        if reg in self.marked_present:
            messagebox.showerror("Error", f"Student {reg} marked PRESENT - cannot excuse")
            return
        
        if reg not in self.marked_absent:
            messagebox.showerror("Error", f"Student {reg} must be marked ABSENT first to excuse")
            return
        
        self.db.mark_attendance(reg, "EXCUSE")
        self.marked_absent.remove(reg)
        self.attend_reg.delete(0, "end")
        self.refresh_attend_tree()
        self.refresh_stats()
        messagebox.showinfo("Success", f"{reg} marked EXCUSE")
    
    def refresh_student_tree(self):
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        
        for student in self.db.get_students():
            self.student_tree.insert('', 'end', values=(student[0], student[1], student[2]))
    
    def refresh_attend_tree(self):
        for item in self.attend_tree.get_children():
            self.attend_tree.delete(item)
        
        today = datetime.now().strftime("%Y-%m-%d")
        for record in self.db.get_attendance():
            if record[0] == today:
                self.attend_tree.insert('', 'end', values=(record[1], record[2], record[3], record[4]))
    
    def refresh_stats(self):
        self.stats_text.config(state="normal")
        self.stats_text.delete(1.0, "end")
        
        students = self.db.get_students()
        attendance = self.db.get_attendance()
        
        today = datetime.now().strftime("%Y-%m-%d")
        today_records = [r for r in attendance if r[0] == today]
        
        present = sum(1 for r in today_records if r[3] == "PRESENT")
        absent = sum(1 for r in today_records if r[3] == "ABSENT")
        excuse = sum(1 for r in today_records if r[3] == "EXCUSE")
        
        stats = f"Total Students: {len(students)} | Present: {present} | Absent: {absent} | Excuse: {excuse} | Marked: {len(today_records)}"
        
        self.stats_text.insert(1.0, stats)
        self.stats_text.config(state="disabled")
    
    def on_closing(self):
        self.db.export_excel("attendance.xlsx")
        self.root.destroy()
    
    def export_excel(self):
        file = filedialog.asksaveasfilename(defaultextension=".xlsx", 
                                           filetypes=[("Excel", "*.xlsx")])
        if not file:
            return
        
        success, msg = self.db.export_excel(file)
        if success:
            messagebox.showinfo("Success", msg)
            self.refresh_stats()
        else:
            messagebox.showerror("Error", msg)


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
