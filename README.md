# SAFE
Automated quality assurance of segmentation techniques with SAFE: statistically-based failure evaluation.

**Publication**: Bartz, K.M. et al. (in press), "Automated quality assurance of segmentation techniques with statistically-based failure evaluation (SAFE)," in [_Proceedings of SPIE Medical Imaging (SPIE-MI 2026), Vancouver, Canada, February 15-19, 2026_], (2026).

## 1. Introduction and Motivation

Algorithms that segment brain structures into distinct tissue types, parcellate tissues into structural regions, and perform volumetric analyses can provide information about cognitive functions and indicate the onset of neurodegenerative diseases. Quality assurance (QA) is a critical final step after processing when using segmentation results for scientific research or clinical management. Although manual QA strategies are the most reliable solutions for verifying segmentations, these approaches are time consuming and extremely difficult, even for experienced neuroanatomy experts. Our work addresses segmentation algorithms that lack an accompanying QA method.

We construct a normative database (mean and standard deviation) of brain region volumes employing statistics generated on 38,251 publicly available magnetic resonance (MR) images. Manual quality assurance was performed to exclude images with limited field-of-view (FOV), aggressive defacing, motion artifacts, noise, extreme atrophy, visual pathology, and other defects. We then propose the statistically-based failure evaluation (SAFE) approach, a binary classification method to accept or reject a brain segmentation based on the constructed normative values. This method is empirically validated on corrupted images using two algorithms: spatially localized atlas network tiles (SLANT) 3D whole brain segmentation and the SynthSeg segmentation tool, which is part of the FreeSurfer software package.

## 2. Model Distribution Database

We performed SLANT and SynthSeg segmentation on 38,251 training images, and then calculated the volume of each brain region. For each ROI, box-plot statistics were used to classify and remove outlier volumes prior to the calculation of the normative measures. The computed mean and standard deviation for all regions generated a model distribution database (MDD), where
independent MDDs were created for both segmentation methods. These normative measures are distributable, and can be found in the files `normative_volumetrics_slant.csv` and `normative_volumetrics_synthseg.csv` for SLANT and SynthSeg segmentations, respectively. **Note**: all listed volume measures are in units $mm^3$.

## 3. SAFE Method

SAFE is a binary method that takes two inputs: a MDD containing the mean volume and standard deviation for each ROI and a 3D segmented MR image volume. We statistically define in-distribution (ID) and out-of-distribution (OOD) following a Gaussian classification, where ID includes data points within 3 standard deviations of the mean. This QA strategy is based on three verification steps. For each segmented ROI, SAFE first calculates the volume of the region. Then, SAFE normalizes the region volume relative to the total brain volume, which we refer to as the ROI’s brain occupancy. As a first check, the method determines if these two measures for each ROI are ID or OOD. Some regions OOD are acceptable due to unaccounted for factors in the MDD, such as age, sex, and health status. Thus, SAFE proceeds to the next check if 95% of the ROIs are ID. Finally, SAFE checks for missing ROIs, where any zero volumes indicate segmentation failure and results in rejection of the segmentation. The associated code is compatible to run the SAFE method with segmentation from SynthSeg or SLANT.

Due to ventricle enlargement that accompanies age and other diseases, the six regions that encompass the ventricles—3rd ventricle, 4th ventricle, right and left lateral ventricle, and right and left inferior lateral ventricle—were excluded from the SAFE method. The remaining 126 brain regions for SLANT and 92 brain regions for SynthSeg informed the statistical measures stored in the MDD and factored in to the SAFE output decision.

### To run SAFE:

Clone and install this repository. Then, run the following command within the project directory.

```
safe \
  --in-dir {folder_path_to_segmentations} \
  [--results-dir {folder_path_to_store_results}] \
  [--head-dir {path_to_safe_installation}] \
  [--synth] \
  [--slant]
```

If `--results-dir` is not specified, the output results are stored in a new folder on the path given after `--in-dir`. Include the arguments `--synth` and `--slant` to specify which types of segmentations are present in path for `--in-dir`. **Note:** the segmentations must contain the string '_slant' or '_synth' to denote which method (SLANT or SynthSeg, respectively) were applied to generate the resulting segmentation.

The output results include two csv files indicating the SAFE decisions for the corresponding SLANT and SynthSeg segmentations, respectively. Some additional information is provided to aid in further analysis of the data:

1. _zero_count_: counts how many regions were missing (volume of 0 $mm^3$) -- factor in SAFE decision
2. _occ_95_count_: counts how many regions by brain occupancy were between the 95% confidence interval (CI) and 99% CI, based on the normative measures. This measure is not included in the SAFE decision, but is provided to allow additional analysis.
3. _occ_99_count_: counts how many regions by brain occupancy were outliers (outside of 99% CI) -- factor in SAFE decision
4. _vol_95_count_: counts how many regions by volume were between the 95% confidence interval (CI) and 99% CI, based on the normative measures. This measure is not included in the SAFE decision, but is provided to allow additional analysis.
5. _vol_99_count_: counts how many regions by volume were outliers (outside of 99% CI) -- factor in SAFE decision

The regions included in each of these five groups are also listed in the resulting data tables. These categories are mutually exclusive.


## 4. Acknowledgments

We refer to the manuscript associated with this work for full citations and references to the two segmentation methods: SLANT and SynthSeg. The code for both segmentation techniques is open source. Full acknowledgements of the publicly available databases used in this work can also be found in the manuscript associated with this project.

