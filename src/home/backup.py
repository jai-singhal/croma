from subprocess import Popen, PIPE
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED
import os
from django.conf import settings


class BackupDatabase():
    def __init__(self, *args, **kwargs):
        self.pg_dump = settings.PGDUMP_LOCATION
        self.USER = settings.DB_USER
        self.PASS = settings.DB_PASS
        self.HOST = settings.DB_HOST
        self.DB = settings.DB_NAME
        self.BACKUP_LOCATION = settings.DB_BACKUP_LOCATION
        super().__init__(*args, **kwargs)


    def getBackupFileName(self, sameDay = False):
        currentDateTime = datetime.now().strftime("%d-%B-%Y")
        BACKUP_FILEPATH = f"{self.BACKUP_LOCATION}\\croma_backup_{currentDateTime}"
        BACKUP_FILE = f"croma_backup_{currentDateTime}"
        currHour = datetime.now().hour
        if sameDay:
            BACKUP_FILEPATH = BACKUP_FILEPATH + f"[{currHour}].gz"
            BACKUP_FILE = BACKUP_FILE + f"[{currHour}].gz"
        else:
            BACKUP_FILEPATH = BACKUP_FILEPATH + f".gz"
            BACKUP_FILE = BACKUP_FILE + f".gz"
        return BACKUP_FILEPATH, BACKUP_FILE

    def getBackupZipFileName(self):
        currentMonthYear = datetime.now().strftime("%B-%Y")
        BACKUP_ZIP = f"{self.BACKUP_LOCATION}\\croma-backup-{currentMonthYear}.zip"
        return BACKUP_ZIP

    def getCommand(self, backupfname):
        cmd = f"{self.pg_dump} -U {self.USER} -h {self.HOST} -Z 9 -f {backupfname} {self.DB}"

        return cmd

    def removeBackupFile(self, backupfname):
        try:
            os.remove(backupfname)
            return True
        except:
            return False

    def getResolvedBackupFileName(self, gzipFile, forcefully):
        backupfpath, backupfname = self.getBackupFileName()
        if "backups/" + backupfname in gzipFile.namelist():
            currHour = datetime.now().hour
            if f"backups/{backupfname[:-3]}[{currHour}]{backupfname[-3:]}" in gzipFile.namelist():
                return {
                    "status": False,
                    "code": 203,
                    "message": "Error in writing to gzip File. Duplicate file exists.Try again later"
                }
            if forcefully:
                backupfpath, backupfname = self.getBackupFileName(sameDay = True)
            else:
                return {
                    "status": False,
                    "code": 202,
                    "message": "Error in writing to gzip File. Duplicate file exists. Do you to forcefully create a backup?"
                }
        return backupfpath
   
    def takeBackup(self, backupfname):
        popen = Popen(
            self.getCommand(backupfname), 
            stdout=PIPE, 
            universal_newlines=True
        )
        popen.stdout.close()
        popen.wait()

    def run(self, forcefully = False):
        
        if not os.path.isdir(os.path.dirname(self.getBackupZipFileName())):
            gzipFile = ZipFile(self.getBackupZipFileName(), 'w', ZIP_DEFLATED)
            gzipFile.close()
            
        with ZipFile(self.getBackupZipFileName(), 
                    'a',
                    ZIP_DEFLATED) as gzipFile:
            os.environ['PGPASSWORD'] = self.PASS
            backupfname = self.getResolvedBackupFileName(gzipFile, forcefully)
            if isinstance(backupfname, dict):
                return backupfname

            self.takeBackup(backupfname)
            try:  
                try:
                    gzipFile.write(backupfname)
                    self.removeBackupFile(backupfname)
                except Exception as e:
                    self.removeBackupFile(backupfname)
                    return {
                        "status": False,
                        "code": 202,
                        "message": f"Error in writing to gzip File. Duplicate file exists!! \n {e}"
                    } 
            except Exception as e:
                return {
                    "status": False,
                    "code": 201,
                    "message": f"Error while taking Backup. Try again later \n {e}"
                }
        
        return {"status": True, "code": 200}    


