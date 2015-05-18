import re
from six.moves.urllib.request import urlopen

link = "http://downloads.kicad-pcb.org/osx/"
response = urlopen(link)
content = response.read()

# Fetch all files here
# TODO: from below statement, revise it to get list of "kicad-extras.*.dmg" and "kicad*.dmg"
re.findall(r'a href=.*>', content)

