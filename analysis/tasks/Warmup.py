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
  warmup_iterations = luigi.Parameter()
  starting_seed = luigi.Parameter()

  def init_branch(self):
    i = self.branch
    self.channel = self.channels.split(' ')[i]
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
      channel = self.channel,
      events = self.events,
      seed = self.seed,
      iterations = self.iterations,
      warmup = 'true',
      production = 'false',
      unit_phase = '')

  def output(self):
    self.init_branch()
    return self.remote_target('{}.{}.{}.warmup.tar.gz'.format(self.process, self.channel, self.name))

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

    outfile = os.path.basename(self.output().path)
    parts = outfile.split('.')
    parts.pop()
    parts.pop()
    parts.append('log')
    logfile = '.'.join(parts)

    os.system('NNLOJET -run ' + name + ' | tee ' + logfile)
    os.system('tar -czf tmp.tar.gz *' + self.channel + '*')
    with open('tmp.tar.gz') as infile:
      with self.output().open('w') as outfile:
        data = infile.read()
        outfile.write(data)

    os.chdir(prevdir)
    shutil.rmtree(dirpath)

