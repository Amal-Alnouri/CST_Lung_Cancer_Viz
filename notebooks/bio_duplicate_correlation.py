import numpy as np
import pandas as pd
from scipy.stats import pearsonr

import matplotlib.pyplot as plt
# %matplotlib inline
import matplotlib
matplotlib.style.use('ggplot')

def main():
  pass


def compare_duplicate_non_duplicate_correlation():

  print('calculating cell-line correlations')

  data_type = ['ptm45_none', 'ptm45_col-qn', 'ptm45_col-iqn', 'ptm45_col-qn_row-zscore','ptm45_filter_none', 'ptm45_filter_col-qn', 'ptm45_filter_col-qn_row-zscore']

  bar_names = []
  bar_values = []

  for inst_type in data_type:
    inst_results = compare_duplicates_to_other(inst_type)

    # print(inst_results)

    for inst_repeat in inst_results:

      full_name = inst_type + '-' + inst_repeat

      # make list of bar names
      bar_names.append(full_name.replace('ptm45_',''))

      # make a list of bar values (correlations)
      bar_values.append(inst_results[inst_repeat][0])

  fig_data = pd.Series(data=bar_values, index=bar_names)

  return fig_data

def compare_duplicates_to_other(data_type):
  '''
  Compare duplicate and non-duplicate cell-line correlations
  '''
  from scipy.spatial.distance import pdist, squareform
  from clustergrammer import Network
  from copy import deepcopy


  filename = '../lung_cellline_3_1_16/lung_cl_all_ptm/precalc_processed/' + \
             data_type + '.txt'

  # load file and export dataframe
  net = deepcopy(Network())
  net.load_file(filename)
  net.swap_nan_for_zero()
  tmp_df = net.dat_to_df()
  df = tmp_df['mat']

  # get cell line names
  cols = df.columns.tolist()

  # transpose to calculte cell line distance matrix

  inst_results = calc_corr(df)

  return inst_results

def calc_corr(df):

  cols = df.columns.tolist()

  dist_mat = np.zeros([len(cols), len(cols)])

  rep_corr = []
  other_corr = []

  rep_pval = []
  other_pval = []

  for x_index in range(len(cols)):
    for y_index in range(len(cols)):

      if x_index <= y_index:
        col_1 = cols[x_index]
        col_2 = cols[y_index]

        vect_1 = df[col_1]
        vect_2 = df[col_2]

        corr_info = pearsonr(vect_1, vect_2)

        inst_corr = corr_info[0]
        inst_pval = corr_info[1]

        dist_mat[x_index, y_index] = inst_corr

        if cols[x_index] != cols[y_index]:
          if cols[x_index].split('_')[0] == cols[y_index].split('_')[0]:
            rep_corr.append(inst_corr)
            rep_pval.append(inst_pval)
          else:
            other_corr.append(inst_corr)
            other_pval.append(inst_pval)

  exp_df = pd.DataFrame(data=dist_mat, index=cols, columns=cols)

  # print(len(rep_pval))
  # print(len(other_pval))

  mean_rep_pval = np.mean(rep_pval)
  mean_other_pval = np.mean(other_pval)

  mean_rep_pval = int(mean_rep_pval*1000)/1000.0
  mean_other_pval = int(mean_other_pval*1000)/1000.0

  mean_rep_corr = np.mean(rep_corr)
  mean_other_corr = np.mean(other_corr)

  mean_rep_corr = int(mean_rep_corr*100)/100.0
  mean_other_corr = int(mean_other_corr*100)/100.0

  results = {}
  results['bio_repeat'] = [mean_rep_corr, mean_rep_pval]
  results['not_repeat'] = [mean_other_corr, mean_other_pval]

  return results

def calc_pdist(df):
  df = df.transpose()

  dist_mat = pdist(df, metric='correlation')

  print(len(dist_mat))
  print(max(dist_mat))
  print(min(dist_mat))

  dist_mat = squareform(dist_mat)

  # dist_mat = 1 - dist_mat

  exp_df = pd.DataFrame(data=dist_mat, index=cols, columns=cols)

  exp_df.to_csv('tmp_cl_dist_mat.txt', sep='\t', na_rep='nan')

# main()