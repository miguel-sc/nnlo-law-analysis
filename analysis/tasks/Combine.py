# -*- coding: utf-8 -*-

import luigi
import os
import fnmatch

from CopyTables import CopyTables

from analysis.framework import Task

class Combine(Task):

  merge_dir = luigi.Parameter()
  cores = luigi.Parameter()

  def requires(self):
    return {
      'tables': CopyTables(),
    }

  def output(self):
    return self.local_target('{}.combine.log'.format(self.name))

  def run(self):
    prevdir = os.getcwd()

    self.output().parent.touch()

    #combine_ini = self.input()['combine_ini']
    #with combine_ini.open('r') as infile:
    #  os.chdir(self.merge_dir + '/' + self.name)
    #  with open('combine.ini', 'w') as outfile:
    #    outfile.write(infile.read())

    os.chdir('{}/{}'.format(self.merge_dir, self.name))
    analysis_path = os.environ['ANALYSIS_PATH']

    os.system('nnlojet-combine.py -C {}/combine.ini -j {} | tee tmp.log'.format(analysis_path, self.cores))

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
          os.system('nnlojet-combine.py -C {}/combine.ini --APPLfast Combined/Final/{} > Combined/Final/{}'.format(analysis_path, filename, endfile))

    with open('tmp.log', 'r') as infile:
      with self.output().open('w') as outfile:
        outfile.write(infile.read())

    os.system('rm tmp.log')

    os.chdir(prevdir)

