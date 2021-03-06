# Precalculated Processed Versions of PTM data
This directory contains different versions of the PTM and CCLE expression data sets after various filterings and normalizations including:
* filter: filtering out missing data
* col-qn: column quantile normalization
* row-zscore: row zscoring

The filename describes the sequential processing steps taken on the data. For instance, `ptm_col-qn_row-zscore.txt` contains PTM data that has two processing steps: 1) column quantile normalization followed by row Z-score (note that files starting with `ptm_` contain PTM data from the 37 cell lines that are also found in the CCLE data, look for files that begin with ptm45 for ptm data from all 45 cell line measurements).

## PTM Datasets
As noted above PTM files are in two formats: 1) `ptm` which includes 37 cell lines found in both the PTM and CCLE data, and 2) `ptm45` which includes all 45 non-unique cell lines found in the CST data.

## QN Normalization
I performed column quantile normalization using the normal quantile normalization [procedure](https://en.wikipedia.org/wiki/Quantile_normalization), with one modification to deal with missing data. First I made a 'mask' that held the positions of all missing data in the PTM dataset. Second, I swapped in zeros for missing data. Third, I ran quantile normalization. Fourth, I swapped back in NaNs using the 'mask' from earlier.

## Python Scripts
I used the following [script](https://github.com/MaayanLab/CST_Lung_Cancer_Viz/blob/master/notebooks/precalc_PTM_norm.py) to calculate these different versions of the PTM data:

