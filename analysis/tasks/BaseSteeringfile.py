# -*- coding: utf-8 -*-

import law
import luigi

from analysis.framework import Task

class BaseSteeringfile(Task):

  steering_name = luigi.Parameter()

  def output(self):
    return law.LocalFileTarget(self.steering_name)

  def run(self):
    return
