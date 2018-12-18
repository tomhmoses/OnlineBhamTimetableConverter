import pickle

queueFilePath = "queue.pickle"

def main():
    queue = loadPickle(queueFilePath)
    for count in range(len(queue)):
        print(str(count) + ". " + queue[count][0])
        print("'" + queue[count][1] + "'")
    print(len(queue))

def removeDuplicates():
    queue = loadPickle(queueFilePath)
    newQueue = []
    for count in range(len(queue)):
        print(str(count) + ". " + queue[count][0])
        print("'" + queue[count][1] + "'")
        if queue[count][1].upper() not in str(newQueue).upper():
            newQueue.append(queue[count])
    print(len(queue))
    print()

    for count in range(len(newQueue)):
        print(str(count) + ". " + newQueue[count][0])
        print("'" + newQueue[count][1] + "'")
    print(len(newQueue))

    saveQueue(newQueue)
    print("saved")

def savePickle(file_name, obj):
    with open(file_name, 'wb') as fobj:
        pickle.dump(obj, fobj)

def loadPickle(file_name):
    with open(file_name, 'rb') as fobj:
        return pickle.load(fobj)

def saveQueue(queue):
    savePickle(queueFilePath,queue)


if __name__ == "__main__":
    main()
