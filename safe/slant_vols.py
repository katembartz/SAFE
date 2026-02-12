import argparse

from pathlib import Path
import nibabel as nib 
import numpy as np
import sys
from tqdm import tqdm

def get_vols_slt(args=None):
    parser = argparse.ArgumentParser(
            description="Compute volumetrics from slant segmentations"
        )
    parser.add_argument("--in-dir", type=Path, required=True)
    parser.add_argument("--results-dir", type=Path, required=True)
    parser.add_argument("--head-dir", type=Path, required=True)
    parsed = parser.parse_args(args)
    
    print("===== Computing volumetrics for slant segmentations =====")
    
    fpaths = sorted(parsed.in_dir.glob("*_slant*.nii*"))
    
    if len(fpaths) == 0:
        raise FileNotFoundError(f"No slant segmentations found in {parsed.in_dir}. Do the file names contain '_slant'?")

    with open(f"{str(parsed.head_dir)}/slant_lut.txt", "r") as f:
        lines = [line.strip().split() for line in f.readlines()]

    slant_lut = {int(k): (name, int(r),int(g),int(b),int(a)) 
                for k, name, r, g, b, a in lines}

    csv_fpath = f"{parsed.results_dir}/slant_volumetrics.csv"
    
    with open(csv_fpath, 'w') as f:
        print("===== Writing header... =====")
        
        f.write("subject")
        for name, *_ in slant_lut.values():
            f.write(f",{name}")
        f.write("\n")

        print("===== Summarizing label volumes... =====")
        
        for fpath in tqdm(fpaths):
            subj_id = fpath.name.split("_slant")[0] 
            x = nib.load(fpath).get_fdata(dtype=np.float32) 
            x = np.around(x).astype(np.int64) 
            img = nib.load(fpath)
            vox_vol = np.around(np.prod(img.header.get_zooms())).astype(np.int64)
            
            f.write(f"{subj_id}")
            for k in slant_lut.keys(): 
                vol = x[x == k].shape[0] 
                vol = vol * vox_vol
                f.write(f",{vol}") 
            f.write("\n") 
            
    print(f"Slant volumetrics saved in {csv_fpath}")
