/**
 * 生成备案中文站产品层级：产品中心 → 分类 → 小类 → 产品详情
 * 生成文件：
 *   - /products-categories.html      产品中心总览页（6大分类）
 *   - /products/category-{slug}.html  分类页（显示小类卡片）
 *   - /products/subcat-{slug}.html    小类页（显示产品列表）
 *   已存在的 /product/{slug}.html     产品详情页（不动）
 */

const fs = require('fs');
const path = require('path');

const DATA_PATH = path.join(__dirname, 'products-data.json');
const products = JSON.parse(fs.readFileSync(DATA_PATH, 'utf-8'));

// ============ 分类定义 ============
const categories = [
  {
    id: 'scrubbers',
    name: '洗地机/洗地吸干机',
    slug: 'scrubbers',
    catKey: '洗地机/洗地吸干机',
    desc: '从紧凑型手推式到驾驶式，满足不同面积的商业和工业地面清洁需求。',
    icon: '洗',
    color: '#1A3A4A'
  },
  {
    id: 'pressure-washers',
    name: '高压清洗机',
    slug: 'pressure-washers',
    catKey: '高压清洗机',
    desc: '冷水、热水及超高压清洗机，适用于工业设备、建筑、车辆等重污垢清洗。',
    icon: '高',
    color: '#2D5A6E'
  },
  {
    id: 'vacuums',
    name: '工业吸尘器',
    slug: 'vacuums',
    catKey: '真空吸尘器',
    desc: '专业干湿两用吸尘器，多级别过滤，适用于工厂、仓库等环境的深度清洁。',
    icon: '吸',
    color: '#3A6B7E'
  },
  {
    id: 'sweepers',
    name: '扫地机',
    slug: 'sweepers',
    catKey: '扫地机',
    desc: '工业级扫地车，手推式及驾驶式，适用于大面积场地、厂区、道路清扫。',
    icon: '扫',
    color: '#1E4D5E'
  },
  {
    id: 'steam-cleaners',
    name: '蒸汽清洁机',
    slug: 'steam-cleaners',
    catKey: '蒸汽清洁机',
    desc: '高温蒸汽深度清洁，无需化学药剂，适用于食品加工、厨房、医疗等高卫生要求场所。',
    icon: '蒸',
    color: '#4A7A8E'
  },
  {
    id: 'dry-ice',
    name: '干冰清洗机',
    slug: 'dry-ice',
    catKey: '干冰清洗机',
    desc: '现代化干冰清洗技术，快速高效无损清洗，适用于模具、电子、食品等行业。',
    icon: '冰',
    color: '#3B6B7E'
  }
];

// ============ 提取小类 ============
function getSubcategories(catKey) {
  const catProducts = products.filter(p => p.category === catKey);
  const subMap = {};
  catProducts.forEach(p => {
    const sub = p.subcategory;
    if (!subMap[sub]) subMap[sub] = [];
    subMap[sub].push(p);
  });
  return subMap;
}

// ============ 生成分类页 ============
function generateCategoryPages() {
  const dir = path.join(__dirname, 'products');
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

  categories.forEach(cat => {
    const subs = getSubcategories(cat.catKey);
    const totalCount = Object.values(subs).flat().length;

    // 构建小类卡片HTML
    let subCards = '';
    const subEntries = Object.entries(subs);
    subEntries.forEach(([subName, items]) => {
      const subSlug = subName
        .replace(/[\/\\]/g, '-')
        .replace(/\s+/g, '-')
        .replace(/[()]/g, '')
        .replace(/--+/g, '-')
        .replace(/^-|-$/g, '');
      const firstItem = items[0];
      const imgSrc = firstItem.image && firstItem.image.startsWith('http')
        ? firstItem.image
        : (firstItem.image ? '/' + firstItem.image : '');
      const count = items.length;

      subCards += `
      <a href="/products/category-${cat.slug}/subcat-${subSlug}.html" class="subcat-card">
        <div class="subcat-img-wrap">
          ${imgSrc ? `<img src="${imgSrc}" alt="${subName}" loading="lazy">` : `<div class="subcat-placeholder">${subName.charAt(0)}</div>`}
        </div>
        <div class="subcat-info">
          <h3>${subName}</h3>
          <span class="subcat-count">${count} 款产品</span>
          <span class="subcat-link">查看产品 &rarr;</span>
        </div>
      </a>`;
    });

    const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${cat.name} | 拜茨清洁设备</title>
<meta name="description" content="拜茨清洁设备提供${cat.name}全系列产品。${cat.desc}">
<link rel="canonical" href="https://www.biocce.cn/products/category-${cat.slug}.html">
<meta property="og:title" content="${cat.name} | 拜茨清洁设备">
<meta property="og:description" content="拜茨清洁设备提供${cat.name}全系列产品。${cat.desc}">
<meta property="og:url" content="https://www.biocce.cn/products/category-${cat.slug}.html">
<meta name="twitter:card" content="summary_large_image">
<!-- Google tag -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-8TF95LBYRV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-8TF95LBYRV');</script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/design-system.css">
<style>
:root{--primary:#1A3A4A;--accent:#C9A84C;--text:#1A1A1A;--text-secondary:#5a6a7a;--text-light:#8a9aa8;--border:#e8ecf0;--card:#fff;--bg:#FAFAF8}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,'Noto Sans SC',sans-serif;background:var(--bg);color:var(--text)}
.page-wrap{padding-top:64px}
.breadcrumb{max-width:1200px;margin:0 auto;padding:20px 24px 0;font-size:14px;color:var(--text-light)}
.breadcrumb a{color:var(--text-light);text-decoration:none}
.breadcrumb a:hover{color:var(--primary)}
.breadcrumb .sep{color:#ccc;margin:0 8px}
.breadcrumb .current{color:var(--primary);font-weight:500}
.page-header{max-width:1200px;margin:0 auto;padding:32px 24px 8px}
.page-header h1{font-size:28px;font-weight:700;margin-bottom:8px;color:var(--text)}
.page-header p{font-size:16px;color:var(--text-secondary);max-width:700px;line-height:1.6}
.page-header .count{font-size:14px;color:var(--text-light);margin-top:8px}
.content{max-width:1200px;margin:0 auto;padding:24px 24px 48px}
.subcat-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:24px}
.subcat-card{background:var(--card);border-radius:16px;overflow:hidden;border:1px solid var(--border);text-decoration:none;color:inherit;display:flex;flex-direction:column;transition:all .35s cubic-bezier(.25,.8,.25,1);box-shadow:0 1px 4px rgba(0,0,0,.04)}
.subcat-card:hover{transform:translateY(-6px);box-shadow:0 12px 40px rgba(26,58,74,.12)}
.subcat-img-wrap{aspect-ratio:16/9;background:linear-gradient(145deg,#f3f4f6,#eef0f3);display:flex;align-items:center;justify-content:center;overflow:hidden}
.subcat-img-wrap img{max-width:75%;max-height:80%;object-fit:contain;filter:drop-shadow(0 4px 12px rgba(0,0,0,.1));transition:transform .4s}
.subcat-card:hover .subcat-img-wrap img{transform:scale(1.05)}
.subcat-placeholder{font-size:48px;color:var(--text-light);opacity:.4}
.subcat-info{padding:20px;display:flex;flex-direction:column;flex:1}
.subcat-info h3{font-size:18px;font-weight:600;margin-bottom:6px;color:var(--text)}
.subcat-count{font-size:13px;color:var(--text-light);margin-bottom:12px}
.subcat-link{font-size:14px;font-weight:600;color:var(--primary);display:inline-flex;align-items:center;gap:4px;margin-top:auto;transition:gap .2s}
.subcat-card:hover .subcat-link{gap:8px}
@media(max-width:768px){.subcat-grid{grid-template-columns:1fr}}`);

    html += `</style>
</head>
<body>
<nav>
  <div class="nav-inner">
    <a href="/" class="nav-left"><div class="logo-mark">拜</div><span class="logo-text">拜茨清洁</span></a>
    <ul class="nav-right" id="navR">
      <li><a href="/">首页</a></li>
      <li><a href="/products-categories.html" class="active">产品中心</a></li>
      <li><a href="/about">关于我们</a></li>
      <li><a href="/services">服务支持</a></li>
      <li><a href="/insights">资讯动态</a></li>
      <li><a href="/contact" class="nav-cta">联系我们</a></li>
    </ul>
    <button class="hamburger" id="ham" aria-label="切换菜单"><span></span><span></span><span></span></button>
  </div>
</nav>
<div class="page-wrap">
  <div class="breadcrumb"><a href="/">首页</a><span class="sep">&rsaquo;</span><a href="/products-categories.html">产品中心</a><span class="sep">&rsaquo;</span><span class="current">${cat.name}</span></div>
  <div class="page-header">
    <h1>${cat.name}</h1>
    <p>${cat.desc}</p>
    <div class="count">共 ${totalCount} 款产品，按类型分类展示</div>
  </div>
  <div class="content">
    <div class="subcat-grid">${subCards}
    </div>
  </div>
</div>
<footer>
  <div class="footer-inner">
    <div><h3>拜茨清洁设备</h3><p>拜茨清洁设备（BAIZ Cleaning Equipment）专注为工商业客户提供清洁设备与清洁用品一站式解决方案，涵盖洗地机、高压清洗机、工业吸尘器、工业擦拭纸等全系列产品。专业服务，品质保障。</p></div>
    <div><h4>快速链接</h4><ul><li><a href="/">首页</a></li><li><a href="/products-categories.html">产品中心</a></li><li><a href="/about">关于我们</a></li><li><a href="/services">服务支持</a></li><li><a href="/contact">联系我们</a></li></ul></div>
    <div><h4>产品分类</h4><ul>${categories.map(c => `<li><a href="/products/category-${c.slug}.html">${c.name}</a></li>`).join('')}</ul></div>
    <div><h4>联系方式</h4><ul class="contact"><li>上海市 · 拜茨清洁设备</li><li><a href="mailto:info@biocce.cn">info@biocce.cn</a></li><li>咨询热线：021-xxxxxxx</li><li><a href="/contact">在线留言 &rarr;</a></li></ul></div>
  </div>
  <div class="social-map-section">
    <div class="social-links">
      <h4>关注我们</h4>
      <div class="social-icons">${['facebook','linkedin','youtube','instagram','tiktok'].map(s => `<a href="#" class="social-icon" aria-label="${s}"><svg>...</svg></a>`).join('')}</div>
    </div>
    <div class="map-container">
      <h4>公司位置</h4>
      <div class="map-embed"><a href="https://maps.google.com/?q=Shanghai+China" target="_blank" rel="noopener noreferrer">上海市 — 点击查看地图</a></div>
    </div>
  </div>
  <div class="footer-bottom"><span>&copy; 2026 上海拜茨清洁设备有限公司 版权所有</span><span><a href="/">www.biocce.cn</a></span></div>
</footer>
<script>
document.getElementById("ham").onclick=function(){document.getElementById("navR").classList.toggle("open");this.classList.toggle("active")};
var nls=document.querySelectorAll(".nav-right a");for(var i=0;i<nls.length;i++)nls[i].onclick=function(){document.getElementById("navR").classList.remove("open");document.getElementById("ham").classList.remove("active")};
</script>
</body>
</html>`;
    const filePath = path.join(__dirname, 'products', `category-${cat.slug}.html`);
    fs.writeFileSync(filePath, html, 'utf-8');
    console.log(`  ✅ 分类页: products/category-${cat.slug}.html (${totalCount}款产品, ${subEntries.length}个小类)`);
  });
}

// ============ 生成小类页 ============
function generateSubcategoryPages() {
  categories.forEach(cat => {
    const subs = getSubcategories(cat.catKey);
    Object.entries(subs).forEach(([subName, items]) => {
      const subSlug = subName
        .replace(/[\/\\]/g, '-')
        .replace(/\s+/g, '-')
        .replace(/[()]/g, '')
        .replace(/--+/g, '-')
        .replace(/^-|-$/g, '');

      // 产品卡片HTML
      let productCards = '';
      items.forEach(p => {
        const imgSrc = p.image && p.image.startsWith('http')
          ? p.image
          : (p.image ? '/' + p.image : '');
        const specKeys = Object.keys(p.specs);
        let specsHtml = '';
        if (specKeys.length > 0) {
          const top3 = specKeys.slice(0, 3);
          specsHtml = top3.map(k => `<span>${k}: ${p.specs[k]}</span>`).join('');
        } else {
          specsHtml = '<span>请联系客服获取详细参数</span>';
        }

        productCards += `
      <a href="/product/${p.slug}.html" class="product-card">
        <div class="product-img-wrap">
          ${imgSrc ? `<img src="${imgSrc}" alt="${p.model}" loading="lazy">` : `<div class="product-placeholder">${p.model.charAt(0)}</div>`}
        </div>
        <div class="product-info">
          <h3>${p.model}</h3>
          <div class="product-price">${p.price}</div>
          <div class="product-specs">${specsHtml}</div>
          <span class="product-link">查看详情 &rarr;</span>
        </div>
      </a>`;
      });

      const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${subName} | ${cat.name} | 拜茨清洁设备</title>
<meta name="description" content="拜茨清洁设备${cat.name} - ${subName}，共${items.length}款产品，适用于工商业清洁。">
<link rel="canonical" href="https://www.biocce.cn/products/category-${cat.slug}/subcat-${subSlug}.html">
<meta property="og:title" content="${subName} | ${cat.name} | 拜茨清洁设备">
<meta property="og:description" content="拜茨清洁设备${cat.name} - ${subName}，共${items.length}款产品。">
<meta property="og:url" content="https://www.biocce.cn/products/category-${cat.slug}/subcat-${subSlug}.html">
<meta name="twitter:card" content="summary_large_image">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/design-system.css">
<style>
:root{--primary:#1A3A4A;--accent:#C9A84C;--text:#1A1A1A;--text-secondary:#5a6a7a;--text-light:#8a9aa8;--border:#e8ecf0;--card:#fff;--bg:#FAFAF8}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,'Noto Sans SC',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;display:flex;flex-direction:column}
.page-wrap{padding-top:64px;flex:1}
.breadcrumb{max-width:1200px;margin:0 auto;padding:20px 24px 0;font-size:14px;color:var(--text-light)}
.breadcrumb a{color:var(--text-light);text-decoration:none}
.breadcrumb a:hover{color:var(--primary)}
.breadcrumb .sep{color:#ccc;margin:0 8px}
.breadcrumb .current{color:var(--primary);font-weight:500}
.page-header{max-width:1200px;margin:0 auto;padding:32px 24px 8px}
.page-header h1{font-size:28px;font-weight:700;margin-bottom:8px}
.page-header p{font-size:16px;color:var(--text-secondary);max-width:700px;line-height:1.6}
.page-header .count{font-size:14px;color:var(--text-light);margin-top:8px}
.content{max-width:1200px;margin:0 auto;padding:24px 24px 48px}
.product-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:24px}
.product-card{background:var(--card);border-radius:16px;overflow:hidden;border:1px solid var(--border);text-decoration:none;color:inherit;display:flex;flex-direction:column;transition:all .35s cubic-bezier(.25,.8,.25,1);box-shadow:0 1px 4px rgba(0,0,0,.04)}
.product-card:hover{transform:translateY(-6px);box-shadow:0 12px 40px rgba(26,58,74,.12)}
.product-img-wrap{aspect-ratio:4/3;background:linear-gradient(145deg,#f3f4f6,#eef0f3);display:flex;align-items:center;justify-content:center;overflow:hidden}
.product-img-wrap img{max-width:80%;max-height:85%;object-fit:contain;filter:drop-shadow(0 4px 12px rgba(0,0,0,.1));transition:transform .4s}
.product-card:hover .product-img-wrap img{transform:scale(1.05)}
.product-placeholder{font-size:48px;color:var(--text-light);opacity:.4}
.product-info{padding:20px;display:flex;flex-direction:column;flex:1}
.product-info h3{font-size:17px;font-weight:600;margin-bottom:6px;color:var(--text)}
.product-price{font-size:18px;font-weight:700;color:var(--primary);margin-bottom:8px}
.product-specs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px}
.product-specs span{font-size:12px;color:var(--text-light);background:#f0f2f4;padding:2px 8px;border-radius:4px}
.product-link{font-size:14px;font-weight:600;color:var(--primary);display:inline-flex;align-items:center;gap:4px;margin-top:auto;transition:gap .2s}
.product-card:hover .product-link{gap:8px}
.empty-state{grid-column:1/-1;text-align:center;padding:60px 20px;color:var(--text-light);font-size:16px}
@media(max-width:768px){.product-grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<nav>
  <div class="nav-inner">
    <a href="/" class="nav-left"><div class="logo-mark">拜</div><span class="logo-text">拜茨清洁</span></a>
    <ul class="nav-right" id="navR">
      <li><a href="/">首页</a></li>
      <li><a href="/products-categories.html" class="active">产品中心</a></li>
      <li><a href="/about">关于我们</a></li>
      <li><a href="/services">服务支持</a></li>
      <li><a href="/insights">资讯动态</a></li>
      <li><a href="/contact" class="nav-cta">联系我们</a></li>
    </ul>
    <button class="hamburger" id="ham" aria-label="切换菜单"><span></span><span></span><span></span></button>
  </div>
</nav>
<div class="page-wrap">
  <div class="breadcrumb">
    <a href="/">首页</a><span class="sep">&rsaquo;</span>
    <a href="/products-categories.html">产品中心</a><span class="sep">&rsaquo;</span>
    <a href="/products/category-${cat.slug}.html">${cat.name}</a><span class="sep">&rsaquo;</span>
    <span class="current">${subName}</span>
  </div>
  <div class="page-header">
    <h1>${subName}</h1>
    <p>${cat.name} — ${subName}</p>
    <div class="count">共 ${items.length} 款产品</div>
  </div>
  <div class="content">
    <div class="product-grid">${productCards}
    </div>
  </div>
</div>
<footer>
  <div class="footer-inner">
    <div><h3>拜茨清洁设备</h3><p>拜茨清洁设备（BAIZ Cleaning Equipment）专注为工商业客户提供清洁设备与清洁用品一站式解决方案，涵盖洗地机、高压清洗机、工业吸尘器、工业擦拭纸等全系列产品。专业服务，品质保障。</p></div>
    <div><h4>快速链接</h4><ul><li><a href="/">首页</a></li><li><a href="/products-categories.html">产品中心</a></li><li><a href="/about">关于我们</a></li><li><a href="/services">服务支持</a></li><li><a href="/contact">联系我们</a></li></ul></div>
    <div><h4>产品分类</h4><ul>${categories.map(c => `<li><a href="/products/category-${c.slug}.html">${c.name}</a></li>`).join('')}</ul></div>
    <div><h4>联系方式</h4><ul class="contact"><li>上海市 · 拜茨清洁设备</li><li><a href="mailto:info@biocce.cn">info@biocce.cn</a></li><li>咨询热线：021-xxxxxxx</li><li><a href="/contact">在线留言 &rarr;</a></li></ul></div>
  </div>
  <div class="social-map-section">
    <div class="social-links">
      <h4>关注我们</h4>
      <div class="social-icons">[social icons]</div>
    </div>
    <div class="map-container">
      <h4>公司位置</h4>
      <div class="map-embed"><a href="https://maps.google.com/?q=Shanghai+China" target="_blank" rel="noopener noreferrer">上海市 — 点击查看地图</a></div>
    </div>
  </div>
  <div class="footer-bottom"><span>&copy; 2026 上海拜茨清洁设备有限公司 版权所有</span><span><a href="/">www.biocce.cn</a></span></div>
</footer>
<script>
document.getElementById("ham").onclick=function(){document.getElementById("navR").classList.toggle("open");this.classList.toggle("active")};
var nls=document.querySelectorAll(".nav-right a");for(var i=0;i<nls.length;i++)nls[i].onclick=function(){document.getElementById("navR").classList.remove("open");document.getElementById("ham").classList.remove("active")};
</script>
</body>
</html>`;
      const subDir = path.join(__dirname, 'products', `category-${cat.slug}`);
      if (!fs.existsSync(subDir)) fs.mkdirSync(subDir, { recursive: true });
      const filePath = path.join(subDir, `subcat-${subSlug}.html`);
      fs.writeFileSync(filePath, html, 'utf-8');
      console.log(`  ✅ 小类页: products/category-${cat.slug}/subcat-${subSlug}.html (${items.length}款)`);
    });
  });
}

// ============ 生成产品中心总览页 ============
function generateOverviewPage() {
  let catCards = '';
  categories.forEach(cat => {
    const subs = getSubcategories(cat.catKey);
    const totalCount = Object.values(subs).flat().length;
    const subCount = Object.keys(subs).length;
    const firstItem = Object.values(subs)[0]?.[0];
    const imgSrc = firstItem?.image && firstItem.image.startsWith('http')
      ? firstItem.image
      : (firstItem?.image ? '/' + firstItem.image : '');

    catCards += `
      <a href="/products/category-${cat.slug}.html" class="cat-card">
        <div class="cat-img-wrap">
          ${imgSrc ? `<img src="${imgSrc}" alt="${cat.name}" loading="lazy">` : `<div class="cat-placeholder">${cat.icon}</div>`}
        </div>
        <div class="cat-info">
          <h3>${cat.name}</h3>
          <p>${cat.desc}</p>
          <div class="cat-meta">${subCount} 个子分类 · ${totalCount} 款产品</div>
          <span class="cat-link">浏览 ${cat.name} &rarr;</span>
        </div>
      </a>`;
  });

  const html = `<!DOCTYPE html>
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
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="design-system.css">
<style>
:root{--primary:#1A3A4A;--accent:#C9A84C;--text:#1A1A1A;--text-secondary:#5a6a7a;--text-light:#8a9aa8;--border:#e8ecf0;--card:#fff;--bg:#FAFAF8}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,'Noto Sans SC',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;display:flex;flex-direction:column}
.page-wrap{padding-top:64px;flex:1}
.breadcrumb{max-width:1200px;margin:0 auto;padding:20px 24px 0;font-size:14px;color:var(--text-light)}
.breadcrumb .current{color:var(--primary);font-weight:500}
.page-header{max-width:1200px;margin:0 auto;padding:32px 24px 8px;text-align:center}
.page-header h1{font-size:32px;font-weight:700;margin-bottom:12px}
.page-header p{font-size:16px;color:var(--text-secondary);max-width:600px;margin:0 auto;line-height:1.6}
.content{max-width:1200px;margin:0 auto;padding:24px 24px 48px}
.cat-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(350px,1fr));gap:24px}
.cat-card{background:var(--card);border-radius:16px;overflow:hidden;border:1px solid var(--border);text-decoration:none;color:inherit;display:flex;flex-direction:column;transition:all .35s cubic-bezier(.25,.8,.25,1);box-shadow:0 1px 4px rgba(0,0,0,.04)}
.cat-card:hover{transform:translateY(-6px);box-shadow:0 12px 40px rgba(26,58,74,.12)}
.cat-img-wrap{aspect-ratio:16/9;background:linear-gradient(145deg,#f0f2f5,#e8ecf0);display:flex;align-items:center;justify-content:center;overflow:hidden}
.cat-img-wrap img{max-width:70%;max-height:75%;object-fit:contain;filter:drop-shadow(0 4px 12px rgba(0,0,0,.1));transition:transform .4s}
.cat-card:hover .cat-img-wrap img{transform:scale(1.08)}
.cat-placeholder{font-size:56px;color:var(--text-light);opacity:.3}
.cat-info{padding:24px;display:flex;flex-direction:column;flex:1}
.cat-info h3{font-size:20px;font-weight:600;margin-bottom:8px;color:var(--text)}
.cat-info p{font-size:14px;color:var(--text-secondary);line-height:1.5;margin-bottom:12px;flex:1}
.cat-meta{font-size:13px;color:var(--text-light);margin-bottom:14px}
.cat-link{font-size:14px;font-weight:600;color:var(--primary);display:inline-flex;align-items:center;gap:4px;transition:gap .2s}
.cat-card:hover .cat-link{gap:8px}
@media(max-width:768px){.cat-grid{grid-template-columns:1fr}.page-header h1{font-size:26px}}
</style>
</head>
<body>
<nav>
  <div class="nav-inner">
    <a href="/" class="nav-left"><div class="logo-mark">拜</div><span class="logo-text">拜茨清洁</span></a>
    <ul class="nav-right" id="navR">
      <li><a href="/">首页</a></li>
      <li><a href="/products-categories.html" class="active">产品中心</a></li>
      <li><a href="/about">关于我们</a></li>
      <li><a href="/services">服务支持</a></li>
      <li><a href="/insights">资讯动态</a></li>
      <li><a href="/contact" class="nav-cta">联系我们</a></li>
    </ul>
    <button class="hamburger" id="ham" aria-label="切换菜单"><span></span><span></span><span></span></button>
  </div>
</nav>
<div class="page-wrap">
  <div class="breadcrumb"><a href="/">首页</a><span class="sep">&rsaquo;</span><span class="current">产品中心</span></div>
  <div class="page-header">
    <h1>产品中心</h1>
    <p>拜茨清洁设备提供全系列工商业清洁设备与清洁用品，按产品分类浏览，快速找到适合您的设备。</p>
  </div>
  <div class="content">
    <div class="cat-grid">${catCards}
    </div>
  </div>
</div>
<footer>
  <div class="footer-inner">
    <div><h3>拜茨清洁设备</h3><p>拜茨清洁设备专注为工商业客户提供清洁设备与清洁用品一站式解决方案。专业服务，品质保障。</p></div>
    <div><h4>快速链接</h4><ul><li><a href="/">首页</a></li><li><a href="/products-categories.html">产品中心</a></li><li><a href="/about">关于我们</a></li><li><a href="/services">服务支持</a></li><li><a href="/contact">联系我们</a></li></ul></div>
    <div><h4>产品分类</h4><ul>${categories.map(c => `<li><a href="/products/category-${c.slug}.html">${c.name}</a></li>`).join('')}</ul></div>
    <div><h4>联系方式</h4><ul class="contact"><li>上海市 · 拜茨清洁设备</li><li><a href="mailto:info@biocce.cn">info@biocce.cn</a></li><li>咨询热线：021-xxxxxxx</li><li><a href="/contact">在线留言 &rarr;</a></li></ul></div>
  </div>
  <div class="social-map-section">
    [social icons + map]
  </div>
  <div class="footer-bottom"><span>&copy; 2026 上海拜茨清洁设备有限公司 版权所有</span><span><a href="/">www.biocce.cn</a></span></div>
</footer>
<script>
document.getElementById("ham").onclick=function(){document.getElementById("navR").classList.toggle("open");this.classList.toggle("active")};
var nls=document.querySelectorAll(".nav-right a");for(var i=0;i<nls.length;i++)nls[i].onclick=function(){document.getElementById("navR").classList.remove("open");document.getElementById("ham").classList.remove("active")};
</script>
</body>
</html>`;
  const filePath = path.join(__dirname, 'products-categories.html');
  fs.writeFileSync(filePath, html, 'utf-8');
  console.log('✅ 产品中心总览页: products-categories.html');
}

// ============ 更新首页导航和产品分类链接 ============
function updateIndex() {
  const indexPath = path.join(__dirname, 'index.html');
  let html = fs.readFileSync(indexPath, 'utf-8');
  // 首页导航的"产品中心"链接指向新页
  html = html.replace(
    /<a href="\/products"[^>]*>产品中心<\/a>/,
    '<a href="/products-categories.html">产品中心</a>'
  );
  // 首页Hero的"查看产品"按钮
  html = html.replace(
    /<a href="\/products"[^>]*class="btn btn-primary">查看产品 &rarr;<\/a>/,
    '<a href="/products-categories.html" class="btn btn-primary">查看产品 &rarr;</a>'
  );
  fs.writeFileSync(indexPath, html, 'utf-8');
  console.log('✅ 已更新首页产品中心链接');
}

// ============ 主流程 ============
console.log('\n=== 开始生成产品层级页面 ===\n');
generateOverviewPage();
generateCategoryPages();
generateSubcategoryPages();
updateIndex();
console.log('\n=== 全部完成 ===');
console.log(`总产品: ${products.length}款`);
console.log(`总分类: ${categories.length}个`);
console.log(`页面数: 1个总览 + ${categories.length}个分类页 + 总小类数`);
