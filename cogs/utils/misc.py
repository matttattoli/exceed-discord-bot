limit = 20


def printOverLimit(message):
    message = str(message)
    if len(message) < limit:
        return message
    printMsg = []
    def cutitup(message):
        if len(message) < limit:
            printMsg.append(message)
            return message
        split = message[:limit - 1].rindex(' ')
        printMsg.append(message[:split])
        return cutitup(message[split:])

    cutitup(message)

    return printMsg