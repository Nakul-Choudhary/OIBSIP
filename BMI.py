import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from PIL import Image, ImageTk 

conn = sqlite3.connect('bmi_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                weight REAL,
                height REAL,
                bmi REAL,
                category TEXT,
                date TEXT
             )''')
conn.commit()

def calculate_bmi(weight, height):
    return weight / (height ** 2)

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

def save_bmi(name, weight, height):
    bmi = calculate_bmi(weight, height)
    category = classify_bmi(bmi)
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO bmi_records (name, weight, height, bmi, category, date) VALUES (?, ?, ?, ?, ?, ?)',
              (name, weight, height, bmi, category, date))
    conn.commit()
    return bmi, category, date

def on_calculate():
    try:
        name = name_entry.get()
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        if not name:
            messagebox.showerror("Input error", "Please enter your name.")
            return
        bmi, category, date = save_bmi(name, weight, height)
        
        result_text.set(f"Your BMI is: {bmi:.2f}\nBMI Category: {category}")
        update_history()
    except ValueError:
        messagebox.showerror("Input error", "Please enter valid numbers for weight and height.")

def update_history():
    name = name_entry.get()
    if name:
        c.execute('SELECT date, bmi FROM bmi_records WHERE name = ? ORDER BY date', (name,))
        records = c.fetchall()
        history_text.set("\n".join([f"{date}: {bmi:.2f}" for date, bmi in records]))

def plot_bmi_trend():
    name = name_entry.get()
    if name:
        c.execute('SELECT date, bmi FROM bmi_records WHERE name = ? ORDER BY date', (name,))
        records = c.fetchall()

        if records:
            dates = [datetime.strptime(record[0], '%Y-%m-%d %H:%M:%S') for record in records]
            bmis = [record[1] for record in records]

            plt.figure(figsize=(10, 5))
            plt.plot(dates, bmis, marker='o')
            plt.xlabel('Date')
            plt.ylabel('BMI')
            plt.title(f'BMI Trend for {name}')
            plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        else:
            messagebox.showinfo("No data", "No BMI records found for this user.")

app = tk.Tk()
app.title("BMI Calculator")

image = Image.open("./background.png")
background_image = ImageTk.PhotoImage(image)

canvas = tk.Canvas(app, width=800, height=600)
canvas.pack(fill="both", expand=True)

canvas.create_image(0, 0, image=background_image, anchor="nw")

frame = tk.Frame(canvas, bg="#ffffff", padx=20, pady=20)
canvas.create_window(400,300, window=frame) 

label_font = ("Arial", 12)
entry_font = ("Arial", 12)
button_font = ("Arial", 12, "bold")
result_font = ("Arial", 14, "bold")

tk.Label(frame, text="Name:", font=label_font, bg="#ffffff").grid(row=0, column=0, padx=10, pady=5, sticky="w")
name_entry = tk.Entry(frame, font=entry_font)
name_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5)

tk.Label(frame, text="Weight (kg):", font=label_font, bg="#ffffff").grid(row=1, column=0, padx=10, pady=5, sticky="w")
weight_entry = tk.Entry(frame, font=entry_font)
weight_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5)

tk.Label(frame, text="Height (m):", font=label_font, bg="#ffffff").grid(row=2, column=0, padx=10, pady=5, sticky="w")
height_entry = tk.Entry(frame, font=entry_font)
height_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=5)

tk.Button(frame, text="Calculate BMI", font=button_font, bg="#4CAF50", fg="#ffffff", command=on_calculate).grid(row=3, columnspan=3, pady=20)
tk.Button(frame, text="View Trend", font=button_font, bg="#2196F3", fg="#ffffff", command=plot_bmi_trend).grid(row=4, columnspan=3, pady=10)

result_text = tk.StringVar()
result_label = tk.Label(frame, textvariable=result_text, font=result_font, bg="#ffffff", fg="#333333")
result_label.grid(row=5, columnspan=3, pady=10)

history_text = tk.StringVar()
history_label = tk.Label(frame, textvariable=history_text, font=label_font, bg="#ffffff", fg="#333333", justify="left")
history_label.grid(row=6, columnspan=3, pady=10)

app.mainloop()

conn.close()