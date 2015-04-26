#!/usr/bin/env python

import random
from utility import *
import os
from math import log

# Function announce
status = 0


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
    d=0
    if status==1: print("Parsing the lers input file")
    current_line = 0
    got_attributes = 0 # 0=haven't started reading, 1=in progress, 2=done
    attributes = []
    attribute_values = []
    i = 0
    decision = ""
    decision_value = ""
    entries = {}
    for line in file:
        current_line += 1
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
                attr_values_to_gather = len(attributes)
            else: # attribute list doesn't end on this line
                got_attributes = 1
                attributes += line[1:len(line)]
        else:
            if got_attributes == 1: # reading attributes still
                if line[-1] == ']': # attribute list ends on this line
                    attributes += line[0:-2]
                    decision = line[-2]
                    got_attributes = 2
                    attr_values_to_gather = len(attributes)
                    diag("Finished reading attributes.\n\nDecision is " + str(decision),d)
                    diag("There are a total of " + str(len(attributes)) + " to find",d)
                    diag("The first attribute read was " + str(attributes[0]) + " and the last attribute read was " + str(attributes[-1]),d)
                else: # attribute list doesn't end on this line
                    attributes += line#[0:-1]
            elif got_attributes == 2: # done reading attributes
                diag("Reading attribute values",d)
                #attribute_values.append(line)
                if len(line)+len(attribute_values) < len(attributes):
                    diag("\nline #" + str(current_line) + " didn't finish the entry (" + str(len(line)+len(attribute_values)) + " vs " + str(len(attributes)) + ")",d)
                    float(line[-1])
                    attribute_values += line
                elif len(line)-1 + len(attribute_values) == len(attributes):
                    diag("\nline #" + str(current_line) + " finished the entry (" + str(len(line)-1+len(attribute_values)) + " vs " + str(len(attributes)) + ")",d)
                    attribute_values += [float(val) for val in line[0:-1]]
                    decision_value = line[-1]
                    entries[i] = entry(attribute_values, decision_value)
                    
                    attribute_values = []
                    i += 1
                else:
                    print("error: Problem reading line #" + str(current_line))
                    quit()

    return (entries,attributes,decision)


################################################
# function to partition a set based on concept #
################################################
def partitionD(entries):
    if status==1: print("Partitioning the decision")
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
    if status==1: print("Partitioning a single attribute")
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
    if status==1: print("Partitioning multiple attributes")
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
def isConsistant(entries,num_attributes):
    if status==1: print("Checking for consistancy")
    # Diagnostics on (1) or off (0)?
    d = 0
    
    partD = partitionD(entries)
    multipart = partitionAttribute(entries,0)
    for i in range(0,num_attributes):
        part = partitionAttribute(entries,i)
        multipart = partitionAttributes(part,multipart)
    
    diag("Decision partition  : " + str(partD),d)
    diag("Attributes partition: " + str(multipart),d)
    
    consistant = True
    for entryM in multipart:
        subset=False
        for entryD in partD:
            diag(str(entryM) + "<=" + str(entryD) + "?",d)
            if set(entryM) <= set(entryD):
                subset = True
                
                diag("\nSubset found",d)
                break
        if subset == False:
            return False
    return True


#####################
# calcualte entropy #
#####################
def entropy(entries, attributes,attr):
    if status==1: print("Computing entropy")
    # Diagnostics on (1) or off (0)?
    d = 0
    
    
    if attr == -1:
        partition = partitionD(entries)
    else:
        partition = partitionAttribute(entries,attr)
    
    sizes = [len(x) for x in partition]
    
    diag("partition: " + str(partition),d)
    diag("size of  : " + str(sizes),d)
    
    ent = 0.0
    
    for x in sizes:
        ent += -(x/len(entries))*log((x/len(entries)),2)
        
    diag(ent)
    return ent


#################################
# calcualte conditional entropy #
#################################
def conditionalEntropy(entries, attributes, attr):
    if status==1: print("Computing conditional entropy")
    # Diagnostics on (1) or off (0)?
    d = 0
    
    partD = partitionD(entries)
    partA = partitionAttribute(entries,attr)
    
    diag("Decision partition : " + str(partD),d)
    diag("Attribute partition: " + str(partA),d)
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
    if status==1: print("Computing average block entropy")
    return conditionalEntropy(entries, attributes, attr) / len(partitionAttribute(entries,attr))

    
################################################################
# Functioon to parse for the attribute values from the entries # 
################################################################
def findAttributeValues(entries,num_attributes):
    attr_values = [[] for attr in range(0,num_attributes)]
    
    # Setting up dependancy info
    for ent in entries:
        for attr in range(0,num_attributes):
            if not(entries[ent].A[attr] in attr_values[attr]):
                attr_values[attr].append(entries[ent].A[attr])
                
    for attr in range(0,num_attributes):
        attr_values[attr].sort()
                
    return attr_values
    


################################
# equal frequency per interval #
################################
def globalConditionalEntropy(entries, attributes,decision):
    # Diagnostics on (1) or off (0)?
    d = 0
    
    k = [2 for attr in attributes]
    old_k = [0 for attr in attributes]
    cutpoints = [[] for attr in attributes]
    #attr_values = [[] for attr in attributes]
    possible_cutpoints = [[] for attr in attributes]
    cutpoints = [[] for attr in attributes]
    temp_cutpoints = [[] for attr in attributes]
    
    attr_values = findAttributeValues(entries,len(attributes))
    
    '''# Setting up dependancy info
    for ent in entries:
        for attr in range(0,len(attributes)):
            if not(entries[ent].A[attr] in attr_values[attr]):
                attr_values[attr].append(entries[ent].A[attr])'''
    
    # Diagnostics: print attribute values
    for attr in range(0,len(attributes)):         
        diag("Attribute #" + str(attr) + "'s values" + str(attr_values[attr]),d)
    
    # Calculate possible cutpoints
    for attr in range(0,len(attributes)):
        attr_values[attr].sort()
        for val in range(0,len(attr_values[attr])-1):
            possible_cutpoints[attr].append(round((attr_values[attr][val] + attr_values[attr][val+1])/2.0,7))
    
    # Diagnostics: print possible cutpoints
    diag("",d)
    for attr in range(0,len(attributes)):         
        diag("Attribute #" + str(attr) + "'s possible cutpoints" + str(possible_cutpoints[attr]),d)
    
    
    # Find cutpoints from possible cutpoints
    while True:
        entropies = [[] for attr in attributes]
        for attr in range(0,len(attributes)):
            # no need to process the same attribute if it's already been done
            diag("" + str(k[attr]) + " vs " + str(old_k[attr]),d)
            if (k[attr] > old_k[attr]):
                diag("\nFor attribute #" + str(attr) + ",",d)
                # for each possible cutpoint for the given attribute:
                for val in range(0,len(possible_cutpoints[attr])):
                    # initialize the cutpoints
                    diag("considering " + str(possible_cutpoints[attr][val]) + " and " + str(cutpoints[attr]),d)
                    temp_cutpoints = [[0] for attr in attributes]
                    temp_cutpoints[attr] = [possible_cutpoints[attr][val]] + cutpoints[attr]
                    
                    temp_entries = buildDiscretizedTable(entries,temp_cutpoints,attr_values)
                    entropies[attr].append(conditionalEntropy(temp_entries,attributes,attr))
                
                lowest_ent = 0
                for val in range(0,len(entropies[attr])):
                    if entropies[attr][val] < entropies[attr][lowest_ent] and not(possible_cutpoints[attr][val] in cutpoints[attr]):
                        lowest_ent = val
                
                
                cutpoints[attr].append(possible_cutpoints[attr][lowest_ent])
                diag("Adding the cutpoint " + str(possible_cutpoints[attr][lowest_ent]) + " to get " + str(cutpoints) + "",d)
                possible_cutpoints[attr].remove(possible_cutpoints[attr][lowest_ent])
                diag("The following remain as possible cutpoints: " + str(possible_cutpoints[attr]) + "\n",d)
                #possible_cutpoints[attr] = [val for val in possible_cutpoints[attr] if val != cutpoints[attr][-1]]
                
        
        # build the table with the new cutpoint(s) 
        diag("\nRebuilding table with cutpoints " + str(cutpoints),d)
        temp_entries = buildDiscretizedTable(entries,cutpoints,attr_values)
        
        # check if the new table is consistant.  If not, increment a k.
        if isConsistant(temp_entries,len(attributes)):
            diag("Discretized table is consistant",d)
            dis_entries = temp_entries
            break
        else:
            diag("Discretized table is not consistant",d)
            #  (old location, old entropy), (new location, new entropy)
            worst_attribute = [(-1,0),()]
            for attr in range(0,len(attributes)):
                worst_attribute[1] = (attr,averageBlockEntropy(temp_entries, attributes, attr))
                diag("Comparing entorpy (new) " + str(worst_attribute[1][1]) + " to (old) " + str(worst_attribute[0][1]) + ". This attribute has " + str(len(possible_cutpoints[attr])) + " possible cutpoints remaining.",d)
                if (worst_attribute[1][1] > worst_attribute[0][1]) and len(possible_cutpoints[attr]) > 0:
                    worst_attribute[0] = worst_attribute[1]
            
            old_k = [val for val in k]
            if worst_attribute[0][0] > -1:
                k[worst_attribute[0][0]] += 1
                diag("Incremented k for attribute #" + str(worst_attribute[0][0]) + ": " + str(k) + "",d)
                diag("There are a total of " + str([len(vals) for vals in attr_values]) + " values per attribute\n",d)
            else:
                print("error: The computed table is not consistant and there are no more cutpoints left to introduce")
                table2file(temp_entries,attributes,cutpoints,attr_values,decision)
                quit()
    
    
    return (dis_entries,cutpoints)


################################
# equal frequency per interval #
################################
def globalEqualFrequencyPerInterval(entries, attributes):
    if status==1: print("Calculating discritiztion via the global equal frequency per interval method")
    
    # Diagnostics on (1) or off (0)?
    d = 0
    
    k = [2 for x in attributes]
    count = len(entries)
    
    attr_values = findAttributeValues(entries,len(attributes))
    
    while True:
    
        (parts,values,cutpoints,dis_entries) = cutpointsEqualFrequencyPerInterval(entries,attributes,attr_values,k)
            
        # Diagnostics
        diag("\nattr values: " + str(values),d)
        diag("cutpoints  : "+str(cutpoints)+"\n",d)
        
        if isConsistant(dis_entries,len(attributes)):
            diag("Cutpoints found, table is consistant.\n",d)
            break
        else:
            ent = []
            toincrement = 0
            
            for attr in range(0,len(attributes)):
                ent.append(averageBlockEntropy(dis_entries, attributes, attr))
            
            diag("The average block entropies are:\n" + str(ent),d)
                
            for attr in range(0,len(attributes)):
                if (ent[attr] > ent[toincrement]) and (k[attr] < len(values[attr])):
                    diag("k: " + str(k[attr]) + " and number of values: " + str(len(values[attr])),d)
                    toincrement = attr
                else:
                    ent[attr] = 0
            
            k[toincrement] += 1
            
            diag("Not done. Here are the new k values:\n" + str(k),d)
            
            diag("The number of values per attribute are:\n" + str([len(x) for x in values]) + "\n",d)
            
    
    return (dis_entries,cutpoints)


###########################################
# cutpoints: equal frequency per interval #
###########################################
def cutpointsEqualFrequencyPerInterval(entries,attributes,attr_values,k):
    if status==1: print("Finding cutpoints using the global equal interval width method")
    # Diagnostics on (1) or off (0)?
    d = 0
    
    cutpoints = [[] for x in attributes]
    parts = []
    total_entries = len(entries)
    
    
    # Calculate the partitions of each attribute
    for i in range(0,len(attributes)):
        parts.append(partitionAttribute(entries,i))
    
    
    
    value_entry = [{} for x in attributes]
    for attr in range(0,len(attributes)):
        for ent in parts[attr]:
            value_entry[attr][(entries[ent[0]].A[attr])] = ent

    diag("\nvalues per attribute\n" + str(attr_values),d)
    diag("sorted value loctions\n" + str(value_entry),d)
    diag("partitions:\n" + str(parts) + "\n",d)

    
    
    # build groupings
    grouping = [[{"values": [], "length": 0} for x in range(0,k[attr])] for attr in range(0,len(attributes))]
    for attr in range(0,len(attributes)):
        values = [val for val in value_entry[attr]]
        values.sort()

        values_needed = k[attr]
        values_left = len(values)

        for grp in range(0,k[attr]):
            diag("\nValues for attribute #" + str(attr) + ": " + str(values) + " (cover " + str(total_entries) + " entries)",d)
            diag("=== Working with group #" + str(grp) + " out of " + str(k[attr]) + " groups ===",d)
            for value in range(0,len(values)):
                diag("Is " + str(values[value]) + " in " + str(grouping[attr]) + "?",d)
                if not(values[value] in [inner for outer in [g["values"] for g in grouping[attr]] for inner in outer]):
                    diag("=Comparing difference in number of entries if we add " + str(values[value]) + " (" + str(len(value_entry[attr][values[value]])) + " entries) to the group:",d)
                    
                    old_length = total_entries / float(k[attr]) - grouping[attr][grp]["length"]
                    new_length = total_entries / float(k[attr]) - grouping[attr][grp]["length"] - len(value_entry[attr][values[value]])
                    diag(str(old_length) + " (old) vs " + str(new_length) + " (new)",d) 
                    
                    if ((abs(old_length) > abs(new_length))and (values_needed < values_left)) or (len(grouping[attr][grp]["values"]) == 0) or (grp == k[attr]-1) or (len(grouping[attr][grp]["values"]) == 0):
                        grouping[attr][grp]["length"] += len(value_entry[attr][values[value]])
                        grouping[attr][grp]["values"].append(values[value])
                        values_left -= 1
                        diag("Added " + str(values[value]) + " to the group. Group #" + str(grp) + " now contains " \
                             + str(grouping[attr][grp]["length"]) + " out of " + str(total_entries) + " entries (target: " + str(total_entries / float(k[attr])) + ")",d)
                    else:
                        diag("Not adding " + str(values[value]) + " to this group",d)
                        values_needed -= 1
                        diag("Group #" + str(grp) + " found for attribute #" + str(attr) + " (covers " + str(grouping[attr][grp]["length"]) + " entries)\n",d)
                        break
        diag("Grouping for the attribute is " + str(grouping[attr]) + "\n\n",d)
                    
    
    diag("\n==Groupings==",d)
    for attr in range(0,len(attributes)):
        diag("For attribute #" + str(attr) + ": " + str(grouping[attr])+"\n",d)
    diag("",d)


    d=0
    # build cutpoints from groupings
    for attr in range(0,len(attributes)):
        diag("\n\nGrouping: " + str(grouping[attr]) + "\n",d)
        for group in range(0,len(grouping[attr])-1):
            diag("\n\nWorking with attribute #" + str(attr) + ", group #" + str(group) + ".  It has a k value of " + str(k[attr]) + " (" + str(k) + ")",d)
            diag("Group contains: " + str(grouping[attr][group]) + "",d)

            diag(str(grouping[attr][group]["values"][-1]),d)
            diag(str(grouping[attr][group+1]["values"]),d) 
            

            diag("Groups (#" + str(group) + ", #" + str(group+1) + "): " + str(grouping[attr][group]["values"]) + ", " + str(grouping[attr][group+1]["values"]),d)
            
            cutpoints[attr].append(round((grouping[attr][group+1]["values"][0] + grouping[attr][group]["values"][-1])/2.0,6))
            
            diag("Cutpoints (updated): " + str(cutpoints[attr]) + " (added cutpoint " + str(round((grouping[attr][group+1]["values"][0] + grouping[attr][group]["values"][-1])/2.0,6)) + ")",d)
    
    dis_entries = buildDiscretizedTable(entries,cutpoints,attr_values)
        
    
    return (parts,attr_values,cutpoints,dis_entries)
    
    
###################################
# cutpoints: equal interval width #
###################################
def buildDiscretizedTable(entries,cutpoints,attr_values):
    d=0
    
    dis_entries = {}
    for i in range(0,len(entries)):
        temp = []
        for attr in entries[i].A:
            cutpoints[attr].sort()
            
            diag(cutpoints[attr],d)
            
            if len(cutpoints[attr]) == 0:
                temp.append(str(attr_values[attr][0]) + ".." + str(attr_values[attr][-1]))
                continue
            else:
                for j in range(0,len(cutpoints[attr])):
                    
                    if entries[i].A[attr] < cutpoints[attr][j]:
                        if j==0:
                            temp.append(str(attr_values[attr][0]) + ".." + str(cutpoints[attr][j]))
                        else: 
                            temp.append(str(cutpoints[attr][j-1]) + ".." + str(cutpoints[attr][j]))
                            
                        break
                
                try:temp[attr]
                except:temp.append(str(cutpoints[attr][-1]) + ".." + str(attr_values[attr][-1]))
            
        dis_entries[i] = entry(temp, entries[i].D)
    
    return dis_entries
    
    
###################################
# cutpoints: equal interval width #
###################################
def cutpointsEqualIntervalWidth(entries,attributes,k):
    if status==1: print("Finding cutpoints using the global equal interval width method")
    # Diagnostics on (1) or off (0)?
    d = 0
    
    
    cutpoints = [] 
    parts = []
    #attr_values = []
    
    for i in range(0,len(attributes)):
        parts.append(partitionAttribute(entries,i))
        #attr_values.append([entries[parts[i][j][0]].A[i] for j in range(0,len(parts[i]))])
        #attr_values[i].sort()
    attr_values = findAttributeValues(entries,len(attributes))
    
    for i in range(0,len(attributes)):
        cutpoints.append([round(attr_values[i][0] + j*(attr_values[i][-1] - attr_values[i][0])/(k[i]),7) for j in range(1,k[i])])
        
        # Diagnostics
        diag("\nAttribute: " + attributes[i],d)
        diag("partition: " + str(parts[i]),d)
        diag("values   : " + str(attr_values[i]),d)
        diag("cutpoints: " + str(cutpoints[i]),d)
    
    dis_entries = buildDiscretizedTable(entries,cutpoints,attr_values)
        
    return (parts,attr_values,cutpoints,dis_entries)


########################
# equal interval width #
########################
def globalEqualIntervalWidth(entries, attributes):
    if status==1: print("Calculating discritiztion via the global equal interval width method")
    # Diagnostics on (1) or off (0)?
    d = 0
    
    k = [2 for x in attributes]
    count = len(entries)
    
    while True:
    
        (parts,values,cutpoints,dis_entries) = cutpointsEqualIntervalWidth(entries,attributes,k)
            
        # Diagnostics
        diag("\nAttr values: " + str(values),d)
        diag("Cutpoints  : "+str(cutpoints)+"\n",d)
        
        if isConsistant(dis_entries,len(attributes)):
            diag("Cutpoints found, table is consistant.\n",d)
            break
        else:
            ent = []
            toincrement = 0
            
            for attr in range(0,len(attributes)):
                ent.append(averageBlockEntropy(dis_entries, attributes, attr))
            
            diag("The average block entropies are:\n" + str(ent),d)
                
            for attr in range(0,len(attributes)):
                if (ent[attr] > ent[toincrement]) and (k[attr] < len(values[attr])):
                    diag("k: " + str(k[attr]) + " and number of values: " + str(len(values[attr])),d)
                    toincrement = attr
                else:
                    ent[attr] = 0
            
            k[toincrement] += 1
            
            diag("Not done. Here are the new k values:\n" + str(k),d)
            
            diag("The number of values per attribute are:\n" + str([len(x) for x in values]) + "\n",d)
            
    
    return (dis_entries,cutpoints)


###################
# merge cutpoints #
###################
def merge(entries, cutpoints, attributes):
    if status==1: print("Merging cutpoints")
    # Diagnostics on (1) or off (0)?
    d = 0
    
    attr_values = findAttributeValues(entries,len(attributes))
    
    for attr in range(0,len(attributes)):
        for cutpoint in cutpoints[attr]:
            temp_cutpoints = cutpoints            
            temp_cutpoints[attr].remove(cutpoint)
            
            diag(temp_cutpoints,d)
            dis_entries = buildDiscretizedTable(entries,temp_cutpoints,attr_values)
            
            if isConsistant(dis_entries,len(attributes)):
                cutpoints = temp_cutpoints
                diag("cutpoint " + str(cutpoint) + " removed from attribute #" + str(attr),d)
    
    return (dis_entries,cutpoints)
    
    
###################
# Begin execution #
###################
class main():
    def discretize(self):
        # file selection
        user_input = 1
        if user_input == 1:
            filename = selectFile()
            if filename == 0:
                quit()
            else:
                file = openfile(filename)
        else:
            file = openfile("jerzy3.txt")
            
            
        (entries,attributes,decision) = parsefile(file)
        file.close()
        
        if not(isConsistant(entries,len(attributes))):
            print("Sorry, the provided table is not consistant")
            quit()


        
        print("\nWhich discretization method would you like to use?")
        print("1: Global conditional entropy")
        print("2: Global equal frequency per interval")
        print("3: Global equal interval width")
        print("4: Exit")
        while True:
            user_input = get_user_input("> ")
            if user_input == "1":
                print("\nOk.  Calculating...")
                (dis_entries,cutpoints) = globalConditionalEntropy(entries, attributes,decision)
                (dis_entries,cutpoints) = merge(entries, cutpoints, attributes)
                break
            elif user_input == "2":
                print("\nOk.  Calculating...")
                (dis_entries,cutpoints) = globalEqualFrequencyPerInterval(entries, attributes)
                (dis_entries,cutpoints) = merge(entries, cutpoints, attributes)
                break
            elif user_input == "3":
                print("\nOk.  Calculating...")
                (dis_entries,cutpoints) = globalEqualIntervalWidth(entries, attributes)
                (dis_entries,cutpoints) = merge(entries, cutpoints, attributes)
                break
            elif user_input == "4":
                quit()
            else:
                print("\nInvalid selection, please try again\n")
        attr_values = findAttributeValues(dis_entries,len(attributes))
        (datafilename,numbfilename) = table2file(dis_entries,attributes,cutpoints,attr_values,decision)
        diag("Table written to " + str(datafilename) + "\nCutpoint info written to " + numbfilename,1)
        
    def __init__(self):
        while True:
            self.discretize()
            
            while True:
                print("\n\nWould you like to perform another discretization (y or n)?")
                user_input = get_user_input("> ")
                
                if user_input.lower() == "y":
                    break
                elif user_input.lower() == "n":
                    print("\nOk.  Quitting")
                    quit()
                else:
                    print("\nerror: Invalid choice, please try again")
                    continue
        
        

main()