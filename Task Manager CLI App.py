'''💡 Objective: Build a simple command-line Task Manager that allows users to 
add, view, update, and delete tasks. This project will help you practice file handling, 
lists, dictionaries, functions, and loops—all fundamentals of Python.'''

'''🔹 Features:
✅ Add new tasks
✅ View all tasks
✅ Mark tasks as completed
✅ Delete tasks
✅ Save tasks to a text file for persistence'''

# Step up the task list
    # Use a list of dictionaries to store tasks.
    # Each task should have a title, status (pending/completed), and due date.

import csv
import os
import pandas as pd


pandas_available = True

tasks = []

def add_task(title, due_date):
    tasks.append({'Title': title, 'Status': 'Pending', 'Due Date': due_date})
    print(f'Task {title} added successfully\n') 

    # Menu Loop
while True: 
    print('''\n--- Welcome Back, Alvin!---\n\n
        \n1. Add a task
        \n2. View tasks
        \n3. Update task status
        \n4. Delete a task
        \n5. Save tasks to a file
        \n6. Load tasks from a file
        \n7. Exit
              ''')
    choice = input('Enter your choice (1-6): ')

    if choice == '1':
        title =  input('Enter task title: ').strip()
        due_date = input('Enter due date (YYYY-MM-DD): ').strip()
        
        if title and due_date:
            add_task(title, due_date)
        else:
            print('Error: Task title and due date cannot be empty.')
    
    # 2. View Task
    elif choice == '2':
        print('\n---Current Task---')
        if not tasks:
            print('No tasks added yet.')
        else:
            for idx, task in enumerate(tasks, start= 1):
                print(f"{idx}. {task['Title']} | {task['Status']} | Due: {task['Due Date']}")

    # 3. Update Task
    elif choice == '3':
        i = input('Select task to update:\n> ')
        if not tasks:
            print('No tasks available to update.')
        else:
            print('\n---Current Task---')
            for idx, task in enumerate(tasks, start=1):
                print(f'{idx}. {task['Title']} | {task['Status']} | Due: {task['Due Date']}')

            try:
                task_index = int(input('Select task number to update (or 0 to cancel): '))
                if task_index == 0:
                    print('Update canceled.')
                elif 1 <= task_index <= len(tasks):

                    new_status = input('Enter new status (Pending/Completed): ').strip().capitalize()
                    if new_status in ['Pending', 'Completed']:
                        tasks[task_index -1]['Status'] = new_status
                        print (f"Task '{tasks[task_index-1]['Title']}' updated to {new_status}")

                    else:
                        print("Invalid status. Please enter 'Pending' or 'Completed'.")
                else:
                    print('Invalid task number.')
            except ValueError:
                print('Please enter a valid number.')

    # 4. Delete Task
    elif choice == '4':
        i = input ('Select task to delete:\n> ')
        if not tasks:
            print('No tasks available to delete.')
        else:
            print('\n---Current Task---')
            for idx, task in enumerate(tasks, start=1):
                print(f'{idx}. {task['Title']} | {task['Status']} | Due: {task['Due Date']}')

            try:
                task_index = int(input('Select task number to delete (or 0 to cancel): '))
                if task_index ==0:
                    print('Deleting task canceled.')
                elif 1 <= task_index <= len(tasks):
                    delete_task = input('Are you sure?: (yes/no): ').strip().capitalize()
                    if delete_task in ['Yes', 'No']:
                        deleted_task = tasks.pop(task_index - 1)
                        print(f"Task '{deleted_task['Title']}' deleted successfully.")
                    else:
                        print('Invalid.')
                else:
                    print('Invalid task number.')
            except ValueError:
                print('Please enter a valid number.')

    # 5. Save tasks to file
    elif choice == '5':
        print('\n---Save Tasks---')
        print('1. Save as CSV')
        print('2. Save as XLSX')
        print('3. Save as TXT')
        save_choice = input('Ent6er your choice (1-3): ')

        filename = input('Enter filename: ').strip()

        if not filename:
            filename = 'tasks'

        if save_choice == '1':
            # Save as csv
            with open(f'{filename}.csv', 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['Title', 'Status', 'Due Date'])
                writer.writeheader()
                writer.writerows(tasks)
            print(f'Tasks saved to {filename}.csv')
        elif save_choice == '2':
            # save as xlsx
            if pandas_available:
                df = pd.DataFrame(tasks)
                df.to_excel(f'{filename}.xlsx', index=False)
                print(f'Tasks saved to {filename}.xlsx')
            else:
                print('Please Install pandas openpyxl')
        elif save_choice == '3':
            # save as txt/json
            with open(f'{filename}.txt', 'w') as file:
                for task in tasks:
                    file.write(f'{task['Title']}|{task['Status']}|{task['Due Date']}\n')
            print(f'Tasks saved to {filename}.txt')

        else:
            print('Invalid choice. Tasks not saved.')

    # 6. Load task file
    # 6. Load tasks from a file
    elif choice == '6':
        print("\n--- Load Tasks ---")
        print("1. Load from CSV")
        print("2. Load from XLSX")
        print("3. Load from TXT")
        load_choice = input("Enter your choice (1-3): ")
        
        filename = input('Enter filename (without extension): ').strip()
        if not filename:
            filename = 'tasks'
        
        if load_choice == '1':
            # Load from CSV
            try:
                with open(f'{filename}.csv', 'r', newline='') as file:
                    reader = csv.DictReader(file)
                    tasks = list(reader)
                print(f'Tasks loaded from {filename}.csv')
            except FileNotFoundError:
                print(f'File {filename}.csv not found.')
            except Exception as e:
                print(f'Error loading tasks: {e}')
        
        elif load_choice == '2':
            # Load from XLSX
            if pandas_available:
                try:
                    df = pd.read_excel(f'{filename}.xlsx')
                    tasks = df.to_dict('records')
                    print(f'Tasks loaded from {filename}.xlsx')
                except FileNotFoundError:
                    print(f'File {filename}.xlsx not found.')
                except Exception as e:
                    print(f'Error loading tasks: {e}')
            else:
                print("XLSX support requires pandas and openpyxl. Please install them using:")
                print("pip install pandas openpyxl")
        
        elif load_choice == '3':
            # Load from TXT (your original method)
            try:
                with open(f'{filename}.txt', 'r') as file:
                    tasks = []
                    for line in file:
                        title, status, due_date = line.strip().split('|')
                        tasks.append({'Title': title, 'Status': status, 'Due Date': due_date})
                print(f'Tasks loaded from {filename}.txt')
            except FileNotFoundError:
                print(f'File {filename}.txt not found.')
            except Exception as e:
                print(f'Error loading tasks: {e}')
        
        else:
            print("Invalid choice. No tasks loaded.")

    elif choice == '7':
        print('Closing program...')
        break



### What if I just got the idea or the task pop on my head so I have to input it.


