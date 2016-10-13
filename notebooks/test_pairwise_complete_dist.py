def main():
  print('I will set up a pairwise-compete matrix')

  data_type = 'ptm_none'
  dist_metric = 'euclidean'
  compare_pdist_to_custom_dist_mat(data_type=data_type, dist_metric=dist_metric)

  # ###########################################
  # from scipy.spatial.distance import pdist, squareform
  # import scipy.spatial.distance as dist_fun

  # dist_metric = 'euclidean'

  # import numpy as np
  # import pandas as pd
  # vect_1 = np.zeros(10,)
  # vect_2 = np.zeros(10,) + 1

  # vect_1[1] = np.NaN
  # vect_2[9] = np.NaN

  # print(vect_1)
  # print(vect_2)

  # mat = np.vstack((vect_1, vect_2)).transpose()

  # print(mat)

  # df = pd.DataFrame(mat)

  # df = df.dropna(axis=0)

  # print('\nshape after dropping NaNs')
  # print(df.shape)

  # df_mean = df.mean(axis=1)

  # print(df_mean)

  # df = df.transpose()
  # dist_pdist = pdist(df, metric=dist_metric)

  # print('\npdist Distance of two vectors')
  # print(dist_pdist)

  # df = df.transpose()

  # inst_dist = dist_fun.euclidean(df[0], df[1])
  # print('\ncustom distance ')
  # print(inst_dist)


def compare_pdist_to_custom_dist_mat(data_type='ptm_none',
   dist_metric='euclidean', swap_nan=True):
  '''
  calculate cell line distance based on data_type (e.g. expression) with
  optional filtering and normalization
  '''

  filename = '../lung_cellline_3_1_16/lung_cl_all_ptm/precalc_processed/' + \
             data_type + '.txt'

  dist_pdist = calc_pdist_dist(filename, data_type, dist_metric)
  dist_custom = calc_custom_dist(filename, data_type, dist_metric,
                                 swap_nan=swap_nan)

  difference = dist_pdist - dist_custom

  print('\nno difference between custom calculation and pdist calculation')
  print('--------------------------------------------------------------------')
  print(dist_pdist[:10])
  print(dist_custom[:10])
  print(sum(difference))

def calc_custom_dist(filename, data_type, dist_metric, swap_nan=True):
  import numpy as np
  import pandas as pd
  import scipy.spatial.distance as dist_fun
  from scipy.spatial.distance import pdist

  df = get_df(filename, swap_nan)

  rows = df.index.tolist()
  cols = df.columns.tolist()

  dist_vector = np.zeros(666,)

  # write for-loop to calculate custom distance matrix and compare result
  # to pdist
  num_calc = 0
  for i in range(len(cols)):

    col_1 = cols[i]

    for j in range(len(cols)):

      if j > i:

        col_2 = cols[j]

        vect_1 = df[col_1]
        vect_2 = df[col_2]

        mat = np.vstack((vect_1, vect_2)).transpose()
        df_small = pd.DataFrame(mat)

        # always dropna (nans will be optionally swapped out elsewhere)
        df_small = df_small.dropna(axis=0)

        # calc distance using pdist (only two vectors)
        df_small = df_small.transpose()
        dist_pdist = pdist(df_small, metric=dist_metric)

        # # calculating distances of two vectors (using pdist instead)
        # if dist_metric == 'euclidean':
        #   inst_dist = dist_fun.euclidean(vect_1, vect_2)
        # elif dist_metric == 'cosine':
        #   inst_dist = dist_fun.cosine(vect_1, vect_2)

        # save to distance vector
        dist_vector[num_calc] = dist_pdist

        num_calc = num_calc + 1

  return dist_vector

def calc_pdist_dist(filename, data_type, dist_metric):
  from scipy.spatial.distance import pdist, squareform

  df = get_df(filename, swap_nan=True)

  # transpose to calc distance matrix of columns
  df = df.transpose()

  dist_pdist = pdist(df, metric=dist_metric)

  return dist_pdist

def get_df(filename, swap_nan=True):
  from copy import deepcopy
  from clustergrammer import Network
  net = deepcopy(Network())

  # load file and export dataframe
  net.load_file(filename)
  if swap_nan == True:
    net.swap_nan_for_zero()
  tmp_df = net.dat_to_df()

  df = tmp_df['mat']

  return df

main()