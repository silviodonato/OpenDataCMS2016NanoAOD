from __future__ import print_function, division, absolute_import

import os

import ROOT

samp = {}

# TODO: change path below
save_path = "/home/sdonato/CMS/CorsoCavasinni/OpenDataCMS2016NanoAOD/"  # can also be just '.', means same directory as script
file_path = "/home/sdonato/CMS/CorsoCavasinni/OpenDataCMS2016NanoAOD/"
histo_path = "/home/sdonato/CMS/CorsoCavasinni/OpenDataCMS2016NanoAOD/ppp_small_project"

if any(p.startswith("The/Path/where/") for p in (save_path, file_path, histo_path)):  # change the defaults!
    raise ValueError("Please specify all path in samples.py first")

for path in (save_path, histo_path):
    if not os.path.exists(path):
        os.makedirs(path)
        print("{} did not exists and was created.".format(path))

# samp["ttbar"] = ROOT.kPink - 7
samp["dy"] = ROOT.kAzure - 8
samp["dy_1file"] = ROOT.kAzure - 8
# samp["wjets"] = ROOT.kTeal - 7
# samp["qcd"] = ROOT.kViolet - 9
samp["ggH4L"] = ROOT.kViolet - 9
# samp["ww"] = ROOT.kOrange - 3
# samp["wz"] = ROOT.kOrange - 2
samp["zz"] = ROOT.kSpring + 4
samp["zz_1file"] = ROOT.kSpring + 4
# samp["single_top"] = ROOT.kPink + 3


# samp["Run2016H_1file"] = ROOT.kBlack