import random
from time import sleep

class entry():
    # class for storing (attribute, value) pairs and the (decision, concept) pair
    def __init__(self, attributes, decision):
        self.A = {}
        for i in range(0,len(attributes)):
            self.A[i] = attributes[i]
        self.D = decision


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
    
def getAttributes(entry):
    attributes = []
    for k,v in (entry.__dict__).items():
        attributes.append(k)
    decision = [attributes[-1]]
    del attributes[-1]
    return attributes,decision
    
def partitionD(entries):
    Dpart = [[0]]
    concepts = [entries[0].D]
    
    # Build partition identifiers
    for i in range(0, len(entries)):
        if not(entries[i].D in concepts):
            Dpart.append([i])
            concepts.append(entries[i].D)
            print(entries[i].D + " (" + str(i) + ") not found")
            
    # Finish populating partition
    for i in range(0, len(entries)):
        for j in range(0, len(Dpart)):
            if not(i in Dpart[j]) and (entries[i].D == concepts[j]):
                Dpart[j].append(i)
        
    print(Dpart)
    return Dpart
    

#def partitionAttribute(entries)
    
def isconsistant(entries):
# http://stackoverflow.com/a/3295662
    for entry in entries:
      print(entries[entry].weight)



#file = readfile()
entries = {}
for i in range(0,10):
    attributes = [random.randint(0, 10), random.randint(20,30), random.randint(40, 50)]
    
    temp = random.randint(0, 2)
    if temp == 0:
        decision = "low"
    elif temp == 1:
        decision = "med"
    else:
        decision = "high"
    entries[i] = entry(attributes, decision)


strng = ""
for i in range(0,len(entries)):
    strng += str(i) + ": " + entries[i].D + ",    "
    
print(strng)

Dpart = partitionD(entries)