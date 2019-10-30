import argparse
from musicID import MusicID
from fileUtils import isFile, isDir
from searchUtils import findAll

def getFiles(fileval, dirval):
    files = []
    if fileval is not None:
        if isFile(fileval) is True:
            files = [fileval]
        else:
            raise ValueError("File {0} is not a file!".format(fileval))
            
    if dirval is not None:
        if isDir(dirval) is True:
            files = findAll(dirval)
        else:
            raise ValueError("File {0} is not a file!".format(fileval))
            
    return files

def fix(val):
    if val is None:
        return ""
    if isinstance(val, list):
        if len(val) > 0:
            return val[0]
        else:
            return str(val)
    return val
    
def p(vals):
    vals = [fix(x) for x in vals]
    print("{0: <4}{1: <6}{2: <7}{3: <30}{4: <30}{5: <30}{6: <40}{7: <10}".format(vals[0], vals[1], vals[2], vals[3], vals[4], vals[5], vals[6], vals[7]))

def header():
    p(["##", "Disc", "Track", "AlbumArtist", "Artist", "Album", "Title", "Size"])
    p(["--", "----", "-----", "-----------", "------", "-----", "-----", "----"])

def main(args):
    
    print('Artist      = {!r}'.format(args.artist))
    print('Album       = {!r}'.format(args.album))
    print('AlbumArtist = {!r}'.format(args.albumartist))
    print('File        = {!r}'.format(args.file))
    print('Dir         = {!r}'.format(args.dir))

    files = getFiles(args.file, args.dir)
    header()
    for i,ifile in enumerate(files):
        results = MusicID(ifile)
        if results.skip is True:
            continue
        r = results.getInfo()

            
        ## Artst
        if args.artist is not None:
            oldName = r["Artist"]
            results.setTag("Artist", args.artist)
            
        r = results.getInfo()
        #if results.isValid() is False:
        #    continue
        #print('R ==>',r)
        p([i, r["DiscNo"], r["TrackNo"], r["AlbumArtist"], r["Artist"], r["Album"], r["Title"], r["Size"]])



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Music ID Tagger')
    parser.add_argument('-artist', action="store", dest="artist")
    parser.add_argument('-album', action="store", dest="album")
    parser.add_argument('-albumartist', action="store", dest="albumartist")
    parser.add_argument('-show', '-s', action="store", dest="show")
    parser.add_argument('-file', '-f', action="store", dest="file")
    parser.add_argument('-dir', '-d', action="store", dest="dir")
    args = parser.parse_args()
    main(args)