import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

# File to store data
DATA_FILE = "bmi_data.json"

# Load existing data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    else:
        return []

# Save a new record
def save_data(entry):
    data = load_data()
    data.append(entry)
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Calculate BMI
def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            messagebox.showerror("Error", "Weight and Height must be positive.")
            return

        bmi = round(weight / (height ** 2), 2)

        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 25:
            category = "Normal"
        elif 25 <= bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        result_label.config(text=f"BMI: {bmi} ({category})", fg="white", bg="#444444")

        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "weight": weight,
            "height": height,
            "bmi": bmi,
            "category": category
        }
        save_data(entry)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers.")

# Show BMI history
def show_history():
    data = load_data()
    if not data:
        messagebox.showinfo("History", "No data available.")
        return

    history_text = "\n".join([f"{d['timestamp']} - BMI: {d['bmi']} ({d['category']})"
                              for d in data])
    messagebox.showinfo("BMI History", history_text)

# Show BMI Trend graph
def show_graph():
    data = load_data()
    if not data:
        messagebox.showinfo("No Data", "No data to show.")
        return

    dates = [d["timestamp"] for d in data]
    bmis = [d["bmi"] for d in data]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, bmis, marker='o', linestyle='-', color='green')
    plt.xticks(rotation=45)
    plt.title("BMI Trend Over Time")
    plt.xlabel("Date and Time")
    plt.ylabel("BMI Value")
    plt.tight_layout()
    plt.grid(True)
    plt.show()

# GUI Setup
window = tk.Tk()
window.title("BMI Calculator")
window.geometry("400x400")
window.config(bg="#282c34")  # Background color

# Styling helper
label_style = {"bg": "#282c34", "fg": "white", "font": ("Helvetica", 12)}
entry_style = {"bg": "#ffffff", "font": ("Helvetica", 12)}
button_style = {"bg": "#61afef", "fg": "white", "font": ("Helvetica", 11, "bold"), "activebackground": "#4fa3d1"}

# Title
tk.Label(window, text="BMI Calculator", bg="#282c34", fg="#61afef", font=("Helvetica", 16, "bold")).pack(pady=10)

# Input fields
tk.Label(window, text="Enter your Weight (kg):", **label_style).pack(pady=5)
weight_entry = tk.Entry(window, **entry_style)
weight_entry.pack(pady=5)

tk.Label(window, text="Enter your Height (m):", **label_style).pack(pady=5)
height_entry = tk.Entry(window, **entry_style)
height_entry.pack(pady=5)

# Buttons
tk.Button(window, text="Calculate BMI", command=calculate_bmi, **button_style).pack(pady=10)
result_label = tk.Label(window, text="", font=("Helvetica", 13, "bold"), bg="#282c34")
result_label.pack(pady=5)

tk.Button(window, text="Show History", command=show_history, **button_style).pack(pady=5)
tk.Button(window, text="Show Graph", command=show_graph, **button_style).pack(pady=5)

window.mainloop()
