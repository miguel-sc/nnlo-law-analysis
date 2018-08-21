# -*- coding: utf-8 -*-

import luigi
import law
import glob
import os
import shutil

from MergeFastProd import MergeFastProd

from analysis.framework import Task

class MergeFinal(Task):

  merge_dir = luigi.Parameter()

  def requires(self):
    return MergeFastProd()

  def output(self):
    return self.local_target('MergeFinal')

  def run(self):

    prevdir = os.getcwd()

    os.chdir('{}/{}/Combined/Final'.format(self.merge_dir, self.name))

    final_tables = {
      'NLO': ['LO', 'R', 'V'],
      'NLO_only': ['R', 'V'],
      'NNLO_only': ['RRa', 'RRb', 'RV', 'VV'],
      'NNLO': ['LO', 'R', 'V', 'RRa', 'RRb', 'RV', 'VV']
    }

    tablenames = []
    for file in glob.glob('*.tab.gz'):
      fileparts = file.split('.')
      obs = fileparts[2]
      if obs not in tablenames:
        tablenames.append(obs)

    
    for order, channels in final_tables.iteritems():
      for obs in tablenames:
        tablestring = ''
        for channel in channels:
          tablestring += '{}.{}.{}.tab.gz '.format(self.process, channel, obs)
        os.system('fnlo-tk-merge2 -add {}{}.{}.{}.tab.gz | tee {}.{}.{}.merge2.log'.format(tablestring, self.process, order, obs, self.process, order, obs))

    os.chdir(prevdir)

    self.output().touch()
