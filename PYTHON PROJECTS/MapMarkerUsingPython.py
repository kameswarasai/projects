import tkinter as tk
from datetime import datetime
import folium
import os
import webview

FILENAME = "data.txt"
MAP_FILE = "map.html"



def save_text(event=None):
    text = entry.get()
    if text.strip():
        timestamp = datetime.now().strftime("%H:%M %d/%m/%y")
        line = f"{timestamp} : {text}"
        with open(FILENAME, "a") as f:
            f.write(line + "\n")
        entry.delete(0, tk.END)
        load_text()

def load_text():
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)
    try:
        with open(FILENAME, "r") as f:
            content = f.read()
            text_area.insert(tk.END, content)
    except FileNotFoundError:
        pass
    text_area.config(state=tk.DISABLED)

def extract_coordinates_from_file():
    coords = []
    try:
        with open(FILENAME, "r") as f:
            for line in f:
                if ":" in line and "," in line:
                    try:
                        timestamp, value = line.strip().split(" : ")
                        lat, lon = map(float, value.split(","))
                        coords.append((lat, lon, timestamp))
                    except:
                        continue
    except FileNotFoundError:
        pass
    return coords

def generate_map():
    data = extract_coordinates_from_file()
    if data:
        last_lat, last_lon, _ = data[-1]
        fmap = folium.Map(location=[last_lat, last_lon], zoom_start=6)
        for lat, lon, ts in data:
            folium.Marker([lat, lon], popup=f"Time: {ts}").add_to(fmap)
    else:
        fmap = folium.Map(location=[20.5937, 78.9629], zoom_start=4)
        folium.Marker([20.5937, 78.9629], popup="No data").add_to(fmap)
    fmap.save(MAP_FILE)

def show_map():
    generate_map()
    map_path = os.path.abspath(MAP_FILE)
    webview.create_window("Map", f"file://{map_path}", width=800, height=600)
    webview.start()

# === GUI Setup ===
root = tk.Tk()
root.title("Data Logger with Map")
root.geometry("500x450")

try:
    root.iconbitmap("icon.ico")  # Replace with your actual icon file name
except Exception as e:
    print("Icon not loaded:", e)

# Entry and Buttons
entry = tk.Entry(root, width=67)
entry.grid(row=0, column=0, padx=(5, 0), pady=5, sticky='w')

save_button = tk.Button(root, text="Save", command=save_text)
save_button.grid(row=0, column=1, padx=(5, 0))

map_button = tk.Button(root, text="Show Map", command=show_map)
map_button.grid(row=1, column=1, padx=(5, 5), sticky='n')

entry.bind("<Return>", save_text)

# Text Area
text_area = tk.Text(root, width=50, height=25, state=tk.DISABLED)
text_area.grid(row=1, column=0, columnspan=1, padx=(5, 5), pady=(0, 5))

# Initial Load
load_text()

root.mainloop()
