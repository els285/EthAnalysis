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
        self.tree_name          = config["tree_name"]
        self.base_frame         = RDataFrame(self.tree_name,self.ROOT_file)

        self.selections         = config["Selections"]
        self.check_branches(config["Observables"])
        self.observables        = config["Observables"]

        self.filtered_dfs       = {}
        self.histograms         = {}


    def check_branches(self,list_of_branches):

        """
        Checks that all listed branches exist in the TTree
        There may be a superior way to do this without 
        """

        file0   = TFile(self.ROOT_file)
        tree    = file0.Get(self.tree_name)
        existing_branches = [br.GetName() for br in tree.GetListOfBranches()]

        non_matched_branches = list(set(list_of_branches) - set(existing_branches))

        if len(non_matched_branches) != 0:
            as_string = " , ".join(non_matched_branches)
            raise KeyError(f"The following branches do exist in the TTree {self.tree_name} in the file {self.ROOT_file}: {as_string}")



    def apply_cuts(self):

        for sel,cuts in self.selections.items():
            cut_string = " && ".join(x for x in cuts)
            self.filtered_dfs[sel] = self.base_frame.Filter(cut_string)


    def make_histograms(self):

        for sel,df in self.filtered_dfs.items():
            self.histograms[sel] = {}
            for obs in self.observables:
                self.histograms[sel][obs] = df.Histo1D(obs)

        for sel_histograms in self.histograms.values():
            for hist in sel_histograms.values():
                print(f"Building histogram {hist}")
                hist.Draw("SAME")

    


F = Frame("config.yml")
F.apply_cuts()
F.make_histograms()
print(F.histograms)
