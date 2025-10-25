#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Login Template
Contains the HTML template for the login page
"""

LOGIN_HTML = '''
<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{login_title}</title>
    <link rel="icon" href="/static/logo/logo.png" type="image/png">
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
    <style>
        body {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .login-container {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
            width: 100%;
            max-width: 400px;
        }}
        .login-header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .login-logo {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            margin-bottom: 20px;
        }}
        .login-logo img {{
            height: 60px;
            width: auto;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
        }}
        .login-logo h2 {{
            margin: 0;
            color: #2a5298;
            font-weight: bold;
            font-size: 2rem;
        }}
        .login-subtitle {{
            color: #6c757d;
            font-size: 0.9rem;
            margin-bottom: 0;
        }}
        .btn-login {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            color: white;
            padding: 12px;
            border-radius: 25px;
            width: 100%;
            font-weight: bold;
        }}
        .btn-login:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(118,75,162,0.4);
            color: white;
        }}
        /* Language selector - dropdown style */
        .language-selector-corner {{
            position: absolute;
            top: 20px;
            right: 20px;
            z-index: 1000;
        }}
        .language-dropdown {{
            position: relative;
            display: inline-block;
        }}
        .language-button {{
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            padding: 8px 12px;
            border-radius: 25px;
            border: 1px solid rgba(255,255,255,0.3);
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .language-button:hover {{
            background: rgba(255,255,255,0.25);
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        }}
        .language-icon {{
            color: white;
            font-size: 18px;
            display: flex;
            align-items: center;
        }}
        .language-current {{
            color: white;
            font-weight: 500;
            font-size: 14px;
        }}
        .language-menu {{
            position: absolute;
            top: 100%;
            right: 0;
            margin-top: 8px;
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            overflow: hidden;
            opacity: 0;
            visibility: hidden;
            transform: translateY(-10px);
            transition: all 0.3s ease;
            min-width: 120px;
        }}
        .language-dropdown:hover .language-menu {{
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }}
        .language-option {{
            padding: 10px 16px;
            color: #2a5298;
            cursor: pointer;
            transition: background 0.2s ease;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .language-option:hover {{
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
        }}
        .language-option.active {{
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.25) 0%, rgba(118, 75, 162, 0.25) 100%);
            color: #667eea;
            font-weight: 600;
        }}
        .github-link-login {{
            position: absolute;
            top: 20px;
            left: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            padding: 8px 16px;
            border-radius: 25px;
            text-decoration: none;
            color: white;
            border: 1px solid rgba(255,255,255,0.2);
            transition: all 0.3s ease;
        }}
        .github-link-login:hover {{
            background: rgba(255,255,255,0.25);
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            color: white;
        }}
        .github-link-login svg {{
            fill: currentColor;
        }}
        .github-stars-login {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 2px 8px;
            background: rgba(255,255,255,0.2);
            border-radius: 12px;
            font-size: 14px;
            font-weight: 600;
        }}
        .github-stars-login svg {{
            width: 14px;
            height: 14px;
        }}
        .alert-error {{
            background: linear-gradient(135deg, rgba(220, 53, 69, 0.1) 0%, rgba(220, 53, 69, 0.05) 100%);
            border: 1px solid rgba(220, 53, 69, 0.3);
            border-left: 4px solid #dc3545;
            color: #dc3545;
            padding: 12px 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .alert-error svg {{
            flex-shrink: 0;
            width: 20px;
            height: 20px;
        }}
    </style>
</head>
<body>
    <a href="https://github.com/maxiao0234/SubProtoX" target="_blank" class="github-link-login">
        <svg width="20" height="20" viewBox="0 0 24 24">
            <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
        </svg>
        GitHub
        <span class="github-stars-login" id="github-stars-login">
            <svg viewBox="0 0 16 16">
                <path d="M8 0.25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25z"/>
            </svg>
            <span id="star-count-login">-</span>
        </span>
    </a>
    <div class="language-selector-corner">
        <div class="language-dropdown">
            <div class="language-button">
                <span class="language-icon">
                    <span class="material-symbols-outlined" style="font-size: 20px;">translate</span>
                </span>
                <span class="language-current">{current_lang_display}</span>
            </div>
            <div class="language-menu">
                <div class="language-option {en_active}" onclick="changeLanguage('en')">
                    EN
                </div>
                <div class="language-option {zh_active}" onclick="changeLanguage('zh')">
                    中文
                </div>
            </div>
        </div>
    </div>
    <div class="login-container">
        <div class="login-header">
            <div class="login-logo">
                <img src="/static/logo/logo.png" alt="SubProtoX Logo">
                <h2>{login_header}</h2>
            </div>
            <p class="login-subtitle">{login_subtitle}</p>
        </div>
        <form method="post" action="login">
            {error_message}
            <div class="mb-3">
                <label class="form-label">{username}</label>
                <input type="text" name="username" class="form-control" required>
            </div>
            <div class="mb-3">
                <label class="form-label">{password}</label>
                <input type="password" name="password" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-login">{login_btn}</button>
        </form>
    </div>

    <script>
        function changeLanguage(lang) {{
            localStorage.setItem('language', lang);
            window.location.href = 'login?lang=' + lang;
        }}

        // Fetch GitHub stars for login page
        fetch('https://api.github.com/repos/maxiao0234/SubProtoX')
            .then(response => response.json())
            .then(data => {{
                if (data.stargazers_count !== undefined) {{
                    document.getElementById('star-count-login').textContent = data.stargazers_count;
                }}
            }})
            .catch(error => {{
                console.error('Failed to fetch GitHub stars:', error);
            }});
    </script>
</body>
</html>
'''
