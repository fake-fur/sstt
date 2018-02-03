# sstt
Stupidly Simple Time Tracker

 Really the title says it all

This is just a ridiculously simple time tracker for my personal use written in Python talking to SQLite. I put the database file in an owncloud folder to sync it between my machines, again to keep it stupidly simple. Really, this is just a starting point for a solution to a problem I choose to solve for myself but feel free to use and improve if you care.

commands currently recognized:

#start {project}
creates a project entry for {project} with now as start time

#stop {project}
looks for open {project} entry and closes it if found - does nothing otherwise

#report {project}
will print out total hours for {project} for each year/month

#list {project}
prints list of all individual entries for given {project} name

#projects
will list all project names currently in the database

