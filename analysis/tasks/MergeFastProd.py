# -*- coding: utf-8 -*-

import luigi
import law
import glob
import os
import fnmatch
import shutil

from Combine import Combine

from analysis.framework import Task, HTCondorWorkflow

class MergeFastProd(Task, HTCondorWorkflow, law.LocalWorkflow):

  merge_dir = luigi.Parameter()

  def create_branch_map(self):
    channels = ['LO', 'R', 'V', 'RRa', 'RRb', 'RV', 'VV']
    tablenames = []
    for file in glob.glob('{}/{}/*/*.tab.gz'.format(self.merge_dir, self.name)):
      fileparts = file.split('.')
      obs = fileparts[3]
      scen = fileparts[0]
      if obs not in tablenames:
        tablenames.append(obs)
    i = 0
    branchmap = {}
    for channel in channels:
      for obs in sorted(tablenames):
        branchmap[i] = {
          'obs': obs,
          'channel': channel
        }
        i += 1
    return branchmap

  def htcondor_workflow_requires(self):
    return {
      'combine': Combine()
    }

  def requires(self):
    return Combine()

  def output(self):
    return law.LocalFileTarget('{}/{}/Combined/Final/{}.{}.{}.tab.gz'.format(self.merge_dir, self.name, self.process, self.branch_data['channel'], self.branch_data['obs']))

  def run(self):
    self.output().parent.touch()

    outfile = self.output().path
    parts = outfile.split('.')
    parts.pop()
    parts.pop()
    parts.append('merge2.log')
    logfile = '.'.join(parts)

    dirpath = 'tmpdir' + str(self.branch)
    os.mkdir(dirpath)
    prevdir = os.getcwd()
    os.chdir(dirpath)

    os.system('fnlo-tk-merge2 -w NNLOJET {merge_dir}/{name}/Combined/Final/NNLO.{obs}.APPLfast.txt {merge_dir}/{name}/{channel}/*.{obs}.s*.tab.gz tmp.tab.gz | tee {log}'.format(obs = self.branch_data['obs'], channel = self.branch_data['channel'], merge_dir = self.merge_dir, name = self.name, log = logfile))

    with open('tmp.tab.gz', 'r') as infile:
      with self.output().open('w') as outfile:
        outfile.write(infile.read())

    os.system('rm tmp.tab.gz')

    os.chdir(prevdir)
    shutil.rmtree(dirpath)
