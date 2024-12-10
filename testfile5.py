import ROOT
from ROOT import *
from array import array
import sys
import csv

#This code takes the efficiency info from the csv and makes it into histograms.
## This creates a basic 2D histogram (no variable bin widths), testfile6.py has same code plus variable bin widths

H_efficiency = TH2F("Efficiency", "2 Photon Pair Mass:3 Photon Pair Mass", 200, 0., 65., 100, 0., 3050.)
H_smallEpct = TH2F("Small Mass Percent", "2 Photon Pair Mass:3 Photon Pair Mass", 200, 0., 65., 100, 0., 3050.)

# Need to pull the masses and efficiency values from the csv table and weigh the overlap of masses by the efficiency.
# step 1: pull from csv table and put into lists i guess
rows = []
largemasses = []
smallmasses = []
n_events = []
n_3phoevents = []
smallEpct = []
efficiency = []
with open('efficiencyinfo1.csv', 'r') as csvfile:
    test1reader = csv.reader(csvfile, dialect='excel')
    for row in test1reader:
        rows.append(row)
        # print(row[2]) #this isolates the third column in each row
        if row[0] != 'Large Mass':
            efficiency.append(float(row[5]))
            largemasses.append(float(row[0]))
            smallmasses.append(row[1])
            n_events.append(float(row[2]))
            n_3phoevents.append(float(row[3]))
            smallEpct.append(float(row[4]))
    numrows = test1reader.line_num
    # print(numrows)
for i in range(numrows-1):
    tmpstr1 = smallmasses[i]
    tmpstr2 = tmpstr1.replace('p','.')
    smallmasses[i] = float(tmpstr2)
# largemasses.pop(0)
# smallmasses.pop(0)
# n_events.pop(0)
# n_3phoevents.pop(0)
# smallEpct.pop(0)
# efficiency.pop(0)
# print(smallEpct)

# step 2: figure out how to weigh the mass overlap 
for i in range(numrows-1):
    H_efficiency.Fill(smallmasses[i], largemasses[i], efficiency[i])
    # print(smallEpct[i])
    H_smallEpct.Fill(smallmasses[i], largemasses[i], smallEpct[i])

H_efficiency.SetStats(0)
H_efficiency.SetTitle("Efficiencies of mass combinations")
gStyle.SetPalette(109)
C1 = TCanvas()
C1.cd()
H_efficiency.Draw("hist")
H_efficiency.Draw("colztext")
C1.SetLogx()
C1.SetLogy()
C1.Print("efficiencymap1.pdf")
C1.Print("efficiencymap1.root")

H_smallEpct.SetStats(0)
H_smallEpct.SetTitle("Percent that smallest photon energies form diphoton pair")
gStyle.SetPalette(68)
C2 = TCanvas()
C2.cd()
H_smallEpct.Draw('hist')
H_smallEpct.Draw('colz')
C2.Print("smallEpctmap1.pdf")
