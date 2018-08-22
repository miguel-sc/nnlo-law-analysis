# -*- coding: utf-8 -*-

import luigi

from analysis.framework import Task

class Steeringfiles(Task):

  source_path = luigi.Parameter()

  def run(self):
    self.output().dump(self.source_path, formatter='tar')

  def output(self):
    return self.remote_target('{}.{}.str.tar.gz'.format(self.process, self.name))

