#!/usr/bin/env bash
# Install Chrome và Chromedriver cho Render (dựa trên docs 2025)

# Cài dependencies hệ thống
apt-get update -y
apt-get install -y wget gnupg unzip xvfb

# Cài Google Chrome (headless version mới nhất 2025)
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
apt-get update -y
apt-get install -y google-chrome-stable

# Tải chromedriver tương thích (version 130+ cho Chrome 2025)
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+')
wget -q https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION%.*}
CHROMEDRIVER_VERSION=$(cat LATEST_RELEASE_${CHROME_VERSION%.*})
rm LATEST_RELEASE_${CHROME_VERSION%.*}
wget -q https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/local/bin/chromedriver
chmod +x /usr/local/bin/chromedriver

# Set PATH cho Chrome và driver
export PATH="/usr/bin/google-chrome:/usr/local/bin:$PATH"

# Xong build
echo "Chrome và Chromedriver đã cài xong!"
