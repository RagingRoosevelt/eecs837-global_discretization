import random
from utility import *

###############################################################################
# class for storing (attribute, value) pairs and the (decision, concept) pair #
###############################################################################
class entry():
    def __init__(self, attributes, decision):
        self.A = {}
        for i in range(0,len(attributes)):
            self.A[i] = attributes[i]
        self.D = decision


############################################################
# function to parse file and extract (a,v) and (d,v) pairs #
############################################################
def parsefile(file):
    entries = {}
    i = 0
    attributes = []
    attribute_values = []
    decision = ""
    decision_value = ""
    for line in file:
        line = line.split()
        if line == []:
            continue
        elif (line[0] == "<") or (line[0] == "!"):
            continue
        elif (line[0] == "["):
            attributes = line[1:-2]
            decision = line[-2]
            #print("found the attribute names: " + str(attributes))
            #print("found the decision name: " + str(decision))
        else:
            attribute_values = [float(x) for x in line[0:-1]]
            decision_value = line[-1]
            #print(str(attribute_values) + " " + str(decision_value))
            
            entries[i] = entry(attribute_values, decision_value)
            i += 1
        
    return entries


############################################################
# function to parse file and extract (a,v) and (d,v) pairs #
############################################################
def parsefile2(file):
    got_attributes = 0
    attributes = []
    attribute_values = []
    i = 0
    decision = ""
    decision_value = ""
    entries = {}
    for line in file:
        line = line.split()
        if line == []: # empty line
            continue
        elif (line[0] == "<") or (line[0] == "!"): # comment or first line
            continue
        elif line[0] == '[': # start of attribute list
            if line[-1] == ']': # attribute list also ends on this line
                attributes = line[1:-2]
                decision = line[-2]
                got_attributes = 2
            else: # attribute list doesn't end on this line
                got_attributes = 1
                attributes = line[1:-1]
        else:
            if got_attributes == 1: # reading attributes still
                if line[-1] == ']': # attribute list ends on this line
                    attributes = line[0:-2]
                    decision = line[-2]
                    got_attributes = 2
                else: # attribute list doesn't end on this line
                    attributes = line[0:-1]
            elif got_attributes == 2: # done reading attributes
                attribute_values = [float(x) for x in line[0:-1]]
                decision_value = line[-1]
                #print(str(attribute_values) + " " + str(decision_value))
                
                entries[i] = entry(attribute_values, decision_value)
                i += 1
                    
                    
        
    return entries


################################################
# function to partition a set based on concept #
################################################
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

##################################################
# function to partition a set based on attribute #
##################################################
def partitionAttribute(entries,Attribute):
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

################################################################
# function to check consistency between attribute and decision # 
################################################################
def isconsistant(entries):
    print("coming soon")


###################
# Begin execution #
###################
def main():
    # generate random LERS file
    if True == True:
        randomLERS(30)

    # read and parse LERS file
    if True == True:    
        file = openfile("jerzy5.txt")
        entries = parsefile2(file)

        for i in range(0,len(entries)):
            print(str(i) + ": " + str(entries[i].A) + ", " + str(entries[i].D))

        # Partition based on decision
        Dpart = partitionD(entries)
main()