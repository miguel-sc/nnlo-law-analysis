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

  def create_branch_map(self):
    regions = ['LO', 'R', 'V', 'RRa', 'RRb', 'RV', 'VV']
    tablenames = []
    for file in glob.glob('{}/{}/*/*.tab.gz'.format(self.merge_dir, self.name)):
      fileparts = file.split('.')
      obs = fileparts[3]
      scen = fileparts[0]
      if obs not in tablenames:
        tablenames.append(obs)
    i = 0
    branchmap = {}
    for region in regions:
      for obs in tablenames:
        branchmap[i] = {
          'obs': obs,
          'region': region
        }
        if (i < 3):
          i += 1
    return branchmap

  def requires(self):
    return Combine()

  def output(self):
    return law.LocalFileTarget('{}/{}/Combined/Final/{}.{}.tab.gz'.format(self.merge_dir, self.name, self.branch_data['region'], self.branch_data['obs']))

  def run(self):
    self.output().parent.touch()

    os.system('fnlo-tk-merge2 -w NNLOJET {merge_dir}/{name}/Combined/Final/NNLO.{obs}.APPLfast.txt {merge_dir}/{name}/{region}/*.{obs}.s*.tab.gz tmp.tab.gz'.format(obs = self.branch_data['obs'], region = self.branch_data['region'], merge_dir = self.merge_dir, name = self.name))

    with open('tmp.tab.gz', 'r') as infile:
      with self.output().open('w') as outfile:
        outfile.write(infile.read())
