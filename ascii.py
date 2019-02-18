
"""
READ ME:

this program turns images into a text representation, on start it will ask you to choose an image file from your file explorer

it is highly recomended that the text editor used to view the final product uses a square(for the most part)
and monospaced font, font size between 1-6 is recomended depending on the detail level

download for an good font option -- http://strlen.com/square/

To change from the simple_ascii mode to full_ascii(beta), scroll to the bottom change start_conversion(0,x) --->(1,x)

To change the level of detail scroll to the bottom and change the second argument or use the prompt in the console, lower is more detailed

"""


import numpy as np
from PIL import Image
import webbrowser
import tkinter as tk
from tkinter import filedialog
import os

pix_ar = {}  # all monochrome pixel data
final_pix = []  # all the average chunked monochrome pixel data
final_ascii = []  # the ascii representation of final_pix(based on the set_pix_to_ascii rules)
chunk = []  # one distinct block of pixel data, sent to avg to find the avg value of the chunk(0-255)


#  breaks the pixel data down into 'chunks' to be averaged
# @param detail, determines the chunk size, larger = less detail, suggested range 1-25
def set_chunks(d):
    hb = 0
    while (d*hb)+d < height:
        wb = 0
        while (wb*d)+d < width:
            for i in range(d*hb,  (d*hb)+d):
                for j in range(wb*d, (wb*d)+d):
                    chunk.append(img.getpixel((j, i)))
            avg_pixel(chunk)
            chunk.clear()
            wb += 1
        final_pix.append("\n")
        hb += 1


#  averages the pixels in each chunk and adds them to the final_pix
#  @param ar is an array of pixel data parsed by the set_chunk method
def avg_pixel(ar):
    total = 0
    number = 0
    for n in ar:
            total += n
            number += 1
    avg = total//number
    final_pix.append(avg)


# takes the final pix and sets each mono value to an ascii char, currently only 4 possible chars
def set_pix_to_ascii():
    for p in range(len(final_pix)):
        if final_pix[p] == "\n":
            final_ascii.append("\n")
        else:
            if final_pix[p] > 225:
                final_ascii.append(" ")
            elif final_pix[p] > 160:
                final_ascii.append("-")
            elif final_pix[p] > 100:
                final_ascii.append("+")
            else:
                final_ascii.append("#")


# same as the set_pix_to_ascii method but using many more chars for a fuller spectrum
# TODO make this method, starting with weighting the values of the ascii chars by there black to white pixel ratio
def set_pix_to_ascii_full():
    ascii_order = ('M', '#', 'B', '@', 'D', 'A', 'E', 'G', 'F', '4', 'S', '$', '5', 'J', '3', 'T', 'n', 'a', 'r', 'I'
                   , '?', '<', '|', '~', '+', '=', '_', '-', ' ')
    for p in range(len(final_pix)):
        if final_pix[p] == "\n":
            final_ascii.append("\n")
        else:
            pv = (255 - final_pix[p])//10
            final_ascii.append(ascii_order[(len(ascii_order)-pv)-1])


# sends the ascii from final_ascii to a file
def draw_ascii():
    f = open("test.txt", "w+")
    for i in range(len(final_ascii)):
        f.write(final_ascii[i])


# main routine for the whole program
# @param mode, either 0 or 1, simple_ascii or full_ascii
# @param detail, how detailed the drawing is recommened scale 1-20, 1 most detail, 20 least
def start_conversion(mode, detail):
    global img
    img = img.convert("L")  # convert the image to gray scale
    pix_ar = np.asarray(img)
    set_chunks(detail)
    if mode == 0:
        set_pix_to_ascii()
    else:
        set_pix_to_ascii_full()
    print("Width: ",width,"  Height: ", height, "  Total ASCII chars: ",len(final_ascii),"  CR: ",width*height//len(final_ascii))
    #  os.system("TASKKILL /F /IM notepad.exe") -- beta
    draw_ascii()
    webbrowser.open("test.txt")


# open the file explorer to choose a image
def get_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    p = Image.open(file_path)  # the image to be converted to ascii
    return p


img = get_file()
(width, height) = img.size

start_conversion(0,int(input("Enter the desired detail, lower is more detail: ")))

"""

"""
