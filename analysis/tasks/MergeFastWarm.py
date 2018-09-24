# -*- coding: utf-8 -*-

import luigi
import six
import os
import shutil
from fnmatch import fnmatch

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
      os.system('fnlo-add-warmup_v23.pl -d -v 2.4 -w . -o {proc}.{obs}.wrm {obs} | tee {proc}.{obs}.addwarmup.log'.format(proc = self.process, obs = obs))

    tarfilter = lambda n : n if (fnmatch(n.name, '{}.*.wrm'.format(self.process)) or fnmatch(n.name, '*.log')) else None
    self.output().dump(os.getcwd(), filter=tarfilter)

    os.chdir(prevdir)
    shutil.rmtree('tmpdir')

