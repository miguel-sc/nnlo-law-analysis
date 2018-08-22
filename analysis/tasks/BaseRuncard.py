# -*- coding: utf-8 -*-

from law.contrib.tasks import TransferLocalFile
from analysis.framework import Task

class BaseRuncard(TransferLocalFile, Task):

  def single_output(self):
    return self.remote_target('{}.{}.run'.format(self.process, self.name))

