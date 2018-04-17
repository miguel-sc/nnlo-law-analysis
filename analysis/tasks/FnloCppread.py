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
  ascode = luigi.Parameter()

  def create_branch_map(self):
    return MergeFastProd().branch_map

  def requires(self):
    return MergeFastProd(branch = self.branch)

  def output(self):
    table = self.input().path
    parts = table.split('.')
    parts.pop()
    parts.pop()
    output = '.'.join(parts) + '_6.log'
    return law.LocalFileTarget(output)

  def run(self):
    self.output().parent.touch()
    
    table = self.input().path
    parts = os.path.basename(table).split('.')

    for table in glob.glob(self.merge_dir + '/' + self.name + '/' + parts[0] + '/*' + parts[1] + '*.tab.gz'):
      parts = table.split('.')
      parts.pop()
      parts.pop()
      logfile = '.'.join(parts)

      os.system('fnlo-tk-cppread {} {} 1 {} | tee {}_0.log'.format(table, self.pdf, self.ascode, logfile))
      os.system('fnlo-tk-cppread {} {} -6 {} | tee {}_6.log'.format(table, self.pdf, self.ascode, logfile))

    table = self.input().path
    parts = table.split('.')
    parts.pop()
    parts.pop()
    logfile = '.'.join(parts)

    os.system('fnlo-tk-cppread {} {} 1 {} | tee {}_0.log'.format(table, self.pdf, self.ascode, logfile))
    os.system('fnlo-tk-cppread {} {} -6 {} | tee {}_6.log'.format(table, self.pdf, self.ascode, logfile))

