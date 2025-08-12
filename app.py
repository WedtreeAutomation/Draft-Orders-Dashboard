import os
import io
import random
import re
from datetime import datetime, timedelta
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import random
from streamlit_extras.stylable_container import stylable_container
from dotenv import load_dotenv
import hashlib

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Shopify Draft Orders Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for modern, professional design with attractive login
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
        
        :root {
            --primary: #667eea;
            --primary-dark: #5a6fd8;
            --secondary: #764ba2;
            --accent: #f093fb;
            --accent-light: #f5576c;
            --success: #10b981;
            --success-dark: #059669;
            --warning: #f59e0b;
            --danger: #ef4444;
            --background: #f8fafc;
            --background-alt: #f1f5f9;
            --card: #ffffff;
            --card-shadow: rgba(0, 0, 0, 0.04);
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --text-light: #94a3b8;
            --border: #e2e8f0;
            --border-light: #f1f5f9;
            --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --gradient-accent: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            --gradient-success: linear-gradient(135deg, #10b981 0%, #059669 100%);
            --gradient-rainbow: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
            --gradient-aurora: linear-gradient(135deg, #a8edea 0%, #fed6e3 50%, #d299c2 100%);
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            --shadow-glow: 0 0 40px rgba(102, 126, 234, 0.3);
        }
        
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        .main {
            background: var(--gradient-primary);
            padding: 0;
            min-height: 100vh;
        }
        
        .main > div {
            background: var(--background);
            border-radius: 24px 24px 0 0;
            margin-top: 1rem;
            padding: 2rem;
            min-height: calc(100vh - 2rem);
            box-shadow: var(--shadow-xl);
        }
        
        /* Enhanced Login Styles */
        .login-page {
            background: var(--gradient-rainbow);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
            position: relative;
            overflow: hidden;
        }
        
        .login-page::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
            animation: float 20s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            33% { transform: translateY(-20px) rotate(1deg); }
            66% { transform: translateY(-10px) rotate(-1deg); }
        }
        
        .login-container {
            max-width: 450px;
            width: 100%;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 32px;
            padding: 3rem 2.5rem;
            box-shadow: var(--shadow-glow), var(--shadow-xl);
            text-align: center;
            position: relative;
            z-index: 10;
            animation: slideUp 0.8s ease-out;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .login-header {
            margin-bottom: 2.5rem;
        }
        
        .login-logo {
            width: 100px;
            height: 100px;
            background: var(--gradient-rainbow);
            border-radius: 28px;
            margin: 0 auto 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.5rem;
            color: white;
            box-shadow: var(--shadow-glow);
            animation: pulse 2s ease-in-out infinite alternate;
            position: relative;
            overflow: hidden;
        }
        
        .login-logo::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shine 3s ease-in-out infinite;
        }
        
        @keyframes pulse {
            from { box-shadow: var(--shadow-glow); }
            to { box-shadow: 0 0 60px rgba(102, 126, 234, 0.5); }
        }
        
        @keyframes shine {
            0% { transform: translateX(-100%) translateY(-100%) rotate(30deg); }
            50% { transform: translateX(100%) translateY(100%) rotate(30deg); }
            100% { transform: translateX(-100%) translateY(-100%) rotate(30deg); }
        }
        
        .login-title {
            font-family: 'Poppins', sans-serif;
            font-size: 2.25rem;
            font-weight: 800;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0 0 0.75rem 0;
            line-height: 1.2;
        }
        
        .login-subtitle {
            color: var(--text-secondary);
            font-size: 1rem;
            font-weight: 500;
            margin-bottom: 1rem;
        }
        
        .login-features {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .login-feature {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.8rem;
            color: var(--text-secondary);
            font-weight: 500;
        }
        
        .login-feature-icon {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: var(--gradient-accent);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
        }
        
        .stTextInput > div > div > input {
            border-radius: 16px !important;
            border: 2px solid var(--border) !important;
            padding: 16px 20px !important;
            font-size: 16px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            background: rgba(255, 255, 255, 0.8) !important;
            backdrop-filter: blur(10px) !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15) !important;
            background: white !important;
            transform: translateY(-2px) !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: var(--text-light) !important;
            font-weight: 400 !important;
        }
        
        .login-button {
            width: 100% !important;
            background: var(--gradient-rainbow) !important;
            color: white !important;
            border: none !important;
            border-radius: 16px !important;
            padding: 16px 32px !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            font-family: 'Poppins', sans-serif !important;
            margin-top: 1.5rem !important;
            transition: all 0.3s ease !important;
            box-shadow: var(--shadow-lg) !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }
        
        .login-button:hover {
            transform: translateY(-3px) !important;
            box-shadow: var(--shadow-glow), var(--shadow-xl) !important;
        }
        
        .login-security {
            margin-top: 2rem;
            padding: 1.5rem;
            background: var(--gradient-aurora);
            border-radius: 20px;
            color: var(--text-secondary);
            font-size: 0.85rem;
            font-weight: 500;
        }
        
        .login-particles {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: 1;
        }
        
        .particle {
            position: absolute;
            background: rgba(255, 255, 255, 0.6);
            border-radius: 50%;
            animation: float-particle 15s infinite linear;
        }
        
        @keyframes float-particle {
            0% {
                transform: translateY(100vh) rotate(0deg);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-100vh) rotate(360deg);
                opacity: 0;
            }
        }
        
        /* Sidebar Styles */
        .sidebar .sidebar-content {
            background: var(--gradient-primary);
            border-radius: 0 24px 24px 0;
            padding: 0;
        }
        
        .sidebar .sidebar-content .block-container {
            padding: 2rem 1rem;
        }
        
        .sidebar-header {
            text-align: center;
            margin-bottom: 2rem;
            padding: 1rem;
        }
        
        .sidebar-logo {
            width: 80px;
            height: 80px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            margin: 0 auto 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            backdrop-filter: blur(10px);
        }
        
        .sidebar-title {
            color: white;
            font-weight: 700;
            font-size: 1.125rem;
            margin: 0;
        }
        
        .sidebar-subtitle {
            color: rgba(255, 255, 255, 0.8);
            font-size: 0.75rem;
            margin: 0.25rem 0 0 0;
        }
        
        /* Main Content Styles */
        .dashboard-header {
            text-align: center;
            margin-bottom: 3rem;
            padding: 2rem 0;
        }
        
        .dashboard-title {
            font-size: 3.5rem;
            font-weight: 800;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0 0 1rem 0;
            line-height: 1.1;
        }
        
        .dashboard-subtitle {
            font-size: 1.25rem;
            color: var(--text-secondary);
            max-width: 600px;
            margin: 0 auto 2rem;
            line-height: 1.6;
        }
        
        .feature-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: var(--gradient-accent);
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 50px;
            font-size: 0.875rem;
            font-weight: 600;
            box-shadow: var(--shadow-md);
        }
        
        /* Metric Cards */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .metric-card {
            background: var(--card);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: var(--shadow-lg);
            transition: all 0.3s ease;
            border: 1px solid var(--border-light);
            position: relative;
            overflow: hidden;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--gradient-primary);
        }
        
        .metric-card.accent::before {
            background: var(--gradient-accent);
        }
        
        .metric-card.secondary::before {
            background: var(--gradient-secondary);
        }
        
        .metric-card.success::before {
            background: var(--gradient-success);
        }
        
        .metric-card:hover {
            transform: translateY(-8px);
            box-shadow: var(--shadow-xl);
        }
        
        .metric-icon {
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            margin-bottom: 1rem;
            background: var(--gradient-primary);
            color: white;
        }
        
        .metric-card.accent .metric-icon {
            background: var(--gradient-accent);
        }
        
        .metric-card.secondary .metric-icon {
            background: var(--gradient-secondary);
        }
        
        .metric-card.success .metric-icon {
            background: var(--gradient-success);
        }
        
        .metric-title {
            color: var(--text-light);
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem;
        }
        
        .metric-value {
            color: var(--text-primary);
            font-size: 2rem;
            font-weight: 700;
            margin: 0;
        }
        
        .metric-change {
            font-size: 0.875rem;
            margin-top: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }
        
        .metric-change.positive {
            color: var(--success);
        }
        
        .metric-change.negative {
            color: var(--danger);
        }
        
        /* Buttons */
        .stButton > button {
            background: var(--gradient-primary) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.75rem 2rem !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            transition: all 0.2s ease !important;
            box-shadow: var(--shadow-md) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: var(--shadow-lg) !important;
        }
        
        /* Refresh Button */
        .refresh-button {
            text-align: center;
            margin: 2rem 0;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: var(--card);
            border-radius: 16px;
            padding: 0.5rem;
            box-shadow: var(--shadow-md);
            border: 1px solid var(--border-light);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 12px;
            color: var(--text-secondary);
            font-weight: 600;
            padding: 1rem 2rem;
            transition: all 0.2s ease;
            border: none;
        }
        
        .stTabs [aria-selected="true"] {
            background: var(--gradient-primary);
            color: white;
            box-shadow: var(--shadow-sm);
        }
        
        /* Sidebar Filters */
        .sidebar-filter {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .sidebar-filter h3 {
            color: white;
            font-weight: 600;
            font-size: 1rem;
            margin: 0 0 1rem 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .sidebar .stSelectbox label,
        .sidebar .stMultiSelect label,
        .sidebar .stDateInput label,
        .sidebar .stCheckbox label {
            color: rgba(255, 255, 255, 0.9) !important;
            font-weight: 500 !important;
            font-size: 0.875rem !important;
        }
        
        /* Data Tables */
        .stDataFrame {
            border-radius: 20px;
            box-shadow: var(--shadow-lg);
            border: 1px solid var(--border-light);
            overflow: hidden;
        }
        
        /* Charts */
        .chart-container {
            background: var(--card);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: var(--shadow-lg);
            border: 1px solid var(--border-light);
            margin: 1rem 0;
        }
        
        /* Export Section */
        .export-section {
            background: var(--card);
            border-radius: 20px;
            padding: 3rem 2rem;
            box-shadow: var(--shadow-lg);
            border: 1px solid var(--border-light);
            text-align: center;
            margin: 2rem 0;
        }
        
        .export-icon {
            width: 80px;
            height: 80px;
            border-radius: 20px;
            background: var(--gradient-primary);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            margin: 0 auto 1.5rem;
        }
        
        .export-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-primary);
            margin: 0 0 0.5rem 0;
        }
        
        .export-description {
            color: var(--text-secondary);
            margin-bottom: 2rem;
            line-height: 1.6;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .main > div {
                padding: 1rem;
                margin-top: 0.5rem;
                border-radius: 16px 16px 0 0;
            }
            
            .dashboard-title {
                font-size: 2.5rem;
            }
            
            .dashboard-subtitle {
                font-size: 1rem;
            }
            
            .metric-card {
                padding: 1.5rem;
            }
            
            .metric-value {
                font-size: 1.75rem;
            }
            
            .login-container {
                margin: 1rem;
                padding: 2rem 1.5rem;
            }
            
            .login-title {
                font-size: 1.75rem;
            }
            
            .login-features {
                gap: 1rem;
            }
        }
        
        /* Status Indicators */
        .status-open {
            background: rgba(249, 115, 22, 0.1);
            color: #ea580c;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        .status-completed {
            background: rgba(16, 185, 129, 0.1);
            color: #059669;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        .status-invoiced {
            background: rgba(99, 102, 241, 0.1);
            color: #4f46e5;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        /* Loading Animation */
        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* Insights Panel */
        .insights-panel {
            background: var(--gradient-primary);
            color: white;
            padding: 2rem;
            border-radius: 20px;
            margin: 2rem 0;
        }
        
        .insights-title {
            font-size: 1.25rem;
            font-weight: 700;
            margin: 0 0 1rem 0;
            color: white;
        }
        
        .insight-item {
            margin: 1rem 0;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            backdrop-filter: blur(10px);
        }
        
        .insight-metric {
            font-size: 1.5rem;
            font-weight: 700;
            color: white;
        }
        
        .insight-label {
            font-size: 0.875rem;
            color: rgba(255, 255, 255, 0.8);
            margin-top: 0.25rem;
        }
    </style>
""", unsafe_allow_html=True)

def check_login():
    """Check if user is logged in"""
    return st.session_state.get('authenticated', False)

def create_login_particles():
    """Create floating particles for login page"""
    particles_html = '<div class="login-particles">'
    for i in range(20):
        size = f"{random.randint(3, 8)}px"
        left = f"{random.randint(0, 100)}%"
        delay = f"{random.randint(0, 15)}s"
        particles_html += f'<div class="particle" style="width: {size}; height: {size}; left: {left}; animation-delay: {delay};"></div>'
    particles_html += '</div>'
    return particles_html

def login_form():
    """Display a clean login form with title centered at top"""
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        .stApp {
            background-color: #ffffff;
            font-family: 'Inter', sans-serif;
        }
        
        .main-title {
            text-align: center;
            font-size: 2.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, #6366f1, #8b5cf6, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 3rem;
            letter-spacing: -0.02em;
        }
        
        .feature-grid {
            display: flex;
            flex-direction: column;
            gap: 32px;
            margin-bottom: 2rem;
        }
        
        .feature-item {
            background: #ffffff;
            border-radius: 16px;
            padding: 28px 24px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            border: 1px solid #f1f5f9;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            margin-bottom: 16px;
        }
        
        .feature-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #6366f1, #8b5cf6, #06b6d4);
            border-radius: 16px 16px 0 0;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .feature-item:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(99, 102, 241, 0.15);
            border-color: #e2e8f0;
        }
        
        .feature-item:hover::before {
            opacity: 1;
        }
        
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 16px;
            display: block;
        }
        
        .feature-title {
            font-weight: 600;
            font-size: 1.3rem;
            margin-bottom: 8px;
            color: #1e293b;
        }
        
        .feature-desc {
            font-size: 0.95rem;
            color: #64748b;
            line-height: 1.5;
            font-weight: 400;
        }
        
        /* Login Form Styling */
        .stForm {
            border: none !important;
        }
        
        .stTextInput > div > div > input {
            background: #ffffff !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 10px !important;
            padding: 14px 16px !important;
            font-size: 15px !important;
            transition: all 0.2s ease !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #6366f1 !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #9ca3af !important;
        }
        
        .stFormSubmitButton > button {
            background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 14px 24px !important;
            font-size: 15px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3) !important;
        }
        
        .stFormSubmitButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4) !important;
        }
        
        /* Alert styling */
        .stAlert {
            border-radius: 10px !important;
            border: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Center title at the very top
    st.markdown("<div class='main-title'>Prashanti Draft Orders Analytics Dashboard</div>", unsafe_allow_html=True)

    # Layout: left = features, right = login
    left_col, right_col = st.columns([1.3, 1])

    # LEFT COLUMN - Feature Cards
    with left_col:
        features = [
            {"icon": "📊", "title": "Real-time Analytics", "desc": "Get instant insights into your business performance with live data"},
            {"icon": "📋", "title": "Order Management", "desc": "Streamline your draft order processing with smart automation"},
        ]

        st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
        for feature in features:
            st.markdown(
                f"""
                <div class="feature-item">
                    <span class="feature-icon">{feature['icon']}</span>
                    <div class="feature-title">{feature['title']}</div>
                    <div class="feature-desc">{feature['desc']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # RIGHT COLUMN - Login Card
    with right_col:
        st.markdown(
            """
            <div style="
                background: #ffffff;
                border-radius: 16px;
                padding: 2.5rem 2rem;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
                border: 1px solid #f1f5f9;
                position: relative;
                margin-top: 1rem;">
                <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; 
                     background: linear-gradient(90deg, #6366f1, #8b5cf6, #06b6d4); 
                     border-radius: 16px 16px 0 0;"></div>
                <div style="text-align: center; font-size: 1.8rem; font-weight: 600; margin-bottom: 0.5rem; color: #1e293b;">
                    Welcome Back! 👋
                </div>
                <div style="text-align: center; color: #64748b; margin-bottom: 2rem; font-size: 1rem;">
                    Sign in to access your dashboard
                </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("login_form", clear_on_submit=False):
            email = st.text_input(
                "Email",  # not empty
                placeholder="Enter your email address",
                key="email",
                label_visibility="collapsed"
            )
            password = st.text_input(
                "Password",  # not empty
                type="password",
                placeholder="Enter your password",
                key="password",
                label_visibility="collapsed"
            )

            submitted = st.form_submit_button("🚀 Sign In to Dashboard", use_container_width=True, type="primary")

            if submitted:
                if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
                    st.session_state.authenticated = True
                    st.success("✅ Login successful! Welcome to your dashboard!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please check your email and password.")

        st.markdown("</div>", unsafe_allow_html=True)
    
def logout():
    """Logout function"""
    st.session_state.authenticated = False
    st.rerun()

# Get credentials from environment variables
SHOP_NAME = os.getenv('SHOPIFY_SHOP_NAME')
ACCESS_TOKEN = os.getenv('SHOPIFY_ACCESS_TOKEN')

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_draft_orders(shop_name, access_token, start_date, end_date):
    """Fetch draft orders from Shopify"""
    url = f"https://{shop_name}/admin/api/2025-07/graphql.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token
    }

    query = """
    query getDraftOrdersByDate($query: String!, $first: Int!, $after: String) {
      draftOrders(first: $first, after: $after, query: $query) {
        edges {
          node {
            id
            name
            status
            createdAt
            updatedAt
            totalPriceSet {
              shopMoney {
                amount
                currencyCode
              }
            }
            customer {
              email
              firstName
              lastName
            }
            events(first: 10, sortKey: CREATED_AT) {
              edges {
                node {
                  createdAt
                  message
                }
              }
            }
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
    """

    date_query = f"created_at:>={start_date} AND created_at:<={end_date}"
    variables = {
        "query": date_query,
        "first": 250,
        "after": None
    }

    all_records = []
    has_next_page = True

    while has_next_page:
        try:
            response = requests.post(url, headers=headers, json={"query": query, "variables": variables})
            response.raise_for_status()
            data = response.json()

            edges = data.get("data", {}).get("draftOrders", {}).get("edges", [])
            page_info = data.get("data", {}).get("draftOrders", {}).get("pageInfo", {})

            for edge in edges:
                node = edge["node"]
                draft_id = node.get("id", "")
                name = node.get("name", "")
                status = node.get("status", "")
                created_at = node.get("createdAt", "")
                updated_at = node.get("updatedAt", "")
                
                # Extract amount from priceSet
                price_data = node.get('totalPriceSet', {}).get('shopMoney', {})
                amount = float(price_data.get('amount', 0)) if price_data else 0
                currency = price_data.get('currencyCode', 'USD') if price_data else 'USD'
                
                customer = node.get("customer") or {}
                customer_name = f"{customer.get('firstName', '')} {customer.get('lastName', '')}".strip()
                customer_email = customer.get("email", "")

                events = node.get("events", {}).get("edges", [])
                event_messages = [event["node"].get("message", "") for event in events]
                all_event_messages = "\n".join(event_messages)

                draft_created_name = ""
                completion_date = None

                for msg in event_messages:
                    creator_match = re.search(r"^(.*?) created this draft order", msg, re.IGNORECASE)
                    if creator_match:
                        draft_created_name = creator_match.group(1).strip()

                    if "marked as completed" in msg.lower():
                        date_match = re.search(r"\d{4}-\d{2}-\d{2}", msg)
                        if date_match:
                            completion_date = date_match.group()

                all_records.append({
                    "draft_id": draft_id,
                    "name": name,
                    "status": status,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "amount": amount,
                    "currency": currency,
                    "customer_name": customer_name,
                    "customer_email": customer_email,
                    "event_messages": all_event_messages,
                    "creator": draft_created_name,
                    "completion_date": completion_date
                })

            has_next_page = page_info.get("hasNextPage", False)
            if has_next_page:
                variables["after"] = page_info.get("endCursor")
                
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
            break

    # Ensure DataFrame always has expected columns
    expected_columns = [
        "draft_id", "name", "status", "created_at", "updated_at",
        "amount", "currency", "customer_name", "customer_email", 
        "event_messages", "creator", "completion_date"
    ]
    df = pd.DataFrame(all_records, columns=expected_columns)
    return df

def render_metric_card(title, value, icon, card_type="primary", change=None):
    """Render a metric card with professional styling"""
    change_html = ""
    if change:
        change_class = "positive" if change > 0 else "negative"
        change_icon = "📈" if change > 0 else "📉"
        change_html = f'''
            <div class="metric-change {change_class}">
                {change_icon} {abs(change):.1f}%
            </div>
        '''
    
    return f'''
        <div class="metric-card {card_type}">
            <div class="metric-icon">{icon}</div>
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            {change_html}
        </div>
    '''

def main():
    # Check authentication
    if not check_login():
        login_form()
        return
    
    # Check environment variables
    if not SHOP_NAME or not ACCESS_TOKEN:
        st.error("🔐 Please set SHOPIFY_SHOP_NAME and SHOPIFY_ACCESS_TOKEN in your .env file")
        st.stop()
    
    # Sidebar with logout option
    with st.sidebar:
        st.markdown("""
        <style>
        .sidebar-header {
            text-align: center;
            color: black !important;
        }
        .sidebar-header .sidebar-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: black !important;
        }
        .sidebar-header .sidebar-subtitle {
            font-size: 0.9rem;
            color: black !important;
        }
        .sidebar-logo {
            font-size: 1.5rem;
        }
        </style>

        <div class="sidebar-header">
            <div class="sidebar-logo">🛍️</div>
            <div class="sidebar-title">Shopify Dashboard</div>
            <div class="sidebar-subtitle">Advanced Analytics</div>
        </div>
        """, unsafe_allow_html=True)

        
        if st.button("🚪 Logout", use_container_width=True):
            logout()
        
        st.markdown("---")
        
        # Date Range Filter
        st.markdown("### 📅 Date Range")
        
        today = datetime.now()
        default_start = today - timedelta(days=30)
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("From", default_start)
        with col2:
            end_date = st.date_input("To", today)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Status Filters
        st.markdown("### 📊 Status Filters")
        status_filter = st.multiselect(
            "Select statuses:",
            ["OPEN", "INVOICED", "COMPLETED", "PAID"],
            default=["OPEN", "INVOICED", "COMPLETED", "PAID"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Load data with spinner
        if 'df' not in st.session_state or st.session_state.get('last_refresh_date') != (start_date, end_date):
            with st.spinner("🚀 Loading Shopify data..."):
                df = fetch_draft_orders(SHOP_NAME, ACCESS_TOKEN, start_date, end_date)
                st.session_state.df = df
                st.session_state.last_refresh_date = (start_date, end_date)
        else:
            df = st.session_state.df
        
        # Creator Filters
        if not df.empty and 'creator' in df.columns:
            creators = sorted(df['creator'].dropna().unique())
            if creators:
                
                st.markdown("### 👥 Creator Analytics")
                
                selected_creators = st.multiselect(
                    "Select creators:",
                    creators,
                    key="creator_filter",
                    default=[],
                    label_visibility="collapsed"
                )
                
                st.markdown(f"""
                    <div style="color: black; font-size: 0.85rem; margin-top: 8px;">
                        {len(selected_creators)} of {len(creators)} selected
                    </div>
                """, unsafe_allow_html=True)

        
        # Display Options
        st.markdown("### ⚙️ Display Options")
        show_events = st.checkbox("Show event messages", value=False)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: black !important; font-size: 0.8rem;">
            <div>📡 Real-time Shopify API</div>
            <div>Version 2.3.0 Professional</div>
        </div>
    """, unsafe_allow_html=True)




    # Main Dashboard Header
    st.markdown("""
        <div class="dashboard-header">
            <h1 class="dashboard-title">🛍️ Shopify Analytics</h1>
            <div class="feature-badge">
                ⚡ Real-time Data • 📊 Advanced Analytics • 📤 Export Ready
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Refresh Button
    st.markdown('<div class="refresh-button">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Refresh Dashboard", use_container_width=True):
            st.cache_data.clear()
            if 'df' in st.session_state:
                del st.session_state.df
            if 'last_refresh_date' in st.session_state:
                del st.session_state.last_refresh_date
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Check if data exists
    if df.empty:
        st.markdown("""
            <div style="text-align: center; padding: 4rem 2rem;">
                <div style="font-size: 6rem; margin-bottom: 2rem;">📭</div>
                <h2 style="color: var(--text-secondary); margin-bottom: 1rem;">No Draft Orders Found</h2>
                <p style="color: var(--text-secondary); font-size: 1.1rem; line-height: 1.6;">
                    No draft orders were found for the selected date range and filters.<br>
                    Try adjusting your date range or removing some filters to see your data.
                </p>
                <div style="margin-top: 2rem;">
                    <div style="background: var(--gradient-primary); color: white; padding: 1.5rem 2rem; 
                            border-radius: 16px; display: inline-block; max-width: 400px;">
                        💡 <strong>Tip:</strong> Expand your date range or check your Shopify connection settings
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        return

    # Apply filters
    filtered_df = df.copy()
    if status_filter:
        filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]
    if st.session_state.get('creator_filter'):
        filtered_df = filtered_df[filtered_df['creator'].isin(st.session_state.creator_filter)]

    # Calculate metrics (using COMPLETED status instead of converted)
    total_drafts = len(filtered_df)
    completed_orders = len(filtered_df[filtered_df['status'] == 'COMPLETED'])
    completed_percentage = (completed_orders / total_drafts * 100) if total_drafts > 0 else 0
    unique_creators = filtered_df['creator'].nunique() if 'creator' in filtered_df.columns else 0
    invoiced_orders = len(filtered_df[filtered_df['status'] == 'INVOICED'])
    open_orders = len(filtered_df[filtered_df['status'] == 'OPEN'])

    if 'amount' in filtered_df.columns:
        total_amount = filtered_df['amount'].sum()
        avg_order_value = (total_amount / total_drafts) if total_drafts > 0 else 0
        completed_amount = filtered_df[filtered_df['status'] == 'COMPLETED']['amount'].sum()
        main_currency = filtered_df['currency'].mode()[0] if 'currency' in filtered_df.columns and len(filtered_df) > 0 else 'USD'
    else:
        total_amount = 0
        avg_order_value = 0
        completed_amount = 0
        main_currency = 'USD'

    # Performance Metrics Dashboard
    st.markdown("## 📈 Performance Overview")
    
    # Primary metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(render_metric_card(
            "Total Draft Orders",
            f"{total_drafts:,}",
            "📋",
            "primary"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(render_metric_card(
            "Total Revenue",
            f"{main_currency} {total_amount:,.2f}",
            "💰",
            "accent"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(render_metric_card(
            "Average Order Value",
            f"{main_currency} {avg_order_value:,.2f}",
            "📊",
            "secondary"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(render_metric_card(
            "Completed Revenue",
            f"{main_currency} {completed_amount:,.2f}",
            "✅",
            "success"
        ), unsafe_allow_html=True)

    # Secondary metrics row
    st.markdown("<br>", unsafe_allow_html=True)
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.markdown(render_metric_card(
            "Completion Rate",
            f"{completed_percentage:.1f}%",
            "🎯",
            "primary"
        ), unsafe_allow_html=True)
    
    with col6:
        st.markdown(render_metric_card(
            "Open Orders",
            f"{open_orders}",
            "📝",
            "accent"
        ), unsafe_allow_html=True)
    
    with col7:
        st.markdown(render_metric_card(
            "Active Creators",
            f"{unique_creators}",
            "👥",
            "secondary"
        ), unsafe_allow_html=True)
    
    with col8:
        st.markdown(render_metric_card(
            "Completed Orders",
            f"{completed_orders}",
            "✅",
            "success"
        ), unsafe_allow_html=True)

    # Enhanced Tabs
    st.markdown("<br><br>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📊 Analytics Dashboard", "🔍 Data Explorer", "📤 Export Center"])

    with tab1:
        st.markdown("## 🎯 Advanced Analytics")
        
        # Order Status Funnel and Insights
        if total_drafts > 0:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                
                
                fig_funnel = go.Figure(go.Funnel(
                    y=["🎯 Draft Created", "📋 Open Orders", "📄 Invoiced", "✅ Completed"],
                    x=[total_drafts, open_orders, invoiced_orders, completed_orders],
                    textposition="inside",
                    textinfo="value+percent initial",
                    opacity=0.9,
                    marker={
                        "color": ["#667eea", "#f59e0b", "#6366f1", "#10b981"],
                        "line": {"width": 2, "color": "white"}
                    },
                    textfont={"size": 16, "color": "white", "family": "Inter"}
                ))
                
                fig_funnel.update_layout(
                    title={
                        "text": "🚀 Order Status Funnel",
                        "x": 0,
                        "font": {"size": 24, "color": "#1e293b", "family": "Inter"}
                    },
                    margin=dict(l=50, r=50, b=50, t=80),
                    height=450,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)"
                )
                
                st.plotly_chart(fig_funnel, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                    <div class="insights-panel">
                        <h3 class="insights-title">🎯 Key Performance Insights</h3>
                        <div class="insight-item">
                            <div class="insight-metric">{:.1f}%</div>
                            <div class="insight-label">Draft to Completed Rate</div>
                        </div>
                        <div class="insight-item">
                            <div class="insight-metric">{:.1f}%</div>
                            <div class="insight-label">Invoiced to Completed</div>
                        </div>
                        <div class="insight-item">
                            <div class="insight-metric">{} {:.0f}</div>
                            <div class="insight-label">Total Pipeline Value</div>
                        </div>
                        <div class="insight-item">
                            <div class="insight-metric">{} {:.0f}</div>
                            <div class="insight-label">Revenue at Risk</div>
                        </div>
                    </div>
                """.format(
                    completed_percentage,
                    (completed_orders / invoiced_orders * 100) if invoiced_orders > 0 else 0,
                    main_currency, total_amount,
                    main_currency, total_amount - completed_amount
                ), unsafe_allow_html=True)

        # Creator Performance Analytics
        st.markdown("## 👥 Creator Performance Analytics")
        
        if 'creator' in filtered_df.columns and 'amount' in filtered_df.columns and not filtered_df.empty:
            creator_stats = filtered_df.groupby('creator').agg(
                total_orders=('draft_id', 'count'),
                total_revenue=('amount', 'sum'),
                completed_orders=('status', lambda x: (x == 'COMPLETED').sum()),
                open_orders=('status', lambda x: (x == 'OPEN').sum()),
                invoiced_orders=('status', lambda x: (x == 'INVOICED').sum())
            ).reset_index()

            if not creator_stats.empty:
                creator_stats['completion_rate'] = (creator_stats['completed_orders'] / 
                                                  creator_stats['total_orders']) * 100
                creator_stats['avg_order_value'] = creator_stats['total_revenue'] / creator_stats['total_orders']
                creator_stats = creator_stats[creator_stats['total_orders'] > 0]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    
                    fig_creator = px.bar(
                        creator_stats.sort_values('completion_rate', ascending=False).head(10),
                        x='creator',
                        y='completion_rate',
                        title='🏆 Top 10 Creators by Completion Rate',
                        labels={'creator': 'Creator Name', 'completion_rate': 'Completion Rate (%)'},
                        color='completion_rate',
                        color_continuous_scale='viridis',
                        text='completion_rate'
                    )
                    
                    fig_creator.update_traces(
                        texttemplate='%{text:.1f}%', 
                        textposition='outside',
                        textfont={"family": "Inter"}
                    )
                    
                    fig_creator.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        title_x=0.5,
                        height=400,
                        font={"family": "Inter"}
                    )
                    
                    st.plotly_chart(fig_creator, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    
                    fig_revenue = px.bar(
                        creator_stats.sort_values('total_revenue', ascending=False).head(10),
                        x='creator',
                        y='total_revenue',
                        title='💰 Top 10 Creators by Revenue',
                        labels={'creator': 'Creator Name', 'total_revenue': f'Total Revenue ({main_currency})'},
                        color='total_revenue',
                        color_continuous_scale='plasma',
                        text='total_revenue'
                    )
                    
                    fig_revenue.update_traces(
                        texttemplate=f'{main_currency} %{{text:,.0f}}',
                        textposition='inside',
                        textfont={"family": "Inter"}
                    )
                    
                    fig_revenue.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        title_x=0.5,
                        height=400,
                        font={"family": "Inter"}
                    )
                    
                    st.plotly_chart(fig_revenue, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                # Creator Performance Table
                st.markdown("### 📊 Detailed Creator Performance")
                creator_display = creator_stats.copy()
                creator_display['total_revenue'] = creator_display['total_revenue'].apply(lambda x: f"{main_currency} {x:,.2f}")
                creator_display['avg_order_value'] = creator_display['avg_order_value'].apply(lambda x: f"{main_currency} {x:.2f}")
                creator_display['completion_rate'] = creator_display['completion_rate'].apply(lambda x: f"{x:.1f}%")
                
                creator_display.columns = ['👤 Creator', '📋 Total Orders', '✅ Completed', '📈 Completion Rate', 
                                         '📝 Open', '📄 Invoiced', '💰 Total Revenue', '📊 Avg Order Value']
                
                st.dataframe(creator_display.sort_values('📈 Completion Rate', ascending=False), 
                           use_container_width=True, height=400)

    with tab2:
        st.markdown("## 🔍 Detailed Order Analysis")
        
        # Enhanced search and filter controls
        search_col1, search_col2, search_col3 = st.columns([2, 1, 1])
        
        with search_col1:
            search_term = st.text_input("🔎 Search orders by name, customer, or creator", 
                                      placeholder="Type to search...")
        
        with search_col2:
            sort_by = st.selectbox("📊 Sort by", 
                                 ["Created Date", "Amount", "Status", "Creator", "Customer"])
        
        with search_col3:
            sort_order = st.selectbox("🔄 Order", ["Descending", "Ascending"])

        # Prepare display columns
        display_cols = {
            "name": "📋 Order Name",
            "status": "📊 Status", 
            "created_at": "📅 Created Date",
            "customer_name": "👤 Customer",
            "customer_email": "📧 Email",
            "creator": "👥 Creator",
            "completion_date": "✅ Completed Date"
        }

        if 'amount' in filtered_df.columns:
            display_cols["amount"] = f"💰 Amount ({main_currency})"

        if show_events and 'event_messages' in filtered_df.columns:
            display_cols["event_messages"] = "📝 Event Messages"

        # Filter existing columns
        available_cols = [col for col in display_cols.keys() if col in filtered_df.columns]
        display_df = filtered_df[available_cols].copy()

        # Format data for better display
        if 'created_at' in display_df.columns:
            display_df['created_at'] = pd.to_datetime(display_df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
        
        if 'amount' in display_df.columns:
            display_df['amount'] = display_df['amount'].apply(lambda x: f"{main_currency} {x:,.2f}")

        # Rename columns
        display_df = display_df.rename(columns=display_cols)

        # Apply search filter
        if search_term:
            mask = display_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)
            ).any(axis=1)
            display_df = display_df[mask]

        # Apply sorting
        sort_column_map = {
            "Created Date": "📅 Created Date",
            "Amount": f"💰 Amount ({main_currency})" if f"💰 Amount ({main_currency})" in display_df.columns else "📅 Created Date",
            "Status": "📊 Status",
            "Creator": "👥 Creator",
            "Customer": "👤 Customer"
        }
        
        sort_column = sort_column_map.get(sort_by, "📅 Created Date")
        if sort_column in display_df.columns:
            ascending = sort_order == "Ascending"
            display_df = display_df.sort_values(sort_column, ascending=ascending)

        # Display data table
        st.dataframe(display_df, use_container_width=True, height=600)

        # Summary statistics for current view
        st.markdown("### 📊 Current View Summary")
        
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
        
        with summary_col1:
            st.markdown(render_metric_card(
                "Orders Shown",
                f"{len(display_df):,}",
                "📋",
                "primary"
            ), unsafe_allow_html=True)
        
        with summary_col2:
            if f"💰 Amount ({main_currency})" in display_df.columns:
                # Get original indices to calculate sum from unformatted data
                if not display_df.empty:
                    total_shown = filtered_df.loc[display_df.index, 'amount'].sum()
                    formatted_total = f"{main_currency} {total_shown:,.2f}"
                else:
                    formatted_total = f"{main_currency} 0.00"
                
                st.markdown(render_metric_card(
                    "Total Value",
                    formatted_total,
                    "💰",
                    "accent"
                ), unsafe_allow_html=True)
        
        with summary_col3:
            completed_shown = len([idx for idx in display_df.index if filtered_df.loc[idx, 'status'] == 'COMPLETED']) if not display_df.empty else 0
            st.markdown(render_metric_card(
                "Completed",
                f"{completed_shown}",
                "✅",
                "success"
            ), unsafe_allow_html=True)
        
        with summary_col4:
            unique_creators_shown = display_df["👥 Creator"].nunique() if "👥 Creator" in display_df.columns else 0
            st.markdown(render_metric_card(
                "Unique Creators",
                f"{unique_creators_shown}",
                "👥",
                "secondary"
            ), unsafe_allow_html=True)

    with tab3:
        st.markdown("## 📤 Export Your Data")
        
        # Enhanced export section
        st.markdown('''
            <div class="export-section">
                <div class="export-icon">📊</div>
                <h3 class="export-title">Professional Excel Reports</h3>
                <p class="export-description">
                    Generate comprehensive Excel reports with detailed order data and advanced creator analytics. 
                    Perfect for business intelligence, performance reviews, and strategic planning.
                </p>
            </div>
        ''', unsafe_allow_html=True)

        # Export features overview
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                #### 📋 Sheet 1: Complete Order Data
                - **Order Details:** Names, IDs, status, dates
                - **Customer Information:** Names, email addresses
                - **Financial Data:** Amounts, currency, totals
                - **Status Tracking:** Completion dates and flags
                - **Event History:** Detailed activity logs (optional)
            """)
        
        with col2:
            st.markdown("""
                #### 👥 Sheet 2: Creator Performance Analytics
                - **Performance Metrics:** Orders created, completion rates
                - **Revenue Analysis:** Total and average order values
                - **Success Tracking:** Completion rates and statistics
                - **Time Analysis:** First and last order dates
                - **Status Breakdown:** Open, invoiced, completed counts
            """)

        # Create and display creator summary
        if 'creator' in filtered_df.columns and not filtered_df.empty:
            creator_summary = filtered_df.groupby('creator').agg({
                'draft_id': 'count',
                'amount': ['sum', 'mean'],
                'status': [
                    lambda x: (x == 'COMPLETED').sum(),
                    lambda x: (x == 'OPEN').sum(),
                    lambda x: (x == 'INVOICED').sum()
                ],
                'created_at': ['min', 'max']
            }).round(2)

            # Flatten column names
            creator_summary.columns = [
                'Total_Drafts_Created',
                'Total_Revenue',
                'Average_Order_Value',
                'Total_Completed',
                'Total_Open',
                'Total_Invoiced',
                'First_Order_Date',
                'Last_Order_Date'
            ]

            # Calculate rates
            creator_summary['Completion_Rate'] = (
                creator_summary['Total_Completed'] / creator_summary['Total_Drafts_Created'] * 100
            ).round(2)

            creator_summary = creator_summary.reset_index()
            
            # Reorder columns
            creator_summary = creator_summary[[
                'creator', 'Total_Drafts_Created', 'Total_Completed', 'Completion_Rate',
                'Total_Open', 'Total_Invoiced', 'Total_Revenue', 'Average_Order_Value',
                'First_Order_Date', 'Last_Order_Date'
            ]]

            # Preview section
            st.markdown("### 👀 Creator Analytics Preview")
            preview_df = creator_summary.head(5).copy()
            
            # Format for display
            preview_df['Total_Revenue'] = preview_df['Total_Revenue'].apply(lambda x: f"{main_currency} {x:,.2f}")
            preview_df['Average_Order_Value'] = preview_df['Average_Order_Value'].apply(lambda x: f"{main_currency} {x:.2f}")
            preview_df['Completion_Rate'] = preview_df['Completion_Rate'].apply(lambda x: f"{x:.1f}%")
            
            st.dataframe(preview_df, use_container_width=True)

        # Export button and functionality
        st.markdown("<br>", unsafe_allow_html=True)
        
        export_col1, export_col2, export_col3 = st.columns([1, 2, 1])
        with export_col2:
            if st.button("📥 Generate & Download Excel Report", 
                        use_container_width=True, type="primary"):
                
                # Create Excel file with multiple sheets
                buffer = io.BytesIO()
                
                with st.spinner("📊 Generating your professional Excel report..."):
                    try:
                        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                            # Prepare main data sheet
                            export_df = filtered_df.copy()
                            
                            # Clean column names for export
                            export_columns = {
                                'draft_id': 'Draft_ID',
                                'name': 'Order_Name', 
                                'status': 'Status',
                                'created_at': 'Created_Date',
                                'updated_at': 'Updated_Date',
                                'amount': 'Amount',
                                'currency': 'Currency',
                                'customer_name': 'Customer_Name',
                                'customer_email': 'Customer_Email',
                                'creator': 'Creator',
                                'completion_date': 'Completion_Date'
                            }

                            if show_events:
                                export_columns['event_messages'] = 'Event_Messages'

                            # Select and rename columns
                            available_export_cols = [col for col in export_columns.keys() if col in export_df.columns]
                            export_df = export_df[available_export_cols].rename(columns=export_columns)

                            # Write main data sheet
                            export_df.to_excel(writer, sheet_name='Draft_Orders', index=False)

                            # Write creator summary sheet
                            if 'creator' in filtered_df.columns and not filtered_df.empty:
                                creator_summary.to_excel(writer, sheet_name='Creator_Analytics', index=False)

                            # Enhanced formatting
                            workbook = writer.book
                            
                            # Header format
                            header_format = workbook.add_format({
                                'bold': True,
                                'text_wrap': True,
                                'valign': 'top',
                                'fg_color': '#667eea',
                                'font_color': 'white',
                                'border': 1,
                                'font_name': 'Inter'
                            })
                            
                            # Data format
                            data_format = workbook.add_format({
                                'font_name': 'Inter',
                                'font_size': 10
                            })
                            
                            # Currency format
                            currency_format = workbook.add_format({
                                'num_format': f'"{main_currency}" #,##0.00',
                                'font_name': 'Inter'
                            })

                            # Format main sheet
                            worksheet1 = writer.sheets['Draft_Orders']
                            
                            # Apply header formatting
                            for col_num, value in enumerate(export_df.columns.values):
                                worksheet1.write(0, col_num, value, header_format)
                            
                            # Auto-adjust column widths
                            for i, col in enumerate(export_df.columns):
                                if export_df.dtypes.iloc[i] == 'object':
                                    max_length = max(
                                        export_df.iloc[:, i].astype(str).map(len).max() if len(export_df) > 0 else 0,
                                        len(str(col))
                                    )
                                    worksheet1.set_column(i, i, min(max_length + 2, 50))
                                else:
                                    worksheet1.set_column(i, i, 15)

                            # Format creator analytics sheet
                            if 'creator' in filtered_df.columns and not filtered_df.empty:
                                worksheet2 = writer.sheets['Creator_Analytics']
                                
                                # Apply header formatting
                                for col_num, value in enumerate(creator_summary.columns.values):
                                    worksheet2.write(0, col_num, value, header_format)
                                
                                # Auto-adjust column widths
                                for i, col in enumerate(creator_summary.columns):
                                    col_width = max(len(str(col)), 15)
                                    worksheet2.set_column(i, i, col_width)

                        # Provide download
                        filename = f"shopify_analytics_report_{start_date}_{end_date}.xlsx"
                        
                        st.download_button(
                            label="📊 Download Excel Report",
                            data=buffer.getvalue(),
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                        
                        st.success("✅ Excel report generated successfully! Click the button above to download.")
                        
                    except Exception as e:
                        st.error(f"❌ Error generating report: {str(e)}")

        # Export summary information
        st.markdown("---")
        st.markdown("### 📋 Export Summary")
        
        summary_col1, summary_col2, summary_col3 = st.columns(3)
        
        with summary_col1:
            st.markdown(f"""
                **📊 Data Range**
                - **From:** {start_date.strftime('%B %d, %Y')}
                - **To:** {end_date.strftime('%B %d, %Y')} 
                - **Total Records:** {len(filtered_df):,}
                - **Filters Applied:** {len([f for f in [status_filter, st.session_state.get('creator_filter')] if f]) if any([status_filter, st.session_state.get('creator_filter')]) else 'None'}
            """)
        
        with summary_col2:
            st.markdown(f"""
                **👥 Creator Analytics**
                - **Active Creators:** {unique_creators}
                - **Completion Tracking:** ✅ Enabled
                - **Performance Metrics:** ✅ Included
                - **Status Breakdown:** ✅ Included
            """)
        
        with summary_col3:
            st.markdown(f"""
                **💰 Financial Overview** 
                - **Total Pipeline:** {main_currency} {total_amount:,.2f}
                - **Completed Value:** {main_currency} {completed_amount:,.2f}
                - **Currency:** {main_currency}
                - **Avg Order Value:** {main_currency} {avg_order_value:.2f}
            """)

if __name__ == "__main__":
    main()
