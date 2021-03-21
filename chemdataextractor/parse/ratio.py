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


from chemdataextractor.parse.cem import cem, chemical_label, lenient_chemical_label, solvent_name
from ..utils import first
from ..model import Compound, RatioOf
from .actions import merge, join
from .base import BaseParser
from .elements import W, I, R, Optional, Any, OneOrMore, Not, ZeroOrMore
from chemdataextractor.model import BaseModel, StringType, ListType, ModelType

log = logging.getLogger(__name__)

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
