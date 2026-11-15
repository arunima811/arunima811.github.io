import type { APIContext } from 'astro';
import { profile } from '../data/profile';
import { getPosts, postHref } from '../lib/posts';

const xml = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

export async function GET({ site }: APIContext) {
  const items = (await getPosts())
    .map((post) => {
      const url = new URL(postHref(post), site).href;
      const summary = post.data.summary ? `<description>${xml(post.data.summary)}</description>` : '';
      return `<item><title>${xml(post.data.title)}</title><link>${url}</link><guid>${url}</guid><pubDate>${post.data.date.toUTCString()}</pubDate>${summary}</item>`;
    })
    .join('');
  const body = `<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>${xml(profile.name)}</title><link>${site}</link><description>${xml(profile.description)}</description>${items}</channel></rss>`;
  return new Response(body, { headers: { 'Content-Type': 'application/rss+xml; charset=utf-8' } });
}
