import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://arunima811.github.io',
  devToolbar: { enabled: false },
  markdown: {
    shikiConfig: { theme: 'github-light' },
  },
});
