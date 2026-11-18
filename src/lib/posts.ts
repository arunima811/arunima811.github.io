import { getCollection, type CollectionEntry } from 'astro:content';

export type Tab = 'work' | 'notwork';
export type Post = CollectionEntry<'posts'> | CollectionEntry<'notebooks'>;

const isVisible = ({ data }: Post) => import.meta.env.DEV || !data.draft;

export async function getPosts(tab?: Tab): Promise<Post[]> {
  const all: Post[] = [
    ...(await getCollection('posts', isVisible)),
    ...(await getCollection('notebooks', isVisible)),
  ];

  const seen = new Set<string>();
  for (const post of all) {
    if (seen.has(post.id)) {
      throw new Error(`Two posts share the slug "${post.id}" (a markdown post and a notebook?)`);
    }
    seen.add(post.id);
  }

  return all
    .filter((post) => !tab || post.data.tab === tab)
    .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}

export const postHref = (post: Post) => post.data.external ?? `/posts/${post.id}/`;

export const tagSlug = (tag: string) =>
  tag
    .toLowerCase()
    .trim()
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');

export const tagHref = (tag: string) => `/blog/tags/${tagSlug(tag)}/`;

export interface Tag {
  name: string;
  slug: string;
  count: number;
}

export function getTags(posts: Post[]): Tag[] {
  const bySlug = new Map<string, Tag>();
  for (const name of posts.flatMap((post) => post.data.tags)) {
    const slug = tagSlug(name);
    if (!slug) throw new Error(`Tag "${name}" has no ASCII letters or digits`);
    const tag = bySlug.get(slug);
    if (tag && tag.name !== name) throw new Error(`Tags "${tag.name}" and "${name}" share the slug "${slug}"`);
    bySlug.set(slug, { name, slug, count: (tag?.count ?? 0) + 1 });
  }
  return [...bySlug.values()].sort((a, b) => b.count - a.count || a.name.localeCompare(b.name));
}

export const formatDate = (date: Date, style: 'short' | 'long' = 'short') =>
  date.toLocaleDateString('en-US', {
    timeZone: 'UTC',
    year: 'numeric',
    month: style === 'short' ? 'short' : 'long',
    ...(style === 'long' && { day: 'numeric' }),
  });
