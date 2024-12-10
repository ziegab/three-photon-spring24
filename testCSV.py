import ROOT
from ROOT import *
from array import array
import sys
import csv

## This file was used to test how to import text/info to a csv file. 

# counter1 = 'photon'
# counter2 = 'events'
# rows = []
# with open('test1.csv', 'a', newline='') as csvfile:
#     test1writer = csv.writer(csvfile, dialect='excel')
#     test1writer.writerow([counter1] + [counter2])

# with open('test1.csv', 'r') as csvfile:
#     test1reader = csv.reader(csvfile, dialect='excel')
#     for row in test1reader:
#         rows.append(row)
#     numrows = test1reader.line_num
#     print(numrows)
#     line_count = numrows-2
#     # print(rows[line_count])
#     for col in rows[line_count]: # this prints all entries in a row
#         print(col)


# ~~ Getting information out of file name ~~
# testname = sys.argv[1]
filenamebase = sys.argv[1]
infile = TFile(filenamebase)
testname = filenamebase[57:]
print(testname)
characters = len(testname)
# print(characters)
testnamechar = [*testname]
for i in range(characters):
    if testnamechar[i].isdigit() == True:
        firstnum = i
        # print(firstnum)
        break
# print(firstnum)
print(testnamechar[firstnum+9])
# largemass = str(testnamechar[firstnum+2])+str(testnamechar[firstnum+3])+str(testnamechar[firstnum+4])+str(testnamechar[firstnum+5])
# print(largemass)
if testnamechar[firstnum+9] == '-':
    largemass = str(testnamechar[firstnum+2])+str(testnamechar[firstnum+3])+str(testnamechar[firstnum+4])+str(testnamechar[firstnum+5])
    print(largemass)
    # smallmass = str(testnamechar[firstnum+10])+str(testnamechar[firstnum+11])
    numcount = firstnum+10
    testnamecharlooper = testnamechar[numcount]
    smallmass = ''
    while testnamecharlooper != '_':
        smallmass += str(testnamecharlooper)
        numcount += 1
        testnamecharlooper = testnamechar[numcount]
    print(smallmass)
else:
    largemass = str(testnamechar[firstnum+2])+str(testnamechar[firstnum+3])+str(testnamechar[firstnum+4])
    print(largemass)
    # smallmass = str(testnamechar[firstnum+9])+str(testnamechar[firstnum+10])
    numcount = firstnum+9
    testnamecharlooper = testnamechar[numcount]
    smallmass = ''
    while testnamecharlooper != '_':
        smallmass += str(testnamecharlooper)
        numcount += 1
        testnamecharlooper = testnamechar[numcount]
    print(smallmass)
