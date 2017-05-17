### FROM: http://sametmax.com/les-environnement-virtuels-python-virtualenv-et-virtualenvwrapper/

to execute the script WITHOUT any activation of VirtualEnv:

```
/home/me/Documents/Codes/python/sb_dwn_logs/env/bin/python dwn_sb_logs.py
```

===========

You have to create few things to make it works:

1- create few logs directories if those scripts are going to fail:

```
mkdir -p apilogs/downloads
mkdir -p apilogs/uploads
```

2- you have to write a **s3config.py** containing your S3 API Key & Secret:

```
AWS_S3_KEY ='AZERTYUIOPQSDFGHJKLMWXCVBN'
AWS_S3_SECRET = 'NBVCXW321MLKJHGF654+POIUYT/789.AZERTY'

if __name__ == '__main__':
    print(f"Key: {AWS_S3_KEY}")
    print(f"SECRET: {AWS_S3_SECRET}")
```

3- run dwn_sb_logs.py first, to download sodabar log from external server:

```
python dwn_sb_logs.py
```

*This script create automatically a new directory called "logs" containing all
distant log files, formatted by date (FR format) and time.
It puts a new line in "apilogs/downloads/timeline.log", with 2 cases:
INFO: everything works fine
WARNING: something wrong with the GET request over http.*

4- run aws.py script, to upload to your S3 instance:
```
python aws.py
```

*This script is uploading each file in "logs/" directory to AWS S3 bucket of
choice.
It puts also a new line in "apilogs/uploads/state_of_union.log", with 2 cases:
INFO: everything is running well
WARNING: no way to upload to AWS server, for any reason.*

5- check success/error in logs:
```
tail -f apilogs/downloads/timeline.log

tail -f apilogs/uploads/state_of_union.log
```

Good nite!
