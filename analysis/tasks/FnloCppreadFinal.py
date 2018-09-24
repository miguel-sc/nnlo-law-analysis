# -*- coding: utf-8 -*-

import law
import luigi
import os
import glob

from subprocess import PIPE
from law.util import interruptable_popen

from MergeFinal import MergeFinal

from analysis.framework import Task

class FnloCppreadFinal(Task, law.LocalWorkflow):

  merge_dir = luigi.Parameter()
  channels = luigi.Parameter()
  final_tables = luigi.DictParameter()
  observables = luigi.ListParameter()

  pdf = luigi.Parameter()
  scalecombs = luigi.Parameter()
  ascode = luigi.Parameter()
  norm = luigi.Parameter()
  scale = luigi.Parameter()

  def create_branch_map(self):
    branchmap = {}
    i = 0
    for observable in self.observables:
      for channel in self.channels.split(' '):
        branchmap[i] = {
          'observable': observable,
          'channel': channel
        }
        i += 1
      for channel in self.final_tables:
        branchmap[i] = {
          'observable': observable,
          'channel': channel
        }
        i += 1
    return branchmap

  def workflow_requires(self):
    return {
      'mergefinal': MergeFinal()
    }

  def requires(self):
    return MergeFinal()

  def output(self):
    return law.LocalFileTarget('{}/{}/Combined/Final/{}.{}.{}.log'.format(self.merge_dir, self.name, self.process, self.branch_data['channel'], self.branch_data['observable']))

  def run(self):
     
    self.output().parent.touch()

    logfile = self.output().path
    parts = logfile.split('.')
    parts.pop()
    parts.append('tab.gz')
    table = '.'.join(parts)

    code, out, error = interruptable_popen(['fnlo-tk-cppread', table, self.pdf, self.scalecombs, self.ascode, self.norm, self.scale],stdout=PIPE, stderr=PIPE)
    with open(logfile, 'w') as outfile:
      outfile.write(out)
    if (code != 0):
      raise Exception(error + 'fnlo-tk-cppread returned non-zero exit status {}'.format(code))

