#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 19:07:26 2024

@author: hamza
"""
import openai
import requests
import json
import re
from requests.auth import HTTPBasicAuth
from pydantic import BaseModel
from Pass import site_url,username,password,GPTToken
 
if __name__=="__main__":

    WT = wordpressTranslator(site_url,username,password,GPTToken)
    
    posts = WT.getPosts()
    print("hahah")
    p0=posts[0]
    p0 = WT.translatePost(posts[0],"French",model="gpt-4o-mini")
    WT.UpdatePost(p0)    