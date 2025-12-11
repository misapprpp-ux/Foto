import tkinter as tk
from tkinter import messagebox
import os

FILENAME = "tasks.txt"

def load_tasks():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r", encoding="utf-8") as f:
        tasks = []
        for line in f.readlines():
            line = line.strip()
            if line.startswith("[x] "):
                tasks.append({"text": line[4:], "done": True})
            else:
                tasks.append({"text": line, "done": False})
        return tasks

def save_tasks():
    with open(FILENAME, "w", encoding="utf-8") as f:
        for task in tasks:
            prefix = "[x] " if task["done"] else ""
            f.write(f"{prefix}{task['text']}\n")

def add_task():
    text = task_entry.get().strip()
    if text:
        tasks.append({"text": text, "done": False})
        task_entry.delete(0, tk.END)
        update_listbox()
        save_tasks()
    else:
        messagebox.showwarning("Attention", "Add a task!")

def delete_task():
    selected = listbox.curselection()
    if selected:
        idx = selected[0]
        confirm = messagebox.askyesno("Delete", f"Do you want to delete the task :\n{tasks[idx]['text']}?")
        if confirm:
            tasks.pop(idx)
            update_listbox()
            save_tasks()
    else:
        messagebox.showwarning("Attention", "Select a task!")

def toggle_done(event=None):
    selected = listbox.curselection()
    if selected:
        idx = selected[0]
        tasks[idx]["done"] = not tasks[idx]["done"]
        update_listbox()
        save_tasks()

def update_listbox(filter_status="all"):
    listbox.delete(0, tk.END)
    for task in tasks:
        if filter_status == "done" and not task["done"]:
            continue
        if filter_status == "todo" and task["done"]:
            continue
        text = task["text"]
        if task["done"]:
            text = "✔ " + text
        listbox.insert(tk.END, text)

def filter_all():
    update_listbox("all")
def filter_done():
    update_listbox("done")
def filter_todo():
    update_listbox("todo")

root = tk.Tk()
root.title("To-Do App")
root.geometry("450x550")
root.configure(bg="#f0f4f8")
root.resizable(False, False)

title = tk.Label(root, text="To-Do List", font=("Segoe UI", 24, "bold"), bg="#f0f4f8", fg="#333")
title.pack(pady=10)

task_entry = tk.Entry(root, font=("Segoe UI", 14))
task_entry.pack(pady=10, padx=20, fill=tk.X)

add_button = tk.Button(root, text="➕ Add task", font=("Segoe UI", 12), bg="#4caf50", fg="white", command=add_task)
add_button.pack(pady=5, padx=20, fill=tk.X)

delete_button = tk.Button(root, text="🗑 Delete task", font=("Segoe UI", 12), bg="#f44336", fg="white", command=delete_task)
delete_button.pack(pady=5, padx=20, fill=tk.X)

listbox = tk.Listbox(root, font=("Segoe UI", 14), bg="white", activestyle="none", selectbackground="#a0c4ff")
listbox.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
listbox.bind("<Double-Button-1>", toggle_done)

frame_filter = tk.Frame(root, bg="#f0f4f8")
frame_filter.pack(pady=5)

btn_all = tk.Button(frame_filter, text="All tasks", command=filter_all, bg="#2cc222", fg="white", width=10)
btn_all.grid(row=0, column=0, padx=5)

btn_done = tk.Button(frame_filter, text="Finished", command=filter_done, bg="#6DA5C0", fg="white", width=10)
btn_done.grid(row=0, column=1, padx=5)

btn_todo = tk.Button(frame_filter, text="Unfinished", command=filter_todo, bg="#86192C", fg="white", width=10)
btn_todo.grid(row=0, column=2, padx=5)

tasks = load_tasks()
update_listbox()

root.mainloop()

