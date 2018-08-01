# -*- coding: utf-8 -*-

import law
import luigi
import os

from FastProd import FastProd

from analysis.framework import Task

class CopyTables(Task, law.LocalWorkflow):

  merge_dir = luigi.Parameter()
  channels = luigi.Parameter()

  def create_branch_map(self):
    return FastProd().branch_map

  def requires(self):
    return FastProd(branch = self.branch)

  def output(self):
    basename = os.path.basename(self.input().path)
    parts = basename.split('.')
    parts.pop()
    parts.pop()
    parts.append('log')
    outfile = '.'.join(parts)
    return law.LocalFileTarget('{}/{}/{}/{}'.format(self.merge_dir, self.name, self.branch_data['channel'], outfile))

  def run(self):
    self.output().parent.touch()
    basename = os.path.basename(self.input().path)
    tarfile = '{}/{}/{}/{}'.format(self.merge_dir, self.name, self.branch_data['channel'], basename)
    with self.input().open('r') as infile:
      with open(tarfile, 'w') as outfile:
        outfile.write(infile.read())
    basename = os.path.basename(self.input().path)
    directory = os.path.dirname(self.output().path)
    os.system('tar -xzvf ' + tarfile + ' -C ' + directory)
    os.system('rm ' + tarfile)

