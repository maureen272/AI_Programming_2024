# 파일 읽어오기
'''
def main():
    file = "FirstPresidents.txt"
    displayWithForLoop(file)
    print()
    displayWithListComprehension(file)
    print()
    displaywithReadline(file)

def displayWithForLoop(file):
    infile = open(file,'r')
    for line in infile:
        print(line.rstrip())
    infile.close()

def displayWithListComprehension(file):
    infile = open(file,'r')
    listPres = [line.rstrip() for line in infile]
    infile.close()
    print(listPres)

def displaywithReadline(file):
    infile = open(file,'r')
    line = infile.readline()
    while line != '':
        print(line.rstrip())
        line = infile.readline()
    infile.close()

main()
'''

#파일 생성하기
'''
def main():
    L = ["George Washington", "John Adams", "Thomas Jefferson"]
    outfile = open("FirstPresidents2.txt", 'w')
    createWithWrite(L,outfile)
    outfile = open("FirstPresidents3.txt", 'w')
    createWithWriteLines(L, outfile)

def createWithWrite(L,outfile):
    for i in range(len(L)):
        outfile.write(L[i]+'\n')
    outfile.close()

def createWithWriteLines(L, outfile):
    for i in range(len(L)):
        L[i] = L[i] + "\n"
    outfile.writelines(L)
    outfile.close()
main()
'''

'''
def main():
    statesList = createListFromFile("States.txt")
    createSortedFile(statesList, "StatesAlpha.txt")

def createListFromFile(fileName):
    infile = open(fileName, 'r')
    desiredList = [file.rstrip() for file in infile]
    infile.close()
    return desiredList

def createSortedFile(listName, fileName):
    listName.sort()
    for i in range(len(listName)):
        listName[i] = listName[i] + "\n"
    outfile = open(fileName, 'w')
    outfile.writelines(listName)
    outfile.close()

main()
'''

'''
def main():
    continent = input("Enter the name of continent: ")
    continent = continent.title()
    if continent != "Antarctica":
        infile = open("UN.txt", 'r')
        for line in infile:
            data = line.split(',')
            if data[1] == continent:
                print(data[0])
    else:
        print("There is no continent in Antarctica")
'''

import pickle

def main():
    nations = getDictionary("USpresStatesDict.dat")
    print(nations)
    #print("Enter the name of a continent", end = '')
    #continent = input("other than Antarctica: ")
    #continentDict = constructContinentNations(nations, continent)
    #displaySortedResults(continentDict)

def getDictionary(fileName):
    infile = open(fileName, 'rb')
    dictionary  = pickle.load(infile)
    infile.close()
    return dictionary