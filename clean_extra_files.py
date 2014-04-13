#A small script to clean the extra files from the server dir.
import os, glob

files_to_delete = []

for pyc_file in glob.glob("*.pyc"):
    files_to_delete.append(pyc_file)

for plugin_pyc in glob.glob("plugins/*.pyc"):
    files_to_delete.append(plugin_pyc)

files_to_delete.append("server.log")

for file_to_delete in files_to_delete:
    print "Removing %s..." % file_to_delete
    os.remove(file_to_delete)
