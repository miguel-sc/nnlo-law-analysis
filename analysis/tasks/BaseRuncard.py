# -*- coding: utf-8 -*-

from analysis.framework import Task

class BaseRuncard(Task):

  def output(self):
    return self.remote_target('{}.run'.format(self.name))

  def run(self):
    with open('{}.run'.format(self.name), 'r') as infile:
      with self.output().open('w') as outfile:
        outfile.write(infile.read())

