#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Management Template
Contains the HTML template for the management interface
"""

# Due to the large size (1800+ lines), the management template is stored as a single string
# This template contains the complete HTML for the converter, history, rules, settings, and API tabs

MANAGEMENT_HTML = '''<!DOCTYPE html>
<html lang="{{ lang }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="icon" href="/static/logo/logo.png" type="image/png">
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">
    <!-- Material Symbols -->
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap" />
    <style>
    {% raw %}
        body {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .main-container {
            max-width: 1400px;
            margin: 0 auto;
        }
        .header-section {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            margin-top: 60px;
            color: white;
            position: relative;
        }

        /* Conversion Type Card Styles */
        .conversion-type-card {
            transition: all 0.3s ease;
        }

        .conversion-type-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.25);
        }

        /* Configuration Fields Styles */
        #config-name:focus, #rule-template:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25) !important;
            outline: none;
        }

        #config-name:hover, #rule-template:hover {
            border-color: #a0a0a0 !important;
        }

        /* Config Section Styles */
        .config-section {
            margin-bottom: 30px;
        }

        .section-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 12px 20px;
            border-radius: 10px 10px 0 0;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .section-header h5 {
            margin: 0;
            color: white;
            font-weight: 600;
            font-size: 1.1rem;
        }

        .step-badge {
            background: white;
            color: #667eea;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.1rem;
            flex-shrink: 0;
        }

        /* Material Symbols - Typography settings */
        .material-symbols-outlined {
            font-family: 'Material Symbols Outlined';
            font-weight: normal;
            font-style: normal;
            display: inline-block;
            line-height: 1;
            text-transform: none;
            letter-spacing: normal;
            word-wrap: normal;
            white-space: nowrap;
            direction: ltr;
        }

        /* Layer 1: Page Title Icons - Largest, Bold (40px, weight 600) */
        .icon-page-title {
            font-size: 40px;
            font-variation-settings:
                'FILL' 0,
                'wght' 600,
                'GRAD' 0,
                'opsz' 48;
            vertical-align: middle;
        }

        /* Layer 2: Section Header Icons - Medium, Bold (24px, weight 500, with circle background) */
        .icon-section {
            background: white;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }

        .icon-section::before {
            font-family: 'Material Symbols Outlined';
            font-size: 18px;
            font-variation-settings:
                'FILL' 0,
                'wght' 500,
                'GRAD' 0,
                'opsz' 20;
        }

        /* Specific section icons */
        .icon-section.history::before {
            content: 'history';
        }

        /* Layer 3: Board Title Icons - Medium, No background (28px, weight 400) */
        .icon-board {
            font-size: 28px;
            font-variation-settings:
                'FILL' 0,
                'wght' 400,
                'GRAD' 0,
                'opsz' 24;
            margin-right: 8px;
            vertical-align: middle;
        }

        /* Layer 4: Inline Icons - Small (20px, weight 300) */
        .icon-inline {
            font-size: 20px;
            font-variation-settings:
                'FILL' 0,
                'wght' 300,
                'GRAD' 0,
                'opsz' 20;
            vertical-align: middle;
            margin-right: 6px;
        }

        /* Layer 5: Button Icons - Tiny (16px, weight 400) */
        .icon-btn {
            font-size: 16px;
            font-variation-settings:
                'FILL' 0,
                'wght' 400,
                'GRAD' 0,
                'opsz' 20;
            vertical-align: middle;
            margin-right: 4px;
        }

        /* Material Icon - Built-in Rules (NO circle background) */
        .icon-builtin {
            font-family: 'Material Symbols Outlined';
            font-size: 28px;
            color: #667eea;
            font-variation-settings:
                'FILL' 0,
                'wght' 400,
                'GRAD' 0,
                'opsz' 24;
            margin-right: 8px;
        }

        .icon-builtin::before {
            content: 'article';
        }

        /* Material Icon - Custom Rules (NO circle background) */
        .icon-custom {
            font-family: 'Material Symbols Outlined';
            font-size: 28px;
            color: #28a745;
            font-variation-settings:
                'FILL' 0,
                'wght' 400,
                'GRAD' 0,
                'opsz' 24;
            margin-right: 8px;
        }

        .icon-custom::before {
            content: 'edit_note';
        }

        /* Create New button with hover animation */
        .btn-create-new {
            background: rgba(255,255,255,0.2);
            border: 1px solid rgba(255,255,255,0.3);
            color: white;
            border-radius: 8px;
            padding: 6px 16px;
            font-size: 0.9rem;
            min-width: auto;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .btn-create-new:hover {
            background: rgba(255,255,255,0.3);
            border-color: rgba(255,255,255,0.5);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }

        .section-content {
            background: white;
            padding: 25px;
            border-radius: 0 0 10px 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }

        /* Language selector in corner - absolute position (same as login page) */
        .language-selector-corner {
            position: absolute;
            top: 20px;
            right: 20px;
            z-index: 1000;
        }

        .language-dropdown {
            position: relative;
            display: inline-block;
        }

        .language-button {
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
        }

        .language-button:hover {
            background: rgba(255,255,255,0.25);
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        }

        .language-icon {
            color: white;
            font-size: 18px;
            display: flex;
            align-items: center;
        }

        .language-current {
            color: white;
            font-weight: 500;
            font-size: 14px;
        }

        .language-menu {
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
        }

        .language-dropdown:hover .language-menu {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }

        .language-option {
            padding: 10px 16px;
            color: #2a5298;
            cursor: pointer;
            transition: background 0.2s ease;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .language-option:hover {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
        }

        .language-option.active {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.25) 0%, rgba(118, 75, 162, 0.25) 100%);
            color: #667eea;
            font-weight: 600;
        }

        /* GitHub link in corner - absolute position (same as login page) */
        .github-link-corner {
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
            z-index: 1000;
        }

        .github-link-corner:hover {
            background: rgba(255,255,255,0.25);
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            color: white;
        }

        .github-link-corner svg {
            fill: currentColor;
        }

        .github-stars {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 2px 8px;
            background: rgba(255,255,255,0.2);
            border-radius: 12px;
            font-size: 14px;
            font-weight: 600;
        }

        .github-stars svg {
            width: 14px;
            height: 14px;
        }

        .header-top-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
        }

        .header-left {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .header-logo {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .header-logo img {
            height: 50px;
            width: auto;
            filter: drop-shadow(0 4px 15px rgba(0,0,0,0.3));
        }

        .header-logo h2 { 
            margin: 0;
            color: white;
            font-weight: bold;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .restart-btn {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 6px 16px;
            border-radius: 20px;
            transition: all 0.3s ease;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 14px;
            min-width: 100px;
            justify-content: center;
            font-weight: 600;
        }

        .restart-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
            color: white;
        }

        .language-selector {
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            padding: 8px 12px;
            border-radius: 25px;
            border: 1px solid rgba(255,255,255,0.3);
            min-width: 100px;
            justify-content: center;
        }
        .language-icon {
            color: white;
            font-size: 18px;
            display: flex;
            align-items: center;
        }
        .language-selector select {
            border: none;
            background: transparent;
            color: white;
            border-radius: 3px;
            padding: 2px 5px;
            outline: none;
            cursor: pointer;
        }
        .language-selector select option {
            background: #2a5298;
            color: white;
        }

        .github-link {
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
        }

        .github-link:hover {
            background: rgba(255,255,255,0.25);
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            color: white;
        }

        .github-link svg {
            fill: currentColor;
        }
        .logout-btn {
            background: rgba(255,255,255,0.2);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.3);
            color: white;
            padding: 6px 16px;
            border-radius: 20px;
            transition: all 0.3s ease;
            min-width: 80px;
            text-align: center;
            display: inline-block;
            text-decoration: none;
            font-size: 14px;
        }

        .logout-btn:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            color: white;
            text-decoration: none;
        }
        .card-custom { 
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            overflow: hidden;
        }
        .card-header-custom {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0;
            font-weight: bold;
            border-radius: 15px 15px 0 0;
        }

        .nav-tabs-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
        }

        .nav-tabs-container .nav-tabs {
            flex: 1;
            margin: 0;
        }

        .tab-actions {
            display: flex;
            gap: 10px;
            align-items: center;
        }

        .tab-actions .logout-btn {
            min-width: 80px;
            padding: 6px 16px;
            font-size: 14px;
            margin: 0;
        }

        .tab-actions .restart-btn {
            min-width: 100px;
            padding: 6px 16px;
            font-size: 14px;
            margin: 0;
        }
        .converter-section {
            padding: 30px 30px 10px 30px;
        }
        .input-group-custom { 
            margin-bottom: 20px;
        }
        .btn-convert {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            color: white;
            padding: 14px 40px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1.05rem;
            transition: all 0.3s ease;
            min-width: 200px;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            position: relative;
            overflow: hidden;
        }

        .btn-convert:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(102, 126, 234, 0.5);
            color: white;
        }

        .btn-convert:active {
            transform: translateY(0);
            box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
        }

        .btn-convert::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }

        .btn-convert:hover::before {
            width: 300px;
            height: 300px;
        }
        .output-box { 
            background: #f8f9fa;
            border: 2px dashed #dee2e6;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            word-break: break-all;
            font-family: monospace;
        }
        .rule-item {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 0;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
            transition: all 0.2s ease;
            position: relative;
        }

        .rule-item:hover {
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transform: translateY(-2px);
            background: #ffffff;
        }

        .rule-item::before {
            content: '›';
            position: absolute;
            left: 15px;
            top: 15px;
            color: rgba(102, 126, 234, 0.7);
            font-size: 16px;
            font-weight: bold;
            transition: all 0.2s ease;
            pointer-events: none;
            line-height: 1;
        }

        .rule-item:hover::before {
            color: #667eea;
        }

        .rule-item.expanded::before {
            transform: rotate(90deg);
            color: #667eea;
        }

        /* Built-in rule styling */
        .rule-item.builtin-rule {
            background: linear-gradient(to right, rgba(102, 126, 234, 0.12) 0%, rgba(102, 126, 234, 0.06) 100%);
            border-left: 3px solid rgba(102, 126, 234, 0.7);
        }

        .rule-item.builtin-rule:hover {
            background: linear-gradient(to right, rgba(102, 126, 234, 0.18) 0%, rgba(102, 126, 234, 0.08) 100%);
            border-left-color: #667eea;
        }

        .rule-item.builtin-rule::before {
            color: rgba(102, 126, 234, 0.7);
        }

        .rule-item.builtin-rule:hover::before,
        .rule-item.builtin-rule.expanded::before {
            color: #667eea;
        }

        /* Custom rule styling */
        .rule-item.custom-rule {
            background: linear-gradient(to right, rgba(40, 167, 69, 0.12) 0%, rgba(40, 167, 69, 0.06) 100%);
            border-left: 3px solid rgba(40, 167, 69, 0.7);
        }

        .rule-item.custom-rule:hover {
            background: linear-gradient(to right, rgba(40, 167, 69, 0.18) 0%, rgba(40, 167, 69, 0.08) 100%);
            border-left-color: #28a745;
        }

        .rule-item.custom-rule::before {
            color: rgba(40, 167, 69, 0.7);
        }

        .rule-item.custom-rule:hover::before,
        .rule-item.custom-rule.expanded::before {
            color: #28a745;
        }

        .btn-primary {
            min-width: 150px;
        }

        .btn-danger {
            min-width: 150px;
        }

        .btn-success {
            min-width: 120px;
        }

        .btn-info {
            min-width: 120px;
        }

        .btn-warning {
            min-width: 120px;
        }

        .btn-secondary {
            min-width: 120px;
        }

        .rule-actions .btn-sm {
            min-width: 80px;
        }

        .history-actions .btn-sm {
            min-width: 80px;
        }

        /* Node preview button */
        #nodes-preview .btn-success {
            min-width: 180px;
        }

        /* Settings save buttons */
        .settings-card .btn-primary {
            min-width: 200px;
        }

        /* Maintenance buttons */
        .maintenance-item .btn-sm {
            min-width: 140px;
        }

        /* Config section transition for enable/disable */
        .config-section {
            transition: opacity 0.3s ease, filter 0.3s ease;
        }

        .config-section.disabled {
            opacity: 0.5;
            pointer-events: none;
            filter: grayscale(30%);
        }

        /* Rule item layout */
        .rule-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 15px;
            padding: 8px 15px 8px 38px;
            cursor: pointer;
        }

        .rule-info {
            flex: 1;
            display: flex;
            align-items: baseline;
            gap: 12px;
            min-width: 0;
        }

        .rule-header h5 {
            margin: 0;
            color: #333;
            font-size: 0.95rem;
            font-weight: 600;
            white-space: nowrap;
            flex-shrink: 0;
        }

        .rule-header p {
            margin: 0;
            color: #888;
            font-size: 0.85rem;
            font-weight: 400;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            flex: 1;
            font-style: italic;
        }

        .rule-actions { 
            flex-shrink: 0;
            display: flex;
            gap: 8px;
        }

        /* Edit rule styles with chevron */
        .rule-edit-chevron {
            display: inline-block;
            transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            margin-right: 5px;
        }

        .rule-edit-chevron.expanded {
            transform: rotate(90deg);
        }

        .rule-edit-form {
            background: rgba(255, 255, 255, 0.7);
            border: 1px solid rgba(102, 126, 234, 0.2);
            border-radius: 10px;
            padding: 0;
            margin-top: 0;
            max-height: 0;
            overflow: hidden;
            opacity: 0;
            transition: all 0.15s ease;
        }

        .rule-edit-form.show {
            padding: 20px;
            margin-top: 10px;
            max-height: 600px;
            opacity: 1;
        }

        .rule-edit-textarea { 
            width: 100%;
            min-height: 200px;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            resize: vertical;
        }

        .rule-edit-buttons { 
            margin-top: 15px;
            display: flex;
            gap: 10px;
        }
        .tab-content {
            background: white;
            padding: 20px;
            border-radius: 0 0 15px 15px;
            min-height: 0;
            height: auto;
            overflow: visible;
        }

        .tab-pane {
            min-height: 0;
            height: auto;
        }

        .tab-pane:not(.active) {
            height: 0;
            overflow: hidden;
            padding: 0;
            margin: 0;
        }
        /* Tab navigation styles */
        .nav-tabs {
            border-bottom: none !important;
        }

        .nav-tabs .nav-link {
            color: rgba(255,255,255,0.8);
            border: none;
            padding: 10px 20px;
            background: transparent;
            margin: 0 2px;
            border-radius: 10px;
            transition: all 0.3s ease;
            min-width: 90px;
            text-align: center;
            font-size: 14px;
        }

        .nav-tabs .nav-link:hover {
            background: rgba(255,255,255,0.1);
            color: white;
            transform: translateY(-2px);
        }

        .nav-tabs .nav-link.active {
            background: rgba(255,255,255,0.2) !important;
            color: white !important;
            font-weight: bold;
        }

        /* Fix select box styles */
        .form-select { 
            background-color: white;
            color: #495057;
        }

        .form-select option { 
            background-color: white;
            color: #495057;
        }

        .form-select option:checked { 
            background-color: #667eea;
            color: white;
        }
        .feature-badge {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            margin: 5px;
            min-width: 120px;
            text-align: center;
        }

        /* Fixed width inputs for consistency */
        #config-name, #sub-config-name {
            width: 100%;
        }

        #links-input, #sub-url {
            width: 100%;
        }

        /* Rule template select */
        #rule-template {
            width: 100%;
        }

        /* Custom dropdown for rule template */
        .custom-dropdown {
            position: relative;
            width: 100%;
            z-index: 1000;
        }

        /* Ensure parent containers allow dropdown to overflow */
        .custom-dropdown .col-md-6,
        .custom-dropdown .row,
        .card-body,
        .section-content {
            overflow: visible !important;
        }

        .custom-dropdown-selected {
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 10px 40px 10px 12px;
            background: white;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
            min-height: 42px;
            position: relative;
            z-index: 101;
        }

        .custom-dropdown-selected:hover {
            border-color: #667eea;
        }

        .custom-dropdown-selected.active {
            border-color: #667eea;
            box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
            z-index: 1001;
        }

        .custom-dropdown-arrow {
            position: absolute;
            right: 12px;
            top: 50%;
            transform: translateY(-50%);
            transition: transform 0.3s ease;
            pointer-events: none;
            z-index: 102;
        }

        .custom-dropdown-arrow svg {
            width: 18px;
            height: 18px;
            stroke: #667eea;
            fill: none;
        }

        .custom-dropdown-selected.active .custom-dropdown-arrow {
            transform: translateY(-50%) rotate(180deg);
        }

        .custom-dropdown-menu {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: white;
            border: 2px solid #667eea;
            border-radius: 8px;
            margin-top: 4px;
            max-height: 300px;
            overflow-y: auto;
            z-index: 9999;
            box-shadow: 0 8px 24px rgba(0,0,0,0.25);
            display: none;
        }

        .custom-dropdown-menu.show {
            display: block;
        }

        .custom-dropdown-option {
            padding: 10px 12px;
            cursor: pointer;
            transition: background 0.2s ease;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.95rem;
        }

        .custom-dropdown-option:hover {
            background: #f8f9fa;
        }

        .custom-dropdown-option.selected {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            font-weight: 500;
        }

        .custom-dropdown-option .material-symbols-outlined {
            font-size: 18px;
        }

        .custom-dropdown-option.builtin {
            color: #2196F3;
        }

        .custom-dropdown-option.custom {
            color: #4CAF50;
        }

        /* Simple dropdown variant (no icons, just text) */
        .custom-dropdown-simple .custom-dropdown-selected {
            padding: 10px 40px 10px 12px;
        }

        .custom-dropdown-simple .custom-dropdown-option {
            padding: 10px 15px;
            justify-content: flex-start;
        }

        /* Copy and download buttons */
        #output .btn-sm {
            min-width: 140px;
            margin-right: 10px;
        }
        .history-item {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
        }

        .history-info {
            flex: 1;
        }

        .history-info a {
            color: #667eea;
            word-break: break-all;
            text-decoration: none;
        }

        .history-info a:hover {
            text-decoration: underline;
        }

        .history-actions {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 10px;
        }

        .history-actions .btn-sm {
            min-width: 70px;
        }

        /* Node preview styles */
        .node-item { 
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            border-left: 4px solid #28a745;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .node-info { 
            flex: 1;
        }

        .node-name-edit {
            width: 200px;
        }

        /* Main title section styles */
        .main-title-section {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin-bottom: 20px;
        }

        .main-logo {
            height: 80px;
            width: auto;
            filter: drop-shadow(0 4px 15px rgba(0,0,0,0.3));
        }

        .main-title-text {
            margin: 0;
            color: white;
            font-weight: bold;
            font-size: 3rem;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }

        /* Settings styles */
        .settings-section {
            margin-bottom: 30px;
        }

        .settings-section-title {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 20px;
            border-radius: 10px 10px 0 0;
            margin-bottom: 0;
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .settings-icon {
            font-size: 1.3rem;
        }

        .settings-card {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 0 0 10px 10px;
            padding: 25px;
        }

        .settings-collapse-section {
            margin-bottom: 12px;
        }

        .settings-collapse-section:last-of-type {
            margin-bottom: 0;
        }

        .settings-collapse-header {
            border-radius: 8px;
            border-left: 4px solid #667eea;
            position: relative;
        }

        .settings-collapse-header:hover {
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15);
        }

        /* Settings tab specific styles */
        #settings .converter-section {
            padding-bottom: 10px;
            min-height: auto !important;
        }

        #settings .config-section:last-child {
            margin-bottom: 0;
        }

        /* Force tab-panes to fit content */
        #settings {
            min-height: auto !important;
            height: auto !important;
        }

        .maintenance-item {
            text-align: center;
            padding: 15px;
            background: white;
            border-radius: 10px;
            height: 100%;
        }

        .maintenance-item h6 {
            color: #667eea;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .form-check-input:checked {
            background-color: #667eea;
            border-color: #667eea;
        }

        /* API Documentation tab styles */
        .alert-info code {
            background: #f1f3f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.9em;
        }

        .alert-info pre {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 10px;
            margin-top: 10px;
            overflow-x: auto;
        }

        .alert-info h5 {
            color: #495057;
            font-weight: 600;
            margin-bottom: 10px;
        }

        /* Rule view form styles */
        .rule-view-form {
            background: white;
            border: 2px solid #28a745;
            border-radius: 10px;
            padding: 20px;
            margin-top: 10px;
            animation: slideDown 0.3s ease;
        }

        @keyframes slideDown {
            from {
                opacity: 0;
                max-height: 0;
                padding-top: 0;
                padding-bottom: 0;
            }
            to {
                opacity: 1;
                max-height: 500px;
                padding-top: 20px;
                padding-bottom: 20px;
            }
        }

        /* Modal close button for white background */
        .btn-close-white {
            filter: brightness(0) invert(1);
        }
    {% endraw %}
    </style>
</head>
<body>
    <!-- Language selector in top-right corner -->
    <div class="language-selector-corner">
        <div class="language-dropdown">
            <div class="language-button">
                <span class="language-icon">
                    <span class="material-symbols-outlined" style="font-size: 20px;">translate</span>
                </span>
                <span class="language-current">{{ current_lang_display }}</span>
            </div>
            <div class="language-menu">
                <div class="language-option {{ 'active' if lang == 'en' else '' }}" onclick="changeLanguage('en')">
                    EN
                </div>
                <div class="language-option {{ 'active' if lang == 'zh' else '' }}" onclick="changeLanguage('zh')">
                    中文
                </div>
            </div>
        </div>
    </div>

    <!-- GitHub link in top-left corner -->
    <a href="https://github.com/maxiao0234/SubProtoX" target="_blank" class="github-link-corner">
        <svg width="20" height="20" viewBox="0 0 24 24">
            <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.30.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
        </svg>
        GitHub
        <span class="github-stars" id="github-stars">
            <svg viewBox="0 0 16 16">
                <path d="M8 0.25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25z"/>
            </svg>
            <span id="star-count">-</span>
        </span>
    </a>

    <div class="main-container">
        <div class="header-section">
            <div class="text-center">
                <div class="main-title-section">
                    <img src="/static/logo/logo.png" alt="SubProtoX Logo" class="main-logo">
                    <h1 class="main-title-text">SubProtoX</h1>
                </div>
                <p class="lead">{{ main_subtitle }}</p>
                <div>
                    <span class="feature-badge">{{ features_ssl }}</span>
                    <span class="feature-badge">{{ features_realtime }}</span>
                    <span class="feature-badge">{{ features_rules }}</span>
                    <span class="feature-badge">{{ features_routing }}</span>
                </div>
            </div>
        </div>

        <div class="card-custom">
            <div class="card-header-custom">
                <div class="nav-tabs-container">
                    <ul class="nav nav-tabs border-0" role="tablist">
                        <li class="nav-item">
                            <a class="nav-link {{ 'active' if active_tab == 'converter' else '' }}" data-bs-toggle="tab" href="#converter">{{ tabs_converter }}</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link {{ 'active' if active_tab == 'history' else '' }}" data-bs-toggle="tab" href="#history">{{ tabs_history }}</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link {{ 'active' if active_tab == 'rules' else '' }}" data-bs-toggle="tab" href="#rules">{{ tabs_rules }}</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link {{ 'active' if active_tab == 'settings' else '' }}" data-bs-toggle="tab" href="#settings">{{ tabs_settings }}</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link {{ 'active' if active_tab == 'api' else '' }}" data-bs-toggle="tab" href="#api">{{ tabs_api }}</a>
                        </li>
                    </ul>
                    <div class="tab-actions">
                        <a href="/logout" class="btn logout-btn">{{ logout_btn }}</a>
                        <button class="restart-btn" onclick="restartService()">
                            <span class="material-symbols-outlined icon-btn">bolt</span>
                            {{ restart_btn }}
                        </button>
                    </div>
                </div>
            </div>

            <div class="tab-content">
                <!-- Converter tab -->
                <div id="converter" class="tab-pane fade {{ 'show active' if active_tab == 'converter' else '' }}">
                    <div class="converter-section">
                        <!-- Page Header -->
                        <div style="text-align: center; margin-bottom: 35px;">
                            <h2 style="color: #667eea; font-weight: 700; font-size: 2rem; margin-bottom: 10px;">
                                <span class="material-symbols-outlined icon-page-title" style="color: #667eea;">rocket_launch</span> {{ converter_page_title }}
                            </h2>
                            <p style="color: #6c757d; font-size: 1rem; margin: 0;">
                                {{ converter_page_subtitle }}
                            </p>
                        </div>

                        <!-- Step 1: Conversion Mode Selection -->
                        <div class="config-section">
                            <div class="section-header">
                                <span class="step-badge">1</span>
                                <h5>{{ converter_select_conversion_mode }}</h5>
                            </div>
                            <div class="section-content">
                                <div class="row">
                                    <div class="col-md-6 mb-3 mb-md-0">
                                        <div class="conversion-type-card" id="card-links" onclick="selectConversionType('links')" style="cursor: pointer; border: 2px solid #667eea; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); border-radius: 12px; padding: 20px; transition: all 0.3s ease; position: relative; min-height: 180px;">
                                            <div style="display: flex; align-items: start; margin-bottom: 10px;">
                                                <input class="form-check-input" type="radio" name="conversion-type" id="type-links" value="links" checked onchange="switchConversionType()" style="margin-top: 5px; cursor: pointer;">
                                                <div style="margin-left: 12px; flex: 1;">
                                                    <h5 style="margin: 0 0 8px 0; color: #667eea; font-weight: 600; font-size: 1.1rem;">
                                                        {{ converter_proxy_links }}
                                                    </h5>
                                                    <p style="margin: 0; color: #666; font-size: 0.9rem; line-height: 1.5;">
                                                        {{ converter_proxy_links_desc }}
                                                    </p>
                                                    <div style="margin-top: 8px;">
                                                        <span style="background: #667eea; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 500;">
                                                            <span class="material-symbols-outlined" style="font-size: 14px; vertical-align: middle;">edit</span> {{ converter_support_node_editing }}
                                                        </span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="conversion-type-card" id="card-subscription" onclick="selectConversionType('subscription')" style="cursor: pointer; border: 2px solid #ddd; background: #f8f9fa; border-radius: 12px; padding: 20px; transition: all 0.3s ease; position: relative; min-height: 180px;">
                                            <div style="display: flex; align-items: start; margin-bottom: 10px;">
                                                <input class="form-check-input" type="radio" name="conversion-type" id="type-subscription" value="subscription" onchange="switchConversionType()" style="margin-top: 5px; cursor: pointer;">
                                                <div style="margin-left: 12px; flex: 1;">
                                                    <h5 style="margin: 0 0 8px 0; color: #666; font-weight: 600; font-size: 1.1rem;">
                                                        {{ converter_subscription_url }}
                                                    </h5>
                                                    <p style="margin: 0; color: #666; font-size: 0.9rem; line-height: 1.5;">
                                                        {{ converter_subscription_url_desc }}
                                                    </p>
                                                    <div style="margin-top: 8px;">
                                                        <span style="background: #6c757d; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 500;">
                                                            <span class="material-symbols-outlined" style="font-size: 14px; vertical-align: middle;">flash_on</span> {{ converter_one_step_conversion }}
                                                        </span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Step 2: Input Area -->
                        <div class="config-section">
                            <div class="section-header">
                                <span class="step-badge">2</span>
                                <h5 id="input-section-title">{{ converter_paste_proxy_links }}</h5>
                            </div>
                            <div class="section-content">
                                <!-- Input Area for Proxy Links -->
                                <div id="links-input-area">
                                    <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; border: 2px dashed #dee2e6;">
                                        <div class="d-flex align-items-center mb-2">
                                            <span class="material-symbols-outlined icon-board" style="color: #667eea;">content_paste</span>
                                            <label class="form-label mb-0" style="font-weight: 500; color: #495057;">
                                                {{ converter_link_input_label }}
                                            </label>
                                        </div>
                                        <textarea id="links-input" class="form-control" rows="5"
                                            placeholder="vless://uuid@server:port?...&#10;vmess://base64...&#10;trojan://password@server:port..."
                                            style="border: 2px solid #e0e0e0; border-radius: 8px; font-family: 'Courier New', monospace; font-size: 0.9rem;"></textarea>
                                        <small class="text-muted mt-2" style="display: block;">
                                            <span class="material-symbols-outlined icon-inline" style="color: #667eea;">lightbulb</span> {{ converter_one_link_per_line }}
                                        </small>
                                    </div>
                                </div>

                                <!-- Input Area for Subscription URL -->
                                <div id="subscription-input-area" style="display: none;">
                                    <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; border: 2px dashed #dee2e6;">
                                        <div class="d-flex align-items-center mb-2">
                                            <span class="material-symbols-outlined icon-board" style="color: #667eea;">link</span>
                                            <label class="form-label mb-0" style="font-weight: 500; color: #495057;">
                                                {{ converter_sub_input_label }}
                                            </label>
                                        </div>
                                        <textarea id="sub-url" class="form-control" rows="5"
                                            placeholder="https://example.com/sub"
                                            style="border: 2px solid #e0e0e0; border-radius: 8px; font-family: 'Courier New', monospace; font-size: 0.9rem;"></textarea>
                                        <small class="text-muted mt-2" style="display: block;">
                                            <span class="material-symbols-outlined icon-inline" style="color: #667eea;">lightbulb</span> Enter your subscription URL here
                                        </small>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Step 3: Basic Configuration -->
                        <div class="config-section" id="step-basic-config">
                            <div class="section-header">
                                <span class="step-badge">3</span>
                                <h5>{{ converter_basic_configuration }}</h5>
                            </div>
                            <div class="section-content" id="basic-config-content">
                                <div class="card" style="border: none; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-radius: 12px; overflow: visible;">
                                    <div class="card-body" style="padding: 20px;">
                                        <div class="row g-3">
                                            <div class="col-md-6">
                                                <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 15px; border-radius: 10px; border-left: 4px solid #667eea; overflow: visible;">
                                                    <label class="form-label d-flex align-items-center" style="font-weight: 600; color: #495057; margin-bottom: 10px;">
                                                        <span class="material-symbols-outlined icon-board" style="color: #667eea;">edit_note</span>
                                                        <span>{{ converter_config_name }}</span>
                                                    </label>
                                                    <input type="text" id="config-name" class="form-control"
                                                        placeholder="{{ converter_config_placeholder }}"
                                                        value="{{ converter_config_default }}"
                                                        style="border: 2px solid #e0e0e0; border-radius: 8px; padding: 10px 12px; background: white; transition: all 0.3s ease;">
                                                    <small class="text-muted mt-2" style="display: block; font-size: 0.85rem; padding-left: 2px;">
                                                        <span class="material-symbols-outlined icon-inline" style="color: #667eea;">lightbulb</span> {{ converter_custom_name_hint }}
                                                    </small>
                                                </div>
                                            </div>

                                            <div class="col-md-6">
                                                <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 15px; border-radius: 10px; border-left: 4px solid #6e64c6; overflow: visible;">
                                                    <label class="form-label d-flex align-items-center" style="font-weight: 600; color: #495057; margin-bottom: 10px;">
                                                        <span class="material-symbols-outlined icon-board" style="color: #6e64c6;">checklist</span>
                                                        <span>{{ converter_rule_template }}</span>
                                                    </label>
                                                    <!-- Custom dropdown instead of native select -->
                                                    <div class="custom-dropdown" id="rule-template-dropdown">
                                                        <div class="custom-dropdown-selected" id="rule-selected" onclick="toggleRuleDropdown()">
                                                            <span class="material-symbols-outlined" style="font-size: 18px; color: #2196F3;">widgets</span>
                                                            <span id="rule-selected-text">Loading...</span>
                                                        </div>
                                                        <div class="custom-dropdown-arrow">
                                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                                                <polyline points="6 9 12 15 18 9"></polyline>
                                                            </svg>
                                                        </div>
                                                        <div class="custom-dropdown-menu" id="rule-menu">
                                                            <!-- Options will be populated by JavaScript -->
                                                        </div>
                                                    </div>
                                                    <!-- Hidden input to store selected value -->
                                                    <input type="hidden" id="rule-template" value="">
                                                    <small class="text-muted mt-2" style="display: block; font-size: 0.85rem; padding-left: 2px;">
                                                        <span style="font-weight: 500; color: #495057; margin-right: 8px;"><span class="material-symbols-outlined icon-inline" style="color: #6e64c6; font-size: 18px;">bookmark</span> {{ converter_rule_types }}</span>
                                                        <span style="display: inline-flex; align-items: center; gap: 6px;">
                                                            <span style="background: linear-gradient(135deg, rgba(33, 150, 243, 0.1) 0%, rgba(33, 150, 243, 0.05) 100%); color: #2196F3; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 500; border: 1px solid rgba(33, 150, 243, 0.2);">
                                                                <span class="material-symbols-outlined" style="font-size: 14px; vertical-align: middle; margin-right: 4px;">widgets</span>{{ converter_built_in }}
                                                            </span>
                                                            <span style="background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(76, 175, 80, 0.05) 100%); color: #4CAF50; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 500; border: 1px solid rgba(76, 175, 80, 0.2);">
                                                                <span class="material-symbols-outlined" style="font-size: 14px; vertical-align: middle; margin-right: 4px;">edit_square</span>{{ converter_custom }}
                                                            </span>
                                                        </span>
                                                    </small>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Step 4: Advanced Settings -->
                        <div class="config-section">
                            <div class="section-header">
                                <span class="step-badge">4</span>
                                <h5>{{ converter_subscription_settings }}</h5>
                            </div>
                            <div class="section-content">
                                <div class="card" style="border: none; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-radius: 12px; overflow: visible;">
                                    <div class="card-body" style="padding: 20px; background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); overflow: visible;">
                                        <div class="row g-3" style="overflow: visible;">
                                            <!-- Auto-Update Card -->
                                            <div class="col-md-4">
                                                <div style="padding: 15px; background: white; border-radius: 10px; border: 2px solid #e9ecef; height: 100%; display: flex; flex-direction: column;">
                                                    <!-- Icon -->
                                                    <div style="text-align: center; margin-bottom: 12px;">
                                                        <span class="material-symbols-outlined" style="font-size: 48px; color: #667eea; font-variation-settings: 'FILL' 0, 'wght' 300, 'GRAD' 0, 'opsz' 48;">refresh</span>
                                                    </div>
                                                    <!-- Label -->
                                                    <label class="form-label text-center d-block" style="font-weight: 600; color: #495057; margin-bottom: 15px; height: 24px; display: flex; align-items: center; justify-content: center;">
                                                        {{ converter_auto_update }}
                                                    </label>
                                                    <!-- Control (Switch) -->
                                                    <div style="flex: 1; display: flex; align-items: center; justify-content: center; min-height: 42px;">
                                                        <div class="form-check form-switch">
                                                            <input class="form-check-input" type="checkbox" id="auto-update-enabled" style="cursor: pointer; width: 48px; height: 24px;">
                                                        </div>
                                                    </div>
                                                    <!-- Description -->
                                                    <small class="text-muted d-block text-center" style="margin-top: 10px; height: 18px; display: flex; align-items: center; justify-content: center;">{{ converter_enable_periodic_refresh }}</small>
                                                </div>
                                            </div>

                                            <!-- Update Interval Card -->
                                            <div class="col-md-4">
                                                <div style="padding: 15px; background: white; border-radius: 10px; border: 2px solid #e9ecef; height: 100%; display: flex; flex-direction: column;">
                                                    <!-- Icon -->
                                                    <div style="text-align: center; margin-bottom: 12px;">
                                                        <span class="material-symbols-outlined" style="font-size: 48px; color: #667eea; font-variation-settings: 'FILL' 0, 'wght' 300, 'GRAD' 0, 'opsz' 48;">schedule</span>
                                                    </div>
                                                    <!-- Label -->
                                                    <label class="form-label text-center d-block" style="font-weight: 600; color: #495057; margin-bottom: 15px; height: 24px; display: flex; align-items: center; justify-content: center;">
                                                        {{ converter_update_interval }}
                                                    </label>
                                                    <!-- Control (Input + Unit Dropdown) -->
                                                    <div style="flex: 1; display: flex; align-items: center; justify-content: center; min-height: 42px;">
                                                        <div style="display: flex; gap: 8px; width: 100%; max-width: 280px;">
                                                            <!-- Number Input -->
                                                            <input type="number" id="update-interval-value" class="form-control" value="0" min="0" style="flex: 1; text-align: center; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 1rem; padding: 8px;">
                                                            <!-- Unit Custom Dropdown -->
                                                            <div class="custom-dropdown custom-dropdown-simple" id="interval-unit-dropdown" style="flex: 0 0 auto; width: 110px;">
                                                                <div class="custom-dropdown-selected" id="interval-unit-selected" onclick="toggleIntervalUnitDropdown()">
                                                                    <span id="interval-unit-selected-text">{{ converter_interval_hours }}</span>
                                                                </div>
                                                                <div class="custom-dropdown-arrow">
                                                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                                                        <polyline points="6 9 12 15 18 9"></polyline>
                                                                    </svg>
                                                                </div>
                                                                <div class="custom-dropdown-menu" id="interval-unit-menu">
                                                                    <div class="custom-dropdown-option selected" data-value="60" onclick="selectIntervalUnit(60, '{{ converter_interval_hours }}')">{{ converter_interval_hours }}</div>
                                                                    <div class="custom-dropdown-option" data-value="1" onclick="selectIntervalUnit(1, '{{ converter_interval_minutes }}')">{{ converter_interval_minutes }}</div>
                                                                    <div class="custom-dropdown-option" data-value="1440" onclick="selectIntervalUnit(1440, '{{ converter_interval_days }}')">{{ converter_interval_days }}</div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                        <input type="hidden" id="update-interval-unit" value="60">
                                                        <input type="hidden" id="update-interval" value="0">
                                                    </div>
                                                    <!-- Description -->
                                                    <small class="text-muted d-block text-center" style="margin-top: 10px; height: 18px; display: flex; align-items: center; justify-content: center;">{{ converter_interval_zero_no_update }}</small>
                                                </div>
                                            </div>

                                            <!-- Traffic Limit Card -->
                                            <div class="col-md-4">
                                                <div style="padding: 15px; background: white; border-radius: 10px; border: 2px solid #e9ecef; height: 100%; display: flex; flex-direction: column;">
                                                    <!-- Icon -->
                                                    <div style="text-align: center; margin-bottom: 12px;">
                                                        <span class="material-symbols-outlined" style="font-size: 48px; color: #667eea; font-variation-settings: 'FILL' 0, 'wght' 300, 'GRAD' 0, 'opsz' 48;">speed</span>
                                                    </div>
                                                    <!-- Label -->
                                                    <label class="form-label text-center d-block" style="font-weight: 600; color: #495057; margin-bottom: 15px; height: 24px; display: flex; align-items: center; justify-content: center;">
                                                        {{ converter_traffic_limit }}
                                                    </label>
                                                    <!-- Control (Input) -->
                                                    <div style="flex: 1; display: flex; align-items: center; justify-content: center; min-height: 42px;">
                                                        <input type="number" id="traffic-limit" class="form-control"
                                                            placeholder="0 = Unlimited" value="0" min="0" max="10000"
                                                            style="border: 2px solid #e0e0e0; border-radius: 8px; text-align: center; height: 42px;">
                                                    </div>
                                                    <!-- Description -->
                                                    <small class="text-muted d-block text-center" style="margin-top: 10px; height: 18px; display: flex; align-items: center; justify-content: center;">{{ converter_zero_unlimited }}</small>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Convert Button -->
                        <div style="text-align: center; margin-top: 30px;">
                            <button class="btn btn-convert" onclick="convertToClash()">{{ converter_convert_btn }}</button>
                        </div>

                        <!-- Node preview and name editing area (only for proxy links mode) -->
                        <div id="nodes-preview" class="mt-4" style="display:none;">
                            <div class="config-section">
                                <div class="section-header">
                                    <span class="step-badge">✓</span>
                                    <h5>{{ converter_node_preview }}</h5>
                                </div>
                                <div class="section-content">
                                    <div id="nodes-list"></div>
                                    <div style="text-align: center; margin-top: 20px;">
                                        <button class="btn btn-success" onclick="generateConfig()" style="border-radius: 10px; padding: 12px 35px; font-weight: 600;">
                                            <span class="material-symbols-outlined icon-btn">check_circle</span>{{ converter_generate_btn }}
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Output Area -->
                        <div id="output" class="output-box" style="display:none;">
                            <div class="config-section">
                                <div class="section-header" style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%);">
                                    <span class="step-badge" style="background: white; color: #28a745;">✓</span>
                                    <h5 style="color: white; margin: 0;">{{ converter_result_title }}</h5>
                                </div>
                                <div class="section-content">
                                    <div id="result-content" style="background: #f8f9fa; padding: 20px; border-radius: 10px; font-family: monospace;"></div>
                                    <div style="text-align: center; margin-top: 20px;">
                                        <button class="btn btn-primary" onclick="copyResult()" style="border-radius: 10px; padding: 10px 25px; margin: 0 5px;">
                                            <span class="material-symbols-outlined icon-btn">content_paste</span>{{ converter_copy_btn }}
                                        </button>
                                        <button class="btn btn-success" onclick="downloadResult()" style="border-radius: 10px; padding: 10px 25px; margin: 0 5px;">
                                            <span class="material-symbols-outlined icon-btn">download</span>{{ converter_download_btn }}
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- History tab -->
                <div id="history" class="tab-pane fade {{ 'show active' if active_tab == 'history' else '' }}">
                    <div class="converter-section">
                        <!-- Page Header -->
                        <div style="text-align: center; margin-bottom: 35px;">
                            <h2 style="color: #667eea; font-weight: 700; font-size: 2rem; margin-bottom: 10px;">
                                <span class="material-symbols-outlined icon-page-title" style="color: #667eea;">history</span> {{ history_page_title }}
                            </h2>
                            <p style="color: #6c757d; font-size: 1rem; margin: 0;">
                                {{ history_page_subtitle }}
                            </p>
                        </div>

                        <!-- History List Section -->
                        <div class="config-section">
                            <div class="section-header">
                                <div style="display: flex; align-items: center; gap: 12px; flex: 1;">
                                    <span class="icon-section history" style="color: #667eea;"></span>
                                    <h5 style="margin: 0;">{{ history_records }}</h5>
                                </div>
                                <button class="btn btn-danger btn-sm" onclick="clearAllHistory()" style="border-radius: 8px; padding: 6px 20px;">
                                    <span class="material-symbols-outlined icon-btn">delete</span>{{ history_clear_all }}
                                </button>
                            </div>
                            <div class="section-content">
                                <div id="history-list"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Rule management tab -->
                <div id="rules" class="tab-pane fade {{ 'show active' if active_tab == 'rules' else '' }}">
                    <div class="converter-section">
                        <!-- Page Header -->
                        <div style="text-align: center; margin-bottom: 35px;">
                            <h2 style="color: #667eea; font-weight: 700; font-size: 2rem; margin-bottom: 10px;">
                                <span class="material-symbols-outlined icon-page-title" style="color: #667eea;">folder_open</span> {{ rules_page_title }}
                            </h2>
                            <p style="color: #6c757d; font-size: 1rem; margin: 0;">
                                {{ rules_page_subtitle }}
                            </p>
                        </div>

                        <!-- Compact Quick Reference Cards -->
                        <div class="row mb-3">
                            <!-- Rule Editing Guide Card -->
                            <div class="col-lg-6 mb-2 mb-lg-0">
                                <div class="card border-0 h-100" style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%); border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                                    <div class="card-body" style="padding: 18px;">
                                        <h6 class="mb-2" style="color: #667eea; font-weight: 700; font-size: 1.05em; display: flex; align-items: center; gap: 8px;">
                                            <span class="material-symbols-outlined" style="font-size: 24px; color: #667eea;">lightbulb</span>
                                            <span>{{ rules_editing_guide }}</span>
                                        </h6>
                                        <div style="font-size: 0.85em;">
                                            <!-- Built-in Rules -->
                                            <div class="mb-2 pb-2" style="border-bottom: 1px solid rgba(102, 126, 234, 0.15);">
                                                <div class="d-flex align-items-start gap-2">
                                                    <span style="background: linear-gradient(135deg, rgba(33, 150, 243, 0.15) 0%, rgba(33, 150, 243, 0.08) 100%); color: #2196F3; padding: 3px 10px; border-radius: 10px; font-size: 0.75rem; font-weight: 600; border: 1px solid rgba(33, 150, 243, 0.25); white-space: nowrap; display: inline-flex; align-items: center; gap: 3px;">
                                                        <span class="material-symbols-outlined" style="font-size: 13px;">widgets</span>{{ converter_built_in }}
                                                    </span>
                                                    <div style="flex: 1;">
                                                        <strong style="font-size: 0.9em; color: #2c3e50;">{{ rules_built_in_templates }}</strong>
                                                        <p class="mb-0 text-muted" style="font-size: 0.82em; line-height: 1.4; margin-top: 2px;">
                                                            {{ rules_built_in_desc }}
                                                        </p>
                                                    </div>
                                                </div>
                                            </div>

                                            <!-- Custom Rules -->
                                            <div class="mb-2 pb-2" style="border-bottom: 1px solid rgba(76, 175, 80, 0.15);">
                                                <div class="d-flex align-items-start gap-2">
                                                    <span style="background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(76, 175, 80, 0.08) 100%); color: #4CAF50; padding: 3px 10px; border-radius: 10px; font-size: 0.75rem; font-weight: 600; border: 1px solid rgba(76, 175, 80, 0.25); white-space: nowrap; display: inline-flex; align-items: center; gap: 3px;">
                                                        <span class="material-symbols-outlined" style="font-size: 13px;">edit_square</span>{{ converter_custom }}
                                                    </span>
                                                    <div style="flex: 1;">
                                                        <strong style="font-size: 0.9em; color: #2c3e50;">{{ rules_custom_rules }}</strong>
                                                        <p class="mb-0 text-muted" style="font-size: 0.82em; line-height: 1.4; margin-top: 2px;">
                                                            {{ rules_custom_desc }}
                                                        </p>
                                                    </div>
                                                </div>
                                            </div>

                                            <!-- Quick Tips -->
                                            <div style="padding: 10px; background: rgba(255, 255, 255, 0.7); border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.2);">
                                                <strong class="d-flex align-items-center gap-2 mb-1" style="color: #667eea; font-size: 0.85em;">
                                                    <span class="material-symbols-outlined" style="font-size: 16px;">tips_and_updates</span>
                                                    <span>{{ rules_quick_tips }}</span>
                                                </strong>
                                                <div style="line-height: 1.5; color: #5a6c7d; font-size: 0.82em;">
                                                    • {{ rules_quick_tip_one_rule }} <code style="font-size: 0.9em; padding: 1px 5px; background: rgba(102, 126, 234, 0.1); border-radius: 3px; color: #667eea;">#</code> {{ rules_quick_tip_for_comments }}<br>
                                                    • {{ rules_quick_tip_top_to_bottom }}<br>
                                                    • {{ rules_quick_tip_end_with_match }} <code style="font-size: 0.9em; padding: 1px 5px; background: rgba(102, 126, 234, 0.1); border-radius: 3px; color: #667eea;">MATCH</code> {{ rules_quick_tip_as_fallback }}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Rule Syntax Reference Card -->
                            <div class="col-lg-6">
                                <div class="card border-0 h-100" style="background: linear-gradient(135deg, rgba(118, 75, 162, 0.08) 0%, rgba(102, 126, 234, 0.08) 100%); border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                                    <div class="card-body" style="padding: 18px;">
                                        <h6 class="mb-2" style="color: #764ba2; font-weight: 700; font-size: 1.05em; display: flex; align-items: center; gap: 8px;">
                                            <span class="material-symbols-outlined" style="font-size: 24px; color: #764ba2;">build</span>
                                            <span>{{ rules_syntax_reference }}</span>
                                        </h6>
                                        <div style="font-size: 0.82em; line-height: 1.4;">
                                            <!-- Domain Matching -->
                                            <div class="mb-2">
                                                <h6 class="mb-1" style="font-size: 0.9em; font-weight: 600; color: #667eea; display: flex; align-items: center; gap: 5px;">
                                                    <span class="material-symbols-outlined" style="font-size: 16px;">language</span>
                                                    <span>{{ rules_syntax_domain_matching }}</span>
                                                </h6>
                                                <div class="ps-2" style="font-size: 0.95em;">
                                                    <div style="margin-bottom: 4px;">
                                                        <code style="font-size: 0.82em; color: #495057; background: rgba(255,255,255,0.6); padding: 1px 5px; border-radius: 3px;">DOMAIN-SUFFIX,google.com,Proxy</code>
                                                        <small class="text-muted ms-1" style="font-size: 0.8em;">→ {{ rules_syntax_match_wildcard }}</small>
                                                    </div>
                                                    <div style="margin-bottom: 4px;">
                                                        <code style="font-size: 0.82em; color: #495057; background: rgba(255,255,255,0.6); padding: 1px 5px; border-radius: 3px;">DOMAIN,www.google.com,DIRECT</code>
                                                        <small class="text-muted ms-1" style="font-size: 0.8em;">→ {{ rules_syntax_exact_match }}</small>
                                                    </div>
                                                </div>
                                            </div>

                                            <!-- IP & Geo Matching -->
                                            <div class="mb-2">
                                                <h6 class="mb-1" style="font-size: 0.9em; font-weight: 600; color: #28a745; display: flex; align-items: center; gap: 5px;">
                                                    <span class="material-symbols-outlined" style="font-size: 16px;">public</span>
                                                    <span>{{ rules_syntax_ip_geo_matching }}</span>
                                                </h6>
                                                <div class="ps-2" style="font-size: 0.95em;">
                                                    <div style="margin-bottom: 4px;">
                                                        <code style="font-size: 0.82em; color: #495057; background: rgba(255,255,255,0.6); padding: 1px 5px; border-radius: 3px;">IP-CIDR,192.168.0.0/16,DIRECT</code>
                                                        <small class="text-muted ms-1" style="font-size: 0.8em;">→ {{ rules_syntax_private_ip }}</small>
                                                    </div>
                                                    <div style="margin-bottom: 4px;">
                                                        <code style="font-size: 0.82em; color: #495057; background: rgba(255,255,255,0.6); padding: 1px 5px; border-radius: 3px;">GEOIP,CN,DIRECT</code>
                                                        <small class="text-muted ms-1" style="font-size: 0.8em;">→ {{ rules_syntax_china_ips }}</small>
                                                    </div>
                                                </div>
                                            </div>

                                            <!-- Advanced Rules -->
                                            <div>
                                                <h6 class="mb-1" style="font-size: 0.9em; font-weight: 600; color: #ffc107; display: flex; align-items: center; gap: 5px;">
                                                    <span class="material-symbols-outlined" style="font-size: 16px;">settings</span>
                                                    <span>{{ rules_syntax_advanced_rules }}</span>
                                                </h6>
                                                <div class="ps-2" style="font-size: 0.95em;">
                                                    <div style="margin-bottom: 4px;">
                                                        <code style="font-size: 0.82em; color: #495057; background: rgba(255,255,255,0.6); padding: 1px 5px; border-radius: 3px;">PROCESS-NAME,chrome,Proxy</code>
                                                        <small class="text-muted ms-1" style="font-size: 0.8em;">→ {{ rules_syntax_by_process }}</small>
                                                    </div>
                                                    <div style="margin-bottom: 4px;">
                                                        <code style="font-size: 0.82em; color: #495057; background: rgba(255,255,255,0.6); padding: 1px 5px; border-radius: 3px;">MATCH,🚀 Proxy</code>
                                                        <small class="text-muted ms-1" style="font-size: 0.8em;">→ {{ rules_syntax_catch_all }}</small>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Built-in Templates Section -->
                        <div class="mb-4">
                            <div class="config-section">
                                <div class="section-header">
                                    <div style="display: flex; align-items: center; gap: 12px; flex: 1;">
                                        <span class="icon-section" style="color: #667eea;">
                                            <span class="material-symbols-outlined" style="font-size: 18px;">widgets</span>
                                        </span>
                                        <h5 style="margin: 0;">{{ rules_built_in_templates }}</h5>
                                    </div>
                                </div>
                                <div class="section-content">
                                    <div id="builtin-rules-list"></div>
                                </div>
                            </div>
                        </div>

                        <!-- Custom Rules Section -->
                        <div>
                            <div class="config-section">
                                <div class="section-header" style="display: flex; justify-content: space-between; align-items: center;">
                                    <div style="display: flex; align-items: center; gap: 12px; flex: 1;">
                                        <span class="icon-section" style="color: #28a745;">
                                            <span class="material-symbols-outlined" style="font-size: 18px;">edit_square</span>
                                        </span>
                                        <h5 style="margin: 0;">{{ rules_custom_rules }}</h5>
                                    </div>
                                    <button class="btn btn-primary btn-create-new" onclick="showCreateRuleModal()">
                                        <span style="margin-right: 4px;">+</span>{{ rules_create_new }}
                                    </button>
                                </div>
                                <div class="section-content">
                                    <div id="custom-rules-list"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Settings tab -->
                <div id="settings" class="tab-pane fade {{ 'show active' if active_tab == 'settings' else '' }}" style="min-height: auto;">
                    <div class="converter-section" style="min-height: auto;">
                        <!-- Page Header -->
                        <div style="text-align: center; margin-bottom: 35px;">
                            <h2 style="color: #667eea; font-weight: 700; font-size: 2rem; margin-bottom: 10px;">
                                <span class="material-symbols-outlined icon-page-title" style="color: #667eea;">settings</span> {{ settings_page_title }}
                            </h2>
                            <p style="color: #6c757d; font-size: 1rem; margin: 0;">
                                {{ settings_page_subtitle }}
                            </p>
                        </div>

                        <!-- System Settings Section -->
                        <div class="config-section mb-4">
                            <div class="section-header">
                                <div style="display: flex; align-items: center; gap: 12px; flex: 1;">
                                    <span class="icon-section" style="color: #667eea;">
                                        <span class="material-symbols-outlined" style="font-size: 18px;">tune</span>
                                    </span>
                                    <h5 style="margin: 0;">{{ settings_system_config }}</h5>
                                </div>
                            </div>

                            <div class="section-content" style="padding: 0;">
                                <div class="settings-card" style="padding: 15px; border-radius: 0 0 12px 12px; background: #f8f9fa;">
                                    <!-- Basic Service Configuration - Default Expanded -->
                                    <div class="settings-collapse-section">
                                        <div class="settings-collapse-header" onclick="toggleSettingsSection('basic-service')" style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%); cursor: pointer; padding: 15px 20px; display: flex; align-items: center; justify-content: space-between; transition: all 0.3s ease;">
                                            <div style="display: flex; align-items: center; gap: 10px;">
                                                <span class="material-symbols-outlined" style="color: #667eea; font-size: 20px;">language</span>
                                                <h6 style="margin: 0; color: #495057; font-weight: 600;">{{ settings_basic_service }}</h6>
                                            </div>
                                            <span class="material-symbols-outlined settings-collapse-icon" id="icon-basic-service" style="color: #667eea; font-size: 20px; transition: transform 0.3s ease; transform: rotate(180deg);">expand_more</span>
                                        </div>
                                    <div class="settings-collapse-content" id="content-basic-service" style="padding: 20px; display: block;">
                                        <div class="row">
                                            <div class="col-md-4 mb-3">
                                                <label class="form-label">{{ settings_server_port }}</label>
                                                <div class="input-group">
                                                    <input type="number" id="server-port" class="form-control" placeholder="7777" min="1" max="65535">
                                                    <span class="input-group-text">Port</span>
                                                </div>
                                                <small class="text-muted">{{ settings_current_port }}: {{ server_port }}</small>
                                            </div>
                                            <div class="col-md-4 mb-3">
                                                <label class="form-label">{{ settings_listen_address }}</label>
                                                <input type="text" id="server-host" class="form-control" placeholder="0.0.0.0">
                                                <small class="text-muted">{{ settings_current_host }}: {{ server_host }}</small>
                                            </div>
                                            <div class="col-md-4 mb-3">
                                                <label class="form-label">{{ panel_base_path_label }}</label>
                                                <div class="input-group">
                                                    <span class="input-group-text" style="background-color: #f8f9fa; color: #6c757d; font-family: monospace; user-select: none;">/</span>
                                                    <input type="text" id="panel-base-path" class="form-control" placeholder="subprotox" value="{{ panel_base_path }}" style="font-family: monospace;">
                                                </div>
                                                <small class="text-muted">{{ panel_base_path_current }}</small>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- SSL/HTTPS Configuration - Default Collapsed -->
                                <div class="settings-collapse-section">
                                    <div class="settings-collapse-header" onclick="toggleSettingsSection('ssl-config')" style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%); cursor: pointer; padding: 15px 20px; display: flex; align-items: center; justify-content: space-between; transition: all 0.3s ease;">
                                        <div style="display: flex; align-items: center; gap: 10px;">
                                            <span class="material-symbols-outlined" style="color: #667eea; font-size: 20px;">security</span>
                                            <h6 style="margin: 0; color: #495057; font-weight: 600;">{{ settings_ssl_https_config }}</h6>
                                        </div>
                                        <span class="material-symbols-outlined settings-collapse-icon" id="icon-ssl-config" style="color: #6c757d; font-size: 20px; transition: transform 0.3s ease;">expand_more</span>
                                    </div>
                                    <div class="settings-collapse-content" id="content-ssl-config" style="padding: 20px; display: none;">
                                        <div class="row">
                                            <div class="col-md-6 mb-3" style="overflow: visible;">
                                                <label class="form-label">{{ settings_ssl_status_label }}</label>
                                                <div class="input-group" style="overflow: visible;">
                                                    <div class="custom-dropdown custom-dropdown-simple" id="ssl-enabled-dropdown" style="flex: 1;">
                                                        <div class="custom-dropdown-selected" onclick="toggleDropdown('ssl-enabled-dropdown')">
                                                            <span id="ssl-enabled-text">{{ ssl_option_disabled if ssl_disabled_selected else ssl_option_enabled }}</span>
                                                        </div>
                                                        <div class="custom-dropdown-arrow">
                                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                                                <polyline points="6 9 12 15 18 9"></polyline>
                                                            </svg>
                                                        </div>
                                                        <div class="custom-dropdown-menu">
                                                            <div class="custom-dropdown-option {{ 'selected' if ssl_disabled_selected else '' }}" onclick="selectOption('ssl-enabled', 'false', '{{ ssl_option_disabled }}')">{{ ssl_option_disabled }}</div>
                                                            <div class="custom-dropdown-option {{ 'selected' if ssl_enabled_selected else '' }}" onclick="selectOption('ssl-enabled', 'true', '{{ ssl_option_enabled }}')">{{ ssl_option_enabled }}</div>
                                                        </div>
                                                    </div>
                                                    <input type="hidden" id="ssl-enabled" value="{{ 'false' if ssl_disabled_selected else 'true' }}">
                                                    <span class="input-group-text {{ ssl_status_bg }}">{{ ssl_icon|safe }}</span>
                                                </div>
                                                <small class="text-muted">{{ settings_ssl_current }}: {{ ssl_enabled_text }}</small>
                                            </div>
                                            <div class="col-md-6 mb-3">
                                                <label class="form-label">{{ settings_ssl_domain_label }}</label>
                                                <input type="text" id="ssl-domain" class="form-control" value="{{ ssl_domain }}" placeholder="example.com">
                                                <small class="text-muted">{{ settings_ssl_domain_hint }}</small>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-md-6 mb-3">
                                                <label class="form-label">{{ settings_ssl_cert_path }}</label>
                                                <input type="text" id="ssl-cert" class="form-control" placeholder="/path/to/cert.pem" value="{{ ssl_cert_value }}">
                                                <small class="text-muted">{{ settings_ssl_cert_hint }}</small>
                                            </div>
                                            <div class="col-md-6 mb-3">
                                                <label class="form-label">{{ settings_ssl_key_path }}</label>
                                                <input type="text" id="ssl-key" class="form-control" placeholder="/path/to/key.pem" value="{{ ssl_key_value }}">
                                                <small class="text-muted">{{ settings_ssl_key_hint }}</small>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-12">
                                                <div class="alert alert-info mb-0">
                                                    <strong>{{ settings_ssl_info_title }}:</strong><br>
                                                    • {{ settings_ssl_status }}: <span class="badge {{ ssl_status_class }}">{{ ssl_status_text }}</span><br>
                                                    • {{ settings_ssl_domain_note }}<br>
                                                    • {{ settings_ssl_config_note }}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Logging and Monitoring Configuration - Default Collapsed -->
                                <div class="settings-collapse-section">
                                    <div class="settings-collapse-header" onclick="toggleSettingsSection('logging-config')" style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%); cursor: pointer; padding: 15px 20px; display: flex; align-items: center; justify-content: space-between; transition: all 0.3s ease;">
                                        <div style="display: flex; align-items: center; gap: 10px;">
                                            <span class="material-symbols-outlined" style="color: #667eea; font-size: 20px;">analytics</span>
                                            <h6 style="margin: 0; color: #495057; font-weight: 600;">{{ settings_logging_monitoring }}</h6>
                                        </div>
                                        <span class="material-symbols-outlined settings-collapse-icon" id="icon-logging-config" style="color: #6c757d; font-size: 20px; transition: transform 0.3s ease;">expand_more</span>
                                    </div>
                                    <div class="settings-collapse-content" id="content-logging-config" style="padding: 20px; display: none;">
                                        <div class="row">
                                            <div class="col-md-6 mb-3" style="overflow: visible;">
                                                <label class="form-label">{{ settings_log_level }}</label>
                                                <div class="custom-dropdown custom-dropdown-simple" id="log-level-dropdown">
                                                    <div class="custom-dropdown-selected" onclick="toggleDropdown('log-level-dropdown')">
                                                        <span id="log-level-text">{% if log_level_debug_selected %}DEBUG{% elif log_level_info_selected %}INFO{% elif log_level_warning_selected %}WARNING{% else %}ERROR{% endif %}</span>
                                                    </div>
                                                    <div class="custom-dropdown-arrow">
                                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                                            <polyline points="6 9 12 15 18 9"></polyline>
                                                        </svg>
                                                    </div>
                                                    <div class="custom-dropdown-menu">
                                                        <div class="custom-dropdown-option {{ 'selected' if log_level_debug_selected else '' }}" onclick="selectOption('log-level', 'DEBUG', 'DEBUG')">DEBUG</div>
                                                        <div class="custom-dropdown-option {{ 'selected' if log_level_info_selected else '' }}" onclick="selectOption('log-level', 'INFO', 'INFO')">INFO</div>
                                                        <div class="custom-dropdown-option {{ 'selected' if log_level_warning_selected else '' }}" onclick="selectOption('log-level', 'WARNING', 'WARNING')">WARNING</div>
                                                        <div class="custom-dropdown-option {{ 'selected' if log_level_error_selected else '' }}" onclick="selectOption('log-level', 'ERROR', 'ERROR')">ERROR</div>
                                                    </div>
                                                </div>
                                                <input type="hidden" id="log-level" value="{% if log_level_debug_selected %}DEBUG{% elif log_level_info_selected %}INFO{% elif log_level_warning_selected %}WARNING{% else %}ERROR{% endif %}">
                                                <small class="text-muted">{{ settings_log_level_hint }}</small>
                                            </div>
                                            <div class="col-md-6 mb-3">
                                                <label class="form-label">{{ settings_log_file }}</label>
                                                <input type="text" id="log-file" class="form-control" placeholder="/var/log/subprotox/app.log" value="{{ log_file_value }}">
                                                <small class="text-muted">{{ settings_log_file_hint }}</small>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-12">
                                                <div class="form-check mb-0">
                                                    <input class="form-check-input" type="checkbox" id="enable-access-log" {{ access_log_checked }}>
                                                    <label class="form-check-label" for="enable-access-log">
                                                        {{ settings_enable_access_log }}
                                                    </label>
                                                </div>
                                                <small class="text-muted d-block mt-1">{{ settings_access_log_hint }}</small>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Debug Mode - Default Collapsed -->
                                <div class="settings-collapse-section">
                                    <div class="settings-collapse-header" onclick="toggleSettingsSection('debug-mode')" style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%); cursor: pointer; padding: 15px 20px; display: flex; align-items: center; justify-content: space-between; transition: all 0.3s ease;">
                                        <div style="display: flex; align-items: center; gap: 10px;">
                                            <span class="material-symbols-outlined" style="color: #667eea; font-size: 20px;">bug_report</span>
                                            <h6 style="margin: 0; color: #495057; font-weight: 600;">{{ settings_debug_mode }}</h6>
                                        </div>
                                        <span class="material-symbols-outlined settings-collapse-icon" id="icon-debug-mode" style="color: #6c757d; font-size: 20px; transition: transform 0.3s ease;">expand_more</span>
                                    </div>
                                    <div class="settings-collapse-content" id="content-debug-mode" style="padding: 20px; display: none;">
                                        <div class="form-check mb-3">
                                            <input class="form-check-input" type="checkbox" id="debug-mode" {{ debug_mode_checked }}>
                                            <label class="form-check-label" for="debug-mode">
                                                {{ settings_enable_debug }}
                                            </label>
                                        </div>
                                        <div class="alert alert-warning mb-0">
                                            <strong><span class="material-symbols-outlined icon-inline" style="color: #ffc107;">warning</span> {{ settings_debug_warning_title }}:</strong><br>
                                            • {{ settings_debug_warning_1 }}<br>
                                            • {{ settings_debug_warning_2 }}<br>
                                            • {{ settings_debug_warning_3 }}
                                        </div>
                                    </div>
                                </div>

                                <!-- Save Button -->
                                <div style="padding: 20px; background: #f8f9fa; border-top: 2px solid #e9ecef;">
                                    <button class="btn btn-primary" onclick="saveSystemSettings()">
                                        <span class="material-symbols-outlined icon-btn">save</span> {{ settings_save_system }}
                                    </button>
                                </div>
                            </div>
                            </div>
                        </div>

                        <!-- Account Settings Section -->
                        <div class="config-section mb-4">
                            <div class="section-header">
                                <div style="display: flex; align-items: center; gap: 12px; flex: 1;">
                                    <span class="icon-section" style="color: #667eea;">
                                        <span class="material-symbols-outlined" style="font-size: 18px;">account_circle</span>
                                    </span>
                                    <h5 style="margin: 0;">{{ settings_account_settings }}</h5>
                                </div>
                            </div>
                            <div class="section-content">
                                <div class="settings-card">
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label class="form-label">{{ settings_current_password }}</label>
                                            <input type="password" id="current-password" class="form-control" placeholder="{{ settings_enter_current_password }}">
                                        </div>
                                        <hr>
                                        <div class="mb-3">
                                            <label class="form-label">{{ settings_new_username }}</label>
                                            <input type="text" id="new-username" class="form-control" placeholder="{{ settings_keep_current }}">
                                        </div>
                                        <div class="mb-3">
                                            <label class="form-label">{{ settings_new_password }}</label>
                                            <input type="password" id="new-password" class="form-control" placeholder="{{ settings_keep_current }}">
                                        </div>
                                        <div class="mb-3">
                                            <label class="form-label">{{ settings_confirm_password }}</label>
                                            <input type="password" id="confirm-password" class="form-control" placeholder="{{ settings_reenter_password }}">
                                        </div>
                                        <button class="btn btn-primary" onclick="changeAccount()">
                                            <span class="material-symbols-outlined icon-btn">manage_accounts</span> {{ settings_update_account }}
                                        </button>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="alert alert-info">
                                            <strong>{{ settings_current_info }}</strong><br>
                                            • Username: <span id="current-username">{{ current_username }}</span><br>
                                            • {{ settings_session_timeout }}<br>
                                            • {{ settings_last_login }}<br><br>
                                            <strong>{{ settings_security_tips }}</strong><br>
                                            • {{ settings_tip1 }}<br>
                                            • {{ settings_tip2 }}<br>
                                            • {{ settings_tip3 }}
                                        </div>
                                    </div>
                                </div>
                            </div>
                            </div>
                        </div>

                        <!-- Conversion Settings Section -->
                        <div class="config-section mb-4">
                            <div class="section-header">
                                <div style="display: flex; align-items: center; gap: 12px; flex: 1;">
                                    <span class="icon-section" style="color: #667eea;">
                                        <span class="material-symbols-outlined" style="font-size: 18px;">sync_alt</span>
                                    </span>
                                    <h5 style="margin: 0;">{{ settings_conversion_settings }}</h5>
                                </div>
                            </div>
                            <div class="section-content">
                                <div class="settings-card">
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">{{ settings_max_proxies }}</label>
                                        <input type="number" id="max-proxies" class="form-control" placeholder="1000" min="1" max="10000">
                                        <small class="text-muted">{{ settings_max_proxies_hint }}</small>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">{{ settings_conv_timeout }}</label>
                                        <input type="number" id="conv-timeout" class="form-control" placeholder="30" min="5" max="300">
                                        <small class="text-muted">{{ settings_timeout_hint }}</small>
                                    </div>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">{{ settings_user_agent }}</label>
                                    <input type="text" id="user-agent" class="form-control" placeholder="SubProtoX/1.0">
                                    <small class="text-muted">{{ settings_user_agent_hint }}</small>
                                </div>
                                <button class="btn btn-primary" onclick="saveConversionSettings()">
                                    <span class="material-symbols-outlined icon-btn">save</span> {{ settings_save_conversion }}
                                </button>
                            </div>
                            </div>
                        </div>

                        <!-- Database Maintenance Section -->
                        <div class="config-section" style="margin-bottom: 10px;">
                            <div class="section-header">
                                <div style="display: flex; align-items: center; gap: 12px; flex: 1;">
                                    <span class="icon-section" style="color: #667eea;">
                                        <span class="material-symbols-outlined" style="font-size: 18px;">database</span>
                                    </span>
                                    <h5 style="margin: 0;">{{ settings_db_maintenance }}</h5>
                                </div>
                            </div>
                            <div class="section-content">
                                <div class="settings-card">
                                <div class="row">
                                    <div class="col-md-4">
                                        <div class="maintenance-item">
                                            <h6>{{ settings_history_records }}</h6>
                                            <p class="text-muted mb-2">{{ settings_clean_old_desc }}</p>
                                            <button class="btn btn-warning btn-sm" onclick="cleanOldHistory()">
                                                <span class="material-symbols-outlined icon-btn">cleaning_services</span> {{ settings_clean_old }}
                                            </button>
                                        </div>
                                    </div>
                                    <div class="col-md-4">
                                        <div class="maintenance-item">
                                            <h6>{{ settings_db_optimize }}</h6>
                                            <p class="text-muted mb-2">{{ settings_optimize_desc }}</p>
                                            <button class="btn btn-info btn-sm" onclick="optimizeDatabase()">
                                                <span class="material-symbols-outlined icon-btn">bolt</span> {{ settings_optimize_db }}
                                            </button>
                                        </div>
                                    </div>
                                    <div class="col-md-4">
                                        <div class="maintenance-item">
                                            <h6>{{ settings_export_backup }}</h6>
                                            <p class="text-muted mb-2">{{ settings_backup_desc }}</p>
                                            <button class="btn btn-success btn-sm" onclick="exportBackup()">
                                                <span class="material-symbols-outlined icon-btn">save</span> {{ settings_export }}
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                </div>

                <!-- API documentation tab -->
                <div id="api" class="tab-pane fade {{ 'show active' if active_tab == 'api' else '' }}">
                    <div class="converter-section">
                        <!-- Page Header -->
                        <div style="text-align: center; margin-bottom: 35px;">
                            <h2 style="color: #667eea; font-weight: 700; font-size: 2rem; margin-bottom: 10px;">
                                <span class="material-symbols-outlined icon-page-title" style="color: #667eea;">menu_book</span> {{ api_page_title }}
                            </h2>
                            <p style="color: #6c757d; font-size: 1rem; margin: 0;">
                                {{ api_page_subtitle }}
                            </p>
                        </div>

                        <!-- Authentication Notice -->
                        <div class="card border-0" style="background: linear-gradient(135deg, rgba(255, 193, 7, 0.08) 0%, rgba(255, 152, 0, 0.08) 100%); border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin-bottom: 25px;">
                            <div class="card-body" style="padding: 18px;">
                                <div class="row">
                                    <!-- Authentication Guide Column -->
                                    <div class="col-md-7">
                                        <h6 class="mb-3" style="color: #f57c00; font-weight: 700; font-size: 1.1em; display: flex; align-items: center; gap: 8px;">
                                            <span class="material-symbols-outlined" style="font-size: 24px; color: #f57c00;">lock</span>
                                            <span>{{ api_auth_guide }}</span>
                                        </h6>
                                        <div style="font-size: 0.9em;">
                                            <!-- Authenticated Endpoints -->
                                            <div class="mb-2 pb-2" style="border-bottom: 1px solid rgba(255, 193, 7, 0.15);">
                                                <div class="d-flex align-items-start gap-2">
                                                    <span style="background: linear-gradient(135deg, rgba(244, 67, 54, 0.15) 0%, rgba(244, 67, 54, 0.08) 100%); color: #f44336; padding: 4px 8px; border-radius: 10px; font-size: 0.8rem; font-weight: 600; border: 1px solid rgba(244, 67, 54, 0.25); white-space: nowrap; display: flex; align-items: center; width: 95px;">
                                                        <span class="material-symbols-outlined" style="font-size: 14px; margin-right: 3px;">shield</span><span style="flex: 1; text-align: center;">{{ api_auth_protected }}</span>
                                                    </span>
                                                    <div style="flex: 1;">
                                                        <strong style="font-size: 0.95em; color: #2c3e50;">{{ api_authenticated_endpoints }}</strong>
                                                        <p class="mb-0 text-muted" style="font-size: 0.88em; line-height: 1.4; margin-top: 2px;">
                                                            {{ api_authenticated_endpoints_desc|safe }}
                                                        </p>
                                                    </div>
                                                </div>
                                            </div>

                                            <!-- Public Endpoints -->
                                            <div class="mb-0">
                                                <div class="d-flex align-items-start gap-2">
                                                    <span style="background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(76, 175, 80, 0.08) 100%); color: #4CAF50; padding: 4px 8px; border-radius: 10px; font-size: 0.8rem; font-weight: 600; border: 1px solid rgba(76, 175, 80, 0.25); white-space: nowrap; display: flex; align-items: center; width: 95px;">
                                                        <span class="material-symbols-outlined" style="font-size: 14px; margin-right: 3px;">public</span><span style="flex: 1; text-align: center;">{{ api_auth_public }}</span>
                                                    </span>
                                                    <div style="flex: 1;">
                                                        <strong style="font-size: 0.95em; color: #2c3e50;">{{ api_public_access }}</strong>
                                                        <p class="mb-0 text-muted" style="font-size: 0.88em; line-height: 1.4; margin-top: 2px;">
                                                            {{ api_public_access_desc|safe }}
                                                        </p>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Quick Tips Column -->
                                    <div class="col-md-5">
                                        <div style="padding: 12px; background: rgba(255, 255, 255, 0.5); border-radius: 8px; height: 100%;">
                                            <strong class="d-flex align-items-center gap-2 mb-2" style="color: #f57c00; font-size: 0.95em;">
                                                <span class="material-symbols-outlined" style="font-size: 18px;">tips_and_updates</span>
                                                <span>{{ api_quick_tips }}</span>
                                            </strong>
                                            <div style="line-height: 1.6; color: #5a6c7d; font-size: 0.88em;">
                                                • {{ api_quick_tips_session }}<br>
                                                • {{ api_quick_tips_cookie }}<br>
                                                • {{ api_quick_tips_default|safe }}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- API Endpoint 1: Parse Links -->
                        <div class="config-section">
                            <div class="section-header">
                                <span class="step-badge">1</span>
                                <h5>{{ api_endpoint_1_title }}</h5>
                            </div>
                            <div class="section-content">
                                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #667eea;">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                        <code style="font-size: 1.1em; color: #667eea; font-weight: 600;">POST /api/parse/links</code>
                                        <button class="btn btn-sm" style="background: rgba(102, 126, 234, 0.12); color: #667eea; border: 1px solid rgba(102, 126, 234, 0.25); border-radius: 6px; padding: 5px 12px; font-size: 0.85rem; font-weight: 500;"
                                            onclick="copyToClipboard('POST /api/parse/links', this)">
                                            <span style="margin-right: 4px;">📋</span><span class="copy-text">{{ api_copy }}</span><span class="copied-text" style="display: none;">{{ api_copied }}</span>
                                        </button>
                                    </div>
                                    <p style="margin: 10px 0; color: #6c757d; font-size: 0.95em;">
                                        <strong>{{ api_description }}</strong> {{ api_endpoint_1_desc }}
                                    </p>
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin: 10px 0;">
                                        <p style="margin: 0; color: #6c757d; font-size: 0.95em;">
                                            <strong>{{ api_request_body }}</strong>
                                        </p>
                                        <button class="btn btn-sm" style="background: rgba(102, 126, 234, 0.12); color: #667eea; border: 1px solid rgba(102, 126, 234, 0.25); border-radius: 6px; padding: 5px 12px; font-size: 0.85rem; font-weight: 500;"
                                            onclick="copyCodeBlock(document.getElementById('request-body-1'))">
                                            <span style="margin-right: 4px;">📋</span><span class="copy-text">{{ api_copy }}</span><span class="copied-text" style="display: none;">{{ api_copied }}</span>
                                        </button>
                                    </div>
                                    <pre id="request-body-1" style="background: white; padding: 15px; border-radius: 8px; margin: 10px 0; border: 1px solid #e0e0e0;">{% raw %}{
  "links": [
    "vless://uuid@server:port?type=ws&security=tls&sni=domain#NodeName",
    "vmess://base64encodedVMessLink",
    "trojan://password@server:port?sni=domain#NodeName"
  ]
}{% endraw %}</pre>
                                    <p style="margin: 10px 0; color: #6c757d; font-size: 0.95em;">
                                        <strong>{{ api_response }}</strong>
                                    </p>
                                    <pre style="background: white; padding: 15px; border-radius: 8px; margin: 0; border: 1px solid #e0e0e0;">{% raw %}{
  "nodes": [
    {
      "name": "NodeName",
      "type": "vless",
      "server": "server.com",
      "port": 443,
      ...
    }
  ]
}{% endraw %}</pre>
                                </div>
                            </div>
                        </div>

                        <!-- API Endpoint 2: Generate Config -->
                        <div class="config-section">
                            <div class="section-header">
                                <span class="step-badge">2</span>
                                <h5>{{ api_endpoint_2_title }}</h5>
                            </div>
                            <div class="section-content">
                                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #764ba2;">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                        <code style="font-size: 1.1em; color: #764ba2; font-weight: 600;">POST /api/generate/config</code>
                                        <button class="btn btn-sm" style="background: rgba(118, 75, 162, 0.12); color: #764ba2; border: 1px solid rgba(118, 75, 162, 0.25); border-radius: 6px; padding: 5px 12px; font-size: 0.85rem; font-weight: 500;"
                                            onclick="copyToClipboard('POST /api/generate/config', this)">
                                            <span style="margin-right: 4px;">📋</span><span class="copy-text">{{ api_copy }}</span><span class="copied-text" style="display: none;">{{ api_copied }}</span>
                                        </button>
                                    </div>
                                    <p style="margin: 10px 0; color: #6c757d; font-size: 0.95em;">
                                        <strong>{{ api_description }}</strong> {{ api_endpoint_2_desc }}
                                    </p>
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin: 10px 0;">
                                        <p style="margin: 0; color: #6c757d; font-size: 0.95em;">
                                            <strong>{{ api_request_body }}</strong>
                                        </p>
                                        <button class="btn btn-sm" style="background: rgba(118, 75, 162, 0.12); color: #764ba2; border: 1px solid rgba(118, 75, 162, 0.25); border-radius: 6px; padding: 5px 12px; font-size: 0.85rem; font-weight: 500;"
                                            onclick="copyCodeBlock(document.getElementById('request-body-2'))">
                                            <span style="margin-right: 4px;">📋</span><span class="copy-text">{{ api_copy }}</span><span class="copied-text" style="display: none;">{{ api_copied }}</span>
                                        </button>
                                    </div>
                                    <pre id="request-body-2" style="background: white; padding: 15px; border-radius: 8px; margin: 10px 0; border: 1px solid #e0e0e0;">{% raw %}{
  "nodes": [ /* array of node objects from parse/links */ ],
  "rule": "default_zh",  // Rule template: default_zh, default, research, minimal
  "config_name": "My Clash Config",
  "auto_update": true,
  "update_interval_hours": 24,
  "traffic_limit_gb": 100  // 0 = unlimited
}{% endraw %}</pre>
                                    <p style="margin: 10px 0; color: #6c757d; font-size: 0.95em;">
                                        <strong>{{ api_response }}</strong>
                                    </p>
                                    <pre style="background: white; padding: 15px; border-radius: 8px; margin: 0; border: 1px solid #e0e0e0;">{% raw %}{
  "success": true,
  "token": "abc123",
  "url": "http://your-server/clash/abc123",
  "proxies_count": 10,
  "auto_update": true,
  "update_interval_hours": 24,
  "traffic_limit_gb": 100
}{% endraw %}</pre>
                                </div>
                            </div>
                        </div>

                        <!-- API Endpoint 3: Convert Subscription -->
                        <div class="config-section">
                            <div class="section-header">
                                <span class="step-badge">3</span>
                                <h5>{{ api_endpoint_3_title }}</h5>
                            </div>
                            <div class="section-content">
                                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #28a745;">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                        <code style="font-size: 1.1em; color: #28a745; font-weight: 600;">GET /api/convert/sub</code>
                                        <button class="btn btn-sm" style="background: rgba(40, 167, 69, 0.12); color: #28a745; border: 1px solid rgba(40, 167, 69, 0.25); border-radius: 6px; padding: 5px 12px; font-size: 0.85rem; font-weight: 500;"
                                            onclick="copyToClipboard('GET /api/convert/sub', this)">
                                            <span style="margin-right: 4px;">📋</span><span class="copy-text">{{ api_copy }}</span><span class="copied-text" style="display: none;">{{ api_copied }}</span>
                                        </button>
                                    </div>
                                    <p style="margin: 10px 0; color: #6c757d; font-size: 0.95em;">
                                        <strong>{{ api_description }}</strong> {{ api_endpoint_3_desc }}
                                    </p>
                                    <p style="margin: 10px 0; color: #6c757d; font-size: 0.95em;">
                                        <strong>{{ api_query_parameters }}</strong>
                                    </p>
                                    <div style="background: white; padding: 15px; border-radius: 8px; margin: 10px 0; border: 1px solid #e0e0e0;">
                                        <ul style="margin: 0; padding-left: 20px; color: #6c757d;">
                                            <li><code>url</code> - <strong>(Required)</strong> Subscription URL to convert</li>
                                            <li><code>rule</code> - <strong>(Optional)</strong> Rule template (default: "default")</li>
                                            <li><code>config_name</code> - <strong>(Optional)</strong> Configuration name</li>
                                            <li><code>auto_update</code> - <strong>(Optional)</strong> Enable auto-update (default: true)</li>
                                            <li><code>update_interval_hours</code> - <strong>(Optional)</strong> Update interval in hours (default: 24)</li>
                                            <li><code>traffic_limit_gb</code> - <strong>(Optional)</strong> Traffic limit in GB (default: 0 = unlimited)</li>
                                        </ul>
                                    </div>
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin: 10px 0;">
                                        <p style="margin: 0; color: #6c757d; font-size: 0.95em;">
                                            <strong>{{ api_example }}</strong>
                                        </p>
                                        <button class="btn btn-sm" style="background: rgba(40, 167, 69, 0.12); color: #28a745; border: 1px solid rgba(40, 167, 69, 0.25); border-radius: 6px; padding: 5px 12px; font-size: 0.85rem; font-weight: 500;"
                                            onclick="copyCodeBlock(document.getElementById('example-url-3'))">
                                            <span style="margin-right: 4px;">📋</span><span class="copy-text">{{ api_copy }}</span><span class="copied-text" style="display: none;">{{ api_copied }}</span>
                                        </button>
                                    </div>
                                    <pre id="example-url-3" style="background: white; padding: 15px; border-radius: 8px; margin: 10px 0; border: 1px solid #e0e0e0;">GET /api/convert/sub?url=https://example.com/subscription&rule=default_zh&config_name=MyConfig&traffic_limit_gb=100</pre>
                                    <p style="margin: 10px 0; color: #6c757d; font-size: 0.95em;">
                                        <strong>{{ api_response }}</strong>
                                    </p>
                                    <pre style="background: white; padding: 15px; border-radius: 8px; margin: 0; border: 1px solid #e0e0e0;">{% raw %}{
  "success": true,
  "token": "xyz789",
  "url": "http://your-server/clash/xyz789",
  "proxies_count": 25,
  "auto_update": true,
  "update_interval_hours": 24,
  "traffic_limit_gb": 100
}{% endraw %}</pre>
                                </div>
                            </div>
                        </div>

                        <!-- API Endpoint 4: Get Clash Config -->
                        <div class="config-section">
                            <div class="section-header">
                                <span class="step-badge">4</span>
                                <h5>{{ api_endpoint_4_title }}</h5>
                            </div>
                            <div class="section-content">
                                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #17a2b8;">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                        <code style="font-size: 1.1em; color: #17a2b8; font-weight: 600;">GET /clash/{token}</code>
                                        <button class="btn btn-sm" style="background: rgba(23, 162, 184, 0.12); color: #17a2b8; border: 1px solid rgba(23, 162, 184, 0.25); border-radius: 6px; padding: 5px 12px; font-size: 0.85rem; font-weight: 500;"
                                            onclick="copyToClipboard('GET /clash/{token}', this)">
                                            <span style="margin-right: 4px;">📋</span><span class="copy-text">{{ api_copy }}</span><span class="copied-text" style="display: none;">{{ api_copied }}</span>
                                        </button>
                                    </div>
                                    <p style="margin: 10px 0; color: #6c757d; font-size: 0.95em;">
                                        <strong>{{ api_description }}</strong> {{ api_endpoint_4_desc }}
                                    </p>
                                    <p style="margin: 10px 0; color: #6c757d; font-size: 0.95em;">
                                        <strong>{{ api_path_parameters }}</strong>
                                    </p>
                                    <div style="background: white; padding: 15px; border-radius: 8px; margin: 10px 0; border: 1px solid #e0e0e0;">
                                        <ul style="margin: 0; padding-left: 20px; color: #6c757d;">
                                            <li><code>token</code> - Unique configuration token returned from generate/convert endpoints</li>
                                        </ul>
                                    </div>
                                    <p style="margin: 10px 0; color: #6c757d; font-size: 0.95em;">
                                        <strong>{{ api_response }}</strong> {{ api_response_yaml_headers }}
                                    </p>
                                    <div style="background: white; padding: 15px; border-radius: 8px; margin: 0; border: 1px solid #e0e0e0;">
                                        <ul style="margin: 0; padding-left: 20px; color: #6c757d;">
                                            <li><code>Content-Type: text/yaml</code></li>
                                            <li><code>profile-title</code> - Configuration display name</li>
                                            <li><code>profile-update-interval</code> - Auto-update interval (if enabled)</li>
                                            <li><code>subscription-userinfo</code> - Traffic usage info (if limit set)</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- API Endpoint 5: History Management -->
                        <div class="config-section">
                            <div class="section-header">
                                <span class="step-badge">5</span>
                                <h5>{{ api_history_management }}</h5>
                            </div>
                            <div class="section-content">
                                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #ffc107;">
                                    <div style="margin-bottom: 20px;">
                                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                            <code style="font-size: 1.1em; color: #f57c00; font-weight: 600;">GET /api/history</code>
                                            <button class="btn btn-sm" style="background: rgba(255, 193, 7, 0.12); color: #f57c00; border: 1px solid rgba(255, 193, 7, 0.25); border-radius: 6px; padding: 5px 12px; font-size: 0.85rem; font-weight: 500;"
                                                onclick="copyToClipboard('GET /api/history', this)">
                                                <span style="margin-right: 4px;">📋</span><span class="copy-text">{{ api_copy }}</span><span class="copied-text" style="display: none;">{{ api_copied }}</span>
                                            </button>
                                        </div>
                                        <p style="margin: 0; color: #6c757d; font-size: 0.95em;">{{ api_history_get_all }}</p>
                                    </div>
                                    <div style="margin-bottom: 20px;">
                                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                            <code style="font-size: 1.1em; color: #f57c00; font-weight: 600;">DELETE /api/history/{token}</code>
                                            <button class="btn btn-sm" style="background: rgba(255, 193, 7, 0.12); color: #f57c00; border: 1px solid rgba(255, 193, 7, 0.25); border-radius: 6px; padding: 5px 12px; font-size: 0.85rem; font-weight: 500;"
                                                onclick="copyToClipboard('DELETE /api/history/{token}', this)">
                                                <span style="margin-right: 4px;">📋</span><span class="copy-text">{{ api_copy }}</span><span class="copied-text" style="display: none;">{{ api_copied }}</span>
                                            </button>
                                        </div>
                                        <p style="margin: 0; color: #6c757d; font-size: 0.95em;">{{ api_history_delete_one }}</p>
                                    </div>
                                    <div>
                                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                            <code style="font-size: 1.1em; color: #f57c00; font-weight: 600;">DELETE /api/history</code>
                                            <button class="btn btn-sm" style="background: rgba(255, 193, 7, 0.12); color: #f57c00; border: 1px solid rgba(255, 193, 7, 0.25); border-radius: 6px; padding: 5px 12px; font-size: 0.85rem; font-weight: 500;"
                                                onclick="copyToClipboard('DELETE /api/history', this)">
                                                <span style="margin-right: 4px;">📋</span><span class="copy-text">{{ api_copy }}</span><span class="copied-text" style="display: none;">{{ api_copied }}</span>
                                            </button>
                                        </div>
                                        <p style="margin: 0; color: #6c757d; font-size: 0.95em;">{{ api_history_clear_all }}</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- API Endpoint 6: Rules Management -->
                        <div class="config-section">
                            <div class="section-header">
                                <span class="step-badge">6</span>
                                <h5>{{ api_rules_management }}</h5>
                            </div>
                            <div class="section-content">
                                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #dc3545;">
                                    <div style="margin-bottom: 20px;">
                                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                            <code style="font-size: 1.1em; color: #dc3545; font-weight: 600;">GET /api/rules</code>
                                            <button class="btn btn-sm" style="background: rgba(220, 53, 69, 0.12); color: #dc3545; border: 1px solid rgba(220, 53, 69, 0.25); border-radius: 6px; padding: 5px 12px; font-size: 0.85rem; font-weight: 500;"
                                                onclick="copyToClipboard('GET /api/rules', this)">
                                                <span style="margin-right: 4px;">📋</span><span class="copy-text">{{ api_copy }}</span><span class="copied-text" style="display: none;">{{ api_copied }}</span>
                                            </button>
                                        </div>
                                        <p style="margin: 0; color: #6c757d; font-size: 0.95em;">{{ api_rules_list_all }}</p>
                                    </div>
                                    <div style="margin-bottom: 20px;">
                                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                            <code style="font-size: 1.1em; color: #dc3545; font-weight: 600;">POST /api/rules</code>
                                            <button class="btn btn-sm" style="background: rgba(220, 53, 69, 0.12); color: #dc3545; border: 1px solid rgba(220, 53, 69, 0.25); border-radius: 6px; padding: 5px 12px; font-size: 0.85rem; font-weight: 500;"
                                                onclick="copyToClipboard('POST /api/rules', this)">
                                                <span style="margin-right: 4px;">📋</span><span class="copy-text">{{ api_copy }}</span><span class="copied-text" style="display: none;">{{ api_copied }}</span>
                                            </button>
                                        </div>
                                        <p style="margin: 0; color: #6c757d; font-size: 0.95em;">{{ api_rules_create }}</p>
                                    </div>
                                    <div style="margin-bottom: 20px;">
                                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                            <code style="font-size: 1.1em; color: #dc3545; font-weight: 600;">GET /api/rules/{id}</code>
                                            <button class="btn btn-sm" style="background: rgba(220, 53, 69, 0.12); color: #dc3545; border: 1px solid rgba(220, 53, 69, 0.25); border-radius: 6px; padding: 5px 12px; font-size: 0.85rem; font-weight: 500;"
                                                onclick="copyToClipboard('GET /api/rules/{id}', this)">
                                                <span style="margin-right: 4px;">📋</span><span class="copy-text">{{ api_copy }}</span><span class="copied-text" style="display: none;">{{ api_copied }}</span>
                                            </button>
                                        </div>
                                        <p style="margin: 0; color: #6c757d; font-size: 0.95em;">{{ api_rules_get_one }}</p>
                                    </div>
                                    <div style="margin-bottom: 20px;">
                                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                            <code style="font-size: 1.1em; color: #dc3545; font-weight: 600;">PUT /api/rules/{id}</code>
                                            <button class="btn btn-sm" style="background: rgba(220, 53, 69, 0.12); color: #dc3545; border: 1px solid rgba(220, 53, 69, 0.25); border-radius: 6px; padding: 5px 12px; font-size: 0.85rem; font-weight: 500;"
                                                onclick="copyToClipboard('PUT /api/rules/{id}', this)">
                                                <span style="margin-right: 4px;">📋</span><span class="copy-text">{{ api_copy }}</span><span class="copied-text" style="display: none;">{{ api_copied }}</span>
                                            </button>
                                        </div>
                                        <p style="margin: 0; color: #6c757d; font-size: 0.95em;">{{ api_rules_update }}</p>
                                    </div>
                                    <div>
                                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                            <code style="font-size: 1.1em; color: #dc3545; font-weight: 600;">DELETE /api/rules/{id}</code>
                                            <button class="btn btn-sm" style="background: rgba(220, 53, 69, 0.12); color: #dc3545; border: 1px solid rgba(220, 53, 69, 0.25); border-radius: 6px; padding: 5px 12px; font-size: 0.85rem; font-weight: 500;"
                                                onclick="copyToClipboard('DELETE /api/rules/{id}', this)">
                                                <span style="margin-right: 4px;">📋</span><span class="copy-text">{{ api_copy }}</span><span class="copied-text" style="display: none;">{{ api_copied }}</span>
                                            </button>
                                        </div>
                                        <p style="margin: 0; color: #6c757d; font-size: 0.95em;">{{ api_rules_delete }}</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Available Rule Templates -->
                        <div class="config-section" style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); border-left: 4px solid #667eea;">
                            <div class="section-content">
                                <h5 style="color: #667eea; margin-bottom: 15px;">
                                    <span class="material-symbols-outlined" style="vertical-align: middle; font-size: 24px;">rule</span>
                                    {{ api_built_in_templates }}
                                </h5>
                                <div style="background: white; padding: 15px; border-radius: 8px; border: 1px solid #e0e0e0;">
                                    <ul style="margin: 0; padding-left: 20px; color: #6c757d;">
                                        <li><code>default</code> - {{ api_template_default }}</li>
                                        <li><code>default_zh</code> - {{ api_template_default_zh }}</li>
                                        <li><code>research</code> - {{ api_template_research }}</li>
                                        <li><code>minimal</code> - {{ api_template_minimal }}</li>
                                    </ul>
                                </div>
                            </div>
                        </div>

                        <!-- Copy to Clipboard JavaScript -->
                        <script>
                        function copyToClipboard(text, button) {
                            const cleanText = text.replace(/{% raw %}|{% endraw %}/g, '').trim();
                            navigator.clipboard.writeText(cleanText).then(() => {
                                const copyText = button.querySelector('.copy-text');
                                const copiedText = button.querySelector('.copied-text');

                                if (copyText && copiedText) {
                                    // Toggle visibility
                                    copyText.style.display = 'none';
                                    copiedText.style.display = 'inline';

                                    const originalBg = button.style.background;
                                    const originalColor = button.style.color;
                                    const originalBorder = button.style.borderColor;

                                    button.style.background = 'rgba(40, 167, 69, 0.2)';
                                    button.style.color = '#28a745';
                                    button.style.borderColor = 'rgba(40, 167, 69, 0.4)';

                                    setTimeout(() => {
                                        copyText.style.display = 'inline';
                                        copiedText.style.display = 'none';
                                        button.style.background = originalBg;
                                        button.style.color = originalColor;
                                        button.style.borderColor = originalBorder;
                                    }, 2000);
                                }
                            });
                        }

                        function copyCodeBlock(elementOrButton) {
                            // Check if the parameter is a button element (called from onclick with 'this')
                            // or a pre element (called with document.getElementById)
                            let preElement, button;

                            if (elementOrButton.tagName === 'BUTTON') {
                                // Old behavior: button is inside pre, passed as 'this'
                                button = elementOrButton;
                                preElement = button.parentElement;
                            } else {
                                // New behavior: pre element passed directly, find the button sibling
                                preElement = elementOrButton;
                                // Find the button in the previous sibling div
                                const parentDiv = preElement.previousElementSibling;
                                button = parentDiv ? parentDiv.querySelector('button') : null;
                            }

                            if (!preElement || !button) return;

                            // Get the text content directly from pre element
                            let text = preElement.textContent.trim();
                            // Copy to clipboard
                            copyToClipboard(text, button);
                        }
                        </script>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Create Rule Modal -->
    <div class="modal fade" id="createRuleModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                    <h5 class="modal-title">✨ {{ rules_create_new }}</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="new-rule-name" class="form-label">{{ rules_rule_name }}</label>
                        <input type="text" class="form-control" id="new-rule-name" placeholder="e.g., my_custom_rule">
                    </div>
                    <div class="mb-3">
                        <label for="new-rule-desc" class="form-label">{{ rules_rule_desc }}</label>
                        <input type="text" class="form-control" id="new-rule-desc" placeholder="Enter rule description">
                    </div>
                    <div class="mb-4">
                        <label class="form-label d-block mb-2"><span class="material-symbols-outlined icon-inline" style="color: #667eea;">rocket_launch</span> Quick Start: Import from Built-in Template</label>
                        <div class="d-grid gap-2" style="grid-template-columns: repeat(2, 1fr); display: grid;">
                            <button type="button" class="btn btn-outline-primary btn-sm" onclick="importTemplate('Default Routing')" style="text-align: left; padding: 8px 12px;">
                                <strong><span class="material-symbols-outlined icon-inline">article</span> Default Routing</strong><br>
                                <small class="text-muted">General purpose routing</small>
                            </button>
                            <button type="button" class="btn btn-outline-primary btn-sm" onclick="importTemplate('Default Routing (Chinese Interface)')" style="text-align: left; padding: 8px 12px;">
                                <strong><span class="material-symbols-outlined icon-inline">article</span> Default Routing (Chinese Interface)</strong><br>
                                <small class="text-muted">Chinese optimized</small>
                            </button>
                            <button type="button" class="btn btn-outline-primary btn-sm" onclick="importTemplate('Academic & Research Routing')" style="text-align: left; padding: 8px 12px;">
                                <strong><span class="material-symbols-outlined icon-inline">article</span> Academic & Research Routing</strong><br>
                                <small class="text-muted">Academic networks</small>
                            </button>
                            <button type="button" class="btn btn-outline-primary btn-sm" onclick="importTemplate('Minimal Rules')" style="text-align: left; padding: 8px 12px;">
                                <strong><span class="material-symbols-outlined icon-inline">article</span> Minimal Rules</strong><br>
                                <small class="text-muted">Basic configuration</small>
                            </button>
                        </div>
                        <small class="text-muted d-block mt-2"><span class="material-symbols-outlined icon-inline">upload</span> Click a template to import its content as your starting point</small>
                    </div>
                    <div class="mb-3">
                        <label for="new-rule-content" class="form-label">{{ rules_rule_content }}</label>
                        <textarea class="form-control" id="new-rule-content" rows="8" style="font-family: monospace;" placeholder="# Example rules:
DOMAIN-SUFFIX,local,DIRECT
IP-CIDR,127.0.0.0/8,DIRECT
GEOIP,CN,DIRECT
MATCH,🚀 Proxy"></textarea>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">{{ rules_cancel }}</button>
                    <button type="button" class="btn btn-success" onclick="createRuleFromModal()">
                        <span class="material-symbols-outlined icon-btn">save</span> {{ rules_save }}
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script src="/static/js/bootstrap.bundle.min.js?v=20251019b"></script>
    <script src="/static/js/axios.min.js?v=20251019b"></script>
    <script>
        // Get base path from current URL
        // Remove trailing slash, but keep the base path
        const currentPath = window.location.pathname;
        const BASE_PATH = currentPath === '/' ? '' : (currentPath.endsWith('/') ? currentPath.slice(0, -1) : currentPath);

        let currentResult = null;
    {% raw %}
        let parsedNodes = []; // Store parsed nodes

        // Translation variables for JavaScript
    {% endraw %}
        const i18n = {
            lang: '{{ lang }}',
            unknown_error: '{{ unknown_error }}',
            alerts_enter_links: '{{ alerts_enter_links }}',
            alerts_parse_failed: '{{ alerts_parse_failed }}',
            alerts_no_nodes: '{{ alerts_no_nodes }}',
            alerts_config_failed: '{{ alerts_config_failed }}',
            alerts_enter_sub: '{{ alerts_enter_sub }}',
            alerts_convert_failed: '{{ alerts_convert_failed }}',
            alerts_history_clear_failed: '{{ alerts_history_clear_failed }}',
            alerts_rule_get_failed: '{{ alerts_rule_get_failed }}',
            alerts_rule_create_failed: '{{ alerts_rule_create_failed }}',
            alerts_restart_failed: '{{ alerts_restart_failed }}',
            rules_create_success: '{{ rules_create_success }}',
            rules_name_empty: '{{ rules_name_empty }}',
            rules_content_empty: '{{ rules_content_empty }}',
            history_cleared: '{{ history_cleared }}',
            settings_new_url_label: '{{ settings_new_url_label }}',
            settings_manual_restart: '{{ settings_manual_restart }}',
            settings_failed_prefix: '{{ settings_failed_prefix }}',
            ssl_validation_empty: '{{ ssl_validation_empty }}',
            ssl_validation_domain: '{{ ssl_validation_domain }}',
            rule_restored_success: '{{ rule_restored_success }}',
            rule_name_empty: '{{ rule_name_empty }}',
            rule_content_empty: '{{ rule_content_empty }}',
            rule_updated_success: '{{ rule_updated_success }}',
            rule_delete_confirm: '{{ rule_delete_confirm }}',
            delete_success: '{{ delete_success }}',
            account_password_required: '{{ account_password_required }}',
            account_password_mismatch: '{{ account_password_mismatch }}',
            account_change_required: '{{ account_change_required }}',
            account_update_failed_prefix: '{{ account_update_failed_prefix }}',
            history_token: '{{ history_token }}',
            history_subscription_link: '{{ history_subscription_link }}',
            history_created: '{{ history_created }}',
            history_nodes: '{{ history_nodes }}',
            history_view: '{{ history_view }}',
            history_copy: '{{ history_copy }}',
            history_download: '{{ history_download }}',
            history_delete: '{{ history_delete }}',
            rules_rule_name_col: '{{ rules_rule_name_col }}',
            rules_rule_description_col: '{{ rules_rule_description_col }}',
            rules_rule_content_col: '{{ rules_rule_content_col }}',
            rules_restore: '{{ rules_restore }}',
            rules_delete: '{{ rules_delete }}',
            rules_save: '{{ rules_save }}',
            rules_cancel: '{{ rules_cancel }}',
            rules_no_custom_rules: '{{ rules_no_custom_rules }}',
            api_copy: '{{ api_copy }}',
            api_copied: '{{ api_copied }}',
            modal_restart_title: '{{ alerts_modal_restart_title }}',
            modal_restart_message: '{{ alerts_modal_restart_message }}',
            modal_restart_confirm: '{{ alerts_modal_restart_confirm }}',
            modal_clear_title: '{{ alerts_modal_clear_title }}',
            modal_clear_message: '{{ alerts_modal_clear_message }}',
            modal_clear_confirm: '{{ alerts_modal_clear_confirm }}',
            modal_delete_history_title: '{{ alerts_modal_delete_history_title }}',
            modal_delete_history_message: '{{ alerts_modal_delete_history_message }}',
            modal_delete_confirm: '{{ alerts_modal_delete_confirm }}',
            modal_restore_title: '{{ alerts_modal_restore_title }}',
            modal_restore_message: '{{ alerts_modal_restore_message }}',
            modal_restore_confirm: '{{ alerts_modal_restore_confirm }}',
            modal_save_title: '{{ alerts_modal_save_title }}',
            modal_save_message: '{{ alerts_modal_save_message }}',
            modal_save_confirm: '{{ alerts_modal_save_confirm }}',
            modal_template_imported: '{{ alerts_modal_template_imported }}',
            modal_template_imported_message: '{{ alerts_modal_template_imported_message }}',
            modal_ok: '{{ alerts_modal_ok }}',
            modal_cancel: '{{ alerts_modal_cancel }}',
            modal_save_settings_title: '{{ alerts_modal_save_settings_title }}',
            modal_save_settings_message: '{{ alerts_modal_save_settings_message }}',
            modal_settings_saved_title: '{{ alerts_modal_settings_saved_title }}',
            modal_settings_saved_message: '{{ alerts_modal_settings_saved_message }}',
            modal_restart_now_title: '{{ alerts_modal_restart_now_title }}',
            modal_restart_now_message: '{{ alerts_modal_restart_now_message }}',
            modal_update_account_title: '{{ alerts_modal_update_account_title }}',
            modal_update_account_message: '{{ alerts_modal_update_account_message }}',
            modal_account_updated_title: '{{ alerts_modal_account_updated_title }}',
            modal_account_updated_message: '{{ alerts_modal_account_updated_message }}',
            modal_save_conversion_title: '{{ alerts_modal_save_conversion_title }}',
            modal_save_conversion_message: '{{ alerts_modal_save_conversion_message }}',
            modal_conversion_saved_title: '{{ alerts_modal_conversion_saved_title }}',
            modal_conversion_saved_message: '{{ alerts_modal_conversion_saved_message }}',
            modal_clean_records_title: '{{ alerts_modal_clean_records_title }}',
            modal_clean_records_message: '{{ alerts_modal_clean_records_message }}',
            modal_records_cleaned_title: '{{ alerts_modal_records_cleaned_title }}',
            modal_records_cleaned_message: '{{ alerts_modal_records_cleaned_message }}',
            modal_optimize_db_title: '{{ alerts_modal_optimize_db_title }}',
            modal_optimize_db_message: '{{ alerts_modal_optimize_db_message }}',
            modal_db_optimized_title: '{{ alerts_modal_db_optimized_title }}',
            modal_db_optimized_message: '{{ alerts_modal_db_optimized_message }}',
            modal_export_backup_title: '{{ alerts_modal_export_backup_title }}',
            modal_export_backup_message: '{{ alerts_modal_export_backup_message }}',
            modal_backup_exported_title: '{{ alerts_modal_backup_exported_title }}',
            modal_backup_exported_message: '{{ alerts_modal_backup_exported_message }}'
        };
    {% raw %}

        // Beautiful Confirm Modal Function
        function showConfirmModal(options) {
            return new Promise((resolve) => {
                // Create modal overlay
                const overlay = document.createElement('div');
                overlay.style.cssText = `
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: rgba(0, 0, 0, 0.5);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 10000;
                    animation: fadeIn 0.2s ease;
                `;

                // Create modal container
                const modal = document.createElement('div');
                modal.style.cssText = `
                    background: white;
                    border-radius: 16px;
                    padding: 0;
                    min-width: 400px;
                    max-width: 500px;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                    animation: slideDown 0.3s ease;
                    overflow: hidden;
                `;

                // Modal header
                const title = options.title || 'Confirm';
                const message = options.message || 'Are you sure?';
                const confirmText = options.confirmText || 'Confirm';
                const cancelText = options.cancelText || 'Cancel';
                const confirmColor = options.confirmColor || '#dc3545';

                modal.innerHTML = `
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px 24px; text-align: center;">
                        <h4 style="color: white; margin: 0; font-weight: 600; font-size: 18px;">${title}</h4>
                    </div>
                    <div style="padding: 24px;">
                        <p style="color: #6c757d; font-size: 15px; line-height: 1.6; margin: 0 0 24px 0; text-align: center;">
                            ${message}
                        </p>
                        <div style="display: flex; gap: 12px; justify-content: center;">
                            <button id="modal-cancel" style="
                                flex: 1;
                                padding: 12px 24px;
                                border: 2px solid #e0e0e0;
                                background: white;
                                color: #6c757d;
                                border-radius: 8px;
                                font-size: 15px;
                                font-weight: 500;
                                cursor: pointer;
                                transition: all 0.2s;
                            ">${cancelText}</button>
                            <button id="modal-confirm" style="
                                flex: 1;
                                padding: 12px 24px;
                                border: none;
                                background: ${confirmColor};
                                color: white;
                                border-radius: 8px;
                                font-size: 15px;
                                font-weight: 500;
                                cursor: pointer;
                                transition: all 0.2s;
                                box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3);
                            ">${confirmText}</button>
                        </div>
                    </div>
                `;

                overlay.appendChild(modal);
                document.body.appendChild(overlay);

                // Button hover effects
                const cancelBtn = modal.querySelector('#modal-cancel');
                const confirmBtn = modal.querySelector('#modal-confirm');

                cancelBtn.onmouseover = () => {
                    cancelBtn.style.background = '#f8f9fa';
                    cancelBtn.style.borderColor = '#6c757d';
                };
                cancelBtn.onmouseout = () => {
                    cancelBtn.style.background = 'white';
                    cancelBtn.style.borderColor = '#e0e0e0';
                };

                confirmBtn.onmouseover = () => {
                    confirmBtn.style.transform = 'translateY(-2px)';
                    confirmBtn.style.boxShadow = '0 6px 16px rgba(220, 53, 69, 0.4)';
                };
                confirmBtn.onmouseout = () => {
                    confirmBtn.style.transform = 'translateY(0)';
                    confirmBtn.style.boxShadow = '0 4px 12px rgba(220, 53, 69, 0.3)';
                };

                // Button click handlers
                cancelBtn.onclick = () => {
                    overlay.style.animation = 'fadeOut 0.2s ease';
                    setTimeout(() => {
                        document.body.removeChild(overlay);
                        resolve(false);
                    }, 200);
                };

                confirmBtn.onclick = () => {
                    overlay.style.animation = 'fadeOut 0.2s ease';
                    setTimeout(() => {
                        document.body.removeChild(overlay);
                        resolve(true);
                    }, 200);
                };

                // Click overlay to cancel
                overlay.onclick = (e) => {
                    if (e.target === overlay) {
                        cancelBtn.click();
                    }
                };

                // ESC key to cancel
                const escHandler = (e) => {
                    if (e.key === 'Escape') {
                        cancelBtn.click();
                        document.removeEventListener('keydown', escHandler);
                    }
                };
                document.addEventListener('keydown', escHandler);
            });
        }

        function showAlertModal(options) {
            const { title, message, confirmText = i18n.modal_ok } = options;

            return new Promise((resolve) => {
                // Create modal overlay with fade animation
                const overlay = document.createElement('div');
                overlay.style.cssText = `
                    position: fixed;
                    top: 0; left: 0; right: 0; bottom: 0;
                    background: rgba(0, 0, 0, 0.5);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 10000;
                    animation: fadeIn 0.2s ease;
                `;

                const modal = document.createElement('div');
                modal.style.cssText = `
                    background: white;
                    border-radius: 16px;
                    min-width: 400px;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                    animation: slideDown 0.3s ease;
                `;

                // Simplified header without icon
                modal.innerHTML = `
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px 24px; border-radius: 16px 16px 0 0;">
                        <h4 style="color: white; margin: 0; font-weight: 600; text-align: center;">${title}</h4>
                    </div>
                    <div style="padding: 24px;">
                        <p style="color: #6c757d; margin-bottom: 24px; text-align: center; font-size: 15px;">${message}</p>
                        <div style="display: flex; justify-content: center;">
                            <button id="modal-confirm" style="
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                color: white;
                                border: none;
                                padding: 10px 32px;
                                border-radius: 8px;
                                font-weight: 500;
                                cursor: pointer;
                                transition: all 0.2s;
                                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
                            ">${confirmText}</button>
                        </div>
                    </div>
                `;

                overlay.appendChild(modal);
                document.body.appendChild(overlay);

                const confirmBtn = document.getElementById('modal-confirm');

                // Button hover effects
                confirmBtn.onmouseover = () => {
                    confirmBtn.style.transform = 'translateY(-2px)';
                    confirmBtn.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.4)';
                };
                confirmBtn.onmouseout = () => {
                    confirmBtn.style.transform = 'translateY(0)';
                    confirmBtn.style.boxShadow = '0 4px 12px rgba(102, 126, 234, 0.3)';
                };

                // Button click handler
                confirmBtn.onclick = () => {
                    overlay.style.animation = 'fadeOut 0.2s ease';
                    setTimeout(() => {
                        document.body.removeChild(overlay);
                        resolve(true);
                    }, 200);
                };

                // Click overlay to close
                overlay.onclick = (e) => {
                    if (e.target === overlay) {
                        confirmBtn.click();
                    }
                };

                // ESC key to close
                const escHandler = (e) => {
                    if (e.key === 'Escape') {
                        confirmBtn.click();
                        document.removeEventListener('keydown', escHandler);
                    }
                };
                document.addEventListener('keydown', escHandler);
            });
        }

        // Add CSS animations
        const style = document.createElement('style');
        style.textContent = `
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes fadeOut {
                from { opacity: 1; }
                to { opacity: 0; }
            }
            @keyframes slideDown {
                from {
                    transform: translateY(-50px);
                    opacity: 0;
                }
                to {
                    transform: translateY(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(style);

        function changeLanguage(lang) {
            localStorage.setItem('language', lang);
            // Get current tab
            const activeTab = document.querySelector('.nav-link.active');
            const tabName = activeTab ? activeTab.getAttribute('href').replace('#', '') : 'converter';
            console.log('Switching language to:', lang);
            console.log('Current active tab:', tabName);
            window.location.href = BASE_PATH + '/?lang=' + lang + '&tab=' + tabName;
        }

        // Select conversion type by clicking card
        function selectConversionType(type) {
            const linksRadio = document.getElementById('type-links');
            const subscriptionRadio = document.getElementById('type-subscription');
            const linksCard = document.getElementById('card-links');
            const subscriptionCard = document.getElementById('card-subscription');

            if (type === 'links') {
                linksRadio.checked = true;
                // Update card styles
                linksCard.style.border = '2px solid #667eea';
                linksCard.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)';
                linksCard.querySelector('h5').style.color = '#667eea';

                subscriptionCard.style.border = '2px solid #ddd';
                subscriptionCard.style.background = '#f8f9fa';
                subscriptionCard.querySelector('h5').style.color = '#666';
            } else {
                subscriptionRadio.checked = true;
                // Update card styles
                subscriptionCard.style.border = '2px solid #667eea';
                subscriptionCard.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)';
                subscriptionCard.querySelector('h5').style.color = '#667eea';

                linksCard.style.border = '2px solid #ddd';
                linksCard.style.background = '#f8f9fa';
                linksCard.querySelector('h5').style.color = '#666';
            }

            switchConversionType();
        }

        // Switch between conversion types
    {% endraw %}
        function switchConversionType() {
            const typeLinks = document.getElementById('type-links').checked;
            const linksArea = document.getElementById('links-input-area');
            const subscriptionArea = document.getElementById('subscription-input-area');
            const nodesPreview = document.getElementById('nodes-preview');
            const linksCard = document.getElementById('card-links');
            const subscriptionCard = document.getElementById('card-subscription');
            const inputSectionTitle = document.getElementById('input-section-title');
            const basicConfigSection = document.getElementById('step-basic-config');
            const basicConfigContent = document.getElementById('basic-config-content');

            if (typeLinks) {
                linksArea.style.display = 'block';
                subscriptionArea.style.display = 'none';
                if (inputSectionTitle) inputSectionTitle.textContent = '{{ converter_paste_proxy_links }}';

                // Update card styles
                linksCard.style.border = '2px solid #667eea';
                linksCard.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)';
                linksCard.querySelector('h5').style.color = '#667eea';

                subscriptionCard.style.border = '2px solid #ddd';
                subscriptionCard.style.background = '#f8f9fa';
                subscriptionCard.querySelector('h5').style.color = '#666';

                // Enable Step 3 (Basic Configuration) for Proxy Links mode
                if (basicConfigSection) {
                    basicConfigSection.style.opacity = '1';
                    basicConfigSection.style.pointerEvents = 'auto';
                    basicConfigSection.style.filter = 'none';
                    if (basicConfigContent) {
                        basicConfigContent.querySelectorAll('input, .custom-dropdown-selected').forEach(el => {
                            el.style.cursor = 'auto';
                            if (el.tagName === 'INPUT') {
                                el.disabled = false;
                                el.style.cursor = 'text';
                            }
                            if (el.classList.contains('custom-dropdown-selected')) {
                                el.style.cursor = 'pointer';
                            }
                        });
                    }
                }
            } else {
                linksArea.style.display = 'none';
                subscriptionArea.style.display = 'block';
                if (inputSectionTitle) inputSectionTitle.textContent = '{{ converter_paste_subscription_url }}';
                // Hide nodes preview when switching to subscription mode
                nodesPreview.style.display = 'none';

                // Update card styles
                subscriptionCard.style.border = '2px solid #667eea';
                subscriptionCard.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)';
                subscriptionCard.querySelector('h5').style.color = '#667eea';

                linksCard.style.border = '2px solid #ddd';
                linksCard.style.background = '#f8f9fa';
                linksCard.querySelector('h5').style.color = '#666';

                // Disable Step 3 (Basic Configuration) for Subscription URL mode
                if (basicConfigSection) {
                    basicConfigSection.style.opacity = '0.5';
                    basicConfigSection.style.pointerEvents = 'none';
                    basicConfigSection.style.filter = 'grayscale(30%)';
                    if (basicConfigContent) {
                        basicConfigContent.querySelectorAll('input, .custom-dropdown-selected').forEach(el => {
                            el.style.cursor = 'not-allowed';
                            if (el.tagName === 'INPUT') {
                                el.disabled = true;
                            }
                        });
                    }
                }
            }
        }
    {% raw %}

        // Unified conversion function
        function convertToClash() {
            const typeLinks = document.getElementById('type-links').checked;

            if (typeLinks) {
                // Proxy Links mode - use two-step conversion
                convertLinks();
            } else {
                // Subscription URL mode - use direct conversion
                convertSubscription();
            }
        }

        function convertLinks() {
            const links = document.getElementById('links-input').value.split('\\n').filter(l => l.trim());
            const rule = document.getElementById('rule-template').value;
            const configName = document.getElementById('config-name').value || 'My Subscription Config';

            if (links.length === 0) {
                showAlertModal({title: i18n.unknown_error, message: i18n.alerts_enter_links});
                return;
            }

            // Parse nodes first
            axios.post(BASE_PATH + '/api/parse/links', {
                links: links
            })
            .then(response => {
                parsedNodes = response.data.nodes;
                showNodesPreview(parsedNodes, rule, configName);
            })
            .catch(error => {
                showAlertModal({title: i18n.unknown_error, message: i18n.alerts_parse_failed + (error.response?.data?.error || i18n.unknown_error)});
            });
        }

        function showNodesPreview(nodes, rule, configName) { 
            const previewDiv = document.getElementById('nodes-preview');
            const nodesList = document.getElementById('nodes-list');

            nodesList.innerHTML = '';

            if (nodes.length === 0) { 
                nodesList.innerHTML = '<p class="text-danger">No valid nodes parsed</p>';
                return;
            }

            nodes.forEach((node, index) => { 
                const nodeItem = document.createElement('div');
                nodeItem.className = 'node-item';
                nodeItem.innerHTML = `
                    <div class="node-info">
                        <strong>Type:</strong> ${node.type.toUpperCase()}<br>
                        <strong>Server:</strong> ${node.server}:${node.port}
                    </div>
                    <div>
                        <label class="form-label">Node Name:</label>
                        <input type="text" class="form-control node-name-edit"
                               value="${node.name}"
                               onchange="updateNodeName(${index}, this.value)">
                    </div>
                `;
                nodesList.appendChild(nodeItem);
            });

            previewDiv.style.display = 'block';
            previewDiv.scrollIntoView({ behavior: 'smooth' });
        }

        function updateNodeName(index, newName) { 
            if (parsedNodes[index]) { 
                parsedNodes[index].name = newName;
            }
        }

        function generateConfig() {
            const rule = document.getElementById('rule-template').value;
            const configName = document.getElementById('config-name').value || 'My Subscription Config';
            const autoUpdate = document.getElementById('auto-update-enabled').checked;
            const updateInterval = parseInt(document.getElementById('update-interval').value) || 24;
            const trafficLimit = parseInt(document.getElementById('traffic-limit').value) || 0;

            axios.post(BASE_PATH + '/api/generate/config', {
                nodes: parsedNodes,
                rule: rule,
                config_name: configName,
                auto_update: autoUpdate,
                update_interval_hours: updateInterval,
                traffic_limit_gb: trafficLimit
            })
            .then(response => {
                showResult(response.data);
                loadHistory();
                // Hide preview area
                document.getElementById('nodes-preview').style.display = 'none';
            })
            .catch(error => {
                showAlertModal({title: i18n.unknown_error, message: i18n.alerts_config_failed + (error.response?.data?.error || i18n.unknown_error)});
            });
        }

        function convertSubscription() {
            const url = document.getElementById('sub-url').value;
            const rule = document.getElementById('rule-template').value;
            const configName = document.getElementById('config-name').value || 'Subscription Config';
            const autoUpdate = document.getElementById('auto-update-enabled').checked;
            const updateInterval = parseInt(document.getElementById('update-interval').value) || 24;
            const trafficLimit = parseInt(document.getElementById('traffic-limit').value) || 0;

            if (!url) {
                showAlertModal({title: i18n.unknown_error, message: i18n.alerts_enter_sub});
                return;
            }

            axios.get(BASE_PATH + '/api/convert/sub', {
                params: {
                    url: url,
                    rule: rule,
                    config_name: configName,
                    auto_update: autoUpdate,
                    update_interval_hours: updateInterval,
                    traffic_limit_gb: trafficLimit
                }
            })
            .then(response => {
                showResult(response.data);
                loadHistory();
            })
            .catch(error => {
                showAlertModal({title: i18n.unknown_error, message: i18n.alerts_convert_failed + (error.response?.data?.error || i18n.unknown_error)});
            });
        }

        function showResult(data) {
            currentResult = data;
            const output = document.getElementById('output');
            const content = document.getElementById('result-content');

            if (data.url) {
    {% endraw %}
                content.innerHTML = `<p>{{ converter_subscription_link }}: <a href="${data.url}" target="_blank">${data.url}</a></p>`;
    {% raw %}
            } else {
                content.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            }

            output.style.display = 'block';
        }

        function copyResult() { 
            if (currentResult && currentResult.url) { 
                navigator.clipboard.writeText(currentResult.url).then(() => { 
                    alert('Link copied');
                });
            }
        }

        function downloadResult() { 
            if (currentResult && currentResult.token) { 
                window.open(BASE_PATH + '/clash/' + currentResult.token, '_blank');
            }
        }

        function loadHistory() {
            axios.get(BASE_PATH + '/api/history')
                .then(response => {
                    const container = document.getElementById('history-list');
                    container.innerHTML = '';

                    // Handle different response formats
                    let data = response.data;
                    if (!Array.isArray(data)) {
                        // If response is an object with a data property
                        data = data.history || data.data || [];
                    }

                    if (data.length === 0) {
                        container.innerHTML = '<p class="text-muted">No history records</p>';
                        return;
                    }

                    data.forEach(item => {
                        const div = document.createElement('div');
                        div.className = 'history-item';

                        // Get request protocol
                        const protocol = window.location.protocol;
                        const host = window.location.host;
                        const subscriptionUrl = `${protocol}//${host}${BASE_PATH}/clash/${item.token}`;

                        div.innerHTML = `
                            <div class="history-info">
                                <strong>${i18n.history_token}:</strong> ${item.token}<br>
                                <strong>${i18n.history_subscription_link}:</strong> <a href="${subscriptionUrl}" target="_blank">${subscriptionUrl}</a><br>
                                <small class="text-muted">${i18n.history_created}: ${item.created_at}</small><br>
                                <small>${i18n.history_nodes}: ${item.proxies_count || 0}</small>
                            </div>
                            <div class="history-actions">
                                <button class="btn btn-sm btn-info" onclick="viewHistory('${item.token}')">${i18n.history_view}</button>
                                <button class="btn btn-sm btn-success" onclick="copyHistoryLink('${subscriptionUrl}', this)">
                                    <span class="copy-text">${i18n.history_copy}</span>
                                    <span class="copied-text" style="display: none;">${i18n.api_copied}</span>
                                </button>
                                <button class="btn btn-sm btn-primary" onclick="downloadHistory('${item.token}')">${i18n.history_download}</button>
                                <button class="btn btn-sm btn-danger" onclick="deleteHistory('${item.token}')">${i18n.history_delete}</button>
                            </div>
                        `;
                        container.appendChild(div);
                    });
                })
                .catch(error => console.error('Error:', error));
        }

        function copyHistoryLink(url, button) {
            navigator.clipboard.writeText(url).then(() => {
                const copyText = button.querySelector('.copy-text');
                const copiedText = button.querySelector('.copied-text');

                if (copyText && copiedText) {
                    // Toggle visibility
                    copyText.style.display = 'none';
                    copiedText.style.display = 'inline';

                    // Save original button styles
                    const originalBg = button.style.background || '';
                    const originalColor = button.style.color || '';
                    const originalBorder = button.style.borderColor || '';

                    // Apply copied state styles (same as API copy buttons)
                    button.style.background = 'rgba(40, 167, 69, 0.2)';
                    button.style.color = '#28a745';
                    button.style.borderColor = 'rgba(40, 167, 69, 0.4)';

                    // Restore after 2 seconds
                    setTimeout(() => {
                        copyText.style.display = 'inline';
                        copiedText.style.display = 'none';
                        button.style.background = originalBg;
                        button.style.color = originalColor;
                        button.style.borderColor = originalBorder;
                    }, 2000);
                }
            }).catch(err => {
                console.error('Failed to copy: ', err);
            });
        }

        function viewHistory(token) { 
            window.open(BASE_PATH + '/clash/' + token, '_blank');
        }

        function downloadHistory(token) {
            // Create a temporary anchor element to force download
            const link = document.createElement('a');
            link.href = BASE_PATH + '/clash/' + token;
            link.download = `config_${token}.yaml`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        async function deleteHistory(token) {
            const confirmed = await showConfirmModal({
                title: i18n.modal_delete_history_title,
                message: i18n.modal_delete_history_message,
                confirmText: i18n.modal_delete_confirm,
                cancelText: i18n.modal_cancel,
                confirmColor: '#dc3545'
            });

            if (!confirmed) return;

            axios.delete(BASE_PATH + '/api/history/' + token)
                .then(response => {
                    loadHistory();
                })
                .catch(error => {
                    showAlertModal({
                        title: i18n.unknown_error,
                        message: 'Delete failed: ' + (error.response?.data?.error || error.message)
                    });
                });
        }

        async function clearAllHistory() {
            const confirmed = await showConfirmModal({
                title: i18n.modal_clear_title,
                message: i18n.modal_clear_message,
                confirmText: i18n.modal_clear_confirm,
                cancelText: i18n.modal_cancel,
                confirmColor: '#dc3545'
            });

            if (!confirmed) return;

            axios.delete(BASE_PATH + '/api/history')
                .then(response => { 
                    showAlertModal({title: i18n.modal_ok, message: i18n.history_cleared});
                    loadHistory();
                })
                .catch(error => { 
                    showAlertModal({title: i18n.unknown_error, message: i18n.alerts_history_clear_failed});
                });
        }

        function loadRules() {
            axios.get(BASE_PATH + '/api/rules')
                .then(response => {
                    const builtinContainer = document.getElementById('builtin-rules-list');
                    const customContainer = document.getElementById('custom-rules-list');
                    builtinContainer.innerHTML = '';
                    customContainer.innerHTML = '';

                    const data = response.data;
                    const builtinRules = data.builtin || [];
                    const customRules = data.custom || [];

                    // Render built-in rules (editable with restore option)
                    if (builtinRules.length === 0) {
                        builtinContainer.innerHTML = '<p class="text-muted">No built-in templates found</p>';
                    } else {
                        builtinRules.forEach(rule => {
                            const item = document.createElement('div');
                            item.className = 'rule-item builtin-rule';
                            item.setAttribute('data-rule-id', rule.id);
                            item.innerHTML = `
                                <div class="rule-header" data-header="true">
                                    <div class="rule-info">
                                        <h5>${rule.name}</h5>
                                        <p>${rule.description || 'No description'}</p>
                                    </div>
                                    <div class="rule-actions" onclick="event.stopPropagation()">
                                        <button class="btn btn-sm" style="background: rgba(102, 126, 234, 0.12); color: #667eea; border: 1px solid rgba(102, 126, 234, 0.25); border-radius: 6px; padding: 5px 12px; font-size: 0.85rem; font-weight: 500; transition: all 0.2s ease;"
                                            onmouseover="this.style.background='rgba(102, 126, 234, 0.2)'; this.style.borderColor='rgba(102, 126, 234, 0.4)'; this.style.color='#5568d3'"
                                            onmouseout="this.style.background='rgba(102, 126, 234, 0.12)'; this.style.borderColor='rgba(102, 126, 234, 0.25)'; this.style.color='#667eea'"
                                            onclick="restoreRule('${rule.id}', '${rule.name}'); event.stopPropagation();">
                                            <span style="margin-right: 4px;">↻</span>${i18n.rules_restore}
                                        </button>
                                    </div>
                                </div>
                            `;
                            // Only attach click handler to the header
                            const header = item.querySelector('[data-header="true"]');
                            header.onclick = (e) => {
                                if (!e.target.closest('.rule-actions')) {
                                    editRule(rule.id);
                                }
                            };
                            builtinContainer.appendChild(item);
                        });
                    }

                    // Render custom rules (editable)
                    if (customRules.length === 0) {
                        customContainer.innerHTML = '<p class="text-muted">' + i18n.rules_no_custom_rules + '</p>';
                    } else {
                        customRules.forEach(rule => {
                            const item = document.createElement('div');
                            item.className = 'rule-item custom-rule';
                            item.setAttribute('data-rule-id', rule.id);
                            item.innerHTML = `
                                <div class="rule-header" data-header="true">
                                    <div class="rule-info">
                                        <h5>${rule.name}</h5>
                                        <p>${rule.description || 'No description'}</p>
                                    </div>
                                    <div class="rule-actions" onclick="event.stopPropagation()">
                                        <button class="btn btn-sm" style="background: rgba(40, 167, 69, 0.12); color: #28a745; border: 1px solid rgba(40, 167, 69, 0.25); border-radius: 6px; padding: 5px 12px; font-size: 0.85rem; font-weight: 500; transition: all 0.2s ease;"
                                            onmouseover="this.style.background='rgba(220, 53, 69, 0.15)'; this.style.borderColor='rgba(220, 53, 69, 0.3)'; this.style.color='#dc3545'"
                                            onmouseout="this.style.background='rgba(40, 167, 69, 0.12)'; this.style.borderColor='rgba(40, 167, 69, 0.25)'; this.style.color='#28a745'"
                                            onclick="deleteRule('${rule.id}'); event.stopPropagation();">
                                            <span style="margin-right: 4px;">×</span>${i18n.rules_delete}
                                        </button>
                                    </div>
                                </div>
                            `;
                            // Only attach click handler to the header
                            const header = item.querySelector('[data-header="true"]');
                            header.onclick = (e) => {
                                if (!e.target.closest('.rule-actions')) {
                                    editRule(rule.id);
                                }
                            };
                            customContainer.appendChild(item);
                        });
                    }

                    // Update converter dropdown
                    updateConverterRulesDropdown(builtinRules, customRules);
                })
                .catch(error => console.error('Error:', error));
        }

        function updateConverterRulesDropdown(builtinRules, customRules) {
            const ruleMenu = document.getElementById('rule-menu');
            const ruleHiddenInput = document.getElementById('rule-template');
            if (!ruleMenu || !ruleHiddenInput) return;

            // Clear existing options
            ruleMenu.innerHTML = '';

            let firstRuleName = null;

            // Add built-in rules first
            builtinRules.forEach((rule, index) => {
                if (index === 0) firstRuleName = rule.name;

                const option = document.createElement('div');
                option.className = 'custom-dropdown-option builtin';
                option.setAttribute('data-value', rule.name);
                option.innerHTML = `
                    <span class="material-symbols-outlined">widgets</span>
                    <span>${rule.name}</span>
                `;
                option.onclick = () => selectRuleOption(rule.name, 'builtin');
                ruleMenu.appendChild(option);
            });

            // Add custom rules
            customRules.forEach(rule => {
                const option = document.createElement('div');
                option.className = 'custom-dropdown-option custom';
                option.setAttribute('data-value', rule.name);
                option.innerHTML = `
                    <span class="material-symbols-outlined">edit_square</span>
                    <span>${rule.name}</span>
                `;
                option.onclick = () => selectRuleOption(rule.name, 'custom');
                ruleMenu.appendChild(option);
            });

            // Set first rule as default
            if (firstRuleName) {
                selectRuleOption(firstRuleName, 'builtin');
            }
        }

        function toggleRuleDropdown() {
            const selected = document.getElementById('rule-selected');
            const menu = document.getElementById('rule-menu');

            selected.classList.toggle('active');
            menu.classList.toggle('show');
        }

        function selectRuleOption(value, type) {
            const selectedText = document.getElementById('rule-selected-text');
            const selectedDiv = document.getElementById('rule-selected');
            const hiddenInput = document.getElementById('rule-template');
            const menu = document.getElementById('rule-menu');

            // Update hidden input value
            hiddenInput.value = value;

            // Update selected text
            selectedText.textContent = value;

            // Update icon and color
            const icon = selectedDiv.querySelector('.material-symbols-outlined');
            if (type === 'builtin') {
                icon.textContent = 'widgets';
                icon.style.color = '#2196F3';
            } else {
                icon.textContent = 'edit_square';
                icon.style.color = '#4CAF50';
            }

            // Update selected state in options
            document.querySelectorAll('.custom-dropdown-option').forEach(opt => {
                opt.classList.remove('selected');
            });
            const selectedOption = document.querySelector(`[data-value="${value}"]`);
            if (selectedOption) {
                selectedOption.classList.add('selected');
            }

            // Close dropdown
            selectedDiv.classList.remove('active');
            menu.classList.remove('show');
        }

        // Close dropdown when clicking outside
        document.addEventListener('click', function(event) {
            const dropdown = document.getElementById('rule-template-dropdown');
            if (dropdown && !dropdown.contains(event.target)) {
                document.getElementById('rule-selected').classList.remove('active');
                document.getElementById('rule-menu').classList.remove('show');
            }

            // Also close interval unit dropdown when clicking outside
            const intervalDropdown = document.getElementById('interval-unit-dropdown');
            if (intervalDropdown && !intervalDropdown.contains(event.target)) {
                const selected = document.getElementById('interval-unit-selected');
                const menu = document.getElementById('interval-unit-menu');
                if (selected && menu) {
                    selected.classList.remove('active');
                    menu.classList.remove('show');
                }
            }
        });

        // Interval unit dropdown functions
        function toggleIntervalUnitDropdown() {
            const selected = document.getElementById('interval-unit-selected');
            const menu = document.getElementById('interval-unit-menu');

            selected.classList.toggle('active');
            menu.classList.toggle('show');
        }

        function selectIntervalUnit(minutes, text) {
            const selectedText = document.getElementById('interval-unit-selected-text');
            const selectedDiv = document.getElementById('interval-unit-selected');
            const hiddenInput = document.getElementById('update-interval-unit');
            const menu = document.getElementById('interval-unit-menu');

            // Update hidden input value
            hiddenInput.value = minutes;

            // Update selected text
            selectedText.textContent = text;

            // Update selected state in options
            const intervalMenu = document.getElementById('interval-unit-menu');
            intervalMenu.querySelectorAll('.custom-dropdown-option').forEach(opt => {
                opt.classList.remove('selected');
                if (parseInt(opt.getAttribute('data-value')) === minutes) {
                    opt.classList.add('selected');
                }
            });

            // Close dropdown
            selectedDiv.classList.remove('active');
            menu.classList.remove('show');

            // Recalculate interval hours
            updateIntervalHours();
        }

        // Generic dropdown toggle function
        function toggleDropdown(dropdownId) {
            const dropdown = document.getElementById(dropdownId);
            if (!dropdown) return;

            const selected = dropdown.querySelector('.custom-dropdown-selected');
            const menu = dropdown.querySelector('.custom-dropdown-menu');

            // Close other dropdowns first
            document.querySelectorAll('.custom-dropdown').forEach(dd => {
                if (dd.id !== dropdownId) {
                    dd.querySelector('.custom-dropdown-selected')?.classList.remove('active');
                    dd.querySelector('.custom-dropdown-menu')?.classList.remove('show');
                }
            });

            selected.classList.toggle('active');
            menu.classList.toggle('show');
        }

        // Generic option selection function
        function selectOption(fieldId, value, displayText) {
            const hiddenInput = document.getElementById(fieldId);
            const textElement = document.getElementById(fieldId + '-text');
            const dropdown = document.getElementById(fieldId + '-dropdown');

            if (!hiddenInput || !textElement || !dropdown) return;

            // Update hidden input value
            hiddenInput.value = value;

            // Update display text
            textElement.textContent = displayText;

            // Update selected state in options
            const menu = dropdown.querySelector('.custom-dropdown-menu');
            menu.querySelectorAll('.custom-dropdown-option').forEach(opt => {
                opt.classList.remove('selected');
            });
            event.target.classList.add('selected');

            // Close dropdown
            const selected = dropdown.querySelector('.custom-dropdown-selected');
            const menuEl = dropdown.querySelector('.custom-dropdown-menu');
            selected.classList.remove('active');
            menuEl.classList.remove('show');
        }

        // Close all dropdowns when clicking outside
        document.addEventListener('click', function(event) {
            if (!event.target.closest('.custom-dropdown')) {
                document.querySelectorAll('.custom-dropdown').forEach(dd => {
                    dd.querySelector('.custom-dropdown-selected')?.classList.remove('active');
                    dd.querySelector('.custom-dropdown-menu')?.classList.remove('show');
                });
            }
        });

        function showCreateRuleModal() {
            const modal = new bootstrap.Modal(document.getElementById('createRuleModal'));
            // Clear form
            document.getElementById('new-rule-name').value = '';
            document.getElementById('new-rule-desc').value = '';
            document.getElementById('new-rule-content').value = '# New Rule' + String.fromCharCode(10) + 'MATCH,🚀 Proxy';
            modal.show();
        }

        function importTemplate(templateName) {
            // Get rule by name from the built-in templates
            axios.get(BASE_PATH + '/api/rules/by-name/' + templateName)
                .then(response => {
                    const rule = response.data;
                    // Import the content into the textarea
                    document.getElementById('new-rule-content').value = rule.content;

                    // Show success modal instead of toast
                    showAlertModal({
                        title: i18n.modal_template_imported,
                        message: i18n.modal_template_imported_message
                    });
                })
                .catch(error => {
                    showAlertModal({
                        title: i18n.unknown_error,
                        message: 'Failed to import template: ' + (error.response?.data?.error || 'Unknown error')
                    });
                });
        }

        function showToast(title, message, type) {
            // Create toast container if it doesn't exist
            let toastContainer = document.getElementById('toast-container');
            if (!toastContainer) {
                toastContainer = document.createElement('div');
                toastContainer.id = 'toast-container';
                toastContainer.className = 'position-fixed top-0 end-0 p-3';
                toastContainer.style.zIndex = '9999';
                document.body.appendChild(toastContainer);
            }

            // Create toast element
            const toastId = 'toast-' + Date.now();
            const bgClass = type === 'success' ? 'bg-success' : 'bg-danger';
            const toastHTML = `
                <div id="${toastId}" class="toast align-items-center text-white ${bgClass} border-0" role="alert" aria-live="assertive" aria-atomic="true">
                    <div class="d-flex">
                        <div class="toast-body">
                            <strong>${title}</strong><br>${message}
                        </div>
                        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                    </div>
                </div>
            `;

            toastContainer.insertAdjacentHTML('beforeend', toastHTML);
            const toastElement = document.getElementById(toastId);
            const toast = new bootstrap.Toast(toastElement, { delay: 4000 });
            toast.show();

            // Remove toast element after it's hidden
            toastElement.addEventListener('hidden.bs.toast', function() {
                toastElement.remove();
            });
        }

        function createRuleFromModal() {
            const name = document.getElementById('new-rule-name').value.trim();
            const description = document.getElementById('new-rule-desc').value.trim();
            const content = document.getElementById('new-rule-content').value.trim();

            if (!name) {
                showAlertModal({title: i18n.unknown_error, message: i18n.rules_name_empty});
                return;
            }

            if (!content) {
                showAlertModal({title: i18n.unknown_error, message: i18n.rules_content_empty});
                return;
            }

            axios.post(BASE_PATH + '/api/rules', {
                name: name,
                description: description,
                content: content
            })
            .then(response => {
                // Hide modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('createRuleModal'));
                modal.hide();
                showAlertModal({title: i18n.modal_ok, message: i18n.rules_create_success});
                loadRules();
            })
            .catch(error => {
                showAlertModal({title: i18n.unknown_error, message: i18n.alerts_rule_create_failed + (error.response?.data?.error || i18n.unknown_error)});
            });
        }

        async function restoreRule(id, ruleName) {
            const confirmed = await showConfirmModal({
                title: i18n.modal_restore_title,
                message: i18n.modal_restore_message,
                confirmText: i18n.modal_restore_confirm,
                cancelText: i18n.modal_cancel,
                confirmColor: '#ffc107'
            });

            if (!confirmed) return;

            // Call backend API to restore rule
            axios.post(`/api/rules/${id}/restore`)
                .then(response => {
                    showAlertModal({
                        title: i18n.modal_restore_title,
                        message: `"${ruleName}" ` + (i18n.rule_restored_success)
                    });
                    loadRules();
                })
                .catch(error => {
                    showAlertModal({
                        title: i18n.unknown_error,
                        message: 'Failed to restore rule: ' + (error.response?.data?.error || 'Unknown error')
                    });
                });
        }

        function createRule() {
            // Legacy function - redirect to modal
            showCreateRuleModal();
        }

        function editRule(id) {
            // Check if already in edit mode
            const ruleItem = document.querySelector(`[data-rule-id="${id}"]`);
            if (!ruleItem) return;

            const existingForm = ruleItem.querySelector('.rule-edit-form');

            if (existingForm && existingForm.classList.contains('show')) {
                // If already editing, collapse it
                existingForm.classList.remove('show');
                ruleItem.classList.remove('expanded');
                setTimeout(() => {
                    if (!existingForm.classList.contains('show')) {
                        existingForm.style.display = 'none';
                    }
                }, 150);
                return;
            }

            // Get rule details and show inline edit form
            axios.get(BASE_PATH + '/api/rules/' + id)
                .then(response => {
                    const rule = response.data;

                    // Check if this is a built-in rule
                    const builtinNames = ['Default Routing', 'Default Routing (Chinese Interface)', 'Academic & Research Routing', 'Minimal Rules'];
                    const isBuiltin = builtinNames.includes(rule.name);

                    // Check if edit form already exists
                    let editForm = ruleItem.querySelector('.rule-edit-form');
                    if (!editForm) {
                        // Create edit form
                        const escapedContent = rule.content.replace(/&/g, '&amp;')
                                                          .replace(/</g, '&lt;')
                                                          .replace(/>/g, '&gt;')
                                                          .replace(/"/g, '&quot;')
                                                          .replace(/'/g, '&#039;');
                        const escapedName = rule.name.replace(/"/g, '&quot;').replace(/'/g, '&#039;');
                        const escapedDesc = (rule.description || '').replace(/"/g, '&quot;').replace(/'/g, '&#039;');

                        const readonlyAttr = isBuiltin ? 'readonly' : '';
                        const readonlyClass = isBuiltin ? 'bg-light' : '';
                        const editFormHTML = `
                            <div class="rule-edit-form" style="display: none;">
                                <div class="mb-3">
                                    <label class="form-label"><strong>${i18n.rules_rule_name_col}</strong></label>
                                    ${isBuiltin ? `<div class="input-group">
                                        <span class="input-group-text bg-light"><span class="material-symbols-outlined" style="font-size: 16px;">lock</span></span>
                                        <input type="text" id="edit-name-${id}" class="form-control ${readonlyClass}" value="${escapedName}" ${readonlyAttr}>
                                    </div>` : `<input type="text" id="edit-name-${id}" class="form-control" value="${escapedName}">`}
                                </div>
                                <div class="mb-3">
                                    <label class="form-label"><strong>${i18n.rules_rule_description_col}</strong></label>
                                    ${isBuiltin ? `<div class="input-group">
                                        <span class="input-group-text bg-light"><span class="material-symbols-outlined" style="font-size: 16px;">lock</span></span>
                                        <input type="text" id="edit-desc-${id}" class="form-control ${readonlyClass}" value="${escapedDesc}" ${readonlyAttr}>
                                    </div>` : `<input type="text" id="edit-desc-${id}" class="form-control" value="${escapedDesc}">`}
                                </div>
                                <div class="mb-3">
                                    <label class="form-label"><strong>${i18n.rules_rule_content_col}</strong></label>
                                    <textarea id="edit-content-${id}" class="rule-edit-textarea" placeholder="Enter rule content...">${escapedContent}</textarea>
                                </div>
                                <div class="rule-edit-buttons">
                                    <button class="btn btn-success" onclick="saveRule('${id}'); event.stopPropagation();"><span class="material-symbols-outlined icon-btn">save</span> ${i18n.rules_save}</button>
                                    <button class="btn btn-secondary" onclick="cancelEdit(\'${id}\'); event.stopPropagation();"><span class="material-symbols-outlined icon-btn">cancel</span> ${i18n.rules_cancel}</button>
                                </div>
                            </div>
                        `;
                        ruleItem.insertAdjacentHTML('beforeend', editFormHTML);
                        editForm = ruleItem.querySelector('.rule-edit-form');
                    } else {
                        // Update existing form data
                        document.getElementById('edit-name-' + id).value = rule.name;
                        document.getElementById('edit-desc-' + id).value = rule.description || '';
                        document.getElementById('edit-content-' + id).value = rule.content;
                    }

                    // Show edit form with smooth animation
                    editForm.style.display = 'block';
                    editForm.offsetHeight; // Force reflow
                    editForm.classList.add('show');
                    ruleItem.classList.add('expanded');
                })
                .catch(error => {
                    showAlertModal({title: i18n.unknown_error, message: i18n.alerts_rule_get_failed + (error.response?.data?.error || i18n.unknown_error)});
                });
        }

        async function saveRule(id) {
            const name = document.getElementById('edit-name-' + id).value;
            const description = document.getElementById('edit-desc-' + id).value;
            const content = document.getElementById('edit-content-' + id).value;

            if (!name.trim()) {
                showAlertModal({
                    title: i18n.unknown_error,
                    message: i18n.rule_name_empty
                });
                return;
            }

            if (!content.trim()) {
                showAlertModal({
                    title: i18n.unknown_error,
                    message: i18n.rule_content_empty
                });
                return;
            }

            const confirmed = await showConfirmModal({
                title: i18n.modal_save_title,
                message: i18n.modal_save_message,
                confirmText: i18n.modal_save_confirm,
                cancelText: i18n.modal_cancel,
                confirmColor: '#28a745'
            });

            if (!confirmed) return;

            axios.put(BASE_PATH + '/api/rules/' + id, {
                name: name,
                description: description,
                content: content
            })
            .then(response => {
                showAlertModal({
                    title: i18n.modal_save_title,
                    message: i18n.rule_updated_success
                });
                cancelEdit(id);
                loadRules();
            })
            .catch(error => {
                showAlertModal({
                    title: i18n.unknown_error,
                    message: 'Update failed: ' + (error.response?.data?.error || 'Unknown error')
                });
            });
        }

        function cancelEdit(id) {
            if (id) {
                // Hide specific edit form with smooth animation
                const ruleItem = document.querySelector(`[data-rule-id="${id}"]`);
                if (ruleItem) {
                    const editForm = ruleItem.querySelector('.rule-edit-form');
                    if (editForm) {
                        editForm.classList.remove('show');
                        setTimeout(() => {
                            if (!editForm.classList.contains('show')) {
                                editForm.style.display = 'none';
                            }
                        }, 300);
                    }

                    // Reset button chevron
                    const editButton = ruleItem.querySelector(`button[onclick="editRule('${id}')"]`);
                    if (editButton) {
                        const chevron = editButton.querySelector('.rule-edit-chevron');
                        if (chevron) {
                            chevron.classList.remove('expanded');
                        }
                    }
                }
            } else {
                // Hide all edit forms smoothly
                document.querySelectorAll('.rule-edit-form.show').forEach(form => {
                    form.classList.remove('show');
                    setTimeout(() => {
                        if (!form.classList.contains('show')) {
                            form.style.display = 'none';
                        }
                    }, 300);
                });

                // Reset all chevrons
                document.querySelectorAll('.rule-edit-chevron').forEach(chevron => {
                    chevron.classList.remove('expanded');
                });
            }
        }

        async function deleteRule(id) {
            const confirmed = await showConfirmModal({
                title: i18n.modal_delete_history_title,
                message: i18n.rule_delete_confirm,
                confirmText: i18n.modal_delete_confirm,
                cancelText: i18n.modal_cancel,
                confirmColor: '#dc3545'
            });

            if (!confirmed) return;

            axios.delete(BASE_PATH + '/api/rules/' + id)
                .then(response => {
                    showAlertModal({
                        title: i18n.modal_delete_confirm,
                        message: i18n.delete_success
                    });
                    loadRules();
                })
                .catch(error => {
                    showAlertModal({
                        title: i18n.unknown_error,
                        message: 'Delete failed: ' + (error.response?.data?.error || error.message)
                    });
                });
        }

        async function restartService() {
            const confirmed = await showConfirmModal({
                title: i18n.modal_restart_title,
                message: i18n.modal_restart_message,
                confirmText: i18n.modal_restart_confirm,
                cancelText: i18n.modal_cancel,
                confirmColor: '#ffc107'
            });

            if (!confirmed) {
                return;
            }

            // Show loading modal
            const modal = document.createElement('div');
            modal.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.7);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 9999;
            `;

            const content = document.createElement('div');
            content.style.cssText = `
                background: white;
                padding: 30px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            `;
            content.innerHTML = `
                <div style="margin-bottom: 20px;">
                    <div style="animation: spin 1s linear infinite;"><span class="material-symbols-outlined" style="font-size: 40px; color: #667eea;">refresh</span></div>
                </div>
                <h4 style="margin: 0 0 10px 0;">Restarting Service...</h4>
                <p style="margin: 0; color: #666;">Please wait, the service is restarting</p>
            `;

            modal.appendChild(content);
            document.body.appendChild(modal);

            // Add spinning animation
            const style = document.createElement('style');
            style.textContent = `
                @keyframes spin {
                    from { transform: rotate(0deg); }
                    to { transform: rotate(360deg); }
                }
            `;
            document.head.appendChild(style);

            axios.post(BASE_PATH + '/api/restart')
                .then(response => {
                    setTimeout(() => {
                        window.location.reload();
                    }, 3000);
                })
                .catch(error => {
                    document.body.removeChild(modal);
                    showAlertModal({title: i18n.unknown_error, message: i18n.alerts_restart_failed + (error.response?.data?.error || i18n.unknown_error)});
                });
        }

        async function changeAccount() {
            const currentPassword = document.getElementById('current-password').value;
            const newUsername = document.getElementById('new-username').value;
            const newPassword = document.getElementById('new-password').value;
            const confirmPassword = document.getElementById('confirm-password').value;

            if (!currentPassword) {
                showAlertModal({
                    title: i18n.unknown_error,
                    message: i18n.account_password_required
                });
                return;
            }

            // If a new password is set, check the confirmation password
            if (newPassword && newPassword !== confirmPassword) {
                showAlertModal({
                    title: i18n.unknown_error,
                    message: i18n.account_password_mismatch
                });
                return;
            }

            if (!newUsername && !newPassword) {
                showAlertModal({
                    title: i18n.unknown_error,
                    message: i18n.account_change_required
                });
                return;
            }

            const confirmed = await showConfirmModal({
                title: i18n.modal_update_account_title,
                message: i18n.modal_update_account_message,
                confirmText: i18n.modal_save_confirm,
                cancelText: i18n.modal_cancel,
                confirmColor: '#28a745'
            });

            if (!confirmed) return;

            axios.post(BASE_PATH + '/api/change-account', {
                current_password: currentPassword,
                new_username: newUsername || null,
                new_password: newPassword || null
            })
            .then(response => {
                showAlertModal({
                    title: i18n.modal_account_updated_title,
                    message: i18n.modal_account_updated_message
                });
                setTimeout(() => {
                    window.location.href = '/logout';
                }, 2000);
            })
            .catch(error => {
                showAlertModal({
                    title: i18n.unknown_error,
                    message: i18n.account_update_failed_prefix + (error.response?.data?.error || i18n.unknown_error)
                });
            });
        }

        // Settings collapse/expand function
        function toggleSettingsSection(sectionId) {
            const content = document.getElementById('content-' + sectionId);
            const icon = document.getElementById('icon-' + sectionId);
            const header = icon.closest('.settings-collapse-header');
            const titleElement = header.querySelector('h6');
            const iconElement = header.querySelector('.material-symbols-outlined:not(.settings-collapse-icon)');

            if (content.style.display === 'none') {
                // Expand - use deeper gradient background (all sections use same purple-blue gradient)
                content.style.display = 'block';
                icon.style.transform = 'rotate(180deg)';
                header.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.25) 0%, rgba(118, 75, 162, 0.25) 100%)';
                icon.style.color = '#667eea';
            } else {
                // Collapse - restore original lighter gradient background
                content.style.display = 'none';
                icon.style.transform = 'rotate(0deg)';
                icon.style.color = '#6c757d';
                header.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%)';
            }
        }

        // Settings functions
        async function saveSystemSettings() {
            const port = document.getElementById('server-port').value;
            const host = document.getElementById('server-host').value;
            const basePath = document.getElementById('panel-base-path').value;
            const sslEnabled = document.getElementById('ssl-enabled').value === 'true';
            const sslDomain = document.getElementById('ssl-domain').value;
            const sslCert = document.getElementById('ssl-cert').value;
            const sslKey = document.getElementById('ssl-key').value;
            const logLevel = document.getElementById('log-level').value;
            const logFile = document.getElementById('log-file').value;
            const accessLog = document.getElementById('enable-access-log').checked;
            const debugMode = document.getElementById('debug-mode').checked;

            // basePath is now just the segment (e.g., "subprotox"), no validation needed

            // Validate SSL settings if enabled
            if (sslEnabled) {
                if (!sslCert || !sslKey) {
                    showAlertModal({
                        title: i18n.unknown_error,
                        message: i18n.ssl_validation_empty
                    });
                    return;
                }
                if (!sslDomain) {
                    showAlertModal({
                        title: i18n.unknown_error,
                        message: i18n.ssl_validation_domain
                    });
                    return;
                }
            }

            // Confirm before saving
            const confirmed = await showConfirmModal({
                title: i18n.modal_save_settings_title,
                message: i18n.modal_save_settings_message,
                confirmText: i18n.modal_save_confirm,
                cancelText: i18n.modal_cancel,
                confirmColor: '#28a745'
            });

            if (!confirmed) return;

            // Send settings to server
            axios.post(BASE_PATH + '/api/settings/system', {
                port: port || null,
                host: host || null,
                base_path: basePath || null,
                ssl_enabled: sslEnabled,
                ssl_domain: sslDomain || null,
                ssl_cert_path: sslCert || null,
                ssl_key_path: sslKey || null,
                log_level: logLevel || null,
                log_file: logFile || null,
                access_log: accessLog,
                debug_mode: debugMode
            })
            .then(async response => {
                if (response.data.success) {
                    if (response.data.base_path_changed) {
                        // Base path changed - show special warning
                        const newPath = response.data.new_base_path;
                        const protocol = window.location.protocol;
                        const host = window.location.host;
                        const newUrl = `${protocol}//${host}${newPath}`;

                        showAlertModal({
                            title: i18n.modal_settings_saved_title,
                            message: response.data.message + String.fromCharCode(10) + String.fromCharCode(10) +
                                  i18n.settings_new_url_label + newUrl + String.fromCharCode(10) + String.fromCharCode(10) +
                                  i18n.settings_manual_restart
                        });
                    } else {
                        showAlertModal({
                            title: i18n.modal_settings_saved_title,
                            message: i18n.modal_settings_saved_message
                        });

                        // Ask to restart for non-base_path changes
                        const shouldRestart = await showConfirmModal({
                            title: i18n.modal_restart_now_title,
                            message: i18n.modal_restart_now_message,
                            confirmText: i18n.modal_restart_confirm,
                            cancelText: i18n.modal_cancel,
                            confirmColor: '#dc3545'
                        });

                        if (shouldRestart) {
                            restartService();
                        }
                    }
                } else {
                    showAlertModal({
                        title: i18n.unknown_error,
                        message: i18n.settings_failed_prefix + (response.data.error || i18n.unknown_error)
                    });
                }
            })
            .catch(error => {
                showAlertModal({
                    title: i18n.unknown_error,
                    message: i18n.settings_failed_prefix + (error.response?.data?.error || i18n.unknown_error)
                });
            });
        }

        async function saveConversionSettings() {
            const confirmed = await showConfirmModal({
                title: i18n.modal_save_conversion_title,
                message: i18n.modal_save_conversion_message,
                confirmText: i18n.modal_save_confirm,
                cancelText: i18n.modal_cancel,
                confirmColor: '#28a745'
            });

            if (!confirmed) return;

            showAlertModal({
                title: i18n.modal_conversion_saved_title,
                message: i18n.lang === 'zh'
                    ? '转换设置保存功能将在配置文件管理中实现'
                    : 'Conversion settings save functionality will be implemented in config file management'
            });
        }

        async function cleanOldHistory() {
            const confirmed = await showConfirmModal({
                title: i18n.modal_clean_records_title,
                message: i18n.modal_clean_records_message,
                confirmText: i18n.modal_delete_confirm,
                cancelText: i18n.modal_cancel,
                confirmColor: '#dc3545'
            });

            if (!confirmed) return;

            showAlertModal({
                title: i18n.modal_records_cleaned_title,
                message: i18n.modal_records_cleaned_message
            });
            // This could call an API endpoint to clean old records
        }

        async function optimizeDatabase() {
            const confirmed = await showConfirmModal({
                title: i18n.modal_optimize_db_title,
                message: i18n.modal_optimize_db_message,
                confirmText: i18n.modal_ok,
                cancelText: i18n.modal_cancel,
                confirmColor: '#28a745'
            });

            if (!confirmed) return;

            showAlertModal({
                title: i18n.modal_db_optimized_title,
                message: i18n.modal_db_optimized_message
            });
            // This could call an API endpoint to run VACUUM on SQLite
        }

        async function exportBackup() {
            const confirmed = await showConfirmModal({
                title: i18n.modal_export_backup_title,
                message: i18n.modal_export_backup_message,
                confirmText: i18n.modal_ok,
                cancelText: i18n.modal_cancel,
                confirmColor: '#28a745'
            });

            if (!confirmed) return;

            showAlertModal({
                title: i18n.modal_backup_exported_title,
                message: i18n.modal_backup_exported_message
            });
            // This could trigger a download of the database file
        }

        // Fetch GitHub stars
        function fetchGitHubStars() {
            const repoUrl = 'https://api.github.com/repos/maxiao0234/SubProtoX';

            fetch(repoUrl)
                .then(response => {
                    if (!response.ok) {
                        console.log('GitHub repository not found yet - stars count will not be displayed');
                        return null;
                    }
                    return response.json();
                })
                .then(data => {
                    if (data && data.stargazers_count !== undefined) {
                        document.getElementById('star-count').textContent = data.stargazers_count;
                    }
                })
                .catch(error => {
                    console.log('GitHub API not available:', error.message);
                });
        }

        // Update interval calculation function (global scope for use by dropdown)
        function updateIntervalHours() {
            const intervalValue = document.getElementById('update-interval-value');
            const intervalUnit = document.getElementById('update-interval-unit');
            const intervalHidden = document.getElementById('update-interval');

            if (!intervalValue || !intervalUnit || !intervalHidden) return;

            const value = parseInt(intervalValue.value) || 0;
            const unitMinutes = parseInt(intervalUnit.value);
            const hours = Math.round((value * unitMinutes) / 60 * 100) / 100; // Convert to hours and round to 2 decimals
            intervalHidden.value = hours;
        }

        // Page load
        document.addEventListener('DOMContentLoaded', () => {
            loadRules();
            loadHistory();
            fetchGitHubStars(); // Fetch GitHub stars on page load

            // Setup update interval input event listener
            const intervalValue = document.getElementById('update-interval-value');
            if (intervalValue) {
                intervalValue.addEventListener('input', updateIntervalHours);
                updateIntervalHours(); // Initial calculation
            }
        });
    {% endraw %}
    </script>
</body>
</html>
'''
