# api.py
from flask import Blueprint, jsonify
from app.models import Post, Page

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/posts', methods=['GET'])
def get_posts():
    # Fetch all posts
    posts = Post.query.all()
    return jsonify([{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'created_at': post.created_at.isoformat(),
        'author': post.author.username
    } for post in posts])

@api_bp.route('/api/posts/<int:id>', methods=['GET'])
def get_post(id):
    # Fetch single post
    post = Post.query.get_or_404(id)
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'created_at': post.created_at.isoformat(),
        'author': post.author.username
    })

@api_bp.route('/api/pages', methods=['GET'])
def get_pages():
    # Fetch all pages
    pages = Page.query.all()
    return jsonify([{
        'id': page.id,
        'title': page.title,
        'content': page.content,
        'created_at': page.created_at.isoformat(),
        'author': page.author.username
    } for page in pages])

@api_bp.route('/api/pages/<int:id>', methods=['GET'])
def get_page(id):
    # Fetch single page
    page = Page.query.get_or_404(id)
    return jsonify({
        'id': page.id,
        'title': page.title,
        'content': page.content,
        'created_at': page.created_at.isoformat(),
        'author': page.author.username
    })