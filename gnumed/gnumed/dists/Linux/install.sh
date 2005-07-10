#!/bin/sh

# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/dists/Linux/Attic/install.sh,v $
# $Id: install.sh,v 1.3 2005-07-10 18:24:48 ncq Exp $
# $Revision: 1.3 $
# license: GPL
# sebastian.hilbert@gmx.net

# todo: 
# log install path for uninstall file
# log installation

# change this to match GNUmed version
REV=0.1

LOG="install-GNUmed-$REV.log"

echo "######################################################################################
#                                                                                    # 
# Welcome. You are about to install GNUmed. Please observe the output on the screen  #
# You will be prompted for target locations for GNUmed. The defaults provided give a #
# working setup on most systems and are considered safe. Your milage may vary.       #   
#                                                                                    #
#                                                      - GNUmed release team -       #
#                                                                                    #
######################################################################################"

echo "Installing GNUmed $REV ..." > $LOG

mkdir -p /usr/lib/python/site-packages/Gnumed/ &> $LOG
mkdir -p /usr/share/doc/gnumed/client &> $LOG
mkdir -p /usr/lib/python/site-packages/Gnumed/exporters/ &> $LOG
mkdir -p /usr/lib/python/site-packages/Gnumed/importers/ &> $LOG
mkdir -p /etc/gnumed/ &> $LOG
mkdir -p /usr/lib/python/site-packages/Gnumed/ &> $LOG
mkdir -p /usr/share/gnumed/pixmaps/ &> $LOG
#mkdir -p ./GNUmed-$REV/client/usr/share/locale/de/LC_MESSAGES/
#mkdir -p ./GNUmed-$REV/client/usr/share/locale/de_DE/LC_MESSAGES/
#mkdir -p ./GNUmed-$REV/client/usr/share/locale/fr/LC_MESSAGES/
#mkdir -p ./GNUmed-$REV/client/usr/share/locale/fr_FR/LC_MESSAGES/
#mkdir -p ./GNUmed-$REV/client/usr/share/locale/es/LC_MESSAGES/
#mkdir -p ./GNUmed-$REV/client/usr/share/locale/es_ES/LC_MESSAGES/

#####################################

dfltgmdir=/usr/share/gnumed
echo "client bitmap target directory [$dfltgmdir]:" 
read newgmdir
if [ "$newgmdir" = "" ]; then
	gmdir=$dfltgmdir
else
	gmdir=$newgmdir
fi
echo "GNUmed directory: $gmdir" &> $LOG

cp -R ./GNUmed-$REV/client/usr/share/gnumed/bitmaps $gmdir &> $LOG
cp -R ./GNUmed-$REV/client/usr/share/gnumed/pixmaps/gnumed.xpm $gmdir/pixmaps/gnumed.xpm &> $LOG
#####################################
dfltpythondir=/usr/lib/python/site-packages/Gnumed
echo "python directory [$dfltpythondir]:" 
read newpythondir
if [ "$newpythondir" = "" ]; then
            pythondir=$dfltpythondir
else
            pythondir=$newpythondir
fi
echo "GNUmed Python directory: $pythondir" &> $LOG

cp -R ./GNUmed-$REV/client/usr/lib/python/site-packages/Gnumed/business $pythondir &> $LOG
cp -R ./GNUmed-$REV/client/usr/lib/python/site-packages/Gnumed/exporters/*.py $pythondir/exporters/
cp -R ./GNUmed-$REV/client/usr/lib/python/site-packages/Gnumed/importers/*.py $pythondir/importers/ &> $LOG
cp -R ./GNUmed-$REV/client/usr/lib/python/site-packages/Gnumed/sitecustomize.py $pythondir &> $LOG
cp -R ./GNUmed-$REV/client/usr/lib/python/site-packages/Gnumed/pycommon $pythondir &> $LOG
cp -R ./GNUmed-$REV/client/usr/lib/python/site-packages/Gnumed/wxpython $pythondir &> $LOG
cp -R ./GNUmed-$REV/client/usr/lib/python/site-packages/Gnumed/__init__.py $pythondir &> $LOG

#######################################
dfltdocdir=/usr/share/doc/gnumed
echo "client documentation target directory [$dfltdocdir]:" 
read newdocdir
if [ "$newdocdir" = "" ]; then
            docdir=$dfltdocdir
else
            docdir=$newdocdir
fi
echo "GNUmed documentation directory: $docdir" &> $LOG

cp -R ./GNUmed-$REV/client/usr/share/doc/gnumed/medical_knowledge $docdir &> $LOG
cp -R ./GnuPublicLicense.txt $docdir &> $LOG

#######################################
dfltconfdir=/etc/gnumed
echo "client config files target directory [$dfltconfdir]:" 
read newconfdir
if [ "$newconfdir" = "" ]; then
            confdir=$dfltconfdir
else
            confdir=$newconfdir
fi
echo "GNUmed configuration directory: $confdir" &> $LOG

cp -R ./GNUmed-$REV/client/etc/gnumed/*.conf $confdir &> $LOG

#######################################
dfltlocaledir=/usr/share/locale
echo "client language files target directory [$dfltlocaledir]:" 
read newlocaledir
if [ "$newlocaledir" = "" ]; then
            localedir=$dfltlocaledir
else
            localedir=$newlocaledir
fi
echo "GNUmed locale directory: $localedir" &> $LOG

cp -R ./GNUmed-$REV/client/usr/share/locale $localedir &> $LOG
#######################################

cp -R ./GNUmed-$REV/client/usr/bin/gnumed /usr/bin &> $LOG

# FIXME: put this some decent place
cp -R ./check-prerequisites.py $docdir &> $LOG
cp -R ./check-prerequisites.sh $docdir &> $LOG

#================================================
# $Log: install.sh,v $
# Revision 1.3  2005-07-10 18:24:48  ncq
# - log what we do into a log file
#
# Revision 1.2  2005/07/10 17:54:04  ncq
# - put check-* into doc dir for now
#
