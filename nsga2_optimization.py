# =========================================================
# NSGA-II INSPIRED SUSTAINABLE CONCRETE MIX DESIGN (TKINTER)
# =========================================================

import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
import joblib

# =========================================================
# LOAD TRAINED MODEL & DATASET
# =========================================================

model = joblib.load("best_model.pkl")

df = pd.read_csv("data/Concrete_Data_10000.csv")

target_col = [c for c in df.columns if "compressive" in c.lower()][0]
features = df.drop(target_col, axis=1).columns.tolist()

X = df[features]

# Identify important columns
cement_col = [c for c in features if "cement" in c.lower()][0]
slag_col   = [c for c in features if "slag" in c.lower()][0]
fly_col    = [c for c in features if "fly" in c.lower()][0]
age_col    = [c for c in features if "age" in c.lower()][0]

# =========================================================
# CO₂ EMISSION FACTORS (kg CO₂ per kg material)
# =========================================================

co2_factors = {
    "cement": 0.90,
    "slag": 0.07,
    "fly": 0.02,
    "water": 0.0003,
    "coarse": 0.005,
    "fine": 0.005,
    "superplasticizer": 0.50
}

def calculate_co2(mix):
    total = 0.0
    for col in mix.index:
        for key, factor in co2_factors.items():
            if key in col.lower():
                total += mix[col] * factor
    return total

# =========================================================
# NSGA-II INSPIRED SUSTAINABLE MIX SELECTION
# =========================================================

def get_sustainable_mix(target_mpa):
    best_mix = None
    best_score = 1e9
    best_co2 = None
    achieved_mpa = None

    for _, row in df.iterrows():
        mix = row[features]

        cement = mix[cement_col]
        slag   = mix[slag_col]
        fly    = mix[fly_col]
        age    = mix[age_col]

        binder = cement + slag + fly
        if binder == 0:
            continue

        # -------- HARD CONSTRAINTS --------
        if not (0.30 <= cement / binder <= 0.50):
            continue
        if not (0.20 <= slag / binder <= 0.40):
            continue
        if not (0.10 <= fly / binder <= 0.30):
            continue
        if age > 56:
            continue

        pred = model.predict(pd.DataFrame([mix], columns=features))[0]
        co2 = calculate_co2(mix)

        # -------- NSGA-II INSPIRED FITNESS --------
        # Objective 1: Strength deviation
        # Objective 2: CO₂ emission
        score = abs(pred - target_mpa) * 100 + co2

        if score < best_score:
            best_score = score
            best_mix = mix
            best_co2 = co2
            achieved_mpa = pred

    if best_mix is None:
        return None, None, None, None

    # CO₂ Risk Classification
    if best_co2 < 200:
        risk = "LOW CO₂ (SUSTAINABLE)"
    elif best_co2 < 300:
        risk = "MODERATE CO₂"
    else:
        risk = "HIGH CO₂"

    return best_mix, achieved_mpa, best_co2, risk

# =========================================================
# TKINTER CALLBACK FUNCTION
# =========================================================

def run_optimization():
    try:
        target = float(target_entry.get())
        mix, achieved, co2, risk = get_sustainable_mix(target)

        if mix is None:
            messagebox.showwarning(
                "No Solution",
                "No sustainable mix satisfies the given constraints."
            )
            return

        output.delete("1.0", tk.END)
        output.insert(tk.END, f"TARGET MPa       : {target}\n")
        output.insert(tk.END, f"ACHIEVED MPa     : {achieved:.2f}\n")
        output.insert(tk.END, f"TOTAL CO₂       : {co2:.2f} kg CO₂/m³\n")
        output.insert(tk.END, f"CO₂ RISK LEVEL  : {risk}\n\n")

        output.insert(tk.END, "BALANCED SUSTAINABLE MIX PROPORTIONS\n")
        output.insert(tk.END, "-" * 60 + "\n")

        for f in features:
            output.insert(tk.END, f"{f}: {mix[f]:.2f}\n")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid MPa value")

# =========================================================
# TKINTER UI (PROFESSIONAL)
# =========================================================

root = tk.Tk()
root.title("Sustainable Concrete Mix Design (NSGA-II Inspired)")
root.geometry("900x650")
root.configure(bg="#f4f6f8")

# Header
header = tk.Frame(root, bg="#1f4e79", height=80)
header.pack(fill="x")

tk.Label(
    header,
    text="SUSTAINABLE CONCRETE MIX DESIGN SYSTEM",
    bg="#1f4e79",
    fg="white",
    font=("Arial", 20, "bold")
).pack(pady=20)

# Main Frame
main_frame = tk.Frame(root, bg="#f4f6f8")
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Input Section
input_frame = tk.LabelFrame(
    main_frame,
    text=" Input: Target Strength ",
    font=("Arial", 12, "bold"),
    bg="#f4f6f8",
    padx=20,
    pady=15
)
input_frame.pack(fill="x", pady=10)

tk.Label(
    input_frame,
    text="Enter Target Compressive Strength (MPa):",
    bg="#f4f6f8",
    font=("Arial", 11)
).grid(row=0, column=0, sticky="w")

target_entry = tk.Entry(input_frame, width=15, font=("Arial", 12))
target_entry.grid(row=0, column=1, padx=10)

# Button
tk.Button(
    main_frame,
    text="Generate Sustainable Mix",
    bg="#2e7d32",
    fg="white",
    font=("Arial", 12, "bold"),
    padx=20,
    pady=8,
    command=run_optimization
).pack(pady=10)

# Output Section
output_frame = tk.LabelFrame(
    main_frame,
    text=" Output: Optimized Mix & CO₂ Assessment ",
    font=("Arial", 12, "bold"),
    bg="#f4f6f8",
    padx=15,
    pady=10
)
output_frame.pack(fill="both", expand=True, pady=10)

output = tk.Text(
    output_frame,
    font=("Consolas", 11),
    bg="white",
    fg="black",
    wrap="word"
)
output.pack(fill="both", expand=True)

# Footer
footer = tk.Frame(root, bg="#e0e0e0", height=30)
footer.pack(fill="x")

tk.Label(
    footer,
    text="M.Tech Final Year Project | Sustainable Concrete Mix Design using ML & NSGA-II Concept",
    bg="#e0e0e0",
    font=("Arial", 9)
).pack(pady=5)

root.mainloop()
