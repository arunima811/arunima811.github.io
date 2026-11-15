import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const webUrl = z.url({ protocol: /^https?$/ });

const postSchema = z.object({
  title: z.string(),
  date: z.coerce.date(),
  tab: z.enum(['work', 'notwork']),
  summary: z.string().optional(),
  tags: z.array(z.string()).default([]),
  draft: z.boolean().default(false),
  external: webUrl.optional(),
  image: z.string().startsWith('/').optional(),
});

const posts = defineCollection({
  loader: glob({ base: './src/content/posts', pattern: '**/*.md' }),
  schema: postSchema,
});

// Written by scripts/nb2md.mjs from notebooks/*.ipynb.
const notebooks = defineCollection({
  loader: glob({ base: './src/generated/notebooks', pattern: '*.md' }),
  schema: postSchema,
});

const projects = defineCollection({
  loader: glob({ base: './src/content/projects', pattern: '*.md' }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    org: z.string(),
    period: z.coerce.string(),
    stack: z.array(z.string()),
    order: z.number(),
    links: z.array(z.object({ label: z.string(), url: webUrl })).default([]),
  }),
});

export const collections = { posts, notebooks, projects };
