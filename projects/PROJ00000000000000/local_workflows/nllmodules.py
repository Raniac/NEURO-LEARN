import logging
import time
import os
import pandas as pd

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