# -*- coding: utf-8 -*-

import luigi
import law
import os
import shutil

from MergeFastProd import MergeFastProd

from analysis.framework import Task

class MergeFinal(Task, law.LocalWorkflow):

  merge_dir = luigi.Parameter()
  final_tables = luigi.DictParameter()
  observables = luigi.ListParameter()

  def create_branch_map(self):
    i = 0
    branchmap = {}
    for order, channels in self.final_tables.iteritems():
      for obs in self.observables:
        branchmap[i] = {
          'obs': obs,
          'order': order,
          'channels': channels
        }
        i += 1
    return branchmap

  def workflow_requires(self):
    return {
      'mergefastprod': MergeFastProd()
    }

  def requires(self):
    return MergeFastProd()

  def output(self):
    return law.LocalFileTarget('{}/{}/Combined/Final/{}.{}.{}.tab.gz'.format(self.merge_dir, self.name, self.process, self.branch_data['order'], self.branch_data['obs']))

  def run(self):

    outfile = self.output().path
    parts = outfile.split('.')
    parts.pop()
    parts.pop()
    parts.append('merge2.log')
    logfile = '.'.join(parts)
    
    tablestring = ''
    for channel in self.branch_data['channels']:
      tablestring += '{}/{}/Combined/Final/{}.{}.{}.tab.gz '.format(self.merge_dir, self.name, self.process, channel, self.branch_data['obs'])
    os.system('fnlo-tk-merge2 -add {}{} | tee {}'.format(tablestring, outfile, logfile))

