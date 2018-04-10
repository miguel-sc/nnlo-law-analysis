# -*- coding: utf-8 -*-

import luigi

from BaseSteeringfile import BaseSteeringfile

from analysis.framework import Task

class Steeringfile(Task):

  steering_name = luigi.Parameter()

  def requires(self):
    return BaseSteeringfile(name = self.name, steering_name = self.steering_name)

  def output(self):
    return self.remote_target(self.steering_name)

  def run(self):
    with self.input().open('r') as infile:
      with self.output().open('w') as outfile:
        outfile.write(infile.read())

