import tkinter as tk
from tkinter import messagebox

class TaskManager:
    def __init__(self, win):
        self.win = win
        self.win.title("Quản Lý Công Việc")
        self.tasks = []
        # Tiêu đề
        self.title_label = tk.Label(win, text="Danh Sách Công Việc", font=("Times new roman", 16))
        self.title_label.pack(pady=10)

        # Frame cho danh sách công việc
        self.task_frame = tk.Frame(win)
        self.task_frame.pack(pady=10)

        # Danh sách công việc
        self.task_listbox = tk.Listbox(self.task_frame, width=60, height=10)
        self.task_listbox.pack(side=tk.LEFT)

        # Thanh cuộn
        self.scrollbar = tk.Scrollbar(self.task_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)

        # Nhập công việc
        self.task_entry = self.create_entry(win, "Nhập công việc")
        
        # Nhập họ tên
        self.name_entry = self.create_entry(win, "Nhập họ tên")

        # Nhập mã số sinh viên
        self.id_entry = self.create_entry(win, "Nhập mã số sinh viên")

        # Nút thêm công việc
        self.add_button = tk.Button(win, text="Thêm Công Việc", command=self.add_task)
        self.add_button.pack(pady=5)

        # Nút sửa công việc
        self.edit_button = tk.Button(win, text="Sửa Công Việc", command=self.edit_task)
        self.edit_button.pack(pady=5)

        # Nút xóa công việc
        self.delete_button = tk.Button(win, text="Xóa Công Việc", command=self.delete_task)
        self.delete_button.pack(pady=5)

    def create_entry(self, parent, placeholder):
        entry = tk.Entry(parent, width=30)
        entry.pack(pady=5)
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda e: self.on_entry_click(entry, placeholder))
        entry.bind("<FocusOut>", lambda e: self.on_focus_out(entry, placeholder))
        return entry

    def on_entry_click(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def on_focus_out(self, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg='grey')

    def add_task(self):
        task = self.task_entry.get()
        name = self.name_entry.get()
        student_id = self.id_entry.get()

        if task and name and student_id:
            full_task = f"{task} | Họ Tên: {name} | Mã SV: {student_id}"
            self.tasks.append(full_task)
            self.task_listbox.insert(tk.END, full_task)
            self.task_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.id_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng nhập đầy đủ thông tin.")

    def edit_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            task_details = self.tasks[selected_index].split(" | ")
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, task_details[0])
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, task_details[1].replace("Họ Tên: ", ""))
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, task_details[2].replace("Mã SV: ", ""))
            
            # Cập nhật công việc sau khi sửa
            self.update_button = tk.Button(self.win, text="Cập Nhật Công Việc", command=lambda: self.update_task(selected_index))
            self.update_button.pack(pady=5)
        except IndexError:
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn công việc để sửa.")

    def update_task(self, index):
        task = self.task_entry.get()
        name = self.name_entry.get()
        student_id = self.id_entry.get()

        if task and name and student_id:
            full_task = f"{task} | Họ Tên: {name} | Mã SV: {student_id}"
            self.tasks[index] = full_task
            self.task_listbox.delete(index)
            self.task_listbox.insert(index, full_task)
            self.task_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.id_entry.delete(0, tk.END)
            self.update_button.destroy()  # Xóa nút cập nhật sau khi sửa xong
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng nhập đầy đủ thông tin.")

    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.task_listbox.delete(selected_index)
            del self.tasks[selected_index]
        except IndexError:
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn công việc để xóa.")

if __name__ == "__main__":
    win = tk.Tk()
    task_manager = TaskManager(win)
    win.mainloop()