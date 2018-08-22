# -*- coding: utf-8 -*-

import luigi
import law
import os
import shutil

from Combine import Combine

from analysis.framework import Task, HTCondorWorkflow

class MergeFastProd(Task, HTCondorWorkflow, law.LocalWorkflow):

  merge_dir = luigi.Parameter()
  channels = luigi.Parameter()
  observables = luigi.ListParameter()

  def create_branch_map(self):
    channels = self.channels.split(' ')
    i = 0
    branchmap = {}
    for channel in channels:
      for obs in self.observables:
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
