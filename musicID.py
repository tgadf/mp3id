from mutagen.easyid3 import EasyID3, ID3
from mutagen.mp4 import MP4
from mutagen.id3 import TXXX
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from fsUtils import isFile
from fileUtils import getExt, getSize

##############################################################################################################################
# MusicID
##############################################################################################################################
class tags:
    def __init__(self, path, artist, albumartist, album, title, track, disc, compilation):
        self.path        = path
        self.artist      = artist
        self.albumartist = albumartist
        self.album       = album
        self.title       = title
        self.track       = track
        self.disc        = disc
        self.compilation = compilation

    def get(self):
        return self.__dict__


##############################################################################################################################
# MusicID
##############################################################################################################################
class MusicID():
    def __init__(self, file=None, debug=False, allowMissing=True, test=False):
        self.mp3Exts  = [".mp3", ".Mp3", ".MP3"]
        self.isMP3    = None
        self.flacExts = [".flac", ".Flac", ".FLAC"]
        self.isFLAC   = None
        self.m4aExts  = [".m4a", ".M4a", ".M4A"]
        self.isM4A    = None
        self.asfExts  = [".wma", ".WMA"]
        self.isASF    = None
        self.oggExts  = [".ogg", ".OGG"]
        self.isOGG    = None
        self.aiffExts = [".aiff", ".AIFF"]
        self.isAIFF   = None
        self.wavExts  = [".wav", ".WAV", ".wv"]
        self.isWAV    = None


        self.skips    = [".jpg", ".JPG", ".jpeg", ".txt", ".log", ".DS_Store", ".bmp", ".m3u", ".png", ".ISO", ".nfo", ".pdf", ".plc", ".pls",
        ".sfv", ".accurip", ".cue", ".mp4", ".mkv", ".gif", ".mov", ".exe", ".m4v", ".db", ".BUP", ".IFO", ".VOB", ".epub", ".webm", ".url", ".m3u8", ".wmv", ".avi",
        '.LOG', '.info', ".torrent", '.ini', '.ico', ".sh", ".avi", ".vob", ".doc", ".m2v", ".mpg", ".html", ".mht", ".rtf", ".jpe", ".docx", ".ffp", ".dff", ".opus",
        ".md5", ".CUE", ".tif", ".PNG", ".ipynb", ".py", ".gz", ".xml", ".to", ".MP2", ".tiff", ".TIFF", ".itlp", ".INF", ".DIR", ".MPG", ".qdat", ".hlp", ".x32", ".lic", ".dll", ".JPEG", ".JPE", ".NFO", ".Jpg", ".rar", ".ape", ".SFV", ".TXT", ".pcx", ".MD5", ".TIF"]
        self.skips   += [".mp2", ".m4p"]
        self.skip     = False

        self.file   = file
        self.debug  = debug
        self.allowMissing = allowMissing
        self.test   = test
        self.format = None

        if file is not None:
            if isFile(self.file):
                self.setMusic(self.file)

        self.mp3tags  = {'TALB': 'Album',
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


        ###############################################################################
        # Key Map
        ###############################################################################
        self.inputMap = {}
        self.inputMap["Artist"]      = "artist"
        self.inputMap["Album"]       = "album"
        self.inputMap["AlbumArtist"] = "albumartist"
        self.inputMap["DiscNo"]      = "discnumber"
        self.inputMap["Disc"]        = "discnumber"
        self.inputMap["TrackNo"]     = "tracknumber"
        self.inputMap["Track"]       = "tracknumber"
        self.inputMap["Title"]       = "title"

        # OGG
        self.inputOGGMap = {}
        self.inputOGGMap["Artist"]      = "artist"
        self.inputOGGMap["Album"]       = "album"
        self.inputOGGMap["AlbumArtist"] = "artist"
        self.inputOGGMap["DiscNo"]      = None
        self.inputOGGMap["Disc"]        = None
        self.inputOGGMap["TrackNo"]     = "tracknumber"
        self.inputOGGMap["Track"]       = "tracknumber"
        self.inputOGGMap["Title"]       = "title"

        # M4A
        self.inputM4AMap = {}
        self.inputM4AMap["Artist"]      = "©ART"
        self.inputM4AMap["Album"]       = "©alb"
        self.inputM4AMap["AlbumArtist"] = "aART"
        self.inputM4AMap["DiscNumber"]  = "disk"
        self.inputM4AMap["DiscNo"]      = "disk"
        self.inputM4AMap["Disc"]        = "disk"
        self.inputM4AMap["TrackNo"]     = "trkn"
        self.inputM4AMap["TrackNumber"] = "trkn"
        self.inputM4AMap["Track"]       = "trkn"
        self.inputM4AMap["Title"]       = "©nam"
        
        # ASF
        self.inputASFMap = {}
        self.inputASFMap["Artist"]      = "WM/AlbumArtist"
        self.inputASFMap["Album"]       = "WM/AlbumTitle"
        self.inputASFMap["AlbumArtist"] = "WM/AlbumArtist"
        self.inputASFMap["DiscNumber"]  = None
        self.inputASFMap["DiscNo"]      = None
        self.inputASFMap["Disc"]        = None
        self.inputASFMap["TrackNo"]     = "WM/TrackNumber"
        self.inputASFMap["TrackNumber"] = "WM/TrackNumber"
        self.inputASFMap["Track"]       = "WM/TrackNumber"
        self.inputASFMap["Title"]       = "Title"



        self.keyMap = {}
        self.keyMap["artist"]       = {True: "artist", False: "TPE1"}
        self.keyMap["album"]        = {True: "album", False: "TALB"}
        self.keyMap["albumartist"]  = {True: "albumartist", False: "TPE2"}
        self.keyMap["title"]        = {True: "title", False: "TIT2"}
        self.keyMap["tracknumber"]  = {True: "tracknumber", False: "TRCK"}
        self.keyMap["discnumber"]   = {True: "discnumber", False: None}
        self.keyMap["date"]         = {True: "date", False: "TDRC"}
        self.keyMap["genre"]        = {True: "genre", False: "TCON"}
        self.keyMap["length"]       = {True: "length", False: "TLEN"}
        self.keyMap["compilation"]  = {True: "compilation", False: "TCMP"}



        self.id3Map = {v: k for k,v in self.mp3tags.items()}

        self.tagsEasyID3 = None
        self.tagsID3     = None
        self.tagsFlac    = None
        self.tagsM4A     = None
        self.tagsOGG     = None
        self.tagsAIFF    = None


    def getTags(self):
        self.setTags()
        return self.tags

    def setTags(self):
        self.tags = tags(path=self.file,
                            artist=self.getArtist(),
                            albumartist=self.getAlbumArtist(),
                            album=self.getAlbum(),
                            title=self.getTitle(),
                            track=self.getTrackNumber(),
                            disc=self.getDiscNumber(),
                            compilation=self.getCompilation())

    def isValid(self):
        if self.isMP3 or self.isFLAC:
            return True
        return False

    def setMusic(self, file):
        if isFile(file):
            self.file = file
            if getExt(file) in self.flacExts:
                self.isFLAC = True
                if self.debug is True:
                    print("  File is FLAC")
            elif getExt(file) in self.mp3Exts:
                self.isMP3 = True
                if self.debug:
                    print("  File is MP3")
            elif getExt(file) in self.m4aExts:
                self.isM4A = True
                if self.debug:
                    print("  File is M4A")
            elif getExt(file) in self.asfExts:
                self.isASF = True
                if self.debug:
                    print("  File is ASF (WMA)")
            elif getExt(file) in self.oggExts:
                self.isOGG = True
                if self.debug:
                    print("  File is OGG")
            elif getExt(file) in self.aiffExts:
                self.isAIFF = True
                if self.debug:
                    print("  File is AIFF")
            elif getExt(file) in self.wavExts:
                self.isWAV = True
                if self.debug:
                    print("  File is WAV")
            elif getExt(file) in self.skips:
                self.skip = True
            elif ".DS_Store" in file:
                self.skip = True
            else:
                raise ValueError("Could not determine format for [{0}] with extention [{1}]".format(file, getExt(file)))

            if self.isMP3 is True:
                #self.findID3Tags()
                self.findEasyTags()
            if self.isFLAC is True:
                self.findFlacTags()
            if self.isM4A is True:
                self.findM4ATags()
            if self.isASF is True:
                self.findASFTags()
            if self.isOGG is True:
                self.findOGGTags()
            if self.isAIFF is True:
                self.findAIFFTags()
            if self.isWAV is True:
                self.findWAVTags()
        else:
            raise ValueError("Could not access {0}".format(ifile))




    ##############################################################################################################
    #
    # OGG Tags
    #
    ##############################################################################################################

    ########################## Finder ##########################
    def findOGGTags(self):
        try:
            audio = OggVorbis(self.file)
        except:
            if self.debug:
                print("Could not get OGG tags for {0}".format(self.file))
            audio = None
        self.tagsOGG = audio


    ########################## Shower ##########################
    def showOGGTags(self):
        if self.tagsOGG is None:
            self.findOGGTags()
        return list(self.tagsOGG.keys())


    ########################## Getter ##########################
    def getOGGTags(self):
        if self.tagsOGG is None:
            self.findOGGTags()
        return self.tagsOGG


    ########################## Setter ##########################
    def setOGGTag(self, tag, tagVal):
        if self.tagsOGG is None:
            self.findOGGTags()

        if self.tagsOGG is None:
            if self.debug:
                print("Could not set OGG tag because tags are None")
            return

        try:
            self.tagsOGG[tag] = tagVal
        except:
            raise ValueError("Could not set tag [{0}] to [{1}] for [{2}]".format(tag, tagVal, self.file))

        if self.test is True:
            print("Not saving because test flag is True")
        else:
            try:
                self.tagsOGG.save()
            except:
                raise ValueError("Could not save tags to {0}".format(self.file))


    ########################## Getter ##########################
    def getOGGTag(self, tag):
        if self.tagsOGG is None:
            self.findOGGTags()

        if self.tagsOGG is None:
            if self.debug:
                print("Could not get OGG tag because tags are None")
            return

        tagValRes = self.tagsOGG.get(tag)

        self.debug = True
        tagVal    = None

        if tagValRes is None:
            if self.allowMissing is True:
                tagVal = None
            else:
                raise ValueError("Could not get OGG tag [{0}] for [{1}]".format(tag, self.file))

        if tagValRes is not None:
            try:
                tagVal = tagValRes
            except:
                if self.allowMissing:
                    tagVal = None
                else:
                    raise ValueError("Could not get OGG tag [{0}] for [{1}] even though it exists".format(tag, self.file))

        return tagVal





    ##############################################################################################################
    #
    # M4A Tags
    #
    ##############################################################################################################

    ########################## Finder ##########################
    def findM4ATags(self):
        try:
            audio = MP4(self.file)
        except:
            if self.debug:
                print("Could not get M4A tags for {0}".format(self.file))
            audio = None
        self.tagsM4A = audio


    ########################## Shower ##########################
    def showM4ATags(self):
        if self.tagsM4A is None:
            self.findM4ATags()
        return list(self.tagsM4A.keys())


    ########################## Getter ##########################
    def getM4ATags(self):
        if self.tagsM4A is None:
            self.findM4ATags()
        return self.tagsM4A


    ########################## Setter ##########################
    def setM4ATag(self, tag, tagVal):
        if self.tagsM4A is None:
            self.findM4ATags()

        if self.tagsM4A is None:
            if self.debug:
                print("Could not set M4A tag because tags are None")
            return

        try:
            self.tagsM4A[tag] = tagVal
        except:
            raise ValueError("Could not set tag [{0}] to [{1}] for [{2}]".format(tag, tagVal, self.file))

        if self.test is True:
            print("Not saving because test flag is True")
        else:
            try:
                self.tagsM4A.save()
            except:
                raise ValueError("Could not save tags to {0}".format(self.file))


    ########################## Getter ##########################
    def getM4ATag(self, tag):
        if self.tagsM4A is None:
            self.findM4ATags()

        if self.tagsM4A is None:
            if self.debug:
                print("Could not get M4A tag because tags are None")
            return

        tagValRes = self.tagsM4A.get(tag)

        self.debug = True
        tagVal    = None

        if tagValRes is None:
            if self.allowMissing is True:
                tagVal = None
            else:
                raise ValueError("Could not get M4A tag [{0}] for [{1}]".format(tag, self.file))

        if tagValRes is not None:
            try:
                tagVal = tagValRes
            except:
                if self.allowMissing:
                    tagVal = None
                else:
                    raise ValueError("Could not get M4A tag [{0}] for [{1}] even though it exists".format(tag, self.file))

        return tagVal






    ##############################################################################################################
    #
    # ASF Tags
    #
    ##############################################################################################################

    ########################## Finder ##########################
    def findASFTags(self):
        try:
            audio = ASF(self.file)
        except:
            if self.debug:
                print("Could not get ASF tags for {0}".format(self.file))
            audio = None
        self.tagsASF = audio


    ########################## Shower ##########################
    def showASFTags(self):
        if self.tagsASF is None:
            self.findASFTags()
        return list(self.tagsASF.keys())


    ########################## Getter ##########################
    def getASFTags(self):
        if self.tagsASF is None:
            self.findASFTags()
        return self.tagsASF


    ########################## Setter ##########################
    def setASFTag(self, tag, tagVal):
        if self.tagsASF is None:
            self.findASFTags()

        if self.tagsASF is None:
            if self.debug:
                print("Could not set ASF tag because tags are None")
            return

        try:
            self.tagsASF[tag] = tagVal
        except:
            raise ValueError("Could not set tag [{0}] to [{1}] for [{2}]".format(tag, tagVal, self.file))

        if self.test is True:
            print("Not saving because test flag is True")
        else:
            try:
                self.tagsASF.save()
            except:
                raise ValueError("Could not save tags to {0}".format(self.file))


    ########################## Getter ##########################
    def getASFTag(self, tag):
        if self.tagsASF is None:
            self.findASFTags()

        if self.tagsASF is None:
            if self.debug:
                print("Could not get ASF tag because tags are None")
            return

        tagValRes = self.tagsASF.get(tag)

        self.debug = True
        tagVal    = None

        if tagValRes is None:
            if self.allowMissing is True:
                tagVal = None
            else:
                raise ValueError("Could not get ASF tag [{0}] for [{1}]".format(tag, self.file))

        if tagValRes is not None:
            try:
                tagVal = tagValRes
            except:
                if self.allowMissing:
                    tagVal = None
                else:
                    raise ValueError("Could not get ASF tag [{0}] for [{1}] even though it exists".format(tag, self.file))

        return tagVal




    ##############################################################################################################
    #
    # Flac Tags
    #
    ##############################################################################################################

    ########################## Finder ##########################
    def findFlacTags(self):
        try:
            audio = FLAC(self.file)
        except:
            if self.debug:
                print("Could not get Flac tags for {0}".format(self.file))
            audio = None
        self.tagsFlac = audio


    ########################## Shower ##########################
    def showFlacTags(self):
        if self.tagsFlac is None:
            self.findFlacTags()
        return list(self.tagsFlac.keys())


    ########################## Getter ##########################
    def getFlacTags(self):
        if self.tagsFlac is None:
            self.findFlacTags()
        return self.tagsFlac


    ########################## Setter ##########################
    def setFlacTag(self, tag, tagVal):
        if self.tagsFlac is None:
            self.findFlacTags()

        if self.tagsFlac is None:
            if self.debug:
                print("Could not set Flac tag because tags are None")
            return

        try:
            self.tagsFlac[tag] = tagVal
        except:
            raise ValueError("Could not set tag [{0}] to [{1}] for [{2}]".format(tag, tagVal, self.file))

        if self.test is True:
            print("Not saving because test flag is True")
        else:
            try:
                self.tagsFlac.save()
            except:
                raise ValueError("Could not save tags to {0}".format(self.file))


    ########################## Getter ##########################
    def getFlacTag(self, tag):
        if self.tagsFlac is None:
            self.findFlacTags()

        if self.tagsFlac is None:
            if self.debug:
                print("Could not get Flac tag because tags are None")
            return

        tagValRes = self.tagsFlac.get(tag)

        self.debug = True
        tagVal    = None

        if tagValRes is None:
            if self.allowMissing is True:
                tagVal = None
            else:
                raise ValueError("Could not get Flac tag [{0}] for [{1}]".format(tag, self.file))

        if tagValRes is not None:
            try:
                tagVal = tagValRes
            except:
                if self.allowMissing:
                    tagVal = None
                else:
                    raise ValueError("Could not get Flac tag [{0}] for [{1}] even though it exists".format(tag, self.file))

        return tagVal




    ##############################################################################################################
    #
    # AIFF Tags
    #
    ##############################################################################################################

    ########################## Finder ##########################
    def findAIFFTags(self):
        try:
            audio = AIFF(self.file)
        except:
            if self.debug:
                print("Could not get AIFF tags for {0}".format(self.file))
            audio = None
        self.tagsAIFF = audio


    ########################## Shower ##########################
    def showAIFFTags(self):
        if self.tagsAIFF is None:
            self.findAIFFTags()
        return list(self.tagsAIFF.keys())


    ########################## Getter ##########################
    def getAIFFTags(self):
        if self.tagsAIFF is None:
            self.findAIFFTags()
        return self.tagsAIFF


    ########################## Setter ##########################
    def setAIFFTag(self, tag, tagVal):
        if self.tagsAIFF is None:
            self.findAIFFTags()

        if self.tagsAIFF is None:
            if self.debug:
                print("Could not set AIFF tag because tags are None")
            return

        try:
            self.tagsAIFF[tag] = tagVal
        except:
            raise ValueError("Could not set tag [{0}] to [{1}] for [{2}]".format(tag, tagVal, self.file))

        if self.test is True:
            print("Not saving because test flag is True")
        else:
            try:
                self.tagsAIFF.save()
            except:
                raise ValueError("Could not save tags to {0}".format(self.file))


    ########################## Getter ##########################
    def getAIFFTag(self, tag):
        if self.tagsAIFF is None:
            self.findAIFFTags()

        if self.tagsFlac is None:
            if self.debug:
                print("Could not get AIFF tag because tags are None")
            return

        tagValRes = self.tagsAIFF.get(tag)

        self.debug = True
        tagVal    = None

        if tagValRes is None:
            if self.allowMissing is True:
                tagVal = None
            else:
                raise ValueError("Could not get AIFF tag [{0}] for [{1}]".format(tag, self.file))

        if tagValRes is not None:
            try:
                tagVal = tagValRes
            except:
                if self.allowMissing:
                    tagVal = None
                else:
                    raise ValueError("Could not get AIFF tag [{0}] for [{1}] even though it exists".format(tag, self.file))

        return tagVal




    ##############################################################################################################
    #
    # WAV Tags
    #
    ##############################################################################################################

    ########################## Finder ##########################
    def findWAVTags(self):
        try:
            audio = WAVE(self.file)
        except:
            if self.debug:
                print("Could not get WAV tags for {0}".format(self.file))
            audio = None
        self.tagsWAV = audio


    ########################## Shower ##########################
    def showWAVTags(self):
        if self.tagsWAV is None:
            self.findWAVTags()
        return list(self.tagsWAV.keys())


    ########################## Getter ##########################
    def getWAVTags(self):
        if self.tagsWAV is None:
            self.findWAVTags()
        return self.tagsWAV


    ########################## Setter ##########################
    def setWAVTag(self, tag, tagVal):
        if self.tagsWAV is None:
            self.findWAVTags()

        if self.tagsWAV is None:
            if self.debug:
                print("Could not set WAV tag because tags are None")
            return

        try:
            self.tagsWAV[tag] = tagVal
        except:
            raise ValueError("Could not set tag [{0}] to [{1}] for [{2}]".format(tag, tagVal, self.file))

        if self.test is True:
            print("Not saving because test flag is True")
        else:
            try:
                self.tagsWAV.save()
            except:
                raise ValueError("Could not save tags to {0}".format(self.file))


    ########################## Getter ##########################
    def getWAVTag(self, tag):
        if self.tagsWAV is None:
            self.findWAVTags()

        if self.tagsFlac is None:
            if self.debug:
                print("Could not get WAV tag because tags are None")
            return

        tagValRes = self.tagsWAV.get(tag)

        self.debug = True
        tagVal    = None

        if tagValRes is None:
            if self.allowMissing is True:
                tagVal = None
            else:
                raise ValueError("Could not get WAV tag [{0}] for [{1}]".format(tag, self.file))

        if tagValRes is not None:
            try:
                tagVal = tagValRes
            except:
                if self.allowMissing:
                    tagVal = None
                else:
                    raise ValueError("Could not get WAV tag [{0}] for [{1}] even though it exists".format(tag, self.file))

        return tagVal

    

    ##############################################################################################################
    #
    # EasyID3 Tags
    #
    ##############################################################################################################

    ########################## Finder ##########################
    def findEasyTags(self):
        try:
            audio = EasyID3(self.file)
        except:
            if self.debug:
                print("Could not get EasyID3 tags for {0}".format(self.file))
            audio = None
        self.tagsEasyID3 = audio


    ########################## Shower ##########################
    def showEasyTags(self):
        if self.tagsEasyID3 is None:
            self.findEasyTags()
        return list(self.tagsEasyID3.keys())


    ########################## Getter ##########################
    def getEasyTags(self):
        if self.tagsEasyID3 is None:
            self.findEasyTags()
        return self.tagsEasyID3


    ########################## Setter ##########################
    def setEasyTag(self, tag, tagVal):
        if self.tagsEasyID3 is None:
            self.findEasyTags()

        if self.tagsEasyID3 is None:
            if self.debug:
                print("Could not set EasyID3 tag because tags are None")
            return

        try:
            self.tagsEasyID3[tag] = tagVal
        except:
            raise ValueError("Could not set tag [{0}] to [{1}] for [{2}]".format(tag, tagVal, self.file))

        if self.test is True:
            print("Not saving because test flag is True")
        else:
            try:
                self.tagsEasyID3.save()
            except:
                raise ValueError("Could not save tags to {0}".format(self.file))


    ########################## Getter ##########################
    def getEasyTag(self, tag):
        if self.tagsEasyID3 is None:
            self.findEasyTags()

        if self.tagsEasyID3 is None:
            if self.debug:
                print("Could not get EasyID3 tag because tags are None")
            return

        tagValRes = self.tagsEasyID3.get(tag)
        tagVal    = None

        if tagValRes is None:
            if self.allowMissing is True:
                tagVal = None
            else:
                raise ValueError("Could not get EasyID3 tag [{0}] for [{1}]".format(tag, self.file))

        if tagValRes is not None:
            try:
                tagVal = tagValRes
            except:
                if self.allowMissing:
                    tagVal = None
                else:
                    raise ValueError("Could not get EasyID3 tag [{0}] for [{1}] even though it exists".format(tag, self.file))

        return tagVal



    ##############################################################################################################
    #
    # ID3 Tags
    #
    ##############################################################################################################

    ########################## Finder ##########################
    def findID3Tags(self):
        try:
            audio = ID3(self.file)
        except:
            if self.debug:
                print("Could not get ID3 tags for {0}".format(self.file))
            audio = None
        self.tagsID3 = audio


    ########################## Shower ##########################
    def showID3Tags(self):
        if self.tagsID3 is None:
            self.findID3Tags()
        return list(self.tagsID3.keys())


    ########################## Getter ##########################
    def getID3Tags(self):
        if self.tagsID3 is None:
            self.findID3Tags()
        return self.tagsID3


    ########################## Setter ##########################
    def setID3Tag(self, tag, tagVal):
        if self.tagsID3 is None:
            self.findID3Tags()

        if self.tagsID3 is None:
            if self.debug:
                print("Could not set ID3 tag because tags are None")
            return


        if tag == "TXXX":
            try:
                self.tagsID3.add(TXXX(encoding=3, text=tagVal))
            except:
                raise ValueError("Could not set ID3 tag [{0}] to [{1}] for [{2}]".format(tag, tagVal, self.file))
        else:
            try:
                self.tagsID3.getall(tag)[0].text[0] = tagVal
            except:
                raise ValueError("Could not set ID3 tag [{0}] to [{1}] for [{2}]".format(tag, tagVal, self.file))

        if self.test is True:
            print("Not saving because test flag is True")
        else:
            try:
                self.tagsID3.save()
            except:
                raise ValueError("Could not save ID3 tags to {0}".format(self.file))


    ########################## Getter ##########################
    def getID3Tag(self, tag):
        if self.tagsID3 is None:
            self.findID3Tags()

        if self.tagsID3 is None:
            if self.debug:
                print("Could not get ID3 tag because tags are None")
            return

        tagValRes = self.tagsID3.getall(tag)
        tagVal    = None

        if tagValRes is None:
            if self.allowMissing is True:
                tagVal = None
            else:
                raise ValueError("Could not get ID3 tag [{0}] for [{1}]".format(tag, self.file))

        if tagValRes is not None:
            try:
                tagVal = tagValRes[0].text[0]
            except:
                if self.allowMissing:
                    tagVal = None
                else:
                    raise ValueError("Could not get ID3 tag [{0}] for [{1}] even though it exists".format(tag, self.file))

        return tagVal




    ##############################################################################################################
    # Specific Tags
    ##############################################################################################################


    ###############################################################################
    # Version
    ###############################################################################
    def getVersion(self, easy=True):
        if self.isMP3:
            if self.tagsEasyID3 is None:
                self.findEasyTags()
            try:
                version = self.tagsEasyID3.version
            except:
                version = None
        else:
            version = None

        return version



    ###############################################################################
    # Tag
    ###############################################################################
    def setTag(self, key, value, easy=True):
        if self.isMP3:
            if self.inputMap.get(key) is not None:
                key = self.inputMap[key]
            if easy is True:
                return self.setEasyTag(key, value)
            else:
                return self.setID3Tag(key, value)
        elif self.isFLAC:
            if self.inputMap.get(key) is not None:
                key = self.inputMap[key]
            return self.setFlacTag(key, value)
        elif self.isM4A:
            if self.inputM4AMap.get(key) is not None:
                key = self.inputM4AMap[key]
            return self.setM4ATag(key, value)
        elif self.isASF:
            if self.inputASFMap.get(key) is not None:
                key = self.inputASFMap[key]
            return self.setASFTag(key, value)
        elif self.isOGG:
            if self.inputOGGMap.get(key) is not None:
                key = self.inputOGGMap[key]
            return self.setOGGTag(key, value)
        elif self.isAIFF:
            if self.inputMap.get(key) is not None:
                key = self.inputMap[key]
            return self.setAIFFTag(key, value)
        elif self.isWAV:
            if self.inputMap.get(key) is not None:
                key = self.inputMap[key]
            return self.setWAVTag(key, value)
        else:
            raise ValueError("Not sure about format for key: value = {0}:{1}".format(key, value))

    def getTag(self, key, easy=True):
        if self.isMP3:
            if self.inputMap.get(key) is not None:
                key = self.inputMap[key]
            if easy is True:
                return self.getEasyTag(key)
            else:
                return self.getID3Tag(key)
        elif self.isFLAC:
            if self.inputMap.get(key) is not None:
                key = self.inputMap[key]
            val = self.getFlacTag(key)
            return val
        elif self.isM4A:
            if self.inputM4AMap.get(key) is not None:
                key = self.inputM4AMap[key]
            val = self.getM4ATag(key)
            return val
        elif self.isASF:
            if self.inputASFMap.get(key) is not None:
                key = self.inputASFMap[key]
            val = self.getASFTag(key)
            return val
        elif self.isOGG:
            if self.inputOGGMap.get(key) is not None:
                key = self.inputOGGMap[key]
            val = self.getOGGTag(key)
            return val
        elif self.isAIFF:
            if self.inputMap.get(key) is not None:
                key = self.inputMap[key]
            val = self.getAIFFTag(key)
            return val
        elif self.isWAV:
            if self.inputMap.get(key) is not None:
                key = self.inputMap[key]
            val = self.getWAVTag(key)
            return val
        else:
            raise ValueError("Not sure about format for key = {0}".format(key))


    ###############################################################################
    # Artist
    ###############################################################################
    def setArtist(self, artistVal, easy=True):
        key = self.keyMap["artist"][easy]
        return self.setTag(key, artistVal, easy)

    def getArtist(self, easy=True):
        key = self.keyMap["artist"][easy]
        return self.getTag(key, easy)


    ###############################################################################
    # Album
    ###############################################################################
    def setAlbum(self, albumVal):
        key = self.keyMap["album"][easy]
        return self.setTag(key, artistVal, easy)

    def getAlbum(self, easy=True):
        key = self.keyMap["album"][easy]
        return self.getTag(key, easy)


    ###############################################################################
    # AlbumArtist
    ###############################################################################
    def setAlbumArtist(self, albumVal):
        key = self.keyMap["albumartist"][easy]
        return self.setTag(key, artistVal, easy)

    def getAlbumArtist(self, easy=True):
        key = self.keyMap["albumartist"][easy]
        return self.getTag(key, easy)


    ###############################################################################
    # Title
    ###############################################################################
    def setTitle(self, albumVal):
        key = self.keyMap["title"][easy]
        return self.setTag(key, artistVal, easy)

    def getTitle(self, easy=True):
        key = self.keyMap["title"][easy]
        return self.getTag(key, easy)


    ###############################################################################
    # Track Number
    ###############################################################################
    def setTrackNumber(self, albumVal):
        key = self.keyMap["tracknumber"][easy]
        return self.setTag(key, artistVal, easy)

    def getTrackNumber(self, easy=True):
        key = self.keyMap["tracknumber"][easy]
        return self.getTag(key, easy)


    ###############################################################################
    # Disc Number
    ###############################################################################
    def setDiscNumber(self, albumVal):
        key = self.keyMap["discnumber"][easy]
        return self.setTag(key, artistVal, easy)

    def getDiscNumber(self, easy=True):
        key = self.keyMap["discnumber"][easy]
        return self.getTag(key, easy)


    ###############################################################################
    # Date
    ###############################################################################
    def setDate(self, albumVal):
        key = self.keyMap["date"][easy]
        return self.setTag(key, artistVal, easy)

    def getDate(self, easy=True):
        key = self.keyMap["date"][easy]
        return self.getTag(key, easy)


    ###############################################################################
    # Genre
    ###############################################################################
    def setGenre(self, albumVal):
        key = self.keyMap["genre"][easy]
        return self.setTag(key, artistVal, easy)

    def getGenre(self, easy=True):
        key = self.keyMap["genre"][easy]
        return self.getTag(key, easy)


    ###############################################################################
    # Length
    ###############################################################################
    def setLength(self, albumVal):
        key = self.keyMap["length"][easy]
        return self.setTag(key, artistVal, easy)

    def getLength(self, easy=True):
        key = self.keyMap["length"][easy]
        return self.getTag(key, easy)


    ###############################################################################
    # Compilation
    ###############################################################################
    def setCompilation(self, albumVal):
        key = self.keyMap["compilation"][easy]
        return self.setTag(key, artistVal, easy)

    def getCompilation(self, easy=True):
        key = self.keyMap["compilation"][easy]
        return self.getTag(key, easy)


    ###############################################################################
    # General Info
    ###############################################################################
    def getRawInfo(self):
        if self.isMP3 is True:
            self.findEasyTags()
            return self.tagsEasyID3
        elif self.isFLAC is True:
            self.findFlacTags()
            return self.tagsFlac
        elif self.isM4A is True:
            self.findM4ATags()
            return self.tagsM4A
        elif self.isASF is True:
            self.findASFTags()
            return self.tagsASF
        elif self.isOGG is True:
            self.findOGGTags()
            return self.tagsOGG
        elif self.isAIFF is True:
            self.findAIFFTags()
            return self.tagsAIFF
        elif self.isWAV is True:
            self.findWAVTags()
            return self.tagsWAV
        else:
            raise ValueError("Cannot get raw info for this file!")


    def getInfo(self):
        size = getSize(self.file, units="MB")
        if isinstance(size[0], float):
            size = round(size[0],2)

        retval = {"Version": self.getTag("Version"),
                  "Artist":  self.getTag("Artist"),
                  "AlbumArtist": self.getTag("AlbumArtist"),
                  "Album": self.getTag("Album"),
                  "Title": self.getTag("Title"),
                  "TrackNo": self.getTag("TrackNumber"),
                  "DiscNo": self.getTag("DiscNumber"),
                  "Compilation": self.getTag("Compilation"),
                  "Language": None,
                  "Size": size}

        return retval
