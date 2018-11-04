from tokenize import tokenize
import sys
import token



class InvalidCharacter(RuntimeError):
    args = []
    def __init__(self, arg):
        self.args = arg

class LispSyntaxError(RuntimeError):
    args = []
    def __init__(self, arg):
        self.args = arg

class evaluationError(RuntimeError):
    args = []
    def __init__(self, arg):
        self.args = arg

class Lisp:
    '''
    Lisp Class is used to handle input, output and evaluation
    '''
    tokens = []
    cursor = 0
    exp = []
    symbolList = []
    dList = {}
    def __init__(self,tokens):
        self.tokens = tokens
        self.symbolList.append('NIL')
        self.symbolList.append('T')
        self.symbolList.append('COND')
        self.symbolList.append('DEFUN')
        self.symbolList.append('QUOTE')
    
    def isSymbolic(self,node):
        if self.isAtom(node) and not isinstance(node,int):
            return True
        else:
            return False

    def findAtom (self,str):
        if isinstance(str,int) or str.isnumeric():
            return int(str)
        else:
            for atom in self.symbolList:
                if atom == str:
                    return atom
            self.symbolList.append(str)
            return self.symbolList[-1]


    def read(self,tokenList):
        self.tokens = tokenList
        self.cursor = 0
        try:
            self.exp = self.input()
            if not self.cursor == len(tokenList):
                raise LispSyntaxError("Unnecessary tokens after Ending")
            self.evaluate()
            self.output()
        except LispSyntaxError as e:
            print (">>>Error: " +str(e.args))

    def isAtom(self,token):
        if token!='$' and token!='(' and token!=')' and token!='.' and not isinstance(token,tree):
            return True
        else:
            return False

    def null(self,exp):
        if exp=='NIL':
            return True
        else:
            return False
    
    def isList(self,exp):
        if not isinstance(exp,tree):
            return False
        while isinstance(exp.right,tree):
            exp = exp.right
        if exp.right != 'NIL':
            return False
        return True

    def evaluate(self):
        if self.isList(self.exp) and self.exp.left == 'DEFUN':
            self.exp = self.defun(self.exp.right)
        else:
            self.exp = self.eval(self.exp,[])

    def eval(self,exp,aList):
        if self.isAtom(exp):
            if not self.isSymbolic(exp):
                return exp
            elif exp == 'NIL':
                return False
            elif exp == 'T':
                return True
            else:
                for pair in aList:
                    if pair[0]==exp:
                        return pair[1]
                raise LispSyntaxError("Unbounded Symbolic Atom")
        elif self.isAtom(exp.left):
            if exp.left == 'QUOTE':
                return exp.right.left
            elif exp.left == 'COND':
                return self.evcon(exp.right,aList)
            elif self.isList(exp):
                return self.apply(exp.left,self.evlis(exp.right,aList),aList)
            else:
                raise LispSyntaxError("Illegal Lisp Expression")
        else:
            raise LispSyntaxError("Illegal Lisp Expression")
        
    def evlis(self,exp,aList):
        if self.null(exp):
            return "NIL"
        else:
            return tree(self.eval(exp.left,aList),self.evlis(exp.right,aList))

    def evcon(self,exp,aList):
        if self.null(exp):
            raise LispSyntaxError("COND End without True Condition")
        elif self.eval(exp.left.left,aList):
            return self.eval(exp.left.right.left,aList)
        else:
            return self.evcon(exp.right,aList)


    def apply(self,f,x,aList):
        if f == 'CAR':
            return x.left.left
        elif f == 'CDR':
            return x.left.right
        elif f == 'CONS':
            return tree(x.left,x.right.left) # check here
        elif f == 'ATOM':
            return self.isAtom(x.left)
        elif f == 'NULL':
            return self.null(x.left)
        elif f == "EQ":
            return x.left == x.right.left
        elif f == 'INT':
            return isinstance(x.left,int)
        elif f == 'PLUS':
            return x.left + x.right.left
        elif f == 'MINUS':
            return x.left - x.right.left
        elif f == 'QUOTIENT':
            return int(x.left / x.right.left)
        elif f == 'TIMES':
            return x.left * x.right.left
        elif f == 'REMAINDER':
            return x.left % x.right.left
        elif f == 'LESS':
            return x.left < x.right.left
        elif f == 'GREATER':
            return x.left > x.right.left
        else:
            try:
                pList = self.dList[f][0]
                while True:
                    aList.insert(0,[pList.left,x.left])
                    if pList.right == 'NIL':
                        if x.right!= 'NIL':
                            raise  LispSyntaxError('Wrong number of parameters')
                        break
                    pList = pList.right
                    x = x.right
                return self.eval(self.dList[f][1],aList)
            except AttributeError:
                raise LispSyntaxError("Wrong number of parameters")
            except KeyError:
                raise LispSyntaxError("Undefined function")
    
    def defun(self,exp):
        try:
            if not self.isAtom(exp.left.left):
                raise LispSyntaxError("Illegal function name")
            if not self.isList(exp.left.right):
                raise LispSyntaxError("Illegal parameter list")
            else:
                self.dList[exp.left.left] = [exp.left.right.left,exp.right.left]
                return exp.left.left
        except AttributeError:
            raise LispSyntaxError("Illegal function definition")


    def inputList(self):
        if self.tokens[self.cursor] == ")":
            self.cursor= self.cursor+1
            temp = self.findAtom('NIL')
            return temp
        else:
            temp = tree(left = self.input())
            tempR = self.inputList()
            temp.right = tempR
            return temp
    
   
    def output(self):
        print(">>>Output: ",self.exp )
        
    
    def input(self):
        if self.cursor >= len(self.tokens):
            raise LispSyntaxError("Early Ending Lisp-expression")
        elif self.isAtom(self.tokens[self.cursor]):
            temp = self.findAtom(self.tokens[self.cursor])
            self.cursor = self.cursor+1
            return temp
        elif self.tokens[self.cursor]=='(':
            self.cursor=self.cursor+1
            if self.tokens[self.cursor] == ')':
                self.cursor=self.cursor+1
                return self.findAtom('NIL')
            temp = tree(left=self.input())
            if self.cursor >= len(self.tokens):
                raise LispSyntaxError("Early Ending Lisp-expression")
            elif self.tokens[self.cursor] == '.':
                self.cursor= self.cursor+1
                temp.right = self.input()
                if self.cursor >= len(self.tokens):
                    raise LispSyntaxError("Early Ending Lisp-expression")
                elif self.tokens[self.cursor]!=")":
                    raise LispSyntaxError("Expected ')' but receive other tokens")
                else:
                    self.cursor= self.cursor+1
                    return temp
            else:
                temp.right = self.inputList()
            return temp
        elif self.tokens[self.cursor]=='.':
            raise LispSyntaxError("Unexpected Dot")
        elif self.tokens[self.cursor]==')':
            raise LispSyntaxError("Unexpected Right Parentheses")



    
            

    

class tree:
    '''
    Data structure for s-exp
    '''
    def __init__(self, left = None, right = None):
        self.left = left
        self.right = right
    
    def __str__(self):
        return '('+str(self.left)+'.'+str(self.right)+')'
        

def main():
    tokens = []
    sign = 0
    errorSign = False
    lastSign = ''
    myLisp = Lisp(tokens)
    for tokenType,t,_,_,_ in tokenize(sys.stdin.buffer.readline):
        '''
        Change the behavior of tokenizer in python to only feed Lisp good tokens
        '''
        try:
            if errorSign == True:
                if t == "$":
                    errorSign = False
                    continue
                else:
                    continue

            
            if tokenType == 59:
                #skip encoding
                pass
            
            elif tokenType==token.NEWLINE or tokenType==58 or tokenType ==token.INDENT or \
                t == ' ' or t=='\n' or t == '\r\n' or t =='\r'  or tokenType ==token.DEDENT:
                t= ' '
            
            elif t == '+' or t == '-':
                #set sign is token is operater
                if t == '-':
                    sign = -1
                else :
                    sign = 1

            
            elif t == '$':
                #send tokens to the lisp interpreter when the token is $
                if lastSign == '$':
                    break
                elif lastSign == ' ':
                    myLisp.read(tokens)
                    tokens = []
                else:
                    raise InvalidCharacter("Unexpected dollar")
            
            
            elif tokenType == 1:
                #if the token is symbolic
                if not t.isupper():
                    raise InvalidCharacter("Only Accept Uppercase Identifier")
                elif len(t)>10:
                    raise InvalidCharacter("Identifier Name too Long")
                elif isinstance(lastSign,int) or lastSign.isnumeric() :
                    raise InvalidCharacter("Identifier Start with number")
                else:
                    tokens.append(t)

            
            elif tokenType == 2:
                #if the token is numberic
                if t.find('.')>=0:
                    ind = t.find('.') 
                    t1 = t[:ind]
                    t2 = t[ind+1:]
                    
                    if len(t1)>6:
                        raise InvalidCharacter("Number too Large") 
                    elif t1 == '':
                        # case .123
                        if not sign == 0:
                            # case +.123
                            raise InvalidCharacter("Invalid use of - or +")
                    else:
                        # normal
                        t1 = int (t1)
                        if not sign == 0:
                            # case +123
                            t1 = sign * int(t1)
                            sign = 0
                        tokens.append(t1)

                    tokens.append('.')

                    if len(t2)>6:
                        raise InvalidCharacter("Number too Large") 
                    elif not t2 == '':
                        t2 = int(t2)
                        tokens.append(t2)
                else:
                    t = int(t)
                    tokens.append(t)

            #just push other possible tokens
            elif t=='(' or t == ')' or t == '.':
                tokens.append(t)

            #Bad tokens
            else:
                raise InvalidCharacter("Character(s) not allowed in LISP")
        
            lastSign = t
            
        except InvalidCharacter as e:
            print (">>>Error: " + str(e.args))
            tokens = []
            errorSign = True


   

if __name__ == "__main__":
    main()


# Lines for test python tokenize in terminal

# from tokenize import tokenize
# import sys
# for line in tokenize(sys.stdin.buffer.readline):
#     print(line)