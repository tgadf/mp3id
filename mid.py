import argparse
from musicID import MusicID
from fileutils import FileInfo, DirInfo
#from fsUtils import mkDir, moveFile, setDir
#from fileUtils import isFile, isDir, getDirname
from searchUtils import findAll, findWalk
from os import getcwd

def getFiles(fileval, dirval):
    finfo = FileInfo(fileval) if isinstance(fileval,str) else None
    dinfo = DirInfo(dirval) if isinstance(dirval,str) else None
    
    files = {}
    if isinstance(finfo,FileInfo):
        if finfo.isFile():
            files[getcwd()] = [fileval]
        else:
            raise ValueError("File {0} is not a file!".format(fileval))
            
    if isinstance(dinfo,DirInfo):
        if dinfo.isDir():
            files = findWalk(dirval)
        else:
            raise ValueError("File {0} is not a file!".format(fileval))
            
    return files

def fix(val):
    if val is None:
        return ""
    if isinstance(val, list):
        if len(val) > 0:
            return str(val[0])
        else:
            return str(val)
    if isinstance(val, tuple):
        return str(val)
    return val
    
def p(vals):
    vals = [fix(x) for x in vals]
    print("{0: <4}{1: <8}{2: <9}{3: <25}{4: <35}{5: <60}{6: <70}{7: <6}".format(vals[0], vals[1], vals[2], vals[3], vals[4], vals[5], vals[6], vals[7]))

def header():
    p(["##", "Disc", "Track", "AlbumArtist", "Artist", "Album", "Title", "Size"])
    p(["--", "----", "-----", "-----------", "------", "-----", "-----", "----"])

def addDefault(args):
    if not any(args.__dict__.values()):
        args.show = True
        args.dir  = getcwd()
    if args.file is None and args.dir is None:
        args.dir  = getcwd()
    if args.search is True:
        args.show = True
        
    return args
    
def main(args):
    args = addDefault(args)
    
    if args.debug is True:
        print('Show        = {!r}'.format(args.show))
        print('Search      = {!r}'.format(args.search))
        print('Artist      = {!r}'.format(args.artist))
        print('Album       = {!r}'.format(args.album))
        print('AlbumArtist = {!r}'.format(args.albumartist))
        print('Title       = {!r}'.format(args.title))
        print('DiscNo      = {!r}'.format(args.discno))
        print('TrackNo     = {!r}'.format(args.trackno))
        print('File        = {!r}'.format(args.file))
        print('Dir         = {!r}'.format(args.dir))

    searchResults = {}
    
    files = getFiles(args.file, args.dir)
    for i,(dirval,filevals) in enumerate(files.items()):
        searchResults[dirval] = []
        j = 0
        first = False

        for jf, ifile in enumerate(filevals):
            results = MusicID(ifile, debug=args.debug)
            if results.skip is True:
                continue
            if first is False:
                first = True
            if first is True:
                print("\nDirectory: {0}".format(dirval))
                header()
                first = None
            r  = results.getInfo()
            j += 1
            
            if args.search is True:
                if args.album is not None:
                    if args.album in r["Album"][0]:
                        searchResults[dirval].append(ifile)
                        continue
                else:
                    raise ValueError("Can only search for album names right now")

            
            if args.show is True:
                p([j, r["DiscNo"], r["TrackNo"], r["AlbumArtist"], r["Artist"], r["Album"], r["Title"], r["Size"]])
                continue

            ## Artst
            if args.artist is not None:
                oldName = r["Artist"]
                results.setTag("Artist", args.artist)

            ## Album
            if args.album is not None:
                oldName = r["Album"]
                results.setTag("Album", args.album)

            ## AlbumArtist
            if args.albumartist is not None:
                oldName = r["AlbumArtist"]
                results.setTag("AlbumArtist", args.albumartist)

            ## Title
            if args.title is not None:
                oldName = r["Title"]
                results.setTag("Title", args.title)

            ## DiscNo
            if args.discno is not None:
                oldName = r["DiscNo"]
                results.setTag("DiscNo", args.discno)

            ## TrackNo
            if args.trackno is not None:
                oldName = r["TrackNo"]
                results.setTag("TrackNo", args.trackno)

            r = results.getInfo()
            p([j, r["DiscNo"], r["TrackNo"], r["AlbumArtist"], r["Artist"], r["Album"], r["Title"], r["Size"]])


    if args.search is True:
        for dirval,files in searchResults.items():
            tmpDir = DirInfo(dirval).join("tmp")
            tmpDir.mkDir()
            #tmpDir = mkDir(setDir(dirval, "tmp"))
            for ifile in files:
                srcFile = FileInfo(ifile)
                dstFile = tmpDir.join(srcFile.name)
                print(srcFile)
                print(dstFile)
                1/0
                srcFile.mvFile(dstFile)
                moveFile(ifile, tmpDir)
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Music ID Tagger')
    parser.add_argument('-artist', '-art', "-a", action="store", dest="artist")
    parser.add_argument('-album', '-alb', action="store", dest="album")
    parser.add_argument('-albumartist', '-aa', action="store", dest="albumartist")
    parser.add_argument('-title', action="store", dest="title")
    parser.add_argument('-trackno', '-track', action="store", dest="trackno")
    parser.add_argument('-discno', '-disc', action="store", dest="discno")
    parser.add_argument('-show', '-s', action="store_true", default=False)
    parser.add_argument('-search', action="store_true", default=False)
    parser.add_argument('-file', '-f', action="store", dest="file")
    parser.add_argument('-dir', '-d', action="store", dest="dir")
    parser.add_argument('-debug', action="store_true", default=False)

    args = parser.parse_args()
    main(args)