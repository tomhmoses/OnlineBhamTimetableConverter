import pickle

queueFilePath = "queue.pickle"

def main():
    while True:
        choice = getMenuChoice()
        if choice == 0:
            view()
        elif choice == 1:
            removeDuplicates()
        elif choice == 2:
            viewWithShortTitle()
        elif choice == 3:
            changeOnToTrue()
        elif choice == 4:
            duplicateFirst()
        elif choice == 5:
            removeFirst()
        elif choice == 6:
            viewWithInfo()
        elif choice == 7:
            changeEmail()
        elif choice == 8:
            moveToFront()
        elif choice == 9:
            findUserPos()
        elif choice == 10:
            dupeAny()
        elif choice == 11:
            moveUsertoFront()

def getMenuChoice():
    choice = ""
    printMenu()
    menuItems = 12
    while choice not in range(menuItems):
        try:
            choice = int(input("Choice: "))
        except:
            None
        if choice not in range(menuItems):
            print("Invalid choice, try again...")
    return choice

def tester(input=None):
    if input: print (input)

def printMenu():
    menu = """\nView Queue Main menu:
    0. View queue normally
    1. Remove duplicates from the queue
    2. View with short title info
    3. Change on to True in shortTitle Boolean
    4. Duplicate first item
    5. Remove first item
    6. View All Queue info (-csv)
    7. Change email for a request
    8. Move somebody to front
    9. Find where somebody is in the queue
    10. Dupe any
    11. Move user to front\n"""
    print(menu)

def view():
    queue = loadPickle(queueFilePath)
    for count in range(len(queue)):
        print(str(count) + ". " + queue[count]["username"])
        print("'" + queue[count]["email"] + "'")
    print("\nLength: " + str(len(queue)))

def changeEmail():
    queue = loadPickle(queueFilePath)
    number = int(input("number: "))
    newEmail = input("new email: ")
    confirm = input("confirm email '" + newEmail + "' (Y/n): ").strip()
    if confirm == "Y":
        queue[number]["email"] = newEmail
        saveQueue(queue)
        print("changed")
    else:
        print("nothing changed")

def moveUsertoFront():
    queue = loadPickle(queueFilePath)
    toMove = None
    toFind = str(input("Enter the username to find: "))
    for count in range(len(queue)):
        if queue[count]["username"].lower() == toFind.lower():
            toMove = count
    if not toMove:
        print("coulnt find user")
    else:
        newQueue = []
        newQueue.append(queue[0])
        newQueue.append(queue[toMove])
        for count in range(1, len(queue)):
            if count != toMove:
                newQueue.append(queue[count])
        saveQueue(newQueue)


def findUserPos():
    queue = loadPickle(queueFilePath)
    toFind = str(input("Enter the username to find: "))
    for count in range(len(queue)):
        if queue[count]["username"].lower() == toFind.lower():
            print(count)

def viewWithInfo():
    queue = loadPickle(queueFilePath)
    for count in range(len(queue)):
        print(str(count) + ". " + queue[count]["username"])
        print(" "*(len(str(count))+2) + "'" + queue[count]["email"] + "'")
        print(" "*(len(str(count))+2) + str(queue[count]["shortenTitle"]))
        print(" "*(len(str(count))+2) + "'" + str(queue[count]["customTitle"])+ "'")
    print("\nLength: " + str(len(queue)))

def viewWithShortTitle():
    queue = loadPickle(queueFilePath)
    for count in range(len(queue)):
        print(str(count) + ". " + queue[count]["username"])
        print("'" + queue[count]["email"] + "'")
        print(queue[count]["shortenTitle"])
    print("\nLength: " + str(len(queue)))

def changeOnToTrue():
    queue = loadPickle(queueFilePath)
    for count in range(len(queue)):
        if queue[count]["shortenTitle"] == "on":
            queue[count]["shortenTitle"] = True
    saveQueue(queue)


def removeDuplicates():
    queue = loadPickle(queueFilePath)
    newQueue = []
    unique = []
    for count in range(len(queue)):
        print(str(count) + ". " + queue[count]["username"])
        print("'" + queue[count]["email"] + "'")
        if queue[count]["email"].lower() + " " + queue[count]["username"].lower() not in unique:
            newQueue.append(queue[count])
            unique.append(queue[count]["email"].lower() + " " + queue[count]["username"].lower())
    print(len(queue))
    print()

    for count in range(len(newQueue)):
        print(str(count) + ". " + newQueue[count]["username"])
        print("'" + newQueue[count]["email"] + "'")
    print(len(newQueue))

    saveQueue(newQueue)
    print("saved")

def removeFirst():
    queue = loadPickle(queueFilePath)
    newQueue = []
    for count in range(1, len(queue)):
        newQueue.append(queue[count])
    saveQueue(newQueue)

def moveToFront():
    toMove = int(input("Number to move (starting at 0): "))
    queue = loadPickle(queueFilePath)
    newQueue = []
    newQueue.append(queue[0])
    newQueue.append(queue[toMove])
    for count in range(1, len(queue)):
        if count != toMove:
            newQueue.append(queue[count])
    saveQueue(newQueue)

def duplicateFirst():
    queue = loadPickle(queueFilePath)
    newQueue = []
    newQueue.append(queue[0])
    for count in range(len(queue)):
        newQueue.append(queue[count])
    saveQueue(newQueue)

def dupeAny():
    queue = loadPickle(queueFilePath)
    toDupe = int(input("Number to duplicate (starting at 0): "))
    newQueue = []
    for count in range(len(queue)):
        newQueue.append(queue[count])
        if count == toDupe:
            newQueue.append(queue[count])
    saveQueue(newQueue)


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
