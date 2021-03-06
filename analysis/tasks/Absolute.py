# -*- coding: utf-8 -*-

import law
import luigi
import os

from law.util import interruptable_popen
from subprocess import PIPE

from FnloCppreadFinal import FnloCppreadFinal

from analysis.framework import Task

class Absolute(Task, law.LocalWorkflow):

  merge_dir = luigi.Parameter()
  plots_dir = luigi.Parameter()
  channels = luigi.Parameter()
  final_tables = luigi.DictParameter()
  observables = luigi.ListParameter()

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
      'fnlocppread': FnloCppreadFinal()
    }

  def output(self):
    return law.LocalDirectoryTarget('{}/{}/Absolute/{}/{}'.format(self.plots_dir, self.name, self.branch_data['channel'], self.branch_data['observable']))

  def run(self):
    try:
      with self.output().temporary_path() as self.temp_output_path:
        os.mkdir(self.temp_output_path)
     
        datfile = '{}/{}/Combined/Final/{}.{}.{}.dat'.format(self.merge_dir, self.name, self.process, self.branch_data['channel'], self.branch_data['observable'])
        logfile = '{}/{}/Combined/Final/{}.{}.{}.log'.format(self.merge_dir, self.name, self.process, self.branch_data['channel'], self.branch_data['observable']) 
        outfile = '{}/{}.{}.{}'.format(self.temp_output_path, self.process, self.branch_data['channel'], self.branch_data['observable'])
     
        code, out, error = interruptable_popen(['fastnnlo_absolute_v2.py', '-d', datfile, '-l', logfile, '-o', outfile],stdout=PIPE, stderr=PIPE)
      
        if (code != 0):
          raise Exception('{} exitcode: {}'.format(error, code))
    except:
      os.rmdir(self.temp_output_path)
      raise

