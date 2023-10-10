from ROOT import RDataFrame,TFile, EnableImplicitMT
import yaml,os 
import numpy as np

EnableImplicitMT()
class Frame(object):

    """
    A wrapper for the RDataFrame class
    Designed to take as input multiple ROOT files and build a single RDataFrame
    Selections can then be applied on the RDataFrame
    Histograms can be generated from observables
    """

    def __init__(self,config_file: str):

        with open(config_file, "r") as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        # Load all ROOT files and check they exist
        self.ROOT_files          = config["ROOT_files"]
        for _file0_ in self.ROOT_files:
            if not os.path.isfile(_file0_):
                raise FileNotFoundError(f"{_file0_} was not found")
        
        self.tree_name           = config["tree_name"]
        self.base_frame          = RDataFrame(self.tree_name,self.ROOT_files)

        self.selections         = config["Selections"]
        self.check_branches(config["Observables"])
        self.observables        = config["Observables"]

        self.filtered_dfs       = {}
        self.histograms         = {}



    def check_branches(self, list_of_branches: list):

        """
        Checks that all listed branches exist in the RDataFrame
        """

        existing_branches    =  [br for br in self.base_frame.GetColumnNames()]
        non_matched_branches =  list(set(list_of_branches) - set(existing_branches))

        if len(non_matched_branches) != 0:
            as_string = " , ".join(non_matched_branches)
            raise KeyError(f"The following branches do exist in the TTree {self.tree_name} in the file {self.ROOT_file}: {as_string}")


    def apply_cuts(self):

        """
        Apply a series of cuts to dataframe. Cuts are not checked
        """

        for sel,cuts in self.selections.items():
            cut_string = " && ".join(x for x in cuts)
            self.filtered_dfs[sel] = self.base_frame.Filter(cut_string)


    def make_histograms(self):

        """
        Projects histograms out of RDataFrame, with user-specified binning
        """

        for sel,df in self.filtered_dfs.items():
            self.histograms[sel] = {}
            for obs,bin_input in self.observables.items():
                if isinstance(bin_input,list):
                    bin_data = (obs,obs,len(bin_input)-1,np.asarray(bin_input,dtype="float64"))
                    self.histograms[sel][obs] = df.Histo1D(bin_data,obs)

                elif not bin_input:
                    self.histograms[sel][obs] = df.Histo1D(obs)

                else:
                    bin_data = bin_input.split(",")
                    if len(bin_data) != 3:
                        raise ValueError(f"The specified binning {bin_input} for {obs} is not of corretc format")
                    bin_data = (obs,obs,int(bin_data[0]),float(bin_data[1]),float(bin_data[2]))
                    self.histograms[sel][obs] = df.Histo1D(bin_data,obs)


        for sel_histograms in self.histograms.values():
            for hist in sel_histograms.values():
                print(f"Building histogram {hist}")
                hist.Draw("SAME")


    def save_histograms(self,save_path:str = "."):

        """
        Save histograms to ROOT files, different file for each selection
        """

        for sel,hist_dic in self.histograms.items():
            try:
                outfile = TFile(f"{save_path}/{sel}.root","RECREATE")
            except not os.path.isdir(save_path):
                raise FileNotFoundError(f"The directory {save_path} does not exist")
            outfile.cd()
            for hist in hist_dic.values():
                hist.Write()
            outfile.Close()


def drive(config:str):
    F = Frame("config.yml")
    F.apply_cuts()
    F.make_histograms()
    F.save_histograms()
