import logging
import time
import os
import zipfile
import pandas as pd
import nilearn
import numpy as np
import matplotlib.pyplot as plt
import codecs
import csv
from nilearn import input_data, plotting, connectome

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

# def writeAllFileToZip(workDir, absDir, zipFile):
#     for f in os.listdir(absDir):
#         absFile = os.path.join(absDir, f)
#         if os.path.isdir(absFile):
#             relFile = absFile
#             zipFile.write(relFile)
#             writeAllFileToZip(absFile, zipFile)
#         else:
#             relFile = absFile
#             zipFile.write(relFile)
#     return

def testNilearn(workDir, dataDir, saveIntermediate):
    """
    :param workDir: the directory where the result files are stored
    :param dataDir: the directory where data files can be found
    :param saveIntermediate: determine if the intermediate files will be saved
    :return: None
    """

    filenames = os.listdir(dataDir + '/fMRI/')
    img_names = [dataDir + '/fMRI/' + filename + '/' + filename + '.nii' for filename in filenames]
    resultDir = workDir + '/connectivity_matrices/'
    os.makedirs(resultDir)
    

    for idx, img_name in enumerate(img_names):
        logging.info('Computing image ' + str(idx) + ' for subject ' + filenames[idx])
        img = nilearn.image.load_img(img_name)

        logging.info('Preprocessing image ...step1')
        # confounds = nilearn.image.high_variance_confounds(img, n_confounds=5, percentile=2.0)
        # img = nilearn.image.clean_img(img, detrend=True, standardize=True, confounds=confounds)
        img = nilearn.image.smooth_img(img, 4)
        coords_table = pd.read_csv(dataDir + '/atlas/AAL90.csv', encoding='gbk')
        coords = pd.concat([coords_table.MNIX, coords_table.MNIY, coords_table.MNIZ], axis=1)
        masker = input_data.NiftiLabelsMasker(labels_img=dataDir + '/atlas/AAL_Contract_90_2MM.nii', standardize=True, memory='nilearn_cache')
        time_series = masker.fit_transform(img)

        if saveIntermediate != 'n':
            intermDir = workDir + '/intermediate_files/'
            if not os.path.exists(intermDir):
                os.makedirs(intermDir)
            plotting.plot_img(img.slicer[:, :, :, 100])
            plt.savefig(intermDir + filenames[idx] + '_preprocessed_step1.png')
            # import nibabel

        logging.info('Computing connectome ...step2')
        correlation_measure = connectome.ConnectivityMeasure(kind='partial correlation')
        correlation_matrix = correlation_measure.fit_transform([time_series])[0]
        # correlation_vector = connectome.sym_matrix_to_vec(correlation_matrix, discard_diagonal=True)
        # correlation_vector = list(correlation_vector)
        # correlation_vector.insert(0, filenames[idx])
        # writer.writerow(correlation_vector)

        if saveIntermediate != 'n':
            plotting.plot_matrix(correlation_matrix, colorbar=True, vmax=0.8, vmin=-0.8)
            plt.savefig(intermDir + filenames[idx] + '_matrix_step2.png')
            plotting.plot_connectome(correlation_matrix, coords, edge_threshold="97%", colorbar=True)
            plt.savefig(intermDir + filenames[idx] + '_connectome_step2.png')

        with codecs.open(resultDir + '/' + filenames[idx] + '.csv', 'w+', encoding='gbk') as result_csv:
            writer = csv.writer(result_csv, delimiter=',')
            for row in correlation_matrix:
                writer.writerow(row)

    # logging.info('Packing results ...step3')
    # with zipfile.ZipFile(workDir + '/' + os.environ['USERNAME'] + '_' + time.strftime('%y%m%d') + '_' + str(len(filenames)) + '_bcn.zip', 'w', zipfile.ZIP_DEFLATED) as zipFile:
    #     absDir = resultDir
    #     writeAllFileToZip(workDir, absDir, zipFile)