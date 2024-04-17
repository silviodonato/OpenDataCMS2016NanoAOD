# OpenDataCMS2016NanoAOD
Code for students in University of Pisa to run a simplified H->4 lepton search using 2016 CMS open data based on NanoAOD format. Part of the code is based on a similar exercise done for University of Zurich Particle Physics laboratory in 2016.

# CMS 2016 data and NanoAOD
News: https://opendata.cern.ch/docs/cms-releases-2016data-2024
 - Data: https://opendata.cern.ch/search?q=&f=experiment%3ACMS&f=type%3ADataset%2Bsubtype%3ACollision&f=year%3A2016&l=list&order=desc&p=1&s=10&sort=mostrecent
    - Two "eras" available:
        - Run2016G (run 278820-280385). List of dataset available [here](https://github.com/silviodonato/OpenDataCMS2016NanoAOD/blob/main/DatasetInfo/Run2016G.txt).
        - Run2016H (run 280919-284044). List of dataset available [here](https://github.com/silviodonato/OpenDataCMS2016NanoAOD/blob/main/DatasetInfo/Run2016H.txt).
    - How to compute luminosity: [link] (https://opendata.cern.ch/docs/cms-guide-luminosity-calculation)
        - Good data selector (aka GoldenJSON [link](https://opendata.cern.ch/record/14221) )
   - Example: /SingleMuon/Run2016H-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD [DOI:10.7483/OPENDATA.CMS.4BUS.64MV] : https://opendata.cern.ch/record/30563 
      - List of triggers [1]
      - File example: `root://eospublic.cern.ch//eos/opendata/cms/Run2016H/SingleMuon/NANOAOD/UL2016_MiniAODv2_NanoAODv9-v1/120000/61FC1E38-F75C-6B44-AD19-A9894155874E.root`
 - Simulation: https://opendata.cern.ch/search?q=&f=experiment%3ACMS&f=type%3ADataset%2Bsubtype%3ASimulated&f=year%3A2016&l=list&order=desc&p=1&s=10&sort=mostrecent 
    - Example: `GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8`
        - Example file: `root://eospublic.cern.ch//eos/opendata/cms/mc/RunIISummer20UL16NanoAODv9/GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8/NANOAODSIM/106X_mcRun2_asymptotic_v17-v2/260000/6116BC4B-92FF-D24E-99F1-2017BCF6C83A.root`


Docker ( [guide](https://opendata.cern.ch/docs/cms-guide-docker) ):
 - gitlab-registry.cern.ch/cms-cloud/root-vnc
 - gitlab-registry.cern.ch/cms-cloud/python-vnc

Example:
~~~
source this
root -l root://eospublic.cern.ch//eos/opendata/cms/derived-data/PFNano/29-Feb-24/SingleMuon/Run2016G-UL2016_MiniAODv2_PFNanoAODv1/240207_205649/0000/nano_data2016_100.root
~~~

# Miscellanea

HLT configuration: https://opendata.cern.ch/record/30300
    - Run 278820, [HLTConfiguration_Run278820_cdaq_physics_Run2016_25ns15e33_v3.1.3_HLT_V15](), release [CMSSW_8_0_17](https://github.com/cms-sw/cmssw/tree/CMSSW_8_0_17)
    - Run 284044, [HLTConfiguration_Run278820_cdaq_physics_Run2016_25ns15e33_v3.1.3_HLT_V15](), release [CMSSW_8_0_19_patch2](https://github.com/cms-sw/cmssw/tree/CMSSW_8_0_19_patch2)
    - 

[1]
HLT_DoubleIsoMu17_eta2p1_noDzCut
HLT_DoubleIsoMu17_eta2p1
HLT_IsoMu16_eta2p1_MET30_LooseIsoPFTau50_Trk30_eta2p1
HLT_IsoMu16_eta2p1_MET30
HLT_IsoMu17_eta2p1_LooseIsoPFTau20_SingleL1
HLT_IsoMu17_eta2p1_LooseIsoPFTau20
HLT_IsoMu18
HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1
HLT_IsoMu19_eta2p1_LooseIsoPFTau20
HLT_IsoMu19_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg
HLT_IsoMu20
HLT_IsoMu21_eta2p1_LooseIsoPFTau20_SingleL1
HLT_IsoMu21_eta2p1_LooseIsoPFTau50_Trk30_eta2p1_SingleL1
HLT_IsoMu21_eta2p1_MediumIsoPFTau32_Trk1_eta2p1_Reg
HLT_IsoMu22_eta2p1
HLT_IsoMu22
HLT_IsoMu24_eta2p1
HLT_IsoMu24
HLT_IsoMu27
HLT_IsoTkMu18
HLT_IsoTkMu20
HLT_IsoTkMu22_eta2p1
HLT_IsoTkMu22
HLT_IsoTkMu24_eta2p1
HLT_IsoTkMu24
HLT_IsoTkMu27
HLT_L1SingleMu16
HLT_L1SingleMu18
HLT_L2Mu10
HLT_Mu10_TrkIsoVVL_DiPFJet40_DEta3p5_MJJ750_HTT350_PFMETNoMu60
HLT_Mu15_IsoVVVL_BTagCSV_p067_PFHT400
HLT_Mu15_IsoVVVL_PFHT350_PFMET50
HLT_Mu15_IsoVVVL_PFHT350
HLT_Mu15_IsoVVVL_PFHT400_PFMET50
HLT_Mu15_IsoVVVL_PFHT400
HLT_Mu15_IsoVVVL_PFHT600
HLT_Mu16_eta2p1_MET30
HLT_Mu20
HLT_Mu24_eta2p1
HLT_Mu27
HLT_Mu28NoFiltersNoVtx_CentralCaloJet40
HLT_Mu28NoFiltersNoVtx_DisplacedJet40_Loose
HLT_Mu300
HLT_Mu30_eta2p1_PFJet150_PFJet50
HLT_Mu33NoFiltersNoVtxDisplaced_DisplacedJet50_Loose
HLT_Mu33NoFiltersNoVtxDisplaced_DisplacedJet50_Tight
HLT_Mu350
HLT_Mu38NoFiltersNoVtxDisplaced_DisplacedJet60_Loose
HLT_Mu38NoFiltersNoVtxDisplaced_DisplacedJet60_Tight
HLT_Mu38NoFiltersNoVtx_DisplacedJet60_Loose
HLT_Mu40_eta2p1_PFJet200_PFJet50
HLT_Mu45_eta2p1
HLT_Mu50_IsoVVVL_PFHT400
HLT_Mu50
HLT_Mu55
HLT_Mu8_TrkIsoVVL_DiPFJet40_DEta3p5_MJJ750_HTT300_PFMETNoMu60
HLT_TkMu17
HLT_TkMu20
HLT_TkMu24_eta2p1
HLT_TkMu27
HLT_TkMu50