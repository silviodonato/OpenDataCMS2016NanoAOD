from __future__ import print_function, division, absolute_import

import sys
import os

sys.path.append(os.path.abspath(os.path.curdir))  # append current dir explicit to path (py2 was implicit)

from MyAnalysis import MyAnalysis
from Plotter import plotVar, plotVarNorm, plotShapes

### Instantiation of an object of kind MyAnalysis for each single sample
# TT = MyAnalysis("ttbar")
# TT.processEvents()

lumi =  8892.1 * 289101.00/1.7402106e+08 # pb-1 (xsec in pb) 
## Run2016G 7625.376423
## Run2016H 8892.128926

DY = MyAnalysis("dy", 6529.0, lumi, maxEvents=200000 )
DY.processEvents()

# QCD = MyAnalysis("qcd")
# QCD.processEvents()

# SingleTop = MyAnalysis("single_top")
# SingleTop.processEvents()

# WJets = MyAnalysis("wjets")
# WJets.processEvents()

# WW = MyAnalysis("ww")
# WW.processEvents()

ggH4L = MyAnalysis("ggH4L", 28.87*0.001, lumi, maxEvents=-2000 )
ggH4L.processEvents()

ZZ = MyAnalysis("zz", 12.14, lumi, maxEvents=-2000 )
ZZ.processEvents()

# WZ = MyAnalysis("wz")
# WZ.processEvents()

Data = MyAnalysis("Run2016H", -1 , -1, maxEvents=-2000)
Data.processEvents()

# samples = ["qcd", "zz", "wz", "ww", "single_top", "dy", "wjets", "ttbar"]
samples = ["ggH4L","zz", "dy"]

variables = ["NIsoMu", "Muon_Pt","Muon_Iso"]

for v in variables:
    print("Variable: ", v)
    ### plotShapes (variable, samples, logScale )
    plotShapes(v, samples, True)
    ### plotVar(variable, samples,isData, logScale )
    plotVar(v, samples, True, True)
