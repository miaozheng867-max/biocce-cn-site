#!/usr/bin/env python3
"""
拜茨中文站 - 每日自动补充产品 + 部署
"""
import sys, os, json, hashlib, base64, re, ssl, urllib.request
from html import unescape
from datetime import datetime

ssl._create_default_https_context = ssl._create_unverified_context

SITE_DIR = r"E:/OneDrive/桌面/biocce-cn-site"
CF_TOKEN = "cfut_NXQWWIBJh7QiBWmtMGKdqfpKdE3HHHxpNjfcF764a85111bd"
CF_ACCOUNT = "95d9539cf07fea1e74e63b77ad015f84"
CF_PROJECT = "biocce-cn-site"
MAX_NEW = 15  # 每次最多新增15个

CATEGORY_URLS = [
    ("洗地机/洗地吸干机", "紧凑式手推式洗地机", "https://www.karcher.cn/cn/professional/floor-scrubbers-scrubber-driers/compact-push-scrubber-driers.html"),
    ("洗地机/洗地吸干机", "手推式洗地吸干机", "https://www.karcher.cn/cn/professional/floor-scrubbers-scrubber-driers/walk-behind-scrubber-driers.html"),
    ("洗地机/洗地吸干机", "驾驶式/站立式洗地吸干机", "https://www.karcher.cn/cn/professional/floor-scrubbers-scrubber-driers/ride-on-step-on-scrubber-driers.html"),
    ("高压清洗机", "冷水-超级型", "https://www.karcher.cn/cn/professional/high-pressure-cleaners/cold-water-high-pressure-cleaners/super-class.html"),
    ("高压清洗机", "冷水-中级型", "https://www.karcher.cn/cn/professional/high-pressure-cleaners/cold-water-high-pressure-cleaners/middle-class.html"),
    ("高压清洗机", "冷水-紧凑型", "https://www.karcher.cn/cn/professional/high-pressure-cleaners/cold-water-high-pressure-cleaners/compact-class.html"),
    ("高压清洗机", "热水-超级型", "https://www.karcher.cn/cn/professional/high-pressure-cleaners/hot-water-high-pressure-cleaners/super-class.html"),
    ("高压清洗机", "热水-中级型", "https://www.karcher.cn/cn/professional/high-pressure-cleaners/hot-water-high-pressure-cleaners/middle-class.html"),
    ("真空吸尘器", "干湿两用-Tact", "https://www.karcher.cn/cn/professional/vacuums/wet-and-dry-vacuum-cleaners/tact-class.html"),
    ("真空吸尘器", "干湿两用-Standard", "https://www.karcher.cn/cn/professional/vacuums/wet-and-dry-vacuum-cleaners/standard-class.html"),
    ("真空吸尘器", "干湿两用-AP", "https://www.karcher.cn/cn/professional/vacuums/wet-and-dry-vacuum-cleaners/ap-class.html"),
    ("扫地机", "驾驶式", "https://www.karcher.cn/cn/professional/sweepers-and-vacuum-sweepers/vacuum-sweepers-ride-on.html"),
    ("蒸汽清洁机", "蒸汽清洁机", "https://www.karcher.cn/cn/professional/steam-cleaners-steam-vacuum-cleaners/steam-cleaners.html"),
    ("干冰清洗机", "干冰清洗机", "https://www.karcher.cn/cn/professional/dry-ice-cleaning.html"),
]

PROD_PATTERN = re.compile(
    r'"id":(\d+),"name":"([^"]*)","partnumber":"(\d+)",'
    r'"image":"([^"]*)","description":"([^"]*)","url":"([^"]*)","type":"([^"]*)"'
)

def fetch_html(url):
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        })
        resp = urllib.request.urlopen(req, timeout=30)
        return resp.read().decode('utf-8', errors='replace')
    except:
        return None

def extract_products(html):
    products = []
    for m in PROD_PATTERN.finditer(html):
        products.append({
            "id": int(m.group(1)),
            "name": m.group(2),
            "partnumber": m.group(3),
            "image_url": m.group(4).replace('\\/', '/'),
            "description_raw": m.group(5),
            "url": m.group(6).replace('\\/', '/'),
        })
    return products

def decode(s):
    if '\\u' in s:
        return s.encode('utf-8').decode('unicode_escape')
    return s

def extract_price(desc):
    m = re.search(r'建议零售价[：:]\s*[￥¥]?([\d,]+\.\d{2})', desc)
    if m:
        return f"¥{m.group(1)}"
    return None

def make_slug(name):
    slug = name.split('*')[0].strip().lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    return slug

def download_image(url, save_path):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=30)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(resp.read())
        return True
    except:
        return False

def deploy():
    """上传到Cloudflare Pages"""
    files = {}
    manifest = {}
    for root, dirs, fnames in os.walk(SITE_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules' and d != 'scripts' and d != '__pycache__' and d != '.git']
        for fname in fnames:
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, SITE_DIR).replace('\\', '/')
            if rel.startswith('.git/') or rel in ('.gitignore',):
                continue
            with open(fpath, 'rb') as f:
                content = f.read()
            files[rel] = base64.b64encode(content).decode('ascii')
            manifest[rel] = hashlib.sha256(content).hexdigest()
    
    import uuid
    boundary = str(uuid.uuid4())
    body_parts = []
    for path, b64 in files.items():
        ext = path.split('.')[-1].lower()
        mime_map = {'html':'text/html','css':'text/css','js':'application/javascript','json':'application/json',
                    'jpg':'image/jpeg','jpeg':'image/jpeg','png':'image/png','svg':'image/svg+xml',
                    'txt':'text/plain','xml':'text/xml','ico':'image/x-icon'}
        mime = mime_map.get(ext, 'application/octet-stream')
        body_parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{path}"\r\nContent-Type: {mime}\r\n\r\n'.encode() + base64.b64decode(b64) + b'\r\n')
    body_parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="manifest"\r\nContent-Type: application/json\r\n\r\n'.encode() + json.dumps(manifest).encode() + f'\r\n--{boundary}--\r\n'.encode())
    
    body = b''.join(body_parts)
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/pages/projects/{CF_PROJECT}/deployments"
    req = urllib.request.Request(url, body)
    req.add_header("Authorization", f"Bearer {CF_TOKEN}")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    
    try:
        resp = urllib.request.urlopen(req, timeout=180)
        result = json.loads(resp.read().decode())
        if result.get('success'):
            print(f"✅ 部署成功! pages.dev/{CF_PROJECT}")
            return True
        else:
            print(f"❌ 部署失败: {result.get('errors','')}")
            return False
    except Exception as e:
        print(f"❌ 部署异常: {e}")
        return False

def main():
    print("=" * 60)
    print(f"拜茨清洁设备 - 每日补充 [{datetime.now().strftime('%Y-%m-%d %H:%M')}]")
    print("=" * 60)
    
    data_path = os.path.join(SITE_DIR, "products-data.json")
    existing = {}
    if os.path.exists(data_path):
        with open(data_path, 'r', encoding='utf-8') as f:
            for p in json.load(f):
                existing[p['partnumber']] = p
    print(f"当前: {len(existing)} 个产品\n")
    
    new_count = 0
    for cat, subcat, url in CATEGORY_URLS:
        if new_count >= MAX_NEW:
            break
        print(f"[{cat}] {subcat}...", end=" ", flush=True)
        html = fetch_html(url)
        if not html:
            print("超时")
            continue
        raw = extract_products(html)
        if not raw:
            print("无")
            continue
        print(f"{len(raw)}个", end=" ")
        
        for rp in raw:
            if new_count >= MAX_NEW:
                break
            pn = rp['partnumber']
            if pn in existing:
                continue
            desc = decode(rp['description_raw'])
            name = decode(rp['name'])
            slug = make_slug(name)
            price = extract_price(desc) or "咨询报价"
            img_name = f"{slug}.jpg"
            img_local = os.path.join(SITE_DIR, "images", "products", img_name)
            
            product = {
                "id": rp['id'], "name": name,
                "model": name.split('*')[0].strip() if '*' in name else name,
                "partnumber": pn, "category": cat, "subcategory": subcat,
                "image": f"images/products/{img_name}",
                "price": price, "description": desc, "specs": {},
                "slug": slug,
            }
            if rp['image_url'] and download_image(rp['image_url'], img_local):
                print(f"+{name}", end=" ", flush=True)
            existing[pn] = product
            new_count += 1
        print()
    
    all_p = list(existing.values())
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(all_p, f, ensure_ascii=False, indent=2)
    
    print(f"\n新增: {new_count} 个, 累计: {len(all_p)} 个")
    
    if new_count > 0:
        print("\n部署中...")
        deploy()
    
    return new_count

if __name__ == "__main__":
    main()
