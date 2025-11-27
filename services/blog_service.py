"""
Blog service for managing blog posts
"""
import json
import os

def get_all_posts():
    """Get all blog posts"""
    posts_file = 'data/blog_posts.json'
    if os.path.exists(posts_file):
        with open(posts_file, 'r') as f:
            return json.load(f)
    else:
        # Default posts
        return [
            {
                'id': '1',
                'title': 'The Future of AI Jobs in 2024',
                'excerpt': 'Exploring how AI is reshaping the job market and creating new opportunities.',
                'date': '2024-01-15',
                'author': 'Analytics Team',
                'thumbnail': '/static/images/blog-1.jpg'
            },
            {
                'id': '2',
                'title': 'Top 10 In-Demand Skills for Data Scientists',
                'excerpt': 'A comprehensive guide to the skills that will make you stand out in 2024.',
                'date': '2024-01-10',
                'author': 'Career Insights',
                'thumbnail': '/static/images/blog-2.jpg'
            },
            {
                'id': '3',
                'title': 'Understanding Job Market Saturation',
                'excerpt': 'Learn how to identify oversaturated markets and find emerging opportunities.',
                'date': '2024-01-05',
                'author': 'Market Research',
                'thumbnail': '/static/images/blog-3.jpg'
            }
        ]

def get_post_by_id(post_id):
    """Get a specific blog post by ID"""
    posts = get_all_posts()
    for post in posts:
        if post['id'] == str(post_id):
            # In a real app, you'd load full content from a file or database
            post['content'] = f"""
            <h2>Introduction</h2>
            <p>This is the full content for {post['title']}. In a production system, 
            this would be loaded from a database or markdown files.</p>
            <h2>Main Content</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
            Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
            """
            return post
    return None

