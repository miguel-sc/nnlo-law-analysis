# -*- coding: utf-8 -*-

import luigi
import law
import glob
import os
import fnmatch

from Combine import Combine

from analysis.framework import Task, HTCondorWorkflow

class MergeFastProd(Task, HTCondorWorkflow, law.LocalWorkflow):

  merge_dir = luigi.Parameter()

  def htcondor_workflow_requires(self):
    return {
      'combine': Combine(),
   }

  def init_branch(self):
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
    self.obs = branchmap[self.branch]['obs']
    self.channel = branchmap[self.branch]['channel']

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

  def requires(self):
    return Combine()

  def output(self):
    self.init_branch()
    return law.LocalFileTarget('{}/{}/Combined/Final/{}.{}.{}.tab.gz'.format(self.merge_dir, self.name, self.process, self.channel, self.obs))

  def run(self):
    self.init_branch()
    self.output().parent.touch()

    outfile = self.output().path
    parts = outfile.split('.')
    parts.pop()
    parts.pop()
    parts.append('merge2.log')
    logfile = '.'.join(parts)

    os.system('fnlo-tk-merge2 -w NNLOJET {merge_dir}/{name}/Combined/Final/NNLO.{obs}.APPLfast.txt {merge_dir}/{name}/{channel}/*.{obs}.s*.tab.gz tmp.tab.gz | tee {log}'.format(obs = self.obs, channel = self.channel, merge_dir = self.merge_dir, name = self.name, log = logfile))

    with open('tmp.tab.gz', 'r') as infile:
      with self.output().open('w') as outfile:
        outfile.write(infile.read())

    os.system('rm tmp.tab.gz')
