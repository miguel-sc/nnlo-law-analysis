# -*- coding: utf-8 -*-

import luigi
import six
import os
import shutil

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
    os.mkdir(self.merge_dir + '/tmpdir')
    prevdir = os.getcwd()
    os.chdir(self.merge_dir + '/tmpdir')

    self.output().parent.touch()

    inputs = self.input()['collection'].targets
    for inp in six.itervalues(inputs):
      try:
        name = os.path.basename(inp.path)
        with inp.open('r') as infile:
          with open(name, 'w') as outfile:
            outfile.write(infile.read())
        os.system('tar -xzvf ' + name)
        os.system('rm ' + name)
      except:
        print name + ' does not exist'

    os.system('rm *.log')
   
    for obs in self.observables:
      os.system('fnlo-add-warmup_v23.pl -d -v 2.4 -w . -o {proc}.{obs}.wrm {obs} | tee {proc}.{obs}.addwarmup.log'.format(proc = self.process, obs = obs))

    os.system('tar -czf tmp.tar.gz ' + self.process + '.*.wrm *.log')

    with open('tmp.tar.gz') as infile:
      with self.output().open('w') as outfile:
        outfile.write(infile.read())

    os.chdir(prevdir)
    shutil.rmtree(self.merge_dir + '/tmpdir')

