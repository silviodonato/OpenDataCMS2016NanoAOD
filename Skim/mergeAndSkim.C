// xrdfs  root://eospublic.cern.ch locate /eos/opendata/cms/Run2016H/SingleMuon/NANOAOD/UL2016_MiniAODv2_NanoAODv9-v1/

// docker run -it --name my_od -P -p 5901:5901 -p 6080:6080 -v /home/sdonato/CMS/OpenDataCavasinni:/home/sdonato/CMS/OpenDataCavasinni  cmsopendata/cmssw_10_6_30-slc7_amd64_gcc700 /bin/bash
// https://opendata.cern.ch/record/30563
// https://opendata.cern.ch/record/30563/files/CMS_Run2016H_SingleMuon_NANOAOD_UL2016_MiniAODv2_NanoAODv9-v1_70000_file_index.txt

#include <fstream> // Include for ifstream
#include"TString.h"
#include"TChain.h"
#include"TTree.h"
#include"TFile.h"
#include"TH1F.h"
#include"TTreeFormula.h"
#include"TLorentzVector.h"
#include <iostream>


std::vector<TLorentzVector> parts;

float computeMass(float pt, float eta, float phi, float mass, int iteration, int length){
    using namespace std;
    float value = 0;
    if(iteration==0){
        parts.clear();
    }
    TLorentzVector part;
    part.SetPtEtaPhiM(pt, eta, phi, mass);
    parts.push_back(part);
    if(iteration==length-1){
        if(parts.size()<2) return -1;
        float maxMass = -1;
        // Loop over all combinations of pairs of particles
        for (size_t i = 0; i < parts.size(); ++i) {
            for (size_t j = i + 1; j < parts.size(); ++j) {
                // Compute invariant mass using TLorentzVector's method
                double mass = (parts[i] + parts[j]).M();
                if (mass > maxMass) {
                    maxMass = mass;
                }
            }
        }        
        return maxMass;
    }
    else return 0;
}

float computeMass4muons(float pt, float eta, float phi, float mass, int iteration, int length){
    using namespace std;
    float value = 0;
    if(iteration==0){
        parts.clear();
    }
    TLorentzVector part;
    part.SetPtEtaPhiM(pt, eta, phi, mass);
    parts.push_back(part);
    if(iteration==length-1){
        if(parts.size()<2) return -1;
        float maxMass = -1;
        // Loop over all combinations of pairs of particles
        for (size_t i = 0; i < parts.size(); ++i) {
            for (size_t j = i + 1; j < parts.size(); ++j) {
                for (size_t k = j + 1; k < parts.size(); ++j) {
                    for (size_t l = k + 1; l < parts.size(); ++j) {
                        // Compute invariant mass using TLorentzVector's method
                        double mass = (parts[i] + parts[j]).M();
                        if (mass > maxMass) {
                            maxMass = mass;
                        }
                    }
                }
            }
        }        
        return maxMass;
    }
    else return 0;
}

void skimAndMergeFile(TString inputFiles, TString prefix=""){ //, TString outputFile
    TString outputFile;
    // Output file name is the same as the input file name, but with the extension .root
    outputFile = inputFiles;
    // split the path and get the last part
    // split "opendata/cms"
    outputFile = outputFile(outputFile.Index("opendata/cms")+13,outputFile.Length());
    outputFile.ReplaceAll("/","_");

    // outputFile = outputFile(outputFile.Last('/')+1,outputFile.Length());

    if(prefix!="") outputFile = prefix+"/"+outputFile;

    cout << "I'm doing "<< outputFile << endl;
    TFile* fileout = new TFile(outputFile,"recreate");
    TChain* tree = new TChain("Events");
    // Read CMS_Run2016H_SingleMuon_NANOAOD_UL2016_MiniAODv2_NanoAODv9-v1_70000_file_index.txt
   
    tree->Add(inputFiles);

    // Disable FatJet branches
    tree->SetBranchStatus("FatJet*",0);
    tree->SetBranchStatus("HLT_*",0);
    tree->SetBranchStatus("HLT_*",0);
    tree->SetBranchStatus("DST_*",0);
    tree->SetBranchStatus("HLT_IsoMu*",1);
    tree->SetBranchStatus("L1_*",0);
    tree->SetBranchStatus("L1_SingleMu*",1);
    tree->SetBranchStatus("nSV*",0);
    tree->SetBranchStatus("SV_*",0);
    tree->SetBranchStatus("LowPtElectron_*",0);
    tree->SetBranchStatus("nLowPtElectron",0);
    tree->SetBranchStatus("TrigObj_*",0);
    tree->SetBranchStatus("nTrigObj",0);
    tree->SetBranchStatus("*SubJet*",0);
    tree->SetBranchStatus("*Proton*",0);
    tree->SetBranchStatus("*SoftActivity*",0);
    tree->SetBranchStatus("*PPS*",0);
    tree->SetBranchStatus("L1Pre*",0);
    tree->SetBranchStatus("*boosted*",0);
    tree->SetBranchStatus("*IsoTrack*",0);
    tree->SetBranchStatus("*CorrT1*",0);
    
    // tree->SetBranchStatus("*",0);
    // tree->SetBranchStatus("run",1);
    // tree->SetBranchStatus("event",1);
    // tree->SetBranchStatus("luminosityBlock",1);
    // tree->SetBranchStatus("bunchCrossing",1);
    // tree->SetBranchStatus("*Electron*",1);
    // tree->SetBranchStatus("*FsrPhoton*",1);
    // tree->SetBranchStatus("*Jet*",1);
    // tree->SetBranchStatus("MET_*",1);
    // tree->SetBranchStatus("PuppiMET_*",1);
    // tree->SetBranchStatus("*Muon*",1);
    // tree->SetBranchStatus("*Photon*",1);
    


    fileout->cd();
    int entries = tree->GetEntries();
    if(entries<=0) {
        cout<<"No entries in file "<<inputFiles<<endl;
        throw 1;
    }
    TTree* newTree = tree->CloneTree(0);
    
    // main skim
    //TTreeFormula* cut = new TTreeFormula("cut","HLT_IsoMu24 && Sum$(computeMass(Muon_pt, Muon_eta, Muon_phi, Muon_mass, Iteration$, Length$))>50 ",tree);
    
    // Prescale
//    TTreeFormula* cut = new TTreeFormula("cut","event%20==0 ",tree); 
    
    // 4 muons
//    TTreeFormula* cut = new TTreeFormula("cut","(nMuon>=4) ",tree); 

    // 2 muons + 2 electrons
//    TTreeFormula* cut = new TTreeFormula("cut","(nMuon>=2) && (nElectron>=2) ",tree); 
 //   TTreeFormula* cut = new TTreeFormula("cut","(Sum$(Electron_mvaFall17V2Iso_WPL)>=2 && Sum$( Muon_looseId && Muon_tkIsoId>=1)>=2) ",tree);
 //   TTreeFormula* cut = new TTreeFormula("cut","Sum$( Muon_looseId && Muon_tkIsoId>=1)>=4",tree);
    TTreeFormula* cut = new TTreeFormula("cut","Sum$( Muon_looseId && Muon_tkIsoId>=1)>=2",tree);
 
//    TTreeFormula* puFilter = new TTreeFormula("puFilter","ptHat>maxPUptHat",tree);
    
    cout << "Total entries " << entries << endl;
   for(int i=0; i<tree->GetEntries(); i++){
        tree->GetEntry(i);
        cut->UpdateFormulaLeaves();
        // puFilter->UpdateFormulaLeaves();
        if(cut->EvalInstance()){ //puFilter->EvalInstance() && 
            newTree->Fill();
        }
        if(i%100==0){
            cout<<i<<endl;
        }
    }
    newTree->Write();

    /// Add histogram with Count ///
    TH1F* Count = new TH1F("Count","Count",1,0,1);
    Count->SetBinContent(1,entries);
    Count->Write();
    fileout->Close();
}

void mergeAndSkim(TString filename, TString prefix="") {
    // skimAndMergeFile(
    //     // https://opendata.cern.ch/record/30563/files/CMS_Run2016H_SingleMuon_NANOAOD_UL2016_MiniAODv2_NanoAODv9-v1_70000_file_index.txt
    //     "CMS_Run2016H_SingleMuon_NANOAOD_UL2016_MiniAODv2_NanoAODv9-v1_70000_file_index.txt", 
    //     "SingleMuon.root"
    //     );

    // Take input file from command line - 1st argument
    skimAndMergeFile(filename, prefix);

    // skimAndMergeFile(
    //     "root://storage01.lcg.cscs.ch//pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/HLT_Ntuple_Hbb_Signal_v5_noAODSIM/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/crab_HLT_Ntuple_Hbb_Signal_v5_noAODSIMQCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/170411_120207/0000/tree_*.root", 
    //     "QCD15to30.root"
    //     );
    // skimAndMergeFile(
    //     "root://storage01.lcg.cscs.ch//pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/HLT_Ntuple_Hbb_Signal_v5_noAODSIM/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/crab_HLT_Ntuple_Hbb_Signal_v5_noAODSIMQCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/170411_120216/0000/tree_*.root", 
    //     "QCD30to50.root"
    //     );
    // skimAndMergeFile(
    //     "root://storage01.lcg.cscs.ch//pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/HLT_Ntuple_Hbb_Signal_v5_noAODSIM/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/crab_HLT_Ntuple_Hbb_Signal_v5_noAODSIMQCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/170411_120223/0000/tree_*.root",
    //     "QCD50to80.root"
    //     );
    // skimAndMergeFile(
    //     "root://storage01.lcg.cscs.ch//pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/HLT_Ntuple_Hbb_Signal_v5_noAODSIM/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/crab_HLT_Ntuple_Hbb_Signal_v5_noAODSIMQCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/170411_120232/0000/tree_*.root",
    //     "QCD80to120.root"
    //     );
    // skimAndMergeFile(
    //     "root://storage01.lcg.cscs.ch//pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/HLT_Ntuple_Hbb_Signal_v5_noAODSIM/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/crab_HLT_Ntuple_Hbb_Signal_v5_noAODSIMQCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/170411_120240/0000/tree_*.root",
    //     "QCD120to170.root"
    //     );
    // skimAndMergeFile(
    //     "root://storage01.lcg.cscs.ch//pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/HLT_Ntuple_Hbb_Signal_v5_noAODSIM/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/crab_HLT_Ntuple_Hbb_Signal_v5_noAODSIMQCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/170411_120247/0000/tree_*.root",
    //     "QCD170to300.root"
    //     );
    // skimAndMergeFile(
    //     "root://storage01.lcg.cscs.ch//pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/HLT_Ntuple_Hbb_Signal_v5_noAODSIM/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/crab_HLT_Ntuple_Hbb_Signal_v5_noAODSIMQCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/170411_120259/0000/tree_*.root",
    //     "QCD300to470.root"
    //     );
    // skimAndMergeFile(
    //     "root://storage01.lcg.cscs.ch//pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/HLT_Ntuple_Hbb_Signal_v5_noAODSIM/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/crab_HLT_Ntuple_Hbb_Signal_v5_noAODSIMQCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/170411_120307/0000/tree_*.root",
    //     "QCD470to600.root"
    //     );
    // skimAndMergeFile(
    //     "root://storage01.lcg.cscs.ch//pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/HLT_Ntuple_Hbb_Signal_v5_noAODSIM/GluGluToHHTo4B_node_SM_13TeV-madgraph/crab_HLT_Ntuple_Hbb_Signal_v5_noAODSIMGluGluToHHTo4B_node_SM_13TeV-madgraph/170411_120500/0000/tree_*.root", 
    //     "ggHH4b.root"
    //     );
    // skimAndMergeFile(
    //     "root://storage01.lcg.cscs.ch//pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/HLT_Ntuple_Hbb_Signal_v5_noAODSIM/ttHTobb_M125_TuneCUETP8M2_13TeV-powheg-pythia8/crab_HLT_Ntuple_Hbb_Signal_v5_noAODSIMttHTobb_M125_TuneCUETP8M2_13TeV-powheg-pythia8/170411_101616/0000/tree_*.root",
    //     "ttHbb.root"
    //     );
    // skimAndMergeFile(
    //     "root://storage01.lcg.cscs.ch//pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/HLT_Ntuple_Hbb_Signal_v5_noAODSIM/VBFHToBB_M-125_13TeV_powheg_pythia8_weightfix/crab_HLT_Ntuple_Hbb_Signal_v5_noAODSIMVBFHToBB_M-125_13TeV_powheg_pythia8_weightfix/170411_120419/0000/tree_*.root",
    //     "VBFHbb.root"
    //     );
    // skimAndMergeFile(
    //     "root://storage01.lcg.cscs.ch//pnfs/lcg.cscs.ch/cms/trivcat/store/user/sdonato/HLT_Ntuple_Hbb_Signal_v5_noAODSIM/GluGluHToBB_M125_13TeV_powheg_pythia8/crab_HLT_Ntuple_Hbb_Signal_v5_noAODSIMGluGluHToBB_M125_13TeV_powheg_pythia8/170411_120440/0000/tree_*.root",
    //     "ggHbb.root"
    //     );
}

