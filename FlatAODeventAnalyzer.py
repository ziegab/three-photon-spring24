import ROOT
from ROOT import *
from array import array
import sys
import csv

# This code reads the event file, finds the efficiencies, and loads it onto a csv file.
## Only works for FlatAOD. 
# Purpose: To compare the effectiveness ("efficiency") of choosing the second two photons in the 3 photon event (the
    # lower energy photons) to compose the diphoton object compared to the first two and the first and last photons.

# ~~ 1D histograms ~~
# 1D histogram = TH1F(const char *name, const char *title, Int_t nbinsx, Double_t xlow, Double_t xup)
H_pt = TH1F("pT", ";all photon p_{T} (GeV):Events",100,0.,2000.)
H_masstot = TH1F("Mass", "Mass:Events", 100, 0., 5000.)
H_genmasstot = TH1F("genMass", "Mass:Events", 100, 0., 5000.)
H_mass01 = TH1F("Mass01", "Mass:Events", 100, 0., 5000.)
H_mass12 = TH1F("Mass12", "Mass:Events", 100, 0., 5000.)
H_mass02 = TH1F("Mass02", "Mass:Events", 100, 0., 5000.)
H_massduo = TH1F("Massduo", "Mass:Events", 100, 0., 100.)

# ~~ 2D histograms ~~
H_2pho3phomass = TH2F("2pho3phomass", "2 Photon Pair Mass:3 Photon Pair Mass", 100, 0., 2000., 100, 0., 2000.)

filenamebase = sys.argv[1]
infile = TFile(filenamebase)
filename = filenamebase[57:] # specific to the file path (isolating just the file name)
intree = infile.Get("flattener/tree") # specific to FlatAOD file type

# ~~ Setting counters, which will be used to calculate percentage of "efficiency"
countertotalp = 0
countervec0 = 0
countervec1 = 0
countervec2 = 0
countertotalevents = 0

for e in intree: #can replace T with any file tree since the process is the same for all
    countertotalevents +=1
    vectors = []
    genpartvectors = []
    genpartvectmomid = []
    # Isolating specific quantities (branches) from each event (these are MonteCarlo generated events)
    pdgid = e.genpart_pdgid
    motherpdgid = e.genpart_motherpdgid
    gen_pt = e.genpart_pt
    gen_eta = e.genpart_eta
    gen_phi = e.genpart_phi
    gen_mass = e.genpart_mass
    gen_energy = e.genpart_energy
    p_pt = e.patpho_pt
    p_eta = e.patpho_eta
    p_phi = e.patpho_phi
    p_mass = e.patpho_mass
    p_energy = e.patpho_energy
    n_pho = len(p_pt)
    n_genpart = len(pdgid) #same length as mompdgid
    for i in range(0,n_genpart):
        part1 = pdgid[i] # particle ID for the particle in question
        part2 = motherpdgid[i] # particle ID for the parent of the particle in question
        if part1 == 22: # particle ID for photons
            # Generating 4-vectors for the 3 photon event, to later reconstruct the original objects
            vtemp2 = TLorentzVector()
            vtemp2.SetPtEtaPhiE(gen_pt[i], gen_eta[i], gen_phi[i], gen_energy[i])
            genpartvectors.append(vtemp2)
            genpartvectmomid.append(part2)
    # Isolating events that come from the Bulk Graviton and the Radion
    if genpartvectmomid[0] == 9000121 and genpartvectmomid[1] == 9000025: # particle IDs for Bulk Graviton and Radion
        genV = genpartvectors[0]+genpartvectors[1]+genpartvectors[2]
        H_genmasstot.Fill(genV.M())

    # Isolating three photon events to use for reconstruction
    if n_pho == 3:
        for i in range(0, n_pho):
            vtemp1 = TLorentzVector()
            vtemp1.SetPtEtaPhiE(p_pt[i], p_eta[i], p_phi[i], p_energy[i])
            vectors.append(vtemp1)
        V = vectors[0]+vectors[1]+vectors[2]
        V0 = vectors[0].M()
        V1 = vectors[1].M()
        V2 = vectors[2].M()
        Vmin = min(V0, V1, V2)
        V01 = vectors[0]+vectors[1]
        V12 = vectors[1]+vectors[2]
        V02 = vectors[0]+vectors[2]
        H_masstot.Fill(V.M()) # plot mass and not energy
        H_mass01.Fill(V01.M())
        H_mass12.Fill(V12.M())
        H_mass02.Fill(V02.M())
        H_2pho3phomass.Fill(V12.M(), V.M())
    
    # Isolating 3 Photon events and finding matching the non-diphoton photon to its gen particle counterpart
    angles0 = []
    if len(vectors) == 3:
        for j in range(0,3):
            angles0.append(genpartvectors[0].DeltaR(vectors[j]))
    if len(angles0) == 3:
        countertotalp += 1
        temp0 = min(angles0)
        res0 = [i for i, j in enumerate(angles0) if j == temp0]
        if res0[0] == 0:
            Vduo = vectors[1]+vectors[2]
            countervec0 += 1
        elif res0[0] == 1:
            Vduo = vectors[0]+vectors[2]
            countervec1 += 1
        elif res0[0] == 2:
            Vduo = vectors[0]+vectors[1]
            countervec2 += 1
        H_massduo.Fill(Vduo.M())

print("Total number of 3 photon events:", countertotalp)

pctvec0 = countervec0/countertotalp*100
pctvec1 = countervec1/countertotalp*100
pctvec2 = countervec2/countertotalp*100
pcttotalevent = countervec0/countertotalevents*100

print("Total number of events:", countertotalevents)
print("Percentage that the smallest energies correspond to the diphoton pair:", "%.2f" % pctvec0)
print("Percentage that this pairing is selected out of total events (efficiency):", "%.2f" % pcttotalevent)

# ~~ Creates 2D histogram of 3 vs. 2 photon masses
H_2pho3phomass.SetStats(0)
C = TCanvas()
C.cd()
H_2pho3phomass.Draw("hist")
H_2pho3phomass.Draw("colz")
# C.Print("Test32D2pho3pho4.pdf")

# # Plotting histograms (multiple on one canvas)
# ~~ Compares the match-up of the photons in the event to the diphoton object
# ~~ The diphoton object should have the vectors adding up to the small mass (R0)

C1 = TCanvas()
C1.cd()
# gStyle.SetOptTitle(kFALSE)
gStyle.SetOptStat(0)
# hs1.Draw("hist")
H_mass12.Draw("PLC PMC hist")
H_mass01.Draw("SAME PLC PMC hist")
H_mass02.Draw("SAME PLC PMC hist")
legend1 = TLegend(0.9,0.7,0.48,0.9)
legend1.SetHeader("Legend","C")
legend1.AddEntry(H_mass01, "Reconstructed mass of first two photons.")
legend1.AddEntry(H_mass12, "Reconstructed mass of second two photons.")
legend1.AddEntry(H_mass02, "Reconstructed mass of first and last photons.")
legend1.Draw()
# C1.Print("Test3vectphomass3.pdf")

# ~~ Gettting information from the file name ~~
characters = len(filename)
testnamechar = [*filename]
for i in range(characters):
    if testnamechar[i].isdigit() == True:
        firstnum = i
        break
if testnamechar[firstnum+9] == '-':
    largemass = str(testnamechar[firstnum+2])+str(testnamechar[firstnum+3])+str(testnamechar[firstnum+4])+str(testnamechar[firstnum+5])
    numcount = firstnum+10
    testnamecharlooper = testnamechar[numcount]
    smallmass = ''
    while testnamecharlooper != '_':
        smallmass += str(testnamecharlooper)
        numcount += 1
        testnamecharlooper = testnamechar[numcount]
else:
    largemass = str(testnamechar[firstnum+2])+str(testnamechar[firstnum+3])+str(testnamechar[firstnum+4])
    numcount = firstnum+9
    testnamecharlooper = testnamechar[numcount]
    smallmass = ''
    while testnamecharlooper != '_':
        smallmass += str(testnamecharlooper)
        numcount += 1
        testnamecharlooper = testnamechar[numcount]

# ~~ Importing efficiency info into a csv file ~~
with open('efficiencyinfo1.csv', 'a', newline='') as csvfile:
    test2writer = csv.writer(csvfile, dialect='excel')
    test2writer.writerow([largemass] + [smallmass] + [countertotalevents] + [countertotalp] + [pctvec0] + [pcttotalevent])
