# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 16:11:30 2017

@author: nl211
"""

import sqlite3
import Common.classStore as st
import Common.classTech as tc
import Solvers.classCHPProblem as pb
import numpy as np
import matplotlib.pyplot as plt


id = 693
pb = pb.CHPproblem(id)

pb.SebastianControl(15)