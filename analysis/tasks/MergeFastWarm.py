# -*- coding: utf-8 -*-

import luigi
import six
import os
import shutil
from fnmatch import fnmatch
from subprocess import PIPE
from law.util import interruptable_popen

from FastWarm import FastWarm

from analysis.framework import Task

class MergeFastWarm(Task):

  merge_dir = luigi.Parameter()
  process = luigi.Parameter()
  observables = luigi.ListParameter()

  def requires(self):
    return FastWarm()

  def output(self):
    return self.remote_target('{}.{}.fastwarm.tar.gz'.format(self.process, self.name))

  def run(self):
    os.mkdir('tmpdir')
    prevdir = os.getcwd()
    os.chdir('tmpdir')

    self.output().parent.touch()

    inputs = self.input()['collection'].targets
    for inp in six.itervalues(inputs):
      try:
        inp.load('')
      except:
        print 'file does not exist'

    os.system('rm *.log')
   
    for obs in self.observables:
      table = '{}.{}.wrm'.format(self.process, obs)
      logfile = '{}.{}.addwarmup.log'.format(self.process, obs)
      code, out, error = interruptable_popen(['fnlo-add-warmup_v23.pl', '-d', '-v', '2.4', '-w', '.', '-o', table, obs],stdout=PIPE, stderr=PIPE)
      with open(logfile, 'w') as outfile:
        outfile.write(out)
      if (code != 0):
        raise Exception(error + 'fnlo-add-warmup returned non-zero exit status {}'.format(code))

    tarfilter = lambda n : n if (fnmatch(n.name, '{}.*.wrm'.format(self.process)) or fnmatch(n.name, '*.log')) else None
    self.output().dump(os.getcwd(), filter=tarfilter)

    os.chdir(prevdir)
    shutil.rmtree('tmpdir')

