from __future__ import print_function, division, absolute_import

import sys
import os

sys.path.append(os.path.abspath(os.path.curdir))  # append current dir explicit to path (py2 was implicit)

from MyAnalysis import MyAnalysis
from Plotter import plotVar, plotVarNorm, plotShapes

lumi_Run2016G = 7625.376423
lumi_Run2016H = 8892.128926

lumi =  (lumi_Run2016G+lumi_Run2016H)/20  # pb-1 (xsec in pb) 

### Instantiation of an object of kind MyAnalysis for each single sample
DY = MyAnalysis("dy", 6529.0, lumi, maxEvents=10000 )
DY.processEvents()

# ggH4L = MyAnalysis("ggH4L", 28.87*0.001, lumi, maxEvents=-1 )
# ggH4L.processEvents()

# ZZ = MyAnalysis("zz", 12.14, lumi, maxEvents=-1 )
# ZZ.processEvents()

Data = MyAnalysis("data", -1 , -1, maxEvents=10000)
Data.processEvents()

## samples to be processed
samples = ["dy"]
# samples = ["ggH4L","zz", "dy"]

variables = ["NIsoMu", "Muon_Pt","Muon_Iso"]

for v in variables:
    print("Variable: ", v)
    ### plotShapes (variable, samples, logScale )
    plotShapes(v, samples, True)
    ### plotVar(variable, samples,isData, logScale )
    plotVar(v, samples, True, True)
