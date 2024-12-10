import ROOT
from ROOT import *
from array import array
import sys
import csv

# This code reads the event file, finds the efficiencies, and loads it onto a csv file.
# only works for NanoAOD

print("ROOT is loaded")

H_pt = TH1F("pT", ";all photon p_{T} (GeV):Events",100,0.,2000.)
H_masstot = TH1F("Mass", "Mass:Events", 100, 0., 5000.)
H_genmasstot = TH1F("genMass", "Mass:Events", 100, 0., 5000.)
H_mass01 = TH1F("Mass01", "Mass:Events", 100, 0., 5000.)
H_mass12 = TH1F("Mass12", "Mass:Events", 100, 0., 5000.)
H_mass02 = TH1F("Mass02", "Mass:Events", 100, 0., 5000.)
H_massduo = TH1F("Massduo", "Mass:Events", 100, 0., 100.)
H_2pho3phomass = TH2F("2pho3phomass", "2 Photon Pair Mass:3 Photon Pair Mass", 100, 0., 2000., 100, 0., 2000.)

filenamebase = sys.argv[1]
infile = TFile(filenamebase)
filename = filenamebase[50:] #fix
print(filename)
inevents = infile.Events

print("tree is loaded.")

countertotalp = 0
countervec0 = 0
countervec1 = 0
countervec2 = 0
countertotalevents = 0

for e in inevents: #can replace T with any file tree since the process is the same for all
    countertotalevents +=1
    vectors = []
    genpartvectors = []
    genpartvectmomid = []
    # print("event has starts:")
    pdgid = e.GenPart_pdgId
    motherpdgid = e.GenPart_genPartIdxMother
    gen_pt = e.GenPart_pt
    gen_eta = e.GenPart_eta
    gen_phi = e.GenPart_phi
    gen_mass = e.GenPart_mass
    # gen_energy = e.GenPart_energy
    p_pt = e.Photon_pt
    p_eta = e.Photon_eta
    p_phi = e.Photon_phi
    p_mass = e.Photon_mass
    # p_energy1 = e.Photon_dEscaleDown
    # p_energy2 = e.Photon_dEscaleUp
    # p_energy3 = e.Photon_dEsigmaDown
    # p_energy4 = e.Photon_dEsigmaUp
    # p_energy5 = e.Photon_eCorr # Up to NanoAOD10, residual energy scale and resolution corrections are applied to the stored electrons to match the data. The original four-momentum (as stored in MiniAOD) can be obtained by rescaling by the reciprocal of Photon_eCorr.
    # # ratio of the calibrated energy/miniaod energy
    # p_energy6 = e.Photon_hoe
    n_pho = len(p_pt)
    n_genpart = len(pdgid) #same length as mompdgid
    # print("event", countertotalevents)
    pdgidlist = []
    # print("event", countertotalevents)
    # for i in range(len(p_mass)):
    #     # print(p_mass[i])
    #     # print(p_energy1[i])
    #     # print(p_energy2[i])
    #     # print(p_energy3[i])
    #     # print(p_energy4[i])
    #     print(p_energy5[i])
    for i in range(0,n_genpart):
        part1 = pdgid[i]
        pdgidlist.append(part1)
    for i in range(n_genpart):
        part1 = pdgid[i]
        locmompart1 = motherpdgid[i]
        # print(part1, part2)
        if part1 == 22:# and (part2 == 9000121 or part2 == 9000025):
            vtemp2 = TLorentzVector()
            # vtemp2.SetPtEtaPhiE(gen_pt[i], gen_eta[i], gen_phi[i], gen_mass[i])
            vtemp2.SetPtEtaPhiM(gen_pt[i], gen_eta[i], gen_phi[i], gen_mass[i])
            genpartvectors.append(vtemp2)
            # genpartvectors.append(TLorentzVector(gen_pt[i], gen_eta[i], gen_phi[i], gen_energy[i]))
            genpartvectmomid.append(pdgidlist[locmompart1])
    if genpartvectmomid[0] == 9000121 and genpartvectmomid[1] == 9000025:
        genV = genpartvectors[0]+genpartvectors[1]+genpartvectors[2]
        # print(genpartvectmomid)
        H_genmasstot.Fill(genV.M())
    # print(genpartvectmomid)
    # print(n_pho)

    if n_pho == 3:
        for i in range(0, n_pho):
            vtemp1 = TLorentzVector()
            # vtemp1.SetPtEtaPhiE(p_pt[i], p_eta[i], p_phi[i], p_mass[i])
            vtemp1.SetPtEtaPhiM(p_pt[i], p_eta[i], p_phi[i], p_mass[i])
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
# C.Print("Test32D2pho3pho5.pdf")

# C = TCanvas()
# C.cd()
# H_genmasstot.Draw("hist")
# # H_massduo.Draw("hist")
# C.Print("TestNanoPhoMass1.pdf")

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
elif testnamechar[firstnum+8] == '-':
    largemass = str(testnamechar[firstnum+2])+str(testnamechar[firstnum+3])+str(testnamechar[firstnum+4])
    # smallmass = str(testnamechar[firstnum+9])+str(testnamechar[firstnum+10])
    numcount = firstnum+9
    testnamecharlooper = testnamechar[numcount]
    smallmass = ''
    while testnamecharlooper != '_':
        smallmass += str(testnamecharlooper)
        numcount += 1
        testnamecharlooper = testnamechar[numcount]
else:
    largemass = str(testnamechar[firstnum+2])+str(testnamechar[firstnum+3])
    # smallmass = str(testnamechar[firstnum+9])+str(testnamechar[firstnum+10])
    numcount = firstnum+8
    testnamecharlooper = testnamechar[numcount]
    smallmass = ''
    while testnamecharlooper != '_':
        smallmass += str(testnamecharlooper)
        numcount += 1
        testnamecharlooper = testnamechar[numcount]

# print(largemass, smallmass)
# ~~ Importing efficiency info into a csv file ~~
with open('efficiencyinfo1.csv', 'a', newline='') as csvfile:
    test2writer = csv.writer(csvfile, dialect='excel')
    test2writer.writerow([largemass] + [smallmass] + [countertotalevents] + [countertotalp] + [pctvec0] + [pcttotalevent])
