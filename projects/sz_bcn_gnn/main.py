import logging
import time
import os

def executeJob(jobID, workDir, dataDir, saveIntermediate):
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(levelname)s] %(message)s')
    logging.basicConfig(level=logging.ERROR, format='[%(asctime)s %(levelname)s] %(message)s')
    logger = logging.getLogger()
    hdlr = logging.FileHandler(workDir + '/autosave_' + jobID + '.log')
    hdlr.setFormatter(logging.Formatter('[%(asctime)s %(levelname)s] %(message)s'))
    logger.addHandler(hdlr)

    logging.info('Working directory: ' + workDir)
    logging.info('Data directory: ' + dataDir)
    logging.info('Username: ' + os.environ['USERNAME'])
    if saveIntermediate == 'n':
        logging.info('Intermediate files will be ignored.')
    else:
        logging.info('Intermediate files will be saved at ' + workDir + '!')
    print()
    
    # ========================================
    # Call NEURO-LEARN-LOCAL modules
    # ========================================
    import nllmodules as nll
    nll.testNilearn(workDir, dataDir, saveIntermediate)

    print('Job is done! Check the autosaved log at ' + workDir + ' for details!')

if __name__ == "__main__":
    print()
    print('\033[0;36;40mNL\033[0m \033[1;36mNEURO-LEARN\033[0m')
    print()
    print('Welcome to \033[0;36mNEURO-LEARN-LOCAL\033[0m! This application is part of \033[0;36mNEURO-LEARN\033[0m developed by Raniac from South China University of Technology.')
    print('We assume that you know about \033[0;36mNEURO-LEARN\033[0m. If not, please check this out! >> https://github.com/Raniac/NEURO-LEARN/wiki')
    print()
    print('Now let\'s get started! This particular version of \033[0;36mNEURO-LEARN-LOCAL\033[0m focuses on extracting brain connectivity features from fMRI data.')
    print('Do you know how to use this? [y/n]')
    doKnow = input()

    if doKnow == 'y' or doKnow == 'Y':

        # Job Configuration
        print()
        print('\033[1mJOB CONFIGURATION\033[0m')
        jobID = time.strftime('%Y-%m-%d-%H-%M-%S')
        print('Job ID: ' + jobID)
        print('Where do we save the results and logs? (Default: ' + os.environ['HOME'] + '/neurolearn/jobs/' + jobID + '/)')
        workDir = input()
        if not workDir:
            workDir = os.environ['HOME'] + '/neurolearn/jobs/' + jobID + '/'
        if not os.path.exists(workDir):
            os.makedirs(workDir)
        print('Do you want us to save the intermediate files? [y/n] (Default: n)')
        saveIntermediate = input()
        if (not saveIntermediate) and (saveIntermediate != ('y' or 'Y')):
            saveIntermediate = 'n'
        print('Where do we find the data? (e.g. ' + os.environ['HOME'] + '/data/)')
        dataDir = input()
        if os.path.exists(dataDir):
            print('Path validity verified!')
        
            # Job Execution
            print()
            print('\033[1mJOB EXECUTION\033[0m')
            executeJob(jobID, workDir, dataDir, saveIntermediate)
        else:
            print('\033[0;31mError: invalid data path!\033[0m')
            os.removedirs(workDir)
    else:
        print('Looks like you need a hand! Try this link! >> https://github.com/Raniac/NEURO-LEARN/wiki')

    print()
    print('Alright! Thanks for using \033[0;36mNEURO-LEARN-LOCAL\033[0m! Press any key to exit! :-)')
    input()