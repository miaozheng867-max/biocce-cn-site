#!/usr/bin/env python3
"""
生成拜茨中文站产品层级页面：
产品中心 → 分类 → 小类 → 产品详情
"""
import json, os, re

BASE = r"E:\OneDrive\桌面\biocce-cn-site"
DATA = os.path.join(BASE, "products-data.json")

with open(DATA, "r", encoding="utf-8") as f:
    products = json.load(f)

CATEGORIES = [
    {"id": "scrubbers", "name": "洗地机/洗地吸干机", "catKey": "洗地机/洗地吸干机",
     "desc": "从紧凑型手推式到驾驶式，满足不同面积的商业和工业地面清洁需求。"},
    {"id": "pressure-washers", "name": "高压清洗机", "catKey": "高压清洗机",
     "desc": "冷水、热水及超高压清洗机，适用于工业设备、建筑、车辆等重污垢清洗。"},
    {"id": "vacuums", "name": "工业吸尘器", "catKey": "真空吸尘器",
     "desc": "专业干湿两用吸尘器，多级别过滤，适用于工厂、仓库等环境的深度清洁。"},
    {"id": "sweepers", "name": "扫地机", "catKey": "扫地机",
     "desc": "工业级扫地车，手推式及驾驶式，适用于大面积场地、厂区、道路清扫。"},
    {"id": "steam-cleaners", "name": "蒸汽清洁机", "catKey": "蒸汽清洁机",
     "desc": "高温蒸汽深度清洁，无需化学药剂，适用于食品加工、厨房、医疗等高卫生要求场所。"},
    {"id": "dry-ice", "name": "干冰清洗机", "catKey": "干冰清洗机",
     "desc": "现代化干冰清洗技术，快速高效无损清洗，适用于模具、电子、食品等行业。"},
]

# SVG icons (simplified)
SOCIAL_ICONS = """
    <a href="https://www.facebook.com/profile.php?id=61590473731923" target="_blank" class="social-icon" aria-label="Facebook"><svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg></a>
    <a href="https://www.linkedin.com/company/biocce" target="_blank" class="social-icon" aria-label="LinkedIn"><svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>
    <a href="https://www.youtube.com/@baici" target="_blank" class="social-icon" aria-label="YouTube"><svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg></a>
    <a href="https://www.instagram.com/biocce_cleaning" target="_blank" class="social-icon" aria-label="Instagram"><svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg></a>
    <a href="https://www.tiktok.com/@biocce" target="_blank" class="social-icon" aria-label="TikTok"><svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg></a>
"""

# Common footer HTML
def footer(cats):
    cat_links = "\n".join(f'        <li><a href="/products/category-{c["id"]}.html">{c["name"]}</a></li>' for c in cats)
    return f"""
<footer>
  <div class="footer-inner">
    <div>
      <h3>拜茨清洁设备</h3>
      <p>拜茨清洁设备专注为工商业客户提供清洁设备与清洁用品一站式解决方案。专业服务，品质保障。</p>
    </div>
    <div>
      <h4>快速链接</h4>
      <ul>
        <li><a href="/">首页</a></li>
        <li><a href="/products-categories.html">产品中心</a></li>
        <li><a href="/about">关于我们</a></li>
        <li><a href="/services">服务支持</a></li>
        <li><a href="/contact">联系我们</a></li>
      </ul>
    </div>
    <div>
      <h4>产品分类</h4>
      <ul>
{cat_links}
      </ul>
    </div>
    <div>
      <h4>联系方式</h4>
      <ul class="contact">
        <li>上海市 · 拜茨清洁设备</li>
        <li><a href="mailto:info@biocce.cn">info@biocce.cn</a></li>
        <li>咨询热线：021-xxxxxxx</li>
        <li><a href="/contact">在线留言 &rarr;</a></li>
      </ul>
    </div>
  </div>
  <div class="social-map-section">
    <div class="social-links">
      <h4>关注我们</h4>
      <div class="social-icons">
{SOCIAL_ICONS}
      </div>
    </div>
    <div class="map-container">
      <h4>公司位置</h4>
      <div class="map-embed">
        <a href="https://maps.google.com/?q=Shanghai+China" target="_blank" rel="noopener noreferrer" class="map-link">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" style="vertical-align:middle;margin-right:6px"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 010-5 2.5 2.5 0 010 5z"/></svg>
          上海市 — 点击查看地图
        </a>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <span>&copy; 2026 上海拜茨清洁设备有限公司 版权所有</span>
    <span><a href="/">www.biocce.cn</a></span>
  </div>
</footer>
"""

# Common nav
NAV = """
<nav>
  <div class="nav-inner">
    <a href="/" class="nav-left">
      <div class="logo-mark">拜</div>
      <span class="logo-text">拜茨清洁</span>
    </a>
    <ul class="nav-right" id="navR">
      <li><a href="/">首页</a></li>
      <li><a href="/products-categories.html" class="active">产品中心</a></li>
      <li><a href="/about">关于我们</a></li>
      <li><a href="/services">服务支持</a></li>
      <li><a href="/insights">资讯动态</a></li>
      <li><a href="/contact" class="nav-cta">联系我们</a></li>
    </ul>
    <button class="hamburger" id="ham" aria-label="切换菜单">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>
"""

COMMON_CSS = """
:root{--primary:#1A3A4A;--accent:#C9A84C;--text:#1A1A1A;--text-secondary:#5a6a7a;--text-light:#8a9aa8;--border:#e8ecf0;--card:#fff;--bg:#FAFAF8}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,'Noto Sans SC',sans-serif;background:var(--bg);color:var(--text)}
.page-wrap{padding-top:64px;flex:1}
.breadcrumb{max-width:1200px;margin:0 auto;padding:20px 24px 0;font-size:14px;color:var(--text-light)}
.breadcrumb a{color:var(--text-light);text-decoration:none}
.breadcrumb a:hover{color:var(--primary)}
.breadcrumb .sep{color:#ccc;margin:0 8px}
.breadcrumb .current{color:var(--primary);font-weight:500}
.content{max-width:1200px;margin:0 auto;padding:24px 24px 48px}
"""

COMMON_SCRIPT = """
<script>
document.getElementById("ham").onclick=function(){document.getElementById("navR").classList.toggle("open");this.classList.toggle("active")};
var nls=document.querySelectorAll(".nav-right a");for(var i=0;i<nls.length;i++)nls[i].onclick=function(){document.getElementById("navR").classList.remove("open");document.getElementById("ham").classList.remove("active")};
</script>
"""

def get_subs(cat_key):
    """Get subcategories for a category key"""
    m = {}
    for p in products:
        if p["category"] == cat_key:
            s = p["subcategory"]
            if s not in m:
                m[s] = []
            m[s].append(p)
    return m

def img_src(p):
    if p["image"]:
        if p["image"].startswith("http"):
            return p["image"]
        else:
            return "/" + p["image"]
    return ""

def specs_html(p):
    keys = list(p["specs"].keys())
    if len(keys) == 0:
        return '<span>联系客服获取参数</span>'
    top3 = keys[:3]
    return "".join(f'<span>{k}: {p["specs"][k]}</span>' for k in top3)

def subcat_slug(name):
    s = name.replace("/", "-").replace("\\", "-").replace(" ", "-").replace("(", "").replace(")", "")
    s = re.sub(r"-+", "-", s)
    s = s.strip("-")
    return s

# ==================== GENERATE ====================


# Ensure directories
prod_dir = os.path.join(BASE, "products")
for cat in CATEGORIES:
    os.makedirs(os.path.join(prod_dir, f"category-{cat['id']}"), exist_ok=True)

# ---- Product Overview Page ---- 
overview = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>产品中心 | 拜茨清洁设备 — 清洁设备与清洁用品一站式解决方案</title>
<meta name="description" content="拜茨清洁设备产品中心 — 洗地机、高压清洗机、工业吸尘器、扫地机、蒸汽清洁机、干冰清洗机等全系列工商业清洁设备。">
<link rel="canonical" href="https://www.biocce.cn/products-categories.html">
<meta property="og:title" content="产品中心 | 拜茨清洁设备">
<meta property="og:description" content="拜茨清洁设备 — 洗地机、高压清洗机、工业吸尘器、扫地机、蒸汽清洁机、干冰清洗机等全系列工商业清洁设备。">
<meta property="og:url" content="https://www.biocce.cn/products-categories.html">
<!-- Google tag -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-8TF95LBYRV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-8TF95LBYRV');</script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="design-system.css">
<style>
{COMMON_CSS}
.page-header{{max-width:1200px;margin:0 auto;padding:32px 24px 8px;text-align:center}}
.page-header h1{{font-size:32px;font-weight:700;margin-bottom:12px}}
.page-header p{{font-size:16px;color:var(--text-secondary);max-width:600px;margin:0 auto;line-height:1.6}}
.cat-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(350px,1fr));gap:24px}}
.cat-card{{background:var(--card);border-radius:16px;overflow:hidden;border:1px solid var(--border);text-decoration:none;color:inherit;display:flex;flex-direction:column;transition:all .35s cubic-bezier(.25,.8,.25,1);box-shadow:0 1px 4px rgba(0,0,0,.04)}}
.cat-card:hover{{transform:translateY(-6px);box-shadow:0 12px 40px rgba(26,58,74,.12)}}
.cat-img-wrap{{aspect-ratio:16/9;background:linear-gradient(145deg,#f0f2f5,#e8ecf0);display:flex;align-items:center;justify-content:center;overflow:hidden}}
.cat-img-wrap img{{max-width:70%;max-height:75%;object-fit:contain;filter:drop-shadow(0 4px 12px rgba(0,0,0,.1));transition:transform .4s}}
.cat-card:hover .cat-img-wrap img{{transform:scale(1.08)}}
.cat-placeholder{{font-size:56px;color:var(--text-light);opacity:.3}}
.cat-info{{padding:24px;display:flex;flex-direction:column;flex:1}}
.cat-info h3{{font-size:20px;font-weight:600;margin-bottom:8px;color:var(--text)}}
.cat-info p{{font-size:14px;color:var(--text-secondary);line-height:1.5;margin-bottom:12px;flex:1}}
.cat-meta{{font-size:13px;color:var(--text-light);margin-bottom:14px}}
.cat-link{{font-size:14px;font-weight:600;color:var(--primary);display:inline-flex;align-items:center;gap:4px;transition:gap .2s}}
.cat-card:hover .cat-link{{gap:8px}}
@media(max-width:768px){{.cat-grid{{grid-template-columns:1fr}}.page-header h1{{font-size:26px}}}}
</style>
</head>
<body>
{NAV}
<div class="page-wrap">
  <div class="breadcrumb"><a href="/">首页</a><span class="sep">›</span><span class="current">产品中心</span></div>
  <div class="page-header">
    <h1>产品中心</h1>
    <p>拜茨清洁设备提供全系列工商业清洁设备与清洁用品，按产品分类浏览，快速找到适合您的设备。</p>
  </div>
  <div class="content">
    <div class="cat-grid">
"""

for cat in CATEGORIES:
    subs = get_subs(cat["catKey"])
    total_count = sum(len(v) for v in subs.values())
    sub_count = len(subs)
    first_sub_items = list(subs.values())[0] if subs else []
    first_item = first_sub_items[0] if first_sub_items else None
    img = img_src(first_item) if first_item else ""

    overview += f"""
      <a href="/products/category-{cat['id']}.html" class="cat-card">
        <div class="cat-img-wrap">
          {f'<img src="{img}" alt="{cat["name"]}" loading="lazy">' if img else f'<div class="cat-placeholder">{cat["name"][0]}</div>'}
        </div>
        <div class="cat-info">
          <h3>{cat['name']}</h3>
          <p>{cat['desc']}</p>
          <div class="cat-meta">{sub_count} 个子分类 · {total_count} 款产品</div>
          <span class="cat-link">浏览 {cat['name']} &rarr;</span>
        </div>
      </a>"""

overview += """
    </div>
  </div>
</div>
""" + footer(CATEGORIES) + COMMON_SCRIPT + """
</body>
</html>"""

with open(os.path.join(BASE, "products-categories.html"), "w", encoding="utf-8") as f:
    f.write(overview)
print("✅ products-categories.html")

# ---- Category Pages ---- 
for cat in CATEGORIES:
    subs = get_subs(cat["catKey"])
    total_count = sum(len(v) for v in subs.values())

    sub_cards = ""
    for sub_name, items in subs.items():
        sslug = subcat_slug(sub_name)
        first_item = items[0]
        img = img_src(first_item)
        count = len(items)

        sub_cards += f"""
      <a href="category-{cat['id']}/subcat-{sslug}.html" class="subcat-card">
        <div class="subcat-img-wrap">
          {f'<img src="{img}" alt="{sub_name}" loading="lazy">' if img else f'<div class="subcat-placeholder">{sub_name[0]}</div>'}
        </div>
        <div class="subcat-info">
          <h3>{sub_name}</h3>
          <span class="subcat-count">{count} 款产品</span>
          <span class="subcat-link">查看产品 &rarr;</span>
        </div>
      </a>"""

    page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{cat['name']} | 拜茨清洁设备</title>
<meta name="description" content="拜茨清洁设备提供{cat['name']}全系列产品。{cat['desc']}">
<link rel="canonical" href="https://www.biocce.cn/products/category-{cat['id']}.html">
<meta property="og:title" content="{cat['name']} | 拜茨清洁设备">
<meta property="og:description" content="拜茨清洁设备提供{cat['name']}全系列产品。{cat['desc']}">
<meta property="og:url" content="https://www.biocce.cn/products/category-{cat['id']}.html">
<!-- Google tag -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-8TF95LBYRV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-8TF95LBYRV');</script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/design-system.css">
<style>
{COMMON_CSS}
body{{min-height:100vh}}
.page-header{{max-width:1200px;margin:0 auto;padding:32px 24px 8px}}
.page-header h1{{font-size:28px;font-weight:700;margin-bottom:8px;color:var(--text)}}
.page-header p{{font-size:16px;color:var(--text-secondary);max-width:700px;line-height:1.6}}
.page-header .count{{font-size:14px;color:var(--text-light);margin-top:8px}}
.subcat-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:24px}}
.subcat-card{{background:var(--card);border-radius:16px;overflow:hidden;border:1px solid var(--border);text-decoration:none;color:inherit;display:flex;flex-direction:column;transition:all .35s cubic-bezier(.25,.8,.25,1);box-shadow:0 1px 4px rgba(0,0,0,.04)}}
.subcat-card:hover{{transform:translateY(-6px);box-shadow:0 12px 40px rgba(26,58,74,.12)}}
.subcat-img-wrap{{aspect-ratio:16/9;background:linear-gradient(145deg,#f3f4f6,#eef0f3);display:flex;align-items:center;justify-content:center;overflow:hidden}}
.subcat-img-wrap img{{max-width:75%;max-height:80%;object-fit:contain;filter:drop-shadow(0 4px 12px rgba(0,0,0,.1));transition:transform .4s}}
.subcat-card:hover .subcat-img-wrap img{{transform:scale(1.05)}}
.subcat-placeholder{{font-size:48px;color:var(--text-light);opacity:.4}}
.subcat-info{{padding:20px;display:flex;flex-direction:column;flex:1}}
.subcat-info h3{{font-size:18px;font-weight:600;margin-bottom:6px;color:var(--text)}}
.subcat-count{{font-size:13px;color:var(--text-light);margin-bottom:12px}}
.subcat-link{{font-size:14px;font-weight:600;color:var(--primary);display:inline-flex;align-items:center;gap:4px;margin-top:auto;transition:gap .2s}}
.subcat-card:hover .subcat-link{{gap:8px}}
@media(max-width:768px){{.subcat-grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
{NAV}
<div class="page-wrap">
  <div class="breadcrumb"><a href="/">首页</a><span class="sep">›</span><a href="/products-categories.html">产品中心</a><span class="sep">›</span><span class="current">{cat['name']}</span></div>
  <div class="page-header">
    <h1>{cat['name']}</h1>
    <p>{cat['desc']}</p>
    <div class="count">共 {total_count} 款产品，按类型分类展示</div>
  </div>
  <div class="content">
    <div class="subcat-grid">{sub_cards}
    </div>
  </div>
</div>
""" + footer(CATEGORIES) + COMMON_SCRIPT + """
</body>
</html>"""

    with open(os.path.join(prod_dir, f"category-{cat['id']}.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print(f"✅ products/category-{cat['id']}.html ({total_count} 款, {len(subs)} 个小类)")

# ---- Subcategory Pages ---- 
for cat in CATEGORIES:
    subs = get_subs(cat["catKey"])
    for sub_name, items in subs.items():
        sslug = subcat_slug(sub_name)

        product_cards = ""
        for p in items:
            img = img_src(p)
            specs = specs_html(p)
            product_cards += f"""
      <a href="/product/{p['slug']}.html" class="product-card">
        <div class="product-img-wrap">
          {f'<img src="{img}" alt="{p["model"]}" loading="lazy">' if img else f'<div class="product-placeholder">{p["model"][0]}</div>'}
        </div>
        <div class="product-info">
          <h3>{p['model']}</h3>
          <div class="product-price">{p['price']}</div>
          <div class="product-specs">{specs}</div>
          <span class="product-link">查看详情 &rarr;</span>
        </div>
      </a>"""

        page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{sub_name} | {cat['name']} | 拜茨清洁设备</title>
<meta name="description" content="拜茨清洁设备{cat['name']} — {sub_name}，共{len(items)}款产品，适用于工商业清洁。">
<link rel="canonical" href="https://www.biocce.cn/products/category-{cat['id']}/subcat-{sslug}.html">
<meta property="og:title" content="{sub_name} | {cat['name']} | 拜茨清洁设备">
<meta property="og:description" content="拜茨清洁设备{cat['name']} — {sub_name}，共{len(items)}款产品。">
<meta property="og:url" content="https://www.biocce.cn/products/category-{cat['id']}/subcat-{sslug}.html">
<!-- Google tag -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-8TF95LBYRV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-8TF95LBYRV');</script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/design-system.css">
<style>
{COMMON_CSS}
body{{min-height:100vh;display:flex;flex-direction:column}}
.page-header{{max-width:1200px;margin:0 auto;padding:32px 24px 8px}}
.page-header h1{{font-size:28px;font-weight:700;margin-bottom:8px}}
.page-header p{{font-size:16px;color:var(--text-secondary);max-width:700px;line-height:1.6}}
.page-header .count{{font-size:14px;color:var(--text-light);margin-top:8px}}
.product-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:24px}}
.product-card{{background:var(--card);border-radius:16px;overflow:hidden;border:1px solid var(--border);text-decoration:none;color:inherit;display:flex;flex-direction:column;transition:all .35s cubic-bezier(.25,.8,.25,1);box-shadow:0 1px 4px rgba(0,0,0,.04)}}
.product-card:hover{{transform:translateY(-6px);box-shadow:0 12px 40px rgba(26,58,74,.12)}}
.product-img-wrap{{aspect-ratio:4/3;background:linear-gradient(145deg,#f3f4f6,#eef0f3);display:flex;align-items:center;justify-content:center;overflow:hidden}}
.product-img-wrap img{{max-width:80%;max-height:85%;object-fit:contain;filter:drop-shadow(0 4px 12px rgba(0,0,0,.1));transition:transform .4s}}
.product-card:hover .product-img-wrap img{{transform:scale(1.05)}}
.product-placeholder{{font-size:48px;color:var(--text-light);opacity:.4}}
.product-info{{padding:20px;display:flex;flex-direction:column;flex:1}}
.product-info h3{{font-size:17px;font-weight:600;margin-bottom:6px;color:var(--text)}}
.product-price{{font-size:18px;font-weight:700;color:var(--primary);margin-bottom:8px}}
.product-specs{{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px}}
.product-specs span{{font-size:12px;color:var(--text-light);background:#f0f2f4;padding:2px 8px;border-radius:4px}}
.product-link{{font-size:14px;font-weight:600;color:var(--primary);display:inline-flex;align-items:center;gap:4px;margin-top:auto;transition:gap .2s}}
.product-card:hover .product-link{{gap:8px}}
.empty{{grid-column:1/-1;text-align:center;padding:60px 20px;color:var(--text-light);font-size:16px}}
@media(max-width:768px){{.product-grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
{NAV}
<div class="page-wrap">
  <div class="breadcrumb">
    <a href="/">首页</a><span class="sep">›</span>
    <a href="/products-categories.html">产品中心</a><span class="sep">›</span>
    <a href="/products/category-{cat['id']}.html">{cat['name']}</a><span class="sep">›</span>
    <span class="current">{sub_name}</span>
  </div>
  <div class="page-header">
    <h1>{sub_name}</h1>
    <p>{cat['name']} — {sub_name}</p>
    <div class="count">共 {len(items)} 款产品</div>
  </div>
  <div class="content">
    <div class="product-grid">{product_cards}
    </div>
  </div>
</div>
""" + footer(CATEGORIES) + COMMON_SCRIPT + """
</body>
</html>"""

        sub_dir = os.path.join(prod_dir, f"category-{cat['id']}")
        os.makedirs(sub_dir, exist_ok=True)
        with open(os.path.join(sub_dir, f"subcat-{sslug}.html"), "w", encoding="utf-8") as f:
            f.write(page)
        print(f"✅ products/category-{cat['id']}/subcat-{sslug}.html ({len(items)} 款)")

# ---- Update index.html ----
index_path = os.path.join(BASE, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    idx = f.read()

# Redirect product center links to new page
idx = idx.replace('/products"', '/products-categories.html"')
idx = idx.replace('/products.', '/products-categories.')  # catch any /products.xxx

with open(index_path, "w", encoding="utf-8") as f:
    f.write(idx)
print("✅ Updated index.html product links")

# ---- Update old product list pages ----
# Replace old breadcrumb links in product detail pages
import glob
for fpath in glob.glob(os.path.join(BASE, "product", "*.html")):
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace('/products.html', '/products-categories.html')
    content = content.replace('/products"', '/products-categories.html"')
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print()
print("=" * 50)
print("全部完成！")
print(f"产品总数: {len(products)} 款")
print(f"分类: {len(CATEGORIES)} 个")
subtotal = sum(len(get_subs(c["catKey"])) for c in CATEGORIES)
print(f"小类: {subtotal} 个")
print(f"生成页面:")
print(f"  1 个产品中心总览页")
print(f"  {len(CATEGORIES)} 个分类页")
print(f"  {subtotal} 个小类页")
print(f"  30 个产品详情页（已有）")
print("=" * 50)
