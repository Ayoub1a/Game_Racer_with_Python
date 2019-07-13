from tkinter import *
from Class_pygame import *
from sys import exit 

def play() :
    user_name = entry_fullname.get()
    root.destroy()
    race_game = Race_game(800 , 600 , (0 , 255 , 0) , "images_races/race1.png" , 44 , user_name.lower() , save = "yes")

root = Tk()


Label(root , text = "Entre your name : ").grid(row = 1 , column = 1)
entr = StringVar()
entr.set("ayoub bouallal")

entry_fullname = Entry(root , bg = "#3333ff"   ,textvariable = entr )
entry_fullname.grid(row = 1 , column = 2)


Button(root , text = "Play Now" ,
 bg = "green" ,bd = 4 , 
 fg = "yellow" ,
 highlightcolor = "blue" ,
 activebackground = "blue" ,
 activeforeground = "red" , 
command = play).grid(row = 2,column = 1)
Button(root , text = "Quit" ,
 bg = "red" ,
 bd = 4 , 
 activebackground = "yellow" ,
 activeforeground = "blue" ,
  command = exit).grid(row = 2 , column = 2)

root.title("Game Race ")
root.geometry("300x100+50+50")
root.mainloop()
