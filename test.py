"""test file.
Used to test the EDMF class



Author: Alberto Costa
Institution: Future Cities Laboratory, Singapore
Version: 0.1
Last modify: 22/02/18
"""


import EDMF



instance = EDMF.EDMF("Template_Input.xlsx", 5)
instance.Monte_Carlo_sampling('p')
instance.Monte_Carlo_sampling('m')
instance.T_bounds(Sidak=True)
print instance.T
instance.falsification()
print instance.CMS

instance.save_CMS("CMS.xlsx")  #NB ID starts from 0

#TODO check Sidak forumula
#TODO add sensor selection option

