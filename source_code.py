import tkinter as tk
from tkinter import messagebox, ttk
import math
import json
import os
import webbrowser
from datetime import datetime

#swaraj-24052025
#python-3.12
#upload-2
#final

DATA_FILE = 'attendance_data.json'

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        history = json.load(f)
else:
    history = []

def get_cumulative():
    total_sum = sum(item['total'] for item in history)
    attended_sum = sum(item['attended'] for item in history)
    percent = (attended_sum / total_sum) * 100 if total_sum > 0 else 0
    return total_sum, attended_sum, percent

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def pct_color(p):
    return 'red' if p < 75 else 'green'

def refresh_display():
    tot_sum, att_sum, cum_perc = get_cumulative()
    for row in overall_table.get_children():
        overall_table.delete(row)
    overall_table.insert('', 'end', values=(att_sum, tot_sum, f"{cum_perc:.2f}%"), tags=(pct_color(cum_perc),))

    for row in history_table.get_children():
        history_table.delete(row)
    for item in history:
        date = datetime.strptime(item['date'], '%Y-%m-%d').strftime('%d%m%Y')
        tot = item['total']
        att = item['attended']
        perc = (att / tot) * 100
        history_table.insert('', 'end', values=(date, att, tot, f"{perc:.2f}%"), tags=(pct_color(perc),))

def calculate_percentage():
    try:
        total = int(entry_total.get())
        attended = int(entry_attended.get())
        if total <= 0 or attended < 0 or attended > total:
            raise ValueError
    except ValueError:
        messagebox.showerror("Input Error", "Enter valid integers: 0 ≤ attended ≤ total, total > 0.")
        return
    percent = (attended / total) * 100
    label_today.config(text=f"Today: {percent:.2f}%", fg=pct_color(percent), font=('Arial', 14, 'bold'))

    try:
        N = int(entry_future.get())
        if N < 0:
            raise ValueError
    except ValueError:
        label_bunks.config(text="Enter valid future lectures.")
        return
    tot_sum, att_sum, _ = get_cumulative()
    required = 0.75 * (tot_sum + total + N)
    min_future = math.ceil(required - (att_sum + attended))
    bunkable = max(0, N - min_future)
    label_bunks.config(text=f"Can bunk {bunkable} lectures out of {N}")

def add_record():
    try:
        total = int(entry_total.get())
        attended = int(entry_attended.get())
    except ValueError:
        messagebox.showerror("Save Error", "Calculate before saving.")
        return
    date_str = datetime.now().strftime('%Y-%m-%d')
    history.append({'date': date_str, 'total': total, 'attended': attended})
    save_data()
    refresh_display()
    messagebox.showinfo("Saved", "Record added.")

root = tk.Tk()
root.title("📝 Attendance Tracker & Bunker")
root.geometry("350x650")  
root.resizable(False, False)
#fixed size cause might later port in mobile

overall_frame = tk.Frame(root, pady=5)
overall_frame.pack()
cols_over = ('Attended', 'Total', '%')
overall_table = ttk.Treeview(overall_frame, columns=cols_over, show='headings', height=1)
for col in cols_over:
    overall_table.heading(col, text=col)
    overall_table.column(col, width=100, anchor='center')
overall_table.pack()
overall_table.tag_configure('red', foreground='red')
overall_table.tag_configure('green', foreground='green')

inputs = tk.Frame(root, padx=10, pady=10)
inputs.pack()

tk.Label(inputs, text="Today's total lectures :").grid(row=0, column=0, padx=5, pady=5)
entry_total = tk.Entry(inputs, width=5)
entry_total.grid(row=0, column=1)

tk.Label(inputs, text="Attended lectures today :").grid(row=1, column=0, padx=5, pady=5)
entry_attended = tk.Entry(inputs, width=5)
entry_attended.grid(row=1, column=1)

tk.Label(inputs, text="Next day total lectures :").grid(row=2, column=0, padx=5, pady=5)
entry_future = tk.Entry(inputs, width=5)
entry_future.grid(row=2, column=1)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)
btn_calc = tk.Button(btn_frame, text="Calculate", width=12, command=calculate_percentage)
btn_calc.pack(side='left', padx=5)
btn_save = tk.Button(btn_frame, text="Save Record", width=12, command=add_record)
btn_save.pack(side='left', padx=5)

label_today = tk.Label(root, text="Today: --%", font=('Arial', 14))
label_today.pack(pady=5)
label_bunks = tk.Label(root, text="Bunks Possible : --", font=('Arial', 12))
label_bunks.pack(pady=5)

hist_frame = tk.Frame(root)
hist_frame.pack(pady=5, fill='both', expand=True)
cols_hist = ('Date', 'Attended', 'Total', '%')
history_table = ttk.Treeview(hist_frame, columns=cols_hist, show='headings', height=8)
for col in cols_hist:
    history_table.heading(col, text=col)
    history_table.column(col, anchor='center', width=70)
history_table.pack(side='left', fill='both', expand=True)
history_table.tag_configure('red', foreground='red')
history_table.tag_configure('green', foreground='green')

scroll = tk.Scrollbar(hist_frame, command=history_table.yview)
history_table.configure(yscroll=scroll.set)
scroll.pack(side='right', fill='y')

brand_frame = tk.Frame(root)
brand_frame.pack(side='bottom', anchor='e', padx=5, pady=2)
brand_label = tk.Label(brand_frame, text="Made by Swaraj -", font=('Arial', 8))
brand_label.pack(side='left')
brand_link = tk.Label(brand_frame, text="GitHub", fg="blue", cursor="hand2", font=('Arial', 8, 'underline'))
brand_link.pack(side='left', padx=(2,0))

def open_link(event):
    webbrowser.open("https://github.com/Swaraj-SG")
brand_link.bind("<Button-1>", open_link)

refresh_display()
root.mainloop()

#end of code :)