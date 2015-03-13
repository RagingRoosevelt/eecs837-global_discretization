def get_user_input(message):
    try:
        # python 2.x function
        user_input = raw_input(message)
    except:
        # python 3.x function
        user_input = input(message)
    return user_input

def readfile():

    # Get filename from user
    user_input = get_user_input("Filename? ")
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
    
def isconsistant(entries):
    for entry in entries:
        
      
class entry():
    # class for storing (attribute, value) pairs and the (decision, concept) pair
    def __init__(self, **attr):
        for key in attr:
            setattr(self, key, attr[key])



#file = readfile()
entries = {}
entries[0] = entry(height=12123.1, weight=1, noise=122, price="vhasdf")
entries[1] = entry(height=123.1, weight=12312.12312, noise=12312, price="vh")

print(entries[0].price)
