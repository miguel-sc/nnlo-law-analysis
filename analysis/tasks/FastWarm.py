# -*- coding: utf-8 -*-

import law
import luigi
import glob
import os
import shutil
from fnmatch import fnmatch
from subprocess import PIPE
from law.util import interruptable_popen

from util import createRuncard

from BaseRuncard import BaseRuncard
from Warmup import Warmup
from Steeringfiles import Steeringfiles

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

  def workflow_requires(self):
    return {
      'warmup': Warmup(),
      'baseruncard': BaseRuncard(),
      'steeringfiles': Steeringfiles()
    }

  def requires(self):
    return {
      'warmup': Warmup(branch = self.branch_data['index']),
      'steeringfiles': Steeringfiles(),
      'baseruncard': BaseRuncard()
    }

  def output(self):
    return self.remote_target('{}.{}.{}.fastwarm.s{}.tar.gz'.format(self.process, self.branch_data['channel'], self.name, self.branch_data['seed']))

  def run(self):
    dirpath = 'tmpdir' + self.branch_data['seed']
    prevdir = os.getcwd()

    try:
      os.mkdir(dirpath)
      os.chdir(dirpath)

      self.output().parent.touch()

      self.input()['warmup'].load('')
      self.input()['steeringfiles'].load('')

      outfile = os.path.basename(self.output().path)
      parts = outfile.split('.')
      parts.pop()
      parts.pop()
      parts.append('log')
      logfile = '.'.join(parts)
      parts.pop()
      parts.append('run')
      runcardfile = '.'.join(parts)

      with open(runcardfile, 'w') as outfile:
        baseRuncard = self.input()['baseruncard'].load(formatter='text')
        runcard = createRuncard(baseRuncard, {
          'channel': self.branch_data['channel'],
          'events': self.branch_data['events'],
          'seed': self.branch_data['seed'],
          'iterations': '1',
          'warmup': 'false',
          'production': 'true',
          'unit_phase': 'UNIT_PHASE'
        })
        outfile.write(runcard)

      code, out, error = interruptable_popen(['NNLOJET', '-run', runcardfile],stdout=PIPE, stderr=PIPE)
      with open(logfile, 'w') as outfile:
        outfile.write(out)
      if (code != 0):
        raise Exception(error + 'NNLOJET returned non-zero exit status {}'.format(code))

      for file in glob.glob('*.wrm'):
        os.rename(file, self.branch_data['seed'] + '.' + file)

      tarfilter = lambda n : n if (fnmatch(n.name, '*.wrm') or fnmatch(n.name, logfile) or fnmatch(n.name, runcardfile)) else None
      self.output().dump(os.getcwd(), filter=tarfilter)

    finally:
      os.chdir(prevdir)
      shutil.rmtree(dirpath)

