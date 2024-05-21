import os
import ROOT
import math

folder = "histos"

Z_mass = 91.1876
mass_points = [x/100 for x in range(9050, 9150)]
fit_range = (85, 95)

rebin = 200

## Shift histo of 1 bin to the right
def shiftHisto(histo, x):
    shiftedHisto = histo.Clone()
    shift_bin = int(x/histo.GetBinWidth(1))
    for i in range(1,histo.GetNbinsX()+1):
        if i+shift_bin > 0 and i+shift_bin < histo.GetNbinsX()+2:
            shiftedHisto.SetBinContent(i+shift_bin, histo.GetBinContent(i))
    return shiftedHisto


def getHisto(folder, sample, var):
    filename = sample + "_histos.root"
    histos_file = os.path.join(folder, filename)
    if not os.path.exists(histos_file):
        print("File " + histos_file + " does not exist."
                                      "Please, check to have processed the corresponding sample")
    else:
        f = ROOT.TFile.Open(histos_file)
        h = f.Get(var)
        if sample == "Data":
            h.SetLineColor(ROOT.kBlack)
        else:
            h.SetLineColor(ROOT.kAzure - 8)
            h.SetLineWidth(2)
    ROOT.gROOT.cd()
    return h.Clone()

DY_histo = getHisto(folder, "Drell-Yan", "DiMuonMass1k")
data_histo = getHisto(folder, "Data", "DiMuonMass1k")
DY_histo.Scale(data_histo.Integral()/DY_histo.Integral())



## Compute LogLikelihood
def computeLogLikelihood(data, mc, rangeLikelihood):
    log_likelihood = 0
    for i in range(data.FindBin(rangeLikelihood[0]), data.FindBin(rangeLikelihood[1])):
        data_i = data.GetBinContent(i+1)
        mc_i = mc.GetBinContent(i+1)
        log_prob = math.log(ROOT.TMath.Poisson(data_i, mc_i))
        #log_prob = -mc_i + data_i*math.log(mc_i)
        #log_prob = - (data_i-mc_i)**2/(mc_i**2+data_i**2)**0.5
        log_likelihood += log_prob
    return log_likelihood

graph = ROOT.TGraph()

data_histo.Rebin(rebin)
for x in mass_points:
    shifted_drell = shiftHisto(DY_histo, x-Z_mass)
    shifted_drell.Rebin(rebin)
    log_likelihood = computeLogLikelihood(data_histo, shifted_drell, fit_range)
    print("x",x,"LogLikelihood: ", log_likelihood)
    graph.SetPoint(graph.GetN(), x, -2*log_likelihood)

## add a constant to the likelihood to avoid negative values
min_likelihood = min(graph.GetY())
for i in range(graph.GetN()):
    graph.SetPoint(i, graph.GetX()[i], graph.GetY()[i]-min_likelihood)


shifted_drell.SetLineColor(ROOT.kRed)
DY_histo.Rebin(rebin)

c1 = ROOT.TCanvas("c1", "c1", 1920, 1080)

DY_histo.SetMaximum(1.2*max(DY_histo.GetMaximum(), data_histo.GetMaximum()))
DY_histo.Draw("hist")
shifted_drell.Draw("hist,same")
data_histo.Draw("P,same")

c2 = ROOT.TCanvas("c2", "c2", 1920, 1080)
graph.Draw("APL")
