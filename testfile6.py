import ROOT
from ROOT import *
from array import array
import sys
import csv

# taking what testfile5.py does (2d histogram of efficiencies with efficiency as bin weight)
    # and modifying it to fill in the white space. 
# need to average the efficiencies according to bin widths and then plot them at the center or something
# trying to fill in the white space in the 2d histogram (propaganda)
# bin widths should be smaller towards the bottom left since that is where the important behavior is
# work with random numbers for now just to test the behavior of the code
# figure out how to average percentages (simple??)
# figure out how to variable bin width 2d histogram

# ~~ Establishing bin widths for x and y directions (x ~ 2 photon mass, y ~ 3 photon mass)
# need to make bins towards the bottom left corner really precise, rest of the space not as defined
NBinsX = 0
NBinsY = 0
binSmallM = []
binLargeM = []
counterX = 0
counterY = 0
Xbinsizes = [1, 1, 1, 1, 1, 1, 2]
Xbinincrements = [0.25, 0.5, 1, 2, 5, 15, 20]
Ybinsizes = [2, 1, 1, 1, 1, 1]
Ybinincrements = [20, 50, 100, 400, 1000, 2000]
# ~~ Defining X and Y bins ~~
for j in range(len(Xbinsizes)):
    for i in range(Xbinsizes[j]):
        counterX += Xbinincrements[j]
        NBinsX += 1
        binSmallM.append(counterX)
for j in range(len(Ybinsizes)):
    for i in range(Ybinsizes[j]):
        counterY += Ybinincrements[j]
        NBinsY += 1
        binLargeM.append(counterY)

# print(binSmallM)
# print(binLargeM)
# print(NBinsX, NBinsY)

# # ~~ Establishing histograms and getting values from csv table ~~
# H_efficiency = TH2F("Efficiency", "2 Photon Pair Mass:3 Photon Pair Mass", 200, 0., 65., 100, 0., 3050.)
# H_smallEpct = TH2F("Small Mass Percent", "2 Photon Pair Mass:3 Photon Pair Mass", 200, 0., 65., 100, 0., 3050.)

H_efficiency = TH2F("Efficiency", "2 Photon Pair Mass: 3 Photon Pair Mass", (NBinsX-1), array('d', binSmallM), (NBinsY-1), array('d', binLargeM))
H_efficiencycount = TH2F("Efficiencycount", "2 Photon Pair Mass: 3 Photon Pair Mass", (NBinsX-1), array('d', binSmallM), (NBinsY-1), array('d', binLargeM))
H_smallEpct = TH2F("Small Mass Percent", "2 Photon Pair Mass: 3 Photon Pair Mass", (NBinsX-1), array('d', binSmallM), (NBinsY-1), array('d', binLargeM))

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
        if row[0] != 'Large Mass':
            largemasses.append(float(row[0]))
            smallmasses.append(row[1])
            n_events.append(float(row[2]))
            n_3phoevents.append(float(row[3]))
            smallEpct.append(float(row[4]))
            efficiency.append(float(row[5]))
    numrows = test1reader.line_num
for i in range(numrows-1):
    tmpstr1 = smallmasses[i]
    tmpstr2 = tmpstr1.replace('p','.')
    smallmasses[i] = float(tmpstr2)

# Next step: average efficiency values over the ranges of the bin widths, then fill.

for i in range(numrows-1):
    H_efficiencycount.Fill(smallmasses[i], largemasses[i])
    H_efficiency.Fill(smallmasses[i], largemasses[i], efficiency[i])
    H_smallEpct.Fill(smallmasses[i], largemasses[i], smallEpct[i])

for j in range(NBinsY):
    for i in range(NBinsX):
        temp1 = H_efficiencycount.GetBinContent(i, j)
        if temp1 > 1:
            temp2 = H_efficiency.GetBinContent(i, j)
            temp3 = H_smallEpct.GetBinContent(i, j)
            H_efficiency.SetBinContent(i,j, temp2/temp1)
            H_smallEpct.SetBinContent(i,j,temp3/temp1)

H_efficiency.SetStats(0)
H_efficiency.SetTitle("Efficiencies of mass combinations")
gStyle.SetPalette(109)
gStyle.SetPaintTextFormat("4.2f")
C1 = TCanvas()
C1.cd()
H_efficiency.Draw("hist")
H_efficiency.Draw("colztext")
C1.SetLogx()
C1.SetLogy()
xAxis = H_efficiency.GetXaxis()
xAxis.SetTitle("Diphoton Mass (GeV)")
xAxis.CenterTitle(kTRUE)
# gStyle.SetNdivisions(n=len(smallmasses), axis='x')
# gStyle.SetPadTickX(smallmasses)


yAxis = H_efficiency.GetYaxis()
yAxis.SetTitle("3 Photon Mass (GeV)")
yAxis.CenterTitle(kTRUE)
C1.Print("efficiencymap7.pdf")
C1.Print("efficiencymap7.root")

H_smallEpct.SetStats(0)
H_smallEpct.SetTitle("Percent that smallest photon energies form diphoton pair")
gStyle.SetPalette(68)
gStyle.SetPaintTextFormat("4.2f")
C2 = TCanvas()
C2.cd()
H_smallEpct.Draw('hist')
H_smallEpct.Draw('colztext')
C2.SetLogx()
C2.SetLogy()
xAxis = H_smallEpct.GetXaxis()
xAxis.SetTitle("Diphoton Mass (GeV)")
xAxis.CenterTitle(kTRUE)
yAxis = H_smallEpct.GetYaxis()
yAxis.SetTitle("3 Photon Mass (GeV)")
yAxis.CenterTitle(kTRUE)
C2.Print("smallEpctmap7.pdf")
C2.Print("smallEpctmap7.root")