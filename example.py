# from __future__ import print_function, division, absolute_import
import sys, os

import ROOT

nparallelprocesses = 1


lumi_Run2016G = 7625.376423
lumi_Run2016H = 8892.128926
# lumi_2mu = 258.33304 * 8892.128926/7625.376423
lumi_2mu = 350

lumi =  (lumi_Run2016G+lumi_Run2016H)  # pb-1 (xsec in pb) 
# lumi =  lumi_Run2016G  # pb-1 (xsec in pb) 


from MyAnalysis_2muons import MyAnalysis as MyAnalysis
inputFolder = "2mu/"
# lumi = lumi_Run2016G *  0.0097997481
lumi = lumi_2mu

# from MyAnalysis_4muons import MyAnalysis as MyAnalysis
# inputFolder = "4mu/"

# from MyAnalysis_2muons2electrons import MyAnalysis as MyAnalysis
# inputFolder = "2e2mu/"

save_path = "outputFiles/"  # can also be just '.', means same directory as script
histo_path = "histos/"

## Load golden JSON and write a function to check if a run, lumi is in the golden JSON
import json
jsonFile = "Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON_MuonPhys.txt"    
with open(jsonFile, 'r') as f:
    goldenJson = json.load(f)

def isGoodData(run, lumi):
    if str(run) not in goldenJson:
        return False
    for l in goldenJson[str(run)]:
        if l[0] <= lumi <= l[1]:
            return True
    return False

## Define the samples to be processed

samples = {
    "Data": {
        "xsec": 0,  ## use xs = 0 for data
        "lumi": lumi, 
        "maxEvents": 100000, 
        "color": ROOT.kBlack, 
        # "file": inputFolder+"data.root",},
        "file": inputFolder+"data_Run2016G_PS20.root",},
    "Drell-Yan": {
        "xsec": 6104.0, 
        "lumi": lumi, 
        "maxEvents": 10000, 
        "color": ROOT.kGreen+2, 
        "file": inputFolder+"dy.root"},
    # "ggZZTo4mu": {
    #     "xsec": 0.00159, 
    #     "lumi": lumi, 
    #     "maxEvents": 3000, 
    #     "color": ROOT.kAzure-2, 
    #     "file": inputFolder+"ggZZTo4mu.root"}, 
    # "ggZZTo2e2mu": {
    #     "xsec": 0.00319, 
    #     "lumi": lumi, 
    #     "maxEvents": 3000, 
    #     "color": ROOT.kAzure-2, 
    #     "file": inputFolder+"ggZZTo2e2mu.root"}, 
    # "qqZZ": {
    #     "xsec": 1.256, #*0.5 
    #     "lumi": lumi, 
    #     "maxEvents": -1, 
    #     "color": ROOT.kAzure+6, 
    #     "file": inputFolder+"qqZZ.root"}, 
    # "ggH4L": {
    #     "xsec": 12.18*1E-3, 
    #     "lumi": lumi, 
    #     "maxEvents": 10000, 
    #     "color": ROOT.kRed-9, 
    #     "file": inputFolder+"ggH4L.root"},
}

sys.path.append(os.path.abspath(os.path.curdir))  # append current dir explicit to path (py2 was implicit)

from Plotter import plotVar, plotVarNorm, plotShapes
from multiprocessing import Pool

## parallel processing
def process_sample(sample):
    infos = samples[sample]
    myAnalysis = MyAnalysis(sample=sample, xsec=infos["xsec"], lumi=infos["lumi"], fileName=infos["file"], histo_folder=histo_path, maxEvents=infos["maxEvents"], isGoodData=isGoodData)
    myAnalysis.processEvents()

if __name__ == '__main__':
    pool = Pool(processes=nparallelprocesses)
    pool.map(process_sample, samples.keys())
    pool.close()
    pool.join()

    sample = "Data"
    histoFile = ROOT.TFile.Open(histo_path +"/"+ sample + "_histos.root")
    if not histoFile:
        print("File " + histo_path +"/"+ sample + "_histos.root" + " does not exist."
                    "Please, check to have processed the corresponding sample")
    else:
        ## Launch plot per each variable
        for v in histoFile.GetListOfKeys():
            v = v.GetName()
            if histoFile.Get(v).Integral() > 0:
                print("Variable: ", v)
                ### plotShapes (variable, samples, logScale )
                plotShapes(v, samples, sample="Drell-Yan",  logScale=False)
                ### plotVar(variable, samples,isData, logScale )
                plotVar(v, samples, sample="Drell-Yan", isData=False, logScale=False)
                plotVar(v, samples, sample="Data", isData=True, logScale=False)
            else:
                print("No events in the variable %s. Skipping"%v)
