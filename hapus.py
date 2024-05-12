import subprocess
from random import randint
import sys

variables = {}
functions = {}
running_while = {"Trueorfalse": False}

def debugtokens(code):
    linenum = 0
    lines = code.split("\n")

    for line in lines:
        tokens = line.split() or line.split("\t")

        if tokens:
            print("tokens:", tokens, "line:", linenum, "\n")
            linenum += 1

def funcinterpret(code):
    lines = code.split("\n")
    in_if = False
    tokenlist = []

    for line in lines:
        tokens = line.split() or line.split("\t")

        if tokens:
            token = tokens[0]

            if in_if == False:
                if token == "talk" and tokens[1] == ">>":
                    msg = tokens[2:]
                    print(" ".join(msg))
                elif token == "talkvar" and tokens[1] == ">>":
                    varname = tokens[2]
                    print(variables.get(tokens[2]))
                elif token == "int":
                    varname = tokens[1]
                    if tokens[2] == "=":
                        value = tokens[3]
                        variables[varname] = int(value)
                    else:
                        print("invalid token: " + tokens[2])
                elif token == "string":
                    varname = tokens[1]
                    if tokens[2] == "=":
                        tokensize = tokens[3]
                        finaltokensize = int(tokensize) + 5
                        if tokens[4] == "\"":
                            string = tokens[5:finaltokensize]
                            if tokens[finaltokensize] == "\"":
                                value = " ".join(string)
                                variables[varname] = value
                            else:
                                print("String not closed, invalid token: " + tokens[finaltokensize])
                        else:
                            print("invalid token to open string: " + tokens[4])
                    else:
                        print("invalid token: " + tokens[2])
                elif token == "" or token.startswith(" ") or token.startswith("\t") or token.startswith("\n") or token.startswith("//"):
                    continue
                elif token == "callfunc" and tokens[1] == "(" and tokens[3] == ")":
                    funcname = tokens[2]
                    for func in functions:
                        if funcname == func:
                            funcinterpret("\n".join(functions[funcname]))
                elif token == "if":
                    for var in variables:
                        if tokens[1] == var:
                            for var2 in variables:
                                if tokens[3] == var2:
                                    if tokens[4] == "{":
                                        in_if = True
                                        tokenlist = []
                                        conditiontype = tokens[2]
                                        varname1 = tokens[1]
                                        varname2 = tokens[3]
                elif token == "input":
                    varname = tokens[1]
                    if tokens[2] == "=":
                        tokensize = tokens[3]
                        finaltokensize = int(tokensize) + 5
                        if tokens[4] == "\"":
                            string = tokens[5:finaltokensize]
                            if tokens[finaltokensize] == "\"":
                                value = " ".join(string)
                                variables[varname] = input(value)
                            else:
                                print("String not closed, invalid token: " + tokens[finaltokensize])
                                break
                        else:
                            print("invalid token to open string: " + tokens[4])
                            break
                    else:
                        print("invalid token: " + tokens[2])
                        break
                elif token == "stop":
                    running_while["Trueorfalse"] = False
                elif token == "randnum":
                    if tokens[1] == ">":
                        varname = tokens[2]
                        if tokens[3] == "<":
                            if tokens[4] == ">":
                                firstnum = tokens[5]
                                if tokens[6] == ",":
                                    lastnum = tokens[7]
                                    if tokens[8] == "<":
                                        variables[varname] = randint(int(firstnum), int(lastnum))
                                    else:
                                        print("invalid token to close code: " + tokens[8])
                                else:
                                    print("invalid token to separate numbers: " + token[6])
                            else:
                                print("invalid token to start code: " + token[4])
                        else:
                            print("invalid token to end set the variable name: " + token[3])
                    else:
                        print("invalid token to start set the variable name: " + token[1])
                elif token == "floating":
                    varname = tokens[1]
                    if tokens[2] == "=":
                        value = tokens[3]
                        variables[varname] = float(value)
                    else:
                        print("invalid token: " + tokens[2])
                        break
                elif token == "realcmd":
                    cmd = tokens[1]
                    if cmd == "normal":
                        finalcmd = " ".join(tokens[2:])
                        subprocess.run(finalcmd, shell=True)
                    else:
                        finalcmd = variables.get(cmd)
                        subprocess.run(finalcmd, shell=True)
                elif token == "splitspaces":
                    varname = tokens[1]
                    keywordname = tokens[2]
                    verifypart = tokens[3]
                    funcname = tokens[4]
                    splitedvalue = variables.get(varname).split() 
                    if splitedvalue[int(verifypart)] == keywordname:
                        funcinterpret("\n".join(functions.get(funcname)))
                elif token == "joinvar":
                    content = []
                    varname1 = tokens[1]
                    content.append(variables.get(varname1))
                    if tokens[2] == ":":
                        varname2 = tokens[3]
                        content.append(variables.get(varname2))
                        value = " ".join(content)
                        if tokens[4] == ">>":
                            varname = tokens[5]
                            variables[varname] = value
                elif token == "modifyintnum":   
                    varname1 = tokens[1]
                    if tokens[2] == "<":
                        num = tokens[3]         
                        if num == "normal":
                            variables[varname1] += int(tokens[4])
                        else:        
                            varname2 = num
                            variables[varname1] += variables.get(varname2)
                    else:   
                        print("invalid token to separate the variables name: " + token[2])
                elif token == "modifyfloatnum":   
                    varname1 = tokens[1]
                    if tokens[2] == "<":
                        num = tokens[3]         
                        if num == "normal":
                            variables[varname1] += float(tokens[4])
                        else:
                            varname2 = num
                            variables[varname1] += variables.get(varname2)
                    else:
                        print("invalid token to separate the variables name: " + token[2])
                elif token == "splitlines":
                    varname1 = tokens[1]
                    varname2 = tokens[2]
                    splitedvalue = variables.get(varname).split("\n") 
                    variables[varname2] = splitedvalue
                elif token == "intinput":
                    varname = tokens[1]
                    if tokens[2] == "=":
                        tokensize = tokens[3]
                        finaltokensize = int(tokensize) + 5
                        if tokens[4] == "\"":
                            string = tokens[5:finaltokensize]
                            if tokens[finaltokensize] == "\"":
                                value = " ".join(string)
                                variables[varname] = int(input(value))
                            else:
                                print("String not closed, invalid token: " + tokens[finaltokensize])
                                break
                        else:
                            print("invalid token to open string: " + tokens[4])
                            break
                    else:
                        print("invalid token: " + tokens[2])
                        break
                elif token == "floatinput":
                    varname = tokens[1]
                    if tokens[2] == "=":
                        tokensize = tokens[3]
                        finaltokensize = int(tokensize) + 5
                        if tokens[4] == "\"":
                            string = tokens[5:finaltokensize]
                            if tokens[finaltokensize] == "\"":
                                value = " ".join(string)
                                variables[varname] = int(input(value))
                            else:
                                print("String not closed, invalid token: " + tokens[finaltokensize])
                                break
                        else:
                            print("invalid token to open string: " + tokens[4])
                            break
                    else:
                        print("invalid token: " + tokens[2])
                        break
                elif token == "readfile":
                    file = tokens[1]
                    if tokens[2] == ">>":
                        varname = tokens[3]
                        with open(file, "r") as fi:
                            content = fi.read()
                        variables[varname] = content
                elif token == "writefile":
                    file = tokens[1]
                    if tokens[2] == "<<":
                        varname = tokens[3]
                        with open(file, "w") as fi:
                            content = variables.get(varname)
                            fi.write(content)
                elif token == "appendfile":
                    file = tokens[1]
                    if tokens[2] == "<<":
                        varname = tokens[3]
                        with open(file, "a") as fi:
                            content = variables.get(varname)
                            fi.write(content)
                elif token == "strlist":
                    varname = tokens[1]
                    if tokens[2] == "=":
                        items = tokens[3:]
                        variables[varname] = items
                elif token == "intlist":
                    varname = tokens[1]
                    if tokens[2] == "=":
                        items = tokens[3:]
                        variables[varname] = int(items)
                elif token == "floatlist":
                    varname = tokens[1]
                    if tokens[2] == "=":
                        items = tokens[3:]
                        variables[varname] = float(items)
                elif token == "getlistitem":
                    listvarname = tokens[1]
                    if tokens[2] == ":":
                        listnum = tokens[3]
                        if tokens[4] == ">>":
                            outputvarname = tokens[5]
                            variables[outputvarname] = variables.get(listvarname[int(listnum)])

            if in_if:
                if token == "}" and tokens[1] == "if":
                    in_if = False
                    linne = "\n".join(tokenlist)
                    if conditiontype == "==":
                        if variables.get(varname1) == variables.get(varname2):
                            funcinterpret(linne)
                    elif conditiontype == "!!":
                        if variables.get(varname1) != variables.get(varname2):
                            funcinterpret(linne)
                    elif conditiontype == "<=":
                        if variables.get(varname1) <= variables.get(varname2):
                            funcinterpret(linne)
                    elif conditiontype == ">=":
                        if variables.get(varname1) >= variables.get(varname2):
                            funcinterpret(linne)
                    elif conditiontype == ">>":
                        if variables.get(varname1) > variables.get(varname2):
                            funcinterpret(linne)
                    elif conditiontype == "<<":
                        if variables.get(varname1) < variables.get(varname2):
                            funcinterpret(linne)
                    elif conditiontype == "startswith":
                        if variables.get(varname1).startswith(varname2):
                            funcinterpret(linne)
                elif token == "if" and tokens[4] == "{":
                    conditiontype = tokens[2]
                    varname1 = tokens[1]
                    varname2 = tokens[3]
                else:
                    tokenlist.append(" ".join(tokens[0:]))

def interpret(code):
    lines = code.split("\n")
    in_main_func = False
    in_normal_func = False
    in_if = False
    in_while = False
    conditiontype = ""
    varname1 = ""
    varname2 = ""
    tokenlist = []

    for line in lines:
        tokens = line.split() or line.split("\t")

        if tokens:
            token = tokens[0]

            if token == "use" and tokens[1] == "main" and tokens[2] == "{":
                in_main_func = True
                continue
            elif token == "func":
                funcname = tokens[1]
                if tokens[2] == "{":
                    functions[funcname] = []
                    in_normal_func = True
                    tokenlist = []
            elif token == "imp":
                file = tokens[1]
                with open(file + ".hap", "r") as fi:
                    content = fi.read()
                interpret(content)
            
            if in_normal_func:
                if token == "}" and tokens[1] == "func":
                    funcname = tokens[2]
                    in_normal_func = False
                    linne = "\n".join(tokenlist)
                    functions[funcname].append(linne)
                else:
                    tokenlist.append(" ".join(tokens[0:]))
            
            if in_main_func:
                if token == "talk" and tokens[1] == ">>":
                    msg = tokens[2:]
                    print(" ".join(msg))
                elif token == "talkvar" and tokens[1] == ">>":
                    varname = tokens[2]
                    print(variables.get(tokens[2]))
                elif token == "int":
                    varname = tokens[1]
                    if tokens[2] == "=":
                        value = tokens[3]
                        variables[varname] = int(value)
                    else:
                        print("invalid token: " + tokens[2])
                        break
                elif token == "string":
                    varname = tokens[1]
                    if tokens[2] == "=":
                        tokensize = tokens[3]
                        finaltokensize = int(tokensize) + 5
                        if tokens[4] == "\"":
                            string = tokens[5:finaltokensize]
                            if tokens[finaltokensize] == "\"":
                                value = " ".join(string)
                                variables[varname] = value
                            else:
                                print("String not closed, invalid token: " + tokens[finaltokensize])
                                break
                        else:
                            print("invalid token to open string: " + tokens[4])
                            break
                    else:
                        print("invalid token: " + tokens[2])
                        break
                elif token == "input":
                    varname = tokens[1]
                    if tokens[2] == "=":
                        tokensize = tokens[3]
                        finaltokensize = int(tokensize) + 5
                        if tokens[4] == "\"":
                            string = tokens[5:finaltokensize]
                            if tokens[finaltokensize] == "\"":
                                value = " ".join(string)
                                variables[varname] = input(value)
                            else:
                                print("String not closed, invalid token: " + tokens[finaltokensize])
                                break
                        else:
                            print("invalid token to open string: " + tokens[4])
                            break
                    else:
                        print("invalid token: " + tokens[2])
                        break
                elif token == "}" and tokens[1] == "main":
                    in_main_func = False
                elif token == "" or token.startswith(" ") or token.startswith("\t") or token.startswith("\n") or token.startswith("//"):
                    continue
                elif token == "callfunc" and tokens[1] == "(" and tokens[3] == ")":
                    funcname = tokens[2]
                    for func in functions:
                        if funcname == func:
                            funcinterpret("\n".join(functions[funcname]))
                elif token == "if":
                    for var in variables:
                        if tokens[1] == var:
                            for var2 in variables:
                                if tokens[3] == var2:
                                    if tokens[4] == "{":
                                        in_if = True
                                        in_main_func = False
                                        tokenlist = []
                                        conditiontype = tokens[2]
                                        varname1 = tokens[1]
                                        varname2 = tokens[3]
                elif token == "while":
                    if tokens[1] == "{":
                        in_while = True
                        running_while["Trueorfalse"] = True
                        in_main_func = False
                        tokenlist = []
                elif token == "realcmd":
                    cmd = tokens[1]
                    if cmd == "normal":
                        finalcmd = " ".join(tokens[2:])
                        subprocess.run(finalcmd, shell=True)
                    else:
                        finalcmd = variables.get(cmd)
                        subprocess.run(finalcmd, shell=True)
                elif token == "randnum":
                    if tokens[1] == ">":
                        varname = tokens[2]
                        if tokens[3] == "<":
                            if tokens[4] == ">":
                                firstnum = tokens[5]
                                if tokens[6] == ",":
                                    lastnum = tokens[7]
                                    if tokens[8] == "<":
                                        variables[varname] = randint(int(firstnum), int(lastnum))
                                    else:
                                        print("invalid token to close code: " + tokens[8])
                                else:
                                    print("invalid token to separate numbers: " + token[6])
                            else:
                                print("invalid token to start code: " + token[4])
                        else:
                            print("invalid token to end set the variable name: " + token[3])
                    else:
                        print("invalid token to start set the variable name: " + token[1])
                elif token == "floating":
                    varname = tokens[1]
                    if tokens[2] == "=":
                        value = tokens[3]
                        variables[varname] = float(value)
                    else:
                        print("invalid token: " + tokens[2])
                        break
                elif token == "splitspaces":
                    varname = tokens[1]
                    keywordname = tokens[2]
                    verifypart = tokens[3]
                    funcname = tokens[4]
                    splitedvalue = variables.get(varname).split() 
                    if splitedvalue[int(verifypart)] == keywordname:
                        funcinterpret("\n".join(functions.get(funcname)))
                elif token == "joinvar":
                    content = []
                    varname1 = tokens[1]
                    content.append(variables.get(varname1))
                    if tokens[2] == ":":
                        varname2 = tokens[3]
                        content.append(variables.get(varname2))
                        value = " ".join(content)
                        if tokens[4] == ">>":
                            varname = tokens[5]
                            variables[varname] = value
                elif token == "modifyintnum":   
                    varname1 = tokens[1]
                    if tokens[2] == "<":
                        num = tokens[3]         
                        if num == "normal":
                            variables[varname1] += int(tokens[4])
                        else:
                            varname2 = num
                            variables[varname1] += variables.get(varname2)
                    else:
                        print("invalid token to separate the variables name: " + token[2])
                elif token == "modifyfloatnum":   
                    varname1 = tokens[1]
                    if tokens[2] == "<":
                        num = tokens[3]         
                        if num == "normal":
                            variables[varname1] += float(tokens[4])
                        else:
                            varname2 = num
                            variables[varname1] += variables.get(varname2)
                    else:
                        print("invalid token to separate the variables name: " + token[2])
                elif token == "splitlines":
                    varname1 = tokens[1]
                    varname2 = tokens[2]
                    splitedvalue = variables.get(varname).split("\n") 
                    variables[varname2] = splitedvalue
                elif token == "intinput":
                    varname = tokens[1]
                    if tokens[2] == "=":
                        tokensize = tokens[3]
                        finaltokensize = int(tokensize) + 5
                        if tokens[4] == "\"":
                            string = tokens[5:finaltokensize]
                            if tokens[finaltokensize] == "\"":
                                value = " ".join(string)
                                variables[varname] = int(input(value))
                            else:
                                print("String not closed, invalid token: " + tokens[finaltokensize])
                                break
                        else:
                            print("invalid token to open string: " + tokens[4])
                            break
                    else:
                        print("invalid token: " + tokens[2])
                        break
                elif token == "floatinput":
                    varname = tokens[1]
                    if tokens[2] == "=":
                        tokensize = tokens[3]
                        finaltokensize = int(tokensize) + 5
                        if tokens[4] == "\"":
                            string = tokens[5:finaltokensize]
                            if tokens[finaltokensize] == "\"":
                                value = " ".join(string)
                                variables[varname] = int(input(value))
                            else:
                                print("String not closed, invalid token: " + tokens[finaltokensize])
                                break
                        else:
                            print("invalid token to open string: " + tokens[4])
                            break
                    else:
                        print("invalid token: " + tokens[2])
                        break
                elif token == "readfile":
                    file = tokens[1]
                    if tokens[2] == ">>":
                        varname = tokens[3]
                        with open(file, "r") as fi:
                            content = fi.read()
                        variables[varname] = content
                elif token == "writefile":
                    file = tokens[1]
                    if tokens[2] == "<<":
                        varname = tokens[3]
                        with open(file, "w") as fi:
                            content = variables.get(varname)
                            fi.write(content)
                elif token == "appendfile":
                    file = tokens[1]
                    if tokens[2] == "<<":
                        varname = tokens[3]
                        with open(file, "a") as fi:
                            content = variables.get(varname)
                            fi.write(content)
                elif token == "strlist":
                    varname = tokens[1]
                    if tokens[2] == "=":
                        items = tokens[3:]
                        variables[varname] = items
                elif token == "intlist":
                    varname = tokens[1]
                    if tokens[2] == "=":
                        items = tokens[3:]
                        variables[varname] = int(items)
                elif token == "floatlist":
                    varname = tokens[1]
                    if tokens[2] == "=":
                        items = tokens[3:]
                        variables[varname] = float(items)
                elif token == "getlistitem":
                    listvarname = tokens[1]
                    if tokens[2] == ":":
                        listnum = tokens[3]
                        if tokens[4] == ">>":
                            outputvarname = tokens[5]
                            variables[outputvarname] = variables.get(listvarname[int(listnum)])
                else:
                    print("main function not closed!")
                    break
            
            if in_if:
                if token == "}" and tokens[1] == "if":
                    in_if = False
                    in_main_func = True
                    linne = "\n".join(tokenlist)
                    if conditiontype == "==":
                        if variables.get(varname1) == variables.get(varname2):
                            funcinterpret(linne)
                    elif conditiontype == "!!":
                        if variables.get(varname1) != variables.get(varname2):
                            funcinterpret(linne)
                    elif conditiontype == "<=":
                        if variables.get(varname1) <= variables.get(varname2):
                            funcinterpret(linne)
                    elif conditiontype == ">=":
                        if variables.get(varname1) >= variables.get(varname2):
                            funcinterpret(linne)
                    elif conditiontype == ">>":
                        if variables.get(varname1) > variables.get(varname2):
                            funcinterpret(linne)
                    elif conditiontype == "<<":
                        if variables.get(varname1) < variables.get(varname2):
                            funcinterpret(linne)
                    elif conditiontype == "startswith":
                        if variables.get(varname1).startswith(varname2):
                            funcinterpret(linne)
                elif token == "if" and tokens[4] == "{":
                    conditiontype = tokens[2]
                    varname1 = tokens[1]
                    varname2 = tokens[3]
                else:
                    tokenlist.append(" ".join(tokens[0:]))

            if in_while:
                if token == "}" and tokens[1] == "while":
                    in_while = False
                    linne = "\n".join(tokenlist)
                    while running_while["Trueorfalse"]:
                        funcinterpret(linne)
                    in_main_func = True
                    
                elif token == "while" and tokens[1] == "{":
                    continue
                else:
                    tokenlist.append(" ".join(tokens[0:]))

def execute_file(filename):
    if filename.endswith(".hap"):
        with open(filename, "r") as f:
            content = f.read()
        interpret(content)
    else:
        print("use a .hap file extension")

def debug_file(filename):
    if filename.endswith(".hap"):
        with open(filename, "r") as f:
            content = f.read()
        debugtokens(content)
    else:
        print("use a .hap file extension")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f"usage: {sys.argv[0]} <cmd>")
        print("commands:")
        print("-v               version of the language")
        print("-i               interactive mode")
        print("-t <file>    debug the tokens")
        print("<file>           executes your file")
        sys.exit()

    command = sys.argv[1]

    if command == "-v":
        print("Hapus version: 1.5")
    elif command == "-i":
        running_while = True
        print("'stop' to stop the interactive mode")
        print("Hapus version 1.5")
        print("made by: josé icaro. with: python")
        while running_while:
            code = input(">> ")
            funcinterpret(code)
    elif command == "-t":
        file = sys.argv[2]
        debug_file(file)
    else:
        execute_file(command)
