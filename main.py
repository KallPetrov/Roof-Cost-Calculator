import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askfloat
import math
import pandas as pd

# Material prices
COSTS = {
    "Tiles": 1.20,
    "Bitumen": 12.00,
    "Metal Sheets": 25.00,
    "Waterproofing": 18.00,
    "Wooden Boards": 15.00,
    "Concrete": 40.00,
}

WOOD_COST_LM = 8.00
BEAM_SPACING = 0.6
LABOR_COST_PER_HOUR = 20.00
SECOND_LABOR_COST_PER_HOUR = 18.00
TRANSPORT_COST_PER_KM = 1.50

# Global variables for report
last_area = 0
last_units = 0
last_cost = 0
beam_cost = 0
labor_cost = 0
second_labor_cost = 0
transport_cost = 0
total_cost = 0

def update_material_prices():
    for material in COSTS:
        new_price = askfloat(f"Price for {material}", f"Enter new price for {material}:")
        if new_price is not None:
            COSTS[material] = new_price

def calculate_beams(length, width, ridge, roof_type):
    spacing = BEAM_SPACING
    if roof_type == "Flat":
        num_beams = math.ceil(length / spacing)
        beam_length = width
    elif roof_type == "Gable":
        num_beams = math.ceil(length / spacing)
        beam_length = math.sqrt((width / 2)**2 + ridge**2)
    elif roof_type == "Hip":
        num_beams = math.ceil(length / spacing) * 2
        beam_length = math.sqrt((width / 2)**2 + ridge**2)
    else:
        return 0, 0, 0

    total_lm = num_beams * beam_length
    total_cost = total_lm * WOOD_COST_LM
    return num_beams, total_lm, total_cost

def calculate_area():
    global last_area, last_units, last_cost
    global beam_cost, labor_cost, second_labor_cost, transport_cost, total_cost

    try:
        length = float(entry_length.get())
        width = float(entry_width.get())
        ridge = float(entry_height.get())
        labor_hours = float(entry_labor_hours.get())
        second_labor_hours = float(entry_second_labor_hours.get())
        transport_km = float(entry_transport_distance.get())

        roof_type = roof_type_var.get()
        cover_type = cover_type_var.get()

        # Area calculation
        if roof_type == "Flat":
            area = length * width
        elif roof_type == "Gable":
            slope = math.sqrt((width / 2)**2 + ridge**2)
            area = 2 * slope * length
        elif roof_type == "Hip":
            slope1 = math.sqrt((width / 2)**2 + ridge**2)
            slope2 = math.sqrt((length / 2)**2 + ridge**2)
            area = 2 * slope1 * length + 2 * slope2 * width
        else:
            messagebox.showerror("Error", "Please select a roof type.")
            return

        if cover_type == "Tiles":
            units = area * 10
        elif cover_type == "Bitumen":
            units = area / 3
        elif cover_type == "Metal Sheets":
            units = area / 2
        elif cover_type == "Waterproofing":
            units = area / 5
        elif cover_type == "Wooden Boards":
            units = area / 4
        elif cover_type == "Concrete":
            units = area / 2
        else:
            units = 0

        cost = math.ceil(units) * COSTS.get(cover_type, 0.0)
        labor_cost = labor_hours * LABOR_COST_PER_HOUR
        second_labor_cost = second_labor_hours * SECOND_LABOR_COST_PER_HOUR
        transport_cost = transport_km * TRANSPORT_COST_PER_KM

        _, _, beam_cost = calculate_beams(length, width, ridge, roof_type)

        total_cost = cost + beam_cost + labor_cost + second_labor_cost + transport_cost

        last_area = area
        last_units = math.ceil(units)
        last_cost = cost

        label_result.config(
            text=f"Area: {area:.2f} m²\n"
                 f"Materials ({cover_type}): {last_units} units | Cost: {cost:.2f} BGN\n"
                 f"Beams: {beam_cost:.2f} BGN\n"
                 f"Labor (Worker 1): {labor_cost:.2f} BGN\n"
                 f"Labor (Worker 2): {second_labor_cost:.2f} BGN\n"
                 f"Transport: {transport_cost:.2f} BGN\n"
                 f"Total: {total_cost:.2f} BGN"
        )

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")

def export_excel():
    try:
        data = {
            "Description": [
                "Roof Type", "Covering", "Area", "Materials",
                "Beams", "Labor (Worker 1)", "Labor (Worker 2)", "Transport", "Total"
            ],
            "Amount": [
                roof_type_var.get(),
                cover_type_var.get(),
                f"{last_area:.2f} m²",
                f"{last_units} pcs | {last_cost:.2f} BGN",
                f"{beam_cost:.2f} BGN",
                f"{labor_cost:.2f} BGN",
                f"{second_labor_cost:.2f} BGN",
                f"{transport_cost:.2f} BGN",
                f"{total_cost:.2f} BGN"
            ]
        }
        df = pd.DataFrame(data)
        df.to_excel("report.xlsx", index=False)
        messagebox.showinfo("Done", "The report has been saved as report.xlsx")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI
root = tk.Tk()
root.title("Roof Cost Calculator by Hexagon Lab")

ttk.Label(root, text="Length (m):").grid(row=0, column=0)
entry_length = ttk.Entry(root)
entry_length.grid(row=0, column=1)

ttk.Label(root, text="Width (m):").grid(row=1, column=0)
entry_width = ttk.Entry(root)
entry_width.grid(row=1, column=1)

ttk.Label(root, text="Ridge Height (m):").grid(row=2, column=0)
entry_height = ttk.Entry(root)
entry_height.grid(row=2, column=1)

ttk.Label(root, text="Labor (hours Worker 1):").grid(row=3, column=0)
entry_labor_hours = ttk.Entry(root)
entry_labor_hours.grid(row=3, column=1)

ttk.Label(root, text="Labor (hours Worker 2):").grid(row=4, column=0)
entry_second_labor_hours = ttk.Entry(root)
entry_second_labor_hours.grid(row=4, column=1)

ttk.Label(root, text="Transport (km):").grid(row=5, column=0)
entry_transport_distance = ttk.Entry(root)
entry_transport_distance.grid(row=5, column=1)

roof_type_var = tk.StringVar(value="Flat")
cover_type_var = tk.StringVar(value="Tiles")

ttk.Combobox(root, textvariable=roof_type_var, values=["Flat", "Gable", "Hip"]).grid(row=6, column=0)
ttk.Combobox(root, textvariable=cover_type_var, values=list(COSTS.keys())).grid(row=6, column=1)

ttk.Button(root, text="Calculate", command=calculate_area).grid(row=7, column=0)
ttk.Button(root, text="Prices", command=update_material_prices).grid(row=7, column=1)
ttk.Button(root, text="Export to Excel", command=export_excel).grid(row=8, column=0, columnspan=2)

label_result = ttk.Label(root, text="Results will appear here", justify="left")
label_result.grid(row=9, column=0, columnspan=2, pady=10)

root.mainloop()
