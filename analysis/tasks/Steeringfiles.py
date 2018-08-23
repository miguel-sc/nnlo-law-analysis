# -*- coding: utf-8 -*-

import luigi
from fnmatch import fnmatch

from analysis.framework import Task

class Steeringfiles(Task):

  source_path = luigi.Parameter()

  def run(self):
    tarfilter = lambda n : n if fnmatch(n.name, '*.str') else None
    self.output().dump(self.source_path, filter=tarfilter)

  def output(self):
    return self.remote_target('{}.{}.str.tar.gz'.format(self.process, self.name))

