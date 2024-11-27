#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 23:06:05 2024

@author: hamza
"""

import openai
import requests
import json
import re
from requests.auth import HTTPBasicAuth
from pydantic import BaseModel
from Pass import site_url,username,password,GPTToken


class CalendarEvent(BaseModel):
    title: str
    blog_post: str
    
class Post:
    def __init__(self, data):
        self.__dict__['_data'] = data

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name in self._data or not name.startswith('_'):
            self._data[name] = value
        else:
            super().__setattr__(name, value)

    def __delattr__(self, name):
        if name in self._data:
            del self._data[name]
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def __repr__(self):
        return f"{self.__class__.__name__}(id{self.id, self.title['rendered']})"
    
    def __dir__(self):
        return list(self._data.keys()) + super().__dir__()

class wordpressTranslator:
    
    def __init__(self,site_url,username,password,GPTAPIAccessToken):
        self.username = username
        self.password = password
        self.site_url = site_url
        self.GPTAPIAccessToken = GPTAPIAccessToken
        self.client = openai.OpenAI(api_key = self.GPTAPIAccessToken) # Use environment variable for security

    def getPosts(self,):
            site_url,username,password = self.site_url,self.username,self.password
            # Make the request
            params = {
            'status': 'draft',  # Fetch only draft posts
            'tags': 6,
            'per_page': 100,     # Number of posts to retrieve
            }
            # Endpoint for retrieving posts
            endpoint = f"{site_url}/wp-json/wp/v2/posts"
            try:
                response = requests.get(endpoint,params=params ,auth=(self.username, self.password) if username and password else None)

                # Check for successful response
                if response.status_code == 200:
                    posts = response.json()
                    return [Post(post) for post in posts]
                    for post in posts:
                        print(f"Title: {post['title']['rendered']}")
                        print(f"Content: {post['content']['rendered']}")
                        print(f"Date: {post['date']}")
                        print("-" * 40)
                        
                else:
                    print(f"Failed to retrieve posts. Status code: {response.status_code}")
                    print(f"Error: {response.text}")
            
            except Exception as e:
                print(f"An error occurred: {e}")
    
    def translatePost(self,post,target_language, model="gpt-4o"):
            prompt = post.content["rendered"]
            
            title = post.title["rendered"]
            blog_post = post.content["rendered"]
            
            # Messages for Chat API
            messages = [
                {
                    "role": "system",
                    "content": f'''You are a fluent {target_language} blog post and seo expert. Translate the following content into {target_language}. Sometimes you will receive incomplete blog posts (the length is too short) if you detect some don't hesitate to use your knowledge to complete the blog post and optimize it's seo ( Transition words,Flesch reading ease,Sentences length ).'''
                },
                {
                    "role": "user",
                    "content": f"""
                    Title: {title}
                    Blog Post: {blog_post}
                    
                    
                    Return the result in JSON format with the structure, Please provide the output as a valid JSON object. The JSON must follow this exact format, with no additional text or line breaks, Use compact formatting without any extra newlines or spaces :
                        {{
                            "title": "Translated title",
                            "blog_post": "Translated blog post content."
                            "meta_description" : "A meta description is over 160 characters."
                        }}
                    
                    """
                }
            ]           
            
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                )
                translated_content = response.choices[0].message.content
                # Regular expression to extract JSON
                json_pattern = re.compile(r'\{[^}]*\}', re.DOTALL)
                json_match = json_pattern.search(translated_content)

                # Extracted JSON
                extracted_json = json_match.group() if json_match else None
                translated_content = json.loads(extracted_json)

                post.content["rendered"] = translated_content["blog_post"]
                post.title["rendered"] = translated_content["title"]

                return post
            except openai.error.OpenAIError as e: 
                return f"An error occurred with the OpenAI API: {e}"
            except Exception as e:
                return f"An unexpected error occurred: {e}"
    
    def UpdatePost(self,post):
        url = f"{self.site_url}/wp-json/wp/v2/posts/{post.id}"
        data = {
                "title": post.title['rendered'],
                "content": post.content["rendered"],
                "tags" : [7],
                "meta": { "_aioseop_description": "This is the updated meta description for the post."}
                }
        response = requests.post(url, json=data, auth=HTTPBasicAuth(self.username, self.password))
        if response.status_code == 200:
            print("Post updated successfully!")
            #print(response.json())
        else:
            print(f"Failed to update post. Status code: {response.status_code}")
            #print(response.json())
        return 0
    
if __name__=="__main__":

    WT = wordpressTranslator(site_url,username,password,GPTToken)
    
    posts = WT.getPosts()
    print("hahah")
    p0=posts[0]
    p0 = WT.translatePost(posts[0],"French",model="gpt-4o-mini")
    WT.UpdatePost(p0)    