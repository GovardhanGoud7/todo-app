#!/usr/bin/env python3
"""To-Do List: add, view, complete and delete tasks. Tasks are saved in tasks.json.

Run:  python todo_app.py
"""
import json
from pathlib import Path

TASK_FILE = Path(__file__).with_name("tasks.json")


def load_tasks():
    try:
        return json.loads(TASK_FILE.read_text())
    except (OSError, ValueError):
        return []


def save_tasks(tasks):
    try:
        TASK_FILE.write_text(json.dumps(tasks, indent=2))
    except OSError:
        print("(Could not save your tasks.)")


def show_tasks(tasks):
    if not tasks:
        print("\nNo tasks yet. Add one with option 1.")
        return
    print("\nYour tasks:")
    for number, task in enumerate(tasks, start=1):
        mark = "x" if task["done"] else " "
        print(f"  {number}. [{mark}] {task['title']}")
    done = sum(task["done"] for task in tasks)
    print(f"  ({done} of {len(tasks)} done)")


def ask_number(prompt, tasks):
    """Ask for a task number; return its index, or None if invalid."""
    if not tasks:
        print("\nThere are no tasks yet.")
        return None
    show_tasks(tasks)
    text = input(prompt).strip()
    if text.isdigit() and 1 <= int(text) <= len(tasks):
        return int(text) - 1
    print(f"  Please enter a number from 1 to {len(tasks)}.")
    return None


def main():
    tasks = load_tasks()
    print("=== To-Do List ===")
    while True:
        print("\n1) Add task   2) View tasks   3) Mark done   4) Delete task   5) Quit")
        choice = input("Your choice: ").strip()

        if choice == "1":
            title = input("Task: ").strip()
            if title:
                tasks.append({"title": title, "done": False})
                save_tasks(tasks)
                print(f"  Added: {title}")
            else:
                print("  A task can't be empty.")
        elif choice == "2":
            show_tasks(tasks)
        elif choice == "3":
            index = ask_number("Number of the task to mark done: ", tasks)
            if index is not None:
                tasks[index]["done"] = True
                save_tasks(tasks)
                print(f"  Done: {tasks[index]['title']}")
        elif choice == "4":
            index = ask_number("Number of the task to delete: ", tasks)
            if index is not None:
                removed = tasks.pop(index)
                save_tasks(tasks)
                print(f"  Deleted: {removed['title']}")
        elif choice == "5":
            break
        else:
            print("  Please enter 1, 2, 3, 4 or 5.")
    print("Goodbye!")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")