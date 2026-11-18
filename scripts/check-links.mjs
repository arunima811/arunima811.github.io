import { readdirSync, readFileSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import config from '../astro.config.mjs';

const DIST = 'dist';
const ORIGIN = new URL(config.site).origin;
const SITE_HOST = new URL(config.site).host;
const NOT_MARKUP = /<(pre|code)\b[\s\S]*?<\/\1>|<!--[\s\S]*?-->/g;
const URL_ATTR = /\s(href|src|srcset)=(?:"([^"]*)"|'([^']*)')/g;
const OG_IMAGE = /<meta\s+(?:property|name)="(?:og|twitter):image"\s+content="([^"]*)"/g;
const ID_ATTR = /\sid=(?:"([^"]*)"|'([^']*)')/g;
const ENTITIES = { amp: '&', quot: '"', apos: "'", lt: '<', gt: '>' };

const unescape = (text) =>
  text.replace(/&(?:#(\d+)|#x([0-9a-f]+)|(\w+));/gi, (all, dec, hex, name) =>
    dec ? String.fromCodePoint(+dec) : hex ? String.fromCodePoint(parseInt(hex, 16)) : (ENTITIES[name] ?? all),
  );

const walk = (dir) =>
  readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const path = join(dir, entry.name);
    return entry.isDirectory() ? walk(path) : [relative(DIST, path).split(sep).join('/')];
  });

let files;
try {
  files = new Set(walk(DIST));
} catch {
  console.error('No dist/ folder: run `npm run build` first.');
  process.exit(1);
}
const pages = [...files].filter((file) => file.endsWith('.html'));
if (pages.length === 0) {
  console.error('No HTML pages in dist/: run `npm run build` first.');
  process.exit(1);
}
const markup = new Map(pages.map((page) => [page, readFileSync(join(DIST, page), 'utf8').replace(NOT_MARKUP, '')]));
const ids = new Map(
  pages.map((page) => [page, new Set([...markup.get(page).matchAll(ID_ATTR)].map((m) => unescape(m[1] ?? m[2])))]),
);

const fileFor = (pathname) => {
  const path = decodeURIComponent(pathname).slice(1);
  const candidates = path === '' || path.endsWith('/') ? [`${path}index.html`] : [path, `${path}/index.html`, `${path}.html`];
  return candidates.find((candidate) => files.has(candidate));
};

const resolves = (page, ref) => {
  try {
    const url = new URL(ref, `${ORIGIN}/${page}`);
    if (!/^https?:$/.test(url.protocol) || url.host !== SITE_HOST) return true;
    const file = fileFor(url.pathname);
    if (!file) return false;
    const fragment = decodeURIComponent(url.hash.slice(1));
    return !fragment || fragment.toLowerCase() === 'top' || !file.endsWith('.html') || ids.get(file).has(fragment);
  } catch {
    return false;
  }
};

const refsIn = (html) => [
  ...[...html.matchAll(URL_ATTR)].flatMap(([, attr, double, single]) => {
    const value = unescape(double ?? single);
    return attr === 'srcset' ? value.split(',').map((candidate) => candidate.trim().split(/\s+/)[0]).filter(Boolean) : [value];
  }),
  ...[...html.matchAll(OG_IMAGE)].map((m) => unescape(m[1])),
];

let checked = 0;
const broken = [];
for (const page of pages) {
  for (const ref of refsIn(markup.get(page))) {
    checked += 1;
    if (!resolves(page, ref)) broken.push(`${DIST}/${page}: ${ref}`);
  }
}

console.log(`Checked ${checked} links.`);
if (broken.length > 0) {
  console.error(`Broken links:\n${broken.join('\n')}`);
  process.exit(1);
}
