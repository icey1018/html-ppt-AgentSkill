#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import { existsSync } from 'node:fs';
import { execSync } from 'node:child_process';

const CANDIDATES = [
  'examples/ai-agent-8p/index.html',
  'dist/ai-agent-8p-offline/index.html',
  'examples/ai-agent-terms-xhs/index.html',
];

const sourceArg = process.argv[2];
const total = Number(process.argv[3] || 12);
const source = sourceArg || CANDIDATES.find((p) => existsSync(p));

if (!source) {
  console.error('No source HTML found. Tried:', CANDIDATES.join(', '));
  process.exit(1);
}

const { chromium } = await import('playwright');

const outDir = path.resolve('dist/png');
await fs.mkdir(outDir, { recursive: true });

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 810, height: 1080 },
  deviceScaleFactor: 4,
});
const page = await context.newPage();

const abs = path.resolve(source);
const url = `file://${abs}`;
await page.goto(url, { waitUntil: 'domcontentloaded' });
await page.waitForLoadState('networkidle');

await page.evaluate(async () => {
  if (document.fonts?.ready) {
    await document.fonts.ready;
  }
  await Promise.all(
    Array.from(document.images || []).map((img) => {
      if (img.complete) return Promise.resolve();
      return new Promise((resolve) => {
        img.addEventListener('load', resolve, { once: true });
        img.addEventListener('error', resolve, { once: true });
      });
    })
  );
});

await page.waitForTimeout(1200);

for (let i = 1; i <= total; i += 1) {
  const file = path.join(outDir, `slide-${String(i).padStart(2, '0')}.png`);
  await page.screenshot({ path: file, type: 'png' });
  if (i < total) {
    await page.keyboard.press('ArrowRight');
    await page.waitForTimeout(700);
  }
}

await browser.close();

const zipPath = path.resolve('dist/all-slides-png.zip');
try {
  execSync(`cd dist/png && zip -q -r ../all-slides-png.zip .`);
} catch {
  console.error('zip command failed. Ensure zip is installed.');
  process.exit(1);
}

console.log(`done: ${total} slides -> ${outDir}`);
console.log(`zip: ${zipPath}`);
