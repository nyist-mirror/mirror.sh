#!/bin/sh

LOCK_FILE=/tmp/rsync.lock
#ARGS=`getopt -o c:: -n 'rsync_mirror.sh' -- "$@"`

#eval set -- "${ARGS}"



if [ -f ${LOCK_FILE} ] #if lock file is exist
then
        exit
else
        trap "rm -fr /tmp/rsync.lock;exit" INT #Before the keyboard Ctrl+c is received, remove the lock File.
        touch ${LOCK_FILE}  #Create Lock File
	
	for i in `cat /data/mirror_list.conf`   
	do

		python /data/mirror.py  --name $i --status rsyncing  --num `ls -lR /usr/mirror/${i} |grep "^-"|wc -l` --size `du -sh /usr/mirror/${i} | cut -f 1`  --log /var/log/mirror/mirror.log  --db=/data/db.json --template /data/templates/index.html  --out /usr/mirror/index.html
        	rsync -azP  --delete mirrors.tuna.tsinghua.edu.cn::$i  /usr/mirror/$i/  &> /dev/null
		python /data/mirror.py  --name $i --status $?  --num `ls -lR /usr/mirror/${i} |grep "^-"|wc -l` --size `du -sh /usr/mirror/${i} | cut -f 1`  --log /var/log/mirror/mirror.log  --db=/data/db.json --template /data/templates/index.html  --out /usr/mirror/index.html
	done
        rm -fr ${LOCK_FILE} #Del Lock File
fi

