#HW7 Python Project -- parser

from tkinter import *
import re

class MyLexicalGUI:  # class definition

    # This is the initialize function for a class.
    # Variables belonging to this class will get created and initialized in this function
    # What is the self parameter? It represents this class itself.
    # By using self.functionname, you can call functions belonging to this class.
    # By using self.variablename, you can create and use variables belonging to this class.
    # It needs to be the first parameter of all the functions in your class

    def __init__(self, root):
        # Master is the default prarent object of all widgets.
        # You can think of it as the window that pops up when you run the GUI code.
        self.master = root
        self.master.title("Lexical Analyzer for TinyPie")

        self.inputLabel = Label(self.master, text="Source Code Input: ", padx = 50)
        self.inputLabel.grid(row=0, column=0, sticky=E)

        self.outputLabel = Label(self.master, text="Lexical Analyzed Result: ", padx = 70)
        self.outputLabel.grid(row=0, column=1, sticky=E)

        self.outputLabel2 = Label(self.master, text="Parse Tree: ", padx=70)
        self.outputLabel2.grid(row=0, column=2, sticky=E)

        self.inputText = Text(self.master, width = 25, height = 10)
        self.inputText.grid(row=1, column=0, sticky=E)

        self.outputText = Text(self.master, width=25, height=10)
        self.outputText.grid(row=1, column=1, padx = 40, sticky=E)

        self.outputText2 = Text(self.master, width=25, height=10)
        self.outputText2.grid(row=1, column=2, sticky=E)

        self.currentLine_Label = Label(self.master, text="Current Processing Line: " , padx = 70 )
        self.currentLine_Label.grid(row=2, column=0, sticky=E)

        self.currentInputLine = 0;
        self.currentOutputLine = 0;
        self.currentLine_Label2 = Label(self.master, text= 0)
        self.currentLine_Label2.grid(row=2, column=0, sticky=E, padx = 50)

        self.nextLine_Button = Button(self.master, text="Next Line", command=self.analyzeResult)
        self.nextLine_Button.grid(row=3, column=0, sticky=E)

        self.quitButton = Button(self.master, text="Quit", command=self.closeGui, width = 8)
        self.quitButton.grid(row=3, column=1, sticky=E, padx = 40)


    def analyzeResult(self):
        text = self.inputText.get('1.0', END).splitlines() #turn inputbox text into list
        if self.currentInputLine < len(text): #avoid index out of range error
            TokenOutputList = CutOneLineTokens(text[self.currentInputLine])
            ParserTokenList = []
            for T in TokenOutputList:
                self.outputText.insert(float(self.currentOutputLine) + 1.0, T + "\n" ) #insert line into output
                self.currentOutputLine += 1 #increment output line
                T = T.replace("<", "")
                T = T.replace(">", "")
                ParserTokenList.append(tuple(T.split (",")))

            self.currentInputLine += 1 #increment input line
            self.currentLine_Label2.configure(text = self.currentInputLine) #update count in currentLine label
            print(str(ParserTokenList))
            parser(ParserTokenList)


    def closeGui(self):
        self.master.destroy() #close Gui


        # HW3 Lexer stuff

def Match(code, word):
    result = re.match(code, word)
    if (result != None):
        return result.group(0)
    else:
        return False

def Search(code, word):
    result = re.search(code, word)
    if (result != None):
        return result.group(0)
    else:
        return False


def CutOneLineTokens(line):
    output = []
    linewithspace = line
    line = line.replace(" ", "") #spaces mess with them for some reason
    while(line != ""): #while just in case there are multiple instances of the same type of token

        key = Match(r'if|else|int|float', line)
        if key != False:
            output.append("<key," + key + ">")
            line = re.sub(r'if|else|int|float', "", line, 1)

        id = Match(r'[A-z]+\d+|[A-z]+', line)
        if id != False:
            output.append("<id," + id + ">")
            line = re.sub(r'[A-z]+\d+|[A-z]+', "", line, 1)

        sep = Match(r'\(|\)|"|:|;', line)
        if sep != False:
            output.append("<sep," + sep + ">")
            line = re.sub(r'\(|\)|"|:|;', "", line, 1)

        op = Match(r'=|\+|>|\*', line)
        if op != False:
            output.append("<op," + op + ">")
            line = re.sub(r'=|\+|>|\*', "", line, 1)

        #literals
        flolit = Match(r'\d*\.\d+', line)  # float
        if flolit != False:
            output.append("<flo_lit," + flolit + ">")
            line = re.sub(r'\d*\.\d+', "", line, 1)
        intlit = Match(r'\d+', line)  # int
        if intlit != False:
            output.append("<int_lit," + intlit + ">")
            line = re.sub(r'\d+', "", line, 1)
        strlit = Search(r'".*"', linewithspace)  # string
        if strlit != False:
            #need to save the string to literal and "" to seperators
            strlit = re.sub(r'"',"",strlit);
            output.append("<sep," + '"' + ">");
            output.append("<str_lit," + strlit + ">")
            output.append("<sep," + '"' + ">");
            line = re.sub(r'".*"', "", line, 1)
            linewithspace = re.sub(r'".*"', "", linewithspace, 1)

    return output


# Mytokens=[("key","float"),("id","myvar"),("op","="),("int","5"),("op","+"),("int","6"),("op","+"),("float","2.3"),("sep",";")]
#Mytokens = [("key", "float"), ("id", "myvar"), ("op", "="), ("int", "5"), ("op", "*"), ("float", "4.3"), ("op", "+"),
           # ("float", "2.1"), ("sep", ";")]
# Mytokens=[("key", "float"),("id","mynum"),("op","="),("float","3.4"),("op","+"),("int","7"),("op","*"),("float","2.1"),("sep",";")]
Mytokens = []
inToken = ("empty", "empty")


def accept_token():
    global inToken
    print("     accept token from the list:" + inToken[1])
    inToken = Mytokens.pop(0)


def math():
    print("\n----parent node math, finding children nodes:")
    global inToken

    multi()
    if (inToken[1] == "+"):
        print("\nchild node (token):" + inToken[1])
        accept_token()
        print("child node (internal): multi")
        multi()


def multi():
    print("\n----parent node multi, finding children nodes:")
    global inToken

    if (inToken[0] == "int_lit"):
        print("child node (internal): int")
        print("   int has child node (token):" + inToken[1])
        accept_token()
    elif (inToken[0] == "flo_lit"):
        print("child node (internal): float")
        print("   float has child node (token):" + inToken[1])
        accept_token()

    if (inToken[1] == "*"):
        print("child node (token):" + inToken[1])
        accept_token()
        print("child node (internal): multi")
        multi()


def exp():
    print("\n----parent node exp, finding children nodes:")
    global inToken;
    typeT, token = inToken;
    if (typeT == "key"):
        print("child node (internal): key")
        print("   key has child node (token):" + token)
        if(token == "if"):
            if_exp()


        accept_token()


    else:
        print("expect key as the first element of the expression!\n")
        return

    if (inToken[0] == "id"):
        print("child node (internal): identifier")
        print("   identifier has child node (token):" + inToken[1])
        accept_token()
    else:
        print("expect identifier as the second element of the expression!\n")
        return

    if (inToken[1] == "="):
        print("child node (token):" + inToken[1])
        accept_token()
    else:
        print("expect = as the third element of the expression!")
        return

    print("Child node (internal): math")
    math()


def if_exp():
    global inToken
    print("*********************************************")
    accept_token()
    if (inToken[0] == "sep"):
        print("child node (internal): operator")
        print("   identifier has child node (token):" + inToken[1])
        accept_token()
    else:
        print("expect identifier as the second element of the expression!\n")
        return

    if (inToken[0] == "id"):
        print("child node (token):" + inToken[1])
        accept_token()
    else:
        print("expect = as the third element of the expression!")
        return

    if (inToken[0] == "op"):
        print("child node (token):" + inToken[1])
        accept_token()
    else:
        print("expect = as the third element of the expression!")
        return

    print("Child node (internal): if_exp")
    if_exp()


def parser(TokenList):
    global Mytokens
    global inToken
    Mytokens = TokenList
    inToken = Mytokens.pop(0)
    exp()
    if (inToken[1] == ";"):
        print("\nparse tree building success!")
    return



if __name__ == '__main__':
    myTkRoot = Tk()
    my_gui = MyLexicalGUI(myTkRoot)
    myTkRoot.mainloop()

