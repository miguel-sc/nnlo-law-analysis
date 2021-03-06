# -*- coding: utf-8 -*-

import luigi
import law

from SingleScalecheck import SingleScalecheck
from Absolute import Absolute
from AbsoluteAll import AbsoluteAll
from Approxtest import Approxtest

class AllPlots(law.WrapperTask):

  def requires(self):
    return {
      'singlescalecheck': SingleScalecheck(),
      'absolute': Absolute(),
      'absoluteall': AbsoluteAll(),
      'approxtest': Approxtest()
    }
