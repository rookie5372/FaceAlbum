#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import envir
from all_search import *


a = urltolabeldict['http://img.youbiaoqing.com/u/914cd6c4f7063aad46d50cfa92cb9c55.gif']
for i in a:
	print i
print img_search('test.jpg')

