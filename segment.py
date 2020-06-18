import argparse
from os.path import join
from searchUtils import findDirs, findPattern
from fsUtils import moveDir, isDir, isFile, moveFile, mkDir, setDir, setFile
from fileUtils import getBasename
from mp3id import mp3ID
from os import getcwd
from os.path import join
   
def main(args):    
    cwd  = getcwd()
    
    albumSegments = {}
    discSegments  = {}
    
    for ifile in findPattern("./", pattern="."):
        try:
            mid = mp3ID(ifile)
        except:
            continue
        album = mid.getAlbum()
        if album is not None:
            album = album[0]
        if albumSegments.get(album) is None:
            albumSegments[album] = []
        albumSegments[album].append(ifile)
        
        disc  = mid.getDiscNumber()
        if disc is not None:
            disc = disc[0]
        if discSegments.get(disc) is None:
            discSegments[disc] = []
        discSegments[disc].append(ifile)
        
        
    if args.album is True:
        for album, albumFiles in albumSegments.items():
            albumDir = setDir(cwd, album)
            mkDir(albumDir)
            for ifile in albumFiles:
                src = ifile
                dst = setFile(albumDir, getBasename(ifile))
                print("Moving [{0}] to [{1}]".format(src, dst))
                moveFile(src, dst, debug=True)
        
    if args.disc is True:
        for disc, discFiles in discSegments.items():
            discDir = setDir(cwd, "Disc {0}".format(disc))
            mkDir(discDir)
            for ifile in discFiles:
                src = ifile
                dst = setFile(discDir, getBasename(ifile))
                #print("Moving [{0}] to [{1}]".format(src, dst))
                moveFile(src, dst, debug=True)
        
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Music ID Tagger')
    parser.add_argument('-disc', action="store_true", dest="disc", default=False)
    parser.add_argument('-album', action="store_true", dest="album", default=False)
    args = parser.parse_args()
    main(args)