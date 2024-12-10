import ROOT
from ROOT import *

## This file was used to test working with FlatAOD root files to get info from them.
## Not super useful anymore, but I feel sentimental towards it

print("ROOT is loaded")

H_nPhotons = TH1I("N_pho", ";Number of pat::photons;Events", 10, 0, 10)

F = TFile("BkkToGRadionToGGG_M1-1000_R0-20_2018_FlatAODv3_0.root")
T = F.Get("flattener/tree")

for e in T:
    p_pt = e.patpho_pt
    #print(len(p_pt))
    H_nPhotons.Fill(len(p_pt))

print("tree is loaded")

C = TCanvas()
C.cd()
H_nPhotons.Draw("hist")
C.Print("Test3.pdf")

#leading pt, leading eta, TLorentzVector (class of a 4 vector), add together to get mass of system, get peak at 1 and 3 TeV
