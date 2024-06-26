# OpenDataCMS2016NanoAOD
Code for students in University of Pisa to run a simplified H->4 lepton search using 2016 CMS open data based on NanoAOD format. 

## Plots

The code `python3 example.py` will make plots using the input files, lumi, and crosssection defined in [example.py](https://github.com/silviodonato/OpenDataCMS2016NanoAOD/blob/main/example.py).
The samples need to be defined also in [Samples.py](https://github.com/silviodonato/OpenDataCMS2016NanoAOD/blob/main/Samples.py#L22).
The histograms are defined in `bookHistos()` in [MyAnalysis.py](https://github.com/silviodonato/OpenDataCMS2016NanoAOD/blob/main/MyAnalysis.py#59).
The event selection is defined in `processEvent()` [MyAnalysis.py](https://github.com/silviodonato/OpenDataCMS2016NanoAOD/blob/main/MyAnalysis.py#L109).
The input files should be a file (or a symbolic link) with the same name of the samples (eg. `ggH.root`).
The input files are typically skimmed from a larger files, using the following Skim section.

## Skim

The code [mergeAndSkim.C](https://github.com/silviodonato/OpenDataCMS2016NanoAOD/blob/main/Skim/mergeAndSkim.C#L113C69-L113C80) apply the selection defined in `cut`,
and can used with `root -l mergeAndSkim.C++\(\"root://eospublic.cern.ch//eos/opendata/cms/Run2016H/SingleMuon/NANOAOD/UL2016_MiniAODv2_NanoAODv9-v1/70000/388AB3E1-8708-7D42-91BA-83E52373E808.root\"\)`.
To submit multiple jobs in parallel using `bsub`, use `python3 makeScriptAndSubmit.py` ([makeScriptAndSubmit.py](https://github.com/silviodonato/OpenDataCMS2016NanoAOD/blob/main/Skim/makeScriptAndSubmit.py)).
To resubmit crahsing jobs, please have a look at [resbumit.py](https://github.com/silviodonato/OpenDataCMS2016NanoAOD/blob/main/Skim/resubmit.py)
The input files can be the CMS NanoAOD open data, as described below.

## CMS 2016 data and NanoAOD
Link to [announcement of 2016 OpenData](https://opendata.cern.ch/docs/cms-releases-2016data-2024)
NanoAOD are [ROOT](https://root.cern/) files containing a `TTree` (named `Events`) storing variables of the reconstructed objects (eg. `Muon_pt`). See documentation: [Getting started with NanoAOD](https://opendata.cern.ch/docs/cms-getting-started-nanoaod). The variables are documented [here](https://opendata.cern.ch/eos/opendata/cms/dataset-semantics/NanoAODSIM/37728/GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8_doc.html)

### 2016 data
[Link to 2016 data available](https://opendata.cern.ch/search?q=&f=experiment%3ACMS&f=type%3ADataset%2Bsubtype%3ACollision&f=year%3A2016&l=list&order=desc&p=1&s=10&sort=mostrecent): 
- Two "eras" available:
  - Run2016G (run 278820-280385). List of dataset available [here](https://github.com/silviodonato/OpenDataCMS2016NanoAOD/blob/main/DatasetInfo/Run2016G.txt).
  - Run2016H (run 280919-284044). List of dataset available [here](https://github.com/silviodonato/OpenDataCMS2016NanoAOD/blob/main/DatasetInfo/Run2016H.txt).
- Example: `/SingleMuon/Run2016H-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD` [DOI:10.7483/OPENDATA.CMS.4BUS.64MV](https://opendata.cern.ch/record/30563) : 
  - File example: `root://eospublic.cern.ch//eos/opendata/cms/Run2016H/SingleMuon/NANOAOD/UL2016_MiniAODv2_NanoAODv9-v1/120000/61FC1E38-F75C-6B44-AD19-A9894155874E.root`

### Simulation
[Link to 2016 simulations available](https://opendata.cern.ch/search?q=&f=experiment%3ACMS&f=type%3ADataset%2Bsubtype%3ASimulated&f=year%3A2016&l=list&order=desc&p=1&s=10&sort=mostrecent)
  - Example: [GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8](https://opendata.cern.ch/record/37728)
    - Example file: `root://eospublic.cern.ch//eos/opendata/cms/mc/RunIISummer20UL16NanoAODv9/GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8/NANOAODSIM/106X_mcRun2_asymptotic_v17-v2/260000/6116BC4B-92FF-D24E-99F1-2017BCF6C83A.root`

### How to access data

You might need to install `xrootd-client`, or using a docker image, or using [cernopendata-client](https://cernopendata-client.readthedocs.io/en/latest/installation.html) (see below).

Example:
~~~
source thisroot.sh ## somewhere
root -l root://eospublic.cern.ch//eos/opendata/cms/derived-data/PFNano/29-Feb-24/SingleMuon/Run2016G-UL2016_MiniAODv2_PFNanoAODv1/240207_205649/0000/nano_data2016_100.root

Events->Scan("run:luminosityBlock:event:nMuon:Muon_pt") ## print event run, lumisection, event number, number of muons in each event, and muon pt
Events->Print("Muon_*") ## check all Muon variable available (with a minimal documentation)
Events->Draw("Muon_pt","Muon_pt<150") ## plot the muon pT distribution
~~~

## Miscellanea

### Docker
Link to the [guide](https://opendata.cern.ch/docs/cms-guide-docker):
 - `gitlab-registry.cern.ch/cms-cloud/root-vnc`
 - `gitlab-registry.cern.ch/cms-cloud/python-vnc`
 - Example:
~~~
[...]
~~~

### How to compute luminosity: 
[Link to the guide] (https://opendata.cern.ch/docs/cms-guide-luminosity-calculation)
- Good data selector (aka GoldenJSON) [link](https://opendata.cern.ch/record/14221) )

### HLT configuration: 
[Link to the HLT configuration used](https://opendata.cern.ch/record/30300)
    - Run 278820, [HLTConfiguration_Run278820_cdaq_physics_Run2016_25ns15e33_v3.1.3_HLT_V15](), release [CMSSW_8_0_17](https://github.com/cms-sw/cmssw/tree/CMSSW_8_0_17)
      - where you can find the dataset definition [1]
    - Run 284044, [HLTConfiguration_Run278820_cdaq_physics_Run2016_25ns15e33_v3.1.3_HLT_V15](), release [CMSSW_8_0_19_patch2](https://github.com/cms-sw/cmssw/tree/CMSSW_8_0_19_patch2)
      - where you can find the dataset definition [2]

    
[1]
```
  SingleMuon = cms.vstring( 'HLT_DoubleIsoMu17_eta2p1_noDzCut_v2',
    'HLT_DoubleIsoMu17_eta2p1_v4',
    'HLT_IsoMu16_eta2p1_MET30_LooseIsoPFTau50_Trk30_eta2p1_v3',
    'HLT_IsoMu16_eta2p1_MET30_v2',
    'HLT_IsoMu17_eta2p1_LooseIsoPFTau20_SingleL1_v6',
    'HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v6',
    'HLT_IsoMu18_v3',
    'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v3',
    'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v3',
    'HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v3',
    'HLT_IsoMu20_v4',
    'HLT_IsoMu21_eta2p1_LooseIsoPFTau20_SingleL1_v3',
    'HLT_IsoMu21_eta2p1_LooseIsoPFTau50_Trk30_eta2p1_SingleL1_v2',
    'HLT_IsoMu21_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v3',
    'HLT_IsoMu22_eta2p1_v2',
    'HLT_IsoMu22_v3',
    'HLT_IsoMu24_v2',
    'HLT_IsoMu27_v5',
    'HLT_IsoTkMu18_v4',
    'HLT_IsoTkMu20_v6',
    'HLT_IsoTkMu22_eta2p1_v3',
    'HLT_IsoTkMu22_v4',
    'HLT_IsoTkMu24_v3',
    'HLT_IsoTkMu27_v6',
    'HLT_L1SingleMu18_v1',
    'HLT_L1SingleMuOpen_v3',
    'HLT_L2Mu10_v2',
    'HLT_Mu10_TrkIsoVVL_DiPFJet40_DEta3p5_MJJ750_HTT350_PFMETNoMu60_v3',
    'HLT_Mu15_IsoVVVL_BTagCSV_p067_PFHT400_v4',
    'HLT_Mu15_IsoVVVL_PFHT350_PFMET50_v5',
    'HLT_Mu15_IsoVVVL_PFHT350_v5',
    'HLT_Mu15_IsoVVVL_PFHT400_PFMET50_v3',
    'HLT_Mu15_IsoVVVL_PFHT400_v3',
    'HLT_Mu15_IsoVVVL_PFHT600_v6',
    'HLT_Mu16_eta2p1_MET30_v2',
    'HLT_Mu20_v3',
    'HLT_Mu24_eta2p1_v4',
    'HLT_Mu27_v4',
    'HLT_Mu28NoFiltersNoVtx_CentralCaloJet40_v3',
    'HLT_Mu28NoFiltersNoVtx_DisplacedJet40_Loose_v3',
    'HLT_Mu300_v2',
    'HLT_Mu30_eta2p1_PFJet150_PFJet50_v3',
    'HLT_Mu33NoFiltersNoVtxDisplaced_DisplacedJet50_Loose_v3',
    'HLT_Mu33NoFiltersNoVtxDisplaced_DisplacedJet50_Tight_v3',
    'HLT_Mu350_v2',
    'HLT_Mu38NoFiltersNoVtxDisplaced_DisplacedJet60_Loose_v3',
    'HLT_Mu38NoFiltersNoVtxDisplaced_DisplacedJet60_Tight_v3',
    'HLT_Mu38NoFiltersNoVtx_DisplacedJet60_Loose_v3',
    'HLT_Mu40_eta2p1_PFJet200_PFJet50_v5',
    'HLT_Mu45_eta2p1_v4',
    'HLT_Mu50_IsoVVVL_PFHT400_v3',
    'HLT_Mu50_v4',
    'HLT_Mu55_v3',
    'HLT_Mu8_TrkIsoVVL_DiPFJet40_DEta3p5_MJJ750_HTT300_PFMETNoMu60_v2',
    'HLT_TkMu20_v4',
    'HLT_TkMu24_eta2p1_v5',
    'HLT_TkMu27_v5',
    'HLT_TkMu50_v3' ),
```

[2]
```
  SingleMuon = cms.vstring( 'HLT_DoubleIsoMu17_eta2p1_noDzCut_v5',
    'HLT_IsoMu16_eta2p1_MET30_LooseIsoPFTau50_Trk30_eta2p1_v5',
    'HLT_IsoMu16_eta2p1_MET30_v4',
    'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v5',
    'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v5',
    'HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v5',
    'HLT_IsoMu20_v6',
    'HLT_IsoMu21_eta2p1_LooseIsoPFTau20_SingleL1_v5',
    'HLT_IsoMu21_eta2p1_LooseIsoPFTau50_Trk30_eta2p1_SingleL1_v4',
    'HLT_IsoMu21_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg_v5',
    'HLT_IsoMu22_eta2p1_v4',
    'HLT_IsoMu22_v5',
    'HLT_IsoMu24_eta2p1_v3',
    'HLT_IsoMu24_v4',
    'HLT_IsoMu27_v7',
    'HLT_IsoTkMu20_v7',
    'HLT_IsoTkMu22_eta2p1_v4',
    'HLT_IsoTkMu22_v5',
    'HLT_IsoTkMu24_eta2p1_v3',
    'HLT_IsoTkMu24_v4',
    'HLT_IsoTkMu27_v7',
    'HLT_L1SingleMu18_v1',
    'HLT_L2Mu10_v3',
    'HLT_Mu10_TrkIsoVVL_DiPFJet40_DEta3p5_MJJ750_HTT350_PFMETNoMu60_v5',
    'HLT_Mu15_IsoVVVL_BTagCSV_p067_PFHT400_v6',
    'HLT_Mu15_IsoVVVL_PFHT400_PFMET50_v5',
    'HLT_Mu15_IsoVVVL_PFHT400_v5',
    'HLT_Mu15_IsoVVVL_PFHT600_v8',
    'HLT_Mu20_v4',
    'HLT_Mu24_eta2p1_v5',
    'HLT_Mu27_v5',
    'HLT_Mu28NoFiltersNoVtx_CentralCaloJet40_v5',
    'HLT_Mu28NoFiltersNoVtx_DisplacedJet40_Loose_v5',
    'HLT_Mu300_v3',
    'HLT_Mu30_eta2p1_PFJet150_PFJet50_v5',
    'HLT_Mu350_v3',
    'HLT_Mu38NoFiltersNoVtxDisplaced_DisplacedJet60_Loose_v5',
    'HLT_Mu38NoFiltersNoVtxDisplaced_DisplacedJet60_Tight_v5',
    'HLT_Mu38NoFiltersNoVtx_DisplacedJet60_Loose_v5',
    'HLT_Mu40_eta2p1_PFJet200_PFJet50_v7',
    'HLT_Mu45_eta2p1_v5',
    'HLT_Mu50_IsoVVVL_PFHT400_v5',
    'HLT_Mu50_v5',
    'HLT_Mu55_v4',
    'HLT_Mu8_TrkIsoVVL_DiPFJet40_DEta3p5_MJJ750_HTT300_PFMETNoMu60_v4',
    'HLT_TkMu17_v1',
    'HLT_TkMu20_v4',
    'HLT_TkMu24_eta2p1_v5',
    'HLT_TkMu27_v5',
    'HLT_TkMu50_v3' ),
```


