import tkinter as tk
from tkinter import simpledialog, messagebox
import pickle
import os

# File paths for pickle data
data_files = {
    'employees': 'employees.pkl',
    'venues': 'venues.pkl',
    'guests': 'guests.pkl',
    'events': 'events.pkl',
    'clients': 'clients.pkl',
    'suppliers': 'suppliers.pkl'
}

# Load data from files or initialize if not present
data = {}
for key in data_files:
    if os.path.exists(data_files[key]):
        with open(data_files[key], 'rb') as file:
            data[key] = pickle.load(file)
    else:
        data[key] = {}

# Save data to files
def save_data():
    for key, items in data.items():
        with open(data_files[key], 'wb') as file:
            pickle.dump(items, file)

# Manage entities
def manage_entity(entity_type):
    def add_or_modify_entity(modify=False):
        entity_id = simpledialog.askstring("ID", "Enter entity ID:")
        if not entity_id:
            return
        if modify and entity_id not in data[entity_type]:
            messagebox.showerror("Error", "Entity not found.")
            return
        entity = data[entity_type].get(entity_id, {})
        # Define attributes based on entity type
        attributes = ['name', 'address', 'contact_details']  # General attributes
        if entity_type in ['events', 'venues']:
            attributes += ['capacity']
        if entity_type in ['employees']:
            attributes += ['department', 'position']
        for attr in attributes:
            value = simpledialog.askstring("Input", f"Enter {attr}:")
            if value:
                entity[attr] = value
        data[entity_type][entity_id] = entity
        save_data()

    def delete_entity():
        entity_id = simpledialog.askstring("Delete", "Enter entity ID:")
        if entity_id in data[entity_type]:
            del data[entity_type][entity_id]
            save_data()
        else:
            messagebox.showerror("Error", "Entity not found.")

    def display_entity():
        entity_id = simpledialog.askstring("Display", "Enter entity ID:")
        entity = data[entity_type].get(entity_id)
        if entity:
            details = '\n'.join(f"{key}: {value}" for key, value in entity.items())
            messagebox.showinfo("Entity Details", details)
        else:
            messagebox.showerror("Error", "Entity not found.")

    # Entity management window
    root = tk.Toplevel()
    root.title(f"Manage {entity_type}")
    tk.Button(root, text="Add Entity", command=lambda: add_or_modify_entity()).pack(fill=tk.X)
    tk.Button(root, text="Modify Entity", command=lambda: add_or_modify_entity(modify=True)).pack(fill=tk.X)
    tk.Button(root, text="Delete Entity", command=delete_entity).pack(fill=tk.X)
    tk.Button(root, text="Display Entity", command=display_entity).pack(fill=tk.X)

# Main window
main_root = tk.Tk()
main_root.title("Event Management System")
categories = ['employees', 'venues', 'guests', 'events', 'clients', 'suppliers']
for category in categories:
    tk.Button(main_root, text=f"Manage {category.capitalize()}", command=lambda c=category: manage_entity(c)).pack(fill=tk.X)
main_root.mainloop()
