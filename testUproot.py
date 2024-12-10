import ROOT
from ROOT import *
from array import array
import sys
import csv
import uproot

# Standard Includes: ----------------------------------------#
import os
import array
from array import *
import glob
import math
import ROOT
from ROOT import *
import sys
import itertools
from itertools import *
from optparse import OptionParser
# Obviously can only be run in a CMSSW Framework
from DataFormats.FWLite import * 
from HLTrigger import *
from ctypes import POINTER, c_int
import uproot
# -----------------------------------------------------------#

## This file is used to learn how to use uproot to analyze files.

print("ROOT, uproot is loaded")

H_nPhotons = TH1I("N_pho", ";Number of pat::photons;Events", 10, 0, 10)

G = TFile("BkkToGRadionToGGG_M1-3000_R0-60_2018_FlatAODv3_0.root")
U = G.Get("flattener/tree")
upG = uproot.open("BkkToGRadionToGGG_M1-3000_R0-60_2018_FlatAODv3_0.root")
# upGf = upG["flattener"]
# upGft = upGf["tree"]
# print(upGft.keys())
# upN = uproot.open("/project01/ndcms/gziemyt2/RSTriPhoton/mc/NanoAODv9/BkkToGRadionToGGG_M1-20_R0-0p1_2018_NanoAODv9_0.root")
# upN = uproot.open("~/Public/scouting_ntuple_1.root")
upN = uproot.open("/project01/ndcms/gziemyt2/DiphotonGun/AtoGG_500events1.0Ma_MiniAOD.root")
N = TFile("/project01/ndcms/gziemyt2/DiphotonGun/AtoGG_15events_MiniAOD.root")
NEvents = N.Events
NParamSets = N.ParameterSets
# print(upN.keys())
upNE = upN["Events"]
upNEe = upNE["EcalRecHitsSorted_reducedEgamma_reducedEBRecHits_PAT."]
# # print(upNE.keys())

def HardGet(e, L, H): # shorthand def for getting collection from event
	e.getByLabel(L, H)
	if H.isValid() and len(H.product()) > 0: 
		return H.product()
	return False


with open("testfile7output.txt", "a") as f:
  print(upNEe.keys(), file=f)

# NEventsSelections = NEvents.EventSelections

# for e in NParamSets:
#     print(e)

# # F = TFile("/project01/ndcms/gziemyt2/RSTriPhoton/test/mc/NanoAODv9/BkkToGRadionToGGG_M1-180_R0-3p6_2018_NanoAODv9_0.root")
# F = TFile("/afs/crc.nd.edu/user/g/gziemyt2/data_analysis/CMSSW_12_3_6/src/AtoGammaGammaFlatMoE_10events.root")
# file = uproot.open("/afs/crc.nd.edu/user/g/gziemyt2/data_analysis/CMSSW_12_3_6/src/AtoGammaGammaFlatMoE_10events.root")
# F = TFile("AtoGammaGammaFlatMoE_NanoAOD_25events.root")
# E = F.Events
# # events = uproot.open("/afs/crc.nd.edu/user/g/gziemyt2/data_analysis/CMSSW_12_3_6/src/AtoGammaGammaFlatMoE_10events.root:events")
# # print(file)
# events = file["Events"]
# # events2 = F.Get("Events")
# # print(events2)
# # events = F.Events
# # print(events.keys())
# # print(len(events))
# # print(file.keys())
# # print(events.keys())
# # print(events.show())
# # print(events.values())
# # print(events["patPhotons_slimmedPhotons__PAT"].array())
# # print(file["Events"])
# testpho = events["patPhotons_slimmedPhotons__PAT."]
# testphop = testpho["patPhotons_slimmedPhotons__PAT.obj"] # no cigar
# eventsel = events["EventSelections"] #nothing
# digi2raw = events["recoGenParticles_genPUProtons_genPUProtons_DIGI2RAW."]
# parentage = file["Parentage"]
# parentaged = parentage["Description"] #empty
# runs = file['Runs']

# with open("testfile7output.txt", "a") as f:
#   print(runs.keys(), file=f)

# # Events = F.Events
# # # F.Print()
# # # F.Show(4)
# # # print(Events)
# # T = F.Get("flattener/tree")

# # for e in file:
# #     print(e)


# # for e in range(len(events)):
# #     # print(len(e))
# #     print(events[e])

# # for e in events2:
# #     # print(e)
# #     print(e.phoEt())


    

# for e in E:
#     # p_pt = e.patpho_pt
#     # p_pt = e.phoEt
#     # p_pt = events.patPhotons_slimmedPhotons__PAT
#     p_pt = e.Photon_pt
#     # print(len(p_pt))
#     H_nPhotons.Fill(len(p_pt))
#     # branches = T.GetEntry(e)
#     # print(branches)
#     # print("i")
    

# # for entry in Events:
# #     # print(entry.Photon_pt)
# #     # var1 = entry.p_pt
# #     # print(len(var1))
# #     print(entry)

# # T = F.Get("Events")
# # T.SetBranchAddress("Photon_pt", Photon_pt)
# # p_pttot = T.GetBranch("Photon_pt")
# # # print(len(p_pttot))
# # print(p_pttot)

# # entries = T.GetEntries()
# # for i in range(entries):
# #     T.GetEntry(i)
# #     H_nPhotons.Fill(len(Photon_pt))
# #     print(len(Photon_pt))


# # for e in T:
# #     p_pt = e.patpho_pt
# #     #print(len(p_pt))
# #     H_nPhotons.Fill(len(p_pt))

# # print("tree is loaded")

# # C = TCanvas()
# # C.cd()
# # H_nPhotons.Draw("hist")
# # C.Print("TestNano1.pdf")