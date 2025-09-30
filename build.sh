#!/bin/bash

# Full Stack Content X AI Studio Build Script for Render
echo "🚀 Building Full Stack Content X AI Studio..."

# Update pip
pip install --upgrade pip

# Install system dependencies for AI/ML packages
apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgthread-2.0-0 \
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libfontconfig1 \
    libice6 \
    libx11-6 \
    libxau6 \
    libxdmcp6 \
    libxcb1 \
    libxss1 \
    libxt6 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt

echo "✅ Full Stack build completed successfully!"
