import tkinter as tk
import webbrowser
from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
from carread import *
from dict import *

# Define window attributes
windowH = 900       # window height
windowW = 1000      # window width
fontW = 'swos'      # Right now assume font installed in system so just name it
version = 'version 0.3'
title = 'SWOS Career Team Explorer'
url = 'https://github.com/EMPI-PL/SWOS_career_team_explorer'
colortone = '#000040'
colortone_info = '#a90000'
color_gk = "#248900"
color_pl = '#2075ee'
color_16 = '#143f7e'
color_re = '#ae131a'

class openfiledialog():
    def __init__(self, initialdir, title, filetype):
        self.initialdir = initialdir
        self.title = title
        self.filetype = filetype
    
    def show(self):
        x = filedialog.askopenfilename(initialdir=self.initialdir, title=self.title, filetypes=self.filetype)
        return x

def opencar():    
    choosecarfile = openfiledialog('/home/','Select SWOS career file',[('SWOS Career file', '*.CAR')])
    pickedfile = choosecarfile.show()
    carfile_output = readcarfile(pickedfile)  # Call func to read squad details
    updateview(carfile_output)   # Call func to view data

def updateview(carfile_output):
    squad = carfile_output[0]
    carfileteaminfo = carfile_output[1]
    squadcanvas = Canvas(mf_leftframe,width=680,borderwidth=0, highlightthickness=0,bg=colortone)
    squadcanvas.place(x=10,y=10)
    counter = 1    
    while counter < len(squad):
        pic_load = Image.open(squad[counter][0])    # Read a "head picture"
        pic_set = ImageTk.PhotoImage(pic_load)
        star_load = Image.open(d_stars[squad[counter][12]])
        star_set = ImageTk.PhotoImage(star_load)
        head_label = Label(squadcanvas,image=pic_set,bg=color_pl,bd=0)
        head_label.image = pic_set
        star_label = Label(squadcanvas,image=star_set,bg=colortone,bd=0)
        star_label.image = star_set
        num_label = Label(squadcanvas,bg=colortone,width=3,height=1,bd=0,highlightthickness=0, font=('swos',16),text=squad[counter][1],fg='white')
        pos_label = Label(squadcanvas,bg=colortone,width=3,height=1,bd=0,highlightthickness=0, font=('swos',16),text=squad[counter][3],fg='white')
        nat_label = Label(squadcanvas,bg=colortone,width=3,height=1,bd=0,highlightthickness=0, font=('swos',16),text=squad[counter][4],fg='white',padx=10)
        if counter<12:
            match squad[counter][3]:
                case 'G':
                    name_label = Label(squadcanvas,bg=color_gk,width=20,height=1,bd=0,highlightthickness=0, font=('swos',16),anchor='w',text=squad[counter][2],fg='white', padx=20)
                case _:
                    name_label = Label(squadcanvas,bg=color_pl,width=20,height=1,bd=0,highlightthickness=0, font=('swos',16),anchor='w',text=squad[counter][2],fg='white', padx=20)
        elif counter <17:
            match squad[counter][3]:
                case 'G':
                    name_label = Label(squadcanvas,bg=color_gk,width=20,height=1,bd=0,highlightthickness=0, font=('swos',16),anchor='w',text=squad[counter][2],fg='white', padx=20)
                case _:
                    name_label = Label(squadcanvas,bg=color_16,width=20,height=1,bd=0,highlightthickness=0, font=('swos',16),anchor='w',text=squad[counter][2],fg='white', padx=20)
        else:
            match squad[counter][3]:
                case 'G':
                    name_label = Label(squadcanvas,bg=color_gk,width=20,height=1,bd=0,highlightthickness=0, font=('swos',16),anchor='w',text=squad[counter][2],fg='white', padx=20)
                case _:
                    name_label = Label(squadcanvas,bg=color_re,width=20,height=1,bd=0,highlightthickness=0, font=('swos',16),anchor='w',text=squad[counter][2],fg='white', padx=20)
        head_label.grid(row=counter,column=0,sticky='n',pady=3)
        num_label.grid(row=counter,column=1,sticky='n',pady=3)
        name_label.grid(row=counter,column=2,sticky='n',pady=3)
        pos_label.grid(row=counter,column=3,sticky='n',pady=3)
        nat_label.grid(row=counter,column=4,sticky='n',pady=3)
        star_label.grid(row=counter,column=5,sticky='n',pady=3)
        
        counter += 1 
    
    # Show team info on the right side
    teamcanvas = Canvas(mf_rightframe,width=280,borderwidth=0, highlightthickness=0,bg=colortone)
    teamcanvas.place(x=10,y=20)
    
    teamnamebox_1 = Label(teamcanvas,bg=colortone,width=15,height=1,bd=0,highlightthickness=0, font=('swos',14),anchor='w',text='TEAM NAME:',fg='yellow')
    teamnamebox_1.grid(row=0,column=0,columnspan=2)
    teamnamebox_2 = Label(teamcanvas,bg=colortone,width=20,height=1,bd=0,highlightthickness=0, font=('swos',10),anchor='e',text=carfileteaminfo.clubname,fg='white')
    teamnamebox_2.grid(row=1,column=1,columnspan=2,pady=5)
    
    box_br1 = Label(teamcanvas,bg=colortone,width=10,height=1,bd=0,highlightthickness=0, font=('swos',12),text=' ',fg='white')
    box_br1.grid(row=2,column=0,columnspan=2)

    teamnamebox_3 = Label(teamcanvas,bg=colortone,width=15,height=1,bd=0,highlightthickness=0, font=('swos',14),anchor='w',text='MANAGER NAME:',fg='yellow')
    teamnamebox_3.grid(row=3,column=0,columnspan=2)
    teamnamebox_4 = Label(teamcanvas,bg=colortone,width=20,height=1,bd=0,highlightthickness=0, font=('swos',10),anchor='e',text=carfileteaminfo.managername,fg='white')
    teamnamebox_4.grid(row=4,column=1,columnspan=2,pady=5)
    
    box_br2 = Label(teamcanvas,bg=colortone,width=10,height=1,bd=0,highlightthickness=0, font=('swos',12),text=' ',fg='white')
    box_br2.grid(row=5,column=0,columnspan=2)

    teamnamebox_5 = Label(teamcanvas,bg=colortone,width=15,height=1,bd=0,highlightthickness=0, font=('swos',14),anchor='w',text='BANK BALLANCE:',fg='yellow')
    teamnamebox_5.grid(row=6,column=0,columnspan=2)
    teamnamebox_6 = Label(teamcanvas,bg=colortone,width=20,height=1,bd=0,highlightthickness=0, font=('swos',10),anchor='e',text="{:0,.2f}".format(float(carfileteaminfo.money)),fg='white')
    teamnamebox_6.grid(row=7,column=1,columnspan=2,pady=5)    
  
def close():
    quit()

def infobox():
    rinf = tk.Tk()
    rinf.title("Info")
    rinf.resizable(0,0) # Make the frame not resizable
    rinf.geometry('400x200')
    rinfframe = Frame(rinf, width=400, height=200, bg=colortone_info, highlightthickness=0, bd=0)
    rinfframe.grid(row=0,column=0)
    
    infocanvas = Canvas(rinfframe,width=400,borderwidth=0, highlightthickness=0,bg=colortone_info)
    infocanvas.place(x=0,y=0)

    x_1 = Label(infocanvas,bg=colortone_info,width=28,height=1,bd=0,highlightthickness=0, font=('swos',13),anchor='c',text=title,fg='yellow')
    x_2 = Label(infocanvas,bg=colortone_info,height=1,bd=0,highlightthickness=0, font=('swos',8),anchor='c',text=version,fg='yellow')
    x_3 = Label(infocanvas,bg=colortone_info,height=1,bd=0,highlightthickness=0, font=('swos',8),anchor='c',text='brought to you by EMPI',fg='white')
    x_br1 = Label(infocanvas,bg=colortone_info,height=3,bd=0,highlightthickness=0, font=('swos',8),anchor='c',text=' ',fg='white')
    x_br2 = Label(infocanvas,bg=colortone_info,height=3,bd=0,highlightthickness=0, font=('swos',8),anchor='c',text=' ',fg='white')
    x_4 = Label(infocanvas,bg=colortone_info,height=1,bd=0,highlightthickness=0, font=('swos',8),anchor='c',text='find me on github or sensiblesoccer.de',fg='white')
    x_br1.grid(row=0,column=0)
    x_1.grid(row=1,column=0)
    x_2.grid(row=2,column=0)
    x_3.grid(row=3,column=0,pady=10)
    x_br2.grid(row=4,column=0)
    x_4.grid(row=5,column=0)
    
    rinf.mainloop()

def launchgitsite():
    webbrowser.open(url)

# Main window setup
root = tk.Tk()
root.title(title)
root.resizable(0,0) # Make the frame not resizable
root.geometry(str(windowW)+'x'+str(windowH))

# Define buttons/images used in app's window
b1 = PhotoImage(file='img/button_quit.png')             # Quit menu button
b2 = PhotoImage(file='img/button_opencar.png')          # Open *.CAR file menu button
img1 = PhotoImage(file='res/sensi_logo_small.png')      # Left-upper corner logo
bg = PhotoImage(file='img/bgswos_700x850.png')          # Left's side background
info = PhotoImage(file='img/button_info.png')           # Open info
git = PhotoImage(file='img/button_git.png')             # Open GitHUB

# Upper frame section (title)
#- - - - - - - - - - - - - - - - -
mf_upperframe = Frame(root, height=50, width=1000, bg=colortone, highlightthickness=0, bd=0)
mf_upperframe.grid(row=0,column=0,columnspan=2)
ImgLogo = Label(mf_upperframe,image=img1,bg=colortone)
ImgLogo.place(x=0,y=4)
txt = Label(mf_upperframe, text='SWOS Career Team Explorer', font=('swos',20), fg='white',bg=colortone,bd=0, anchor='w',width=50,highlightthickness='0')
txt.place(x=80,y=15)
txt = Label(mf_upperframe, text=version, font=('swos',8), fg='yellow',bg=colortone,bd=0, anchor='w',width=50,highlightthickness='0')
txt.place(x=880,y=22)

# Left frame section (squad)
#- - - - - - - - - - - - - - - - -
mf_leftframe = Frame(root, height=850, width=700,bg=colortone, highlightthickness=0, bd=0)
mf_leftframe.grid(row=1,column=0)
bg_label = Label(mf_leftframe,image=bg,bd=0,highlightthickness=0)   # Label to store bg image
bg_label.place(x=0,y=0)

# Right frame section (menu)
#- - - - - - - - - - - - - - - - -
mf_rightframe = Frame(root, height=850, width=300, bg=colortone, highlightthickness=0,bd=0) # Label with menu
mf_rightframe.grid(row=1,column=1)
Button(mf_rightframe, image=b1, borderwidth=0, highlightthickness=0, command=close).place(y=800,x=30)
Button(mf_rightframe, image=b2, borderwidth=0, highlightthickness=0, command=opencar).place(y=750,x=30)
Button(mf_rightframe, image=info, borderwidth=0, highlightthickness=0, command=infobox).place(y=700,x=160)
Button(mf_rightframe, image=git, borderwidth=0, highlightthickness=0, command=launchgitsite).place(y=700,x=30)

root.mainloop()