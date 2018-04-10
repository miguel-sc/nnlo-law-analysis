# -*- coding: utf-8 -*-

import luigi

from BaseRuncard import BaseRuncard

from analysis.framework import Task

class Runcard(Task):

  job = luigi.Parameter(default = '-1')
  warmup = luigi.Parameter()
  production = luigi.Parameter()
  events = luigi.Parameter()
  seed = luigi.Parameter()
  iterations = luigi.Parameter()
  channel = luigi.Parameter()
  region = luigi.Parameter()
  unit_phase = luigi.Parameter()

  def requires(self):
    return BaseRuncard(name = self.name)

  def output(self):

    if (self.region == 'all'):
      region = self.channel
    else:
      region = self.channel + self.region

    if (self.warmup == 'true'):
      subdir = 'Warmup'
    elif (self.unit_phase == ''):
      subdir = 'FastProd'
    else:
      subdir = 'FastWarm'

    if (int(self.job) < 0):
      filename = '{}/{}_{}.run'.format(subdir, self.name, region)
    else:
      filename = '{}/{}_{}_{}.run'.format(subdir, self.name, region, self.job)

    return self.remote_target(filename)

  def run(self):
    self.output().parent.touch()
    substitutions = {
      '@SEED@': self.seed,
      '@WARMUP@': self.warmup,
      '@PRODUCTION@': self.production,
      '@EVENTS@': self.events,
      '@ITERATIONS@': self.iterations,
      '@CHANNEL@': self.channel,
      '@REGION@': self.region,
      '@UNIT_PHASE@': self.unit_phase
    }
    with self.input().open('r') as infile:
      with self.output().open('w') as outfile:
        data = infile.read()
        for key, value in substitutions.iteritems():
          data = data.replace(key, value)
        outfile.write(data)
