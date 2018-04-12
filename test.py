"""test file.
Used to test the EDMF class

#TODO check Sidak forumula
#TODO add sensor selection option

Author: Alberto Costa
Institution: Future Cities Laboratory, Singapore
Version: 0.1
Last modify: 12/04/18
"""


import EDMF
import numpy as np



#create an object EDMF with data taken from Template_Input.xlsx, where the number of parameters is 5
#instance = EDMF.EDMF("Template_Input.xlsx", 5)
instance = EDMF.EDMF("Input.xlsx", 3)

#run the Monte Carlo sampling for the predictions
instance.Monte_Carlo_sampling('p')

#run the Monte Carlo sampling for the measurements
instance.Monte_Carlo_sampling('m')

#compute T bounds, use Sidak
instance.T_bounds(Sidak=True)
#print instance.T

#perform falsification
instance.falsification()

#print CMS
print instance.CMS


#save instances of the CMS in CMS.xlsx file
instance.save_CMS("CMS.xlsx")




