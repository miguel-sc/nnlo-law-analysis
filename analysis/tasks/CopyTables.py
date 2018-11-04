# -*- coding: utf-8 -*-

import law
import luigi
import os
from law.util import interruptable_popen
from subprocess import PIPE

from FastProd import FastProd

from analysis.framework import Task

class CopyTables(Task, law.LocalWorkflow):

  merge_dir = luigi.Parameter()
  channels = luigi.Parameter()

  def create_branch_map(self):
    return FastProd().branch_map

  def workflow_requires(self):
    return {
      "fastprod": FastProd()
    }

  def output(self):
    basename = os.path.basename(FastProd(branch = self.branch).output().path)
    parts = basename.split('.')
    parts.pop()
    parts.pop()
    parts.append('log')
    outfile = '.'.join(parts)
    return law.LocalFileTarget('{}/{}/{}/{}'.format(self.merge_dir, self.name, self.branch_data['channel'], outfile))

  def run(self):
    self.output().parent.touch()
    prevdir = os.getcwd()
    os.chdir(self.output().parent.path)
    FastProd(branch = self.branch).output().load('')
    os.chdir(prevdir)
