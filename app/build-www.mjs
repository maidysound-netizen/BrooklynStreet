// Copies the game into www/ for the app, with three.js bundled so the app works without internet
// and without the game being on any public web address.
import { cpSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
const root = process.env.GAME_DIR ? new URL('file://' + process.env.GAME_DIR.replace(/\/?$/, '/')) : new URL('../', import.meta.url), out = new URL('www/', import.meta.url);
rmSync(out, { recursive: true, force: true }); mkdirSync(out);
for (const f of ['bgm.mp3', 'founder-bigman.webp', 'founder-cho.webp', 'founder-runner.webp', 'takako-logo.webp']) cpSync(new URL(f, root), new URL(f, out));
cpSync(new URL('node_modules/three/build/three.module.js', import.meta.url), new URL('three.module.js', out));
const cdn = 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';
const html = readFileSync(new URL('index.html', root), 'utf8');
if (!html.includes(cdn)) throw new Error('three.js import not found in index.html');
writeFileSync(new URL('index.html', out), html.replace(cdn, './three.module.js'));
console.log('www ready');
