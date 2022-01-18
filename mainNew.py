#josue gallardo 10/6/2021

from tkinter import *
import tkinter.messagebox
import re



#var to keep current line
countLine=0


#separate by type
def cutOneLineTokens(word):

    # storing matching regex
    emptyList = []

    while 1:


        # remove spaces
        word = word.replace(" ", "")

        # check lengh string
        if len(word) == 0:
            break


        # check for keywords
        x = re.match("(if|int|else|float)", word)
        if x != None:
            emptyList.append(f'<keyword,{x.group()}>')
            # remove x.group from orignal string
            word = word[:x.span()[0]] + word[x.span()[1]:]

        # check for keywords
        x = re.match(r"(\t)", word)
        if x != None:
            emptyList.append(f'<tab,{x.group()}>')
            # remove x.group from orignal string
            word = word[:x.span()[0]] + word[x.span()[1]:]

        # check for operator
        x = re.match(r"(=|\+|>|<|\*)", word)
        if x != None:
            emptyList.append(f'<operator,{x.group()}>')
            # remove x.group from orignal string
            word = word[:x.span()[0]] + word[x.span()[1]:]

        # check for separator
        x = re.match(r"(\(|\)|:|\"|;)", word)
        if x != None:
            emptyList.append(f'<separator,{x.group()}>')
            # remove x.group from orignal string
            word = word[:x.span()[0]] + word[x.span()[1]:]

        # check for float_literals
        x = re.match(r"(\d+\.\d+)", word)
        if x != None:
            emptyList.append(f'<float_literals,{x.group()}>')
            # remove x.group from orignal string
            word = word[:x.span()[0]] + word[x.span()[1]:]

        # check for int_literals
        x = re.match(r"(\d+)", word)
        if x != None:
            emptyList.append(f'<int_literals,{x.group()}>')
            # remove x.group from orignal string
            word = word[:x.span()[0]] + word[x.span()[1]:]

        # check for identifier
        x = re.match(r"\w([a-zA-z0-9])*", word)
        if x != None:
            emptyList.append(f'<identifier,{x.group()}>')
            # remove x.group from orignal string
            word = word[:x.span()[0]] + word[x.span()[1]:]

    print(emptyList)
    return emptyList


# class definition
class MyFirstGUI:

    def __init__(self, root):
        # Master is the default prarent object of all widgets.
        # You can think of it as the window that pops up when you run the GUI code.
        self.master = root
        self.master.title("Lexical Analizer for TinyPie")

        #label Source Code
        self.sourceLabel = Label(self.master, text="Source Code Input: ")
        self.sourceLabel.grid(row=0, column=0, sticky=E)

        #text input
        self.sourceInput = Text(self.master, height=10, width=20)
        self.sourceInput.grid(row=1, column=0, sticky=E)

        #Current processing line
        self.sourcePro = Label(self.master, text="Current Processing Line: ")
        self.sourcePro.grid(row=2, column=0, sticky=E)

        #Current processing line number
        self.sourceProLine = Entry(self.master)
        self.sourceProLine.grid(row=2, column=1, sticky=E)


        #button
        self.sourceButton = Button(self.master, text="Next Line ", command=self.nextLine)
        self.sourceButton.grid(row=3, column=1, sticky=E)

        #label Lexical Analized
        self.lexicalLabel = Label(self.master, text="Lexical Analized Result: ")
        self.lexicalLabel.grid(row=0, column=2, sticky=E)

        #text output
        self.userOutput = Text(self.master,height=10, width=20)
        self.userOutput.grid(row=1, column=2, sticky=E)

        #button
        self.sourceButton = Button(self.master, text="Quit ", command=self.quitGUI)
        self.sourceButton.grid(row=3, column=2, sticky=E)

        # parse tree
        self.parserTree = Label(self.master, text="Parse Tree: ")
        self.parserTree.grid(row=0, column=3, sticky=E)

        # tree output
        self.treeOutput = Text(self.master, height=10, width=20)
        self.treeOutput.grid(row=1, column=3, sticky=E)



    #fun check each line
    def nextLine(self):

        global countLine

        #split the input lines
        individualLine=self.sourceInput.get("1.0", "end-1c").split("\n")

        #check for last line
        if countLine > len(individualLine) - 1:
            self.warningPop()
            return


        #increase count
        self.sourceProLine.delete(0, END)
        self.sourceProLine.insert(END, countLine+1)

        #divide into token
        texttoken=cutOneLineTokens(word=individualLine[countLine])

        for index in texttoken:
            self.userOutput.insert(END, index + '\n')

        #print out
        #self.userOutput.insert(END, individualLine[countLine] + '\n')

        countLine+=1


    #terminate
    def quitGUI(self):
        myTkRoot.quit()

    #out of lines
    def warningPop(self):
        tkinter.messagebox.showinfo("Error", "maximum recursion depth exceeded, tap quit.")


#Mytokens = [("key", "float"), ("id", "myvar"), ("op", "="), ("int", "5"), ("op", "+"), ("int", "6"), ("op", "+"), ("float", "2.3"),
            #("sep", ";")]
Mytokens=[("key", "float"),("id","myvar"),("op","="),("int","5"),("op","*"),("float","4.3"),("op","+"),("float","2.1"),("sep",";")]

inToken = ("empty", "empty")


def accept_token():
    global inToken
    print("     accept token from the list:" + inToken[1])
    inToken = Mytokens.pop(0)



def math():
    print("\n----parent node math, finding children nodes:")
    global inToken
    multi()

    if(inToken[1]=="+"):
        print("child node (token):" + inToken[1])
        accept_token()
        print("child node (internal): multi")
        multi()

    else:
        print("error, math expects float or int")

def multi():
    print("\n----parent node multi, finding children nodes:")
    global inToken

    if (inToken[0] == "float"):
        print("child node (internal): float")
        print("   float has child node (token):" + inToken[1])
        accept_token()
    elif (inToken[0] == "int"):
        print("child node (internal): int")
        print("   int has child node (token):" + inToken[1])
        accept_token()

        if (inToken[1] == "+"):
            print("child node (token):" + inToken[1])
            accept_token()

            print("child node (internal): math")
            multi()

        elif (inToken[1] == "*"):
            print("child node (token):" + inToken[1])
            accept_token()

            print("child node (internal): math")
            multi()
        else:
            print("error, you need + after the int in the math")

def exp():
    print("\n----parent node exp, finding children nodes:")
    global inToken;
    typeT, token = inToken;

    if(typeT == "key"):
        print("child node (internal): key")
        print("   identifier has child node (token):" + token)
        accept_token()

    if (inToken[0] == "id"):
        print("child node (internal): identifier")
        print("   identifier has child node (token):" + inToken[0])
        accept_token()
    else:
        print("expect identifier as the first element of the expression!\n")
        return

    if (inToken[1] == "="):
        print("child node (token):" + inToken[1])
        accept_token()
    else:
        print("expect = as the second element of the expression!")
        return

    print("Child node (internal): math")
    math()


def parser():
    global inToken
    inToken = Mytokens.pop(0)
    exp()
    if (inToken[1] == ";"):
        print("\nparse tree building success!")
    return


parser()


if __name__ == '__main__':
    myTkRoot = Tk()
    my_gui = MyFirstGUI(myTkRoot)
    myTkRoot.mainloop()


