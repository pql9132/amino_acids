import xml.etree.ElementTree as ET
import tkinter as tk
from PIL import Image, ImageTk
from random import randint, choice

amino_acids = {}
img_directory = "amino_acid_img/"
img_extension = ".png"
current_amino_acid = ""
current_image = None

#Load amino acid data from XML
for item in ET.parse('aminoacids.xml').iter("amino_acid"):
    name = item.find("name").text
    amino_acids[name] = [item.find("symbol").text]
    amino_acids[name].append(Image.open(img_directory + name + img_extension))

#Define functions
def set_amino_acid():
    global current_amino_acid
    current_amino_acid = choice(list(amino_acids.keys()))

def display_amino_acid(display_canvas, amino_acid):
    global current_image
    angle = choice([0,90,-90, 180])
    current_image = ImageTk.PhotoImage(amino_acids[amino_acid][1].rotate(angle))
    display_canvas.delete("all")
    display_canvas.create_image(450/2,450/2,image=current_image)

def display_symbol(display_canvas, amino_acid):
    display_canvas.delete("all")
    display_canvas.create_text(450/2, 450/2, text=amino_acids[amino_acid][0], font=("Noto Sans", 100))

def reset(display_canvas):
    global current_amino_acid
    set_amino_acid()
    if randint(0,6) == 5:
        display_symbol(display_canvas, current_amino_acid)
    else:
        display_amino_acid(display_canvas, current_amino_acid)

def submit_button(entry_box, submission, display_canvas):
    if submission.get() == current_amino_acid:
        entry_box.configure(fg="#000000")
        entry_box.delete(0,tk.END)
        reset(display_canvas)
    else:
        entry_box.configure(fg="#ff0000")

#Create and run window
window = tk.Tk()
window.title("Amino Acids")
window.geometry("450x550")
window.resizable(width=False,height=False)

#Create window canvases
display_canvas = tk.Canvas(window, width=450, height=450)
input_canvas   = tk.Canvas(window, width=450, height=100)
display_canvas.pack()
input_canvas.pack()

#Define display canvas items

#Define input canvas items
submission = tk.StringVar()

entry_box = tk.Entry(input_canvas, width=20, borderwidth=0, fg="#000000", textvar=submission)
entry_button = tk.Button(input_canvas, width=30, height=2, text="Submit")
entry_button.configure(command=lambda:submit_button(entry_box, submission, display_canvas))

entry_box.grid(row=0,column=0, pady=10)
entry_button.grid(row=1,column=0)

#Initialize the game
reset(display_canvas)

#Window loop
window.mainloop()