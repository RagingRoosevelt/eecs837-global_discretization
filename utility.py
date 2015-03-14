# function to get user input regardless of python version
def get_user_input(message):
    try:
        # python 2.x function
        user_input = raw_input(message)
    except:
        # python 3.x function
        user_input = input(message)
    return user_input


# function to get filename from user (if none specified) and then open a file
def openfile(path=""):
    if path == "":
        # Get filename from user
        user_input = get_user_input("Filename? ")
    else:
        user_input = path

    
    while True:
        try:
            # try to open file
            file = open(user_input)
            break
        except:
            # if file doesn't open, re-prompt for filename and try to open again
            print("\nerror: File not found")
            user_input = get_user_input("Filename? ")
            
    return file


