# -*- coding: utf-8 -*-

import law
import luigi
import glob
import os

from law import util
from subprocess import PIPE

from Combine import Combine
from FnloCppread import FnloCppread

from analysis.framework import Task

class Approxtest(Task, law.LocalWorkflow):

  merge_dir = luigi.Parameter()
  channels = luigi.Parameter()
  plots_dir = luigi.Parameter()
  observables = luigi.ListParameter()

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
    try:
      with self.output().temporary_path() as self.temp_output_path:
        os.mkdir(self.temp_output_path)

        weightfile = '{}/{}/Combined/Final/{}.{}.APPLfast.txt'.format(self.merge_dir, self.name, self.branch_data['channel'], self.branch_data['observable'])
        datfile = glob.glob('{}/{}/{}/*{}*.dat'.format(self.merge_dir, self.name, self.branch_data['channel'], self.branch_data['observable']))[0]
        outfile = '{}/{}.{}.{}'.format(self.temp_output_path, self.process, self.branch_data['channel'], self.branch_data['observable'])

        code, out, error = util.interruptable_popen(['fastnnlo_approxtest_v2.py', '-v', '-d', datfile, '-w', weightfile, '-o', outfile],stdout=PIPE, stderr=PIPE)
        
        if (code != 0):
          raise Exception('{} exitcode: {}'.format(error, code))
    except:
      os.rmdir(self.temp_output_path)
      raise
