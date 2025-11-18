#!/usr/bin/env bash
set -e

# Tải chromedriver tương thích với Chromium trên Render (version 130+ cho 2025)
cd /tmp
wget -q https://chromedriver.storage.googleapis.com/LATEST_RELEASE_130
CHROMEDRIVER_VERSION=$(cat LATEST_RELEASE_130)
wget -q https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/chromedriver
sudo chmod +x /usr/local/bin/chromedriver

# Set PATH
export PATH="/usr/local/bin:$PATH"

echo "Chromedriver installed successfully!"
