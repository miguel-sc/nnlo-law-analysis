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

  def create_branch_map(self):
    branchmap = {}
    for i, channel in enumerate(self.channels.split(' ')):
      branchmap[i] = {
        'channel': channel,
        'events': self.warmup_events.split(' ')[i],
        'iterations': self.warmup_iterations.split(' ')[i],
        'seed': str(i + int(self.starting_seed))
      }
    return branchmap

  def requires(self):
    return Runcard(
      channel = self.branch_data['channel'],
      events = self.branch_data['events'],
      seed = self.branch_data['seed'],
      iterations = self.branch_data['iterations'],
      warmup = 'true',
      production = 'false',
      unit_phase = '')

  def output(self):
    return self.remote_target('{}.{}.{}.warmup.tar.gz'.format(self.process, self.branch_data['channel'], self.name))

  def run(self):
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
    os.system('tar -czf tmp.tar.gz *{}*'.format(self.branch_data['channel']))
    with open('tmp.tar.gz') as infile:
      with self.output().open('w') as outfile:
        data = infile.read()
        outfile.write(data)

    os.chdir(prevdir)
    shutil.rmtree(dirpath)

