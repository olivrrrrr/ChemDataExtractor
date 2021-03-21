from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .base import BaseParser
from .elements import W, R, Optional
from ..model import StringType, Compound
from .actions import merge

ratio = R(u'\w+:\w+')(u'value')

class RatioParser(BaseParser):
    """"""
    root = ratio
    
    def __init__(self):
        pass

    def interpret(self, result, start, end):
        c = Compound(
      
                  ratio=result.xpath('./text()')
        )

        yield c
