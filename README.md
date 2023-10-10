# EthAnalysis
ROOT-based histogramming package

## Installation
Requires ROOT 

Install through `pip`:
```bash
python3 -m pip install 
```

## Example Config
```yaml
ROOT_files: 
- <path2file1>
- <path2file2>
tree_name: nominal
Observables:
  reco_cosphi: 8,-1,1
  reco_lep_pt: [0,100,200,300,400,500,600,700,1000]
  reco_lep_eta:
Selections:
    SignalRegion:
        - reco_ttbar_m > 340
        - reco_ttbar_m < 380
    Validation1:
        - reco_ttbar_m > 380
        - reco_ttbar_m < 500
```
