#!/usr/bin/env python3
"""
拜茨清洁设备中文站 - 每日产品补充脚本
每天从凯驰(karcher.cn)爬取新产品，补充到拜茨网站
每次运行爬取所有品类的新产品，输出到 products-data.json
"""
import re, json, os, ssl, urllib.request
from html import unescape

ssl._create_default_https_context = ssl._create_unverified_context

SITE_DIR = r"E:/OneDrive/桌面/biocce-cn-site"

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
    ("扫地机", "手推式", "https://www.karcher.cn/cn/professional/sweepers-and-vacuum-sweepers/sweepers-and-vacuum-sweepers-walk-behind.html"),
    ("扫地机", "驾驶式", "https://www.karcher.cn/cn/professional/sweepers-and-vacuum-sweepers/vacuum-sweepers-ride-on.html"),
    ("蒸汽清洁机", "蒸汽清洁机", "https://www.karcher.cn/cn/professional/steam-cleaners-steam-vacuum-cleaners/steam-cleaners.html"),
    ("干冰清洗机", "干冰清洗机", "https://www.karcher.cn/cn/professional/dry-ice-cleaning.html"),
    ("地毯清洗机", "地毯清洗机", "https://www.karcher.cn/cn/professional/carpet-cleaner.html"),
]

# 精确匹配产品数据的正则
PROD_PATTERN = re.compile(
    r'"id":(\d+),"name":"([^"]*)","partnumber":"(\d+)",'
    r'"image":"([^"]*)","description":"([^"]*)","url":"([^"]*)","type":"([^"]*)"'
)

def fetch_html(url):
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml',
        })
        resp = urllib.request.urlopen(req, timeout=30)
        html = resp.read().decode('utf-8', errors='replace')
        return html
    except Exception as e:
        print(f"  [ERROR] {url}: {e}")
        return None

def extract_products(html):
    """从HTML提取产品数据"""
    products = []
    for m in PROD_PATTERN.finditer(html):
        products.append({
            "id": int(m.group(1)),
            "name": m.group(2).replace('\\/', '/').replace('\\u', '\\u'),  # 保留unicode
            "partnumber": m.group(3),
            "image_url": m.group(4).replace('\\/', '/'),
            "description_raw": m.group(5).replace('\\/', '/'),
            "url": m.group(6).replace('\\/', '/'),
            "type": m.group(7),
        })
    return products

def decode_unicode(s):
    """解码unicode转义"""
    return s.encode('utf-8').decode('unicode_escape') if '\\u' in s else s

def extract_price(desc):
    m = re.search(r'建议零售价[：:]\s*[￥¥]?([\d,]+\.\d{2})', desc)
    return f"¥{m.group(1)}" if m else None

def download_image(url, save_path):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=30)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(resp.read())
        return True
    except Exception as e:
        print(f"    [IMG FAIL] {e}")
        return False

def make_slug(name):
    slug = name.split('*')[0].strip().lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    return slug

def main():
    print("=" * 60)
    print("拜茨清洁设备 - 每日产品补充脚本")
    print("=" * 60)

    data_path = os.path.join(SITE_DIR, "products-data.json")
    existing = {}
    if os.path.exists(data_path):
        with open(data_path, 'r', encoding='utf-8') as f:
            for p in json.load(f):
                existing[p['partnumber']] = p

    print(f"当前已有产品: {len(existing)} 个")
    new_count = 0

    for category, subcat, url in CATEGORY_URLS:
        print(f"\n[{category}] {subcat}...", end=" ", flush=True)
        html = fetch_html(url)
        if not html:
            print("FAIL")
            continue

        raw = extract_products(html)
        if not raw:
            print("无产品")
            continue

        print(f"{len(raw)}个", end="", flush=True)

        for rp in raw:
            pn = rp['partnumber']
            if pn in existing:
                continue

            desc = decode_unicode(rp['description_raw'])
            name = decode_unicode(rp['name'])
            slug = make_slug(name)
            price = extract_price(desc) or "咨询报价"
            img_name = f"{slug}.jpg"
            img_local = os.path.join(SITE_DIR, "images", "products", img_name)

            product = {
                "id": rp['id'],
                "name": name,
                "model": name.split('*')[0].strip() if '*' in name else name,
                "partnumber": pn,
                "category": category,
                "subcategory": subcat,
                "image": f"images/products/{img_name}",
                "price": price,
                "description": desc,
                "specs": {},
                "slug": slug,
            }

            # 下载图片
            if rp['image_url']:
                if download_image(rp['image_url'], img_local):
                    print(f" [+{name}]", end="", flush=True)

            existing[pn] = product
            new_count += 1

    # 写入
    all_products = list(existing.values())
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(all_products, f, ensure_ascii=False, indent=2)

    print(f"\n\n{'=' * 60}")
    print(f"本次新增: {new_count} 个")
    print(f"累计总数: {len(all_products)} 个")
    return new_count

if __name__ == "__main__":
    main()
