from __future__ import print_function, division, absolute_import

import os

import ROOT

save_path = "outputFiles/"  # can also be just '.', means same directory as script
file_path = "inputFiles/"
histo_path = "histos/"


# from Samples import samp, save_path, histo_path

# ROOT.gROOT.Reset()
ROOT.gROOT.SetStyle('Plain')
ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch()  # don't pop up canvases
ROOT.TH1.SetDefaultSumw2()
ROOT.TH1.AddDirectory(False)


def setStyle(histo, color, style=0, fill=0):
    histo.GetXaxis().SetLabelFont(42)
    histo.GetYaxis().SetLabelFont(42)
    histo.GetXaxis().SetTitleFont(42)
    histo.GetYaxis().SetTitleFont(42)
    histo.GetXaxis().SetTitleOffset(0.9)
    histo.GetYaxis().SetTitleOffset(1.2)
    histo.SetTitleFont(42)
    histo.SetTitle("")
    if color != ROOT.kRed:
        histo.SetLineColor(1)
    else:
        histo.SetLineColor(color)
    histo.SetLineWidth(1)
    histo.SetLineStyle(style)
    histo.SetFillColor(color)
    histo.SetFillStyle(fill)
    if fill == 0:
        histo.SetMarkerStyle(23)
        histo.SetMarkerSize(1.1)
    nEvts = (histo.GetXaxis().GetXmax() - histo.GetXaxis().GetXmin()) / histo.GetNbinsX()
    histo.GetYaxis().SetTitle("Events/{:.2f}".format(nEvts))


def setStyleStack(hs, options=""):
    hs.Draw(options)
    hs.GetHistogram().GetXaxis().SetLabelFont(42)
    hs.GetHistogram().GetYaxis().SetLabelFont(42)
    hs.GetHistogram().GetXaxis().SetTitleFont(42)
    hs.GetHistogram().GetYaxis().SetTitleFont(42)
    hs.GetHistogram().GetXaxis().SetTitleOffset(0.9)
    hs.GetHistogram().GetYaxis().SetTitleOffset(1.)
    hs.GetHistogram().SetTitleFont(42)
    hs.GetHistogram().SetTitle("")

    hs.GetHistogram().GetXaxis().SetLabelSize(0.05)
    hs.GetHistogram().GetYaxis().SetLabelSize(0.05)
    hs.GetHistogram().GetXaxis().SetTitleSize(0.06)
    hs.GetHistogram().GetYaxis().SetTitleSize(0.06)

    nEvts = ((hs.GetHistogram().GetXaxis().GetXmax() - hs.GetHistogram().GetXaxis().GetXmin()) /
             hs.GetHistogram().GetNbinsX())
    hs.GetHistogram().GetYaxis().SetTitle("Number of events / {:.2f}".format(nEvts))


def setStyleLegend(leg):
    leg.SetNColumns(3)
    leg.SetFillColor(0)
    leg.SetTextSize(0.045)
    leg.SetTextFont(42)

legValues = (0.49, 0.89, 0.99, 0.99)

def getStack(var, samples, excludeSig=False):
    """

    Parameters
    ----------
    var : str
    samples : List[str]
    excludeSig : bool

    Returns
    -------
    Tuple[ROOT.THStack, ROOT.TLegend]
    """
    hs = ROOT.THStack(var, "")
    leg = ROOT.TLegend(*legValues)
    setStyleLegend(leg)

    for s in samples:
        histos_file = os.path.join(histo_path, s + "_histos.root")
        if not os.path.isfile(histos_file):
            print("File " + histos_file + " does not exist."
                                          "Please, check to have processed the corresponding sample")
            continue
        else:
            if samples[s]["xsec"] == 0: ## do not plot data in the stack!
                continue
            if excludeSig and s == "ggH4L":
                continue
            f = ROOT.TFile.Open(histos_file)
            h = f.Get(var)
            setStyle(h, samples[s]["color"], 1, 1001)
            hs.Add(h, "HIST")
            leg.AddEntry(h, s, "f")

    print("getStack DONE.")
    return hs, leg


def plotVar(var, samples, sample, isData=False, logScale=False):
    c = ROOT.TCanvas()
    if logScale:
        c.SetLogy()
    hs = getStack(var, samples)[0]
    leg = getStack(var, samples)[1]
    hs.Draw()
    ### Superimposing signal events (ttbar) to visualise its shape
    histos_file = os.path.join(histo_path, "%s_histos.root"%sample)
    print(histo_path)
    print(histos_file)
    if isData:
        data_histos = os.path.join(histo_path, "%s_histos.root"%sample)
        if not os.path.exists(data_histos):
            print("File " + data_histos + "does not exist."
                                          "Please, check to have processed the corresponding sample")
        else:
            f = ROOT.TFile.Open(data_histos)
            h = f.Get(var)
            setStyle(h, ROOT.kBlack, 0, 0)
            h.Draw("same")
            leg.AddEntry(h, sample, "P")
    else:
        if not os.path.exists(histos_file):
            print("File " + histos_file + " does not exist."
                                        "Please, check to have processed the corresponding sample")
        else:
            f = ROOT.TFile.Open(histos_file)
            h = f.Get(var)
            setStyle(h, samples[sample]["color"], 0, 0)
            h.SetLineColor(samples[sample]["color"])
            h.SetLineWidth(2)
            h.Draw("histsame")
            leg.AddEntry(h, sample, "L")

    ymax = max(hs.GetStack().Last().GetMaximum(), h.GetMaximum())
    leg.Draw("SAME")
    if hs.GetStack().Last().Integral() >0:
        if isData:
            hs.SetMaximum(ymax * 1.3)
            c.SaveAs(os.path.join(save_path, var + ".pdf"))
            c.SaveAs(os.path.join(save_path, var + ".root"))
        else:
            c.SaveAs(os.path.join(save_path, var + "_MC.pdf"))
            c.SaveAs(os.path.join(save_path, var + "_MC.root"))
    else:
        print("WARNING. No events in the sample %s var %s"%(sample, var))
    print("plotVar DONE.")

def plotVarNorm(var, samples, logScale=False):
    """

    Parameters
    ----------
    var :  str
    samples : List[str]
    logScale : bool
    """
    c = ROOT.TCanvas()
    c.cd()
    if logScale:
        c.SetLogy()

    leg = ROOT.TLegend(*legValues)
    setStyleLegend(leg)

    for s in samples:
        histos_file = os.path.join(histo_path, s + "_histos.root")
        if not os.path.isfile(histos_file):
            print("File " + histos_file + " does not exist."
                                          "Please, check to have processed the corresponding sample")
            continue
        else:
            f = ROOT.TFile.Open(histos_file)
            h = f.Get(var)
            setStyle(h, samp[s], 0, 0)
            h.SetLineColor(samp[s])
            h.SetLineWidth(2)
            if h.Integral() != 0.:
                h.Scale(1 / h.Integral())
            h.Draw("histsame")
            leg.AddEntry(h, s, "l")

    leg.Draw("SAME")
    c.SaveAs(os.path.join(save_path, var + "_Norm_MC.pdf"))
    print("plotVarNorm DONE.")


def plotShapes(var, samples, sample, logScale=False):
    """

    Parameters
    ----------
    var : str
    samples : List[str]
    logScale : bool
    """
    c = ROOT.TCanvas()
    c.cd()
    if logScale:
        c.SetLogy()
    hs = getStack(var, samples, True)[0]
    leg = ROOT.TLegend(*legValues)
    setStyleLegend(leg)

    h_bkg = hs.GetStack().Last()
    if h_bkg.Integral() != 0.:
        h_bkg.Scale(1 / h_bkg.Integral())
    setStyle(h_bkg, ROOT.kBlue, 0, 0)
    h_bkg.SetLineWidth(2)
    h_bkg.Draw("hist")
    leg.AddEntry(h_bkg, "Background", "l")

    histos_file = os.path.join(histo_path, "Drell-Yan_histos.root")
    if not os.path.exists(histos_file):
        print("File " + histos_file + " does not exist."
                                      "Please, check to have processed the corresponding sample")

    else:
        f = ROOT.TFile.Open(histos_file)
        h = f.Get(var)
        setStyle(h, samples[sample]["color"], 0, 0)
        h.SetLineColor(ROOT.kPink - 8)
        h.SetLineWidth(2)
        if h.Integral() != 0.:
            h.Scale(1 / h.Integral())
        h.Draw("histsame")
        leg.AddEntry(h, sample, "L")

    leg.Draw("SAME")
    c.SaveAs(os.path.join(save_path, var + "_Shape_MC.pdf"))
    print("plotShapes DONE.")

def getBkgHisto(var, samples):
    """

    Parameters
    ----------
    var : str
    samples : iterable

    Returns
    -------

    """
    hs = getStack(var, samples, True)[0]
    h_bkg = hs.GetStack().Last()
    setStyle(h_bkg, ROOT.kBlue, 0, 0)
    h_bkg.SetLineColor(ROOT.kBlue)
    h_bkg.SetLineWidth(2)
    ROOT.SetOwnership(h_bkg, False)
    h_bkg.SetDirectory(0)

    return h_bkg.Clone()


def getHisto(var, sample):
    """

    Parameters
    ----------
    var : str
    sample : str

    Returns
    -------

    """
    h = ROOT.TH1F()
    filename = sample + "_histos.root"
    histos_file = os.path.join(histo_path, filename)
    if not os.path.exists(histos_file):
        print("File " + histos_file + " does not exist."
                                      "Please, check to have processed the corresponding sample")

    else:
        f = ROOT.TFile.Open(histos_file)
        h = f.Get(var)
        if sample == "data":
            setStyle(h, ROOT.kBlack, 0, 0)
        else:
            setStyle(h, samp[sample], 0, 0)
            h.SetLineColor(samp[sample])
            h.SetLineWidth(2)

    return h


def getSigHisto(var):
    h = getHisto(var, "dy")

    return h
