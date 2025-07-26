'''
Author: Andebb (Github)
Version: 1.1
Description:
Downloads necessary modules for image handling automatically,
traverses the content of a folder and converts all found heic-images
to .JPEG images, and saves them in a pre-selected file.
Requirements: Python 3.11
'''


import os
import importlib.util
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

#First checks to download pillow_heif and pillow

if not importlib.util.find_spec("PIL"):
    print("Installing PIL")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])

if not importlib.util.find_spec('pillow_heif'):
    print("Installing pillow_heif")
    subprocess.check_call([sys.executable,"-m", 'pip', 'install', 'pillow-heif'])
    
import pillow_heif
from PIL import Image

# Global variables to store selected file path
#File that has the .HEIC images:
filename = ''
#File that gets the .jpg images:
new_filename = ''
time_label = ''
i = False
remaining_images = ''

pillow_heif.register_heif_opener()

def calculate_time(elapsed_time, file_length,files_passed):
    total_time_left = int(elapsed_time*(file_length-files_passed)*100)/100
    hours = int(total_time_left/(60*60))
    minutes = int((total_time_left - hours*60*60)/60)
    seconds = int(total_time_left-hours*60*60-minutes*60)
    return str(hours) + "hours, " + str(minutes) + "minutes, " + str(seconds) + "seconds."

def convert_image(file):
    heic_path = file
    file_name_base = os.path.splitext(os.path.basename(file))[0]
    jpg_path = os.path.join(new_filename,file_name_base + '.jpg')

    try:
        image = Image.open(heic_path)
        image.save(jpg_path,'JPEG',quality = 95, subsampling = 0)
        status = f"Converted: " + file_name_base.lower()
    except Exception as e:
        status = f"Failed to convert: " + file_name_base.lower() + " with error: " +str(e)
    
    file_size = os.path.getsize(heic_path)

    return (status, file_size)

def determine_size_text(size):

    if size >= 1000000000:
        return str(int(size/1000000000*100)/100) + "GB"
    elif size >= 1000000:
        return str(int(size/1000000*100)/100) + "MB"
    elif size >= 1000:
        return str(int((size/1000*100))/100) + "KB"
    else:
        return str(size) + "B"

def change_images():
    global time_label
    global remaining_images
    total_size = 0
    file_list = []
    converted = 0
    for rootpart, dirs, files in os.walk(filename, True):
        for file_name in files:
            if file_name.lower()[-5:] == '.heic':
                f = os.path.join(rootpart, file_name)
                file_list.append(f)
                total_size += os.path.getsize(f)
    progress['maximum'] = total_size
    total = 0
    total_elapsed = 0
    before_time = time.time()
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(convert_image,file): file for file in file_list}
        for future in as_completed(futures):
            status, file_size = future.result()
            total += file_size
            if status[0] == 'C':
                converted += 1
            total_elapsed += 1
            label.config(text=status)

            progress['value'] = total
            elapsed_time = time.time()-before_time
            if total>0:
                total_left = calculate_time(elapsed_time/total,total_size,total)
            time_label.config(text= f"Remaining time: " + total_left)
            remaining_images.config(text=f"Remaining images: " + str(len(file_list)-total_elapsed) + " - [" + determine_size_text(total_size - total) +"]" )
            root.update()    
        label.config(text=f'Success! Converted: ' + str(converted) + " images out of: " + str(len(file_list)))
    root.after(2000,root.destroy)


def browse_file():
    global filename
    global new_filename
    global i
    file_path = filedialog.askdirectory()
    if file_path:
        if not i:
            filename = file_path
            label.config(text=f"Selected .HEIC containing folder: {file_path}")
        else:
            new_filename = file_path
            label.config(text=f"Selected .jpg-getting folder: {new_filename}")


def on_next():
    global time_label
    global remaining_images
    global i
    if (not i and filename) or (i and new_filename):
        if i:
            next_button.destroy()
            browse_button.destroy()
            time_label = tk.Label(root,text="Remaining time: ")
            time_label.pack(pady=2)
            remaining_images = tk.Label(root, text="Remaining images: N/A")
            remaining_images.pack(pady=5)

            change_images()
        else:
            i = not i
            label.config(text=f"Choose folder that gets .jpg images.")

# Create the main window
root = tk.Tk()
root.title("Folder Selector")
root.geometry("500x200")

# Create and place widgets
label = tk.Label(root, text="No .heic-containing folder selected.")
label.pack(pady=10)

progress = ttk.Progressbar(root, orient='horizontal',length=300,mode="determinate")
progress.pack(pady=5)

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=2)

next_button = tk.Button(root, text="Next", command=on_next)
next_button.pack(pady=2)

# Start the GUI loop
root.mainloop()

