""" 

---- TODO list ---

This proj is a simple todo list

 - way to receive input
 - way to store input
 - way to display input
 - way to delete input
 - way to edit input

"""

import json
file_path = "todo_list.json"

def start(): 
    print("""
    1. Add a task
    2. View tasks
    3. Delete a task
    4. Update a task

    q. Quit
    
    """
    )


    choice = input("Enter your choice: ")
    choice = choice.lower()

    if choice == "1":
        add_task()
    elif choice == "2":
        view_tasks()
    elif choice == "3":
        delete_task()
    elif choice == "4":
        update_tasks()
    elif choice == "q":
        quit()
    else:
        print("No valid input")

def add_task():
    task = input("Enter the task: ")
    todos[task] = False
    print(f"Task '{task}' added successfully!")

def view_tasks():
    if todos == {}:
        print("No tasks found!")
        return 0
    for task, completed in todos.items():
        print(f"{task} {'[x] --- Completed' if completed else '[ ]'}")

def update_tasks():
    if view_tasks() == 0:
        return 0
    update = input("Do you want to update a task? (y/n): ")

    if update.lower() == 'y':
        task = input("Enter the task to update: ")
        if task in todos:
            todos[task] = True
            print(f"Task '{task}' updated successfully!")
        else:
            print(f"Task '{task}' not found!")

def delete_task():
    view_tasks()
    task = input("Enter the task to delete: ")

    if task in todos:
        del todos[task]
        print(f"Task '{task}' deleted successfully!")
    else:
        print(f"Task '{task}' not found!")




# Try to load existing tasks from the JSON file
try:
    with open(file_path, 'r') as f:
        todos = json.load(f)
except FileNotFoundError:
    todos = {}  # If the file doesn't exist, initialize an empty dictionary

print("Welcome to the TODO list! what do you want to do?")
while True:
    start()
    with open(file_path, 'w') as f:     # Save the updated dictionary to the JSON file
        json.dump(todos, f, indent=4)





