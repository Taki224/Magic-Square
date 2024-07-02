import time
import datetime
from random import randint
from threading import Thread
from exercise4 import MagicSquare
from tkinter import *
from tkinter import messagebox, filedialog

root = Tk()
root.title("Magic Squares")
#Set the size and open it centered
w = 500
ws = root.winfo_screenwidth()
h = 250
hs = root.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

#the gameOn variable shows if the game is on or not
def setGameOn(state):
    global gameOn
    gameOn = state
#at the beginning it is false
setGameOn(False)

#this function checks if the game is on and if it is, it asks if you want to start a new game
def newGameCheck(n = 1, bytemp = False):
    if gameOn:
        msg_box = messagebox.askquestion('Restart', 'Are you sure you want quit the current puzzle?',icon='warning')
        if msg_box == 'yes':
            generateTable(n)
    else:
        generateTable(n, bytemp)

#this functions opens the a new window where the player can choose the size of the magic square
def openNewWindow():
    newWindow = Toplevel(root)
    newWindow.title("Magic squares")
    w = 400
    ws = newWindow.winfo_screenwidth()
    h = 300
    hs = newWindow.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    newWindow.geometry('%dx%d+%d+%d' % (w, h, x, y))

    label = Label(newWindow, text="Generate new puzzle", font=("Arial", 20))
    label.grid(row=0, column=0, padx=10, columnspan=2)

    btn1 = Button(newWindow, text="5x5", font=("Arial", 20), command=lambda: [newGameCheck(5), newWindow.destroy()])
    btn1.grid(row=1, column=0, padx=10, pady=10)
    btn2 = Button(newWindow, text="7x7", font=("Arial", 20), command=lambda: [newGameCheck(7), newWindow.destroy()])
    btn2.grid(row=1, column=1, padx=10, pady=10)

    label2 = Label(newWindow, text="Or", font=("Arial", 20))
    label2.grid(row=2, column=0, padx=10, columnspan=2)

    btn3 = Button(newWindow, text="Load puzzle from text file", font=("Arial", 20), command=lambda: [newGameCheck(bytemp=True), newWindow.destroy()])
    btn3.grid(row=3, column=0, padx=10, pady=10, columnspan=2)
    return newWindow

#This function generates the table, the bytemp variable shows if the table is generated from a text file or not
def generateTable(n=1, bytemp = False):
    #if there was a previous table, it is destroyed and the game is stopped
    setGameOn(False)
    for widget in f.winfo_children():
        widget.destroy()
    for widget in fl.winfo_children():
        widget.destroy()
    global tab
    tab = []
    global size
    size = n
    global mconst
    global table
    global solution
    #set the attributes of the table based on the generating method (from file or not)
    if not bytemp:
        global magicSquare
        magicSquare = MagicSquare(n)
        table = magicSquare.puzzle()
        mconst = magicSquare.magic_constant()
        solution = magicSquare.solution()
    else:
        table, solution, mconst, size = loadFromFile()
    label = Label(fl, text=f'You are now playing magic square with {size}x{size} squares.', font=("Arial", 20))
    label.grid(row=1, column=0, padx=10, columnspan=4, sticky=W)
    label2 = Label(fl, text="Magic constant is: "+str(mconst), font=("Arial", 20))
    label2.grid(row=2, column=0, padx=10, columnspan=4,sticky=W)
    global label3
    label3 = Label(fl, text="Time: 0:00:00", font=("Arial", 20), fg="green")
    label3.grid(row=3, column=2, padx=10, columnspan=2,sticky=W)
    #generate the grid
    for row in range(size):
        #loading the Entries
        for col in range(size+1):
            if col < len(table):
                sv = StringVar()
                sv.trace("w", lambda name, index, mode, sv=sv: calcSums())
                e = Entry(f, width=4, font=('Arial', 20))
                #the non 0 values are preloaded and disabled
                if table[row][col] != 0:
                    sv = StringVar(value=table[row][col])
                    e.config(state=DISABLED)
                e.config(textvariable=sv, highlightthickness=1, highlightbackground="black", justify=CENTER)
                e.grid(row=row+3, column=col, padx=3, pady=3)
                tab.append(e)
            #Putting a sum entry at the end of each row
            else:
                e = Entry(f, width=4, font=('Arial', 20), bg='yellow', fg='red', highlightthickness=1, highlightbackground="black")
                e.grid(row=row+3, column=col, padx=3, pady=3)
                e.config(state=DISABLED, disabledbackground='yellow', disabledforeground='red', justify=CENTER)
                tab.append(e)
    #putting a sum entry at the end of each column
    for col in range(size):
        e= Entry(f, width=4, font=('Arial', 20), bg='yellow', fg='red', highlightthickness=1, highlightbackground="black", justify=CENTER)
        e.grid(row=row+4, column=col, padx=3, pady=3)
        e.config(state=DISABLED, disabledbackground='yellow', disabledforeground='red')
        tab.append(e)
    sumLabel = Label(f, text='SUM', font=("Arial", 20), fg='red')
    sumLabel.grid(row=row+4, column=col+1, padx=3, pady=3)
    root.update()
    #get the size of the frame, based on this the size of the window is changed to fit the table
    width = f.winfo_width()
    height = f.winfo_height()
    root.geometry(f'{width+130}x{height+250}')
    calcSums()
    #start the game and the timer
    setGameOn(True)
    thread = Thread(target=timer)
    thread.setDaemon(True)
    thread.start()

#this function checks if the entered value is number or not
def checkInput():
    for e in tab:
        #if it is not a number, the content is deleted
        if e.get() != '' and not int(e.get().isnumeric()):
            e.delete(0, END)
            return False
    return True

#this function calculates the sums of the rows, columns. It is called after every change in the table
def calcSums():
    #if the entered value is not a number, the function is aborted
    if not checkInput():
        return
    row, col = 0,0
    rowSums = {}
    colSums = {}
    #calculating the sums of the rows and columns
    for i in range(len(tab)):
        if i % (size+1) == 0:
            row += 1
            col = 0
        col = i - (row-1)*(size+1)
        #if the value is not empty, it is added to the sum or if the row is not in the dictionary, it is added
        if row-1 in rowSums.keys():
            if row-1 < size and col < size:
                rowSums[row-1] += int(tab[i].get()) if tab[i].get() != '' else 0
        else:
            if row-1 < size and col < size:
                rowSums[row-1] = int(tab[i].get()) if tab[i].get() != '' else 0
        #same, but for columns
        if col in colSums.keys():
            if col < size and row-1 < size:
                colSums[col] += int(tab[i].get()) if tab[i].get() != '' else 0
        else:
            if col < size and row-1 < size:
                colSums[col] = int(tab[i].get()) if tab[i].get() != '' else 0
    sums = []
    #putting the sums into the right entries
    for k in colSums.keys():
        tab[(size+1)*(size)+k].config(state=NORMAL)
        tab[(size+1)*(size)+k].delete(0, END)
        tab[(size+1)*(size)+k].insert(END, colSums[k])
        #if the sum is correct, the entry is green, otherwise red
        if colSums[k] == mconst:
            tab[(size+1)*(size)+k].config(disabledforeground='green')
        else:
            tab[(size+1)*(size)+k].config(disabledforeground='red')
        tab[(size+1)*(size)+k].config(state=DISABLED)
        sums.append(colSums[k])
    for k in rowSums.keys():
        tab[(k+1)*size+k].config(state=NORMAL)
        tab[(k+1)*size+k].delete(0, END)
        tab[(k+1)*size+k].insert(END, rowSums[k])
        if rowSums[k] == mconst:
            tab[(k+1)*size+k].config(disabledforeground='green')
        else:
            tab[(k+1)*size+k].config(disabledforeground='red')
        tab[(k+1)*size+k].config(state=DISABLED)
        # print(k, rowSums[k])
        sums.append(colSums[k])
    #this checks if all the sums are correct. If so, the game is over, the timer stops
    if len(set(sums)) == 1 and list(set(sums))[0]==mconst:
        setGameOn(False)


#the timer function runs on a separate thread
def timer():
    starttime = time.time()
    while gameOn:
        time.sleep(1)
        sec = int(time.time() - starttime)
        #the time is displayed in the format h:mm:ss in a label
        label3.config(text=f'Time: {str(datetime.timedelta(seconds=sec))}')

#this function clears all the player's entries. It does not clear the entries if it was given as a hint.
def clearInput():
    #if the game is not running, the button does nothing
    if not gameOn:
        return
    for i in range(len(tab)):
        if tab[i].cget('state') != DISABLED:
            tab[i].delete(0, END)
    calcSums()

#this function shows the solution by filling out all the entries with the correct values. If this function is called, the game is over
def showSolution():
    #if the game is not running, the button does nothing
    if not gameOn:
        return
    setGameOn(False)
    sol = []
    for row in solution:
        for n in row:
            sol.append(n)
        sol.append('sum')
    for i in range(len(tab)):
        if tab[i].cget('state') != DISABLED:
            tab[i].delete(0, END)
            tab[i].insert(END, sol[i])
            tab[i].config(state=DISABLED, disabledforeground='green')
    calcSums()

#this function chooses a random entry and fills it with a correct value.
def getHint():
    #if the game is not running, the button does nothing
    if not gameOn:
        return
    sol = []
    for row in solution:
        for n in row:
            sol.append(n)
        sol.append('sum')
    #check if there is an empty entry
    theresEmpty = False
    for e in tab:
        if e.get() == '':
            theresEmpty = True
            break
    #is there is an empty entry, a random one is chosen and filled with a correct value
    if theresEmpty:
        r = randint(0, (size+1)*(size)-1)
        while (tab[r].cget('state') == DISABLED or tab[r].get()!=''):
            r = randint(0, (size+1)*(size+1)-2)
        tab[r].insert(END, sol[r])
        tab[r].config(state=DISABLED, disabledforeground='green')

#this function is called if the load from file option is chosen
def loadFromFile():
    #the player can choose a file
    filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
    so = []
    ta = []
    sob = True
    #if there was a file chosen, the content is read
    if filename != '':
        file = open(filename, mode='r').read().split('\n')
        #first the solution
        for r in file:
            #this checks if we read the puzzle or the solution
            if '-' in r:
                sob = False
            else:
                if sob:
                    so.append(list(map(int,r.replace('[', '').replace(']', '').strip().split(' '))))
                else:
                    if len(r)>1:
                        ta.append(list(map(int,r.replace(' ', '').replace('|', ' ').strip().split(' '))))
    #calculates the magic constant
    const = sum(so[0])
    #returns all the neccessary attributes for the game
    return ta, so, const, len(so[0])

#the button for the main functions
newButton = Button(root, text="New Puzzle", height=2, command=openNewWindow)
newButton.grid(row=0, column=0, sticky=N+E+S+W, padx=10, pady=10)

hintButton = Button(root, text="Get Hint", height=2, command=lambda: getHint())
hintButton.grid(row=0, column=1, sticky=N+E+S+W,padx=10, pady=10)

solutionButton = Button(root, text="Show Solution", height=2, command=lambda: showSolution())
solutionButton.grid(row=0, column=2, sticky=N+E+S+W,padx=10, pady=10)

clearButton = Button(root, text="Clear Input",height=2, command=lambda: clearInput())
clearButton.grid(row=0, column=3, sticky=N+E+S+W,padx=10, pady=10)

#the frame for the texts
fl = Frame(root)
fl.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

#the frame for the table
f = Frame(root)
f.grid(row=4, column=0, columnspan=4, padx=10, pady=10)


mainloop()