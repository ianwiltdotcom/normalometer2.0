import storage
import os

def unlock():
    storage.remount("/", False)

def lock():
    storage.remount("/", True)

def saveFile(data, mode):
    unlock()
    fileIndex = 0
    fileName = "/records/record{}.csv"
    newFile = False
    while (not newFile):
        try:
            os.stat(fileName.format(fileIndex))
            fileIndex += 1
        except:
            newFile = True
    try: #will fail if /records/ doesn't exist
        file = open(fileName.format(fileIndex), "wt")
    except:
        os.mkdir("records")
        file = open(fileName.format(fileIndex), "wt")

    #file = open("records/recordtest.csv", "wt")
    file.write("Time")
    numCols = 1
    if (mode & 1):
        file.write(",X")
        numCols += 1
    if (mode & 2):
        file.write(",Y")
        numCols += 1
    if (mode & 4):
        file.write(",Z")
        numCols += 1

    for i in range(len(data)):
        if (i % numCols == 0):
            file.write("\n")
        file.write(str(data[i]) + ",")

    file.close()
    lock()
    return fileIndex