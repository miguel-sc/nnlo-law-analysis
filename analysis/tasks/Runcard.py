# -*- coding: utf-8 -*-

import luigi

from BaseRuncard import BaseRuncard

from analysis.framework import Task

class Runcard(Task):

  warmup = luigi.Parameter()
  production = luigi.Parameter()
  events = luigi.Parameter()
  process = luigi.Parameter()
  seed = luigi.Parameter()
  iterations = luigi.Parameter()
  channel = luigi.Parameter()
  unit_phase = luigi.Parameter()

  def requires(self):
    return BaseRuncard()

  def output(self):

    if (self.warmup == 'true'):
      subdir = 'Warmup'
    elif (self.unit_phase == ''):
      subdir = 'FastProd'
    else:
      subdir = 'FastWarm'

    filename = '{}/{}.{}.s{}.run'.format(subdir, self.process, self.channel, self.name, self.seed)

    return self.remote_target(filename)

  def run(self):
    self.output().parent.touch()

    if (self.channel == 'RRa'):
      channel = 'RR'
      region = 'a'
    elif (self.channel == 'RRb'):
      channel = 'RR'
      region = 'b'
    else:
      channel = self.channel
      region = 'all'

    substitutions = {
      '@SEED@': self.seed,
      '@WARMUP@': self.warmup,
      '@PRODUCTION@': self.production,
      '@EVENTS@': self.events,
      '@ITERATIONS@': self.iterations,
      '@CHANNEL@': channel,
      '@REGION@': region,
      '@UNIT_PHASE@': self.unit_phase
    }
    with self.input().open('r') as infile:
      with self.output().open('w') as outfile:
        data = infile.read()
        for key, value in substitutions.iteritems():
          data = data.replace(key, value)
        outfile.write(data)
