# 3888-Capstone

# Code Guide

This is a guide explaining how to run Brain 2's morse code interpreter, as well as its dependencies and an overview of how it functions. We turn first to the dependencies.

## Dependencies

Our code runs on *Python 3.8*. It requires the following packages to be installed to run:

- Pandas (Python Data Analysis Library);
- NumPy;
- Pyserial;
- Tkinter;
- Pickle;
- Argparse;
- Os;
- SciPy;
- Scikit-learn; and,
- Catch22.

## How to Run

Simply run the *main.py* script inside the Implementation folder.

## How it Works

Running *main.py* initialises the loop within *UI.py*. We first give quote the sequence of functions it runs, and second explain where these functions are and how they individually work.

>    def actual_main_loop(self):
>
>        output = streamIn(self.cport)
>
>        output_filtered = notchFilter(output)
>
>        output_buttered = butterFilter(output_filtered)
>
>        model = pickle.load(open("model.sav", 'rb'))
>
>        a, b = self.strassifier.classify(output_buttered, model)
>
>        self.app.inputNumber(b)  # b will be a list of events
>
>        self.app.update()
>
>        self.update()
>
>        if self.app.open:
>
>            self.root.after(200, self.actual_main_loop)

### streamIn

streamIn takes in data from the SpikerBox, taking in as an input the cport of the SpikerBox. It has a buffer of one second, and each time actual_main_loop calls it, it outputs that buffered data as a NumPy array.

streamIn can be located in the *SpikerStream_Python3_Script.py* script inside the Implementation folder.

### notchFilter/butterFilter

These two filters remove the 50 Hz line noise from the output data, then apply a lowpass filter to remove higher frequency components. The result is a NumPy array which has been significantly smoothed out, leaving a high signal-to-noise ratio with more discernable blinking events.

notchFilter and butterFilter can be located in *butterFilter.py*.

### pickle.load

This line uses the pickle package to load in the saved parameters of the classifier from the *model.sav* file. This circumvents the need to re-train the classifier model each time the code is initiated.

*model.sav* can be found in the Implementation folder.

### strassifier.classify

*strassifier* is an object called from the classifier script in *catchClass.py*. Within this objectis the function *classify*, which using the loaded in parameters, finds each event, classifies it, and outputs a list of values within [-1,0,1]. It takes in the filtered data, and the loaded in model from *model.sav*.

### UI Updates

The lines using the *app* object, in essence, turn the outputted -1, 0 or 1 into a dash, dot or long blink respectively. Then, in *self.update()*, the UI update function is called which updates the UI to display the corresponding Morse code output. It will also display the Morse code letter it corresponds as part of the word currently being formed.

# Github Guide
Hello friends,


I thought id set up a quick github guide for the people in the group that arent familiar with it.

## Setting up github for the first time
Github is a hub of gits, so the first thing you'll need to do is download and install git. You can find the download link [here](https://git-scm.com/downloads).


Next you'll need a text editor for your code and bash terminal, so why not get two birds with one stone and download [vscode](https://code.visualstudio.com/). VS code is a text editor with a built- in terminal and it is automatically in night mode so you know its good.

To test if everything is working type `git` into the VScode terminal (terminal -> new terminal)  and see if it throws an error.

So at this point you have git installed and VS code set up. Now you want to configure your local git so that it knows who you are. To do this we want to open a new terminal in vscode (terminal -> new terminal). Then type in the command window:

`git config --global user.name "your-unikey-here"`

and your email

`git config --global user.email "your-unikey-here@uni.sydney.edu.au"`

and now git knows who you are.


Now you need to navigate to the folder that you want to do all your work in (file -> open folder). Note: you will probably want an empty folder for this so create a new one in your *well organised* folders.

Once you are in this folder you will need to create a new terminal. Then using this terminal, you need to create a new local git repository.

`git init` 

and it should initialize an empty repository. Then to link up your local git to the repo on github type: 

`git remote add origin https://github.sydney.edu.au/zhwu3591/3888-Capstone`

Think of this as creating a remote connection to the shared github from the local git you just created and then naming that connection origin.

## general use of github

Now you want to merge your current git with the github repository. This basically just means you are downlaoding the git to work on it. So you must call a pull request to the origin connection we just created. In terminal type:

`git pull origin master` 

and this will pull the master branch ("the main branch") from the github repository and save it to your local git repository. WARNING make sure you have no work you have already done in your local git that you havent saved somewhere (or pushed) as it will delete that work.

Sweet now you can start working on the git.

To save the work to the local git you need to first save each file and then manually add each file to the next commit. do this by typing 

`git add <filename>`

for each file and after you have added all files you commit those adds to the local git by typing:

`git commit -m "desription of changes"`

Then to send that work from your local repo to the shared github (so your friends can see it) type the following command:

`git push origin master`

and look at that youre an expert.