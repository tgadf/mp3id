from os.path import join
from searchUtils import findDirs
from fsUtils import moveDir

for dname in findDirs("./"):
    sep  = " - "
    vals = dname.split(sep)
    newName = sep.join(vals[1:])
    moveDir(dname, newName, debug=True)
