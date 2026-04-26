import sharp from 'sharp';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const assetsIn = path.resolve(__dirname, '../brand_assets/webflow');
const assetsOut = path.resolve(__dirname, '../brand_assets/optimized');

const tasks = [
  // Logo: square brand mark; nav h-10 = 40px @ 2x retina = 80px. 160px = 4x for safety.
  { in: 'logo-grout-academy-black.png', out: 'logo-grout-academy-black-160.png', resize: { width: 160, height: 160, fit: 'inside' }, format: 'png' },

  // Hero: shown at ~507x380 (mobile) up to 600x520 (desktop). Two WebP variants.
  { in: 'hero-shower-regrouting.jpeg', out: 'hero-shower-regrouting-640.webp', resize: { width: 640 }, format: 'webp', quality: 78 },
  { in: 'hero-shower-regrouting.jpeg', out: 'hero-shower-regrouting-1200.webp', resize: { width: 1200 }, format: 'webp', quality: 80 },
];

for (const t of tasks) {
  const inPath = path.join(assetsIn, t.in);
  const outPath = path.join(assetsOut, t.out);
  let pipe = sharp(inPath).resize(t.resize);
  if (t.format === 'webp') pipe = pipe.webp({ quality: t.quality });
  if (t.format === 'png') pipe = pipe.png({ compressionLevel: 9, palette: true });
  const info = await pipe.toFile(outPath);
  console.log(`${t.out}: ${info.width}x${info.height}, ${(info.size / 1024).toFixed(1)} KiB`);
}
