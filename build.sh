#!/bin/bash
# Vercel build script for Billing System

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Build completed successfully!"
