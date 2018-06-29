def printOverLimit(message):
    if len(str(message)) < 2000:
        return message
    printMsg = []
    message = str(message)
    for x in range(0, len(message), 1999):
        printMsg.append(message[x:x+1999])
    return printMsg
