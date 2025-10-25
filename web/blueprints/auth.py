#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Authentication Blueprint
Handles login, logout, and authentication
"""

from flask import Blueprint, request, session, redirect, render_template_string, url_for
from functools import wraps
from web.templates.login import LOGIN_HTML
from web.i18n.languages import LANGUAGES, get_text

auth_bp = Blueprint('auth', __name__)


def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    from flask import current_app
    converter = current_app.config['CONVERTER']

    # Get language from query parameter or session
    lang = request.args.get('lang')
    if lang and lang in LANGUAGES:
        session['language'] = lang
    elif 'language' not in session:
        session['language'] = 'en'

    current_lang = session['language']

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if converter.verify_user(username, password):
            session['logged_in'] = True
            session['username'] = username
            # Redirect to index page (Flask will handle base_path automatically)
            return redirect(url_for('management.index'))
        else:
            error_text = '用户名或密码错误' if current_lang == 'zh' else 'Invalid username or password'
            error_html = f'''<div class="alert-error">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
                <span>{error_text}</span>
            </div>'''
            return render_template_string(
                LOGIN_HTML.format(
                    lang=current_lang,
                    login_title=get_text('login_title', current_lang),
                    login_header=get_text('login_header', current_lang),
                    login_subtitle=get_text('login_subtitle', current_lang),
                    username=get_text('username', current_lang),
                    password=get_text('password', current_lang),
                    login_btn=get_text('login_btn', current_lang),
                    current_lang_display='EN' if current_lang == 'en' else '中文',
                    en_active='active' if current_lang == 'en' else '',
                    zh_active='active' if current_lang == 'zh' else '',
                    error_message=error_html
                )
            )

    return render_template_string(
        LOGIN_HTML.format(
            lang=current_lang,
            login_title=get_text('login_title', current_lang),
            login_header=get_text('login_header', current_lang),
            login_subtitle=get_text('login_subtitle', current_lang),
            username=get_text('username', current_lang),
            password=get_text('password', current_lang),
            login_btn=get_text('login_btn', current_lang),
            current_lang_display='EN' if current_lang == 'en' else '中文',
            en_active='active' if current_lang == 'en' else '',
            zh_active='active' if current_lang == 'zh' else '',
            error_message=''
        )
    )


@auth_bp.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('auth.login'))
