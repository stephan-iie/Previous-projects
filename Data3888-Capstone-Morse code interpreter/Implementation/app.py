class MorseApp:
    #  well formed morse - https://datagenetics.com/blog/march42012/index.html#:~:text=Each%20letter%20is%20represented%20by,is%20left%20between%20each%20word).
    # a dictionary containing alphanumeric to morse code values.
    MORSE = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}
    # a dictionary that is the reverse of MORSE
    ALPHA = {value : key for (key, value) in MORSE.items()}
    
    def __init__(self,filename = None):
        self.storage = []
        ## current values in memory ( lower panel)
        self.currentLetter = ''
        self.currentWord = ''
        # if false close application:
        self.open = True
        # if true end respective term:
        self.endLetter = False
        self.endWord = False
        # Stores chagnes for both the top window and bottom window
        self.changed = False
        self.topChange = []
        self.bottomChange = ''
        self.emptyTracker = 0

    def close(self):
        ''' closes application and saves all data'''
        self.storageToFile()
        self.userInt.close()

    def num2morse(self,dotdash):
        ''' converts input number to morse code'''
        if dotdash == 0:
            print('dot')
            self.bottomChange = '.'
            self.changed = True
            return "."
        elif dotdash == -1:
            print('dash')
            self.bottomChange = '-'
            self.changed = True
            return '-'

    def inputNumber(self,num): #0 for blink #1 long #-1 double
        ''' inputs number as morse to current letter or ends letter/word'''
        if len(num) == 0:
            self.emptyTracker += 1
            if self.emptyTracker == 3:
                self.endLetter = True
                self.emptyTracker = 0
        for i in num:
            if i in [-1,0]:
                self.currentLetter += self.num2morse(i)
                self.emptyTracker = 0
            # elif self.emptyTracker == 3:
            #     self.endLetter = True
            #     self.emptyTracker = 0
            elif i == 1:
                self.endWord = True
                self.emptyTracker = 0
        # print(self.emptyTracker)

    def endCurrentLetter(self):
        ''' end the current letter and adds it to the current word '''
        if self.currentLetter == '------': # thinking i might set this to '\close' and set a convention where backslash means command.
            self.open = False
            return
        else:
            if self.currentLetter in self.ALPHA.keys():
                letter = self.ALPHA[self.currentLetter]
                self.currentLetter = ''
                self.currentWord += letter
                self.changed = True
                self.endLetter = False
            else:
                print("sorry, letter does not exist try again. Restarting input...")
                self.currentLetter = ''
                self.endLetter = False
                self.changed = True


    def endCurrentWord(self):
        ''' end the current word and add it to storage '''
        ## gonna have to do spellcheck here
        self.endCurrentLetter()
        word = self.currentWord
        self.storage.append(word)
        self.topChange.append(word)
        self.endWord = False
        self.currentWord = ''

    def update(self):
        ''' given all of the changes that have occured in the backend it updates the changes '''
        if self.endWord:
            self.endCurrentWord()
        elif self.endLetter:
            self.endCurrentLetter()
        if not self.open:
            print('Closing')
            self.close()

    def getChanges(self):
        if self.changed:
            print('The application has been changed')
            result = [self.topChange, self.currentWord, self.bottomChange]
            self.changed = False
            self.topChange = []
            self.bottomChange = ''
            return result
        else:
            print('the application has not been changed')
            return None

