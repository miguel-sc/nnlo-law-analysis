# -*- coding: utf-8 -*-

import law
import luigi
import os

from analysis.framework import Task

class BaseSteeringfile(Task):

  def output(self):
    analysis_path = os.environ['ANALYSIS_PATH']
    return law.LocalFileTarget('{}/{}.{}.str'.format(analysis_path, self.process, self.name))

  def run(self):
    return
