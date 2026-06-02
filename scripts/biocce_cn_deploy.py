#!/usr/bin/env python3
"""
拜茨网站部署脚本 - 将网站文件上传到Cloudflare Pages
"""
import os
import sys
import json
import hashlib
import base64
import urllib.request
import urllib.parse
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

SITE_DIR = "E:/OneDrive/桌面/biocce-cn-site"
CLOUDFLARE_TOKEN = "cfut_NXQWWIBJh7QiBWmtMGKdqfpKdE3HHHxpNjfcF764a85111bd"
ACCOUNT_ID = "95d9539cf07fea1e74e63b77ad015f84"
PROJECT = "biocce-cn-site"

def upload_deployment():
    """通过Cloudflare API上传整个网站"""
    files = {}
    manifest = {}
    
    for root, dirs, fnames in os.walk(SITE_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules' and d != 'scripts' and d != '__pycache__']
        for fname in fnames:
            fpath = os.path.join(root, fname)
            relpath = os.path.relpath(fpath, SITE_DIR).replace('\\', '/')
            if relpath.startswith('.git/') or relpath == '.gitignore' or relpath.startswith('.wrangler'):
                continue
            with open(fpath, 'rb') as f:
                content = f.read()
            files[relpath] = base64.b64encode(content).decode('ascii')
            manifest[relpath] = hashlib.sha256(content).hexdigest()
    
    print(f"准备上传 {len(files)} 个文件...")
    
    # 用multipart form-data上传
    boundary = f"----WebKitFormBoundary{hashlib.md5(os.urandom(16)).hexdigest()}"
    body = b""
    
    for path, b64 in files.items():
        body += f"--{boundary}\r\n".encode()
        body += f'Content-Disposition: form-data; name="{path}"\r\n'.encode()
        ext = path.split('.')[-1].lower()
        mime_map = {
            'html': 'text/html', 'css': 'text/css', 'js': 'application/javascript',
            'json': 'application/json', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
            'png': 'image/png', 'svg': 'image/svg+xml', 'txt': 'text/plain',
            'xml': 'text/xml', 'ico': 'image/x-icon', 'pdf': 'application/pdf',
        }
        mime = mime_map.get(ext, 'application/octet-stream')
        body += f"Content-Type: {mime}\r\n\r\n".encode()
        body += base64.b64decode(b64)
        body += b"\r\n"
    
    body += f"--{boundary}\r\n".encode()
    body += 'Content-Disposition: form-data; name="manifest"\r\n'.encode()
    body += 'Content-Type: application/json\r\n\r\n'.encode()
    body += json.dumps(manifest).encode()
    body += f"\r\n--{boundary}--\r\n".encode()
    
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT}/deployments"
    req = urllib.request.Request(url, data=body)
    req.add_header("Authorization", f"Bearer {CLOUDFLARE_TOKEN}")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        result = json.loads(resp.read().decode())
        if result.get('success'):
            dep_id = result['result']['id'][:12]
            print(f"✅ 部署成功! ID: {dep_id}")
            pages_url = f"https://{PROJECT}.pages.dev"
            print(f"   访问地址: {pages_url}")
            return True
        else:
            print(f"❌ 部署失败: {result}")
            return False
    except Exception as e:
        print(f"❌ 部署异常: {e}")
        return False

if __name__ == "__main__":
    upload_deployment()
