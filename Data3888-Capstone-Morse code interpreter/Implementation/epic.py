from tkinter import *
import datetime

root = Tk()

lab = Label(root)
lab.pack()

def clock():
    currentString = ''
    currentString = update_string(currentString)
    lab.config(text=currentString)
    #lab['text'] = time
    root.after(1000, clock) # run itself again after 1000 ms

def update_string(str1):
    str2 = input('hello')
    str1 += str2
    return str1
# run first time
clock()

root.mainloop()




# from tkinter import *
# from time import sleep

# root = Tk()
# var = StringVar()
# var.set('hello')

# l = Label(root, textvariable = var)
# l.pack()

# for i in range(6):
#     sleep(1) # Need this to slow the changes down
#     var.set('goodbye' if i%2 else 'hello')
#     root.update_idletasks()


# from tkinter import *
# import time

# root = Tk()
# v = StringVar()

# def callback(*args):
#     global tex
#     tex = e.get()
# v.trace("w", callback)

# def change():   
#     if tex  == ("cat"):
#         root.after(1000,e.insert(0, "dog"))
#         #time.sleep(0.5)
#         pass
#     else:
#         root.after(1000,e.delete(0, END))
#         #time.sleep(0.5)
#         root.after(1000,e.insert(0, "dog"))



# # def callback(*args):
# #     global tex
# #     tex = e.get()
# # v.trace("w", callback)

# e = Entry(root, textvariable=v)
# e.insert(0, "cat")
# e.pack(side=BOTTOM)
# #tex = e.get() #When text is defined with get(), it does not change 
#               #dynamically with the entry widget


# l = Label(root, textvariable=v)
# l.pack(side=TOP)

# change()
# v.trace("w", callback)
# root.mainloop()