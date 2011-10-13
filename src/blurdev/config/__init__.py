##
#	\namespace	blurdev.config
#
#	\remarks	Creates a configuration module for the blurdev system
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		11/19/10
#

from blurdev.configset import ConfigSet

# create the main config set
configSet = ConfigSet()
configSet.loadFrom( __file__, __name__ )