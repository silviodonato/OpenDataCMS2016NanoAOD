# from __future__ import print_function, division, absolute_import
import sys, os

import ROOT

nparallelprocesses = 4

save_path = "outputFiles/"  # can also be just '.', means same directory as script
# inputFolder = "inputFiles/"
#inputFolder = "4muons/"
# inputFolder = "prescale20/"
inputFolder = "2muons2electrons/"
histo_path = "histos/"


lumi_Run2016G = 7625.376423
lumi_Run2016H = 8892.128926

lumi =  (lumi_Run2016G+lumi_Run2016H)/20  # pb-1 (xsec in pb) 

samples = {
    "Data": {
        "xsec": 0,  ## use xs = 0 for data
        "lumi": lumi, 
        "maxEvents": 10000, 
        "color": ROOT.kBlack, 
        "file": inputFolder+"data.root"},
    "Drell-Yan": {
        "xsec": 6529.0, 
        "lumi": lumi, 
        "maxEvents": 10000, 
        "color": ROOT.kAzure - 8, 
        "file": inputFolder+"dy.root"},
    # "ggH4L": {
    #     "xsec": 28.87 * 0.001, 
    #     "lumi": lumi, 
    #     "maxEvents": 1000, 
    #     "color": ROOT.kViolet - 9, 
    #     "file": inputFolder+"ggH4L.root"},
    # "ZZ": {
    #     "xsec": 12.14, 
    #     "lumi": lumi, 
    #     "maxEvents": -1, 
    #     "color": ROOT.kSpring + 4, 
    #     "file": inputFolder+"zz.root"}, 
}

sys.path.append(os.path.abspath(os.path.curdir))  # append current dir explicit to path (py2 was implicit)

from MyAnalysis import MyAnalysis
from Plotter import plotVar, plotVarNorm, plotShapes
from multiprocessing import Pool

## parallel processing
def process_sample(sample):
    infos = samples[sample]
    myAnalysis = MyAnalysis(sample=sample, xsec=infos["xsec"], lumi=infos["lumi"], fileName=infos["file"], histo_folder=histo_path, maxEvents=infos["maxEvents"])
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
