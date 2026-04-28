import customtkinter as ctk
from datetime import datetime
import tkinter.messagebox as messagebox
import os
import sys

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ExpresswayPro_v1(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Expressway Pro Toolkit v1.0")
        self.geometry("900x600")

        self.apply_custom_icon()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="TRIP SETTINGS", font=("Roboto", 18, "bold")).pack(pady=20)

        self.vehicle_type = ctk.CTkOptionMenu(self.sidebar, values=["Car/Jeep", "Van/Bus", "Multi-Axle"])
        self.vehicle_type.pack(pady=10, padx=20)

        self.fuel_price = ctk.CTkEntry(self.sidebar, placeholder_text="Fuel Price (LKR per L)")
        self.fuel_price.pack(pady=10, padx=20)

        self.limit_val = ctk.IntVar(value=100)
        self.limit_label = ctk.CTkLabel(self.sidebar, text="Speed Limit: 100 km/h")
        self.limit_label.pack(pady=(20, 0))
        self.limit_slider = ctk.CTkSlider(self.sidebar, from_=60, to=120, variable=self.limit_val, command=self.update_limit_label)
        self.limit_slider.pack(pady=10, padx=20)

        self.cons_val = ctk.IntVar(value=12)
        self.cons_label = ctk.CTkLabel(self.sidebar, text="Fuel Economy: 12 km/L")
        self.cons_label.pack(pady=(20, 0))
        self.cons_slider = ctk.CTkSlider(self.sidebar, from_=5, to=30, variable=self.cons_val, command=self.update_cons_label)
        self.cons_slider.pack(pady=10, padx=20)

        self.export_btn = ctk.CTkButton(self.sidebar, text="Export Trip Log", fg_color="#28a745", hover_color="#218838", command=self.export_data)
        self.export_btn.pack(side="bottom", pady=20, padx=20)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=30, pady=20, sticky="nsew")

        self.input_row = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.input_row.pack(fill="x", pady=10)

        self.dist_entry = ctk.CTkEntry(self.input_row, placeholder_text="Distance (km)", width=140)
        self.dist_entry.grid(row=0, column=0, padx=5)
        self.entry_time = ctk.CTkEntry(self.input_row, placeholder_text="Entry (HH:MM)", width=140)
        self.entry_time.grid(row=0, column=1, padx=5)
        self.exit_time = ctk.CTkEntry(self.input_row, placeholder_text="Exit (HH:MM)", width=140)
        self.exit_time.grid(row=0, column=2, padx=5)

        self.calc_btn = ctk.CTkButton(self.main_frame, text="Calculate Trip Data", command=self.calculate_all, height=45, font=("Roboto", 16, "bold"))
        self.calc_btn.pack(pady=20, fill="x")

        self.res_frame = ctk.CTkFrame(self.main_frame)
        self.res_frame.pack(fill="both", expand=True, pady=10)
        self.speed_display = ctk.CTkLabel(self.res_frame, text="Avg Speed: -- km/h", font=("Roboto", 24, "bold"))
        self.speed_display.pack(pady=15)
        self.cost_display = ctk.CTkLabel(self.res_frame, text="Est. Fuel Cost: --", font=("Roboto", 16))
        self.cost_display.pack(pady=5)

        self.history_box = ctk.CTkTextbox(self.main_frame, height=180)
        self.history_box.pack(fill="x", pady=5)

    def apply_custom_icon(self):
        """Forces the custom icon onto the window, handling PyInstaller paths."""
        icon_name = "icon.ico"
        
        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, icon_name)
        else:
            icon_path = os.path.join(os.path.abspath("."), icon_name)

        if os.path.exists(icon_path):
            try:
                self.after(200, lambda: self.iconbitmap(icon_path))
                self.after(500, lambda: self.iconbitmap(icon_path))
                self.after(1000, lambda: self.iconbitmap(icon_path))
            except:
                pass

    def update_limit_label(self, value):
        self.limit_label.configure(text=f"Speed Limit: {int(value)} km/h")

    def update_cons_label(self, value):
        self.cons_label.configure(text=f"Fuel Economy: {int(value)} km/L")

    def calculate_all(self):
        try:
            d = float(self.dist_entry.get())
            t1 = datetime.strptime(self.entry_time.get(), "%H:%M")
            t2 = datetime.strptime(self.exit_time.get(), "%H:%M")
            duration = (t2 - t1).total_seconds() / 3600
            if duration <= 0:
                messagebox.showerror("Time Error", "Exit time must be later than entry time.")
                return

            avg_speed = round(d / duration, 2)
            limit = self.limit_val.get()
            color = "#ff4d4d" if avg_speed > limit else "#4ade80"
            status = "⚠️ SPEEDING" if avg_speed > limit else "✅ SAFE"

            self.speed_display.configure(text=f"Avg Speed: {avg_speed} km/h ({status})", text_color=color)

            fuel_text = "N/A"
            if self.fuel_price.get():
                total_cost = (d / self.cons_val.get()) * float(self.fuel_price.get())
                fuel_text = f"Rs. {round(total_cost, 2)}"
                self.cost_display.configure(text=f"Est. Fuel Cost: {fuel_text}")

            self.history_box.insert("0.0", f"[{datetime.now().strftime('%H:%M:%S')}] {self.vehicle_type.get()} | {d}km | {avg_speed}km/h | {status}\n")
        except:
            messagebox.showerror("Input Error", "Check your inputs (Distance: numbers, Time: HH:MM).")

    def export_data(self):
        content = self.history_box.get("1.0", "end-1c").strip()
        if not content:
            messagebox.showwarning("Export Failed", "History is empty.")
            return
        try:
            filename = f"trip_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"EXPRESSWAY PRO V1.0 LOG\n{content}")
            messagebox.showinfo("Export Successful", f"Log saved as: {filename}")
        except Exception as e:
            messagebox.showerror("File Error", str(e))

if __name__ == "__main__":
    app = ExpresswayPro_v1()
    app.mainloop()