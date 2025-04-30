import tkinter as tk
from tkinter import ttk, messagebox
import csv

# Function to load the CSV file and create the graph
def load_graph(file_path):
    graph = {}
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        print("CSV Headers:", headers)  # Debugging line to print headers
        for edge in reader:
            from_node = edge['from_node']
            to_node = edge['to_node']
            weight = int(edge['cost'])
            capacity = int(edge['capacity'])
            pipe_name = edge['pipe_name']
            
            if from_node not in graph:
                graph[from_node] = []
            graph[from_node].append((to_node, weight, capacity, pipe_name))
            
            if to_node not in graph:
                graph[to_node] = []
            graph[to_node].append((from_node, weight, capacity, pipe_name))
    return graph

# Function to find all paths with constraints
def find_paths(graph, start, end, max_cost, min_capacity):
    def dfs(node, cost, path, pipes):
        if cost > max_cost:
            return
        if node == end:
            paths.append((path.copy(), pipes.copy()))
            return
        for neighbor, weight, capacity, pipe_name in graph.get(node, []):
            if capacity >= min_capacity and neighbor not in path:
                path.append(neighbor)
                pipes.append((pipe_name, capacity))
                dfs(neighbor, cost + weight, path, pipes)
                path.pop()
                pipes.pop()
    
    paths = []
    dfs(start, 0, [start], [])
    return paths

# Function to handle the button click event
def on_find_paths():
    start_node = start_node_entry.get()
    end_node = end_node_entry.get()
    max_cost = int(max_cost_entry.get())
    min_capacity = int(min_capacity_entry.get())
    
    paths = find_paths(graph, start_node, end_node, max_cost, min_capacity)
    
    path_listbox.delete(0, tk.END)
    pipe_listbox.delete(0, tk.END)
    
    if paths:
        for i, (path, pipes) in enumerate(paths):
            path_str = f"Path {i+1}: " + " -> ".join(path)
            path_listbox.insert(tk.END, path_str)
            path_data[path_str] = pipes
    else:
        path_listbox.insert(tk.END, "No paths found.")

# Function to handle the selection of a path
def on_select_path(event):
    selected_path_index = path_listbox.curselection()
    if not selected_path_index:
        return
    selected_path = path_listbox.get(selected_path_index)
    pipes = path_data.get(selected_path, [])
    
    pipe_listbox.delete(0, tk.END)
    
    for pipe_name, capacity in pipes:
        pipe_listbox.insert(tk.END, f"{pipe_name} (Capacity: {capacity})")

# Function to handle the selection of a pipe and copy it to clipboard
def on_select_pipe(event):
    selected_pipe_index = pipe_listbox.curselection()
    if not selected_pipe_index:
        return
    selected_pipe = pipe_listbox.get(selected_pipe_index)
    root.clipboard_clear()
    root.clipboard_append(selected_pipe)
    root.update()  # Now it stays on the clipboard after the window is closed

# Load the graph from the CSV file
graph = load_graph('Lambdas.csv')

# Create the main window
root = tk.Tk()
root.title("Path Finder")

# Create and place the input fields and labels
ttk.Label(root, text="Start Node:").grid(column=0, row=0, padx=10, pady=5, sticky="ew")
start_node_entry = ttk.Entry(root)
start_node_entry.grid(column=1, row=0, padx=10, pady=5, sticky="ew")

ttk.Label(root, text="End Node:").grid(column=0, row=1, padx=10, pady=5, sticky="ew")
end_node_entry = ttk.Entry(root)
end_node_entry.grid(column=1, row=1, padx=10, pady=5, sticky="ew")

ttk.Label(root, text="Max Cost:").grid(column=0, row=2, padx=10, pady=5, sticky="ew")
max_cost_entry = ttk.Entry(root)
max_cost_entry.grid(column=1, row=2, padx=10, pady=5, sticky="ew")

ttk.Label(root, text="Min Capacity:").grid(column=0, row=3, padx=10, pady=5, sticky="ew")
min_capacity_entry = ttk.Entry(root)
min_capacity_entry.grid(column=1, row=3, padx=10, pady=5, sticky="ew")

# Create and place the button
find_paths_button = ttk.Button(root, text="Find Paths", command=on_find_paths)
find_paths_button.grid(column=0, row=4, columnspan=2, padx=10, pady=10, sticky="ew")

# Create and place the listbox for displaying paths
path_listbox = tk.Listbox(root)
path_listbox.grid(column=0, row=5, columnspan=2, padx=10, pady=10, sticky="nsew")
path_listbox.bind('<<ListboxSelect>>', on_select_path)

# Create and place the listbox for displaying pipes
pipe_listbox = tk.Listbox(root)
pipe_listbox.grid(column=2, row=5, columnspan=2, padx=10, pady=10, sticky="nsew")
pipe_listbox.bind('<<ListboxSelect>>', on_select_pipe)

# Make the listboxes resizable
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_rowconfigure(5, weight=1)

# Dictionary to store path data
path_data = {}

# Start the main event loop
root.mainloop()
