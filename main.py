#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 19:07:26 2024

@author: hamza
"""
from WPTranslator import wordpressTranslator
from Pass import site_url,username,password,GPTToken
from tqdm import tqdm
if __name__=="__main__":

    WT = wordpressTranslator(site_url,username,password,GPTToken)
    
    posts = WT.getPosts()
    
    for post in tqdm(posts):
        translatedPost = WT.translatePost(post,"French",model="gpt-4o-mini")
        WT.UpdatePost(translatedPost)    