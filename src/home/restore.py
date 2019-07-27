import gzip
import subprocess
import os
from django.conf import settings


psql = "C:\\Program Files\\PostgreSQL\\10\\bin\\psql.exe"
USER = settings.DB_USER
PASS = settings.DB_PASS
HOST = settings.DB_HOST
DB = settings.DB_NAME

BACKUP_DIR = "D:\\backups\\backup.gz"
cmd = f"{psql} -U {USER} -d {DB} -f backup.sql"
# psql -U postgres -d croma  -f croma_backup_20-July-2019.sql
