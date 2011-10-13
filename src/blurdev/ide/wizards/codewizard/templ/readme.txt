The folders that could have been created for this BlurDev code Language are:

apps/		Contains source code for installed & compiled applications
lib/		Contains source code for commonly used library methods and files
plugins/	Contains source code for compiled & installed application extensions
scripts/	Contains source code for simple scripted utilties
tools/		Contains source code for BlurDev Tool scripts

Most of these definitions can be what you wish, however, the tools/ folder must
follow the BlurDev Tool system for it to properly work with the Treegrunt utility.


There are 2 types of folders in the tools/ folder tree hierarchy - Categories, and Tools

A tool is simply defined as a folder that contains a __meta__.xml file in it, such as:

[language]/tools/MyTool/__meta__.xml

The __meta__.xml file contains registration information about the tool - its main file, its help info, etc.
We chose an xml registration system to support all coding languages generically - as long as the system
can run the script file, then it doesn't matter what language its written in for the Tools system

Categories are simply folders that do not contain a __meta__.xml file.  While there is no naming convention
enforced for Categories programmatically, we recommend starting categories with an underscore to easily see
what folder is a tool, and what folder is a category.

For instance:

[language]/tools/_Animation_Tools/PastePose/
[language]/tools/_Animation_Tools/CopyPose/
[language]/tools/_Animation_Tools/_Caching/SaveCache/
[language]/tools/_Animation_Tools/_Caching/LoadCache/

would be visible as:

+ Animation Tools
+ --- Caching
+ ------ SaveCache
+ ------ LoadCache
+ --- PastePose
+ --- CopyPose

as the Treegrunt Category hierarchy