#!/bin/python

# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/check-prerequisites.py,v $
# $Revision: 1.10 $

import sys

print "=> checking for Python module 'mxDateTime' ..."
try:
	import mx.DateTime
	print "=> found"
except ImportError:
	print "ERROR: mxDateTime not installed"
	print "ERROR: this is needed to handle dates and times"
	print "ERROR: mxDateTime is available from http://www.egenix.com/files/python/"
	print "INFO : sys.path is set as follows:"
	print "INFO :", "\nINFO : ".join(sys.path)
	sys.exit(-1)

print "=> checking for Python module 'pyPgSQL' ..."
try:
	import pyPgSQL.PgSQL
	print "=> found"
except ImportError:
	print "ERROR: pyPgSQL not installed"
	print "ERROR: this is needed to access PostgreSQL"
	print "ERROR: pyPgSQL is available from http://pypgsql.sourceforge.net"
	print "INFO : sys.path is set as follows:"
	print "INFO :", "\nINFO : ".join(sys.path)
	sys.exit(-1)

print "=> checking for Python module 'wxVersion' ..."
if hasattr(sys, 'frozen'):
	print "INFO : py2exe or similar in use, cannot check wxPython version"
	print "INFO : skipping test and hoping for the best"
	print "INFO : wxPython must be > v2.6 and unicode-enabled"
	print "=> cannot check"
else:
	try:
		import wxversion
		print "   - installed versions:", wxversion.getInstalled()
		print "=> found"
		print "   - selecting unicode enabled version >= 2.6"
		wxversion.select(versions='2.6-unicode', optionsRequired=True)
		print "=> selected"
	except ImportError:
		print "ERROR: wxversion not installed"
		print "ERROR: this is used to select the proper wxPython version"
		print "INFO : for details, see here:"
		print "INFO : http://wiki.wxpython.org/index.cgi/MultiVersionInstalls"
		print "INFO : skipping test and hoping for the best"
		print "INFO : wxPython must be > v2.6 and unicode-enabled"
		print "=> NOT found"
	except wxversion.VersionError:
		print "ERROR: wxPython-2.6-unicode not installed"
		print "ERROR: this is needed to show the GNUmed GUI"
		print "INFO : wxPython is available from http://www.wxpython.org"
		print "INFO : sys.path is set as follows:"
		print "INFO :", "\nINFO : ".join(sys.path)
		sys.exit(-1)

print "=> checking for Python module 'wxPython' ..."
try:
	import wx
	print "   - active version:", wx.VERSION_STRING
	try:
		print "   - platform info:", wx.PlatformInfo
	except: pass
	print "=> found"
except ImportError:
	import os
	if os.getenv('DISPLAY') is None:
		print "INFO : you may have to explicitely set $DISPLAY"
	print "ERROR: wxPython not installed"
	print "ERROR: this is needed to show the GNUmed GUI"
	print "INFO : wxPython is available from http://www.wxpython.org"
	print "INFO : on Mac OSX Panther you may have to use 'export DISPLAY=:0'"
	print "INFO : sys.path is set as follows:"
	print "INFO :", "\nINFO : ".join(sys.path)
	sys.exit(-1)

print "=> checking for Python module 'sane' ..."
try:
	import sane
	print "=> found"
except ImportError:
	print "ERROR: sane not installed"
	print "INFO : this is needed to access scanners on Linux"
	print "INFO : GNUmed will work but you will be unable to scan"

print "=> checking for Python module 'twain' ..."
try:
	import twain
	print "=> found"
except ImportError:
	print "ERROR: twain not installed"
	print "INFO : this is needed to access scanners on Windows"
	print "INFO : GNUmed will work but you will be unable to scan"

print "=> checking for GNUmed's own Python modules ..."
try:
	from Gnumed.pycommon import gmNull
	print "=> found"
except ImportError:
	print "ERROR: GNUmed's own Python modules not found"
	print "ERROR: these handle most of the work in GNUmed"
	print "INFO : sys.path is set as follows:"
	print "INFO :", "\nINFO : ".join(sys.path)
	sys.exit(-1)

print "\n****************************************************"
print "* Most likely you can run GNUmed without problems. *"
print "****************************************************"
sys.exit(0)

#=================================================================
# $Log: check-prerequisites.py,v $
# Revision 1.10  2006-08-09 14:05:28  ncq
# - more unified output
# - better wxversion/wxPython detection
# - add checks for SANE/TWAIN
#
# Revision 1.9  2006/08/08 10:41:35  ncq
# - improve debug output
#
# Revision 1.8  2006/08/01 18:47:43  ncq
# - improved wording/readability
# - add test for GNUmed's own Python modules
#
# Revision 1.7  2005/10/15 11:29:14  ncq
# - some wxPythons don't support wx.PlatformInfo so don't error on it
#
# Revision 1.6  2005/09/24 09:11:46  ncq
# - enhance wxPython checks
#
# Revision 1.5  2005/07/11 08:31:23  ncq
# - string fixes
#
# Revision 1.4  2005/02/21 18:05:38  ncq
# - add some reassuring text in the case of success
#
# Revision 1.3  2004/07/05 03:33:55  dgrant
# Removed extraneous print "found"
#
# Revision 1.2  2004/05/29 22:39:14  ncq
# - warn on export DISPLAY on Mac OSX
#
# Revision 1.1  2004/02/19 16:51:08  ncq
# - first version
#
