# -*- coding: utf-8 -*-

import luigi
import glob
import os
import shutil

from FastWarm import FastWarm

from analysis.framework import Task

class MergeFastWarm(Task):

  merge_dir = luigi.Parameter()

  def requires(self):
    return FastWarm(name = self.name)

  def output(self):
    return self.remote_target('{}_MergedFastWarm.tar.gz'.format(self.name))

  def run(self):
    os.mkdir(self.merge_dir + '/tmpdir')
    prevdir = os.getcwd()
    os.chdir(self.merge_dir)

    self.output().parent.touch()

    inputs = self.input()['collection'].targets
    for inp in six.itervalues(inputs):
      name = os.path.basename(inp.path)
      with inp.open('r') as infile:
        with open(name, 'w') as outfile:
          outfile.write(infile.read())
      os.system('tar -xzvf ' + name)
      os.system('rm ' + name)

    tablenames = []
    for file in glob.glob('*.wrm'):
      fileparts = file.split('.')
      obs = fileparts[3]
      scen = fileparts[1]
      if obs not in tablenames:
        tablenames.append(obs)

    for obs in tablenames:
      os.system('perl $ANALYSIS_PATH/scripts/fnlo-add-warmup.pl -v 2.4 -w . -o ' + scen + '.' + obs + '.wrm ' + scen + ' ' + obs)

    os.system('tar -czf tmp.tar.gz ' + scen + '.*')

    with open('tmp.tar.gz') as infile:
      with self.output().open('w') as outfile:
        outfile.write(infile.read())

    os.chdir(prevdir)
    shutil.rmtree(self.merge_dir + '/tmpdir')

