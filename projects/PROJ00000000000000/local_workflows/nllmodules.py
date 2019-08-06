import logging
import time
import os
import pandas as pd
import nilearn
import numpy as np
import codecs
import csv

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
    """
    :param workDir: the directory where the result files are stored
    :param dataDir: the directory where data files can be found
    :param saveIntermediate: determine if the intermediate files will be saved
    :return: None
    """

    filenames = os.listdir(dataDir + '/fMRI/')
    img_names = [dataDir + '/fMRI/' + filename + '/' + filename + '.nii' for filename in filenames]
    results_csv = codecs.open(workDir + '/' + os.environ['USERNAME'] + '_' + time.strftime('%y%m%d') + '_' + str(len(filenames)) + '_bcn.csv', 'w+', encoding='gbk')
    writer = csv.writer(results_csv, delimiter=',')
    writer.writerow(['ID'])

    for idx, img_name in enumerate(img_names):
        logging.info('Computing image ' + str(idx) + ' for subject ' + filenames[idx])
        img = nilearn.image.load_img(img_name)

        # confounds = nilearn.image.high_variance_confounds(img, n_confounds=5, percentile=2.0)
        # img = nilearn.image.clean_img(img, detrend=True, standardize=True, confounds=confounds)
        img = nilearn.image.smooth_img(img, 4)
        coords_table = pd.read_csv(dataDir + '/atlas/AAL90.csv', encoding='gbk')
        coords = pd.concat([coords_table.MNIX, coords_table.MNIY, coords_table.MNIZ], axis=1)
        # print(coords_table)
        logging.info('The shape of the image is ' + str(img.shape))

        from nilearn import input_data
        masker = input_data.NiftiLabelsMasker(labels_img=dataDir + '/atlas/AAL_Contract_90_2MM.nii', standardize=True, memory='nilearn_cache')
        time_series = masker.fit_transform(img)
        logging.info('The shape of the time series is ' + str(time_series.shape))

        if saveIntermediate != 'n':
            dir2Save = workDir + '/intermediate/'
            if not os.path.exists(dir2Save):
                os.makedirs(dir2Save)
            from nilearn import plotting
            plotting.plot_img(img.slicer[:, :, :, 100])
            import matplotlib.pyplot as plt
            plt.savefig(dir2Save + filenames[idx] + '_preprocessed.png')
            # import nibabel

        from nilearn import connectome
        correlation_measure = connectome.ConnectivityMeasure(kind='partial correlation')
        correlation_matrix = correlation_measure.fit_transform([time_series])[0]
        correlation_vector = connectome.sym_matrix_to_vec(correlation_matrix, discard_diagonal=True)
        correlation_vector = list(correlation_vector)
        correlation_vector.insert(0, filenames[idx])
        writer.writerow(correlation_vector)

        if saveIntermediate != 'n':
            from nilearn import plotting
            plotting.plot_matrix(correlation_matrix, colorbar=True, vmax=0.8, vmin=-0.8)
            plt.savefig(dir2Save + filenames[idx] + '_matrix.png')
            plotting.plot_connectome(correlation_matrix, coords, edge_threshold="97%", colorbar=True)
            plt.savefig(dir2Save + filenames[idx] + '_connectome.png')
    results_csv.close()