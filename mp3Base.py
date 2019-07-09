from mutagen.easyid3 import EasyID3, ID3
from mutagen.id3 import TXXX
from fsUtils import getSize


###############################################################################
# EasyID3 Tags
###############################################################################
def getEasyID3(mp3, debug = False):
    try:
        audio = EasyID3(mp3)
    except:
        if debug: print "  Could not get EasyID3 tags for mp3:",mp3
        audio = None
    return audio



###############################################################################
# ID3 Tags
###############################################################################
def getID3TagMap():
    tagMap = {'TALB': 'Album',
              'TBPM': 'BPM',
              'TCMP': 'Compilation',
              'TCOM': 'Composer',
              'TCOP': 'Copyright',
              'TENC': 'EncodedBy',
              'TEXT': 'Lyricist',
              'TIT2': 'Title',
              'TIT3': 'Version',
              'TLEN': 'Length',
              'TMED': 'Media',
              'TMOO': 'Mood',
              'TOLY': 'Author',
              'TPE1': 'Artist',
              'TPE2': 'Performer',
              'TPE3': 'Conductor',
              'TPE4': 'Arranger',
              'TPOS': 'DiscNumber',
              'TPUB': 'Organization',
              'TRCK': 'TrackNumber',
              'TSO2': 'AlbumArtist',
              'TSOA': 'Album',
              'TSOC': 'Composer',
              'TSOP': 'Artist',
              'TSOT': 'Title',
              'TSRC': 'Isrc',
              'TSST': 'DiscSubtitle'}
    
    id3Map = {v: k for k,v in tagMap.iteritems()}
    return id3Map
    

def getID3(mp3, debug = False):
    try:
        audio = ID3(mp3)
    except:
        if debug: print "  Could not get ID3 tags for mp3:",mp3
        audio = None
    return audio
        


###############################################################################
# Set Tag
###############################################################################
def setEasyTag(mp3, tag, tagVal, debug = False):
    if isinstance(mp3, EasyID3):
        audio = mp3
    else:
        audio = getEasyID3(mp3)

    if audio == None:
        if debug: raise ValueError("  Could not get tags to set tags for",mp3)
        return None
    
    
    if audio.get(tag) or True:
        try:
            audio[tag] = tagVal
            audio.save()
            if debug: print "  Set",tag,"to",tagVal,"for",mp3
            return True
        except:
            raise ValueError("  Could not set tag",tag,"to",tagVal,"for",mp3)
    else:
        if debug:
            print "Tag",tag,"does not exist!"
    
    return False
        


###############################################################################
# Get Tag
###############################################################################
def getEasyTag(mp3, tag, allowMissing = False, debug = False):
    if isinstance(mp3, EasyID3):
        audio = mp3
    else:
        audio = getEasyID3(mp3)

    if audio == None:
        if debug: print "  Could not get tags for",mp3
        return None
    
    if audio.get(tag) == None:
        if allowMissing:
            return False
        else:
            raise ValueError("  Could not get tag",tag,"for",mp3)
    else:
        try:
            tagVal = audio[tag][0]
            return tagVal
        except:
            if allowMissing:
                return False
            else:
                raise ValueError("  Tag exists, but could not access it correctly!")
    
    return False
        


###############################################################################
# Set Tag
###############################################################################
def setTag(mp3, tag, tagVal, debug = False):
    if isinstance(mp3, ID3):
        audio = mp3
    else:
        audio = getID3(mp3)

    if audio == None:
        if debug: raise ValueError("  Could not get tags to set tags for",mp3)
        return None
    

    if audio.getall(tag):
        try:
            audio.getall(tag)[0].text[0] = tagVal
            audio.save()
            if debug: print "  Set",tag,"to",tagVal,"for",mp3
            return True
        except:
            raise ValueError("  Could not set existing tag",tag,"to",tagVal,"for",mp3)
    else:
        if tag == "TXXX":
            try:
                audio.add(TXXX(encoding=3, text=tagVal))
                audio.save()
                return True
            except:
                raise ValueError("  Could not set new tag",tag,"to",tagVal,"for",mp3)
        else:
            print "Tag",tag,"does not exist."

    return False
        


###############################################################################
# Set Tag
###############################################################################
def getTag(mp3, tag, allowMissing = False, debug = False):
    if isinstance(mp3, ID3):
        audio = mp3
    else:
        audio = getID3(mp3)

    if audio == None:
        if debug: raise ValueError("  Could not get tags to set tags for",mp3)
        return None
    

    if audio.getall(tag):
        try:
            tagVal = audio.getall(tag)[0].text[0]
            return tagVal
        except:
            raise ValueError("  Could not get tag",tag,"to",tagVal,"for",mp3)
    else:
        if allowMissing:
            return False
        else:
            raise ValueError("  Tag exists, but could not access it correctly!")

    return False

        


###############################################################################
# Version
###############################################################################
def getVersion(mp3, allowMissing = True, debug = False):
    if not isinstance(mp3, EasyID3):
        audio = getEasyID3(mp3)
    else:
        audio = mp3
        
    try:
        version = audio.version
    except:
        version = False
        
    return version

        


###############################################################################
# Compilation
###############################################################################
def setCompilation(mp3, compVal, debug = False):
    retval = setEasyTag(mp3, 'compilation', compVal, debug)
    return retval

def getCompilation(audio, allowMissing = True, debug = False):
    retval = getEasyTag(audio, 'compilation', allowMissing, debug)
    return retval



###############################################################################
# Artist
###############################################################################
def setArtist(mp3, artistVal, debug = False):
    retval = setEasyTag(mp3, 'artist', artistVal, debug)
    return retval


def getArtist(audio, allowMissing = False, debug = False):
    retval = getEasyTag(audio, 'artist', allowMissing, debug)
    return retval



###############################################################################
# Artist
###############################################################################
def setAlbumArtist(mp3, artistVal, debug = False):
    retval = setEasyTag(mp3, 'albumartist', artistVal, debug)
    return retval


def getAlbumArtist(audio, allowMissing = False, debug = False):
    retval = getEasyTag(audio, 'albumartist', allowMissing, debug)
    return retval



###############################################################################
# Album
###############################################################################
def setAlbum(mp3, albumVal, debug = False):
    retval = setEasyTag(mp3, 'album', albumVal, debug)
    return retval


def getAlbum(audio, allowMissing = False, debug = False):
    retval = getEasyTag(audio, 'album', allowMissing, debug)
    return retval



###############################################################################
# Title
###############################################################################
def setTitle(mp3, albumVal, debug = False):
    retval = setEasyTag(mp3, 'title', albumVal, debug)
    return retval


def getTitle(audio, allowMissing = False, debug = False):
    retval = getEasyTag(audio, 'title', allowMissing, debug)
    return retval



###############################################################################
# Disc Number
###############################################################################
def setDiscNo(mp3, DiscNoVal, debug = False):
    retval = setEasyTag(mp3, 'discnumber', DiscNoVal, debug)
    return retval

def setDiscNumber(mp3, DiscNoVal, debug = False):
    return setDiscNo(mp3, DiscNoVal, debug)


def getDiscNo(audio, allowMissing = False, debug = False):
    retval = getEasyTag(audio, 'discnumber', allowMissing, debug)
    return retval

def getDiscNumber(audio, debug = False):
    return getDiscNo(audio, debug)



###############################################################################
# Track Number
###############################################################################
def setTrackNo(mp3, trackNoVal, debug = False):
    retval = setEasyTag(mp3, 'tracknumber', trackNoVal, debug)
    return retval

def setTrackNumber(mp3, trackNoVal, debug = False):
    return setTrackNo(mp3, trackNoVal, debug)


def getTrackNo(audio, allowMissing = False, debug = False):
    retval = getEasyTag(audio, 'tracknumber', allowMissing, debug)
    return retval

def getTrackNumber(audio, debug = False):
    return getTrackNo(audio, debug)



###############################################################################
# Language
###############################################################################
def setCountry(mp3, country, debug = False):
    retval = setTag(mp3, 'TXXX', country, debug)
    return retval

def getCountry(mp3, allowMissing = False, debug = False):
    return getTag(mp3, "TXXX", allowMissing, debug)
    
    
    
###############################################################################
# General Info
###############################################################################
def getInfo(mp3, easyID3 = True, allowMissing = True, debug = False):
    try:
        size = getsize(mp3)
    except:
        size = False

    
    if easyID3:
        audio    = getEasyID3(mp3)
        audioID3 = getID3(mp3)
        if audio == None:
            retval = {"Version": None, "Artist": None, "AlbumArtist": None, "Album": None, "Title": None, "TrackNo": None, "DiscNo": None, "Compilation": None, "Other": None, "Size": size, "Country": None}
            return retval
    
        version     = getVersion(audio, allowMissing, debug)
        artist      = getArtist(audio, allowMissing, debug)
        albumartist = getAlbumArtist(audio, allowMissing, debug)
        album       = getAlbum(audio, allowMissing, debug)
        title       = getTitle(audio, allowMissing, debug)
        discno      = getDiscNo(audio, allowMissing, debug)
        trackno     = getTrackNo(audio, allowMissing, debug)
        compilation = getCompilation(audio, allowMissing, debug)        
        country     = getCountry(audioID3, allowMissing, debug)
        try:
            other = {}
            audioKeys = audio.keys()
            audioVals = audio.values()
            for i in range(len(audioKeys)):
                key = audioKeys[i]
                if key in ["albumartist", "tracknumber", "album", "title", "artist", "compilation"]:
                    continue
                other[key] = audioVals[i]
        except:
            other   = None
        
    retval = {"Version": version, "Artist": artist, "AlbumArtist": albumartist, "Album": album, "Title": title, "DiscNo": discno, "TrackNo": trackno, "Compilation": compilation, "Other": other, "Size": size, "Country": country}
    return retval