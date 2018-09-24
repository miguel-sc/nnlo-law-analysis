# -*- coding: utf-8 -*-

import luigi
import os
import fnmatch
from subprocess import PIPE
from law.util import interruptable_popen

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

    code, job_out, error = interruptable_popen(['nnlojet-combine.py', '-C', self.combine_ini, '-j', self.cores],stdout=PIPE, stderr=PIPE)
    if (code != 0):
      raise Exception(error + 'nnlojet-combine returned non-zero exit status {}'.format(code))

    for root, dirnames, filenames in os.walk('.'):
      for filename in fnmatch.filter(filenames, '*.APPLfast.txt'):
        parts = filename.split('.')
        if 'cross' not in parts:
          parts.pop()
          parts.pop()
          parts.append('dat')
          parts.insert(0, self.process)
          endfile = '.'.join(parts)
          
          code, out, error = interruptable_popen('nnlojet-combine.py -C {} --APPLfast Combined/Final/{} > Combined/Final/{}'.format(self.combine_ini, filename, endfile), shell=True ,stdout=PIPE, stderr=PIPE)
          if (code != 0):
            raise Exception(error + 'NNLOJET returned non-zero exit status {}'.format(code))

    self.output().dump(job_out, formatter="text")

    os.chdir(prevdir)

