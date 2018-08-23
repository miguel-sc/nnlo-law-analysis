# -*- coding: utf-8 -*-

import luigi
import os
import fnmatch

from CopyTables import CopyTables

from analysis.framework import Task

class Combine(Task):

  merge_dir = luigi.Parameter()
  cores = luigi.Parameter()
  combine_ini = luigi.Parameter()

  def requires(self):
    return {
      'tables': CopyTables()
    }

  def output(self):
    return self.local_target('{}.combine.log'.format(self.name))

  def run(self):
    prevdir = os.getcwd()

    self.output().parent.touch()

    os.chdir('{}/{}'.format(self.merge_dir, self.name))

    os.system('nnlojet-combine.py -C {} -j {} | tee tmp.log'.format(self.combine_ini, self.cores))

    for root, dirnames, filenames in os.walk('.'):
      for filename in fnmatch.filter(filenames, '*.APPLfast.txt'):
        parts = filename.split('.')
        if 'cross' not in parts:
          parts.pop()
          parts.pop()
          parts.append('dat')
          parts.insert(0, self.process)
          endfile = '.'.join(parts)
          print endfile
          os.system('nnlojet-combine.py -C {} --APPLfast Combined/Final/{} > Combined/Final/{}'.format(self.combine_ini, filename, endfile))

    with open('tmp.log', 'r') as infile:
      self.output().dump(infile.read(), formatter="text")

    os.system('rm tmp.log')

    os.chdir(prevdir)

