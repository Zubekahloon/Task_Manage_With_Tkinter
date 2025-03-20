import json
from datetime import datetime
from tkinter import messagebox
import tkinter as tk

class Task:
    def __init__(self, title, description, due_date, completed=False):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed
    
    def mark_completed(self):
        self.completed = True

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "completed": self.completed
        }

    def from_dict(task_dict):
        return Task(
            task_dict["title"],
            task_dict["description"],
            task_dict["due_date"],
            task_dict["completed"],
        )


class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()
        

    def save_tasks(self):
        with open(self.filename, "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)
      
    def load_tasks(self):
        try:
            with open(self.filename, "r") as file:
                return [Task.from_dict(task) for task in json.load(file)]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
    
    def add_task(self, title, description, due_date):
        new_task = Task(title, description, due_date)
        self.tasks.append(new_task)
        self.save_tasks()
    
    
    def mark_task_completed(self, task_index):
        try:
            self.tasks[task_index].mark_completed()
            self.save_tasks()
            print("Task marked as completed!")
        except IndexError:
            messagebox.showerror("Invalid task number.")
    
    def delete_task(self, task_index):
        try:
            del self.tasks[task_index]
            self.save_tasks()
            print("Task deleted successfully!")
        except IndexError:
            messagebox.showerror("Invalid task number.")

    def download_tasks(self):
        self.save_tasks()
        messagebox.showinfo("Tasks Saved in tasks.json successfully")
    

class TaskApp:
    def __init__(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("400x450")
       
        self.task_listbox = tk.Listbox(root, width=50, height=15)
        self.task_listbox.pack(pady=10)

        tk.Button(root, text="Add Task", command=self.add_tasks).pack(pady=5)
        tk.Button(root, text="Mark Completed", command=self.mark_completed).pack(pady=5)
        tk.Button(root, text="Delete Task", command=self.delete_task).pack(pady=5)
        tk.Button(root, text="Saved Tasks", command=self.download_tasks).pack(pady=5)

        self.load_tasks()

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for idx, task in enumerate(self.manager.tasks):
            status = "Complete" if task.completed else "Pending"
            self.task_listbox.insert(tk.END, f"{idx + 1}. {task.title} - {task.description} - {status} - {task.due_date}")

    def add_tasks(self):
        addtask = tk.Toplevel(self.root)
        addtask.title("Add Task")
        addtask.geometry("300x200")

        tk.Label(addtask, text="Title:").pack()
        title_entry = tk.Entry(addtask)
        title_entry.pack()

        tk.Label(addtask, text="Description:").pack()
        desc_entry = tk.Entry(addtask)
        desc_entry.pack()

        tk.Label(addtask, text="Due Date (YYYY-MM-DD):").pack()
        date_entry = tk.Entry(addtask)
        date_entry.pack()

        def submit():
            title = title_entry.get()
            description = desc_entry.get()
            due_date = date_entry.get()

            if title and due_date:
                self.manager.add_task(title, description, due_date)
                self.load_tasks()
                addtask.destroy()
            else:
                messagebox.showwarning("Bhai Enter Karo Task Ka Data")

        tk.Button(addtask, text="Add", command=submit).pack()

    def mark_completed(self):
        selected = self.task_listbox.curselection()
        if selected:
            self.manager.mark_task_completed(selected[0])
            self.load_tasks()
        else:
            messagebox.showwarning("Select task to mark as completed!")

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            self.manager.delete_task(selected[0])
            self.load_tasks()
        else:
            messagebox.showwarning("Select task to delete!")

    def download_tasks(self):
        self.manager.download_tasks()



root = tk.Tk()
app = TaskApp(root)
root.mainloop()
