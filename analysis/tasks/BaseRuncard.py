# -*- coding: utf-8 -*-

import os

from analysis.framework import Task

class BaseRuncard(Task):

  def output(self):
    return self.remote_target('{}.{}.run'.format(self.process, self.name))

  def run(self):
    self.output().parent.touch()
    basename = os.path.basename(self.output().path)
    analysis_path = os.environ['ANALYSIS_PATH']
    input_path = '{}/{}'.format(analysis_path, basename)
    with open(basename, 'r') as infile:
      with self.output().open('w') as outfile:
        outfile.write(infile.read())

