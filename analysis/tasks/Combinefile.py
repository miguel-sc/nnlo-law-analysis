# -*- coding: utf-8 -*-

import law
import luigi

from analysis.framework import Task

class Combinefile(Task):

  combine_ini = luigi.Parameter()

  def output(self):
    return law.LocalFileTarget(self.combine_ini)

  def run(self):
    return
