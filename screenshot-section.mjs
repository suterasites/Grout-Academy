import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const url = process.argv[2];
const selector = process.argv[3] || '#gallery';
const label = process.argv[4] || 'section';

const screenshotDir = path.join(__dirname, 'temporary screenshots');
const existing = fs.readdirSync(screenshotDir).filter(f => f.startsWith('screenshot-'));
let maxNum = 0;
for (const f of existing) { const m = f.match(/^screenshot-(\d+)/); if (m) maxNum = Math.max(maxNum, parseInt(m[1])); }
const num = maxNum + 1;
const filename = `screenshot-${num}-${label}.png`;

(async () => {
  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
  // Scroll through page so lazy images load
  await page.evaluate(async () => {
    await new Promise(resolve => {
      let y = 0; const step = 400;
      const t = setInterval(() => {
        window.scrollTo(0, y); y += step;
        if (y > document.body.scrollHeight) { clearInterval(t); window.scrollTo(0,0); resolve(); }
      }, 100);
    });
  });
  await new Promise(r => setTimeout(r, 500));
  const el = await page.$(selector);
  if (!el) { console.log(`Selector not found: ${selector}`); process.exit(1); }
  await el.screenshot({ path: path.join(screenshotDir, filename) });
  console.log(`Saved: ${filename}`);
  await browser.close();
})();
