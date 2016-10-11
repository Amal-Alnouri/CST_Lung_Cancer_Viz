def main():
  '''
  This script will make cell-line by cell-line distnace vectors and using the
  gene expression data (with and withouth gene-zscoring) and PTM data. I'll
  then check how different PTM data processing methods (normalization/filtering)
  affect the distances (and/or similarities) between all cell line pairs in
  gene-expression space
  '''

  # pre-processing of PTM data to make comparable to gene-exp
  ############################################################
  # calculate similarity vector based on ptm data
  save_gene_exp_compatible_ptm_data()

  # calculate similarities of cell lines
  ##########################################
  # # calculte similarity vector based on expression data
  # sim_exp = calc_cl_sim(data_type='exp')

  # # calculate alternate similiarites
  # # sim_exp_filt = calc_cl_sim(data_type='exp', var_filter=1000)
  # sim_exp_filt = calc_cl_sim(data_type='exp', var_filter=1000)

  # # compare similarity vectors based on expression and ptm data
  # ###############################################################
  # sim_data = compare_sim_vectors(sim_exp, sim_exp_filt)
  # print(sim_data)

def save_gene_exp_compatible_ptm_data():
  '''
  This will make a PTM matrix that is compatible with (e.g. easily comparable)
  with the gene expression matrix: 1) average duplicate cell line measurements,
  2) only include the 37 cell lines that are found in CCLE, 3) put cell lines
  into the same order as the gene expression data.
  '''
  import pandas as pd
  from clustergrammer import Network
  from copy import deepcopy


  # # only need to run once
  # ############################
  # combine_and_save_ptm()

  # only need to run once
  average_plex_runs()

  # # load all ptm ratios
  # filename_all_ptm = '../lung_cellline_3_1_16/lung_cellline_TMT_all_ptm_ratios.tsv'

  # net_ptm = deepcopy(Network())
  # net_ptm.load_file(filename_all_ptm)

  # tmp_df = net_ptm.dat_to_df()
  # df_ptm = tmp_df['mat']

  # print('shape of all ptms')
  # print(df_ptm.shape)

  # # get gene-exp cell lines
  # net_exp = deepcopy(Network())
  # net_exp.load_file('../CCLE_gene_expression/CCLE_NSCLC_all_genes.txt')

  # tmp_df = net_exp.dat_to_df()
  # df_exp = tmp_df['mat']

  # print('shape of exp')
  # print(df_exp.shape)



  # # only keep gene expression cell lines
  # #######################################

  # cl_ptm = df_ptm.columns.tolist()
  # cl_exp = df_exp.columns.tolist()

  # cl_ptm = [i.split('_')[0] for i in cl_ptm]

  # print(cl_ptm)

  # cl_found = []
  # for inst_cl in cl_exp:

  #   if inst_cl in cl_ptm:
  #     cl_found.append(inst_cl)


  # print(len(cl_found))


def average_plex_runs():
  import pandas as pd
  from clustergrammer import Network
  from copy import deepcopy

  print('averaging plex runs and saving to new tsv')

  # load all ptm ratios
  filename_all_ptm = '../lung_cellline_3_1_16/lung_cellline_TMT_all_ptm_ratios.tsv'

  net_ptm = deepcopy(Network())
  net_ptm.load_file(filename_all_ptm)

  tmp_df = net_ptm.dat_to_df()
  df_ptm = tmp_df['mat']

  ptm_cols = df_ptm.columns.tolist()

  print('shape of all ptms')
  print(df_ptm.shape)

  cl_with_duplicates = []

  for inst_cl in ptm_cols:
    if '_plex' in inst_cl:
      print(inst_cl)

      inst_cl = inst_cl.split('_plex')[0]
      cl_with_duplicates.append(inst_cl)

  cl_with_duplicates = list(set(cl_with_duplicates))
  cl_with_duplicates.sort()

  # merge data



def combine_and_save_ptm():
  # combine all ptm data into single dataframe
  #################################################################
  # use simple col names

  from clustergrammer import Network
  import pandas as pd
  from copy import deepcopy

  ptm_data = {
  'phos': '../lung_cellline_3_1_16/lung_cellline_phospho/lung_cellline_TMT_phospho_combined_ratios.tsv',
  'act': '../lung_cellline_3_1_16/lung_cellline_Ack/lung_cellline_TMT_Ack_combined_ratios.tsv',
  'met_arg': '../lung_cellline_3_1_16/lung_cellline_Rme1/lung_cellline_TMT_Rme1_combined_ratios.tsv',
  'met_lys': '../lung_cellline_3_1_16/lung_cellline_Kme1/lung_cellline_TMT_Kme1_combined_ratios.tsv'
  }

  df_all = pd.DataFrame()

  for inst_type in ptm_data:

    net = deepcopy(Network())
    filename = ptm_data[inst_type]

    net.load_file(filename)

    tmp_df = net.dat_to_df()
    inst_df = tmp_df['mat']

    col_tuples = inst_df.columns.tolist()

    col_names = []
    for inst_tuple in col_tuples:
      col_names.append(inst_tuple[0])

    inst_df.columns = col_names

    print('\ninst_type ' + inst_type)
    print(inst_df.shape)

    df_all = pd.concat([df_all, inst_df], axis=0)

  filename_all_ptm = '../lung_cellline_3_1_16/lung_cellline_TMT_all_ptm_ratios.tsv'

  print('\nshape of mat')
  print(df_all.shape)

  df_all.to_csv(filename_all_ptm, sep='\t')

  print('\ncheck if rows are unique')
  all_rows = df_all.index.tolist()
  print(len(all_rows))
  all_rows = list(set(all_rows))
  print(len(all_rows))

  print('\nnumber of cell lines ')
  print(len(df_all.columns.tolist()))




  # sort names in place
  # col_names.sort()

  # check that the cell lines are in the same order in both exp and PTM data


def calc_cl_sim(data_type='exp', sum_filter=None, var_filter=None,
                    row_zscore=False, col_qn=False, col_zscore=False):
  '''
  calculate cell line similarity based on data_type (e.g. expression) with
  optional filtering and normalization
  '''

  from scipy.spatial.distance import pdist, squareform
  from clustergrammer import Network

  net = Network()

  all_data = {
    'exp':'../CCLE_gene_expression/CCLE_NSCLC_all_genes.txt'
  }

  filename = all_data[data_type]

  net.load_file(filename)

  # col normalization
  ######################

  # run col qn before anything
  if col_qn != False:
    print('column qn')
    net.normalize(axis='col', norm_type='qn')

  # run col zscore before anything
  if col_zscore != False:
    print('zscore the cols')
    net.normalize(axis='col', norm_type='zscore')

  # row normalization
  ######################

  # run row zscore after col qn
  if row_zscore != False:
    print('zscore the rows')
    net.normalize(axis='row', norm_type='zscore')

  # row filtering
  ######################

  # filter rows after normalization
  if sum_filter != None:
    print('filter top ' + str(sum_filter) + ' rows based on sum')
    net.filter_N_top('row', sum_filter, rank_type='sum')

  if var_filter != None:
    print('filter top ' + str(var_filter) + ' rows based on variance')
    net.filter_N_top('row', var_filter, rank_type='var')



  tmp_df = net.dat_to_df()

  df = tmp_df['mat']

  col_names = df.columns.tolist()

  print(df.shape)

  # transpose to calc distance matrix of columns
  df = df.transpose()

  # calculate the similarity of cell line data based on gene expression
  sim = 1 - pdist(df, metric='cosine')

  return sim

def compare_sim_vectors(sim_exp, sim_ptm):
  from scipy.spatial.distance import pdist, squareform
  import numpy as np

  # combine similarity vectors into matrix
  inst_mat = np.vstack((sim_exp, sim_ptm))

  sim_data = 1 - pdist(inst_mat, metric='cosine')

  return sim_data

  # calculate PTM sim mat of cell lines
  ########################################

  # I need to check whether a pairwise complete function exists
  # I will use clustergrammer to do normalization etc.



main()