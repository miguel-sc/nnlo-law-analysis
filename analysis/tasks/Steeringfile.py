# -*- coding: utf-8 -*-

import luigi

from BaseSteeringfile import BaseSteeringfile

from analysis.framework import Task

class Steeringfile(Task):

  def requires(self):
    return BaseSteeringfile()

  def output(self):
    return self.remote_target('{}.{}.str'.format(self.process, self.name))

  def run(self):
    with self.input().open('r') as infile:
      with self.output().open('w') as outfile:
        outfile.write(infile.read())

