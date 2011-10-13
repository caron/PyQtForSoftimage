[templ::py_header]

from trax.api.data import [baseclass]

class [classname]( [baseclass] ):
	""" define the custom methods for the [baseclass] subclasss """
	pass

import trax.api.data
trax.api.data.register( '[baseclass]', [classname] )