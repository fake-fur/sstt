#!/usr/local/bin/python3

import sys
import sqlite3
import configparser

# read dbpath from config file
config = configparser.ConfigParser()
config.read('sstt.config')
dbpath = config.get('database','dbpath',fallback='sstt.db')
conn = sqlite3.connect(dbpath)
conn.row_factory = sqlite3.Row

conn.execute("""
	create table if not exists tbl_times
	(id integer primary key not null,
        status text default 'A',
	project text not null,
	start datetime default current_timestamp,
	end datetime default null);
""")

# ok so we need 2 arguments:
# project_name & command (start|stop)
if len(sys.argv) < 2:
	print("Missing arguments")
	sys.exit(-1)

cmd = sys.argv[1].upper()

try:
	project = sys.argv[2]
except:
	project = "-"


if cmd == "START":
	# do we have an open project called that already? if so ignore start command
	print("starting: ", project)
	conn.execute("""insert into tbl_times (project) values (?)""",[project])
	conn.commit()

elif cmd == "STOP":
	# do we have an open project called that? if so close it
	res = conn.execute("""select id from tbl_times where project=? and end is null order by id desc limit 1""",[project])
	row = res.fetchone()
	if row != None:
		print("Stopping: ", project)
		conn.execute("""update tbl_times set end=current_timestamp where id=?""",[row[0]])
		conn.commit()

elif cmd == "REPORT":
	# do a report on all projects grouped by project
	for row in conn.execute("""
		select project,
		strftime('%Y-%m',start) yr_mon,
		round(sum(julianday(end) - julianday(start))*24*60,0) as mins
		from tbl_times
		group by yr_mon,project
	"""):
		t = divmod(row['mins'],60)
		print("%s: %s - %d:%d hrs" % (row['yr_mon'],row['project'],t[0],t[1]))

elif cmd == "LIST":
	# show listing of all items in given project
	print()
	for row in conn.execute("""select id,status,project,start,end from tbl_times where project=? order by id""",[project]):
		print(" > %d | %s | %s | %s | %s" % (row['id'],row['status'],row['start'],row['end'],row['project']))
	print()

elif cmd == "PROJECTS":
	# show listing of all project names
	print()
	for row in conn.execute("""select distinct project from tbl_times order by project"""):
		print(" > %s" % (row['project']))
	print()	
