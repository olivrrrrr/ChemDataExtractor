"""
chemdataextractor.parse.ratio
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Ratio text parser.

"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import re


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .base import BaseParser
from .elements import W, R, Optional
from ..model import StringType, Compound
from .actions import merge


prefix = (I(u'ratio') | I(u'of') | I(u'and')).hide()

value = R(u'\w+:\w+')(u'value')

ro = (prefix + value)(u'ro')

class RoParser(BaseParser):
    """"""
    root = ro
    
    def __init__(self):
        pass

    def interpret(self, result, start, end):
        compound = Compound(
      
                  value=result.xpath('./text()')
        )

        yield compound
