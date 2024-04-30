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
#include <iostream>

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

    fileout->cd();
    int entries = tree->GetEntries();
    if(entries<=0) {
        cout<<"No entries in file "<<inputFiles<<endl;
        throw 1;
    }
    TTree* newTree = tree->CloneTree(0);
    
    TTreeFormula* cut = new TTreeFormula("cut","HLT_IsoMu24_eta2p1",tree);
//    TTreeFormula* puFilter = new TTreeFormula("puFilter","ptHat>maxPUptHat",tree);
    
   for(int i=0; i<tree->GetEntries(); i++){
        tree->GetEntry(i);
        cut->UpdateFormulaLeaves();
        // puFilter->UpdateFormulaLeaves();
        if(cut->EvalInstance()){ //puFilter->EvalInstance() && 
            newTree->Fill();
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

