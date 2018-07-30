# -*- coding: utf-8 -*-

import law
import luigi
import os
import glob

from MergeFastProd import MergeFastProd

from analysis.framework import Task

class FnloCppread(Task, law.LocalWorkflow):

  merge_dir = luigi.Parameter()
  pdf = luigi.Parameter()
  scalecombs = luigi.Parameter()
  ascode = luigi.Parameter()
  norm = luigi.Parameter()
  scale = luigi.Parameter()

  def create_branch_map(self):
    return MergeFastProd().branch_map

  def requires(self):
    return MergeFastProd(branch = self.branch)

  def output(self):
    table = self.input().path
    parts = table.split('.')
    parts.pop()
    parts.pop()
    output = '.'.join(parts) + '.log'
    return law.LocalFileTarget(output)

  def run(self):
    self.output().parent.touch()
    
    table = self.input().path
    parts = os.path.basename(table).split('.')

    for table in glob.glob(self.merge_dir + '/' + self.name + '/' + parts[1] + '/*' + parts[2] + '*.tab.gz'):
      parts = table.split('.')
      parts.pop()
      parts.pop()
      logfile = '.'.join(parts)

      os.system('fnlo-tk-cppread {} {} {} {} {} {} | tee {}.log'.format(table, self.pdf, self.scalecombs, self.ascode, self.norm, self.scale, logfile))

    table = self.input().path
    parts = table.split('.')
    parts.pop()
    parts.pop()
    logfile = '.'.join(parts)

    os.system('fnlo-tk-cppread {} {} {} {} {} {} | tee {}.log'.format(table, self.pdf, self.scalecombs, self.ascode, self.norm, self.scale, logfile))

