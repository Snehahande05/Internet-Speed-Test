import speedtest
import tkinter as tk
from tkinter import ttk, Canvas, PhotoImage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
from io import BytesIO

# Global variable to store speed test results
speed_history = {"download": [], "upload": [], "ping": []}

# Function to perform the speed test
def run_speed_test():
    global speed_history
    status_label.config(text="Testing... Please wait.", foreground="yellow")
    root.update()

    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        ping = st.results.ping
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps

        speed_history["ping"].append(ping)
        speed_history["download"].append(download_speed)
        speed_history["upload"].append(upload_speed)

        download_label.config(text=f"Download Speed: {download_speed:.2f} Mbps")
        upload_label.config(text=f"Upload Speed: {upload_speed:.2f} Mbps")
        ping_label.config(text=f"Ping: {ping:.2f} ms")

        status_label.config(text="✅ Test Completed!", foreground="lightgreen")

        # Update the graph
        update_graph()

    except Exception as e:
        status_label.config(text="⚠️ Error: Check Connection", foreground="red")

# Function to update the speed trend graph
def update_graph():
    plt.clf()
    plt.plot(speed_history["download"], marker="o", linestyle="-", label="Download Speed (Mbps)", color="cyan")
    plt.plot(speed_history["upload"], marker="o", linestyle="-", label="Upload Speed (Mbps)", color="green")
    plt.xlabel("Test Attempts")
    plt.ylabel("Speed (Mbps)")
    plt.title("Internet Speed Trend")
    plt.legend()
    plt.grid()
    canvas.draw()

# Function to fetch and display ISP logo
def fetch_isp_logo():
    try:
        ip_info = requests.get("https://ipinfo.io/json").json()
        isp_name = ip_info.get("org", "Unknown ISP")
        isp_label.config(text=f"ISP: {isp_name}")

        # Try to get ISP logo from Clearbit API
        domain = isp_name.split()[-1].lower() + ".com"
        logo_url = f"https://logo.clearbit.com/{domain}"
        response = requests.get(logo_url)

        if response.status_code == 200:
            img_data = BytesIO(response.content)
            img = PhotoImage(data=img_data.read())
            isp_logo_label.config(image=img)
            isp_logo_label.image = img
    except:
        isp_label.config(text="ISP: Unknown")

# Function to switch theme
def switch_theme():
    global current_theme
    if current_theme == "tech_neon":
        root.configure(bg="lightblue")
        frame.configure(bg="white")
        status_label.configure(bg="white", foreground="black")
        download_label.configure(bg="white", foreground="black")
        upload_label.configure(bg="white", foreground="black")
        ping_label.configure(bg="white", foreground="black")
        isp_label.configure(bg="white", foreground="black")
        theme_button.config(text="Switch to Tech Neon")
        current_theme = "soft_blue"
    else:
        root.configure(bg="black")
        frame.configure(bg="black")
        status_label.configure(bg="black", foreground="lightgreen")
        download_label.configure(bg="black", foreground="cyan")
        upload_label.configure(bg="black", foreground="cyan")
        ping_label.configure(bg="black", foreground="cyan")
        isp_label.configure(bg="black", foreground="cyan")
        theme_button.config(text="Switch to Soft Blue")
        current_theme = "tech_neon"

# GUI Setup
root = tk.Tk()
root.title("Internet Speed Test")
root.geometry("600x500")

# Default theme
current_theme = "tech_neon"
root.configure(bg="black")

frame = tk.Frame(root, bg="black")
frame.pack(pady=20)

status_label = tk.Label(frame, text="Press 'Start Test' to begin", font=("Arial", 14), bg="black", fg="lightgreen")
status_label.pack(pady=10)

download_label = tk.Label(frame, text="Download Speed: -- Mbps", font=("Arial", 12), bg="black", fg="cyan")
download_label.pack()

upload_label = tk.Label(frame, text="Upload Speed: -- Mbps", font=("Arial", 12), bg="black", fg="cyan")
upload_label.pack()

ping_label = tk.Label(frame, text="Ping: -- ms", font=("Arial", 12), bg="black", fg="cyan")
ping_label.pack()

isp_label = tk.Label(frame, text="Fetching ISP...", font=("Arial", 12), bg="black", fg="cyan")
isp_label.pack()

isp_logo_label = tk.Label(frame, bg="black")
isp_logo_label.pack()

# Start Test Button
start_button = ttk.Button(root, text="Start Test", command=run_speed_test)
start_button.pack(pady=10)

# Theme Switch Button
theme_button = ttk.Button(root, text="Switch to Soft Blue", command=switch_theme)
theme_button.pack(pady=10)

# Matplotlib Graph
fig, ax = plt.subplots(figsize=(5, 3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Fetch ISP logo on start
fetch_isp_logo()

# Run the GUI loop
root.mainloop()
