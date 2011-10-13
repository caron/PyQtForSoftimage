##
#	\author		eric@blur.com
#	\author		Blur Studio
#	\date		03/01/11
#

The Blur Tools Environment system allows us to organize and distribute tools easily throughout the studio, using 1 main tool (the Treegrunt) to house and manage all other tools.

The system works as a standalone utility, as well as inside of 3dsMax, Softimage, and Motion Builder - but can easily be adapted for any application that runs Python.

The folders that have been created for the environment are:

[environment]/
	appdata/					Used for storing custom information for an individual application such as 3dsMax or Softimage (preferences, etc.)
	bin/							Used for storing compiled applications and DLLs for distribution
	code/						Contains all the source code for the environment, broken down by language.  Use the BlurDev >> Code Wizard to add new languages to your environment
	docs/						Additional documentation for developers
	resource/				Additional files that need to be accessed by multiple applications or tools
	workgroups/			Defines a location for creating and distributing Softimage workgroups
	
The only folder that you really "need" for the environment/Treegrunt system to work is the code/ folder, the other folders can be added or removed as needed.