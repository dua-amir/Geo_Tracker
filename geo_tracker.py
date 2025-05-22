import requests
import folium
import tkinter as tk
from tkinter import messagebox, simpledialog
import webbrowser

def get_geolocation(ip=None):
    try:
        url = f"https://ipinfo.io/{ip}/json" if ip else "https://ipinfo.io/json"
        response = requests.get(url)
        data = response.json()

        if 'bogon' in data:
            raise Exception("Invalid or private IP address.")

        loc = data['loc'].split(',')
        return {
            'ip': data.get('ip', 'N/A'),
            'city': data.get('city', 'Unknown'),
            'region': data.get('region', 'Unknown'),
            'country': data.get('country', 'Unknown'),
            'latitude': float(loc[0]),
            'longitude': float(loc[1]),
            'org': data.get('org', 'Unknown'),
            'timezone': data.get('timezone', 'Unknown')
        }
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get geolocation:\n{e}")
        return None

def show_on_map(geo):
    map_ = folium.Map(location=[geo['latitude'], geo['longitude']], zoom_start=12)
    folium.Marker(
        [geo['latitude'], geo['longitude']],
        popup=f"{geo['city']}, {geo['region']}, {geo['country']}\nIP: {geo['ip']}",
        tooltip="📍 IP Location"
    ).add_to(map_)
    map_file = "geolocation_map.html"
    map_.save(map_file)
    webbrowser.open(map_file)

def fetch_my_location():
    geo = get_geolocation()
    if geo:
        display_info(geo)
        show_on_map(geo)

def fetch_other_ip_location():
    ip = simpledialog.askstring("Input IP", "Enter an IP address:")
    if ip:
        geo = get_geolocation(ip.strip())
        if geo:
            display_info(geo)
            show_on_map(geo)

def display_info(geo):
    info = (
        f"🌍 IP Address: {geo['ip']}\n"
        f"📍 Location: {geo['city']}, {geo['region']}, {geo['country']}\n"
        f"🌐 ISP: {geo['org']}\n"
        f"🕒 Timezone: {geo['timezone']}\n"
        f"📌 Coordinates: {geo['latitude']}, {geo['longitude']}"
    )
    result_label.config(text=info)

# GUI setup
app = tk.Tk()
app.title("Geolocation Tracker")
app.geometry("520x450")
app.config(bg="#001f3d")  # Royal Blue background

# Fonts
title_font = ("Helvetica", 22, "bold")
button_font = ("Arial", 12, "bold")
info_font = ("Arial", 12)

# Frame for central content
frame = tk.Frame(app, bg="#003b5c", bd=2, relief="flat")
frame.place(relx=0.5, rely=0.5, anchor="center", width=480, height=380)

tk.Label(frame, text="🌐 Geolocation Tracker", font=title_font, fg="gold", bg="#003b5c").pack(pady=20)

tk.Button(frame, text="📍 Track My Location", command=fetch_my_location, font=button_font,
          bg="gold", fg="#003b5c", activebackground="#b37a00", width=25, relief="flat", bd=2).pack(pady=8)

tk.Button(frame, text="🔎 Track IP Location", command=fetch_other_ip_location, font=button_font,
          bg="gold", fg="#003b5c", activebackground="#b37a00", width=25, relief="flat", bd=2).pack(pady=8)

result_label = tk.Label(frame, text="", font=info_font, bg="#003b5c", fg="white",
                        wraplength=440, justify="left")
result_label.pack(pady=20)

tk.Label(app, text="© Dua Amir, Python Intern, Rhombix Technologies",
         font=("Arial", 9), fg="#f7d600", bg="#001f3d").pack(side="bottom", pady=6)

app.mainloop()
