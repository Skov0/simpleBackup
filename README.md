# simpleBackup
Really simple and quick backup script written in Python for backing up a directory and a MySQL database on Linux.

Can be set to run automatically using cronjob, use example below to run everyday at 9 PM:
```
0 21 * * * /usr/bin/python simpleBackup.py >> simpleBackup.log
```


The script requires ftplib.

