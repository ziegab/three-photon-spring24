import ROOT
from ROOT import *
from array import array
import sys
import csv

# This code reads the event file, finds the efficiencies, and loads it onto a csv file.
# only works for FlatAOD
## Cleaned up and moved this code to FlatAODeventAnalyzer.py, but keeping this for structural reasons

# print("ROOT is loaded.")

# ~~ 1D histograms ~~
# 1D histogram = TH1I(name, title, x dimension (bin, x start, x end)) --> for integers
# 1D histogram = TH1F(const char *name, const char *title, Int_t nbinsx, Double_t xlow, Double_t xup)
# H_nPhotons = TH1F("N_pho", ";Number of pat::photons;Events", 10, 0, 10)
H_pt = TH1F("pT", ";all photon p_{T} (GeV):Events",100,0.,2000.)
H_masstot = TH1F("Mass", "Mass:Events", 100, 0., 5000.)
H_genmasstot = TH1F("genMass", "Mass:Events", 100, 0., 5000.)
# H_masstot = TH1F("Mass", "Mass:Events", (NBins-1), array('d',binLowE))
H_mass01 = TH1F("Mass01", "Mass:Events", 100, 0., 5000.)
H_mass12 = TH1F("Mass12", "Mass:Events", 100, 0., 5000.)
H_mass02 = TH1F("Mass02", "Mass:Events", 100, 0., 5000.)
H_massduo = TH1F("Massduo", "Mass:Events", 100, 0., 100.)
# H_mass01 = TH1F("Mass01", "Mass:Events", (NBins-1), array('d',binLowE))
# H_mass12 = TH1F("Mass12", "Mass:Events", (NBins-1), array('d',binLowE))
# H_mass02 = TH1F("Mass02", "Mass:Events", (NBins-1), array('d',binLowE))
# H_massduo = TH1F("Massduo", "Mass:Events", (NBins-1), array('d', binLowE))

# ~~ 2D histograms ~~
# 2D histogram = TH2F(name, title, )
# 2D histogram = TH2F((const char *name, const char *title, Int_t nbinsx, const Double_t *xbins, Int_t nbinsy, const Double_t *ybins)) --> variable bins
# const char *name, const char *title, Int_t nbinsx, Double_t xlow, Double_t xup, Int_t nbinsy, Double_t ylow, Double_t yup
H_2pho3phomass = TH2F("2pho3phomass", "2 Photon Pair Mass:3 Photon Pair Mass", 100, 0., 2000., 100, 0., 2000.)

F = TFile("BkkToGRadionToGGG_M1-1000_R0-20_2018_FlatAODv3_0.root")
T = F.Get("flattener/tree")
G = TFile("BkkToGRadionToGGG_M1-3000_R0-60_2018_FlatAODv3_0.root")
U = G.Get("flattener/tree")
filenamebase = sys.argv[1]
infile = TFile(filenamebase)
filename = filenamebase[57:]
intree = infile.Get("flattener/tree")

print("tree is loaded.")

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
    # print("event has starts:")
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
    # print(p_mass)
    # print(gen_mass)
    # print(len(pdgid))
    # print(len(motherpdgid))
    p_energy = e.patpho_energy
    n_pho = len(p_pt)
    n_genpart = len(pdgid) #same length as mompdgid
    # print(n_pho)
    for i in range(0,n_genpart):
        part1 = pdgid[i]
        part2 = motherpdgid[i]
        if part1 == 22:# and (part2 == 9000121 or part2 == 9000025):
            vtemp2 = TLorentzVector()
            vtemp2.SetPtEtaPhiE(gen_pt[i], gen_eta[i], gen_phi[i], gen_energy[i])
            genpartvectors.append(vtemp2)
            # genpartvectors.append(TLorentzVector(gen_pt[i], gen_eta[i], gen_phi[i], gen_energy[i]))
            genpartvectmomid.append(part2)
    # if len(genpartvectors) ==3:
    #     counter1 += 1
    # if len(genpartvectmomid) < 3:
    #     break
    if genpartvectmomid[0] == 9000121 and genpartvectmomid[1] == 9000025:
        genV = genpartvectors[0]+genpartvectors[1]+genpartvectors[2]
        # print(genpartvectmomid)
        H_genmasstot.Fill(genV.M())
    # print(genpartvectmomid)

    if n_pho == 3:
        for i in range(0, n_pho):
            vtemp1 = TLorentzVector()
            vtemp1.SetPtEtaPhiE(p_pt[i], p_eta[i], p_phi[i], p_energy[i])
            vectors.append(vtemp1)
            # vectors.append(TLorentzVector(p_pt[i], p_eta[i], p_phi[i], p_energy[i]))
            # vectors.append(TLorentzVector(p_pt[i], p_eta[i], p_phi[i], p_mass[i]))
        # print(vectors)
        V = vectors[0]+vectors[1]+vectors[2]
        V0 = vectors[0].M()
        V1 = vectors[1].M()
        V2 = vectors[2].M()
        # print(V0, V1, V2)
        Vmin = min(V0, V1, V2)
        V01 = vectors[0]+vectors[1]
        V12 = vectors[1]+vectors[2]
        V02 = vectors[0]+vectors[2]
        # print(V.E())
        H_masstot.Fill(V.M()) # plot mass and not energy
        H_mass01.Fill(V01.M())
        H_mass12.Fill(V12.M())
        H_mass02.Fill(V02.M())
        H_2pho3phomass.Fill(V12.M(), V.M())
    
    angles0 = []
    if len(vectors) == 3:
        for j in range(0,3):
            angles0.append(genpartvectors[0].DeltaR(vectors[j]))
    # # print(angles)
    # anglestemp = angles.copy()
    if len(angles0)==3:
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
        # print(Vduo)
        H_massduo.Fill(Vduo.M())

print("Total number of 3 photon events:", countertotalp)

pctvec0 = countervec0/countertotalp*100
pctvec1 = countervec1/countertotalp*100
pctvec2 = countervec2/countertotalp*100
pcttotalevent = countervec0/countertotalevents*100

# print(pctvec0, pctvec1, pctvec2)
# print(countertotalp, countertotalevents, pctvec0, pctvec1, pctvec2)
print("Total number of events:", countertotalevents)
print("Percentage that the smallest energies correspond to the diphoton pair:", "%.2f" % pctvec0)
print("Percentage that this pairing is selected out of total events (efficiency):", "%.2f" % pcttotalevent)

H_2pho3phomass.SetStats(0)
C = TCanvas()
C.cd()
# H_genmasstot.Draw("hist")
H_2pho3phomass.Draw("hist")
H_2pho3phomass.Draw("colz")
# C.Print("Test32D2pho3pho4.pdf")

# Test3massduo1.pdf is the photon pair reconstructed mass with correct formatting
# Test3massduo2.pdf is the photon pair reconstructed mass using TH1F and not TH1I. Seems like the same.
# Test32D2pho3pho3.pdf is with the 3000GeV sample
# Tets32D3pho3pho3.pdf is 1000gev 10gev sample

# # Plotting histograms (multiple on one canvas)

# # hs1 = THStack("hs1","")
# # hs1.Add(H_mass01)
# # hs1.Add(H_mass12)
# # hs1.Add(H_mass02)

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
#test3vectphomass2.pdf is the 1p25 file - i think it's saying the small mass is 1.25 GeV??

# ~~ Gettting information from the file name ~~
characters = len(filename)
testnamechar = [*filename]
for i in range(characters):
    if testnamechar[i].isdigit() == True:
        firstnum = i
        break
if testnamechar[firstnum+9] == '-':
    largemass = str(testnamechar[firstnum+2])+str(testnamechar[firstnum+3])+str(testnamechar[firstnum+4])+str(testnamechar[firstnum+5])
    # smallmass = str(testnamechar[firstnum+10])+str(testnamechar[firstnum+11])
    numcount = firstnum+10
    testnamecharlooper = testnamechar[numcount]
    smallmass = ''
    while testnamecharlooper != '_':
        smallmass += str(testnamecharlooper)
        numcount += 1
        testnamecharlooper = testnamechar[numcount]
else:
    largemass = str(testnamechar[firstnum+2])+str(testnamechar[firstnum+3])+str(testnamechar[firstnum+4])
    # smallmass = str(testnamechar[firstnum+9])+str(testnamechar[firstnum+10])
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
