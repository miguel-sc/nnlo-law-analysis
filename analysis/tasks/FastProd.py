# -*- coding: utf-8 -*-

import law
import luigi
import os
import shutil

from law.contrib.htcondor.job import HTCondorJobManager

from BaseRuncard import BaseRuncard
from Runcard import Runcard
from Warmup import Warmup
from MergeFastWarm import MergeFastWarm
from Steeringfile import Steeringfile

from analysis.framework import Task, HTCondorWorkflow

class FastProd(Task, HTCondorWorkflow, law.LocalWorkflow):

  fastprod_events = luigi.Parameter()
  channels = luigi.Parameter()
  process = luigi.Parameter()
  fastprod_jobs = luigi.Parameter()
  starting_seeds = luigi.Parameter()

  def create_branch_map(self):
    i = 0
    branchmap = {}
    for j, channel in enumerate(self.channels.split(' ')):
      for k in xrange(int(self.fastprod_jobs.split(' ')[j])):
        branchmap[i] = {
          'index': j,
          'channel': channel,
          'events': self.fastprod_events.split(' ')[j],
          'seed': str(k + int(self.starting_seeds.split(' ')[j]))
        }
        i += 1
    return branchmap

  def htcondor_workflow_requires(self):
    return {
      'baseruncard': BaseRuncard(),
      'warmup': Warmup(),
      'fastwarm': MergeFastWarm(),
      'steeringfile': Steeringfile()
   }

  def requires(self):
    return {
      'warmup': Warmup(branch = self.branch_data['index']),
      'fastwarm': MergeFastWarm(),
      'steeringfile': Steeringfile(),
      'runcard': Runcard(
        channel = self.branch_data['channel'],
        events = self.branch_data['events'],
        seed = self.branch_data['seed'],
        iterations = '1',
        warmup = 'false',
        production = 'true',
        unit_phase = ''
      )
    }

  def output(self):
    return self.remote_target('{}.{}.{}.fastprod.s{}.tar.gz'.format(self.process, self.branch_data['channel'], self.name, self.branch_data['seed']))

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

    fastwarm = self.input()['fastwarm']
    with fastwarm.open('r') as infile:
      with open('fastwarm.tar.gz', 'w') as outfile:
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
    os.system('tar -xzvf fastwarm.tar.gz')
    
    outfile = os.path.basename(self.output().path)
    parts = outfile.split('.')
    parts.pop()
    parts.pop()
    parts.append('log')
    logfile = '.'.join(parts)

    os.system('NNLOJET -run tmp.run | tee {}'.format(logfile))

    # for tab in glob.glob('*.tab.gz'):
    #   parts = tab.split('.')
    #   parts[1] = self.channel
    #   del parts[2]
    #   newtab = '.'.join(parts)      
    #   os.rename(tab, newtab)

    os.system('tar -czf tmp.tar.gz *.tab.gz *.dat {}'.format(logfile))

    with open('tmp.tar.gz') as infile:
      with self.output().open('w') as outfile:
        outfile.write(infile.read())

    os.chdir(prevdir)
    shutil.rmtree(dirpath)

