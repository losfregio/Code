# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 11:00:41 2017

@author: nl211
"""
import pandas as pd
import numpy as np
import math as m # For inifinity
import os
import sys
sys.path.append(os.path.abspath(".\\Common\\")) # Module is in seperate folder, hence the elaboration
sys.path.append(os.path.abspath(".\\Solvers\\")) # Module is in seperate folder, hence the elaboration
import Common.classStore as st
import Solvers.classCHPProblem as pb

def operation_sim(file_name = 'operation_results.csv', store_range = range(400,3000)):
    # Writes results of operation simulation to csv file
    with open(file_name,'w') as f:
        f.write("Store_ID,Tech_ID,BAU,SimpleOptiControl,LoadFollow \n")
        
        # Run through all the stores
        for store_id in store_range:

            try:
                # Try to run a simulation on a store
                problem_instance = pb.problem(store_id)
                for tech_id in range(1,9):
                    
                    # Try to run simulations and save to csv (data might not be available for that month)
                    try: 
                        out_1 = problem_instance.SimpleOptiControl(tech_id)
                        out_2 = problem_instance.LoadFollowControl(tech_id)
    
                        f.write("%d,%d," %(store_id, tech_id))
        #                out = problem_instance.SimpleOpti5NPV(1, tech_range=tech_id)
        #                out = problem_instance.SimpleOpti5NPV(2, tech_range=tech_id)
                        f.write("%.1f," %(sum(out_1[0])))
                        f.write("%.1f," %(sum(out_1[1])))
                        f.write("%.1f\n" %(sum(out_2[1])))
                        
                        print("Store ID = %d" %store_id)
                        
                    except:
                        pass
                # Couldn't find a good way of getting the average heating
                # demand of the stores, so just returned this from one of the
                # functions and printed it (stupid but whatever)
                print("Electricity average = %f" %(np.mean(out_1[3])))
                print("Heat average = %f" %(np.mean(out_1[4])))
                    
            # If store ID not found, pass
            except:
                pass
            
def operation_sim_opt_unit(file_name = 'operation_results_opt.csv', store_range = range(400,3000)):
    
    # Writes results of operation simulation to csv file, but only does this for the optimal unit for that store
    with open(file_name,'w') as f:
        f.write("Store_ID,Tech_ID,BAU,SimpleOptiControl,LoadFollow,SimpleOptiControl_NPV,LoadFollow_NPV \n")
        
        # Run through all the stores
        for store_id in store_range:

            try:
                # Try to run a simulation on a store
                problem_instance = pb.problem(store_id)
                print("Store ID = %d" %store_id)

                # Try to find best technology then compare stores
                # Use Niccolo's method to find best tech
                
                try:
                    out = problem_instance.SimpleOpti5NPV(method = 1)
                    tech_opt = out[0]
                    f.write("%d,%d," %(store_id,tech_opt))
                    
                    if tech_opt != -1: # If -1 that means that no optimal technology was found
                        print("tech_opt = %d" %tech_opt)
                        
                        out_1 = problem_instance.SimpleOptiControl(tech_opt)
                        out_2 = problem_instance.LoadFollowControl(tech_opt)
                        out_3 = problem_instance.SimpleOpti5NPV(method=1, tech_range=[tech_opt])
                        out_4 = problem_instance.SimpleOpti5NPV(method=2, tech_range=[tech_opt])
        
                        f.write("%.1f," %(sum(out_1[0]))) # This is BAU costs
                        f.write("%.1f," %(sum(out_1[1]))) # This is SimpleControl's costs
                        f.write("%.1f," %(sum(out_2[1]))) # This is LoadFollow costs
                        f.write("%.1f," %(out_3[2])) # This is SimpleControl's savings compared to BAU
                        f.write("%.1f" %(out_4[2])) # This is LoadFollow savings compared to BAU, using NPV
                        
                    f.write("\n")
                except:
                    pass
                
            # If store ID not found, pass
            except:
                pass
            
def uncertainty_sim(file_name = 'uncertainty_results.csv', store_range = range(400,3000),  u = [0.30, 0.05, 0.1], iterations = 1000):
    
    # Writes results of simulation results to csv file
    with open(file_name,'w') as f:    
        f.write("Store_ID,Tech_ID,BAU,SimpleOptiControl,u_el,u_a_el,u_gas \n")
        u_el = u[0]; u_a_el = u[1]; u_gas = u[2];
        f.write(",,,,%.3f,%.3f,%.3f\n" %(u_el,u_a_el,u_gas))
        
        # Run through all the stores
        for store_id in store_range:
            
            try:
                # Try to create a problm instance
                problem_instance = pb.problem(store_id)
                
                # Try to solve optimisation and iterate with uncertainty
                # Use Niccolo's method
                try:
                    out = problem_instance.SimpleOpti5NPV(method = 1)
                    tech_opt = out[0]
                    
                    print("tech_opt = %d" %tech_opt)
                    print("Store ID = %d" %store_id)
                    
                    for i in range(iterations+1):
                        print(i)
                        out = problem_instance.SimpleOptiControl(tech_opt, uncertainty = u)
                        f.write("%d,%d," %(store_id,tech_opt))
                        f.write("%.1f," %(sum(out[0]))) # This is BAU costs
                        f.write("%.1f\n" %(sum(out[1]))) # This is SimpleControl's costs
                        # TODO: RETURN NPV!!! Only returning op costs right now
                except:
                    pass
                
            # If store ID not found, pass
            except:
                pass


p1 = pb.CHPproblem(555)
#m001 = p1.SebastianControl(15, CHPQA = True, mipgap = 0.01)
#m01 = p1.SebastianControl(15, CHPQA = True, mipgap = 0.1)
m1 = p1.SebastianControl(15, CHPQA = False, mipgap = 1)

#operation_sim_opt_unit(store_range=range(500,820))
# uncertainty_sim(store_range = range(781,782))

# Move files to MATLAB analysis folder. You need to close the Code folder to do this!!!
os.system('move *.csv .\\Matlab_analysis')
