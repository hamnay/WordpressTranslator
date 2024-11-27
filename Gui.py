#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 23:31:19 2024

@author: hamza
"""
import sys
import tkinter as tk
from tkinter import messagebox, scrolledtext, Listbox, END
from tkhtmlview import HTMLLabel
from WPTranslator import wordpressTranslator
from Pass import site_url, username, password, GPTToken

# Initialize the WordPress Translator object
WT = wordpressTranslator(site_url, username, password, GPTToken)

class WPTranslatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WordPress Translator GUI")
        self.root.geometry("800x800")

        # Button to fetch draft posts
        self.fetch_button = tk.Button(root, text="Fetch Draft Posts", command=self.fetch_posts)
        self.fetch_button.pack(pady=10)

        # List to show the fetched posts
        self.posts_list = Listbox(root, height=10)
        self.posts_list.pack(fill=tk.BOTH, padx=10, pady=5)
        self.posts_list.bind('<<ListboxSelect>>', self.display_post)

        # Label and widget to show original post
        self.original_label = tk.Label(root, text="Original Post:")
        self.original_label.pack()
        self.original_text = HTMLLabel(root, width=80, height=10)
        self.original_text.pack(padx=10, pady=5)
        self.original_text.config(wrap=tk.WORD)

        # Button to translate post
        self.translate_button = tk.Button(root, text="Translate Post", command=self.translate_post)
        self.translate_button.pack(pady=10)

        # Label and widget to show translated post
        self.translated_label = tk.Label(root, text="Translated Post:")
        self.translated_label.pack()
        self.translated_text = HTMLLabel(root, width=80, height=10)
        self.translated_text.pack(padx=10, pady=5)
        self.translated_text.config(wrap=tk.WORD)

        # Button to update the post
        self.update_button = tk.Button(root, text="Update Post", command=self.update_post)
        self.update_button.pack(pady=10)

    def fetch_posts(self):
        try:
            self.posts = WT.getPosts()
            if self.posts:
                self.posts_list.delete(0, END)
                for post in self.posts:
                    self.posts_list.insert(END, post.title["rendered"])
            else:
                messagebox.showinfo("Info", "No draft posts found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch posts: {e}")

    def display_post(self, event):
        try:
            selected_index = self.posts_list.curselection()
            if selected_index:
                selected_title = self.posts_list.get(selected_index)
                for post in self.posts:
                    if post.title["rendered"] == selected_title:
                        self.current_post = post
                        self.original_text.set_html(post.content["rendered"] if post.content.get("rendered") else "<p>No content available</p>")
                        break
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display post: {e}")

    def translate_post(self):
        try:
            if hasattr(self, 'current_post') and self.current_post:
                translated_post = WT.translatePost(self.current_post, "French", model="gpt-4o-mini")
                if translated_post and translated_post.content.get("rendered"):
                    self.translated_text.set_html(translated_post.content["rendered"])
                else:
                    messagebox.showwarning("Warning", "Translation failed or no content available.")
            else:
                messagebox.showwarning("Warning", "No post to translate.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to translate post: {e}")

    def update_post(self):
        try:
            if hasattr(self, 'current_post') and self.current_post:
                translated_content = self.translated_text.get(1.0, END).strip()
                if translated_content:
                    self.current_post.content["rendered"] = translated_content
                    WT.UpdatePost(self.current_post)
                    messagebox.showinfo("Success", "Post updated successfully!")
                else:
                    messagebox.showwarning("Warning", "Translated content is empty, cannot update the post.")
            else:
                messagebox.showwarning("Warning", "No post to update.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update post: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = WPTranslatorGUI(root)
    root.mainloop()
