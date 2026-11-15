// Converts notebooks/*.ipynb into markdown posts for the `notebooks` collection.
// The first cell of each notebook must be a raw cell holding the post's YAML front matter.
import { existsSync, mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { basename, join } from 'node:path';
import { parse as parseYaml } from 'yaml';

const SOURCE_DIR = 'notebooks';
const OUT_DIR = 'src/generated/notebooks';
const ASSET_DIR = 'public/notebooks';
const SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const TERMINAL_CODES = /\x1b\[[0-?]*[ -/]*[@-~]|\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)/g;
const IMAGE_TYPES = { 'image/png': 'png', 'image/jpeg': 'jpg', 'image/gif': 'gif' };
const SKIP_DRAFTS = process.argv.includes('--production');

const text = (source) => (Array.isArray(source) ? source.join('') : (source ?? ''));

const escapeHtml = (s) =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

// Drops escape codes and keeps only the last redraw of lines that use \r (progress bars).
const terminalText = (s) =>
  s
    .replace(TERMINAL_CODES, '')
    .replace(/\r\n/g, '\n')
    .split('\n')
    .map((line) => line.slice(line.lastIndexOf('\r') + 1))
    .join('\n');

function fenced(body, lang) {
  const longestRun = Math.max(0, ...(body.match(/`+/g) ?? []).map((run) => run.length));
  const fence = '`'.repeat(Math.max(3, longestRun + 1));
  return `${fence}${lang}\n${body.replace(/\n$/, '')}\n${fence}`;
}

const preformatted = (s) => `<pre class="output"><code>${escapeHtml(terminalText(s).replace(/\n$/, ''))}</code></pre>`;

// Markdown ends a raw HTML block at a blank line; an empty comment keeps the block (and <pre> spacing) intact.
const htmlBlock = (html) => `<div class="nb-output">\n${html.trim().replace(/^[ \t]*$/gm, '<!---->')}\n</div>`;

function frontMatter(cell, file) {
  const raw = cell?.cell_type === 'raw' ? text(cell.source).trim() : '';
  const yaml = raw.match(/^---\r?\n([\s\S]*?)\r?\n---$/)?.[1];
  if (yaml === undefined) {
    throw new Error(`${file}: the first cell must be a raw cell with YAML front matter (--- title, date, tab ---)`);
  }
  try {
    return { raw, data: parseYaml(yaml) ?? {} };
  } catch (err) {
    throw new Error(`${file}: invalid front matter (${err.message})`);
  }
}

function writeImage(bundle, writeAsset) {
  const type = Object.keys(IMAGE_TYPES).find((t) => bundle[t]);
  if (type) return writeAsset(IMAGE_TYPES[type], Buffer.from(text(bundle[type]), 'base64'));
  if (bundle['image/svg+xml']) return writeAsset('svg', text(bundle['image/svg+xml']));
  return null;
}

function renderData(data, writeAsset, file) {
  const image = writeImage(data, writeAsset);
  if (image) return `![output](${image})`;
  const html = text(data['text/html']);
  if (html && !/<script/i.test(html)) return htmlBlock(html);
  if (html) {
    console.warn(`nb2md: ${file}: skipped an output that needs JavaScript (blocked on the site); save it as an image`);
    return '';
  }
  if (data['text/markdown']) return text(data['text/markdown']);
  if (data['text/plain']) return preformatted(text(data['text/plain']));
  return '';
}

function renderOutput(output, writeAsset, file) {
  switch (output.output_type) {
    case 'stream':
      return preformatted(text(output.text));
    case 'error':
      return preformatted(output.traceback?.length ? output.traceback.join('\n') : `${output.ename}: ${output.evalue}`);
    case 'execute_result':
    case 'display_data':
      return renderData(output.data ?? {}, writeAsset, file);
    default:
      return '';
  }
}

const markdownCell = (cell, writeAsset) =>
  Object.entries(cell.attachments ?? {}).reduce((source, [name, bundle]) => {
    const path = writeImage(bundle, writeAsset);
    return path ? source.replaceAll(`attachment:${name}`, path) : source;
  }, text(cell.source));

function renderCell(cell, lang, writeAsset, file) {
  const tags = cell.metadata?.tags ?? [];
  if (tags.includes('remove-cell')) return [];
  if (cell.cell_type === 'markdown') return [markdownCell(cell, writeAsset)];
  if (cell.cell_type !== 'code') return [];
  const source = text(cell.source);
  const input = tags.includes('remove-input') || !source.trim() ? [] : [fenced(source, lang)];
  const outputs = tags.includes('remove-output') ? [] : (cell.outputs ?? []).map((o) => renderOutput(o, writeAsset, file));
  return [...input, ...outputs];
}

function readNotebook(file) {
  try {
    return JSON.parse(readFileSync(join(SOURCE_DIR, file), 'utf8'));
  } catch (err) {
    throw new Error(`${file}: not a readable notebook (${err.message})`);
  }
}

function convert(file) {
  const slug = basename(file, '.ipynb');
  if (!SLUG.test(slug)) throw new Error(`${file}: rename to lowercase-with-dashes (it becomes the URL)`);

  const notebook = readNotebook(file);
  const [first, ...cells] = notebook.cells ?? [];
  const meta = frontMatter(first, file);
  if (SKIP_DRAFTS && meta.data.draft === true) return null;
  const lang = notebook.metadata?.kernelspec?.language ?? notebook.metadata?.language_info?.name ?? 'python';

  let assetCount = 0;
  const writeAsset = (ext, content) => {
    const dir = join(ASSET_DIR, slug);
    mkdirSync(dir, { recursive: true });
    const name = `out-${++assetCount}.${ext}`;
    writeFileSync(join(dir, name), content);
    return `/notebooks/${slug}/${name}`;
  };

  const blocks = [meta.raw, ...cells.flatMap((cell) => renderCell(cell, lang, writeAsset, file))];
  writeFileSync(join(OUT_DIR, `${slug}.md`), `${blocks.filter(Boolean).join('\n\n')}\n`);
  return slug;
}

rmSync(OUT_DIR, { recursive: true, force: true });
rmSync(ASSET_DIR, { recursive: true, force: true });
mkdirSync(OUT_DIR, { recursive: true });

const files = existsSync(SOURCE_DIR) ? readdirSync(SOURCE_DIR).filter((f) => f.endsWith('.ipynb')) : [];
try {
  const slugs = files.map(convert).filter(Boolean);
  console.log(`nb2md: ${slugs.length} notebook(s)${slugs.length ? `: ${slugs.join(', ')}` : ''}`);
} catch (err) {
  console.error(`nb2md: ${err.message}`);
  process.exit(1);
}
