# -*- coding: utf-8 -*-

import law
import luigi
import os
import shutil
import re
import tempfile

from util import createRuncard

from fnmatch import fnmatch
from subprocess import PIPE
from law.util import interruptable_popen

from BaseRuncard import BaseRuncard

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

  def workflow_requires(self):
    return {
      'baseruncard': BaseRuncard()
    }

  def requires(self):
    return BaseRuncard()

  def output(self):
    return self.remote_target('{}.{}.{}.warmup.tar.gz'.format(self.process, self.branch_data['channel'], self.name))

  def run(self):
    dirpath = 'tmpdir' + self.branch_data['seed']
    prevdir = os.getcwd()

    try:
      os.mkdir(dirpath)
      os.chdir(dirpath)

      self.output().parent.touch()

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
        baseRuncard = self.input().load(formatter='text')
        runcard = createRuncard(baseRuncard, {
          'channel': self.branch_data['channel'],
          'events': self.branch_data['events'],
          'seed': self.branch_data['seed'],
          'iterations': self.branch_data['iterations'],
          'warmup': '1',
          'production': '.false.',
          'unit_phase': ''
        })
        outfile.write(runcard)

      os.environ['OMP_NUM_THREADS'] = self.htcondor_request_cpus

      code, out, error = interruptable_popen(['NNLOJET', '-run', runcardfile],stdout=PIPE, stderr=PIPE)
      with open(logfile, 'w') as outfile:
        outfile.write(out)
      if (code != 0):
        raise Exception(error + 'NNLOJET returned non-zero exit status {}'.format(code))

      tarfilter = lambda n : n if fnmatch(n.name, '*{}*'.format(self.branch_data['channel'])) else None
      self.output().dump(os.getcwd(), filter=tarfilter)

    finally:
      os.chdir(prevdir)
      shutil.rmtree(dirpath)

