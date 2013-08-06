# thor
#
# Process files in a given rootFolder to meet specific naming criteria
#
# @created 5/4/2013
# @modified 8/5/2013
# @author Nick Barone

import os, re, string

# folder to process
rootFolder = "/home/dlna01/stream/videos/"

# processFile
# return root folder
#
# @param string path
# @return string root path
def processFileForRootFolder(path):
	root = filter(None, path.replace(rootFolder,"").split("/"))
	return root[0]

# cleanDirs
# Changes directory names based on predetermined rules
def cleanDirs():
	rootDirs = []
	for dirname, dirnames, filenames in os.walk(rootFolder):
		for filename in filenames:
			rootDirs.append(processFileForRootFolder(os.path.join(dirname, filename)))

	# filter files from dirs
	dirContents = list(set(filter(None, rootDirs)))
	for videoDir in list(set(filter(None, rootDirs))):
		if not os.path.isdir(rootFolder + videoDir):
			dirContents.remove(videoDir)

	# clean up dir names
	for vDir in dirContents:
		vDirOld = vDir
		# replace common inaccuracies
		vDir = vDir.replace(".", " ")
		vDir = vDir.replace("_", " ")
		rpMap = [ "'" , "\"" , "/" , "\\" ]
		for rpMapItem in rpMap:
			vDir = vDir.replace(rpMapItem, "")
		#remove anything contained in brackets [ ]
		vDir = re.sub(re.compile('\[.+?\]', re.DOTALL), "", vDir)
		#remove and year stamps and everything after them
		vDir = re.sub(re.compile('\(*\d{4}\)*.+', re.DOTALL), "", vDir)
		#remove common includes
		rpMap = [ "hdtv.+", "x264.+", "1080i.+", "1080p.+", "720p.+", "480p.+", "dvdrip.+" ]
		for rpMapItem in rpMap:
			vDir = re.sub(re.compile(rpMapItem, re.IGNORECASE | re.DOTALL), "", vDir)
		# replace crowded dash
		vDir = vDir.replace("-", " - ")
		# strip extra spaces
		vDir = re.sub(re.compile(' +'), " ", vDir).strip()

		if vDirOld != vDir:
			print "RENAME: " + vDirOld + " >>> " + vDir
			os.rename(rootFolder+vDirOld, rootFolder+vDir)

# cleanFiles
# Changes filenames based on predetermined rules
def cleanFiles():
	rootDirs = []
	for dirname, dirnames, filenames in os.walk(rootFolder):
		for filename in filenames:
			rootDirs.append(os.path.join(dirname, filename))

	# filter dirs from files
	dirContents = list(set(filter(None, rootDirs)))

	# clean up dir names
	for vDir in dirContents:
		vDirOld = vDir

		splitFile = vDir.split("/", -1)
		vFileName = splitFile.pop().split(".")
		vFileDir = "/".join(splitFile) + "/"
		vFileExt = vFileName.pop()
		vFileName = ".".join(vFileName)

		vFileNameOld = vFileName + "." + vFileExt

		if(vFileExt.lower() in [ "jpg", "jpeg", "png", "txt", "srt", "ds_store", "nfo", "yify", "part", "ass", "doc", "docx", "7z" ]):
			# delete file
			os.remove(vDirOld)
			continue
		if "sample" in vFileName.lower():
			# delete file
			os.remove(vDirOld)
			continue

		# replace common inaccuracies
		vFileName = vFileName.replace(".", " ")
		vFileName = vFileName.replace("_", " ")
		rpMap = [ "'" , "\"" , "/" , "\\" ]
		for rpMapItem in rpMap:
			vFileName = vFileName.replace(rpMapItem, "")
		#remove anything contained in brackets [ ]
		vFileName = re.sub(re.compile('\[.+?\]', re.DOTALL), "", vFileName)
		#remove and year stamps and everything after them
		vFileName = re.sub(re.compile('\(*\d{4}\)*.+', re.DOTALL), "", vFileName)
		#remove common includes
		rpMap = [ "hdtv.+", "x264.+", "1080i.+", "1080p.+", "720p.+", "dvdrip.+" ]
		for rpMapItem in rpMap:
			vFileName = re.sub(re.compile(rpMapItem, re.IGNORECASE | re.DOTALL), "", vFileName)
		# replace crowded dash
		if vFileName[0] == '-':
			vFileName = vFileName[1:]
		vFileName = vFileName.replace("-", " - ")
#		if vFileName[0] == '-'
		# strip extra spaces
		vFileName = re.sub(re.compile(' +'), " ", vFileName).strip()
		vFileName = vFileName + "." + vFileExt
		if vFileNameOld != vFileName:
			print "RENAME: " + vFileNameOld + " >>> " + vFileName
			os.rename(vDirOld, vFileDir + vFileName)

# scanDirs
# Scans dirs for one containing file, and moves it up one level
def scanDirs(path):
	if not os.path.isdir(path):
		return

	# run on subfolders
	files = os.listdir(path)
	if len(files):
		for f in files:
			fullpath = os.path.join(path, f)
			if os.path.isdir(fullpath):
				scanDirs(fullpath)

	# if folder empty, delete it
	files = os.listdir(path)
	if len(files) == 1:
		newpath = path.split("/")
		newpath = filter(None, newpath);
		newpath.pop()
		newpath = '/'+'/'.join(newpath)+'/'+files[0]
		os.rename(path+'/'+files[0], newpath)

# cleanEmptyDirs
# Deleted any directories that are empty after cleaning is complete
def cleanEmptyDirs(path):
	if not os.path.isdir(path):
		return

	# remove empty subfolders
	files = os.listdir(path)
	if len(files):
		for f in files:
			fullpath = os.path.join(path, f)
			if os.path.isdir(fullpath):
				cleanEmptyDirs(fullpath)

	# if folder empty, delete it
	files = os.listdir(path)
	if len(files) == 0:
		print "REMOVING:" + path
		os.rmdir(path)

# run
# Run set of commands for proper execution
def run():
	cleanDirs()
	cleanFiles()
	scanDirs(rootFolder)
	cleanEmptyDirs(rootFolder)

# run
run()
