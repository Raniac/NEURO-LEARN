import logging
import time
import os
import pandas as pd
import nilearn
import numpy as np

def test(workDir, dataDir, saveIntermediate):
    """
    :param workDir: the directory where the result files are stored
    :param dataDir: the directory where data files can be found
    :return: None
    """
    
    logging.info('Testing function calling.')
    time.sleep(1)
    logging.info('Loading models...')
    time.sleep(1)
    logging.info('Computing image 1...')
    time.sleep(1)
    logging.info('Computing image 2...')
    time.sleep(1)

    pseudoData = {'ID': ['001', '002'], 'Feature0': ['0.1', '0.05']}
    pseudoData = pd.DataFrame(pseudoData)
    pseudoData.to_csv(workDir + os.environ['USERNAME'] + '_' + time.strftime('%y%m%d') + '_' + str(len(pseudoData.ID)) + '_bcn.csv')

    return

def preprocessing():
    pass

def computeBCN():
    pass

def testNilearn(workDir, dataDir, saveIntermediate):
    img = nilearn.image.load_img(dataDir + '/fMRI/NC_08_0001/NC_08_0001.nii')

    confounds = nilearn.image.high_variance_confounds(img, n_confounds=5, percentile=2.0)
    img = nilearn.image.clean_img(img, detrend=True, standardize=True, confounds=confounds)
    img = nilearn.image.smooth_img(img, 4)
    coords_table = pd.read_csv(dataDir + '/atlas/AAL90.csv', encoding='gbk')
    coords = pd.concat([coords_table.MNIX, coords_table.MNIY, coords_table.MNIZ], axis=1)
    print(coords_table)

    from nilearn import input_data
    masker = input_data.NiftiLabelsMasker(labels_img=dataDir + '/atlas/AAL_Contract_90_2MM.nii', standardize=True, memory='nilearn_cache', verbose=5)
    time_series = masker.fit_transform(img)
    print(time_series.shape)

    from nilearn import connectome
    correlation_measure = connectome.ConnectivityMeasure(kind='partial correlation')
    correlation_matrix = correlation_measure.fit_transform([time_series])[0]
    np.fill_diagonal(correlation_matrix, 0)

    from nilearn import plotting
    plotting.plot_matrix(correlation_matrix, colorbar=True, vmax=0.8, vmin=-0.8)
    plotting.plot_connectome(correlation_matrix, coords, edge_threshold="97%", colorbar=True)
    plotting.show()