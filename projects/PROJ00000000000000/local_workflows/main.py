import logging
import time
import os

def executeJob(jobID, workDir, dataDir):
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(levelname)s] %(message)s')
    logging.basicConfig(level=logging.ERROR, format='[%(asctime)s %(levelname)s] %(message)s')
    logger = logging.getLogger()
    hdlr = logging.FileHandler(workDir + '/autosave_' + jobID + '.log')
    hdlr.setFormatter(logging.Formatter('[%(asctime)s %(levelname)s] %(message)s'))
    logger.addHandler(hdlr)

    logging.info('Working directory: ' + workDir)
    logging.info('Data directory: ' + dataDir)
    
    # ========================================
    # Call NEURO-LEARN-LOCAL modules
    # ========================================
    import nllmodules as nll
    nll.test(workDir, dataDir)

    print('Job is done! Check the autosaved log at ' + workDir + ' for details!')

if __name__ == "__main__":
    print()
    print('\033[0;36;40mNL\033[0m \033[1;36mNEURO-LEARN\033[0m')
    print()
    print('Welcome to \033[0;36mNEURO-LEARN-LOCAL\033[0m! This application is part of \033[0;36mNEURO-LEARN\033[0m developed by Raniac from South China University of Technology.')
    print('We assume that you know about \033[0;36mNEURO-LEARN\033[0m. If not, please check this out! >> https://github.com/Raniac/NEURO-LEARN/wiki')
    time.sleep(1)
    print()
    print('Now let\'s get started! Do you know how to use this? [y/n]')
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
        print('Where do we find the data? (e.g. ' + os.environ['HOME'] + '/data/)')
        dataDir = input()
        if os.path.exists(dataDir):
            print('Path validity verified!')
        
            # Job Execution
            print()
            print('\033[1mJOB EXECUTION\033[0m')
            executeJob(jobID, workDir, dataDir)
        else:
            print('\033[0;31mError: invalid data path!\033[0m')
            os.removedirs(workDir)
    else:
        print('Looks like you need a hand! Try this link! >> https://github.com/Raniac/NEURO-LEARN/wiki')

    print()
    print('Alright! Thanks for using \033[0;36mNEURO-LEARN-LOCAL\033[0m! Press any key to exit! :-)')
    input()