import ROOT
from ROOT import *
from array import array

print("ROOT is loaded.")

# ~~ Comment this in or out if need variable bin lengths
## variable bin length - array must be (NBins+1) from beginning to end of range
# binLowE = [2,4,9,15,20,22]
# binLowE = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, ]
# binLowE = []
# counter1 = 1
# NBins = 0
# for i in range(0,20):
#     binLowE.append(counter1)
#     counter1 += 0.5
#     NBins += 1
# counter2 = 11
# for i in range(0, 25):
#     binLowE.append(counter2)
#     counter2 += 1
#     NBins += 1
# counter3 = 38
# for i in range(0, 100):
#     binLowE.append(counter3)
#     counter3 += 2
#     NBins += 1
# counter4 = 242
# for i in range(0,50):
#     binLowE.append(counter4)
#     counter4 += 5
#     NBins += 1
# counter5 = 502
# for i in range(0, 40):
#     binLowE.append(counter5)
#     counter5 += 10
#     NBins += 1
# counter6 = 922
# for i in range(0, 40):
#     binLowE.append(counter6)
#     counter6 += 50
#     NBins += 1

# # print(binLowE)
# print(NBins)

# ~~ Setting up all the histograms
# histogram = TH1I(name, title, x dimension (bin, x start, x end))
# H_nPhotons = TH1I("N_pho", ";Number of pat::photons;Events", 10, 0, 10)
H_pt = TH1I("pT", ";all photon p_{T} (GeV):Events",100,0.,2000.)
H_masstot = TH1I("Mass", "Mass:Events", 100, 0., 5000.)
H_genmasstot = TH1I("genMass", "Mass:Events", 100, 0., 5000.)
# H_masstot = TH1I("Mass", "Mass:Events", (NBins-1), array('d',binLowE))
H_mass01 = TH1I("Mass01", "Mass:Events", 100, 0., 5000.)
H_mass12 = TH1I("Mass12", "Mass:Events", 100, 0., 5000.)
H_mass02 = TH1I("Mass02", "Mass:Events", 100, 0., 5000.)
H_massduo = TH1I("Massduo", "Mass:Events", 100, 0., 5000.)
# H_mass01 = TH1I("Mass01", "Mass:Events", (NBins-1), array('d',binLowE))
# H_mass12 = TH1I("Mass12", "Mass:Events", (NBins-1), array('d',binLowE))
# H_mass02 = TH1I("Mass02", "Mass:Events", (NBins-1), array('d',binLowE))
# H_massduo = TH1I("Massduo", "Mass:Events", (NBins-1), array('d', binLowE))

# ~~ Opening files and trees
F = TFile("BkkToGRadionToGGG_M1-1000_R0-20_2018_FlatAODv3_0.root")
G = TFile("BkkToGRadionToGGG_M1-3000_R0-60_2018_FlatAODv3_0.root")
T = F.Get("flattener/tree")
U = G.Get("flattener/tree")

print("tree is loaded.")

# pt is transverse momentum?? figure that out --> it is
# counter1=0
for e in T:
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
        if part1 == 22: # and (part2 == 9000121 or part2 == 9000025): --> these two ids aren't in the guide
            genpartvectors.append(TLorentzVector(gen_pt[i], gen_eta[i], gen_phi[i], gen_energy[i]))
            genpartvectmomid.append(part2)
    # if len(genpartvectors) ==3:
    #     counter1 += 1
    # if len(genpartvectmomid) < 3:
    #     break
    if genpartvectmomid[0] == 9000121 and genpartvectmomid[1] == 9000025: # this gets the 3 photon events (maybe)
        genV = genpartvectors[0]+genpartvectors[1]+genpartvectors[2]
        # print(genpartvectmomid)
    H_genmasstot.Fill(genV.M())
    # print(genpartvectmomid)

    if n_pho == 3:
        for i in range(0, n_pho):
            vectors.append(TLorentzVector(p_pt[i], p_eta[i], p_phi[i], p_energy[i]))
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
        H_masstot.Fill(Vmin) # plot mass and not energy
        H_mass01.Fill(V01.M())
        H_mass12.Fill(V12.M())
        H_mass02.Fill(V02.M())
    


    angles0 = []
    if len(vectors) == 3:
        for j in range(0,3):
            angles0.append(genpartvectors[0].DeltaR(vectors[j]))
    # # print(angles)
    # anglestemp = angles.copy()
    if len(angles0)==3:
        temp0 = min(angles0)
        res0 = [i for i, j in enumerate(angles0) if j == temp0]
        if res0[0] == 0:
            Vduo = vectors[1]+vectors[2]
        elif res0[0] == 1:
            Vduo = vectors[0]+vectors[2]
        elif res0[0] == 2:
            Vduo = vectors[0]+vectors[1]
        # print(Vduo)
        H_massduo.Fill(Vduo.M())
        # anglestemp.remove(temp0)
        # temp1 = min(anglestemp)
        # res1 = [i for i, j in enumerate(angles) if j == temp1]
        # anglestemp.remove(temp1)
        # temp2 = min(anglestemp)
        # res2 = [i for i, j in enumerate(angles) if j == temp2]
        # # print(res0[0], res1[0], res2[0])


    # angles0 = []
    # angles1 = []
    # angles2 = []
    # if len(vectors) > 2:
    #     for i in range(0,3):
    #         # angles0.append(genpartvectors[0].DeltaR(vectors[i]))
    #         angles1.append(genpartvectors[1].DeltaR(vectors[i]))
    #         angles2.append(genpartvectors[2].DeltaR(vectors[i]))
    #         # angles0.append(vectors[0].DeltaR(genpartvectors[i]))
    #         # angles1.append(vectors[1].DeltaR(genpartvectors[i]))
    #         # angles2.append(vectors[2].DeltaR(genpartvectors[i]))
    # print(angles0)
    # print(angles1)
    # print(angles2)
    # if len(angles1) > 2:
    #     # temp0 = min(angles0[0], angles0[1], angles0[2])
    #     # res0 = [i for i, j in enumerate(angles0) if j == temp0]
    #     temp1 = min(angles1)
    #     res1 = [i for i, j in enumerate(angles1) if j == temp1]
    #     temp2 = min(angles2)
    #     res2 = [i for i, j in enumerate(angles2) if j == temp2]
    #     # if res0 == res1 or res0 == res2 or res1 == res2:
    #     #     temp3 = min(temp0, temp1, temp2)
    #     #     if temp3 == temp0:
    #     #         temp4 = min(temp1, temp2)
                
        # print(res1[0], res2[0])
    
    # vectors = []
    # genpartvectors = []
    # genpartvectmomid = []
    # V = vectors[0] + vectors[1] + vectors[2]
    # print(V)
    
    #print(p_pt)
    # for i in range(n_pho):
    #      H_pt.Fill(p_pt[i])
    # H_nPhotons.Fill(p_mass)
    #print(len(p_pt))
    # H_nPhotons.Fill(len(p_eta)) #this just gives number of photons, since we're taking the length of each entry.
        #  patpho_pt and patpho_eta have the same number of photons

# ~~ Other tree
# for e in U:
#     # print("event has starts:")
#     p_pt = e.patpho_pt
#     p_eta = e.patpho_eta
#     p_phi = e.patpho_phi
#     p_mass = e.patpho_mass
#     p_energy = e.patpho_energy
#     n_pho = len(p_pt)
#     # print(n_pho)
#     if n_pho > 2:
#         for i in range(0, n_pho):
#             vectors.append(TLorentzVector(p_pt[i], p_eta[i], p_phi[i], p_energy[i]))
#             # vectors.append(TLorentzVector(p_pt[i], p_eta[i], p_phi[i], p_mass[i]))
#         # print(vectors)
#         V = vectors[0]+vectors[1]+vectors[2]
#         # print(V.E())
#         # H_mass.Fill(V.E())
#         vectors = []

# for e in T:
#     p_eta = e.patpho_eta
# print(counter1)

# ~~ Creating histograms
C = TCanvas()
C.cd()
# H_genmasstot.Draw("hist")
H_massduo.Draw("hist")
C.Print("Testmassduo4.pdf")
#Testpmass4.pdf is photon=3 events, p_energy as last vector comp
#Testpmass5.pdf is photon>2 events. There are some events with 4 photons?? p_energy as last vector comp
#Testpmass6.pdf is photon>2 events. p_mass as last vector comp. bad idea, it's just zeroes
#Testpmass7.pdf is photon>2 events for 3000
#Testpmass8.pdf is photon>2 events for 1000 and 3000.
#Testpmass9.pdf is photon>2 events for 1000, first two vectors in event.
#Testpmass10.pdf is photon>2 events for 1000, second two vectors in event.
#Testpmass11.pdf is photon>2 events for 1000, first and last vectors in event.
# was plotting V.E() before, switch to plotting V.M() now.
#Testpmass12.pdf is photon>2 events for 1000, plotting mass
#Testpmass13.pdf is photon>2 events for 1000, first two vectors in event.
#Testpmass14.pdf is photon>2 events for 1000, second two vectors in event.
#Testpmass15.pdf is photon>2 events for 1000, first and last vectors in event.
#Testpmass16.pdf is testing the variable binning
#Testpmass17.pdf is minimum masses
#Testpmass18.pdf is minimum masses up to 100 GeV (expecting a peak at 20 GeV but there isn't)
#Testpmass19.pdf
#Testmassduo.pdf is maybe the two photon pair and their masses :(
#Testmassduo2.pdf is the same thing with variable bin widths.
#Testmassduo3.pdf is the diphoton pair and their reconstructed energy.

# # Plotting histograms (multiple on one canvas)

# # hs1 = THStack("hs1","")
# # hs1.Add(H_mass01)
# # hs1.Add(H_mass12)
# # hs1.Add(H_mass02)

# C1 = TCanvas()
# C1.cd()
# # gStyle.SetOptTitle(kFALSE)
# gStyle.SetOptStat(0)
# # hs1.Draw("hist")
# H_mass12.Draw("PLC PMC hist")
# H_mass01.Draw("SAME PLC PMC hist")
# H_mass02.Draw("SAME PLC PMC hist")

# legend1 = TLegend(0.9,0.7,0.48,0.9)
# legend1.SetHeader("Legend","C")
# legend1.AddEntry(H_mass01, "Reconstructed mass of first two photons.")
# legend1.AddEntry(H_mass12, "Reconstructed mass of second two photons.")
# legend1.AddEntry(H_mass02, "Reconstructed mass of first and last photons.")
# legend1.Draw()

# C1.Print("vectphomass5.pdf")
# #vectphomass2 is variable binning with focus around small GeV, later bins too big though
