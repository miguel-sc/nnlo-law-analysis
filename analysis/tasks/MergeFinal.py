# -*- coding: utf-8 -*-

import luigi
import law
import os
import shutil

from MergeFastProd import MergeFastProd

from analysis.framework import Task

class MergeFinal(Task):

  merge_dir = luigi.Parameter()
  final_tables = luigi.DictParameter()
  observables = luigi.ListParameter()

  def requires(self):
    return MergeFastProd()

  def output(self):
    return self.local_target('MergeFinal')

  def run(self):

    prevdir = os.getcwd()

    os.chdir('{}/{}/Combined/Final'.format(self.merge_dir, self.name))

    for order, channels in self.final_tables.iteritems():
      for obs in self.observables:
        tablestring = ''
        for channel in channels:
          tablestring += '{}.{}.{}.tab.gz '.format(self.process, channel, obs)
        os.system('fnlo-tk-merge2 -add {}{}.{}.{}.tab.gz | tee {}.{}.{}.merge2.log'.format(tablestring, self.process, order, obs, self.process, order, obs))

    os.chdir(prevdir)

    self.output().touch()
