import random
from utility import *
import os
from math import log


#######################
# write Table to file #
#######################
def table2file(entries,attributes):
    file = open("output.txt",'w')
    
    file.write("[ ")
    for attr in attributes:
        file.write(str(attr) + " ")
    file.write("]\n")
    
    for entry in [entries[i] for i in entries]:
        for val in [entry.A[i] for i in entry.A]:
            file.write(" " + str(val))
        file.write("\t" + str(entry.D) + "\n")


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
            diag("found the attribute names: " + str(attributes))
            diag("found the decision name: " + str(decision))
        else:
            attribute_values = [float(x) for x in line[0:-1]]
            decision_value = line[-1]
            diag(str(attribute_values) + " " + str(decision_value))
            
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
                    
                    
        
    return (entries,attributes)


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
            #print(entries[i].D + " (" + str(i) + ") not found")
            
    # Finish populating partition
    for i in range(0, len(entries)):
        for j in range(0, len(Dpart)):
            if not(i in Dpart[j]) and (entries[i].D == concepts[j]):
                Dpart[j].append(i)
        
    #print(Dpart)
    return Dpart

##################################################
# function to partition a set based on attribute #
##################################################
def partitionAttribute(entries,Att):
    partition = [[0]]
    concepts = [entries[0].A[Att]]
    
    # Build partition identifiers
    for i in range(0, len(entries)):
        if not(entries[i].A[Att] in concepts):
            partition.append([i])
            concepts.append(entries[i].A[Att])
            #print(str(entries[i].A[Att]) + " (" + str(i) + ") not found")
            
    # Finish populating partition
    for i in range(0, len(entries)):
        for j in range(0, len(partition)):
            if not(i in partition[j]) and (entries[i].A[Att] == concepts[j]):
                partition[j].append(i)
        
    #print(partition)
    return partition

####################################################################
# function to compute the partition of several attributes together #
####################################################################
def partitionAttributes(part1,part2):
    part = []
    for elmnt1 in part1:
        for elmnt2 in part2:
            temp = list(set(elmnt1) & set(elmnt2))
            if not(temp == []):
                part.append(temp)
    return part
    
################################################################
# function to check consistency between attribute and decision # 
################################################################
def isconsistant(entries,num_attributes):
    partD = partitionD(entries)
    multipart = partitionAttribute(entries,0)
    for i in range(0,num_attributes):
        part = partitionAttribute(entries,i)
        multipart = partitionAttributes(part,multipart)
        
    diag("Decision partition  : " + str(partD))
    diag("Attributes partition: " + str(multipart))
    
    consistant = True
    for entryM in multipart:
        subset=False
        for entryD in partD:
            diag(str(entryM) + "<=" + str(entryD) + "?")
            if set(entryM) <= set(entryD):
                subset = True
                diag("Subset found")
                break
        if subset == False:
            return False
    return True


#####################
# calcualte entropy #
#####################
def entropy(entries, attributes,attr):
    if attr == -1:
        partition = partitionD(entries)
    else:
        partition = partitionAttribute(entries,attr)
    
    sizes = [len(x) for x in partition]
    
    diag("partition: " + str(partition))
    diag("size of  : " + str(sizes))
    
    ent = 0.0
    
    for x in sizes:
        ent += -(x/len(entries))*log((x/len(entries)),2)
        
    diag(ent)
    return ent


#################################
# calcualte conditional entropy #
#################################
def conditionalEntropy(entries, attributes, attr):
    partD = partitionD(entries)
    partA = partitionAttribute(entries,attr)
    
    diag("Decision partition : " + str(partD))
    diag("Attribute partition: " + str(partA))
    sizes = [len(x) for x in partA]
    
    ent = 0.0
    for x in partA:
        subPartD = {}
        for y in x:
            try:
                subPartD[entries[y].D] += 1
            except:
                subPartD[entries[y].D] = 1
                
        diag(subPartD)
        
        for y in subPartD:
            xl = float(len(x))
            yl = float(subPartD[y])
            diag(str(len(x))+"/"+str(len(entries))+" x -"+str(subPartD[y])+"/"+str(len(x))+" x lg("+str(subPartD[y])+"/"+str(len(x))+")")
            ent += xl/len(entries)*(-yl/xl)*log(yl/xl,2)
    diag(ent)
    return ent


###################################
# calcualte average block entropy #
###################################
def averageBlockEntropy(entries, attributes, attr):
    return conditionalEntropy(entries, attributes, attr) / len(partitionAttribute(entries,attr))


'''###########################################
# cutpoints: equal frequency per interval #
###########################################
def globalEqualFrequencyPerInterval(entries, attributes):
    k = [2 for x in attributes]
    count = len(entries)
    parts = []
    cutpoints = []
    for i in range(0,len(attributes)):
        parts.append(partitionAttribute(entries,i))
        cutpoints.append([entries[parts[i][j][0]].A[i] for j in range(0,len(parts[i]))])
        diag("Attribute: " + attributes[i],1)
        diag(parts[i],1)
        diag(cutpoints[i],1)
        
    diag(cutpoints,1)'''


###################################
# cutpoints: equal interval width #
###################################
def globalEqualIntervalWidth(entries, attributes):
    k = [2 for x in attributes]
    count = len(entries)
    parts = []
    values = []
    cutpoints = []
    for i in range(0,len(attributes)):
        parts.append(partitionAttribute(entries,i))
        values.append([entries[parts[i][j][0]].A[i] for j in range(0,len(parts[i]))])
        
    for i in range(0,len(attributes)):
        cutpoints.append([round(values[i][0] + j*(values[i][-1] - values[i][0])/(k[i]),7) for j in range(1,k[i])])
        
        # Diagnostics
        d = 1
        diag("\nAttribute: " + attributes[i],d)
        diag("partition: " + str(parts[i]),d)
        diag("values   : " + str(values[i]),d)
        diag("cutpoints: " + str(cutpoints[i]),d)
        
    # Diagnostics
    d = 1
    diag("\nattr values: " + str(values),d)
    diag("cutpoints  : "+str(cutpoints)+"\n",d)
    
    dis_entries = {}
    for i in range(0,len(entries)):
        temp = []
        for attr in entries[i].A:
            for val in cutpoints[attr]:
                if entries[i].A[attr] < val:
                    temp.append("x<" + str(val))
                    break
            try:temp[attr]
            except:temp.append("x>" + str(cutpoints[attr][-1]))
        dis_entries[i] = entry(temp, entries[i].D)
    
        
    table2file(dis_entries,attributes)
    
    
###################
# Begin execution #
###################
def main():
    # generate random LERS file
    if True == False:
        randomLERS(30)
        
    # file selection
    if True == False:
        filename = selectFile()
        file = openfile(filename)
    else:
        file = openfile("jerzy1.txt")

    # read and parse LERS file
    if True == True:    
        (entries,attributes) = parsefile2(file)
        
        #print(entropy(entries,attributes,1))
        #print(conditionalEntropy(entries, attributes, 1))
        #print(averageBlockEntropy(entries, attributes, 1))
        globalEqualIntervalWidth(entries, attributes)
        '''
        for i in range(0,len(entries)):
            print(str(i) + ": " + str(entries[i].A) + ", " + str(entries[i].D))
        '''

        #isconsistant(entries,len(attributes))
                
main()