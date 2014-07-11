def lookslike(mystr, listofstr):
    result = -1
    for another in listofstr:
        result = mystr.find(another)
        if result > -1:
            break
    return result