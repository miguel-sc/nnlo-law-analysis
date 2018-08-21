# -*- coding: utf-8 -*-

import law
import luigi
import os
import glob

from MergeFinal import MergeFinal

from analysis.framework import Task

class FnloCppreadFinal(Task):

  merge_dir = luigi.Parameter()
  pdf = luigi.Parameter()
  scalecombs = luigi.Parameter()
  ascode = luigi.Parameter()
  norm = luigi.Parameter()
  scale = luigi.Parameter()

  def requires(self):
    return MergeFinal()

  def output(self):
    return self.local_target('FnloCppreadFinal')

  def run(self):
    for table in glob.glob(self.merge_dir + '/' + self.name + '/Combined/Final/*.tab.gz'):
      parts = table.split('.')
      parts.pop()
      parts.pop()
      logfile = '.'.join(parts)

      os.system('fnlo-tk-cppread {} {} {} {} {} {} | tee {}.log'.format(table, self.pdf, self.scalecombs, self.ascode, self.norm, self.scale, logfile))

    self.output().touch()

