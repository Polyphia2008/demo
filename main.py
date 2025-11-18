from flask import Flask, request, jsonify
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

app = Flask(__name__)

# Khởi tạo driver một lần khi start server
driver = None

def init_driver():
    global driver
    if driver is None:
        options = uc.ChromeOptions()
        options.add_argument('--headless')  # Chạy ẩn
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = uc.Chrome(options=options)
    return driver

@app.route('/api.php', methods=['GET'])
def check_username():
    username = request.args.get('username', '')
    
    if not username:
        return jsonify({
            'error': 'Username không được để trống',
            'usage': 'api.php?username=TenNguoiDung'
        }), 400
    
    api_url = 'https://manager.lqchecker.site/api/check'
    
    try:
        # Khởi tạo driver
        browser = init_driver()
        
        # Inject fetch request qua JavaScript
        script = f"""
        return fetch('{api_url}', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json',
            }},
            body: JSON.stringify({{username: '{username}'}})
        }})
        .then(response => response.text())
        .then(data => {{
            try {{
                return JSON.parse(data);
            }} catch(e) {{
                return data;
            }}
        }})
        .catch(err => ({{error: err.toString()}}));
        """
        
        # Navigate to the site first để có cookies
        browser.get('https://manager.lqchecker.site')
        time.sleep(3)  # Đợi Cloudflare challenge
        
        # Execute fetch request
        result = browser.execute_script(script)
        
        response = jsonify({
            'request': {
                'username': username,
                'api_url': api_url
            },
            'response': {
                'data': result
            }
        })
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response, 200
        
    except Exception as e:
        return jsonify({
            'error': f'Error: {str(e)}'
        }), 500

@app.route('/close', methods=['GET'])
def close_driver():
    """Endpoint để đóng browser khi cần"""
    global driver
    if driver:
        driver.quit()
        driver = None
        return jsonify({'message': 'Driver closed'})
    return jsonify({'message': 'No driver running'})

if __name__ == '__main__':
    # Chỉ chạy local thôi
    print("Server đang chạy tại: http://localhost:5000")
    print("Ví dụ: http://localhost:5000/api.php?username=ĐóiThìĐiNgủ")
    print("Để đóng browser: http://localhost:5000/close")
    app.run(debug=False, host='0.0.0.0', port=5000)
else:
    # Khi chạy trên Railway → dùng PORT của Railway và KHÔNG chạy debug
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
