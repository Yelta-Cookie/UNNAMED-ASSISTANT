"""
For y'all searching the Ccode, I've got a FAT BONUS!
My RETROPIC MODULE!
My brother told me about Visco girls and that they are named after the image
editing mobile app Visco, and then he showed me the app, and I told him my code
is shit but even I can do better than this. So I did.
"""

import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageTk
import random
import time

pic = Image.open("bgpic.png")
scales = []

# Noise Space (%), Noise R,G,B, Sat, Light, Cont, Shift R,G,B, Colorfilter R,G,B, Special Filter, Horizontal Noise
mods = [50,           20,20,20,  10,    20,  -10,      4,0,2,             0,0,10,  "None",         30]

def render():
    global pic, img, panel,savebu

    for i in range(14):
        mods[i] = scales[i].get()
    print(mods[13])

    img = Image.open("bgpic.png")
    px = img.load() ; pxt = px

    vertnice = []
    for i in range(img.size[1]):
        vertnice.append(random.randrange(0, mods[14]) - int(mods[14] / 2))
    
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            Rot, Grün, Blau = img.getpixel((i, j))[:3]
            # shift
            a = 0
            if i > img.size[0] // 2:
                a = img.size[0]
            if mods[7] != 0:    
                Rot = img.getpixel((i+mods[7]-a,j))[0]
            if mods[8] != 0:  
                Grün = img.getpixel((i+mods[8]-a,j))[1]
            if mods[9] != 0:  
                Blau = img.getpixel((i+mods[9]-a,j))[2]
            # noise
            if random.randrange(1,101) < mods[0]:
                a = random.randrange(1,101)/100
                Grün += int(a*mods[2]) ; Rot += int(a*mods[1]) ; Blau += int(a*mods[3])
            # saturation
            if Rot > 122:
                Rot += mods[4]
            else:
                Rot -= mods[4]
            if Grün > 122:
                Grün += mods[4]
            else:
                Grün -= mods[4]
            if Blau > 122:
                Blau += mods[4]
            else:
                Blau -= mods[4]
            # lighting
            Grün += mods[5] ; Rot += mods[5] ; Blau += mods[5]
            # contrast
            if Grün + Blau + Rot > 366:
                Grün += mods[6] ; Rot += mods[6] ; Blau += mods[6]
            else:
                Grün -= mods[6] ; Rot -= mods[6] ; Blau -= mods[6]
            # colorfilters
            Rot += mods[10]
            Grün += mods[11]
            Blau += mods[12]
            # Special filters
            if mods[13] == "Gameboy":
                if Rot+Blau+Grün < 256:
                    Rot = 16 ; Grün = 58 ; Blau = 0
                elif Rot+Blau+Grün < 384:
                    Rot = 61 ; Grün = 114 ; Blau = 60
                elif Rot+Blau+Grün < 612:
                    Rot = 157 ; Grün = 183 ; Blau = 24
                else:
                    Rot = 170 ; Grün = 197 ; Blau = 24
            if mods[13] == "1-Bit":
                if Rot+Blau+Grün < 320:
                    Rot = 0 ; Grün = 0 ; Blau = 0
                elif Rot+Blau+Grün < 384:
                    if i//2==i/2 and j//2==j/2:
                        Rot = 255 ; Grün = 255 ; Blau = 255
                    else:
                        Rot = 0 ; Grün = 0 ; Blau = 0
                elif Rot+Blau+Grün < 548:
                    if i//2==i/2 and j//2==j/2:
                        Rot = 0 ; Grün = 0 ; Blau = 0
                    else:
                        Rot = 255 ; Grün = 255 ; Blau = 255
                else:
                    Rot = 255 ; Grün = 255 ; Blau = 255
            # Horizontal Noise
            Rot += vertnice[j] ; Blau += vertnice[j] ; Grün += vertnice[j]

            px[i, j] = Rot, Grün, Blau
    savebu = img
    img = ImageTk.PhotoImage(img.resize((480,360)))
    panel.destroy()
    panel = tk.Label(window, image = img)
    panel.pack(anchor=tk.N)

def save():
    global savebu
    savebu.save('./Downloads/retro'+str(int(time.time()))+".png")
    (savebu.resize((480,360))).save('./Downloads/retrox'+str(int(time.time()))+".png")

def generatetab():
    global scales, panel,fi
    fi = "None"
    ns = Scale(window, label="Noise Space in %", orient=HORIZONTAL, length=400, from_=0, to=100, width=8)
    ns.set(mods[0])
    ns.pack(anchor=tk.W)
    nr = Scale(window, label="Noise R", orient=HORIZONTAL, length=400, from_=0, to=200, width=8)
    nr.set(mods[1])
    nr.pack(anchor=tk.W)
    ng = Scale(window, label="Noise G", orient=HORIZONTAL, length=400, from_=0, to=200, width=8)
    ng.set(mods[2])
    ng.pack(anchor=tk.W)
    nb = Scale(window, label="Noise B", orient=HORIZONTAL, length=400, from_=0, to=200, width=8)
    nb.set(mods[3])
    nb.pack(anchor=tk.W)
    sa = Scale(window, label="Saturation", orient=HORIZONTAL, length=400, from_=0, to=256, width=8)
    sa.set(mods[4])
    sa.pack(anchor=tk.W)
    li = Scale(window, label="Lighting", orient=HORIZONTAL, length=400, from_=-200, to=200, width=8)
    li.set(mods[5])
    li.pack(anchor=tk.W)
    co = Scale(window, label="Contrast", orient=HORIZONTAL, length=400, from_=-256, to=256, width=8)
    co.set(mods[6])
    co.pack(anchor=tk.W)
    sr = Scale(window, label="R Shift", orient=HORIZONTAL, length=400, from_=0, to=pic.size[0]//2-1, width=8)
    sr.set(mods[7])
    sr.pack(anchor=tk.W)
    sg = Scale(window, label="G Shift", orient=HORIZONTAL, length=400, from_=0, to=pic.size[0]//2-1, width=8)
    sg.set(mods[8])
    sg.pack(anchor=tk.W)
    sb = Scale(window, label="B Shift", orient=HORIZONTAL, length=400, from_=0, to=pic.size[0]//2-1, width=8)
    sb.set(mods[9])
    sb.pack(anchor=tk.W)
    fr = Scale(window, label="Filter R", orient=HORIZONTAL, length=400, from_=-255, to=255, width=8)
    fr.set(mods[10])
    fr.pack(anchor=tk.W)
    fg = Scale(window, label="Filter G", orient=HORIZONTAL, length=400, from_=-255, to=255, width=8)
    fg.set(mods[11])
    fg.pack(anchor=tk.W)
    fb = Scale(window, label="Filter B", orient=HORIZONTAL, length=400, from_=-255, to=255, width=8)
    fb.set(mods[12])
    fb.pack(anchor=tk.W)
    fx = ttk.Combobox(window, values=("None","Gameboy","1-Bit"), textvariable=fi)
    fx.current(0)
    fx.pack(anchor=tk.W)
    vs = Scale(window, label="Horizontal Noise", orient=HORIZONTAL, length=400, from_=0, to=500, width=8)
    vs.set(mods[14])
    vs.pack(anchor=tk.W)
    print(fx.get())
    for i in [ns,nr,ng,nb,sa,li,co,sr,sg,sb,fr,fg,fb,fx,vs]:
        scales.append(i)

    img = ImageTk.PhotoImage(pic.resize((480,360)))
    panel = tk.Label(window, image = img)
    panel.pack(anchor=tk.N)

window = tk.Tk() ; window.title("project_fortress'flag")

Label(window, text="Tip: This is way faster if you downgrade your image to a retro resolution first. Remember that e.g. 360p is not twice, but four times as fast as 720p.").pack()

Button(window, text="Update preview", command=render).pack(anchor=tk.W)
Button(window, text="Save image to project_unnamed/Downloads", command=save).pack(anchor=tk.W)

generatetab()
render()

window.mainloop()






