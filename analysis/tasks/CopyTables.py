# -*- coding: utf-8 -*-

import law
import luigi
import os

from FastProd import FastProd

from analysis.framework import Task

class CopyTables(Task, law.LocalWorkflow):

  merge_dir = luigi.Parameter()
  channels = luigi.Parameter()
  regions = luigi.Parameter()

  def __init__(self, *args, **kwargs):
    super(CopyTables, self).__init__(*args, **kwargs)
    self.channels_array = self.channels.split(' ')
    self.regions_array = self.regions.split(' ')

  def create_branch_map(self):
    return FastProd(name = self.name).branch_map

  def requires(self):
    return FastProd(name = self.name, branch = self.branch)

  def output(self):
    if (self.regions_array[self.branch_data] == 'all'):
      region = self.channels_array[self.branch_data]
    else:
      region = self.channels_array[self.branch_data] + self.regions_array[self.branch_data]
    basename = os.path.basename(self.input().path)
    return law.LocalFileTarget('{}/{}/{}/{}'.format(self.merge_dir, self.name, region, basename))

  def run(self):
    self.output().parent.touch()
    with self.input().open('r') as infile:
      with self.output().open('w') as outfile:
        outfile.write(infile.read())
    directory = os.path.dirname(self.output().path)
    os.system('tar -xzvf ' + self.output().path + ' -C ' + directory)

