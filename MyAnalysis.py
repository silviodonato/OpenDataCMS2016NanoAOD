from __future__ import print_function, division, absolute_import

import os
import copy

import ROOT

from Samples import samp, file_path, histo_path


class MyAnalysis(object):
    def __init__(self, sample, xsec, lumi, maxEvents=-1):

        """ The Init() function is called when an object MyAnalysis is initialised
        The tree corresponding to the specific sample is picked up
        and histograms are booked.
        """

        # self._tree = ROOT.TTree()
        if sample not in samp and sample != "data" and not "Run20" in sample:
            raise RuntimeError("Sample {} not valid. Please choose among these: {}".format(sample,
                                                                                           list(samp)))
        self.histograms = {}
        self.sample = sample
        filename = os.path.join(file_path, sample + ".root")
        if not os.path.isfile(filename):
            raise ValueError("{} is not an existing file!".format(filename))
        self._file = ROOT.TFile.Open(filename)
        self._file.cd()
        # tree = self._file.Get("Events")
        self._tree = self._file.Get("Events")
        self.xsec = xsec
        self.lumi = lumi
        self.nEvents = self._tree.GetEntries()
        self.maxEvents = maxEvents
        print("Number of entries for {}: {}".format(self.sample, self.nEvents))

        # self._tree.SetBranchStatus("*",0)
        # self._tree.SetBranchStatus("run",1)
        # self._tree.SetBranchStatus("luminosityBlock",1)
        # self._tree.SetBranchStatus("event",1)
        # self._tree.SetBranchStatus("nMuon",1)
        # self._tree.SetBranchStatus("Muon_pt",1)
        # self._tree.SetBranchStatus("Muon_eta",1)
        # self._tree.SetBranchStatus("Muon_phi",1)
        # self._tree.SetBranchStatus("Muon_mass",1)
        # self._tree.SetBranchStatus("Muon_pfRelIso03_all",1)
        # self._tree.SetBranchStatus("genWeight",1)

        ### Book histograms
        self.bookHistos()

    def getTree(self):
        return self._tree

    def getHistos(self):
        return self.histograms

    def bookHistos(self):
        h_nJet = ROOT.TH1F("NJet", "#of jets", 6, -0.5, 6.5)
        h_nJet.SetXTitle("%# of jets")
        self.histograms["NJet"] = h_nJet

        h_nJetFinal = ROOT.TH1F("NJetFinal", "#of jets", 6, -0.5, 6.5)
        h_nJetFinal.SetXTitle("%# of jets")
        self.histograms["NJetFinal"] = h_nJetFinal

        h_MuonIso = ROOT.TH1F("Muon_Iso", "Muon Isolation", 25, 0., 3.)
        h_MuonIso.SetXTitle("Muon Isolation")
        self.histograms["Muon_Iso"] = h_MuonIso

        h_NIsoMu = ROOT.TH1F("NIsoMu", "Number of isolated muons", 5, -0.5, 5.5)
        h_NIsoMu.SetXTitle("Number of isolated muons")
        self.histograms["NIsoMu"] = h_NIsoMu

        h_MuonPt = ROOT.TH1F("Muon_Pt", "Muon P_T", 50, 0., 200.)
        h_MuonPt.SetXTitle("Muon P_T")
        self.histograms["Muon_Pt"] = h_MuonPt

        h_METpt = ROOT.TH1F("MET_Pt", "MET P_T", 25, 0., 300.)
        h_METpt.SetXTitle("MET P_T")
        self.histograms["MET_Pt"] = h_METpt

        h_JetPt = ROOT.TH1F("Jet_Pt", "Jet P_T", 50, 0., 200.)
        h_JetPt.SetXTitle("Jet P_T")
        self.histograms["Jet_Pt"] = h_JetPt

        h_JetBtag = ROOT.TH1F("Jet_Btag", "Jet B tag", 10, 1., 6.)
        h_JetBtag.SetXTitle("Jet B tag")
        self.histograms["Jet_btag"] = h_JetBtag

        h_NBtag = ROOT.TH1F("NBtag", "Jet B tag", 4, 0.5, 4.5)
        h_NBtag.SetXTitle("Number of B tagged jets")
        self.histograms["NBtag"] = h_NBtag


    def saveHistos(self):
        outfilename = os.path.join(histo_path, self.sample + "_histos.root")
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
        print(self.xsec,self.lumi,count , self.nEvents,nevts, self.xsec*self.lumi/count * self.nEvents/nevts)
            # weight = weight * self.nEvents/nevts ## larger weight if only a fraction of events is used
        tree = self.getTree()
        muon = ROOT.TLorentzVector()

        ### This is the place where to implement the analysis strategy: study of most sensitive variables
        ### and signal-like event selection
        for entry,event in enumerate(tree):
            if entry%1000==0: print(entry)
            if entry>=nevts: break
            if hasattr(event,"genWeight"):  ## is MC
                w = weight * (event.genWeight>0)
            else: 
                w = self.nEvents / nevts ## for data, ==1 if all events are processed

            ### Muon selection - Select events with at least 1 isolated muon
            ### with pt>25 GeV to match trigger requirements
            muonPtCut = 25
            muonRelIsoCut = 0.05
            nIsoMu = 0

            for m in range(event.nMuon):
                self.histograms["Muon_Iso"].Fill(event.Muon_tkRelIso[m], w)
                if (event.Muon_mediumId[m] == 1) and (event.Muon_tkIsoId[m] == 1):
                    nIsoMu += 1
                    # # muon.SetPtEtaPhiM(event.Muon_pt[m], event.Muon_eta[m], event.Muon_phi[m], event.Muon_mass[m])
                    # if muon.Pt() > muonPtCut and (event.Muon_pfRelIso03_all[m] / muon.Pt()) < muonRelIsoCut:
                    #     nIsoMu += 1
                    #     self.histograms["Muon_Pt"].Fill(muon.Pt(), w)
            self.histograms["NIsoMu"].Fill(nIsoMu, w)
            # print(self.histograms["NIsoMu"].Integral())

        self.saveHistos()
