# -*- coding: utf-8 -*-

import law
import luigi
import os
from law import util
from subprocess import PIPE

from FnloCppreadFinal import FnloCppreadFinal

from analysis.framework import Task

class AbsoluteAll(Task, law.LocalWorkflow):

  merge_dir = luigi.Parameter()
  plots_dir = luigi.Parameter()
  observables = luigi.ListParameter()

  def create_branch_map(self):
    branchmap = {}
    i = 0
    for observable in self.observables:
      branchmap[i] = {
        'observable': observable
      }
      i += 1
    return branchmap

  def workflow_requires(self):
    return {
      'fnlocppread': FnloCppreadFinal()
    }

  def output(self):
    return law.LocalDirectoryTarget('{}/{}/AbsoluteAll/NNLO/{}'.format(self.plots_dir, self.name, self.branch_data['observable']))

  def run(self):
    try:
      with self.output().temporary_path() as self.temp_output_path:
        os.mkdir(self.temp_output_path)

        datfile1 = '{}/{}/Combined/Final/{}.LO.{}.dat'.format(self.merge_dir, self.name, self.process, self.branch_data['observable'])
        datfile2 = '{}/{}/Combined/Final/{}.NLO.{}.dat'.format(self.merge_dir, self.name, self.process, self.branch_data['observable'])
        datfile3 = '{}/{}/Combined/Final/{}.NNLO.{}.dat'.format(self.merge_dir, self.name, self.process, self.branch_data['observable'])
        logfile = '{}/{}/Combined/Final/{}.NNLO.{}.log'.format(self.merge_dir, self.name, self.process, self.branch_data['observable'])
        outfile = '{}/{}.NNLO.{}'.format(self.temp_output_path, self.process, self.branch_data['observable'])

        code, out, error = util.interruptable_popen(['fastnnlo_absolute_all_v2.py', '-d', datfile1, datfile2, datfile3, '-l', logfile, '-o', outfile],stdout=PIPE, stderr=PIPE)

        if (code != 0):
          raise Exception('{} exitcode: {}'.format(error, code))
    except:
      os.rmdir(self.temp_output_path)
      raise

