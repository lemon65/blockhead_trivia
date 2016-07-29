#!/usr/bin/python

import os
import sys
import time
import requests

################ Description ##################
# Function to go to the trivia API and gather information.

def trivia_caller():
    r = requests.get('http://jservice.io/api/random')
    response = r.json()
    return response
