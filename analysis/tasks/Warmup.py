# -*- coding: utf-8 -*-

import law
import luigi
import os
import shutil

from Runcard import Runcard

from analysis.framework import Task, HTCondorWorkflow


class Warmup(Task, HTCondorWorkflow, law.LocalWorkflow):

  warmup_events = luigi.Parameter()
  channels = luigi.Parameter()
  regions = luigi.Parameter()
  warmup_iterations = luigi.Parameter()
  starting_seed = luigi.Parameter()

  def init_branch(self):
    i = self.branch
    self.channel = self.channels.split(' ')[i]
    self.region = self.regions.split(' ')[i]
    self.events = self.warmup_events.split(' ')[i]
    self.iterations = self.warmup_iterations.split(' ')[i]
    self.seed = str(self.branch + int(self.starting_seed))

  def create_branch_map(self):
    branchmap = {}
    for i, channel in enumerate(self.channels.split(' ')):
      branchmap[i] = i
    return branchmap

  def requires(self):
    self.init_branch()
    return Runcard(
      name = self.name,
      channel = self.channel,
      region = self.region,
      events = self.events,
      seed = self.seed,
      iterations = self.iterations,
      warmup = 'true',
      production = 'false',
      unit_phase = '')

  def output(self):
    self.init_branch()
    if (self.region == 'all'):
      region = ''
    else:
      region = self.region
    return self.remote_target('{}_Warmup_{}.tar.gz'.format(self.name, self.channel + region))

  def run(self):
    self.init_branch()
    dirpath = 'tmpdir'
    os.mkdir(dirpath)
    prevdir = os.getcwd()
    os.chdir(dirpath)

    self.output().parent.touch()
    name = os.path.basename(self.input().path)
    with self.input().open('r') as infile:
      with open(name, 'w') as outfile:
        outfile.write(infile.read())

    os.environ['OMP_NUM_THREADS'] = self.htcondor_request_cpus

    os.system('NNLOJET -run ' + name)
    os.system('tar -czf tmp.tar.gz *' + self.channel + '*')
    with open('tmp.tar.gz') as infile:
      with self.output().open('w') as outfile:
        data = infile.read()
        outfile.write(data)

    os.chdir(prevdir)
    shutil.rmtree(dirpath)

