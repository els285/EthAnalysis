from ROOT import RDataFrame,TFile, EnableImplicitMT
import yaml,os 

EnableImplicitMT()
class Frame(object):

    def __init__(self,config_file):

        with open(config_file, "r") as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        # Check that the specified file exists
        if not os.path.isfile(config["ROOT_file"]):
            raise FileNotFoundError(f"{config['ROOT_file']} was not found")
        
        self.ROOT_file          = config["ROOT_file"]
        self.tree_name          = config["tree_names"]
        self.base_frame         = RDataFrame(self.tree_name,self.ROOT_file)

        self.selections         = config["Selections"]
        self.observables        = config["Observables"]

        self.filtered_dfs       = {}
        self.histograms         = {}

    def apply_cuts(self):

        for sel,cuts in self.selections.values():
            cut_string = " && ".join(x for x in cuts)
        self.filtered_dfs[sel] = self.base_frame.Filter(cut_string)
    



        







# class Projection(object):

#     def __init__(self,config_file):
#         self.config_file = config_file



# df = RDataFrame("particleLevel","../ttbar_baseline_sample_particleLevel.root")
# h = df.Filter("jet_phi > 0.0").Histo1D("jet_eta")
# h.Draw()

# hist_jet_pt.Draw()
# # print(hist_jet_pt)