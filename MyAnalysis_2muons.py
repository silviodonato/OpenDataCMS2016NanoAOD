from __future__ import print_function, division, absolute_import

Z_mass = 91.1876

import os
import copy

import ROOT


import math
    
def compute_invariant_mass(muon1, muon2):
    pt1, eta1, phi1, mass1 = muon1
    pt2, eta2, phi2, mass2 = muon2
    # Calculate energy and momentum components for particle 1
    E1 = math.sqrt(pt1**2 * math.cosh(eta1)**2 + mass1**2)
    px1 = pt1 * math.cos(phi1)
    py1 = pt1 * math.sin(phi1)
    pz1 = pt1 * math.sinh(eta1)
    
    # Calculate energy and momentum components for particle 2
    E2 = math.sqrt(pt2**2 * math.cosh(eta2)**2 + mass2**2)
    px2 = pt2 * math.cos(phi2)
    py2 = pt2 * math.sin(phi2)
    pz2 = pt2 * math.sinh(eta2)
    
    # Calculate the components of the total 4-momentum
    E = E1 + E2
    px = px1 + px2
    py = py1 + py2
    pz = pz1 + pz2
    
    # Calculate the invariant mass
    invariant_mass = math.sqrt(E**2 - px**2 - py**2 - pz**2)
    
    return invariant_mass

class MyAnalysis(object):
    def __init__(self, sample, xsec, lumi, fileName, histo_folder, maxEvents=-1, isGoodData=None):

        """ The Init() function is called when an object MyAnalysis is initialised
        The tree corresponding to the specific sample is picked up
        and histograms are booked.
        """

        # self._tree = ROOT.TTree()
        # if sample not in samp and sample != "data" and not "Run20" in sample:
        #     raise RuntimeError("Sample {} not valid. Please choose among these: {}".format(sample,
        #                                                                                    list(samp)))
        self.histograms = {}
        self.sample = sample
        if not os.path.isfile(fileName):
            raise ValueError("{} is not an existing file!".format(fileName))
        self._file = ROOT.TFile.Open(fileName)
        self._file.cd()
        # tree = self._file.Get("Events")
        self._tree = self._file.Get("Events")
        if self._tree == None:
            raise ValueError("TTree not found in file %s" % fileName)
        self.xsec = xsec
        self.lumi = lumi
        if isGoodData:
            self.isGoodData = isGoodData
        else:
            self.isGoodData = None
        self.fileName = fileName
        self.histo_folder = histo_folder
        self.nEvents = self._tree.GetEntries()
        self.maxEvents = maxEvents
        print("Number of entries for {}: {}".format(self.sample, self.nEvents))

        ### Book histograms
        self.bookHistos()

    def bookHistos(self):

        histos ={
            "Muon_Pt": ((50, 0., 100.), "Muon P_T"),
            "Muon_Eta": ((60, -3, +3), "Muon Eta"),
            "DiMuonMass": ((100, 70., 120.), "Di-muon mass"),
            "DiMuonMass1k": ((10000, 70., 120.), "Di-muon mass"),
            "NGoodMuons": ((5, 0, 5), "Number of good muons"),
        }

        ## Create histograms
        for h in histos:
            ##Eg. self.histograms["NJet"] = ROOT.TH1F("NJet", "Number of jets", 6, -0.5, 6.5)
            self.histograms[h] = ROOT.TH1F(h, histos[h][1], *histos[h][0])
            self.histograms[h].GetXaxis().SetTitle(histos[h][1])

    def saveHistos(self):
        outfilename = os.path.join(self.histo_folder, self.sample + "_histos.root")
        outfile = ROOT.TFile.Open(outfilename, "RECREATE")
        outfile.cd()
        for h in self.histograms.values():
            h.Write()
        outfile.Close()
        print("Histograms saved in {}".format(outfilename))

    ### processEvents run the function processEvent on each event stored in the tree
    def processEvents(self):
        nevts = self.nEvents
        count = self._file.Get("Count").GetBinContent(1)
        if self.maxEvents>0:
            nevts = min(nevts, self.maxEvents)
        weight = self.xsec*self.lumi/count * self.nEvents/nevts
        print("Xsec: ", self.xsec)
        print("Lumi: ", self.lumi)
        print("Count: ", count)
        print("NEvents: ", self.nEvents)
        print("Nevts: ", nevts)
        print("Weight: ", weight)
        tree = self._tree

        ### This is the place where to implement the analysis strategy: study of most sensitive variables
        ### and signal-like event selection
        count = 0
        for entry,event in enumerate(tree):
            if entry%1000==0: print(entry)
            if entry>=nevts: break
            if not event.HLT_IsoMu24:
                continue
            if hasattr(event,"genWeight"):  ## is MC
                w = weight * (event.genWeight>0)                
            else: 
                w = self.nEvents / nevts ## for data, ==1 if all events are processed
                if not self.isGoodData(event.run, event.luminosityBlock):
                    continue

            muons_p = []
            muons_n = []

            nGoodMuons = 0
            for m in range(tree.nMuon):
                if tree.Muon_tkIsoId[m]>=1 and tree.Muon_looseId[m]==1 and tree.Muon_pt[m]>5 and tree.Muon_sip3d[m]<4 and abs(tree.Muon_eta[m])<2.4: #abs(tree.Muon_dxy[m])<0.01
                    nGoodMuons += 1
                    if tree.Muon_charge[m] == 1:
                        muons_p.append((tree.Muon_pt[m], tree.Muon_eta[m], tree.Muon_phi[m], tree.Muon_mass[m]))
                    elif tree.Muon_charge[m] == -1:
                        muons_n.append((tree.Muon_pt[m], tree.Muon_eta[m], tree.Muon_phi[m], tree.Muon_mass[m]))
                    else:
                        print("Muon charge not 1 or -1")

                    self.histograms["Muon_Eta"].Fill(tree.Muon_eta[m], w)
                    self.histograms["Muon_Pt"].Fill(tree.Muon_pt[m], w)

            self.histograms["NGoodMuons"].Fill(nGoodMuons, w)

            if len(muons_p)<1 or len(muons_n)<1:
                continue

            dimuon_mass = compute_invariant_mass(muons_p[0], muons_n[0])

            self.histograms["DiMuonMass"].Fill(dimuon_mass, w)
            self.histograms["DiMuonMass1k"].Fill(dimuon_mass, w)
            # print(self.histograms["NIsoMu"].Integral())
            count += 1
        print("Calling saveHistos()")
        self.saveHistos()
        if count == 0:
            print("WARNING. No events accepted for sample %s" % self.sample)
        print("COUNT: ", count)
