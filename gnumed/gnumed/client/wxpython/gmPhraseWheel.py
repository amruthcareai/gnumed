"""
A class, extending wxTextCtrl, which has a drop-down pick list,
automatically filled based on the inital letters typed. Based on the
interface of Richard Terry's Visual Basic client

This is based on seminal work by Ian Haywood <ihaywood@gnu.org>
"""
#@copyright: GPL

############################################################################
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/wxpython/gmPhraseWheel.py,v $
# $Id: gmPhraseWheel.py,v 1.6 2003-09-13 17:46:29 ncq Exp $
__version__ = "$Revision: 1.6 $"
__author__  = "K.Hilbert <Karsten.Hilbert@gmx.net>, I.Haywood"

import string, types, time, sys, re

if __name__ == "__main__":
	sys.path.append ("../python-common/")

import gmLog
_log = gmLog.gmDefLog

from wxPython.wx import *

_true = (1==1)
_false = (1==0)
#------------------------------------------------------------
# generic base class
#------------------------------------------------------------
class cMatchProvider:
	"""Base class for match providing objects.

	Match sources might be:
	- database tables
	- flat files
	- previous input
	- config files
	- in-memory list created on the fly
	"""
	__threshold = {}
	default_word_separators = re.compile('[- \t=+&:_@]+')
	default_ignored_chars = re.compile("""[?!."'\\(){}\[\]<>~#*$%^]+""")
	#--------------------------------------------------------
	def __init__(self):
		self.enableMatching()
		self.enableLearning()
		self.setThresholds()
		self.setWordSeparators()
		self.ignored_chars = cMatchProvider.default_ignored_chars
	#--------------------------------------------------------
	# actions
	#--------------------------------------------------------
	def getMatches(self, aFragment = None):
		"""Return matches according to aFragment and matching thresholds.

		FIXME: design decision: we don't worry about data source changes
			   during the lifetime of a MatchProvider
		FIXME: sort according to weight
		FIXME: append _("*get all items*") on truncation
		"""
		# do we return matches at all ?
		if not self.__deliverMatches:
			return (_false, [])

		# sanity check
		if aFragment is None:
			_log.Log(gmLog.lErr, 'Cannot find matches without a fragment.')
			raise ValueError, 'Cannot find matches without a fragment.'

		# user explicitely wants all matches
		if aFragment == "*":
			return self.getAllMatches()

		# case insensitivity
		tmpFragment = string.lower(aFragment)
		# remove ignored chars
		tmpFragment = self.ignored_chars.sub('', tmpFragment)
		# normalize word separators
		tmpFragment = string.join(self.word_separators.split(tmpFragment), ' ')
		# length in number of significant characters only
		lngFragment = len(tmpFragment)
		# order is important !
		if lngFragment >= self.__threshold['substring']:
			return self.getMatchesBySubstr(tmpFragment)
		elif lngFragment >= self.__threshold['word']:
			return self.getMatchesByWord(tmpFragment)
		elif lngFragment >= self.__threshold['phrase']:
			return self.getMatchesByPhrase(tmpFragment)
		else:
			return (_false, [])
	#--------------------------------------------------------
	def getAllMatches(self):
		pass
	#--------------------------------------------------------
	def getMatchesByPhrase(self, aFragment):
		pass
	#--------------------------------------------------------
	def getMatchesByWord(self, aFragment):
		pass
	#--------------------------------------------------------
	def getMatchesBySubstr(self, aFragment):
		pass
	#--------------------------------------------------------
	def increaseScore(self, anItem):
		"""Increase the score/weighting for a particular item due to it being used."""
		pass
	#--------------------------------------------------------
	def learn(self, anItem, aContext):
		"""Add this item to the match source so we can find it next time around.

		- aContext can be used to denote the context where to use this item for matching
		- it is typically used to select a context sensitive item list during matching
		"""
		pass
	#--------------------------------------------------------
	def forget(self, anItem, aContext):
		"""Remove this item from the match source if possible."""
		pass
	#--------------------------------------------------------
	# configuration
	#--------------------------------------------------------
	def setThresholds(self, aPhrase = 1, aWord = 3, aSubstring = 5):
		"""Set match location thresholds.

		- the fragment passed to getMatches() must contain at least this many
		  characters before it triggers a match search at:
		  1) phrase_start - start of phrase (first word)
		  2) word_start - start of any word within phrase
		  3) in_word - _inside_ any word within phrase
		"""
		# sanity checks
		if aSubstring < aWord:
			_log.Log(gmLog.lErr, 'Setting substring threshold (%s) lower than word-start threshold (%s) does not make sense. Retaining original thresholds (%s:%s, respectively).' % (aSubstring, aWord, self.__threshold['substring'], self.__threshold['word']))
			return (1==0)
		if aWord < aPhrase:
			_log.Log(gmLog.lErr, 'Setting word-start threshold (%s) lower than phrase-start threshold (%s) does not make sense. Retaining original thresholds (%s:%s, respectively).' % (aSubstring, aWord, self.__threshold['word'], self.__threshold['phrase']))
			return (1==0)

		# now actually reassign thresholds
		self.__threshold['phrase']	= aPhrase
		self.__threshold['word']	= aWord
		self.__threshold['substring']	= aSubstring

		return _true
	#--------------------------------------------------------
	def setWordSeparators(self, separators = None):
		if separators is None:
			self.word_separators = cMatchProvider.default_word_separators
			return 1
		if separators == "":
			_log.Log(gmLog.lErr, 'Not defining any word separators does not make sense ! Keeping previous setting.')
			return None
		try:
			self.word_separators = re.compile(separators)
		except:
			_log.LogException('cannot compile word separators regex >>>%s<<<, keeping previous setting' % separators)
			return None
		return _true
	#--------------------------------------------------------
	def disableMatching(self):
		"""Don't search for matches.

		Useful if a slow network database link is detected, for example.
		"""
		self.__deliverMatches = _false
	#--------------------------------------------------------
	def enableMatching(self):
		self.__deliverMatches = _true
	#--------------------------------------------------------
	def disableLearning(self):
		"""Immediately stop learning new items."""
		self.__learnNewItems = _false
	#--------------------------------------------------------
	def enableLearning(self):
		"""Immediately start learning new items."""
		self.__learnNewItems = _true
#------------------------------------------------------------
# usable instances
#------------------------------------------------------------
class cMatchProvider_FixedList(cMatchProvider):
	"""Match provider where all possible options can be held
	   in a reasonably sized, pre-allocated list.
	"""
	def __init__(self, aSeq = None):
		"""aSeq must be a list of dicts. Each dict must have the keys (ID, label, weight)
		"""
		if not type(aSeq) in [types.ListType, types.TupleType]:
			print "aList must be a list or tuple"
			return None

		self.__items = aSeq
		cMatchProvider.__init__(self)
	#--------------------------------------------------------
	# internal matching algorithms
	#
	# if we end up here:
	#	- aFragment will not be "None"
	#   - aFragment will be lower case
	#	- we _do_ deliver matches (whether we find any is a different story)
	#--------------------------------------------------------
	def getMatchesByPhrase(self, aFragment):
		"""Return matches for aFragment at start of phrases."""
		matches = []
		# look for matches
		for item in self.__items:
			# at start of phrase, that is
			if string.find(string.lower(item['label']), aFragment) == 0:
				matches.append(item)
		# no matches found
		if len(matches) == 0:
			return (_false, [])

		matches.sort(self.__cmp_items)
		return (_true, matches)
	#--------------------------------------------------------
	def getMatchesByWord(self, aFragment):
		"""Return matches for aFragment at start of words inside phrases."""
		matches = []
		# look for matches
		for item in self.__items:
			pos = string.find(string.lower(item['label']), aFragment)
			# found at start of phrase
			if pos == 0:
				matches.append(item)
			# found as a true substring
			elif pos > 0:
				# but use only if substring is at start of a word
				if (item['label'])[pos-1] == ' ':
					matches.append(item)
		# no matches found
		if len(matches) == 0:
			return (_false, [])

		matches.sort(self.__cmp_items)
		return (_true, matches)
	#--------------------------------------------------------
	def getMatchesBySubstr(self, aFragment):
		"""Return matches for aFragment as a true substring."""
		matches = []
		# look for matches
		for item in self.__items:
			if string.find(string.lower(item['label']), aFragment) != -1:
				matches.append(item)
		# no matches found
		if len(matches) == 0:
			return (_false, [])

		matches.sort(self.__cmp_items)
		return (_true, matches)
	#--------------------------------------------------------
	def getAllMatches(self):
		"""Return all items."""
		matches = self.__items
		# no matches found
		if len(matches) == 0:
			return (_false, [])

		matches.sort(self.__cmp_items)
		return (_true, matches)
	#--------------------------------------------------------
	def __cmp_items(self, item1, item2):
		"""Compare items based on weight."""
		# do it the wrong way round to do sorting/reversing at once
		if item1['weight'] < item2['weight']:
			return 1
		elif item1['weight'] > item2['weight']:
			return -1
		else:
			return 0
#------------------------------------------------------------
#------------------------------------------------------------
class cWheelTimer(wxTimer):
	"""Timer for delayed fetching of matches.

	It would be quite useful to tune the delay
	according to current network speed either at
	application startup or even during runtime.

	No logging in here as this should be as fast as possible.
	"""
	def __init__(self, aCallback = None, aDelay = 300):
		"""Set up our timer with reasonable defaults.

		- delay default is 300ms as per Richard Terry's experience
		- delay should be tailored to network speed/user speed
		"""
		# sanity check
		if aCallback is None:
			_log.Log(gmLog.lErr, "No use setting up a timer without a callback function.")
			return None
		else:
			self.__callback = aCallback

		self.__delay = aDelay

		wxTimer.__init__(self)
	#--------------------------------------------------------
	def Notify(self):
		self.__callback()
#------------------------------------------------------------
#------------------------------------------------------------
class cPhraseWheel (wxTextCtrl):
	"""Widget for smart guessing of user fields, after Richard Terry's interface."""

	default_phrase_separators = re.compile('[;/|]+')

	def __init__ (self,
					parent,
					id_callback,
					id = -1,
					pos = wxDefaultPosition,
					size = wxDefaultSize,
					aMatchProvider = None,
					aDelay = 300):
		"""
		id_callback holds a reference to another Python function.
		This function is called when the user selects a value.
		This function takes a single parameter -- being the ID of the
		value so selected"""

		if not isinstance(aMatchProvider, cMatchProvider):
			_log.Log(gmLog.lErr, "aMatchProvider must be a match provider object")
			return None
		self.__matcher = aMatchProvider
		self.__currMatches = []
		self.phrase_separators = cPhraseWheel.default_phrase_separators
		self.__timer = cWheelTimer(self._on_timer_fired, aDelay)

		wxTextCtrl.__init__ (self, parent, id, "", pos, size)
		# unneccsary as we are using styles
		#self.SetBackgroundColour (wxColour (200, 100, 100))
		self.parent = parent

		# set event handlers
		# 1) entered text changed
		EVT_TEXT	(self, self.GetId(), self.__on_text_update)
		# 2) a key was released
		EVT_KEY_UP	(self, self.__on_key_released)
		# 3) evil user wants to resize widget
		EVT_SIZE	(self, self.on_resize)

		self.id_callback = id_callback

		x, y = pos
		width, height = size
		self.__picklist_win = wxWindow (parent, -1, pos = (x, y+height), size = (width, width))
		self.panel = wxPanel(self.__picklist_win, -1)
		self.__picklist = wxListBox(self.panel, -1, style=wxLB_SINGLE | wxLB_NEEDED_SB)
		self.__picklist.Clear()
		self.__picklist_win.Hide ()
		self.__picklist_visible = _false
	#--------------------------------------------------------
	def __updateMatches(self):
		"""Get the matches for the currently typed input fragment."""

		# get current(ly relevant part of) input
		relevant_input = self.GetValue()
#		cursor_pos = self.GetInsertionPoint()
		# find last phrase separator position before cursor position
#		prev_pos = self.phrase_separators.##(relevant_input)
		# get all currently matching items
		(matched, self.__currMatches) = self.__matcher.getMatches(relevant_input)
		# and refill our picklist with them
		self.__picklist.Clear()
		if matched:
			for item in self.__currMatches:
				self.__picklist.Append(item['label'], clientData = item['ID'])
	#--------------------------------------------------------
	def __show_picklist(self):
		"""Display the pick list."""

		# recalculate position
		# FiXME: check for number of entries - shrink list windows
		#pos = self.ClientToScreen ((0,0))
		#dim = self.GetSize ()
		#self.__picklist_win.Position(pos, (0, dim.height))

		# select first value
		self.__picklist.SetSelection(0)

		# remember that we have a list window
		self.__picklist_visible = _true

		# and show it
		# FIXME: we should _update_ the list window instead of redisplaying it
		self.__picklist_win.Show()
		self.__picklist.Show()
	#--------------------------------------------------------
	def __hide_picklist(self):
		"""Hide the pick list."""
		if self.__picklist_visible:
			self.__picklist_win.Hide()		# dismiss the dropdown list window
		self.__picklist_visible = _false
	#--------------------------------------------------------
	# specific event handlers
	#--------------------------------------------------------
	def OnSelected (self):
		"""Gets called when user selected a list item."""
		self.__hide_picklist()

		n = self.__picklist.GetSelection()		# get selected item
		data = self.__picklist.GetClientData(n)		# get data associated with selected item
		self.SetValue (self.__picklist.GetString(n))	# tell the input field to display that data

		self.id_callback (data)				# and tell our parent about the user's selection
	#--------------------------------------------------------
	# individual key handlers
	#--------------------------------------------------------
	def __on_enter (self):
		"""Called when the user pressed <ENTER>.

		FIXME: this might be exploitable for some nice statistics ...
		"""

		# if we have a pick list
		if self.__picklist_visible:
			# tell the input field about it
			self.OnSelected()
	#--------------------------------------------------------
	def __on_down_arrow(self):
		# if we already have a pick list go to next item
		if self.__picklist_visible:
			selected = self.__picklist.GetSelection()
			# but only if not at end of list already
			if selected < (self.__picklist.GetCount() - 1):
				self.__picklist.SetSelection(selected + 1)

		# if we don't yet have a pick list
		# - open new pick list
		# (this can happen when we TAB into a field pre-filled
		#  with the top-weighted contextual data but want to
		#  select another contextual item)
		else:
			# don't need timer anymore since user explicitely requested list
			self.__timer.Stop()
			# update matches according to current input
			self.__updateMatches()
			# if we do have matches now show list
			if len(self.__currMatches) > 0:
				self.__show_picklist()
	#--------------------------------------------------------
	def __on_up_arrow(self):
		if self.__picklist_visible:
			selected = self.__picklist.GetSelection()
			# select previous item if available
			if selected > 0:
				self.__picklist.SetSelection(selected-1)
			else:
				# FIXME: return to input field and close pick list ?
				pass
		else:
			# FIXME: input history ?
			pass
	#--------------------------------------------------------
	# event handlers
	#--------------------------------------------------------
	def __on_key_released (self, key):
		"""Is called when a key is released."""
		# user moved down
		if key.GetKeyCode() == WXK_DOWN:
			self.__on_down_arrow()
			return
		# user moved up
		if key.GetKeyCode() == WXK_UP:
			self.__on_up_arrow()
			return
		# FIXME: need PAGE UP/DOWN//POS1/END here

		# user pressed <ENTER>
		if key.GetKeyCode() == WXK_RETURN:
			self.__on_enter()
			return

		key.Skip()
	#--------------------------------------------------------
	def __on_text_update (self, event):
		"""Internal handler for EVT_TEXT (called when text has changed)"""

		# if empty string then kill list dropdown window
		# we also don't need a timer event then
		if len(self.GetValue()) == 0:
			self.__hide_picklist()
			# and kill timer lest there be a zombie of it running
			self.__timer.Stop()
		else:
			# start timer for delayed match retrieval
			self.__timer.Start(oneShot = _true)
	#--------------------------------------------------------
	def on_resize (self, event):
		sz = self.GetSize()
		self.__picklist.SetSize ((sz.width, sz.height*6))
		# as wide as the textctrl, and 6 times the height
		self.panel.SetSize (self.__picklist.GetSize ())
		self.__picklist_win.SetSize (self.panel.GetSize())
	#--------------------------------------------------------
	def _on_timer_fired (self):
		"""Callback for delayed match retrieval timer.

		if we end up here:
		 - delay has passed without user input
		 - the value in the input field has not changed since the timer started
		"""
		# update matches according to current input
		self.__updateMatches()
		# we now have either:
		# - all possible items (within reasonable limits) if input was '*'
		# - all matching items
		# - an empty match list if no matches were found
		# also, our picklist is refilled and sorted according to weight

		# display list - but only if we have any matches
		if len(self.__currMatches) > 0:
			# show it
			self.__show_picklist()
		else:
			# we may have had a pick list window so we need to
			# dismiss that since we don't have input anymore
			self.__hide_picklist()
#--------------------------------------------------------
# MAIN
#--------------------------------------------------------
if __name__ == '__main__':
	import gmI18N
	#----------------------------------------------------
	def clicked (data):
		print "Selected :%s" % data
	#----------------------------------------------------
	class TestApp (wxApp):
		def OnInit (self):
			items = [	{'ID':1, 'label':"Bloggs", 	'weight':5},
						{'ID':2, 'label':"Baker",  	'weight':4},
						{'ID':3, 'label':"Jones",  	'weight':3},
						{'ID':4, 'label':"Judson", 	'weight':2},
						{'ID':5, 'label':"Jacobs", 	'weight':1},
						{'ID':6, 'label':"Judson-Jacobs",'weight':5}
					]
			mp = cMatchProvider_FixedList(items)

			frame = wxFrame (None, -4, "phrase wheel test for GNUmed", size=wxSize(300, 350), style=wxDEFAULT_FRAME_STYLE|wxNO_FULL_REPAINT_ON_RESIZE)

			# actually, aDelay of 300ms is also the built-in default
			ww = cPhraseWheel(frame, clicked, pos = (50, 50), size = (180, 30), aMatchProvider=mp)
			ww.on_resize (None)
			frame.Show (1)
			return 1
	#--------------------------------------------------------
	app = TestApp ()
	app.MainLoop ()

#==================================================
# $Log: gmPhraseWheel.py,v $
# Revision 1.6  2003-09-13 17:46:29  ncq
# - pattern match word separators
# - pattern match ignore characters as per Richard's suggestion
# - start work on phrase separator pattern matching with extraction of
#   relevant input part (where the cursor is at currently)
#
# Revision 1.5  2003/09/10 01:50:25  ncq
# - cleanup
#
#
#==================================================

#----------------------------------------------------------
# ideas
#----------------------------------------------------------
#- display possible completion but highlighted for deletion
#(- cycle through possible completions)
#- pre-fill selection with SELECT ... LIMIT 25
#- weighing by incrementing counter - if rollover, reset all counters to percentage of self.value()
#- ageing of item weight
#- async threads for match retrieval instead of timer
#  - on truncated results return item "..." -> selection forcefully retrieves all matches

#- plugin for pattern matching/validation of input

#- generators/yield()
#- OnChar() - process a char event

# split input into words and match components against known phrases
# -> accumulate weights into total item weight

# - case insensitive by default but
# - make case sensitive matching possible
#   - if no matches found revert to case _insensitive_ matching
# - maybe _sensitive_ by default + auto-revert if too few matches ?

# make special list window:
# - deletion of items
# - highlight matched parts
# - faster scrolling
# - wxEditableListBox ?

# - press down only once to get into list
# - auto repeat on down arrow key
# - moving between list members is too slow

# - if non-learning (i.e. fast select only): autocomplete with match
#   and move cursor to end of match
#-----------------------------------------------------------------------------------------------
# darn ! this clever hack won't work since we may have crossed a search location threshold
#----
#	#self.__prevFragment = "XXXXXXXXXXXXXXXXXX-very-unlikely--------------XXXXXXXXXXXXXXX"
#	#self.__prevMatches = []		# a list of tuples (ID, listbox name, weight)
#
#	# is the current fragment just a longer version of the previous fragment ?
#	if string.find(aFragment, self.__prevFragment) == 0:
#	    # we then need to search in the previous matches only
#	    for prevMatch in self.__prevMatches:
#		if string.find(prevMatch[1], aFragment) == 0:
#		    matches.append(prevMatch)
#	    # remember current matches
#	    self.__prefMatches = matches
#	    # no matches found
#	    if len(matches) == 0:
#		return [(1,_('*no matching items found*'),1)]
#	    else:
#		return matches
#----
#TODO:
# - see spincontrol for list box handling
