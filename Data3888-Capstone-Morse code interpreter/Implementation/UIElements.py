import tkinter as tk

# create the window with title

def close(self):
        # close the window; used in the close box
        self.app.close()
        self.root.destroy()
        print("Closing the window.")

def save(self):
    # saves the current text in the output box as .txt file
    self.filepath = asksaveasfilename(defaultextension="txt",filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if not self.filepath:
        return
    with open(self.filepath, "w") as self.output_file:
        self.text = self.text_output.get("1.0",tk.END)
        self.output_file.write(self.text)
    self.root.title("Morse Code Interface")
    print('Saving the file.')

root = tk.Tk()
root.title("Morse Code Interface")

# create the frame containing the text boxes
frm_text = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
frm_text.pack()

# create the text boxes, buttons(s) and label(s)
morse_input = tk.Text(master=frm_text)
text_output = tk.Text(master=frm_text)
btn_close = tk.Button(master=frm_text,text="Close",command=close)
btn_save = tk.Button(master=frm_text,text="Save",command=save)
#btn_clock = tk.Button(master=frm_text,text='Clock',command=clock)
lbl_current_word = tk.Label(master=frm_text, text="Current word:")
ent_current_word = tk.Entry(master=frm_text, width = 50)

# configure grid (geometry manager)
root.rowconfigure(2,minsize=500,weight=1)
root.columnconfigure(1,minsize=500,weight=1)

# assign text boxes, buttons and labels to grid
morse_input.grid(row=2,column=1,sticky="nsew")
text_output.grid(row=0,column=1)
btn_close.grid(row=2,column=0,sticky="ew")
btn_save.grid(row=0,column=0,sticky="ew")
#btn_clock.grid(row=1,column=0,sticky="ew")
#lbl_current_word.grid(row=1,column=1,sticky="w")
ent_current_word.grid(row=1,column=1,pady=10)

# apply the update_morse function
#update_morse(None)
#needed to get it to work
#clock()

root.mainloop()