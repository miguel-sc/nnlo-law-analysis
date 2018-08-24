# -*- coding: utf-8 -*-

import law
import luigi
import os
import glob

from FastProd import FastProd
from FnloCppread import FnloCppread

from analysis.framework import Task

class SingleScalecheck(Task, law.LocalWorkflow):

  merge_dir = luigi.Parameter()
  channels = luigi.Parameter()
  plots_dir = luigi.Parameter()
  observables = luigi.ListParameter()

  def create_branch_map(self):
    branchmap = {}
    i = 0
    for j, channel in enumerate(self.channels.split(' ')):
      for observable in self.observables:
        branchmap[i] = {
       	  'channel': channel,
          'observable': observable,
          'seed': FastProd().starting_seeds.split(' ')[j]
        }
        i += 1
    return branchmap

  def workflow_requires(self):
    return {
      'fnlocppread': FnloCppread()
    }

  def requires(self):
    return FnloCppread()

  def output(self):
    return law.LocalDirectoryTarget('{}/SingleScalecheck/{}/{}'.format(self.plots_dir, self.branch_data['channel'], self.branch_data['observable']))

  def run(self):
    self.output().touch()

    for datfile in glob.glob(self.merge_dir + '/' + self.name + '/' + self.branch_data['channel'] + '/*' + self.branch_data['observable'] + '*' + self.branch_data['seed'] + '*.dat'):
      parts = datfile.split('.')
      parts.pop()
      parts.append('log')
      logfile = '.'.join(parts)

      os.system('fastnnlo_scalecheck_v2.py -d {} -l {} -o {}/{}.{}.{}'.format(datfile, logfile, self.output().path, self.process, self.branch_data['channel'], self.branch_data['observable']))

