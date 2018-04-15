# -*- coding: utf-8 -*-

import luigi
import os
import fnmatch

from CopyTables import CopyTables
from Combinefile import Combinefile

from analysis.framework import Task

class Combine(Task):

  merge_dir = luigi.Parameter()
  cores = luigi.Parameter()

  def requires(self):
    return {
      'tables': CopyTables(),
      'combine_ini': Combinefile()
    }

  def output(self):
    return self.remote_target('{}.combine.log'.format(self.name))

  def run(self):
    prevdir = os.getcwd()

    self.output().parent.touch()

    combine_ini = self.input()['combine_ini']
    with combine_ini.open('r') as infile:
      os.chdir(self.merge_dir + '/' + self.name)
      with open('combine.ini', 'w') as outfile:
        outfile.write(infile.read())

    os.system('nnlojet-combine.py -C combine.ini -j {} | tee tmp.log'.format(self.cores))

    for root, dirnames, filenames in os.walk('.'):
      for filename in fnmatch.filter(filenames, '*.APPLfast.txt'):
        filename = os.path.join(root, filename)
        parts = filename.split('.')
        if 'cross' not in parts:
          parts.pop()
          parts.pop()
          parts.append('dat')
          endfile = '.'.join(parts)
          print filename
          print endfile
          parts.pop()
          parts.append('def.dat')
          defdat = '.'.join(parts)
          os.system('mv {} {}'.format(endfile, defdat))
          os.system('nnlojet-combine.py -C combine.ini --APPLfast {} > {}'.format(filename, endfile))

    with open('tmp.log', 'r') as infile:
      with self.output().open('w') as outfile:
        outfile.write(infile.read())

    os.system('rm tmp.log')

    os.chdir(prevdir)

