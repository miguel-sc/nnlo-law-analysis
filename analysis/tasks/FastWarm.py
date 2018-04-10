# -*- coding: utf-8 -*-

import law
import luigi
import glob
import os
import shutil
from Warmup import Warmup
from Steeringfile import Steeringfile

from analysis.framework import Task, HTCondorWorkflow

class FastWarm(Task, HTCondorWorkflow, law.LocalWorkflow):

  fastwarm_events = luigi.Parameter()
  channels = luigi.Parameter()
  regions = luigi.Parameter()
  fastwarm_jobs = luigi.Parameter()
  starting_seed = luigi.Parameter()

  def init_branch(self):
    i = 0
    branchmap = {}
    for j, channel in enumerate(self.channels.split(' ')):
      for k in xrange(int(self.fastwarm_jobs.split(' ')[j])):
        branchmap[i] = j
        i += 1
    i = branchmap[self.branch]
    self.channel = self.channels.split(' ')[i]
    self.region = self.regions.split(' ')[i]
    self.events = self.fastwarm_events.split(' ')[i]
    self.seed = str(self.branch + int(self.starting_seed))
    self.index = i

  def create_branch_map(self):
    i = 0
    branchmap = {}
    for j, channel in enumerate(self.channels.split(' ')):
      for k in xrange(int(self.fastwarm_jobs.split(' ')[j])):
        branchmap[i] = j
        i += 1
    return branchmap

  def htcondor_workflow_requires(self):
    return {
      'warmup': Warmup(name = self.name),
      'steeringfile': Steeringfile(name = self.name)
    }

  def requires(self):
    self.init_branch()
    return {
      'warmup': Warmup(name = self.name, branch = self.index),
      'steeringfile': Steeringfile(name = self.name),
      'runcard': Runcard(
        name = self.name,
        channel = self.channel,
        events = self.events,
        region = self.region,
        seed = self.seed,
        iterations = '1',
        job = str(self.branch),
        warmup = 'false',
        production = 'true',
        unit_phase = 'UNIT_PHASE'
      )
    }

  def output(self):
    self.init_branch()
    if (self.region == 'all'):
      region = ''
    else:
      region = self.region
    return self.remote_target('{}_FastWarm_{}_{}.tar.gz'.format(self.name, self.channel + region, str(self.branch)))

  def run(self):
    dirpath = 'tmpdir'
    os.mkdir(dirpath)
    prevdir = os.getcwd()
    os.chdir(dirpath)

    self.output().parent.touch()

    warmup = self.input()['warmup']
    with warmup.open('r') as infile:
      with open('warmup.tar.gz', 'w') as outfile:
        outfile.write(infile.read())

    runcard = self.input()['runcard']
    with runcard.open('r') as infile:
      with open('tmp.run', 'w') as outfile:
        outfile.write(infile.read())

    steeringfile = self.input()['steeringfile']
    steeringname = os.path.basename(steeringfile.path)
    with steeringfile.open('r') as infile:
      with open(steeringname, 'w') as outfile:
        outfile.write(infile.read())

    os.system('tar -xzvf warmup.tar.gz')
    os.system('NNLOJET -run tmp.run')

    for file in glob.glob('*'):
      os.rename(file, str(self.branch) + '.' + file)

    os.system('tar -czf tmp.tar.gz *.wrm *.log')

    with open('tmp.tar.gz') as infile:
      with self.output().open('w') as outfile:
        outfile.write(infile.read())

    os.chdir(prevdir)
    shutil.rmtree(dirpath)

