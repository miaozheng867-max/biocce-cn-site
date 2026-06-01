const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const dir = 'E:/OneDrive/桌面/biocce-new-site/images';

(async () => {
  // 产品PNG → 高品质JPG（减到10%体积）
  const pngs = ['product-bc1250.png', 'product-bc1000.png', 'product-bc600.png', 'product-bc500.png'];
  for (const f of pngs) {
    const src = path.join(dir, f);
    if (!fs.existsSync(src)) continue;
    const before = fs.statSync(src).size;
    
    const jpgName = f.replace('.png', '.jpg');
    const jpgPath = path.join(dir, jpgName);
    
    await sharp(src)
      .jpeg({ quality: 80, mozjpeg: true })
      .toFile(jpgPath);
    
    const after = fs.statSync(jpgPath).size;
    const saved = ((before - after) / before * 100).toFixed(0);
    console.log(`${f} → ${jpgName}: ${(before/1024).toFixed(0)}KB → ${(after/1024).toFixed(0)}KB (节省${saved}%)`);
    
    // 删除原PNG
    fs.unlinkSync(src);
  }
  
  // 最终统计
  console.log('\n=== 最终images目录 ===');
  const remaining = fs.readdirSync(dir).filter(f => f.endsWith('.jpg') || f.endsWith('.png')).sort();
  for (const f of remaining) {
    const s = fs.statSync(path.join(dir, f));
    console.log(`${(s.size/1024).toFixed(0)}KB\t${f}`);
  }
  
  // 删除压缩脚本
  fs.unlinkSync(path.join(dir, 'compress.js'));
})();
