# -*- coding: utf-8 -*-

import law
import luigi
import os
import glob

from Combine import Combine
from FnloCppread import FnloCppread

from analysis.framework import Task

class Approxtest(Task, law.LocalWorkflow):

  merge_dir = luigi.Parameter()
  channels = luigi.Parameter()
  plots_dir = luigi.Parameter()
  observables = luigi.ListParameter()
  fscl = luigi.Parameter()

  def create_branch_map(self):
    branchmap = {}
    i = 0
    for channel in self.channels.split(' '):
      for observable in self.observables:
        branchmap[i] = {
       	  'channel': channel,
          'observable': observable
        }
        i += 1
    return branchmap

  def workflow_requires(self):
    return {
      'combine': Combine(),
      'fnlocppread': FnloCppread()
    }

  def output(self):
    return law.LocalDirectoryTarget('{}/{}/Approxtest/{}/{}'.format(self.plots_dir, self.name, self.branch_data['channel'], self.branch_data['observable']))

  def run(self):
    self.output().touch()

    weightfile = '{}/{}/Combined/Final/{}.{}.APPLfast.txt'.format(self.merge_dir, self.name, self.branch_data['channel'], self.branch_data['observable'])
    datfile = glob.glob('{}/{}/{}/*{}*.dat'.format(self.merge_dir, self.name, self.branch_data['channel'], self.branch_data['observable']))[0]
    outfile = '{}/{}.{}.{}'.format(self.output().path, self.process, self.branch_data['channel'], self.branch_data['observable'])

    os.system('fastnnlo_approxtest_v2.py -d {} -w {} -f {} -o {}'.format(datfile, weightfile, self.fscl, outfile))

