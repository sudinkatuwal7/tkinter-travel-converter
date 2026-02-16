from tkinter import *

# functions part

def safe_float(value):
    try:
        return float(value)
    except ValueError:
        return None

def update_formula_label():
    if show_formula_var.get() == 1:
        if mode_var.get() == 1:
            formula_label.config(text="Formula: km = miles × 1.609")
        else:
            formula_label.config(text="Formula: miles = km ÷ 1.609")
    else:
        formula_label.config(text="")

def convert():
    value = safe_float(input_entry.get())
    if value is None:
        result_label.config(text="⚠ enter a number")
        return

    precision = int(precision_scale.get())
    multiplier = int(multiplier_spin.get())

    value = value * multiplier

    if mode_var.get() == 1:  # Miles -> Km
        result = value * 1.609
        result_label.config(text=f"{result:.{precision}f}")
        history_text.insert(END, f"{value} miles = {result:.{precision}f} km\n")
    else:  # Km -> Miles
        result = value / 1.609
        result_label.config(text=f"{result:.{precision}f}")
        history_text.insert(END, f"{value} km = {result:.{precision}f} miles\n")

    history_text.see(END)
    update_formula_label()

def clear_all():
    input_entry.delete(0, END)
    result_label.config(text="0")
    history_text.delete("1.0", END)

def preset_selected(event):
    selection = preset_listbox.curselection()
    if not selection:
        return
    val = preset_listbox.get(selection[0]).split(" - ")[0]
    input_entry.delete(0, END)
    input_entry.insert(END, val)

# screen set up

window = Tk()
window.title("Travel Converter (Unique Tkinter)")
window.config(padx=20, pady=20)

# Title
title = Label(text="🚗 Travel Converter", font=("Arial", 16, "bold"))
title.grid(column=0, row=0, columnspan=4, pady=(0, 10))

# Input
Label(text="Value:").grid(column=0, row=1, sticky="e")
input_entry = Entry(width=12)
input_entry.grid(column=1, row=1, sticky="w")

Label(text="×").grid(column=2, row=1)
multiplier_spin = Spinbox(from_=1, to=50, width=5)
multiplier_spin.grid(column=3, row=1, sticky="w")

# Mode (Radio buttons)
mode_var = IntVar(value=1)
Label(text="Mode:").grid(column=0, row=2, sticky="e")
rb1 = Radiobutton(text="Miles → Km", value=1, variable=mode_var, command=lambda: (update_formula_label(), convert()))
rb2 = Radiobutton(text="Km → Miles", value=2, variable=mode_var, command=lambda: (update_formula_label(), convert()))
rb1.grid(column=1, row=2, sticky="w")
rb2.grid(column=2, row=2, columnspan=2, sticky="w")

# Precision (Scale)
Label(text="Decimals:").grid(column=0, row=3, sticky="e")
precision_scale = Scale(from_=0, to=6, orient=HORIZONTAL)
precision_scale.set(2)
precision_scale.grid(column=1, row=3, columnspan=3, sticky="we")

# Show formula (Checkbutton)
show_formula_var = IntVar(value=1)
show_formula_cb = Checkbutton(text="Show formula", variable=show_formula_var, command=update_formula_label)
show_formula_cb.grid(column=1, row=4, columnspan=3, sticky="w")

formula_label = Label(text="", fg="gray")
formula_label.grid(column=0, row=5, columnspan=4, sticky="w")
update_formula_label()

# Result
Label(text="Result:", font=("Arial", 11, "bold")).grid(column=0, row=6, sticky="e", pady=(10, 0))
result_label = Label(text="0", font=("Arial", 14, "bold"))
result_label.grid(column=1, row=6, sticky="w", pady=(10, 0))

# Buttons
convert_btn = Button(text="Convert", command=convert)
convert_btn.grid(column=2, row=6, sticky="we", padx=(10, 0), pady=(10, 0))

clear_btn = Button(text="Clear", command=clear_all)
clear_btn.grid(column=3, row=6, sticky="we", pady=(10, 0))

# Presets (Listbox)
Label(text="Quick presets:").grid(column=0, row=7, sticky="ne", pady=(10, 0))
preset_listbox = Listbox(height=7, width=28)
presets = [
    "3.1 - 5K race",
    "6.2 - 10K race",
    "13.1 - Half Marathon",
    "26.2 - Marathon",
    "100 - Road trip",
    "250 - Long drive",
    "1 - Just testing",
]
for p in presets:
    preset_listbox.insert(END, p)

preset_listbox.bind("<<ListboxSelect>>", preset_selected)
preset_listbox.grid(column=1, row=7, columnspan=3, sticky="w", pady=(10, 0))

# History (Text)
Label(text="History:").grid(column=0, row=8, sticky="ne", pady=(10, 0))
history_text = Text(height=8, width=40)
history_text.grid(column=1, row=8, columnspan=3, sticky="we", pady=(10, 0))

# Make columns stretch nicely
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_columnconfigure(3, weight=1)

window.mainloop()
