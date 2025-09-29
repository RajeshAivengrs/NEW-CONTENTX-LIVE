"""
Content X AI Studio - Simplified Version for Local Testing
Complete enterprise-grade AI content generation platform
"""

import asyncio
import json
import logging
import hashlib
import random
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form, Header
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import content backend (with error handling for missing dependencies)
try:
    from real_content_backend import real_content_backend
    CONTENT_BACKEND_AVAILABLE = True
    logger.info("Real content backend loaded with full video generation capabilities!")
except ImportError as e:
    logger.warning(f"Real content backend not available: {e}")
    CONTENT_BACKEND_AVAILABLE = False
    real_content_backend = None

# Import publishing backend
try:
    from publishing_backend import publishing_backend
    PUBLISHING_BACKEND_AVAILABLE = True
    logger.info("Publishing backend loaded with social media automation!")
except ImportError as e:
    logger.warning(f"Publishing backend not available: {e}")
    PUBLISHING_BACKEND_AVAILABLE = False
    publishing_backend = None

# Import payment backend
try:
    from razorpay_backend import razorpay_backend
    PAYMENT_BACKEND_AVAILABLE = True
    logger.info("Razorpay payment backend loaded for Indian market!")
except ImportError as e:
    logger.warning(f"Razorpay payment backend not available: {e}")
    PAYMENT_BACKEND_AVAILABLE = False
    razorpay_backend = None

# Import auth backend
try:
    from auth_backend import auth_backend
    AUTH_BACKEND_AVAILABLE = True
    logger.info("Auth backend loaded with OAuth integration!")
except ImportError as e:
    logger.warning(f"Auth backend not available: {e}")
    AUTH_BACKEND_AVAILABLE = False
    auth_backend = None

# Import voice backend
try:
    from voice_backend import voice_backend
    VOICE_BACKEND_AVAILABLE = True
    logger.info("Voice backend loaded with Speechelo integration!")
except ImportError as e:
    logger.warning(f"Voice backend not available: {e}")
    VOICE_BACKEND_AVAILABLE = False
    voice_backend = None

# Import database backend
try:
    from simple_database_backend import simple_database_backend
    DATABASE_BACKEND_AVAILABLE = True
    logger.info("Database backend loaded with PostgreSQL integration!")
except ImportError as e:
    logger.warning(f"Database backend not available: {e}")
    DATABASE_BACKEND_AVAILABLE = False
    simple_database_backend = None

# Initialize FastAPI app
app = FastAPI(
    title="Content X AI Studio",
    description="Enterprise-Grade AI Content Generation Platform",
    version="3.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global data storage
analytics_data = {
    "total_users": 1247,
    "total_scripts": 8932,
    "total_requests": 45678,
    "uptime_start": datetime.now(timezone.utc)
}

@app.get("/")
async def content_x_homepage():
    """Content X AI Studio Professional Homepage"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Content X - AI Studio | Enterprise Content Generation Platform</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
            
            :root {
                /* Aqua Global Color Palette */
                --aqua-primary: #00D4FF;
                --aqua-secondary: #0099CC;
                --aqua-accent: #33E6FF;
                --aqua-deep: #006699;
                --aqua-light: #B3F0FF;
                --aqua-dark: #004466;
                
                /* Global Neutrals */
                --white: #FFFFFF;
                --black: #0A0A0A;
                --gray-50: #FAFAFA;
                --gray-100: #F5F5F5;
                --gray-200: #E5E5E5;
                --gray-300: #D4D4D4;
                --gray-400: #A3A3A3;
                --gray-500: #737373;
                --gray-600: #525252;
                --gray-700: #404040;
                --gray-800: #262626;
                --gray-900: #171717;
                
                /* Premium Gradients */
                --gradient-aqua: linear-gradient(135deg, var(--aqua-primary) 0%, var(--aqua-secondary) 50%, var(--aqua-deep) 100%);
                --gradient-ocean: linear-gradient(135deg, #0066CC 0%, #0099FF 25%, #00CCFF 50%, #33E6FF 75%, #66F0FF 100%);
                --gradient-deep: linear-gradient(135deg, var(--aqua-dark) 0%, var(--aqua-deep) 50%, var(--aqua-secondary) 100%);
                --gradient-glass: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
                
                /* Shadows */
                --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
                --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
                --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
                --shadow-aqua: 0 10px 25px rgba(0, 212, 255, 0.3);
                --shadow-glow: 0 0 30px rgba(0, 212, 255, 0.5);
                
                /* Spacing Scale */
                --space-1: 0.25rem;
                --space-2: 0.5rem;
                --space-3: 0.75rem;
                --space-4: 1rem;
                --space-5: 1.25rem;
                --space-6: 1.5rem;
                --space-8: 2rem;
                --space-10: 2.5rem;
                --space-12: 3rem;
                --space-16: 4rem;
                --space-20: 5rem;
                --space-24: 6rem;
                
                /* Border Radius */
                --radius-sm: 0.375rem;
                --radius-md: 0.5rem;
                --radius-lg: 0.75rem;
                --radius-xl: 1rem;
                --radius-2xl: 1.5rem;
                --radius-full: 9999px;
            }

            * { 
                margin: 0; 
                padding: 0; 
                box-sizing: border-box; 
            }
            
            body { 
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.6;
                color: var(--white);
                background: var(--gradient-ocean);
                overflow-x: hidden;
                position: relative;
                min-height: 100vh;
            }

            body::before {
                content: '';
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: 
                    radial-gradient(circle at 20% 80%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(51, 230, 255, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 40% 40%, rgba(0, 153, 204, 0.1) 0%, transparent 50%);
                pointer-events: none;
                z-index: -1;
            }
            
            /* Header */
            .header {
                background: rgba(0, 68, 102, 0.95);
                backdrop-filter: blur(20px);
                border-bottom: 1px solid rgba(0, 212, 255, 0.2);
                color: var(--white);
                padding: var(--space-6) 0;
                position: fixed;
                width: 100%;
                top: 0;
                z-index: 1000;
                box-shadow: var(--shadow-xl);
            }
            
            .nav-container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 2rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .logo {
                font-size: 2.5rem;
                font-weight: 800;
                background: var(--gradient-aqua);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                letter-spacing: -0.02em;
                font-family: 'Space Grotesk', sans-serif;
                text-shadow: 0 0 30px rgba(0, 212, 255, 0.4);
                animation: aquaGlow 2s ease-in-out infinite alternate;
            }
            
            @keyframes aquaGlow {
                0% { filter: brightness(1) drop-shadow(0 0 10px rgba(0, 212, 255, 0.3)); }
                100% { filter: brightness(1.2) drop-shadow(0 0 20px rgba(0, 212, 255, 0.6)); }
            }
            
            @keyframes gradientShift {
                0%, 100% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
            }
            
            @keyframes aquaGlow {
                0% { filter: brightness(1) drop-shadow(0 0 20px rgba(0, 212, 255, 0.3)); }
                100% { filter: brightness(1.1) drop-shadow(0 0 30px rgba(0, 212, 255, 0.6)); }
            }
            
            .nav-links {
                display: flex;
                gap: 2rem;
                list-style: none;
            }
            
            .nav-links a {
                color: white;
                text-decoration: none;
                font-weight: 500;
                transition: opacity 0.3s;
            }
            
            .nav-links a:hover { opacity: 0.8; }
            
            .cta-buttons {
                display: flex;
                gap: 1rem;
            }
            
            .btn {
                padding: 0.75rem 1.5rem;
                border: none;
                border-radius: 50px;
                font-weight: 600;
                text-decoration: none;
                cursor: pointer;
                transition: all 0.3s ease;
                display: inline-block;
            }
            
            .btn-primary {
                background: #fff;
                color: #667eea;
            }
            
            .btn-secondary {
                background: transparent;
                color: white;
                border: 2px solid white;
            }
            
            .btn:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
            
            /* Hero Section */
            .hero {
                background: var(--gradient-deep);
                color: var(--white);
                padding: 12rem var(--space-8) 8rem;
                text-align: center;
                margin-top: 100px;
                position: relative;
                overflow: hidden;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .hero::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: 
                    radial-gradient(circle at 20% 80%, rgba(0, 212, 255, 0.15) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(51, 230, 255, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 40% 40%, rgba(0, 153, 204, 0.2) 0%, transparent 50%);
                pointer-events: none;
                animation: aquaFloat 6s ease-in-out infinite;
            }
            
            @keyframes aquaFloat {
                0%, 100% { transform: translateY(0px) rotate(0deg); }
                50% { transform: translateY(-20px) rotate(1deg); }
            }
            
            .hero-container {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .hero h1 {
                font-size: 5.5rem;
                font-weight: 900;
                margin-bottom: var(--space-8);
                background: var(--gradient-aqua);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                letter-spacing: -0.03em;
                line-height: 1.1;
                position: relative;
                z-index: 2;
                font-family: 'Space Grotesk', sans-serif;
                text-shadow: 0 0 40px rgba(0, 212, 255, 0.5);
                animation: heroGlow 3s ease-in-out infinite alternate;
            }
            
            @keyframes heroGlow {
                0% { 
                    filter: brightness(1) drop-shadow(0 0 20px rgba(0, 212, 255, 0.3));
                    transform: scale(1);
                }
                100% { 
                    filter: brightness(1.1) drop-shadow(0 0 30px rgba(0, 212, 255, 0.6));
                    transform: scale(1.02);
                }
            }
            
            .hero p {
                font-size: 1.5rem;
                font-weight: 300;
                margin-bottom: 3.5rem;
                opacity: 0.85;
                max-width: 700px;
                margin-left: auto;
                margin-right: auto;
                line-height: 1.7;
                position: relative;
                z-index: 2;
            }
            
            .hero-cta {
                display: flex;
                gap: 1.5rem;
                justify-content: center;
                flex-wrap: wrap;
            }
            
            .btn-hero {
                padding: var(--space-6) var(--space-12);
                font-size: 1.2rem;
                border-radius: var(--radius-full);
                font-weight: 700;
                text-decoration: none;
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                display: inline-block;
                position: relative;
                background: var(--gradient-aqua);
                color: var(--white);
                box-shadow: var(--shadow-aqua);
                border: 2px solid transparent;
                overflow: hidden;
                letter-spacing: 0.5px;
                text-transform: uppercase;
            }
            
            .btn-hero::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
                transition: left 0.6s;
            }
            
            .btn-hero-primary {
                background: var(--gradient-aqua);
                background-size: 200% 200%;
                color: var(--white);
                border: none;
                box-shadow: var(--shadow-aqua);
                animation: aquaShimmer 3s ease infinite;
            }
            
            .btn-hero-secondary {
                background: transparent;
                color: var(--aqua-primary);
                border: 2px solid var(--aqua-primary);
                backdrop-filter: blur(10px);
                box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
            }
            
            .btn-hero:hover {
                transform: translateY(-4px) scale(1.05);
                box-shadow: var(--shadow-glow);
                border-color: var(--aqua-accent);
            }
            
            .btn-hero:hover::before {
                left: 100%;
            }
            
            .btn-hero-primary:hover {
                box-shadow: 0 0 40px rgba(0, 212, 255, 0.8);
            }
            
            @keyframes aquaShimmer {
                0%, 100% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
            }
            
            /* Features Section */
            .features {
                padding: var(--space-20) var(--space-8);
                background: var(--gradient-glass);
                backdrop-filter: blur(20px);
                position: relative;
                border-top: 1px solid rgba(0, 212, 255, 0.1);
            }
            
            .features::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: 
                    radial-gradient(circle at 30% 20%, rgba(120, 119, 198, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 70% 80%, rgba(255, 119, 198, 0.05) 0%, transparent 50%);
                pointer-events: none;
            }
            
            .features-container {
                max-width: 1200px;
                margin: 0 auto;
                text-align: center;
            }
            
            .features h2 {
                font-size: 4rem;
                font-weight: 900;
                margin-bottom: 1.5rem;
                background: linear-gradient(135deg, #ffffff, #f8f9fa, #e9ecef);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: -0.02em;
                position: relative;
                z-index: 2;
            }
            
            .features-subtitle {
                font-size: 1.4rem;
                font-weight: 300;
                color: rgba(255, 255, 255, 0.8);
                margin-bottom: 5rem;
                max-width: 700px;
                margin-left: auto;
                margin-right: auto;
                line-height: 1.7;
                position: relative;
                z-index: 2;
            }
            
            .features-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 3rem;
                margin-bottom: 4rem;
            }
            
            .feature-card {
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 3rem;
                border-radius: 24px;
                text-align: center;
                box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                position: relative;
                overflow: hidden;
            }
            
            .feature-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .feature-card:hover {
                transform: translateY(-15px) scale(1.02);
                box-shadow: 0 30px 60px rgba(0,0,0,0.4);
                border-color: rgba(255, 255, 255, 0.2);
            }
            
            .feature-card:hover::before {
                opacity: 1;
            }
            
            .feature-icon {
                font-size: 4rem;
                margin-bottom: 2rem;
                position: relative;
                z-index: 2;
            }
            
            .feature-card h3 {
                font-size: 1.8rem;
                font-weight: 700;
                margin-bottom: 1.5rem;
                color: white;
                position: relative;
                z-index: 2;
            }
            
            .feature-card p {
                color: rgba(255, 255, 255, 0.8);
                line-height: 1.7;
                font-size: 1.1rem;
                position: relative;
                z-index: 2;
            }
            
            /* Stats Section */
            .stats {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 4rem 2rem;
                text-align: center;
            }
            
            .stats-container {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 3rem;
            }
            
            .stat-item {
                text-align: center;
            }
            
            .stat-number {
                font-size: 3rem;
                font-weight: bold;
                margin-bottom: 0.5rem;
            }
            
            .stat-label {
                font-size: 1.1rem;
                opacity: 0.9;
            }
            
            /* CTA Section */
            .cta-section {
                background: white;
                padding: 6rem 2rem;
                text-align: center;
            }
            
            .cta-container {
                max-width: 800px;
                margin: 0 auto;
            }
            
            .cta-section h2 {
                font-size: 2.5rem;
                margin-bottom: 1.5rem;
                color: white;
            }
            
            .cta-section p {
                font-size: 1.2rem;
                color: rgba(255, 255, 255, 0.8);
                margin-bottom: 3rem;
            }
            
            /* Footer */
            .footer {
                background: #2d3748;
                color: white;
                padding: 3rem 2rem 2rem;
                text-align: center;
            }
            
            .footer-container {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            @media (max-width: 768px) {
                .hero h1 { font-size: 2.5rem; }
                .hero p { font-size: 1.1rem; }
                .hero-cta { flex-direction: column; align-items: center; }
                .nav-links { display: none; }
                .features-grid { grid-template-columns: 1fr; }
                .stats-grid { grid-template-columns: repeat(2, 1fr); }
            }
        </style>
    </head>
    <body>
        <!-- Header -->
        <header class="header">
            <div class="nav-container">
                <div class="logo">Content X</div>
                <nav class="nav-links">
                    <a href="#features">Features</a>
                    <a href="/pricing">Pricing</a>
                    <a href="#about">About</a>
                    <a href="#contact">Contact</a>
                </nav>
                <div class="cta-buttons">
                    <a href="#" class="btn btn-secondary">Sign In</a>
                    <a href="/auth/google" class="btn btn-primary">Get Started Free</a>
                </div>
            </div>
        </header>

        <!-- Hero Section -->
        <section class="hero">
            <div class="hero-container">
                <h1>Craft Extraordinary Content<br>with AI Precision</h1>
                <p>Experience the future of content creation. Our enterprise-grade AI platform transforms your creative vision into compelling narratives that captivate audiences and drive unprecedented engagement.</p>
                <div class="hero-cta">
                    <a href="/auth/google" class="btn-hero btn-hero-primary">🚀 Start Your Free Trial</a>
                    <a href="/demo" class="btn-hero btn-hero-secondary">📺 Watch Demo</a>
                </div>
            </div>
        </section>

        <!-- Features Section -->
        <section class="features" id="features">
            <div class="features-container">
                <h2>Everything You Need to Scale Content Creation</h2>
                <p class="features-subtitle">From AI script generation to advanced analytics, Content X AI Studio provides enterprise-grade tools for modern content teams.</p>
                
                <div class="features-grid">
                    <div class="feature-card">
                        <div class="feature-icon">🤖</div>
                        <h3>AI Script Generation</h3>
                        <p>Generate professional scripts in seconds with our advanced AI. Multiple styles, tones, and formats for any use case.</p>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon">🎥</div>
                        <h3>Video Content Creation</h3>
                        <p>Transform scripts into high-quality videos with voice cloning, automated editing, and professional templates.</p>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon">📊</div>
                        <h3>Advanced Analytics</h3>
                        <p>Track performance, optimize content strategy, and measure ROI with comprehensive analytics and reporting.</p>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon">🎯</div>
                        <h3>ICP Targeting</h3>
                        <p>Build detailed Ideal Customer Profiles and create personalized content that resonates with your audience.</p>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon">🔗</div>
                        <h3>Enterprise Integrations</h3>
                        <p>Seamlessly integrate with your existing workflow tools, CRM systems, and marketing platforms.</p>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon">👥</div>
                        <h3>Team Collaboration</h3>
                        <p>Work together with advanced team features, approval workflows, and brand consistency tools.</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Stats Section -->
        <section class="stats">
            <div class="stats-container">
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-number">10,000+</div>
                        <div class="stat-label">Enterprise Customers</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">50M+</div>
                        <div class="stat-label">Content Pieces Created</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">98%</div>
                        <div class="stat-label">Customer Satisfaction</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">85%</div>
                        <div class="stat-label">Time Savings</div>
                    </div>
                </div>
            </div>
        </section>

        <!-- CTA Section -->
        <section class="cta-section">
            <div class="cta-container">
                <h2>Ready to Transform Your Content Strategy?</h2>
                <p>Join thousands of enterprise teams already using Content X AI Studio to create better content faster.</p>
                <a href="/auth/google" class="btn-hero btn-hero-primary">🚀 Start Your Free Trial</a>
            </div>
        </section>

        <!-- Footer -->
        <footer class="footer">
            <div class="footer-container">
                <div class="logo">Content X</div>
                <p style="margin-top: 1rem; opacity: 0.8;">© 2025 Content X AI Studio. All rights reserved.</p>
            </div>
        </footer>

        <script>
            // Smooth scrolling for navigation links
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function (e) {
                    e.preventDefault();
                    document.querySelector(this.getAttribute('href')).scrollIntoView({
                        behavior: 'smooth'
                    });
                });
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Auth page redirects to frontend
@app.get("/auth/google")
async def auth_page_redirect():
    """Redirect to frontend auth page"""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Redirecting to Content X Auth...</title>
        <script>
            window.location.href = 'http://localhost:3000/auth/google';
        </script>
    </head>
    <body>
        <p>Redirecting to authentication page...</p>
    </body>
    </html>
    """)

@app.get("/features")
async def features():
    """Interactive Feature Discovery Page"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Discover Features - Content X AI Studio</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: var(--gradient-ocean);
                color: var(--white);
                min-height: 100vh;
                position: relative;
                overflow-x: hidden;
            }
            
            body::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: 
                    radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.15) 0%, transparent 50%),
                    radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.1) 0%, transparent 50%);
                pointer-events: none;
            }
            
            .header {
                background: rgba(0, 68, 102, 0.95);
                backdrop-filter: blur(20px);
                border-bottom: 1px solid rgba(0, 212, 255, 0.2);
                color: var(--white);
                padding: var(--space-16) 0;
                text-align: center;
                position: relative;
                z-index: 10;
                box-shadow: var(--shadow-xl);
            }
            
            .header h1 {
                font-size: 4rem;
                font-weight: 900;
                margin-bottom: var(--space-6);
                background: var(--gradient-aqua);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                letter-spacing: -0.02em;
                font-family: 'Space Grotesk', sans-serif;
                text-shadow: 0 0 40px rgba(0, 212, 255, 0.5);
                animation: aquaGlow 3s ease-in-out infinite alternate;
            }
            
            .header p {
                font-size: 1.4rem;
                font-weight: 300;
                opacity: 0.85;
                max-width: 600px;
                margin: 0 auto;
                line-height: 1.7;
            }
            
            .container {
                max-width: 1200px;
                margin: 4rem auto;
                padding: 0 2rem;
                position: relative;
                z-index: 2;
            }
            
            .feature-categories {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 2.5rem;
                margin-bottom: 4rem;
            }
            
            .category-card {
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 24px;
                padding: 2.5rem;
                box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                cursor: pointer;
                position: relative;
                overflow: hidden;
            }
            
            
            .category-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .category-card:hover {
                transform: translateY(-10px) scale(1.02);
                box-shadow: 0 30px 60px rgba(0,0,0,0.4);
                border-color: rgba(255, 255, 255, 0.2);
            }
            
            .category-card:hover::before {
                opacity: 1;
            }
            
            .category-card.selected {
                border-color: #4ecdc4;
                background: rgba(78, 205, 196, 0.1);
            }
            
            .category-icon {
                font-size: 3rem;
                margin-bottom: 1rem;
            }
            
            .category-card h3 {
                font-size: 1.5rem;
                color: white;
                margin-bottom: 1rem;
            }
            
            .category-card p {
                color: rgba(255, 255, 255, 0.8);
                margin-bottom: 1.5rem;
                line-height: 1.6;
            }
            
            .feature-list {
                list-style: none;
                padding: 0;
            }
            
            .feature-list li {
                padding: 0.5rem 0;
                color: rgba(255, 255, 255, 0.9);
                position: relative;
                padding-left: 1.5rem;
            }
            
            .feature-list li:before {
                content: '✓';
                position: absolute;
                left: 0;
                color: #48bb78;
                font-weight: bold;
            }
            
            .cta-section {
                text-align: center;
                background: white;
                border-radius: 15px;
                padding: 3rem;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                margin-top: 3rem;
            }
            
            .cta-section h2 {
                color: white;
                margin-bottom: 1rem;
                font-size: 2rem;
            }
            
            .cta-section p {
                color: rgba(255, 255, 255, 0.8);
                margin-bottom: 2rem;
                font-size: 1.1rem;
            }
            
            .btn {
                display: inline-block;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 1rem 2rem;
                text-decoration: none;
                border-radius: 50px;
                font-weight: 600;
                transition: transform 0.2s;
                margin: 0.5rem;
            }
            
            .btn:hover { transform: translateY(-2px); }
            
            @media (max-width: 768px) {
                .feature-categories { grid-template-columns: 1fr; }
                .header h1 { font-size: 2rem; }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🚀 Discover Content X Features</h1>
            <p>Explore our comprehensive suite of AI-powered content creation tools</p>
        </div>
        
        <div class="container">
            <div class="feature-categories">
                <!-- Scripting Category -->
                <div class="category-card" onclick="selectCategory('scripting')">
                    <div class="category-icon">📝</div>
                    <h3>AI Scripting</h3>
                    <p>Generate professional scripts for any purpose with our advanced AI engine.</p>
                    <ul class="feature-list">
                        <li>Multiple writing styles</li>
                        <li>Industry-specific templates</li>
                        <li>Real-time collaboration</li>
                        <li>Brand voice consistency</li>
                        <li>SEO optimization</li>
                    </ul>
                </div>
                
                <!-- Content Category -->
                <div class="category-card" onclick="selectCategory('content')">
                    <div class="category-icon">🎥</div>
                    <h3>Video Content</h3>
                    <p>Transform scripts into high-quality videos with voice cloning and editing.</p>
                    <ul class="feature-list">
                        <li>✓ AI voice generation</li>
                        <li>✓ Automated video editing</li>
                        <li>✓ Custom avatars</li>
                        <li>✓ Multiple export formats</li>
                        <li>✓ Batch processing</li>
                    </ul>
                </div>
                
                <!-- Analytics Category -->
                <div class="category-card" onclick="selectCategory('analytics')">
                    <div class="category-icon">📊</div>
                    <h3>Advanced Analytics</h3>
                    <p>Track performance, measure ROI, and optimize your content strategy.</p>
                    <ul class="feature-list">
                        <li>✓ Performance tracking</li>
                        <li>✓ A/B testing</li>
                        <li>✓ Competitor analysis</li>
                        <li>✓ Custom reports</li>
                        <li>✓ Predictive insights</li>
                    </ul>
                </div>
                
                <!-- Enterprise Category -->
                <div class="category-card" onclick="selectCategory('enterprise')">
                    <div class="category-icon">🏢</div>
                    <h3>Enterprise Solutions</h3>
                    <p>Scale your content operations with enterprise-grade tools and support.</p>
                    <ul class="feature-list">
                        <li>✓ Team collaboration</li>
                        <li>✓ Advanced security</li>
                        <li>✓ Custom integrations</li>
                        <li>✓ Dedicated support</li>
                        <li>✓ White-label options</li>
                    </ul>
                </div>
            </div>
            
            <div class="cta-section">
                <h2>Ready to Choose Your Plan?</h2>
                <p>Select the perfect subscription tier for your content creation needs</p>
                <a href="/pricing" class="btn">🎯 View Pricing Plans</a>
                <a href="/publishing" class="btn">📤 Publishing Dashboard</a>
                <a href="/" class="btn">🏠 Back to Home</a>
            </div>
        </div>
        
        <script>
            let selectedCategories = [];
            
            function selectCategory(category) {
                const card = event.currentTarget;
                
                const isSelected = card.classList.contains('selected');
                
                if (isSelected) {
                    card.classList.remove('selected');
                    selectedCategories = selectedCategories.filter(c => c !== category);
                } else {
                    card.classList.add('selected');
                    selectedCategories.push(category);
                }
                
                // Store selected categories
                localStorage.setItem('selected_categories', JSON.stringify(selectedCategories));
            }
            
            // Load previously selected categories
            const saved = localStorage.getItem('selected_categories');
            if (saved) {
                selectedCategories = JSON.parse(saved);
                selectedCategories.forEach(category => {
                    document.querySelector(`[onclick="selectCategory('${category}')"]`).classList.add('selected');
                });
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/pricing")
async def pricing():
    """Plan Selection - Choose Your Content Creation Path"""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Choose Your Plan - Content X AI Studio</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: var(--gradient-ocean);
                color: var(--white);
                min-height: 100vh;
                position: relative;
                overflow-x: hidden;
            }
            
            body::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: 
                    radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.15) 0%, transparent 50%),
                    radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.1) 0%, transparent 50%);
                pointer-events: none;
            }
            .header {
                background: rgba(0, 68, 102, 0.95);
                backdrop-filter: blur(20px);
                border-bottom: 1px solid rgba(0, 212, 255, 0.2);
                color: var(--white);
                padding: var(--space-16) 0;
                text-align: center;
                position: relative;
                z-index: 10;
                box-shadow: var(--shadow-xl);
            }
            .header h1 { 
                font-size: 4rem; 
                font-weight: 900;
                margin-bottom: 1.5rem;
                background: linear-gradient(135deg, #ffffff, #f8f9fa, #e9ecef);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: -0.02em;
            }
            .header p { 
                font-size: 1.4rem; 
                font-weight: 300;
                opacity: 0.85; 
                max-width: 700px; 
                margin: 0 auto;
                line-height: 1.7;
            }
            .container { max-width: 1200px; margin: 0 auto; padding: 3rem 2rem; }
            .plans-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-bottom: 3rem; }
            .plan-card { 
                background: var(--gradient-glass);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(0, 212, 255, 0.2);
                border-radius: var(--radius-2xl); 
                padding: var(--space-10); 
                box-shadow: var(--shadow-xl); 
                position: relative; 
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
                text-align: center;
                overflow: hidden;
            }
            .plan-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .plan-card:hover { 
                transform: translateY(-10px) scale(1.02);
                box-shadow: var(--shadow-glow);
                border-color: var(--aqua-primary);
            }
            
            .plan-card:hover::before {
                opacity: 1;
            }
            
            .plan-card.popular { 
                border-color: var(--aqua-primary); 
                transform: scale(1.05);
                background: rgba(0, 212, 255, 0.1);
                box-shadow: var(--shadow-aqua);
            }
            .free-badge { position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: var(--aqua-primary); color: var(--white); padding: var(--space-2) var(--space-6); border-radius: var(--radius-full); font-size: 0.9rem; font-weight: 600; box-shadow: var(--shadow-aqua); }
            .plan-icon { 
                font-size: 4rem; 
                margin-bottom: 1.5rem; 
                position: relative;
                z-index: 2;
            }
            .plan-name { 
                font-size: 1.8rem; 
                font-weight: 700; 
                color: white; 
                margin-bottom: 1.5rem;
                position: relative;
                z-index: 2;
            }
            .plan-price { 
                font-size: 3rem; 
                font-weight: 900; 
                background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 1.5rem;
                position: relative;
                z-index: 2;
            }
            .plan-price span { 
                font-size: 1.2rem; 
                color: rgba(255, 255, 255, 0.7); 
                font-weight: 500;
            }
            .plan-description { 
                color: rgba(255, 255, 255, 0.8); 
                margin-bottom: 2rem; 
                line-height: 1.7;
                font-size: 1.1rem;
                position: relative;
                z-index: 2;
            }
            .plan-features { 
                list-style: none; 
                padding: 0; 
                margin-bottom: 2rem; 
                text-align: left;
                position: relative;
                z-index: 2;
            }
            .plan-features li { 
                padding: 0.8rem 0; 
                color: rgba(255, 255, 255, 0.9); 
                position: relative; 
                padding-left: 2rem;
                font-size: 1rem;
            }
            .plan-features li:before { 
                content: '✓'; 
                position: absolute; 
                left: 0; 
                color: #4ecdc4; 
                font-weight: 700;
                font-size: 1.2rem;
            }
            .plan-btn { 
                width: 100%; 
                padding: 1.2rem; 
                background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1);
                background-size: 200% 200%;
                color: white; 
                border: none; 
                border-radius: 12px; 
                font-size: 1.1rem; 
                font-weight: 700; 
                cursor: pointer; 
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
                text-decoration: none; 
                display: inline-block;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                position: relative;
                z-index: 2;
                animation: gradientShift 3s ease infinite;
            }
            .plan-btn:hover { 
                transform: translateY(-3px) scale(1.05);
                box-shadow: 0 15px 30px rgba(255, 107, 107, 0.4);
            }
            .btn-free { 
                background: linear-gradient(135deg, #4ecdc4, #45b7d1);
                animation: none;
            }
            .cta-section { 
                text-align: center; 
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 24px; 
                padding: 3rem; 
                box-shadow: 0 20px 40px rgba(0,0,0,0.3); 
                margin-top: 3rem;
                position: relative;
                z-index: 2;
            }
            .btn { 
                display: inline-block; 
                background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1);
                background-size: 200% 200%;
                color: white; 
                padding: 1.2rem 2.5rem; 
                text-decoration: none; 
                border-radius: 60px; 
                font-weight: 700; 
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
                margin: 0.5rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                animation: gradientShift 3s ease infinite;
            }
            .btn:hover { 
                transform: translateY(-3px) scale(1.05);
                box-shadow: 0 15px 30px rgba(255, 107, 107, 0.4);
            }
            @media (max-width: 768px) { .header h1 { font-size: 2rem; } .plans-grid { grid-template-columns: 1fr; } .plan-card.popular { transform: none; } }
            
    /* Value Analysis Styles */
    .value-analysis {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .value-analysis h4 {
        color: white;
        margin-bottom: 1rem;
        font-size: 1.1rem;
        font-weight: 600;
        text-align: center;
    }

    .value-breakdown {
        margin-bottom: 1rem;
    }

    .value-summary {
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding-top: 1rem;
        margin-top: 1rem;
    }

    .savings-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        color: #4ecdc4;
        font-weight: 600;
        border-top: 1px solid rgba(78, 205, 196, 0.2);
        margin-top: 0.5rem;
    }

    .roi-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        color: #ffd700;
        font-weight: 700;
        font-size: 1.1rem;
        border-top: 1px solid rgba(255, 215, 0, 0.2);
        margin-top: 0.5rem;
    }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🚀 Choose Your Content Creation Path</h1>
            <p>Select the perfect plan for your content automation needs</p>
        </div>
        <div class="container">
            <div class="plans-grid">
                <!-- Script Creation Plan -->
                <div class="plan-card">
                    <div class="plan-icon">📝</div>
                    <div class="plan-name">Script Creation</div>
                    <div class="plan-price">₹120<span>/script</span></div>
                    <div class="plan-description">AI-powered script generation with your writing style</div>
                    <ul class="plan-features">
                        <li>AI-powered script generation</li>
                        <li>Your writing style training</li>
                        <li>Multiple content formats</li>
                        <li>Brand voice customization</li>
                        <li>Export in multiple formats</li>
                    </ul>
                    <a href="/icp-builder?plan=script" class="plan-btn">Start Scripting</a>
                </div>
                
                <!-- Video & Reel Creation Plan -->
                <div class="plan-card popular">
                    <div class="plan-icon">🎬</div>
                    <div class="plan-name">Video & Reel Creation</div>
                    <div class="plan-price">₹1,500<span>+ ₹250/reel</span></div>
                    <div class="plan-description">Create videos and reels with AI voice and avatar</div>
                    <ul class="plan-features">
                        <li>Everything in Script Creation</li>
                        <li>AI voice cloning</li>
                        <li>Video generation</li>
                        <li>Avatar creation</li>
                        <li>Custom backgrounds</li>
                    </ul>
                    <a href="/icp-builder?plan=content" class="plan-btn">Create Reels</a>
                </div>
                
                <!-- Publishing & Distribution Plan -->
                <div class="plan-card">
                    <div class="plan-icon">📱</div>
                    <div class="plan-name">Publishing & Distribution</div>
                    <div class="plan-price">₹3,000<span>+ ₹50/publish</span></div>
                    <div class="plan-description">Automated publishing across all social media platforms</div>
                    <ul class="plan-features">
                        <li>Everything in Video Creation</li>
                        <li>Multi-platform publishing</li>
                        <li>Automated scheduling</li>
                        <li>Analytics dashboard</li>
                        <li>Performance tracking</li>
                    </ul>
                    <a href="/icp-builder?plan=publishing" class="plan-btn">Start Publishing</a>
                </div>
            </div>
            
            <div class="cta-section">
                <h2>Ready to Get Started?</h2>
                <p>Complete your setup to begin creating amazing content with AI</p>
                <a href="/features" class="btn">🔙 Back to Features</a>
            </div>
        </div>
        
        <script>
            // Simple pricing page - show all 3 plans
            document.addEventListener('DOMContentLoaded', function() {
                // All plans are always visible in the simplified structure
                console.log('Content X Studio - 3 Simple Plans Loaded');
            });
        </script>
    </body>
    </html>
    """)

@app.get("/icp-builder")
async def icp_builder(plan: str = "free"):
    """Plan-Specific ICP Builder - Content Sample Upload & AI Training"""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ICP Builder - Content X AI Studio</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
                color: #ffffff;
                min-height: 100vh;
                position: relative;
                overflow-x: hidden;
                padding: 2rem;
            }
            
            body::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: 
                    radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.15) 0%, transparent 50%),
                    radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.1) 0%, transparent 50%);
                pointer-events: none;
            }
            
            .header {
                background: rgba(10, 10, 10, 0.95);
                backdrop-filter: blur(20px);
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                color: white;
                padding: 3rem;
                border-radius: 15px;
                text-align: center;
                margin-bottom: 2rem;
            }
            .header h1 { font-size: 2.5rem; margin-bottom: 1rem; }
            .header p { font-size: 1.2rem; opacity: 0.9; }
            .container { max-width: 1000px; margin: 0 auto; }
            .step-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 2rem; margin-bottom: 2rem; }
            .step-card { 
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 2.5rem; 
                border-radius: 24px; 
                box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                position: relative;
                z-index: 2;
            }
            .step-card h3 { color: white; margin-bottom: 1rem; font-size: 1.3rem; font-weight: 700; }
            .step-card p { color: rgba(255, 255, 255, 0.8); margin-bottom: 1rem; line-height: 1.6; }
            .step-card select, .step-card textarea, .step-card input { 
                width: 100%; 
                padding: 1rem; 
                border: 2px solid rgba(255, 255, 255, 0.2); 
                border-radius: 12px; 
                font-size: 1rem; 
                margin-bottom: 1rem;
                background: rgba(255, 255, 255, 0.05);
                color: white;
                backdrop-filter: blur(10px);
            }
            .step-card select:focus, .step-card textarea:focus, .step-card input:focus { 
                outline: none; 
                border-color: #4ecdc4; 
                box-shadow: 0 0 0 3px rgba(78, 205, 196, 0.2);
                background: rgba(255, 255, 255, 0.1);
            }
            .checkbox-group { display: flex; flex-direction: column; gap: 0.5rem; }
            .checkbox-item { display: flex; align-items: center; gap: 0.5rem; }
            .checkbox-item input[type="checkbox"] { width: auto; }
            .upload-area { 
                border: 2px dashed rgba(255, 255, 255, 0.3); 
                border-radius: 12px; 
                padding: 2rem; 
                text-align: center; 
                background: rgba(255, 255, 255, 0.05); 
                margin: 1rem 0; 
                cursor: pointer; 
                transition: all 0.3s ease;
                color: white;
                position: relative;
                z-index: 2;
            }
            .upload-area:hover { 
                border-color: #4ecdc4; 
                background: rgba(78, 205, 196, 0.1);
            }
            .file-list { margin-top: 1rem; }
            .file-item { 
                display: flex; 
                align-items: center; 
                justify-content: space-between; 
                padding: 0.8rem; 
                background: rgba(255, 255, 255, 0.05); 
                border-radius: 8px; 
                margin: 0.5rem 0;
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            .btn { 
                background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1);
                background-size: 200% 200%;
                color: white; 
                padding: 1.2rem 2.5rem; 
                border: none; 
                border-radius: 12px; 
                font-size: 1.1rem; 
                font-weight: 700; 
                cursor: pointer; 
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
                margin: 0.5rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                position: relative;
                z-index: 2;
                animation: gradientShift 3s ease infinite;
            }
            .btn:hover { 
                transform: translateY(-3px) scale(1.05);
                box-shadow: 0 15px 30px rgba(255, 107, 107, 0.4);
            }
            .btn-secondary { 
                background: linear-gradient(135deg, #6b7280, #9ca3af);
                animation: none;
            }
            .btn-success { 
                background: linear-gradient(135deg, #4ecdc4, #45b7d1);
                animation: none;
            }
            .progress-bar { 
                background: rgba(255, 255, 255, 0.1); 
                height: 8px; 
                border-radius: 4px; 
                margin: 1rem 0; 
                overflow: hidden;
                position: relative;
                z-index: 2;
            }
            .progress-fill { 
                background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1); 
                height: 100%; 
                border-radius: 4px; 
                transition: width 0.3s ease;
                background-size: 200% 200%;
                animation: gradientShift 2s ease infinite;
            }
            .ai-training { 
                background: rgba(78, 205, 196, 0.1); 
                border: 1px solid #4ecdc4; 
                border-radius: 12px; 
                padding: 1.5rem; 
                margin: 1rem 0;
                color: white;
                position: relative;
                z-index: 2;
            }
            .ai-training h4 { color: white; margin-bottom: 0.5rem; font-weight: 700; }
            .ai-training p { color: rgba(255, 255, 255, 0.8); font-size: 0.9rem; }
            .plan-info { 
                background: rgba(78, 205, 196, 0.1); 
                border: 1px solid #4ecdc4; 
                border-radius: 12px; 
                padding: 1.5rem; 
                margin-bottom: 2rem;
                position: relative;
                z-index: 2;
            }
            .plan-info h3 { color: white; margin-bottom: 0.5rem; font-weight: 700; }
            .plan-info p { color: rgba(255, 255, 255, 0.8); margin: 0; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1 id="pageTitle">🤖 AI Training Setup</h1>
            <p id="pageSubtitle">Upload your content samples to train AI agents</p>
        </div>
        
        <div class="container">
            <div class="plan-info">
                <h3 id="planName">Free Plan</h3>
                <p id="planDescription">Perfect for getting started with AI content creation</p>
            </div>
            
            <div class="step-grid">
                <!-- Step 1: Company Information -->
                <div class="step-card">
                    <h3>🏢 Company Information</h3>
                    <input type="text" id="companyName" placeholder="Company Name" required>
                    <select id="industry" required>
                        <option value="">Select your industry...</option>
                        <option value="technology">Technology & Software</option>
                        <option value="healthcare">Healthcare & Medical</option>
                        <option value="finance">Finance & Banking</option>
                        <option value="education">Education & Training</option>
                        <option value="retail">Retail & E-commerce</option>
                        <option value="manufacturing">Manufacturing</option>
                        <option value="consulting">Consulting & Services</option>
                        <option value="media">Media & Entertainment</option>
                    </select>
                    <select id="companySize" required>
                        <option value="">Select company size...</option>
                        <option value="1-10">1-10 employees (Startup)</option>
                        <option value="11-50">11-50 employees (Small Business)</option>
                        <option value="51-200">51-200 employees (Medium Business)</option>
                        <option value="201-1000">201-1000 employees (Large Business)</option>
                        <option value="1000+">1000+ employees (Enterprise)</option>
                    </select>
                </div>
                
                <!-- Step 2: Goals & Target Audience -->
                <div class="step-card">
                    <h3>🎯 Goals & Target Audience</h3>
                    <div class="checkbox-group">
                        <div class="checkbox-item">
                            <input type="checkbox" id="goal1" value="brand-awareness">
                            <label for="goal1">Brand Awareness</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="goal2" value="lead-generation">
                            <label for="goal2">Lead Generation</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="goal3" value="sales-conversion">
                            <label for="goal3">Sales Conversion</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="goal4" value="thought-leadership">
                            <label for="goal4">Thought Leadership</label>
                        </div>
                    </div>
                    <textarea id="targetAudience" rows="3" placeholder="Describe your target audience..." required></textarea>
                </div>
                
                <!-- Step 3: Upload Content Samples (Plan-Specific) -->
                <div class="step-card">
                    <h3>📝 Upload Script Samples</h3>
                    <p>Upload 3-5 of your best scripts so our AI can learn your writing style and tone.</p>
                    <div class="upload-area" onclick="document.getElementById('scriptFiles').click()">
                        <div>📁 Click to upload or drag & drop script files</div>
                        <div style="font-size: 0.9rem; color: rgba(255, 255, 255, 0.6); margin-top: 0.5rem;">Supports: .txt, .doc, .docx, .pdf</div>
                    </div>
                    <input type="file" id="scriptFiles" multiple accept=".txt,.doc,.docx,.pdf" style="display: none;" onchange="handleFileUpload('scriptFiles', 'scriptList')">
                    <div id="scriptList" class="file-list"></div>
                </div>
                
                <!-- Voice Samples (Content+Voice+Video Plans Only) -->
                <div class="step-card" id="voiceCard" style="display: none;">
                    <h3>🎤 Upload Voice Samples</h3>
                    <p>Upload 2-3 voice recordings (30-60 seconds each) for AI voice cloning.</p>
                    <div class="upload-area" onclick="document.getElementById('voiceFiles').click()">
                        <div>🎵 Click to upload or drag & drop voice files</div>
                        <div style="font-size: 0.9rem; color: rgba(255, 255, 255, 0.6); margin-top: 0.5rem;">Supports: .mp3, .wav, .m4a</div>
                    </div>
                    <input type="file" id="voiceFiles" multiple accept=".mp3,.wav,.m4a" style="display: none;" onchange="handleFileUpload('voiceFiles', 'voiceList')">
                    <div id="voiceList" class="file-list"></div>
                </div>
                
                <!-- Video Samples (Content+Voice+Video Plans Only) -->
                <div class="step-card" id="videoCard" style="display: none;">
                    <h3>🎥 Upload Video/Avatar Samples</h3>
                    <p>Upload 1-2 video samples or avatar images to train the video generation AI for creating custom avatars.</p>
                    <div class="upload-area" onclick="document.getElementById('videoFiles').click()">
                        <div>🎬 Click to upload or drag & drop video/image files</div>
                        <div style="font-size: 0.9rem; color: rgba(255, 255, 255, 0.6); margin-top: 0.5rem;">Supports: .mp4, .mov, .avi, .jpg, .png, .jpeg</div>
                    </div>
                    <input type="file" id="videoFiles" multiple accept=".mp4,.mov,.avi,.jpg,.png,.jpeg" style="display: none;" onchange="handleFileUpload('videoFiles', 'videoList')">
                    <div id="videoList" class="file-list"></div>
                </div>
                
                <div class="step-card" id="avatarCard" style="display: none;">
                    <h3>👤 Upload Avatar Samples <span style="background: linear-gradient(135deg, #ff6b6b, #4ecdc4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 0.8rem; font-weight: 700; margin-left: 0.5rem;">COMING SOON</span></h3>
                    <p>Upload 3-5 high-quality photos from different angles for 3D avatar creation. We'll use these to build a dynamic avatar that can speak and move.</p>
                    <div class="upload-area" onclick="document.getElementById('avatarFiles').click()">
                        <div>📸 Click to upload or drag & drop avatar photos</div>
                        <div style="font-size: 0.9rem; color: rgba(255, 255, 255, 0.6); margin-top: 0.5rem;">Supports: .jpg, .png, .jpeg (High resolution, multiple angles recommended)</div>
                    </div>
                    <input type="file" id="avatarFiles" multiple accept=".jpg,.png,.jpeg" style="display: none;" onchange="handleFileUpload('avatarFiles', 'avatarList')">
                    <div id="avatarList" class="file-list"></div>
                    
                    <div class="avatar-requirements" style="margin-top: 1rem; padding: 1rem; background: rgba(78, 205, 196, 0.1); border-radius: 8px; border: 1px solid #4ecdc4;">
                        <h4 style="color: white; margin-bottom: 0.5rem; font-size: 1rem;">📋 Avatar Photo Requirements:</h4>
                        <ul style="color: rgba(255, 255, 255, 0.8); font-size: 0.9rem; margin: 0; padding-left: 1.5rem;">
                            <li>Front-facing photo (looking at camera)</li>
                            <li>Profile photo (side view)</li>
                            <li>45-degree angle photo</li>
                            <li>Smiling expression photo</li>
                            <li>Neutral expression photo</li>
                        </ul>
                    </div>
                </div>
                
                <div class="step-card" id="videoSamplesCard" style="display: none;">
                    <h3>🎬 Upload Video Samples (Optional) <span style="background: linear-gradient(135deg, #ff6b6b, #4ecdc4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 0.8rem; font-weight: 700; margin-left: 0.5rem;">COMING SOON</span></h3>
                    <p>Upload 1-2 short video clips (10-30 seconds) to capture your natural movements, gestures, and speaking style for better avatar animation.</p>
                    <div class="upload-area" onclick="document.getElementById('videoSampleFiles').click()">
                        <div>🎥 Click to upload or drag & drop video samples</div>
                        <div style="font-size: 0.9rem; color: rgba(255, 255, 255, 0.6); margin-top: 0.5rem;">Supports: .mp4, .mov, .avi (Short clips, good lighting)</div>
                    </div>
                    <input type="file" id="videoSampleFiles" multiple accept=".mp4,.mov,.avi" style="display: none;" onchange="handleFileUpload('videoSampleFiles', 'videoSampleList')">
                    <div id="videoSampleList" class="file-list"></div>
                </div>
                
                <!-- Dynamic Pricing Slider with Cost Analysis -->
                <div class="step-card" id="pricingCard" style="display: none;">
                    <h3>💰 Choose Your Volume & View Cost Analysis</h3>
                    <div class="pricing-slider-container">
                        <div class="slider-info">
                            <p>How many <span id="unitType">scripts</span> do you want to create per month?</p>
                            <div class="quantity-display">
                                <span id="quantityDisplay">10</span> <span id="unitType">scripts</span>
                            </div>
                        </div>
                        
                        <div class="slider-container">
                            <input type="range" id="quantitySlider" min="5" max="100" value="10" 
                                   oninput="onQuantityChange(this.value)" 
                                   style="width: 100%; height: 8px; border-radius: 5px; background: linear-gradient(135deg, #ff6b6b, #4ecdc4); outline: none;">
                            <div class="slider-labels">
                                <span>5</span>
                                <span>50</span>
                                <span>100</span>
                            </div>
                        </div>
                        
                        <div class="pricing-display">
                            <div class="price-breakdown">
                                <div class="price-item">
                                    <span>Base Plan:</span>
                                    <span id="basePrice">₹0</span>
                                </div>
                                <div class="price-item">
                                    <span>Volume (<span id="quantityDisplay2">10</span> <span id="unitType2">scripts</span>):</span>
                                    <span id="volumePrice">₹1,200</span>
                                </div>
                                <div class="price-total">
                                    <span>Your Monthly Investment:</span>
                                    <span id="totalPrice">₹1,200</span>
                                </div>
                            </div>
                            
                            <!-- Value Proposition Section -->
                            <div class="value-analysis">
                                <h4>🎯 What You Get</h4>
                                <div class="value-breakdown" id="valueBreakdown">
                                    <div class="value-item">
                                        <span>AI Script Generation:</span>
                                        <span>Premium Quality</span>
                                    </div>
                                    <div class="value-item">
                                        <span>Processing Speed:</span>
                                        <span>Lightning Fast</span>
                                    </div>
                                    <div class="value-item">
                                        <span>Storage & Backup:</span>
                                        <span>Unlimited</span>
                                    </div>
                                </div>
                                
                                <div class="value-summary">
                                    <div class="value-item">
                                        <span>Content Quality:</span>
                                        <span>Enterprise Grade</span>
                                    </div>
                                    <div class="value-item">
                                        <span>Delivery Time:</span>
                                        <span>Instant</span>
                                    </div>
                                    <div class="savings-item">
                                        <span>vs Traditional Methods:</span>
                                        <span id="traditionalSavings">Save 80% Time</span>
                                    </div>
                                    <div class="roi-item">
                                        <span>Expected ROI:</span>
                                        <span id="customerROI">300%+</span>
                                    </div>
                                </div>
                            </div>
                            
                            <button class="btn btn-primary" onclick="proceedToPayment()" style="width: 100%; margin-top: 1rem;">
                                Start Creating - <span id="monthlyPrice">₹1,200/month</span>
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- AI Training Progress -->
                <div class="step-card">
                    <h3>🤖 AI Agent Training</h3>
                    <div class="ai-training">
                        <h4>Script Agent Training</h4>
                        <div class="progress-bar">
                            <div class="progress-fill" id="scriptProgress" style="width: 0%;"></div>
                        </div>
                        <p id="scriptStatus">Upload script samples to begin training...</p>
                    </div>
                    <div class="ai-training" id="voiceTraining" style="display: none;">
                        <h4>Voice Agent Training</h4>
                        <div class="progress-bar">
                            <div class="progress-fill" id="voiceProgress" style="width: 0%;"></div>
                        </div>
                        <p id="voiceStatus">Upload voice samples to begin training...</p>
                    </div>
                    <div class="ai-training" id="videoTraining" style="display: none;">
                        <h4>Video Agent Training</h4>
                        <div class="progress-bar">
                            <div class="progress-fill" id="videoProgress" style="width: 0%;"></div>
                        </div>
                        <p id="videoStatus">Upload video samples to begin training...</p>
                    </div>
                    <div class="ai-training" id="avatarTraining" style="display: none;">
                        <h4>3D Avatar Creation <span style="background: linear-gradient(135deg, #ff6b6b, #4ecdc4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 0.7rem; font-weight: 700; margin-left: 0.5rem;">COMING SOON</span></h4>
                        <div class="progress-bar">
                            <div class="progress-fill" id="avatarProgress" style="width: 0%;"></div>
                        </div>
                        <p id="avatarStatus">Upload avatar photos to begin 3D model creation...</p>
                        <div style="font-size: 0.9rem; color: rgba(255, 255, 255, 0.7); margin-top: 0.5rem;">
                            <strong>Process:</strong> Facial mapping → 3D model generation → Rigging → Animation setup
                        </div>
                    </div>
                    
                    <div class="ai-training" id="videoGenerationTraining" style="display: none;">
                        <h4>Video Generation Setup <span style="background: linear-gradient(135deg, #ff6b6b, #4ecdc4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 0.7rem; font-weight: 700; margin-left: 0.5rem;">COMING SOON</span></h4>
                        <div class="progress-bar">
                            <div class="progress-fill" id="videoGenProgress" style="width: 0%;"></div>
                        </div>
                        <p id="videoGenStatus">Setting up video generation pipeline...</p>
                        <div style="font-size: 0.9rem; color: rgba(255, 255, 255, 0.7); margin-top: 0.5rem;">
                            <strong>Pipeline:</strong> Script → Voice → Lip Sync → Avatar Animation → Video Rendering
                        </div>
                    </div>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 2rem;">
                <a href="/dashboard" class="btn btn-secondary">Skip to Dashboard</a>
            </div>
        </div>
        
        <script>
            let uploadedFiles = { scripts: [], voices: [], videos: [] };
            let currentPlan = 'free';
            
            // Plan configurations - OPTIMIZED COST STRUCTURE for profitability
            const planConfigs = {
                'script': {
                    name: 'Script Creation',
                    description: 'AI-powered script generation with your writing style',
                    features: ['Script samples only'],
                    pricing: { base: 0, perScript: 120 }, // ₹120 per script (reduced from ₹150)
                    costs: {
                        openai_gpt35: 15,    // ₹15 per script (GPT-3.5 Turbo instead of GPT-4)
                        processing: 5,       // ₹5 processing cost (optimized)
                        storage: 2,          // ₹2 storage cost (compressed)
                        total: 22            // ₹22 total cost per script (66% reduction)
                    }
                },
                'content': {
                    name: 'Video & Reel Creation',
                    description: 'Create videos and reels with AI voice and avatar',
                    features: ['Script samples', 'Voice samples', 'Video samples'],
                    pricing: { base: 1500, perReel: 250 }, // ₹1500 base + ₹250 per reel (optimized pricing)
                    costs: {
                        script: 22,          // ₹22 script generation (optimized)
                        voice_tts: 25,       // ₹25 TTS (free/cheap TTS instead of ElevenLabs)
                        video_processing: 45, // ₹45 video processing (optimized pipeline)
                        processing: 8,       // ₹8 processing cost (efficient)
                        storage: 5,          // ₹5 storage cost (compressed)
                        total: 105           // ₹105 total cost per reel (74% reduction)
                    }
                },
                'publishing': {
                    name: 'Publishing & Distribution',
                    description: 'Automated publishing across all social media platforms',
                    features: ['Script samples', 'Voice samples', 'Video samples', 'Publishing automation'],
                    pricing: { base: 3000, perPublish: 50 }, // ₹3000 base + ₹50 per publish (optimized)
                    costs: {
                        content: 105,        // ₹105 content creation cost (optimized)
                        api_calls: 3,        // ₹3 social media API calls (bulk pricing)
                        monitoring: 2,       // ₹2 monitoring/analytics (automated)
                        processing: 5,       // ₹5 processing cost (efficient)
                        total: 115           // ₹115 total cost per publish (74% reduction)
                    }
                }
            };
            
            // Initialize based on plan
            function initializePlan() {
                const urlParams = new URLSearchParams(window.location.search);
                currentPlan = urlParams.get('plan') || 'free';
                
                const config = planConfigs[currentPlan];
                document.getElementById('planName').textContent = config.name;
                document.getElementById('planDescription').textContent = config.description;
                
                // Show/hide sections based on plan
                const voiceCard = document.getElementById('voiceCard');
                const videoCard = document.getElementById('videoCard');
                const avatarCard = document.getElementById('avatarCard');
                const videoSamplesCard = document.getElementById('videoSamplesCard');
                const voiceTraining = document.getElementById('voiceTraining');
                const videoTraining = document.getElementById('videoTraining');
                const avatarTraining = document.getElementById('avatarTraining');
                const videoGenerationTraining = document.getElementById('videoGenerationTraining');
                
                if (config.features.includes('Voice samples')) {
                    voiceCard.style.display = 'block';
                    voiceTraining.style.display = 'block';
                }
                
                if (config.features.includes('Video samples')) {
                    videoCard.style.display = 'block';
                    videoTraining.style.display = 'block';
                }
                
                // Show avatar card and training for content creation plans
                if (config.features.some(feature => feature.includes('Avatar creation'))) {
                    avatarCard.style.display = 'block';
                    avatarTraining.style.display = 'block';
                    videoSamplesCard.style.display = 'block';
                    videoGenerationTraining.style.display = 'block';
                } else {
                    // Hide avatar and video cards for script-only plans
                    avatarCard.style.display = 'none';
                    avatarTraining.style.display = 'none';
                    videoSamplesCard.style.display = 'none';
                    videoGenerationTraining.style.display = 'none';
                }
                
                // Show pricing slider for all plans
                document.getElementById('pricingCard').style.display = 'block';
                updatePricing();
            }
            
            function handleFileUpload(inputId, listId) {
                const input = document.getElementById(inputId);
                const list = document.getElementById(listId);
                const files = Array.from(input.files);
                
                files.forEach(file => {
                    const fileItem = document.createElement('div');
                    fileItem.className = 'file-item';
                    fileItem.innerHTML = `
                        <span>📄 ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)</span>
                        <button onclick="removeFile('${inputId}', '${file.name}')" style="background: #e53e3e; color: white; border: none; padding: 0.3rem 0.6rem; border-radius: 4px; cursor: pointer;">Remove</button>
                    `;
                    list.appendChild(fileItem);
                    
                    // Store file info
                    const category = inputId.replace('Files', 's');
                    uploadedFiles[category].push(file);
                });

                tryAutoStartTraining();
            }
            
            function removeFile(inputId, fileName) {
                const category = inputId.replace('Files', 's');
                uploadedFiles[category] = uploadedFiles[category].filter(f => f.name !== fileName);
                // Refresh the list
                const list = document.getElementById(inputId.replace('Files', 'List'));
                list.innerHTML = '';
                uploadedFiles[category].forEach(file => {
                    const fileItem = document.createElement('div');
                    fileItem.className = 'file-item';
                    fileItem.innerHTML = `
                        <span>📄 ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)</span>
                        <button onclick="removeFile('${inputId}', '${file.name}')" style="background: #e53e3e; color: white; border: none; padding: 0.3rem 0.6rem; border-radius: 4px; cursor: pointer;">Remove</button>
                    `;
                    list.appendChild(fileItem);
                });

                tryAutoStartTraining();
            }

            function hasRequiredUploads() {
                if (uploadedFiles.scripts.length === 0) return false;
                if (currentPlan !== 'free' && currentPlan !== 'script') {
                    // For content plans, voice is recommended but not strictly required
                    // For full content plans with video, at least one of voice/video is acceptable
                }
                return true;
            }

            let trainingStarted = false;
            let selectedQuantity = 10; // Default quantity
            
            function tryAutoStartTraining() {
                if (trainingStarted) return;
                const companyName = document.getElementById('companyName').value;
                const industry = document.getElementById('industry').value;
                const companySize = document.getElementById('companySize').value;
                const targetAudience = document.getElementById('targetAudience').value;
                if (!companyName || !industry || !companySize || !targetAudience) return;
                if (!hasRequiredUploads()) return;
                trainingStarted = true;
                simulateTraining();
            }
            
            // Dynamic pricing slider with cost analysis
            function updatePricing() {
                const config = planConfigs[currentPlan];
                const quantity = selectedQuantity;
                let basePrice = 0;
                let unitPrice = 0;
                let totalPrice = 0;
                let unitType = '';
                let unitCost = 0;
                let totalCost = 0;
                
                if (currentPlan === 'script') {
                    basePrice = 0;
                    unitPrice = config.pricing.perScript;
                    unitCost = config.costs.total;
                    totalPrice = quantity * unitPrice;
                    totalCost = quantity * unitCost;
                    unitType = 'scripts';
                } else if (currentPlan === 'content') {
                    basePrice = config.pricing.base;
                    unitPrice = config.pricing.perReel;
                    unitCost = config.costs.total;
                    totalPrice = basePrice + (quantity * unitPrice);
                    totalCost = quantity * unitCost;
                    unitType = 'reels';
                } else if (currentPlan === 'publishing') {
                    basePrice = config.pricing.base;
                    unitPrice = config.pricing.perPublish;
                    unitCost = config.costs.total;
                    totalPrice = basePrice + (quantity * unitPrice);
                    totalCost = quantity * unitCost;
                    unitType = 'publishes';
                }
                
                const profit = totalPrice - totalCost;
                const profitMargin = totalPrice > 0 ? ((profit / totalPrice) * 100).toFixed(1) : 0;
                
                // Update all display elements
                document.getElementById('quantityDisplay').textContent = quantity;
                document.getElementById('quantityDisplay2').textContent = quantity;
                document.getElementById('unitType').textContent = unitType;
                document.getElementById('unitType2').textContent = unitType;
                document.getElementById('basePrice').textContent = `₹${basePrice}`;
                document.getElementById('volumePrice').textContent = `₹${quantity * unitPrice}`;
                document.getElementById('totalPrice').textContent = `₹${totalPrice}`;
                document.getElementById('monthlyPrice').textContent = `₹${totalPrice}/month`;
                
        // Update value analysis
        updateValueAnalysis(config, quantity, totalPrice);
            }
            
            function updateValueAnalysis(config, quantity, totalPrice) {
                // Calculate value metrics
                const timeSaved = quantity * 2; // 2 hours saved per script
                const traditionalCost = quantity * 500; // Traditional method cost
                const savings = traditionalCost - totalPrice;
                const savingsPercentage = Math.round((savings / traditionalCost) * 100);
                const roi = Math.round((savings / totalPrice) * 100);

                // Update value breakdown
                let valueBreakdown = '';
                if (currentPlan === 'script') {
                    valueBreakdown = `
                        <div class="value-item">
                            <span>AI Script Generation:</span>
                            <span>Premium Quality</span>
                        </div>
                        <div class="value-item">
                            <span>Processing Speed:</span>
                            <span>Lightning Fast</span>
                        </div>
                        <div class="value-item">
                            <span>Storage & Backup:</span>
                            <span>Unlimited</span>
                        </div>
                    `;
                } else if (currentPlan === 'content') {
                    valueBreakdown = `
                        <div class="value-item">
                            <span>AI Video Creation:</span>
                            <span>Professional Quality</span>
                        </div>
                        <div class="value-item">
                            <span>Voice Cloning:</span>
                            <span>Studio Quality</span>
                        </div>
                        <div class="value-item">
                            <span>Avatar Generation:</span>
                            <span>Custom Built</span>
                        </div>
                    `;
                } else if (currentPlan === 'publishing') {
                    valueBreakdown = `
                        <div class="value-item">
                            <span>Multi-Platform Publishing:</span>
                            <span>All Social Media</span>
                        </div>
                        <div class="value-item">
                            <span>Automated Scheduling:</span>
                            <span>Smart Timing</span>
                        </div>
                        <div class="value-item">
                            <span>Analytics & Insights:</span>
                            <span>Real-time Data</span>
                        </div>
                    `;
                }

                document.getElementById('valueBreakdown').innerHTML = valueBreakdown;
                
                // Update value summary
                document.getElementById('traditionalSavings').textContent = `Save ${savingsPercentage}% vs Traditional`;
                document.getElementById('customerROI').textContent = `${roi}% ROI`;
            }
            
            function onQuantityChange(value) {
                selectedQuantity = parseInt(value);
                updatePricing();
            }
            
            function proceedToPayment() {
                const config = planConfigs[currentPlan];
                const quantity = selectedQuantity;
                
                // Store payment info in localStorage
                localStorage.setItem('selectedPlan', currentPlan);
                localStorage.setItem('selectedQuantity', quantity);
                localStorage.setItem('totalPrice', document.getElementById('totalPrice').textContent);
                
                // Redirect to payment processing
                alert(`Proceeding to payment for ${quantity} ${config.name.toLowerCase()} - ${document.getElementById('totalPrice').textContent}/month`);
                
                // In real implementation, redirect to Stripe/payment processor
                // window.location.href = '/payment?plan=' + currentPlan + '&quantity=' + quantity;
                
                // For demo, redirect to dashboard
                window.location.href = '/dashboard';
            }
            
            function simulateTraining() {
                // Script Agent Training (Always)
                let scriptProgress = 0;
                const scriptInterval = setInterval(() => {
                    scriptProgress += Math.random() * 20;
                    if (scriptProgress >= 100) {
                        scriptProgress = 100;
                        clearInterval(scriptInterval);
                        document.getElementById('scriptStatus').textContent = '✅ Script Agent trained successfully!';
                    }
                    document.getElementById('scriptProgress').style.width = scriptProgress + '%';
                    document.getElementById('scriptStatus').textContent = `Training script agent... ${Math.round(scriptProgress)}%`;
                }, 500);
                
                // Voice Agent Training (if applicable)
                if (currentPlan !== 'free' && currentPlan !== 'script' && uploadedFiles.voices.length > 0) {
                    let voiceProgress = 0;
                    const voiceInterval = setInterval(() => {
                        voiceProgress += Math.random() * 15;
                        if (voiceProgress >= 100) {
                            voiceProgress = 100;
                            clearInterval(voiceInterval);
                            document.getElementById('voiceStatus').textContent = '✅ Voice Agent trained successfully!';
                        }
                        document.getElementById('voiceProgress').style.width = voiceProgress + '%';
                        document.getElementById('voiceStatus').textContent = `Training voice agent... ${Math.round(voiceProgress)}%`;
                    }, 600);
                }
                
                // Video Agent Training (if applicable)
                if ((currentPlan === 'content-voice-video' || currentPlan === 'publishing' || currentPlan === 'fullstack') && uploadedFiles.videos.length > 0) {
                    let videoProgress = 0;
                    const videoInterval = setInterval(() => {
                        videoProgress += Math.random() * 10;
                        if (videoProgress >= 100) {
                            videoProgress = 100;
                            clearInterval(videoInterval);
                            document.getElementById('videoStatus').textContent = '✅ Video Agent trained successfully!';
                        }
                        document.getElementById('videoProgress').style.width = videoProgress + '%';
                        document.getElementById('videoStatus').textContent = `Training video agent... ${Math.round(videoProgress)}%`;
                    }, 700);
                }
                
                // Complete setup after 5 seconds
                setTimeout(() => {
                    const icpData = {
                        companyName: document.getElementById('companyName').value,
                        industry: document.getElementById('industry').value,
                        companySize: document.getElementById('companySize').value,
                        plan: currentPlan,
                        goals: Array.from(document.querySelectorAll('input[type="checkbox"]:checked')).map(cb => cb.value),
                        targetAudience: document.getElementById('targetAudience').value,
                        uploadedFiles: uploadedFiles,
                        aiTrainingComplete: true,
                        completedAt: new Date().toISOString()
                    };
                    
                    localStorage.setItem('icp_profile', JSON.stringify(icpData));
                    window.location.href = '/dashboard';
                }, 5000);
            }
            
            // Initialize on page load
            initializePlan();
            // Auto-start when user fills form fields
            ['companyName','industry','companySize','targetAudience'].forEach(id => {
                const el = document.getElementById(id);
                el.addEventListener('change', tryAutoStartTraining);
                el.addEventListener('input', tryAutoStartTraining);
            });
        </script>
    </body>
    </html>
    """)

@app.get("/publishing")
async def publishing_dashboard():
    """Publishing Dashboard Page"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Publishing Dashboard - Content X AI Studio</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: var(--gradient-ocean);
                color: var(--white);
                min-height: 100vh;
                position: relative;
                overflow-x: hidden;
            }
            
            body::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: 
                    radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.15) 0%, transparent 50%),
                    radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.1) 0%, transparent 50%);
                pointer-events: none;
            }
            
            .header {
                background: rgba(10, 10, 10, 0.95);
                backdrop-filter: blur(20px);
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                color: white;
                padding: 2rem 0;
                text-align: center;
                position: relative;
                z-index: 10;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }
            
            .header h1 {
                font-size: 3rem;
                font-weight: 900;
                margin-bottom: 1rem;
                background: linear-gradient(135deg, #ffffff, #f8f9fa, #e9ecef);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: -0.02em;
            }
            
            .header p {
                font-size: 1.2rem;
                font-weight: 300;
                opacity: 0.85;
                max-width: 600px;
                margin: 0 auto;
                line-height: 1.7;
            }
            
            .container {
                max-width: 1400px;
                margin: 2rem auto;
                padding: 0 2rem;
                position: relative;
                z-index: 2;
            }
            
            .dashboard-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 2rem;
                margin-bottom: 2rem;
            }
            
            .widget {
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 24px;
                padding: 2rem;
                box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }
            
            .widget:hover {
                transform: translateY(-5px);
                box-shadow: 0 30px 60px rgba(0,0,0,0.4);
                border-color: rgba(255, 255, 255, 0.2);
            }
            
            .widget h3 {
                font-size: 1.5rem;
                color: white;
                margin-bottom: 1.5rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            .platform-status {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
            }
            
            .platform-card {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                padding: 1.5rem;
                text-align: center;
                transition: all 0.3s ease;
            }
            
            .platform-card.connected {
                border-color: #48bb78;
                background: rgba(72, 187, 120, 0.1);
            }
            
            .platform-card.disconnected {
                border-color: #f56565;
                background: rgba(245, 101, 101, 0.1);
            }
            
            .platform-icon {
                font-size: 2rem;
                margin-bottom: 0.5rem;
            }
            
            .platform-name {
                font-weight: 600;
                margin-bottom: 0.5rem;
            }
            
            .platform-status-text {
                font-size: 0.9rem;
                opacity: 0.8;
            }
            
            .connect-btn {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s;
                margin-top: 0.5rem;
            }
            
            .connect-btn:hover {
                transform: translateY(-2px);
            }
            
            .publishing-form {
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 24px;
                padding: 2rem;
                box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                margin-bottom: 2rem;
            }
            
            .form-group {
                margin-bottom: 1.5rem;
            }
            
            .form-group label {
                display: block;
                color: white;
                margin-bottom: 0.5rem;
                font-weight: 600;
            }
            
            .form-group input,
            .form-group textarea,
            .form-group select {
                width: 100%;
                padding: 1rem;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                background: rgba(255, 255, 255, 0.05);
                color: white;
                font-size: 1rem;
                transition: all 0.3s ease;
            }
            
            .form-group input:focus,
            .form-group textarea:focus,
            .form-group select:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            
            .form-group textarea {
                min-height: 120px;
                resize: vertical;
            }
            
            .platform-checkboxes {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 1rem;
                margin-top: 0.5rem;
            }
            
            .platform-checkbox {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                color: white;
                cursor: pointer;
            }
            
            .platform-checkbox input[type="checkbox"] {
                width: auto;
                margin: 0;
            }
            
            .publish-buttons {
                display: flex;
                gap: 1rem;
                margin-top: 2rem;
            }
            
            .btn {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border: none;
                padding: 1rem 2rem;
                border-radius: 12px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s;
                flex: 1;
            }
            
            .btn:hover {
                transform: translateY(-2px);
            }
            
            .btn-secondary {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .scheduled-posts {
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 24px;
                padding: 2rem;
                box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            }
            
            .post-item {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                padding: 1.5rem;
                margin-bottom: 1rem;
                transition: all 0.3s ease;
            }
            
            .post-item:hover {
                border-color: rgba(255, 255, 255, 0.2);
                transform: translateY(-2px);
            }
            
            .post-header {
                display: flex;
                justify-content: between;
                align-items: center;
                margin-bottom: 1rem;
            }
            
            .post-content {
                color: rgba(255, 255, 255, 0.9);
                margin-bottom: 1rem;
                line-height: 1.6;
            }
            
            .post-platforms {
                display: flex;
                gap: 0.5rem;
                margin-bottom: 1rem;
            }
            
            .platform-tag {
                background: rgba(102, 126, 234, 0.2);
                color: #667eea;
                padding: 0.25rem 0.75rem;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 600;
            }
            
            .post-schedule {
                color: rgba(255, 255, 255, 0.7);
                font-size: 0.9rem;
            }
            
            .post-actions {
                display: flex;
                gap: 0.5rem;
                margin-top: 1rem;
            }
            
            .btn-small {
                padding: 0.5rem 1rem;
                font-size: 0.9rem;
                border-radius: 8px;
            }
            
            .btn-danger {
                background: #f56565;
            }
            
            .analytics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1.5rem;
                margin-top: 2rem;
            }
            
            .analytics-card {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                padding: 1.5rem;
                text-align: center;
            }
            
            .analytics-number {
                font-size: 2rem;
                font-weight: 900;
                color: #4ecdc4;
                margin-bottom: 0.5rem;
            }
            
            .analytics-label {
                color: rgba(255, 255, 255, 0.8);
                font-size: 0.9rem;
            }
            
            @media (max-width: 768px) {
                .dashboard-grid { grid-template-columns: 1fr; }
                .publish-buttons { flex-direction: column; }
                .platform-checkboxes { grid-template-columns: 1fr; }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📤 Publishing Dashboard</h1>
            <p>Automate your content publishing across all social media platforms</p>
        </div>
        
        <div class="container">
            <!-- Platform Status Widget -->
            <div class="widget">
                <h3>🔗 Platform Connections</h3>
                <div class="platform-status" id="platformStatus">
                    <!-- Platform status will be loaded here -->
                </div>
            </div>
            
            <!-- Publishing Form -->
            <div class="publishing-form">
                <h3>📝 Create New Post</h3>
                <form id="publishingForm">
                    <div class="form-group">
                        <label for="postContent">Content</label>
                        <textarea id="postContent" placeholder="What's on your mind? Write your post content here..." required></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="hashtags">Hashtags (comma-separated)</label>
                        <input type="text" id="hashtags" placeholder="contentx, aistudio, automation, socialmedia">
                    </div>
                    
                    <div class="form-group">
                        <label for="mediaUrl">Media URL (optional)</label>
                        <input type="url" id="mediaUrl" placeholder="https://example.com/image.jpg">
                    </div>
                    
                    <div class="form-group">
                        <label>Select Platforms</label>
                        <div class="platform-checkboxes">
                            <label class="platform-checkbox">
                                <input type="checkbox" value="instagram" checked>
                                <span>📷 Instagram</span>
                            </label>
                            <label class="platform-checkbox">
                                <input type="checkbox" value="facebook" checked>
                                <span>📘 Facebook</span>
                            </label>
                            <label class="platform-checkbox">
                                <input type="checkbox" value="linkedin" checked>
                                <span>💼 LinkedIn</span>
                            </label>
                            <label class="platform-checkbox">
                                <input type="checkbox" value="twitter" checked>
                                <span>🐦 Twitter</span>
                            </label>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label for="scheduleTime">Schedule Time (optional)</label>
                        <input type="datetime-local" id="scheduleTime">
                    </div>
                    
                    <div class="publish-buttons">
                        <button type="button" class="btn" onclick="publishImmediately()">🚀 Publish Now</button>
                        <button type="button" class="btn btn-secondary" onclick="schedulePost()">⏰ Schedule Post</button>
                    </div>
                </form>
            </div>
            
            <!-- Scheduled Posts -->
            <div class="scheduled-posts">
                <h3>📅 Scheduled Posts</h3>
                <div id="scheduledPostsList">
                    <!-- Scheduled posts will be loaded here -->
                </div>
            </div>
            
            <!-- Analytics -->
            <div class="analytics-grid">
                <div class="analytics-card">
                    <div class="analytics-number" id="totalPosts">0</div>
                    <div class="analytics-label">Total Posts</div>
                </div>
                <div class="analytics-card">
                    <div class="analytics-number" id="successRate">0%</div>
                    <div class="analytics-label">Success Rate</div>
                </div>
                <div class="analytics-card">
                    <div class="analytics-number" id="scheduledCount">0</div>
                    <div class="analytics-label">Scheduled</div>
                </div>
                <div class="analytics-card">
                    <div class="analytics-number" id="connectedPlatforms">0</div>
                    <div class="analytics-label">Connected Platforms</div>
                </div>
            </div>
        </div>
        
        <script>
            const userId = 'demo_user_123';
            
            // Load platform status
            async function loadPlatformStatus() {
                try {
                    const response = await fetch('/api/publishing/platforms/status');
                    const data = await response.json();
                    
                    const statusContainer = document.getElementById('platformStatus');
                    const platforms = [
                        { name: 'Instagram', icon: '📷', key: 'instagram' },
                        { name: 'Facebook', icon: '📘', key: 'facebook' },
                        { name: 'LinkedIn', icon: '💼', key: 'linkedin' },
                        { name: 'Twitter', icon: '🐦', key: 'twitter' }
                    ];
                    
                    statusContainer.innerHTML = platforms.map(platform => {
                        const status = data.platforms[platform.key];
                        const isConnected = status.connected;
                        
                        return `
                            <div class="platform-card ${isConnected ? 'connected' : 'disconnected'}">
                                <div class="platform-icon">${platform.icon}</div>
                                <div class="platform-name">${platform.name}</div>
                                <div class="platform-status-text">
                                    ${isConnected ? 'Connected' : 'Not Connected'}
                                </div>
                                <button class="connect-btn" onclick="connectPlatform('${platform.key}')">
                                    ${isConnected ? 'Reconnect' : 'Connect'}
                                </button>
                            </div>
                        `;
                    }).join('');
                    
                    document.getElementById('connectedPlatforms').textContent = data.total_connected;
                } catch (error) {
                    console.error('Error loading platform status:', error);
                }
            }
            
            // Connect to platform
            async function connectPlatform(platform) {
                try {
                    const formData = new FormData();
                    formData.append('platform', platform);
                    formData.append('access_token', 'demo_token_' + platform);
                    formData.append('user_id', userId);
                    
                    const response = await fetch('/api/publishing/connect', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (result.status === 'success') {
                        alert(`Successfully connected to ${platform}!`);
                        loadPlatformStatus();
                    } else {
                        alert(`Failed to connect to ${platform}: ${result.error}`);
                    }
                } catch (error) {
                    console.error('Error connecting to platform:', error);
                    alert('Error connecting to platform');
                }
            }
            
            // Publish immediately
            async function publishImmediately() {
                const content = document.getElementById('postContent').value;
                const hashtags = document.getElementById('hashtags').value;
                const mediaUrl = document.getElementById('mediaUrl').value;
                const selectedPlatforms = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
                    .map(cb => cb.value);
                
                if (!content.trim()) {
                    alert('Please enter post content');
                    return;
                }
                
                if (selectedPlatforms.length === 0) {
                    alert('Please select at least one platform');
                    return;
                }
                
                try {
                    const formData = new FormData();
                    formData.append('user_id', userId);
                    formData.append('content', content);
                    formData.append('platforms', selectedPlatforms.join(','));
                    formData.append('hashtags', hashtags);
                    formData.append('media_url', mediaUrl);
                    
                    const response = await fetch('/api/publishing/publish', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (result.status === 'publishing') {
                        alert(`Post is being published to ${selectedPlatforms.length} platforms!`);
                        loadScheduledPosts();
                        loadAnalytics();
                    } else {
                        alert(`Failed to publish: ${result.error}`);
                    }
                } catch (error) {
                    console.error('Error publishing:', error);
                    alert('Error publishing post');
                }
            }
            
            // Schedule post
            async function schedulePost() {
                const content = document.getElementById('postContent').value;
                const hashtags = document.getElementById('hashtags').value;
                const mediaUrl = document.getElementById('mediaUrl').value;
                const scheduleTime = document.getElementById('scheduleTime').value;
                const selectedPlatforms = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
                    .map(cb => cb.value);
                
                if (!content.trim()) {
                    alert('Please enter post content');
                    return;
                }
                
                if (selectedPlatforms.length === 0) {
                    alert('Please select at least one platform');
                    return;
                }
                
                if (!scheduleTime) {
                    alert('Please select a schedule time');
                    return;
                }
                
                try {
                    const formData = new FormData();
                    formData.append('user_id', userId);
                    formData.append('content', content);
                    formData.append('platforms', selectedPlatforms.join(','));
                    formData.append('hashtags', hashtags);
                    formData.append('media_url', mediaUrl);
                    formData.append('schedule_time', scheduleTime + 'Z');
                    
                    const response = await fetch('/api/publishing/schedule', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (result.status === 'success') {
                        alert(`Post scheduled for ${new Date(scheduleTime).toLocaleString()}!`);
                        loadScheduledPosts();
                        loadAnalytics();
                    } else {
                        alert(`Failed to schedule: ${result.error}`);
                    }
                } catch (error) {
                    console.error('Error scheduling:', error);
                    alert('Error scheduling post');
                }
            }
            
            // Load scheduled posts
            async function loadScheduledPosts() {
                try {
                    const response = await fetch(`/api/publishing/scheduled/${userId}`);
                    const data = await response.json();
                    
                    const postsContainer = document.getElementById('scheduledPostsList');
                    
                    if (data.posts.length === 0) {
                        postsContainer.innerHTML = '<p style="text-align: center; color: rgba(255,255,255,0.6); padding: 2rem;">No scheduled posts</p>';
                        return;
                    }
                    
                    postsContainer.innerHTML = data.posts.map(post => `
                        <div class="post-item">
                            <div class="post-header">
                                <strong>Post #${post.post_id.substring(0, 8)}</strong>
                                <span class="post-schedule">
                                    ${new Date(post.schedule_time).toLocaleString()}
                                </span>
                            </div>
                            <div class="post-content">${post.content.text}</div>
                            <div class="post-platforms">
                                ${post.platforms.map(platform => 
                                    `<span class="platform-tag">${platform}</span>`
                                ).join('')}
                            </div>
                            <div class="post-actions">
                                <button class="btn btn-small btn-danger" onclick="cancelPost('${post.post_id}')">
                                    Cancel
                                </button>
                            </div>
                        </div>
                    `).join('');
                    
                    document.getElementById('scheduledCount').textContent = data.posts.length;
                } catch (error) {
                    console.error('Error loading scheduled posts:', error);
                }
            }
            
            // Cancel post
            async function cancelPost(postId) {
                if (!confirm('Are you sure you want to cancel this post?')) return;
                
                try {
                    const response = await fetch(`/api/publishing/cancel/${postId}`, {
                        method: 'DELETE'
                    });
                    
                    const result = await response.json();
                    
                    if (result.status === 'success') {
                        alert('Post cancelled successfully');
                        loadScheduledPosts();
                        loadAnalytics();
                    } else {
                        alert(`Failed to cancel: ${result.message}`);
                    }
                } catch (error) {
                    console.error('Error cancelling post:', error);
                    alert('Error cancelling post');
                }
            }
            
            // Load analytics
            async function loadAnalytics() {
                try {
                    const response = await fetch(`/api/publishing/analytics/${userId}?days=30`);
                    const data = await response.json();
                    
                    document.getElementById('totalPosts').textContent = data.total_posts;
                    document.getElementById('successRate').textContent = data.success_rate + '%';
                } catch (error) {
                    console.error('Error loading analytics:', error);
                }
            }
            
            // Initialize dashboard
            document.addEventListener('DOMContentLoaded', function() {
                loadPlatformStatus();
                loadScheduledPosts();
                loadAnalytics();
                
                // Set default schedule time to 1 hour from now
                const now = new Date();
                now.setHours(now.getHours() + 1);
                document.getElementById('scheduleTime').value = now.toISOString().slice(0, 16);
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/dashboard")
async def dashboard():
    """Ultra Premium Enterprise Dashboard - Next Gen UI"""
    with open('/Users/baba/AI CONTENT STUDIO/content-x-studio/new_dashboard.html', 'r') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    uptime = datetime.now(timezone.utc) - analytics_data["uptime_start"]
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "content-x-ai-studio",
        "version": "3.0.0",
        "uptime_seconds": int(uptime.total_seconds())
    }

# API Endpoints for functionality
@app.post("/api/scripts/generate")
async def generate_script_api(request: Request):
    """Generate AI script via API"""
    try:
        data = await request.json()
        topic = data.get("topic", "Content Creation")
        style = data.get("style", "professional")
        duration = data.get("duration", 60)
        
        # Generate script ID
        script_id = hashlib.md5(f"{topic}_{datetime.now(timezone.utc)}".encode()).hexdigest()[:12]
        
        # Simulate content generation
        await asyncio.sleep(2)  # Simulate processing time
        
        # Create script content
        script_content = f"""
        # {topic} - {style.title()} Script
        
        **Duration:** {duration} seconds
        **Style:** {style}
        **Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}
        
        ## Opening Hook
        Welcome to today's content about {topic}. This is going to be an amazing journey into {topic.lower()}.
        
        ## Main Content
        Let's dive deep into {topic}. Here are the key points we need to cover:
        
        1. **Introduction to {topic}**
        2. **Key concepts and strategies**
        3. **Practical applications**
        4. **Real-world examples**
        
        ## Call to Action
        If you found this content valuable, make sure to like, subscribe, and share!
        
        ## Closing
        Thank you for watching! See you in the next video.
        """
        
        # Store in analytics
        analytics_data["scripts_generated"] += 1
        analytics_data["total_requests"] += 1
        
        result = {
            "script_id": script_id,
            "topic": topic,
            "style": style,
            "duration": duration,
            "content": script_content.strip(),
            "status": "completed",
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error generating script: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/avatar/create")
async def create_avatar_api(request: Request):
    """Create 3D avatar from photos"""
    try:
        data = await request.json()
        user_id = data.get("user_id", "demo_user")
        photos = data.get("photos", [])
        video_samples = data.get("video_samples", [])
        
        # Generate avatar ID
        avatar_id = hashlib.md5(f"{user_id}_{datetime.now(timezone.utc)}".encode()).hexdigest()[:12]
        
        # Simulate avatar creation
        await asyncio.sleep(3)  # Simulate processing time
        
        # Create avatar result
        result = {
            "avatar_id": avatar_id,
            "user_id": user_id,
            "photos_processed": len(photos),
            "video_samples_processed": len(video_samples),
            "status": "completed",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "avatar_url": f"https://contentx-studio.s3.amazonaws.com/avatars/{avatar_id}.glb",
            "preview_url": f"https://contentx-studio.s3.amazonaws.com/avatars/{avatar_id}_preview.jpg"
        }
        
        # Store in analytics
        analytics_data["avatars_created"] += 1
        analytics_data["total_requests"] += 1
        
        return result
        
    except Exception as e:
        logger.error(f"Error creating avatar: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/video/generate")
async def generate_video_api(request: Request):
    """Generate video with avatar speaking"""
    try:
        data = await request.json()
        script_id = data.get("script_id", "")
        avatar_id = data.get("avatar_id", "")
        voice_id = data.get("voice_id", "")
        duration = data.get("duration", 60)
        
        # Generate video ID
        video_id = hashlib.md5(f"{script_id}_{avatar_id}_{datetime.now(timezone.utc)}".encode()).hexdigest()[:12]
        
        # Simulate video generation
        await asyncio.sleep(5)  # Simulate processing time
        
        # Create video result
        result = {
            "video_id": video_id,
            "script_id": script_id,
            "avatar_id": avatar_id,
            "voice_id": voice_id,
            "duration": duration,
            "status": "completed",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "video_url": f"https://contentx-studio.s3.amazonaws.com/videos/{video_id}.mp4",
            "thumbnail_url": f"https://contentx-studio.s3.amazonaws.com/videos/{video_id}_thumb.jpg"
        }
        
        # Store in analytics
        analytics_data["videos_generated"] += 1
        analytics_data["total_requests"] += 1
        
        return result
        
    except Exception as e:
        logger.error(f"Error generating video: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Content Creation API Endpoints
@app.post("/api/content/setup")
async def content_setup(
    user_id: str = Form(...),
    script_samples: List[UploadFile] = File(None),
    voice_samples: List[UploadFile] = File(None),
    avatar_files: List[UploadFile] = File(None)
):
    """Start content setup process with uploaded files"""
    if not CONTENT_BACKEND_AVAILABLE:
        return JSONResponse(
            status_code=503,
            content={"error": "Content backend not available"}
        )
    
    try:
        result = real_content_backend.setup_content(
            user_id=user_id,
            script_samples=script_samples,
            voice_samples=voice_samples,
            avatar_files=avatar_files
        )
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error in content setup: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Content setup failed: {str(e)}"}
        )

@app.get("/api/content/setup/status/{user_id}")
async def get_setup_status(user_id: str):
    """Get content setup status for user"""
    if not CONTENT_BACKEND_AVAILABLE:
        return JSONResponse(
            status_code=503,
            content={"error": "Content backend not available"}
        )
    
    try:
        status = real_content_backend.get_setup_status(user_id)
        
        return JSONResponse(content=status)
    except Exception as e:
        logger.error(f"Error getting setup status: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to get status: {str(e)}"}
        )

@app.post("/api/content/generate")
async def generate_content_with_ai(
    user_id: str = Form(...),
    script: str = Form(...),
    content_type: str = Form(...)
):
    """Generate content using user's trained AI models"""
    if not CONTENT_BACKEND_AVAILABLE:
        return JSONResponse(
            status_code=503,
            content={"error": "Content backend not available"}
        )
    
    try:
        result = await real_content_backend.generate_content(
            user_id=user_id,
            script=script,
            content_type=content_type
        )
        
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Content generation failed: {str(e)}"}
        )

@app.get("/api/content/generation/status/{job_id}")
async def get_generation_status(job_id: str):
    """Get status of content generation job"""
    if not CONTENT_BACKEND_AVAILABLE:
        return JSONResponse(
            status_code=503,
            content={"error": "Content backend not available"}
        )
    
    try:
        status = real_content_backend.get_generation_status(job_id)
        return JSONResponse(content=status)
    except Exception as e:
        logger.error(f"Error getting generation status: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to get status: {str(e)}"}
        )

@app.get("/api/content/backend/stats")
async def get_backend_stats():
    """Get backend statistics and model information"""
    if not CONTENT_BACKEND_AVAILABLE:
        return JSONResponse(
            status_code=503,
            content={"error": "Content backend not available"}
        )
    
    try:
        stats = real_content_backend.get_available_models()
        return JSONResponse(content=stats)
    except Exception as e:
        logger.error(f"Error getting backend stats: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to get stats: {str(e)}"}
        )

# ============================================================================

@app.post("/api/publishing/connect")
async def connect_platform(
    platform: str = Form(...),
    access_token: str = Form(...),
    user_id: str = Form(...)
):
    """Connect to a social media platform"""
    if not PUBLISHING_BACKEND_AVAILABLE:
        return JSONResponse(
            status_code=503,
            content={"error": "Publishing backend not available"}
        )
    
    try:
        result = publishing_backend.connect_platform(
            platform=platform,
            access_token=access_token,
            user_id=user_id
        )
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error connecting to platform: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to connect: {str(e)}"}
        )

@app.post("/api/publishing/schedule")
async def schedule_post(
    user_id: str = Form(...),
    content: str = Form(...),
    platforms: str = Form(...),
    schedule_time: str = Form(...),
    hashtags: str = Form(""),
    media_url: str = Form("")
):
    """Schedule a post across multiple platforms"""
    if not PUBLISHING_BACKEND_AVAILABLE:
        return JSONResponse(
            status_code=503,
            content={"error": "Publishing backend not available"}
        )
    
    try:
        result = publishing_backend.schedule_post(
            user_id=user_id,
            content=content,
            platforms=platforms.split(','),
            schedule_time=schedule_time,
            hashtags=hashtags.split(',') if hashtags else [],
            media_url=media_url
        )
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error scheduling post: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to schedule: {str(e)}"}
        )

@app.post("/api/publishing/publish")
async def publish_immediately(
    user_id: str = Form(...),
    content: str = Form(...),
    platforms: str = Form(...),
    hashtags: str = Form(""),
    media_url: str = Form("")
):
    """Publish content immediately across platforms"""
    if not PUBLISHING_BACKEND_AVAILABLE:
        return JSONResponse(
            status_code=503,
            content={"error": "Publishing backend not available"}
        )
    
    try:
        result = publishing_backend.publish_immediately(
            user_id=user_id,
            content=content,
            platforms=platforms.split(','),
            hashtags=hashtags.split(',') if hashtags else [],
            media_url=media_url
        )
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error publishing immediately: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to publish: {str(e)}"}
        )

@app.get("/api/publishing/status/{post_id}")
async def get_publishing_status(post_id: str):
    """Get status of a publishing job"""
    if not PUBLISHING_BACKEND_AVAILABLE:
        return JSONResponse(
            status_code=503,
            content={"error": "Publishing backend not available"}
        )
    
    try:
        status = publishing_backend.get_publishing_status(post_id)
        return JSONResponse(content=status)
        
    except Exception as e:
        logger.error(f"Error getting publishing status: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to get status: {str(e)}"}
        )

@app.get("/api/publishing/scheduled/{user_id}")
async def get_scheduled_posts(user_id: str):
    """Get all scheduled posts for a user"""
    if not PUBLISHING_BACKEND_AVAILABLE:
        return JSONResponse(
            status_code=503,
            content={"error": "Publishing backend not available"}
        )
    
    try:
        posts = publishing_backend.get_scheduled_posts(user_id)
        return JSONResponse(content={"posts": posts})
        
    except Exception as e:
        logger.error(f"Error getting scheduled posts: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to get posts: {str(e)}"}
        )

@app.get("/api/publishing/analytics/{user_id}")
async def get_publishing_analytics(user_id: str):
    """Get publishing analytics for a user"""
    try:
        if not PUBLISHING_BACKEND_AVAILABLE:
            return JSONResponse(
                status_code=503,
                content={"error": "Publishing backend not available"}
            )
        
        analytics = publishing_backend.get_analytics(user_id)
        return JSONResponse(content=analytics)
        
    except Exception as e:
        logger.error(f"Error getting publishing analytics: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to get analytics: {str(e)}"}
        )

@app.get("/api/content/optimization/stats")
async def get_optimization_stats():
    """Get optimization statistics and cost reductions"""
    try:
        # Get optimization stats from real content backend
        if real_content_backend:
            optimization_stats = real_content_backend.get_optimization_stats()
        else:
            optimization_stats = {
                "voice_cache_hits": 0,
                "batch_queue_size": 0,
                "active_jobs": 0,
                "optimizations_active": {
                    "batch_processing": False,
                    "smart_caching": False,
                    "gpu_acceleration": False,
                    "custom_models": False
                },
                "cost_reductions": {
                    "script_generation": "0%",
                    "voice_generation": "0%",
                    "video_processing": "0%",
                    "overall": "0%"
                }
            }
        
        # Add current cost analysis
        current_costs = {
            "script_generation": {
                "current_cost": "₹22",
                "optimized_cost": "₹8",
                "savings": "₹14 (64% reduction)"
            },
            "voice_generation": {
                "current_cost": "₹25",
                "optimized_cost": "₹10",
                "savings": "₹15 (60% reduction)"
            },
            "video_processing": {
                "current_cost": "₹45",
                "optimized_cost": "₹25",
                "savings": "₹20 (44% reduction)"
            },
            "overall_impact": {
                "monthly_savings": "₹6,75,000+",
                "processing_speed": "80% faster",
                "user_capacity": "300% increase",
                "profit_margin": "85%+ (from 81.7%)"
            }
        }
        
        return {
            "status": "success", 
            "optimization_stats": optimization_stats,
            "cost_analysis": current_costs,
            "next_level_opportunities": {
                "custom_ai_models": "₹50,000 investment → ₹2,00,000 monthly return",
                "batch_processing": "₹25,000 investment → ₹1,00,000 monthly return",
                "smart_caching": "₹15,000 investment → ₹75,000 monthly return",
                "gpu_acceleration": "₹1,00,000 investment → ₹3,00,000 monthly return"
            }
        }
    except Exception as e:
        logger.error(f"Error getting optimization stats: {str(e)}")
        return {"status": "error", "message": str(e)}

# ===== OAUTH AUTHENTICATION ENDPOINTS =====

@app.get("/api/auth/google")
async def google_oauth():
    """Initiate Google OAuth flow"""
    if not AUTH_BACKEND_AVAILABLE:
        return {"status": "error", "message": "Auth backend not available"}
    
    try:
        state = auth_backend.generate_oauth_state()
        oauth_url = await auth_backend.google_oauth_url(state)
        
        return {
            "status": "success",
            "oauth_url": oauth_url,
            "state": state
        }
    except Exception as e:
        logger.error(f"Error initiating Google OAuth: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/api/auth/linkedin")
async def linkedin_oauth():
    """Initiate LinkedIn OAuth flow"""
    if not AUTH_BACKEND_AVAILABLE:
        return {"status": "error", "message": "Auth backend not available"}
    
    try:
        state = auth_backend.generate_oauth_state()
        oauth_url = await auth_backend.linkedin_oauth_url(state)
        
        return {
            "status": "success",
            "oauth_url": oauth_url,
            "state": state
        }
    except Exception as e:
        logger.error(f"Error initiating LinkedIn OAuth: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/auth/callback")
async def oauth_callback(code: str = None, state: str = None, provider: str = "google"):
    """Handle OAuth callback"""
    if not AUTH_BACKEND_AVAILABLE:
        return {"status": "error", "message": "Auth backend not available"}
    
    try:
        if provider == "google":
            result = await auth_backend.handle_google_callback(code, state)
        elif provider == "linkedin":
            result = await auth_backend.handle_linkedin_callback(code, state)
        else:
            return {"status": "error", "message": "Invalid provider"}
        
        if result["status"] == "success":
            # Redirect to dashboard with token
            return HTMLResponse(content=f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Authentication Successful - Content X</title>
                <style>
                    body {{ 
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        min-height: 100vh;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin: 0;
                        color: white;
                    }}
                    .success-container {{
                        background: rgba(255, 255, 255, 0.1);
                        backdrop-filter: blur(20px);
                        border-radius: 20px;
                        padding: 3rem;
                        text-align: center;
                        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    }}
                    .success-icon {{
                        font-size: 4rem;
                        margin-bottom: 1rem;
                    }}
                    .btn {{
                        background: white;
                        color: #667eea;
                        padding: 1rem 2rem;
                        border: none;
                        border-radius: 50px;
                        font-weight: 600;
                        text-decoration: none;
                        display: inline-block;
                        margin-top: 1rem;
                        transition: transform 0.2s;
                    }}
                    .btn:hover {{ transform: translateY(-2px); }}
                </style>
            </head>
            <body>
                <div class="success-container">
                    <div class="success-icon">✅</div>
                    <h2>Welcome to Content X AI Studio!</h2>
                    <p>Authentication successful. Redirecting to dashboard...</p>
                    <a href="/dashboard" class="btn">Go to Dashboard</a>
                </div>
                <script>
                    // Store user data
                    localStorage.setItem('auth_token', '{result["token"]}');
                    localStorage.setItem('user_data', JSON.stringify({result["user"]}));
                    
                    // Redirect after 2 seconds
                    setTimeout(() => {{
                        window.location.href = '/dashboard';
                    }}, 2000);
                </script>
            </body>
            </html>
            """)
        else:
            return {"status": "error", "message": result.get("error", "Authentication failed")}
            
    except Exception as e:
        logger.error(f"Error handling OAuth callback: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/api/auth/register")
async def register_user(request: Request):
    """Register new user"""
    if not AUTH_BACKEND_AVAILABLE:
        return {"status": "error", "message": "Auth backend not available"}
    
    try:
        data = await request.json()
        email = data.get("email")
        name = data.get("name")
        password = data.get("password")
        
        if not all([email, name, password]):
            return {"status": "error", "message": "Missing required fields"}
        
        result = await auth_backend.create_user(email, name, password)
        return result
        
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/api/auth/login")
async def login_user(request: Request):
    """Login user"""
    if not AUTH_BACKEND_AVAILABLE:
        return {"status": "error", "message": "Auth backend not available"}
    
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")
        
        if not all([email, password]):
            return {"status": "error", "message": "Missing email or password"}
        
        result = await auth_backend.login_user(email, password)
        return result
        
    except Exception as e:
        logger.error(f"Error logging in user: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/api/auth/user")
async def get_current_user(request: Request):
    """Get current user info"""
    if not AUTH_BACKEND_AVAILABLE:
        return {"status": "error", "message": "Auth backend not available"}
    
    try:
        # Get token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return {"status": "error", "message": "No token provided"}
        
        token = auth_header.split(" ")[1]
        user = auth_backend.get_user_by_token(token)
        
        if not user:
            return {"status": "error", "message": "Invalid token"}
        
        return {
            "status": "success",
            "user": user
        }
        
    except Exception as e:
        logger.error(f"Error getting current user: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/api/auth/stats")
async def get_auth_stats():
    """Get authentication statistics"""
    if not AUTH_BACKEND_AVAILABLE:
        return {"status": "error", "message": "Auth backend not available"}
    
    try:
        stats = auth_backend.get_user_stats()
        return {
            "status": "success",
            "stats": stats
        }
    except Exception as e:
        logger.error(f"Error getting auth stats: {e}")
        return {"status": "error", "message": str(e)}

# ===== RAZORPAY PAYMENT ENDPOINTS =====

@app.post("/api/payments/create-customer")
async def create_customer(request: Request):
    """Create a new customer for payments"""
    if not PAYMENT_BACKEND_AVAILABLE:
        return JSONResponse(
            status_code=503,
            content={"success": False, "error": "Payment backend not available"}
        )
    
    try:
        data = await request.json()
        email = data.get("email")
        name = data.get("name")
        phone = data.get("phone")
        
        if not email or not name:
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "Email and name are required"}
            )
        
        result = razorpay_backend.create_customer(email, name, phone)
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error creating customer: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "Internal server error"}
        )

@app.post("/api/payments/create-payment-intent")
async def create_payment_intent(request: Request):
    """Create payment intent for subscription"""
    if not PAYMENT_BACKEND_AVAILABLE:
        return JSONResponse(
            status_code=503,
            content={"success": False, "error": "Payment backend not available"}
        )
    
    try:
        data = await request.json()
        customer_id = data.get("customer_id")
        plan_id = data.get("plan_id")
        quantity = data.get("quantity", 1)
        
        if not customer_id or not plan_id:
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "Customer ID and plan ID are required"}
            )
        
        result = razorpay_backend.create_payment_intent(customer_id, plan_id, quantity)
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error creating payment intent: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "Internal server error"}
        )

@app.post("/api/payments/verify-payment")
async def verify_payment(request: Request):
    """Verify payment after successful transaction"""
    if not PAYMENT_BACKEND_AVAILABLE:
        return JSONResponse(
            status_code=503,
            content={"success": False, "error": "Payment backend not available"}
        )
    
    try:
        data = await request.json()
        order_id = data.get("order_id")
        payment_id = data.get("payment_id")
        signature = data.get("signature")
        
        if not all([order_id, payment_id, signature]):
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "Order ID, payment ID, and signature are required"}
            )
        
        result = razorpay_backend.verify_payment(order_id, payment_id, signature)
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error verifying payment: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "Internal server error"}
        )

@app.get("/api/payments/plans")
async def get_pricing_plans():
    """Get all available pricing plans"""
    if not PAYMENT_BACKEND_AVAILABLE:
        return JSONResponse(
            status_code=503,
            content={"success": False, "error": "Payment backend not available"}
        )
    
    try:
        result = razorpay_backend.get_pricing_plans()
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error getting pricing plans: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "Internal server error"}
        )

@app.get("/api/payments/stats")
async def get_payment_stats():
    """Get payment backend statistics"""
    if not PAYMENT_BACKEND_AVAILABLE:
        return JSONResponse(
            status_code=503,
            content={"success": False, "error": "Payment backend not available"}
        )
    
    try:
        result = razorpay_backend.get_stats()
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error getting payment stats: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "Internal server error"}
        )

if __name__ == "__main__":
    logger.info("🚀 Starting Content X AI Studio...")
    logger.info("📡 Server will be available at: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
