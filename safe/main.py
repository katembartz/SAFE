import argparse
from pathlib import Path

import numpy as np
import sys
import csv
from datetime import datetime

from .slant_vols import get_vols_slt
from .synthseg_vols import get_vols_syn
from .safe_slant import safe_for_slant
from .safe_synthseg import safe_for_synth

def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--in-dir", type=Path, required=True, help="Path to segmentation directory")
    parser.add_argument("--results-dir", type=Path, default=None, help="Path to output safe results")
    parser.add_argument("--head-dir", type=Path, default=Path.cwd(), help="Path to installed code for safe") 
    parser.add_argument("--synth", action="store_true", help="Input directory includes SynthSeg segmentations")
    parser.add_argument("--slant", action="store_true", help="Input directory includes slant segmentations")
    parsed = parser.parse_args(args)
    
    if parsed.results_dir == None:
        now = datetime.now()
        formatted = now.strftime("%Y_%m_%d_%H_%M_%S")
        res_dir = Path(f"{str(parsed.in_dir)}/safe_results_{formatted}")
        parsed.results_dir =  res_dir
        res_dir.mkdir(exist_ok=True)
        print(f'All results will be saved to {parsed.results_dir}')
        
    if parsed.head_dir == Path.cwd():
        parsed.head_dir =  Path(f"{str(parsed.head_dir)}/safe")
        
    if not parsed.slant and not parsed.synth:
        raise ValueError(f"Incomplete command: please specify '--slant' or '--synth' to specify segmentation(s) in {parsed.in_dir}")
    
    # SLANT
    if parsed.slant:
        print("===== Running safe for slant segmentations =====")
        get_vols_slt([
            "--in-dir", str(parsed.in_dir),
            "--results-dir", str(parsed.results_dir),
            "--head-dir", str(parsed.head_dir)
        ])
        
        print("===== Determining safe decisions for slant =====")
        safe_for_slant(f'{parsed.results_dir}/slant_volumetrics.csv', parsed.head_dir)
    
    # SynthSeg
    if parsed.synth:
        print("Running safe for synthseg segmentations")
        get_vols_syn([
            "--in-dir", str(parsed.in_dir),
            "--results-dir", str(parsed.results_dir),
            "--head-dir", str(parsed.head_dir)
        ])
        
        print("===== Determining safe decisions for synthseg =====")
        safe_for_synth(f'{parsed.results_dir}/synthseg_volumetrics.csv', parsed.head_dir)
    
    # call
    
if __name__ == "__main__":
    main()
