# -*- coding: utf-8 -*-

import law
import luigi
import glob
import os
import shutil

from BaseRuncard import BaseRuncard
from Runcard import Runcard
from Warmup import Warmup
from Steeringfile import Steeringfile

from analysis.framework import Task, HTCondorWorkflow

class FastWarm(Task, HTCondorWorkflow, law.LocalWorkflow):

  fastwarm_events = luigi.Parameter()
  process = luigi.Parameter()
  channels = luigi.Parameter()
  fastwarm_jobs = luigi.Parameter()
  starting_seeds = luigi.Parameter()

  def create_branch_map(self):
    i = 0
    branchmap = {}
    for j, channel in enumerate(self.channels.split(' ')):
      for k in xrange(int(self.fastwarm_jobs.split(' ')[j])):
        branchmap[i] = {
          'index': j,
          'channel': channel,
          'events': self.fastwarm_events.split(' ')[j],
          'seed': str(k + int(self.starting_seeds.split(' ')[j]))
        }
        i += 1
    return branchmap

  def htcondor_workflow_requires(self):
    return {
      'warmup': Warmup(),
      'baseruncard': BaseRuncard(),
      'steeringfile': Steeringfile()
    }

  def requires(self):
    return {
      'warmup': Warmup(branch = self.branch_data['index']),
      'steeringfile': Steeringfile(),
      'runcard': Runcard(
        channel = self.branch_data['channel'],
        events = self.branch_data['events'],
        seed = self.branch_data['seed'],
        iterations = '1',
        warmup = 'false',
        production = 'true',
        unit_phase = 'UNIT_PHASE'
      )
    }

  def output(self):
    return self.remote_target('{}.{}.{}.fastwarm.s{}.tar.gz'.format(self.process, self.branch_data['channel'], self.name, self.branch_data['seed']))

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

    outfile = os.path.basename(self.output().path)
    parts = outfile.split('.')
    parts.pop()
    parts.pop()
    parts.append('log')
    logfile = '.'.join(parts)

    os.system('NNLOJET -run tmp.run | tee {}'.format(logfile))

    for file in glob.glob('*.wrm'):
      os.rename(file, self.branch_data['seed'] + '.' + file)

    os.system('tar -czf tmp.tar.gz *.wrm {}'.format(logfile))

    with open('tmp.tar.gz') as infile:
      with self.output().open('w') as outfile:
        outfile.write(infile.read())

    os.chdir(prevdir)
    shutil.rmtree(dirpath)

