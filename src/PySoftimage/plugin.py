##
#	\namespace	blurdev.cores.studiomaxcore.plugin
#
#	\remarks	Defines the plugin methods needed for the softimage session using the blurdev package
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		04/12/10
#

#-------------------------------------------------------------------------------------------------------------
# define python plugin information

from win32com.client 	import constants
from PyQt4.QtCore		import Qt

#-------------------------------------------------------------------------------------------------------------

# Create a mapping of virtual keys
import win32con
KEY_MAPPING 	= {
	# key: ( Qt::Key,			ascii,	modifiers )
	
	  8: ( Qt.Key_Backspace,	'',		None ),
	  9: ( Qt.Key_Tab,			'\t',	None ),
	 13: ( Qt.Key_Enter,		'\n',	None ),
	 16: ( Qt.Key_Shift,		'',		None ),
	 17: ( Qt.Key_Control,		'',		None ),
	 18: ( Qt.Key_Alt,			'',		None ),
	 19: ( Qt.Key_Pause,		'',		None ),
	 20: ( Qt.Key_CapsLock,		'',		None ),
	 27: ( Qt.Key_Escape, 		'',		None ),
	 32: ( Qt.Key_Space,		' ',	None ),
	 33: ( Qt.Key_PageUp,		'',		None ),
	 34: ( Qt.Key_PageDown,		'',		None ),
	 35: ( Qt.Key_End,			'',		None ),
	 36: ( Qt.Key_Home,			'',		None ),
	 37: ( Qt.Key_Left,			'',		None ),
	 38: ( Qt.Key_Up,			'',		None ),
	 39: ( Qt.Key_Right,		'',		None ),
	 40: ( Qt.Key_Down,			'',		None ),
	 44: ( Qt.Key_SysReq,		'',		None ),
	 45: ( Qt.Key_Insert,		'',		None ),
	 46: ( Qt.Key_Delete,		'',		None ),
	 48: ( Qt.Key_0,			'0',	None ),
	 49: ( Qt.Key_1,			'1',	None ),
	 50: ( Qt.Key_2,			'2',	None ),
	 51: ( Qt.Key_3,			'3',	None ),
	 52: ( Qt.Key_4,			'4',	None ),
	 53: ( Qt.Key_5,			'5',	None ),
	 54: ( Qt.Key_6,			'6',	None ),
	 55: ( Qt.Key_7,			'7',	None ),
	 56: ( Qt.Key_8,			'8',	None ),
	 57: ( Qt.Key_9,			'9',	None ),
	 65: ( Qt.Key_A,			'a',	None ),
	 66: ( Qt.Key_B,			'b',	None ),
	 67: ( Qt.Key_C,			'c',	None ),
	 68: ( Qt.Key_D,			'd',	None ),
	 69: ( Qt.Key_E,			'e',	None ),
	 70: ( Qt.Key_F,			'f',	None ),
	 71: ( Qt.Key_G,			'g',	None ),
	 72: ( Qt.Key_H,			'h',	None ),
	 73: ( Qt.Key_I,			'i',	None ),
	 74: ( Qt.Key_J,			'j',	None ),
	 75: ( Qt.Key_K,			'k',	None ),
	 76: ( Qt.Key_L,			'l',	None ),
	 77: ( Qt.Key_M,			'm',	None ),
	 78: ( Qt.Key_N,			'n',	None ),
	 79: ( Qt.Key_O,			'o',	None ),
	 80: ( Qt.Key_P,			'p',	None ),
	 81: ( Qt.Key_Q,			'q',	None ),
	 82: ( Qt.Key_R,			'r',	None ),
	 83: ( Qt.Key_S,			's',	None ),
	 84: ( Qt.Key_T,			't',	None ),
	 85: ( Qt.Key_U,			'u',	None ),
	 86: ( Qt.Key_V,			'v',	None ),
	 87: ( Qt.Key_W,			'w',	None ),
	 88: ( Qt.Key_X,			'x',	None ),
	 89: ( Qt.Key_Y,			'y',	None ),
	 90: ( Qt.Key_Z,			'z',	None ),
	 93: ( Qt.Key_Print,		'',		None ),
	 96: ( Qt.Key_0,			'0',	Qt.KeypadModifier ),
	 97: ( Qt.Key_1,			'1',	Qt.KeypadModifier ),
	 98: ( Qt.Key_2,			'2',	Qt.KeypadModifier ),
	 99: ( Qt.Key_3,			'3',	Qt.KeypadModifier ),
	100: ( Qt.Key_4,			'4',	Qt.KeypadModifier ),
	101: ( Qt.Key_5,			'5',	Qt.KeypadModifier ),
	102: ( Qt.Key_5,			'6',	Qt.KeypadModifier ),
	103: ( Qt.Key_5,			'7',	Qt.KeypadModifier ),
	104: ( Qt.Key_5,			'8',	Qt.KeypadModifier ),
	105: ( Qt.Key_5,			'9',	Qt.KeypadModifier ),
	106: ( Qt.Key_Asterisk,		'*',	Qt.KeypadModifier ),
	107: ( Qt.Key_Plus,			'+',	Qt.KeypadModifier ),
	109: ( Qt.Key_Minus,		'-',	Qt.KeypadModifier ),
	110: ( Qt.Key_Period,		'.',	Qt.KeypadModifier ),
	111: ( Qt.Key_Slash,		'/',	Qt.KeypadModifier ),
	112: ( Qt.Key_F1,			'',		None ),
	113: ( Qt.Key_F2,			'',		None ),
	114: ( Qt.Key_F3,			'',		None ),
	115: ( Qt.Key_F4,			'',		None ),
	116: ( Qt.Key_F5,			'',		None ),
	117: ( Qt.Key_F6,			'',		None ),
	118: ( Qt.Key_F7,			'',		None ),
	119: ( Qt.Key_F8,			'',		None ),
	120: ( Qt.Key_F9,			'',		None ),
	121: ( Qt.Key_F10,			'',		None ),
	122: ( Qt.Key_F11,			'',		None ),
	113: ( Qt.Key_F12,			'',		None ),
	144: ( Qt.Key_NumLock,		'',		None ),
	145: ( Qt.Key_ScrollLock,	'',		None ),
	186: ( Qt.Key_Semicolon,	';',	None ),
	187: ( Qt.Key_Equal,		'=',	None ),
	188: ( Qt.Key_Comma,		',',	None ),
	189: ( Qt.Key_Minus,		'-',	None ),
	190: ( Qt.Key_Period,		'.',	None ),
	191: ( Qt.Key_Slash,		'/',	None ),
	192: ( Qt.Key_QuoteLeft,	'`',	None ),
	219: ( Qt.Key_BracketLeft,	'[',	None ),
	220: ( Qt.Key_Backslash,	'\\',	None ),
	221: ( Qt.Key_BraceRight,	']',	None ),
	222: ( Qt.Key_QuoteLeft,	"'",	None ),
		
	# Calculate the SHIFT key as 300 + key value
	348: ( Qt.Key_ParenRight,	')',	None ),	# Shift+0
	349: ( Qt.Key_Exclam,		'!',	None ),	# Shift+1
	350: ( Qt.Key_At,			'@',	None ),	# Shift+2
	351: ( Qt.Key_NumberSign,	'#',	None ),	# Shift+3
	352: ( Qt.Key_Dollar,		'$',	None ),	# Shift+4
	353: ( Qt.Key_Percent,		'%',	None ),	# Shift+5
	354: ( Qt.Key_6,			'6',	None ),
	355: ( Qt.Key_Ampersand,	'&',	None ),	# Shift+7
	356: ( Qt.Key_Asterisk,		'*',	None ),	# Shift+8
	357: ( Qt.Key_ParenLeft,	'(',	None ),	# Shift+9
	
	365: ( Qt.Key_A,			'A',	None ),
	366: ( Qt.Key_B,			'B',	None ),
	367: ( Qt.Key_C,			'C',	None ),
	368: ( Qt.Key_D,			'D',	None ),
	369: ( Qt.Key_E,			'E',	None ),
	370: ( Qt.Key_F,			'F',	None ),
	371: ( Qt.Key_G,			'G',	None ),
	372: ( Qt.Key_H,			'H',	None ),
	373: ( Qt.Key_I,			'I',	None ),
	374: ( Qt.Key_J,			'J',	None ),
	375: ( Qt.Key_K,			'K',	None ),
	376: ( Qt.Key_L,			'L',	None ),
	377: ( Qt.Key_M,			'M',	None ),
	378: ( Qt.Key_N,			'N',	None ),
	379: ( Qt.Key_O,			'O',	None ),
	380: ( Qt.Key_P,			'P',	None ),
	381: ( Qt.Key_Q,			'Q',	None ),
	382: ( Qt.Key_R,			'R',	None ),
	383: ( Qt.Key_S,			'S',	None ),
	384: ( Qt.Key_T,			'T',	None ),
	385: ( Qt.Key_U,			'U',	None ),
	386: ( Qt.Key_V,			'V',	None ),
	387: ( Qt.Key_W,			'W',	None ),
	388: ( Qt.Key_X,			'X',	None ),
	389: ( Qt.Key_Y,			'Y',	None ),
	390: ( Qt.Key_Z,			'Z',	None ),
	
	486: ( Qt.Key_Colon,		':',	None ), # Shift+;
	487: ( Qt.Key_Plus,			'+',	None ), # Shift++
	488: ( Qt.Key_Less,			'<',	None ), # Shift+,
	489: ( Qt.Key_Underscore,	'_',	None ), # Shift+-
	490: ( Qt.Key_Greater,		'>',	None ),	# Shift+>
	491: ( Qt.Key_Question,		'?',	None ),	# Shift+?
	492: ( Qt.Key_AsciiTilde,	'~',	None ), # Shift+`
	519: ( Qt.Key_BraceLeft,	'{',	None ), # Shift+[
	520: ( Qt.Key_Bar,			'|',	None ), # Shift+\
	521: ( Qt.Key_BraceRight,	'}',	None ),	# Shift+]
	522: ( Qt.Key_QuoteDbl,		'"',	None ), # Shift+'
}

def consumeKey( ctxt, pressed ):
	kcode	= ctxt.GetAttribute( 'KeyCode' )
	mask 	= ctxt.GetAttribute( 'ShiftMask' )
	
	# Build the modifiers
	modifier = Qt.NoModifier
	if ( mask & constants.siShiftMask ):
		if ( kcode + 300 in KEY_MAPPING ):
			kcode 	+= 300
			
		modifier 	|= Qt.ShiftModifier
		
	if ( mask & constants.siCtrlMask ):
		modifier	|= Qt.ControlModifier
	
	if ( mask & constants.siAltMask ):
		modifier 	|= Qt.AltModifier
	
	# Generate a Qt Key Event to be processed
	result 	= KEY_MAPPING.get( kcode )
	
	if ( result ):
		from PyQt4.QtGui		import QApplication, QKeyEvent
		
		if ( pressed ):
			event = QKeyEvent.KeyPress
		else:
			event = QKeyEvent.KeyRelease
		
		if ( result[2] ):
			modifier |= result[2]
		
		# Send the event along to the focused widget
		QApplication.sendEvent( QApplication.focusWidget(), QKeyEvent( event, result[0], modifier, result[1] ) )

#-------------------------------------------------------------------------------------------------------------

def XsiApplication_keyDown_OnEvent( ctxt ):
	import blurdev
	
	# Block XSI keys from processing, pass along to Qt
	if ( not blurdev.core.isKeystrokesEnabled() ):
		consumeKey( ctxt, True )
			
		# Block the Signal from XSI
		ctxt.SetAttribute( 'Consumed', True )

def XsiApplication_keyUp_OnEvent( ctxt ):
	import blurdev
	
	# Block XSI keys from processing, pass along to Qt
	if ( not blurdev.core.isKeystrokesEnabled() ):
		consumeKey( ctxt, False )
		
		# Block the Signal from XSI
		ctxt.SetAttribute( 'Consumed', True )

#-------------------------------------------------------------------------------------------------------------

def XsiApplication_fileExportRequested_OnEvent( ctxt ):
	import blurdev
	blurdev.core.fileExportRequested.emit()
	
def XsiApplication_fileExportFinished_OnEvent( ctxt ):
	import blurdev
	blurdev.core.fileExportFinished.emit()
	
def XsiApplication_fileImportRequested_OnEvent( ctxt ):
	import blurdev
	blurdev.core.fileImportRequested.emit()
	
def XsiApplication_fileImportFinished_OnEvent( ctxt ):
	import blurdev
	blurdev.core.fileImportFinished.emit()
	
def XsiApplication_objectAdded_OnEvent( ctxt ):
	import blurdev
	blurdev.core.objectAdded.emit()
	
def XsiApplication_objectRemoved_OnEvent( ctxt ):
	import blurdev
	blurdev.core.objectRemoved.emit()
	
def XsiApplication_projectChanged_OnEvent( ctxt ):
	import blurdev
	blurdev.core.projectChanged.emit( str( ctxt.GetAttribute( 'NewProjectPath' ) ), str( ctxt.GetAttribute( 'OldProjectPath' ) ) )
	
def XsiApplication_refModelSaved_OnEvent( ctxt ):
	import blurdev
	blurdev.core.refModelSaved.emit()
	
def XsiApplication_refModelLoadRequested_OnEvent( ctxt ):
	import blurdev
	blurdev.core.refModelLoadRequested.emit()
	
def XsiApplication_refModelLoadFinished_OnEvent( ctxt ):
	import blurdev
	blurdev.core.refModelLoadFinished.emit()
	
def XsiApplication_renderFrameRequested_OnEvent( ctxt ):
	import blurdev
	blurdev.core.renderFrameRequested.emit( int( ctxt.GetAttribute( 'RenderType' ) ), str( ctxt.GetAttribute( 'FileName' ) ), int( ctxt.GetAttribute( 'Frame' ) ), int( ctxt.GetAttribute( 'Sequence' ) ), int( ctxt.GetAttribute( 'RenderField' ) ) )
	
def XsiApplication_renderFrameFinished_OnEvent( ctxt ):
	import blurdev
	blurdev.core.renderFrameFinished.emit( int( ctxt.GetAttribute( 'RenderType' ) ), str( ctxt.GetAttribute( 'FileName' ) ), int( ctxt.GetAttribute( 'Frame' ) ), int( ctxt.GetAttribute( 'Sequence' ) ), int( ctxt.GetAttribute( 'RenderField' ) ) )
	
def XsiApplication_sceneClosed_OnEvent( ctxt ):
	import blurdev
	blurdev.core.sceneClosed.emit()
	
def XsiApplication_sceneNewRequested_OnEvent( ctxt ):
	import blurdev
	blurdev.core.sceneNewRequested.emit()
	
def XsiApplication_sceneNewFinished_OnEvent( ctxt ):
	import blurdev
	blurdev.core.sceneNewFinished.emit()
	
def XsiApplication_sceneOpenRequested_OnEvent( ctxt ):
	import blurdev
	blurdev.core.sceneOpenRequested.emit( str( ctxt.GetAttribute( 'FileName' ) ) )
	
def XsiApplication_sceneOpenFinished_OnEvent( ctxt ):
	import blurdev
	blurdev.core.sceneOpenFinished.emit( str( ctxt.GetAttribute( 'FileName' ) ) )
	
def XsiApplication_sceneSaveRequested_OnEvent( ctxt ):
	import blurdev
	blurdev.core.sceneSaveRequested.emit()
	
def XsiApplication_sceneSaveFinished_OnEvent( ctxt ):
	import blurdev
	blurdev.core.sceneSaveFinished.emit()
	
def XsiApplication_sceneSaveAsRequested_OnEvent( ctxt ):
	import blurdev
	blurdev.core.sceneSaveAsRequested.emit( str( ctxt.GetAttribute( 'FileName' ) ) )
	
def XsiApplication_sceneSaveAsFinished_OnEvent( ctxt ):
	import blurdev
	blurdev.core.sceneSaveAsFinished.emit( str( ctxt.GetAttribute( 'FileName' ) ) )
	
def XsiApplication_selectionChanged_OnEvent( ctxt ):
	import blurdev
	# Send different signals based on this
	# int( ctxt.GetAttribute( 'ChangeType' )
	blurdev.core.selectionChanged.emit()
	
def XsiApplication_sequenceRenderRequested_OnEvent( ctxt ):
	import blurdev
	blurdev.core.sequenceRenderRequested.emit( int( ctxt.GetAttribute( 'RenderType' ) ), str( ctxt.GetAttribute( 'FileName' ) ), int( ctxt.GetAttribute( 'Frame' ) ), int( ctxt.GetAttribute( 'Sequence' ) ), int( ctxt.GetAttribute( 'RenderField' ) ) )
	
def XsiApplication_sequenceRenderFinished_OnEvent( ctxt ):
	import blurdev
	blurdev.core.sequenceRenderFinished.emit( int( ctxt.GetAttribute( 'RenderType' ) ), str( ctxt.GetAttribute( 'FileName' ) ), int( ctxt.GetAttribute( 'Frame' ) ), int( ctxt.GetAttribute( 'Sequence' ) ), int( ctxt.GetAttribute( 'RenderField' ) ) )
	
def XsiApplication_timeChanged_OnEvent( ctxt ):
	import blurdev
	blurdev.core.currentFrameChanged.emit( int( ctxt.GetAttribute( 'Frame' ) ) )
	
def XsiApplication_valueChanged_OnEvent( ctxt ):
	import blurdev
	blurdev.core.valueChanged.emit( str( ctxt.GetAttribute( 'Object' ) ), str( ctxt.GetAttribute( 'fullName' ) ), str( ctxt.GetAttribute( 'PreviousValue' ) ) )

#-------------------------------------------------------------------------------------------------------------

# Initialize the Python menu
def Python_Eval( ctxt ):
	item = ctxt.Source
	
	if ( item.name == 'Treegrunt' ):
		import blurdev
		blurdev.core.showTreegrunt()
	
	elif ( item.name == 'New Script' ):
		import blurdev
		blurdev.core.newScript()
		
	elif ( item.name == 'Open Script' ):
		import blurdev
		blurdev.core.openScript()
		
	elif ( item.name == 'Run Script' ):
		import blurdev
		blurdev.core.runScript()
		
	elif ( item.name == 'Python Logger' ):
		import blurdev
		blurdev.core.showLogger()
	
def Python_Init( ctxt ):
	menu = ctxt.Source
	
	# Add Menu Items
	menu.AddCallbackItem( 'Treegrunt',		'Python_Eval' )
	menu.AddSeparatorItem()
	menu.AddCallbackItem( 'New Script',		'Python_Eval' )
	menu.AddCallbackItem( 'Open Script',	'Python_Eval' )
	menu.AddCallbackItem( 'Run Script',		'Python_Eval' )
	menu.AddSeparatorItem()
	menu.AddCallbackItem( 'Python Logger',	'Python_Eval' )

def XSILoadPlugin( reg ):
	reg.author 	= 'Blur Studio'
	reg.name 	= 'Blur QXsi'
	reg.email	= 'beta@blur.com'
	reg.url		= 'www.blur.com'
	reg.major	= 1
	reg.minor	= 0
	
	# Register signals
#	reg.RegisterEvent( 'XsiApplication_fileExportRequested',		constants.siOnBeginFileExport )
#	reg.RegisterEvent( 'XsiApplication_fileExportFinished',			constants.siOnEndFileExport )
#	reg.RegisterEvent( 'XsiApplication_fileImportRequested',		constants.siOnBeginFileImport )
#	reg.RegisterEvent( 'XsiApplication_fileImportFinished',			constants.siOnEndFileImport )
#	reg.RegisterEvent( 'XsiApplication_objectAdded',				constants.siOnObjectAdded )
#	reg.RegisterEvent( 'XsiApplication_objectRemoved',				constants.siOnObjectRemoved )
#	reg.RegisterEvent( 'XsiApplication_projectChanged',				constants.siOnChangeProject )
#	reg.RegisterEvent( 'XsiApplication_refModelSaved',				constants.siOnRefModelModSave )
#	reg.RegisterEvent( 'XsiApplication_refModelLoadRequested',		constants.siOnBeginRefModelModLoad )
#	reg.RegisterEvent( 'XsiApplication_refModelLoadFinished',		constants.siOnEndRefModelModLoad )
#	reg.RegisterEvent( 'XsiApplication_renderFrameRequested',		constants.siOnBeginFrame )
#	reg.RegisterEvent( 'XsiApplication_renderFrameFinished',		constants.siOnEndFrame )
#	reg.RegisterEvent( 'XsiApplication_sceneClosed',				constants.siOnCloseScene )
#	reg.RegisterEvent( 'XsiApplication_sceneNewRequested',			constants.siOnBeginNewScene )
#	reg.RegisterEvent( 'XsiApplication_sceneNewFinished',			constants.siOnEndNewScene )
#	reg.RegisterEvent( 'XsiApplication_sceneOpenRequested',			constants.siOnBeginSceneOpen )
#	reg.RegisterEvent( 'XsiApplication_sceneOpenFinished',			constants.siOnEndSceneOpen )
#	reg.RegisterEvent( 'XsiApplication_sceneSaveRequested',			constants.siOnBeginSceneSave )
#	reg.RegisterEvent( 'XsiApplication_sceneSaveFinished',			constants.siOnEndSceneSave )
#	reg.RegisterEvent( 'XsiApplication_sceneSaveAsRequested',		constants.siOnBeginSceneSaveAs )
#	reg.RegisterEvent( 'XsiApplication_sceneSaveAsFinished',		constants.siOnEndSceneSaveAs )
#	reg.RegisterEvent( 'XsiApplication_selectionChanged',			constants.siOnSelectionChange )
#	reg.RegisterEvent( 'XsiApplication_sequenceRenderRequested',	constants.siOnBeginSequence )
#	reg.RegisterEvent( 'XsiApplication_sequenceRenderFinished',		constants.siOnEndSequence )
#	reg.RegisterEvent( 'XsiApplication_timeChanged',				constants.siOnTimeChange )
#	reg.RegisterEvent( 'XsiApplication_valueChanged',				constants.siOnValueChange )
	
	# Keystroke Blocker
	reg.RegisterEvent( 'XsiApplication_keyUp',						constants.siOnKeyUp )
	reg.RegisterEvent( 'XsiApplication_keyDown',					constants.siOnKeyDown )
	
	# Register menu
	reg.RegisterMenu( constants.siMenuMainTopLevelID, 	'Python' )
	
	return True

def XSIUnloadPlugin( reg ):
	pass
