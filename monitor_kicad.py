from six.moves.urllib.request import urlopen
from subprocess import call
import re, ConfigParser, os, inspect

def run_monitor ():
	print ("Checking for latest packagas of Kicad nightly build ...")
	
	script_folder  = os.path.dirname(os.path.abspath (inspect.stack()[0][1]))
	configParser   = ConfigParser.RawConfigParser()
	configFilePath = script_folder + '/config.inf'
	configParser.read (configFilePath)
	
	link                 = configParser.get ('link',      'webfolder_link') 
	current_extras_pkg_d = configParser.get ('extras',    'current')
	current_pkg_r        = configParser.get ('kicad',     'current')
	download_folder      = configParser.get ('directory', 'download_folder')
	download_cmd         = configParser.get ('command',   'download')
	
	response = urlopen (link)
	content  = response.read ()
	current_folder = os.getcwd ()
	
	latest_extras_pkg = re.findall (r'a href="(kicad-extras.*\.dmg)">', content)[-1]
	latest_kicad_pkg  = re.findall (r'a href="(kicad-r.*\.dmg)">', content)[-1]
	
	latest_extras_pkg_d = re.findall (r'kicad-extras\.(.*)-.*\.dmg', latest_extras_pkg)[0]
	latest_pkg_r        = re.findall (r'kicad-r(.*)\..*\.dmg', latest_kicad_pkg)[0]
	
	have_newer = 0
	
	if (latest_pkg_r > current_pkg_r):
		print ("There is newer revision nightly built of Kicad - current %s - latest %s" %( current_pkg_r, latest_pkg_r))
		have_newer = 1
		print ("Downloading latest Kicad. Old file in download folder will be replaced ...")
		os.chdir (download_folder)
		if (os.path.isfile (download_folder + "/" + latest_kicad_pkg)):
			call ("rm -f " + latest_kicad_pkg, shell = True) 
		call (download_cmd + " " + link + latest_kicad_pkg, shell = True)  
		# Check if downloaded file exists
		if (os.path.isfile (download_folder + "/" + latest_kicad_pkg)):
			configParser.set ('kicad', 'current', latest_pkg_r)
			print ("Done.")
		else:
			print ("Error.")
	
	if (latest_extras_pkg_d > current_extras_pkg_d):
		print ("There is newer revision nightly built of extras package- current %s - latest %s" %(current_extras_pkg_d, latest_extras_pkg_d))
		have_newer = 1
		print ("Downloading latest extras package. Old file in download folder will be replaced ...")
		os.chdir (download_folder)
		if (os.path.isfile (download_folder + "/" + latest_extras_pkg)):
			call ("rm -f " + latest_extras_pkg, shell = True) 
		call (download_cmd + " " + link + latest_extras_pkg, shell = True)  
		# Check if downloaded file exists
		if (os.path.isfile (download_folder + "/" + latest_extras_pkg)):
			configParser.set ('extras', 'current', latest_extras_pkg_d)
			print ("Done.")
		else:
			print ("Error.")
	
	with open (configFilePath, 'wb') as configfile:
		configParser.write (configfile)
	os.chdir (current_folder)

	if (have_newer == 1):
		print ("All latest packages have been downloaded to %s. Please install manually." %(download_folder))
	else:
		print ("You're using latest packages.")

if __name__ == "__main__":
	run_monitor ()
