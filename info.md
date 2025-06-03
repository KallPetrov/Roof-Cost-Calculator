## 🧾 How It Works

### 📐 Input Fields

* Length, Width, Ridge Height (in meters)
* Roof type: `Flat`, `Gable`, `Hip`
* Cover material: `Tiles`, `Bitumen`, `Metal Sheets`, etc.
* Labor hours (two workers), transport distance

### 🧮 Calculations

* **Surface area** based on roof geometry
* **Material units and cost** from selected type
* **Beam cost** using spacing and slope math
* **Labor cost**: Two different hourly rates
* **Transport**: Cost per km

### 📤 Exporting

Click **"Export to Excel"** to generate a file named `report.xlsx` in the working directory.

---

## 🧰 Material Cost Configuration

You can update per-unit material costs dynamically from the GUI.
Click the **"Prices"** button, enter new values as prompted.

### Default Material Costs

| Material      | Price (BGN/unit) |
| ------------- | ---------------- |
| Tiles         | 1.20             |
| Bitumen       | 12.00            |
| Metal Sheets  | 25.00            |
| Waterproofing | 18.00            |
| Wooden Boards | 15.00            |
| Concrete      | 40.00            |

---

## 📁 Project Structure

```
roof-cost-calculator/
├── app.py                    # Main application
├── report.xlsx               # Auto-generated Excel report
├── screenshots/              # UI screenshots (optional)
│   └── roof_calculator_ui.png
└── README.md                 # Documentation
```

---

## 🧑‍💻 Customization Ideas

* Add other roof types (e.g., Shed, Mansard)
* Support for multiple material layers
* Localization (e.g., Bulgarian language support)
* Save/load past estimates
* Add PDF export

---

## ⚠️ Notes

* App assumes all units are metric (meters, square meters, km).
* Ensure numerical inputs are valid to avoid errors.
* You must install `openpyxl` if Excel export doesn't work.

---

## 📜 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
Feel free to use and modify for personal or commercial use.

---

## 🤝 Contributing

Pull requests are welcome! Improve calculations, add features, or just refactor the GUI.

