[templ::py_header]

from trax.api.notifications import NotificationEventDef

class [classname]( NotificationEventDef ):
	Component 	= '[component]'	# define the notification component
	Event		= '[event]'		# define the notification event
	Version		= 0				# used to sync preferences with users
	
	@classmethod
	def brief( cls, record, **kwds ):
		"""
			\remarks	return a brief version of the notification (used by jabber and other text-only methods)
			\param		record		<trax.api.data.Record>
			\return		<str> simple text
		"""
		return '[Trax] Missing Notification Brief (%s::%s)' % (cls.Component,cls.Event)
	
	@classmethod
	def collectUsers( cls, record, **kwds ):
		"""
			\remarks	collect a list of user records that needs to be notified based on the inputed record
			\param		record		<trax.api.data.Record>
			\return		<list> [ <trax.api.data.User>, .. ]
		"""
		return []
	
	@classmethod
	def html( cls, record, **kwds ):
		"""
			\remarks	return a rich text version of the notification (used by email and other HTML capable methods)
			\param		record		<trax.api.data.Record>
			\return		<str> html
		"""
		return '<div style="color:red"/><b>Warning:</b> Missing HTML method (%s::%s)</div>' % (cls.Component,cls.Event)
	
	@classmethod
	def occursAt( cls, record, **kwds ):
		"""
			\remarks	return a QDateTime instance representing the date the notification will actually occur.  Return a NULL QDateTime instance
						for non-specific events
			\param		record		<trax.api.data.Record>
			\return		<QDateTime>
		"""
		from PyQt4.QtCore import QDateTime
		return QDateTime()
		
	@classmethod
	def setupDefaultPrefs( cls, users, upgradeVersion = 0 ):
		"""
			\remarks	create the default NotificationUserPref instances that will drive the notification system for the inputed user
			\param		user	<list> [ <trax.api.data.User>, .. ]
			\return		<int> number created
		"""
		return 0
		
	@classmethod
	def subject( cls, record, **kwds ):
		"""
			\remarks	return the subject line to be used when emailing or jabbering this notification
			\param		record	<trax.api.data.Record>
			\return		<str> subject
		"""
		return '[Trax] Missing Notification Subject (%s::%s)' % (cls.Component,cls.Event)
		
# register the notification event definition
import trax.api
from trax.api import notifications
notifications.register( '%s::%s' % ([classname].Component,[classname].Event), [classname] )