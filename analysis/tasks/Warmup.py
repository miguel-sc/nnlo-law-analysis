# -*- coding: utf-8 -*-

import law
import luigi
import os
import shutil
import re
from fnmatch import fnmatch
from subprocess import PIPE
from law.util import interruptable_popen

from BaseRuncard import BaseRuncard
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

  def workflow_requires(self):
    return {
      'baseruncard': BaseRuncard()
    }

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
    dirpath = 'tmpdir' + self.branch_data['seed']
    os.mkdir(dirpath)
    prevdir = os.getcwd()
    os.chdir(dirpath)

    self.output().parent.touch()

    with open('tmp.run', 'w') as outfile:
      outfile.write(self.input().load(formatter='text'))

    os.environ['OMP_NUM_THREADS'] = self.htcondor_request_cpus

    outfile = os.path.basename(self.output().path)
    parts = outfile.split('.')
    parts.pop()
    parts.pop()
    parts.append('log')
    logfile = '.'.join(parts)

    code, out, error = interruptable_popen(['NNLOJET', '-run', 'tmp.run'],stdout=PIPE, stderr=PIPE)
    with open(logfile, 'w') as outfile:
      outfile.write(out)
    if (code != 0):
      raise Exception(error + 'NNLOJET returned non-zero exit status {}'.format(code))

    tarfilter = lambda n : n if fnmatch(n.name, '*{}*'.format(self.branch_data['channel'])) else None
    self.output().dump(os.getcwd(), filter=tarfilter)

    os.chdir(prevdir)
    shutil.rmtree(dirpath)

