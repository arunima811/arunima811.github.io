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

export const formatDate = (date: Date, style: 'short' | 'long' = 'short') =>
  date.toLocaleDateString('en-US', {
    timeZone: 'UTC',
    year: 'numeric',
    month: style === 'short' ? 'short' : 'long',
    ...(style === 'long' && { day: 'numeric' }),
  });
