import ftplib
import logging
import os
import datetime

# set the working dir
TEMP_DIR = '/home/backupJob/backups_temp/' # Set the temp folder
os.chdir(TEMP_DIR)

# current time
date = datetime.datetime.today()
date = date.strftime("%d-%m-%Y")

# set filename
FILENAME_FINAL = ''

# create logger
LOG_FILE = 'backup.log'
logger = logging.getLogger('SimpleBackup')
logger.setLevel(logging.DEBUG)

# set level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# set format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
ch.setFormatter(formatter)
logger.addHandler(ch)

def Main():
    logger.info('Backup job stated...')
    # call zipping function
    ZipAndStore()

def ZipAndStore():
    cmd = "sudo zip -r backup%s.zip /home/folder/"%(date) # replace "/home/folder" with the folder you want to backup.
    logger.info('Files are being ziped..')
    os.system(cmd)
    FILENAME_FINAL = "%sbackup%s.zip"%(TEMP_DIR, date)
    logger.info('Files zipped successfully..')
    # ready for upload call ConnectAndUpload
    DumpSQLAndSave(FILENAME_FINAL)

def DumpSQLAndSave(Filename):
    cmdDump = "mysqldump tcdb > backup.sql" # Change tcdb to your db
    logger.debug('Dumping database now..')
    os.system(cmdDump)
    logger.info('Adding database to zip file..')
    cmdSave = "sudo zip -g backup%s.zip backup.sql"%(date)
    os.system(cmdSave)
    ConnectAndUpload(Filename)

def ConnectAndUpload(Filename):
    try:
        logger.info('Connecting to FTP server...')
        session = ftplib.FTP('FTP IP ADDRESS', 'USERNAME', 'PASSWORD')
        logger.debug('Successfully connected!')
	logger.info('Starting upload..')

        # open the file set for upload
	# set new filename
	N_Filename = "backup%s.zip"%(date)
        file = open(Filename, 'rb')
        session.storbinary('STOR %s'%(N_Filename), file)
        logger.info('Backup job done!')
        # lose the seesion
        file.close()
        session.quit()

	# send mail
	succs = 'echo Backup Succesfull | mail -s "BackupJob Done" root@localhost'
	os.system(succs)
	# delete temp files
	DeleteAndCleanup(N_Filename)

    except Exception, e:
        logger.error(e)
	    fail = 'echo Backup Failed | mail -s "BackupJob Done" root@localhost'
	    os.system(fail)

def DeleteAndCleanup(Filename):
	cmdClean = "rm -rf %s%s"%(TEMP_DIR, Filename)
	cmdCleanSQL = "rm -rf backup.sql"
	os.system(cmdClean)
	os.system(cmdCleanSQL)
	logger.info('Temp files was deleted..')


if __name__ == "__main__":
    Main()
