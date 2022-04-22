## all of the "updates" for the main loop
from butterFilter import butterFilter, notchFilter
# from catch_for_main_loop_v2 import SimulateInReal, model
from CatchClass import Streaming_classifier as Strassifier
# from catch_for_main_loop_v2 import Streaming_classifier as Strassifier
import tkinter as tk
import test
from app import MorseApp as Mapp
from tkinter.filedialog import asksaveasfilename
from SpikerStream_Python3_Script import streamIn
from serial.tools import list_ports
import pickle


class UserInterface:

    def __init__(self):
        self.app = Mapp()
        self.strassifier = Strassifier()
        self.save_array = []
        global j
        i = 0
        j = 0

        # create the window with title
        self.root = tk.Tk()
        self.root.title("Morse Code Interface")

        # create the frame containing the text boxes
        self.frm_text = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
        self.frm_text.pack()

        # create the text boxes, buttons(s) and label(s)
        self.morse_input = tk.Text(master=self.frm_text)  ## bottom text window
        self.text_output = tk.Text(master=self.frm_text)  ## top text window
        self.btn_close = tk.Button(master=self.frm_text, text="Close", command=self.close)
        self.btn_save = tk.Button(master=self.frm_text, text="Save", command=self.save)
        # self.btn_clock = tk.Button(master=self.frm_text,text='Clock',command=self.clock)
        self.lbl_current_word = tk.Label(master=self.frm_text, text="Current word:")
        self.ent_current_word = tk.Entry(master=self.frm_text, width=50)  ## word bar

        # configure grid (geometry manager)
        self.root.rowconfigure(2, minsize=500, weight=1)
        self.root.columnconfigure(1, minsize=500, weight=1)

        # assign text boxes, buttons and labels to grid
        self.morse_input.grid(row=2, column=1, sticky="nsew")
        self.text_output.grid(row=0, column=1)
        self.btn_close.grid(row=2, column=0, sticky="ew")
        self.btn_save.grid(row=0, column=0, sticky="ew")
        self.ent_current_word.grid(row=1, column=1, pady=10)

        ################
        # port selection
        ################

        ports = list_ports.comports()
        for port in ports:
            print(port)
        self.cport = 'COM5'  # input('Which port?\n')

        ## plot stuff
        # plt.ion()
        # plt.show()
        # self.fig, self.ax = plt.subplots()
        self.epic_loop()
        #self.actual_main_loop()  # change this to go between the different loops
        self.root.mainloop()

    def close(self):
        self.save()
        self.root.destroy()
        print("Closing the window.")

    def actual_main_loop(self):
        output = streamIn(self.cport)
        output_filtered = notchFilter(output)
        output_buttered = butterFilter(output_filtered)
        model = pickle.load(open("model.sav", 'rb'))
        a, b = self.strassifier.classify(output_buttered, model)
        print('This is b:' + str(b))
        self.app.inputNumber(b)  # b will be a list of events
        self.app.update()
        self.update()
        if self.app.open:
            self.root.after(200, self.actual_main_loop)

    def simulated_main_loop(self):
        print("I am simulating SpikerBox input from the .csv file.")
        i = 0
        self.output = SimulateInReal('output.csv', i)
        self.output_filtered = notchFilter(self.output)
        model = pickle.load(open("model.sav", 'rb'))
        a, b = self.strassifier.classify(10000, self.output_filtered[1:len(self.output_filtered)], model)
        print(b)
        if len(b) == 1:
            self.app.inputNumber(b[0])
        else:
            self.app.inputNumber(b)
        self.app.update()
        self.update()
        if self.app.open:
            i += 1
            self.root.after(1000, self.simulated_main_loop)
        elif i == 59:
            self.close()


    def random_input_loop(self):
        b = test.arrReader()
        self.app.inputNumber(b)  # b will be a list of events
        print(self.app.endWord)
        self.app.update()
        self.update()
        print(self.app.currentLetter)
        for i in range(0,4):
            self.app.inputNumber([])  # b will be a list of events
            self.app.update()
            self.update()
        if self.app.open:
            self.root.after(4000, self.random_input_loop)

    def epic_loop(self):
        global j
        epic = [[0],[],[],[],[0],[-1],[-1],[0],[],[],[],[0],[0],[],[],[],[-1],[0],[-1],[0],[1]]
        self.app.inputNumber(epic[j])  # b will be a list of events
        print(self.app.endWord)
        self.app.update()
        self.update()
        j += 1
        self.root.after(1000,self.epic_loop)

    def update(self):
        app = self.app
        changes = app.getChanges()
        if changes == None:
            return
        print(changes)
        self.morse_input.insert(tk.END, changes[2])  ## changes[2] is bottomChange
        self.ent_current_word.delete(0, tk.END)
        self.ent_current_word.insert(tk.END, changes[1])
        if not len(changes[0]) == 0:
            self.text_output.insert(tk.END, " " + " ".join(changes[0]))

    def save(self):
        # saves the current text in the output box as .txt file
        self.filepath = asksaveasfilename(defaultextension="txt",
                                          filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not self.filepath:
            return
        with open(self.filepath, "w") as self.output_file:
            self.text = self.text_output.get("1.0", tk.END)
            self.output_file.write(self.text)
        self.root.title("Morse Code Interface")
        print('Saving the file.')


app = UserInterface()
