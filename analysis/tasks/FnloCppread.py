# -*- coding: utf-8 -*-

import law
import luigi
import os
import glob

from subprocess import PIPE
from law.util import interruptable_popen

from CopyTables import CopyTables

from analysis.framework import Task

class FnloCppread(Task, law.LocalWorkflow):

  merge_dir = luigi.Parameter()
  pdf = luigi.Parameter()
  scalecombs = luigi.Parameter()
  ascode = luigi.Parameter()
  norm = luigi.Parameter()
  scale = luigi.Parameter()

  def create_branch_map(self):
    return CopyTables().branch_map

  def workflow_requires(self):
    return {
      'copytables': CopyTables()
    }

  def requires(self):
    return CopyTables(branch = self.branch)

  def output(self):
    return self.local_target('{}.{}.s{}.cppread'.format(self.process, self.branch_data['channel'], self.branch_data['seed']))

  def run(self):
    table = self.input().path
    parts = os.path.basename(table).split('.')

    for table in glob.glob(self.merge_dir + '/' + self.name + '/' + self.branch_data['channel'] + '/*.s' + self.branch_data['seed'] + '.tab.gz'):
      parts = table.split('.')
      parts.pop()
      parts.pop()
      parts.append('log')
      logfile = '.'.join(parts)

      code, out, error = interruptable_popen(['fnlo-tk-cppread', table, self.pdf, self.scalecombs, self.ascode, self.norm, self.scale],stdout=PIPE, stderr=PIPE)
      with open(logfile, 'w') as outfile:
        outfile.write(out)
      if (code != 0):
        raise Exception(error + 'fnlo-tk-cppread returned non-zero exit status {}'.format(code))

    self.output().touch()

