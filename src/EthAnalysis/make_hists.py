from EthAnalysis import Frame

def drive(config:str):
    F = Frame("config.yml")
    F.apply_cuts()
    F.make_histograms()
    F.save_histograms()
