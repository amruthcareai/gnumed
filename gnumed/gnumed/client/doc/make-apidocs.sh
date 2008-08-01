#!/bin/bash

# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/doc/make-apidocs.sh,v $
# $Revision: 1.13 $
# license: GPL
# author: Karsten.Hilbert@gmx.net

BASE=~/gm-cvs-branches/HEAD/gnumed/gnumed/Gnumed
#MODULES=" $BASE/pycommon/ $BASE/business/ $BASE/connectors/ $BASE/exporters/ $BASE/importers/ $BASE/wxpython/"
LOG=~/gm-apidocs/epydoc-errors.txt

export DISPLAY=":0.0"
export PYTHONPATH="${PYTHONPATH}:~/gm-cvs-head/gnumed/gnumed/"
nice -n 19 epydoc -v --debug --show-imports -n "GNUmed Never Sleeps" -u http://www.gnumed.org --no-private -o ~/gm-apidocs $BASE/ &> $LOG
cat $LOG

#============================================
# $Log: make-apidocs.sh,v $
# Revision 1.13  2008-08-01 10:08:49  ncq
# - /bin/sh -> /bin/bash
#
# Revision 1.12  2007/01/25 08:32:30  ncq
# - fix path for salaam
#
# Revision 1.11  2005/12/27 17:55:01  ncq
# - various tweaks regarding $BASE
#
# Revision 1.10  2005/12/23 22:52:52  ncq
# - try fixing the obscure epydoc errors "no such module Gnumed.pycommon"
#
# Revision 1.9  2005/12/22 00:25:02  ncq
# - more verbose errors
# - show imported modules even if they fail to be doc'ed
# - proper base directory
#
# Revision 1.8  2005/12/09 20:58:06  ncq
# - add wxpython now that wxPython doesn't need a DISPLAY anymore
#
# Revision 1.7  2005/12/09 20:53:09  ncq
# - proper BASE dir
#
# Revision 1.6  2005/12/09 20:43:25  ncq
# - improved output
#
# Revision 1.5  2005/02/15 18:37:33  ncq
# - capture log for display in the Wiki
#
# Revision 1.4  2005/02/15 12:01:20  ncq
# - since there is no easy answer to cronning epydoc over wxPython
#   exclude that for now such that we at least get the rest of the
#   API epydoced regularly
#
# Revision 1.3  2005/01/19 09:27:59  ncq
# - let callers deal with output, don't predefine target as file (cron mails it)
#
# Revision 1.2  2005/01/09 15:58:56  ncq
# - add export DISPLAY to make epydoc think it can open the local display for importing wx to succeed
#
# Revision 1.1  2004/07/14 10:11:04  ncq
# - first checkin
#
