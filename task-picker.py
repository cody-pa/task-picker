import os
import random

def parseFile(fileName, resultList, resultDict):
    entryName = ""
    leafFile = open(fileName, "r")
    line = leafFile.readline()
    while (line):
        if line.startswith("name: "):
            entryName = line.replace("name: ", "", 1).replace("\n", "")
        
        elif line.startswith("import: "):
            fname = line.replace("import: ", "", 1).replace("\n", "")
            if os.path.isfile(fname):
                if entryName == "":
                    entryName = parseFile(fname, resultList, resultDict)
                
                else:
                    parseFile(fname, resultList, resultDict)
                
            
            else:
                comb = os.path.dirname(fileName) + "/" + fname
                if os.path.isfile(comb):
                    if entryName == "":
                        entryName = parseFile(comb, resultList, resultDict)
                    
                    else:
                        parseFile(comb, resultList, resultDict)
                    
                
                else:
                    comb = fname.replace("$DATA", "./data")
                    if os.path.isfile(comb):
                        if entryName == "":
                            entryName = parseFile(comb, resultList, resultDict)
                        
                        else:
                            parseFile(comb, resultList, resultDict)
                        
                    
                    else:
                        print("Couldn't import %s" % fname)
                    
                
            
        
        else:
            if not line in resultDict:
                resultDict[line] = True
                resultList.append(line)
            
        
        line = leafFile.readline()
    
    return entryName	

def scan(fileName):
    entryName = ""
    single = False
    
    if os.path.isdir(fileName):
        show = True
        if os.path.isfile(fileName + "/_meta"):
            metaFile = open(fileName + "/_meta", "r")
            line = metaFile.readline()
            while(line):
                if line.startswith("name: "):
                    entryName = line.replace("name: ", "", 1).replace("\n", "")
                
                elif line.startswith("single: "):
                    if line.replace("single: ", "", 1).replace("\n", "") == "true":
                        single = True;
                    
                
                elif line.startswith("show: "):
                    if line.replace("show: ", "", 1).replace("\n", "") == "false":
                        show = False;
                    
                
                line = metaFile.readline()
            
        
        fileList = os.listdir(fileName)
        if single:
            chosenFile = "_meta" 
            while chosenFile == "_meta" or chosenFile.startswith("."):
                chosenFile = random.choice(fileList)
            
            value, name = scan(fileName + "/" + chosenFile)
            if name == "":
                name = chosenFile
            
            if entryName != "" and show:
                return "%s: %s\n%s" % (entryName, name, value), entryName
            
            else:
                return value, entryName
            
        
        else:
            bigstr = ""
            for filestr in fileList:
                if filestr != "_meta" and not filestr.startswith("."):
                    val, name = scan(fileName + "/" + filestr)
                    bigstr += val
                
            
            return bigstr, entryName
        
    
    else:
        resultList = []
        resultDict = {}
        entryName = parseFile(fileName, resultList, resultDict)
        resStr = random.choice(resultList)
        if entryName == "":
            entryName = fileName
        
        return "%s: %s" % (entryName, resStr), entryName
    

val, garbage = scan("./items")
print(val)


