'''
Sets up profile's "Profile History" page

Created by Jessica - 04.25
'''
############################### IMPORTS ###############################
from sqlalchemy import create_engine
from flask import Flask, render_template

import service_recc as sr
import convert_sql as cs
import db_connect as db

#######################################################################################

'''
Get watchlist from database to print out on its page

Inputs:
Returns:

Created by Jessica - 04.26
'''
