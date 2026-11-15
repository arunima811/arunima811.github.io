export interface Link {
  label: string;
  href: string;
}

export interface Photo {
  src: string;
  alt: string;
}

export interface TimelineEntry {
  when: string;
  role: string;
  org: string;
  where: string;
  highlights: string[];
}

export interface Dated {
  when: string;
  what: string;
}

export interface SideProject extends Dated {
  title: string;
  href: string;
}

export const profile = {
  name: 'Arunima Shukla',
  description:
    'Arunima Shukla is a software engineer in New York who builds reliable, high-throughput systems end to end: services, data pipelines, data lakes and warehouses, infrastructure and ML infrastructure.',

  work: {
    greeting: "Hi, I'm Arunima.",
    aka: 'You can call me Ru',
    photo: { src: '/me.jpg', alt: 'Arunima Shukla' } satisfies Photo,
    intro: [
      "I'm a software engineer in New York. I build reliable, high-throughput systems that scale, and I work across every part of them: services, data pipelines, data lakes and warehouses, and the infrastructure underneath.",
      'I own products end to end, from the first design to running in production, and have done so since 2019 at Dell EMC, Goldman Sachs and Rokt. The work I love most is ML infrastructure and data engineering: the systems that feed the models that act as the brain of a business.',
      "I'm enthusiastic about new technologies, tools and AI-driven development, and always up to talk about them.",
    ],
    now: 'at Rokt, streaming pipelines on Flink, an Iceberg lakehouse, and AI agents that help my team ship.',
    links: [
      { label: 'GitHub', href: 'https://github.com/arunima811' },
      { label: 'GitHub (Rokt)', href: 'https://github.com/arunima-rokt' },
      { label: 'LinkedIn', href: 'https://www.linkedin.com/in/arunima-shukla-pg/' },
      { label: 'Email', href: 'mailto:shukla.arunima0811@gmail.com' },
      { label: 'Résumé (PDF)', href: '/resume.pdf' },
    ] satisfies Link[],
  },

  timeline: [
    {
      when: 'Nov 2025 – now',
      role: 'Senior Software Engineer, Data Platform',
      org: 'Rokt',
      where: 'New York',
      highlights: [
        'Built the Flink pipeline that brings mParticle events into Rokt at about 10× the earlier volume (~50k events/s), and the visit processing that joins browsing, referral and conversion events into one history per user.',
        'Redesigned the lakehouse around a medallion layout; its clean, enriched silver layer now serves the revenue and ML teams.',
        'Designed a StarRocks query layer to replace Trino, and Iceberg bucketing that made Spark joins 8× faster.',
      ],
    },
    {
      when: 'Mar 2023 – Nov 2025',
      role: 'Software Development Engineer II',
      org: 'Goldman Sachs',
      where: 'New York',
      highlights: [
        'Moved a 2.8 PB legacy object store to AWS S3.',
        'Built the ingestion layer between market-risk pipelines and financial policy controls, with privacy-controlled access in Snowflake.',
        'Made daily risk pipelines (60M+ positions) about 30% more resilient, and used Kafka so a budgeting app stopped losing requests.',
      ],
    },
    {
      when: 'Jan – Dec 2022',
      role: 'Research Assistant, CogAI Lab',
      org: 'Indiana University',
      where: 'Bloomington, IN',
      highlights: [
        'Computational neuroscience with Prof. Zoran Tiganj: LSTM-based reinforcement learning models of grid and place cells, trained on human navigation data instead of the usual simulated rat paths.',
        'Helped teach advanced machine learning and reinforcement learning to graduate students.',
      ],
    },
    {
      when: '2021 – 2022',
      role: 'M.S. Data Science',
      org: 'Indiana University',
      where: 'Bloomington, IN',
      highlights: ['President of the Data Science Club.', 'Grace Hopper Celebration scholar, 2022.'],
    },
    {
      when: 'Jan 2019 – Aug 2021',
      role: 'Software Development Engineer',
      org: 'Dell EMC',
      where: 'Bangalore',
      highlights: [
        'Led a zero-downtime upgrade of a 5+ TB Elasticsearch order store used by 30+ services, with no data loss.',
        'Moved 30+ Scala subscribers to Kubernetes and 10+ Spring Boot services to PCF; automated a 100K+ events/hour pub-sub pipeline.',
        'Planned capacity for Black Friday order traffic.',
      ],
    },
    {
      when: 'May – Jul 2018',
      role: 'Data Engineering Intern',
      org: 'Niyo',
      where: 'Bangalore',
      highlights: [
        'Built a real-time anomaly-detection dashboard over application access logs, using Spark and Elasticsearch to ingest 70 GB of data.',
      ],
    },
    {
      when: '2015 – 2019',
      role: 'B.Tech, Computer Science & Engineering (minor in Economics)',
      org: 'Shiv Nadar University',
      where: 'Delhi NCR',
      highlights: ['Full academic scholarship from the Shiv Nadar Foundation.'],
    },
  ] satisfies TimelineEntry[],

  sideProjects: [
    {
      when: '2022',
      title: 'SARSA from scratch',
      what: 'A reinforcement learning algorithm run on OpenAI Gym’s Frozen Lake, CartPole and Lunar Lander.',
      href: 'https://github.com/arunima811/sarsa-open-ai-gym-environments',
    },
    {
      when: '2021',
      title: 'Cloud-agnostic key-value store',
      what: 'Built from scratch, with MapReduce for search and one-click deploy on Google Cloud Functions.',
      href: 'https://github.com/arunima811/cloud-agnostic-KV-store',
    },
    {
      when: '2020',
      title: 'Trust and Donate',
      what: 'A small Python blockchain that lets donors track how NGOs and relief funds use their money.',
      href: 'https://github.com/arunima811/basic-blockchain-api',
    },
    {
      when: '2019',
      title: 'BSE top 10',
      what: 'A CherryPy and Redis app that shows the current top 10 stocks on the Bombay Stock Exchange.',
      href: 'https://github.com/arunima811/BSE-top10',
    },
    {
      when: '2018',
      title: 'IPL data analytics',
      what: 'A web app that visualises insights from IPL cricket data.',
      href: 'https://github.com/arunima811/IPL-Data-Analytics-Webapp',
    },
  ] satisfies SideProject[],

  recognition: [
    { when: '2022', what: 'Scholar, Grace Hopper Celebration' },
    { when: '2021', what: 'Open-source mentor, Grace Hopper Celebration' },
    { when: '2021 – 22', what: 'President, Data Science Club, Indiana University' },
    { when: '', what: 'Winner, Dell Hack-to-Hire Machine Learning Hackathon' },
    {
      when: '2016',
      what: 'Paper (with Aryan Aggrawal): “Channelizing Potential of Indian Youth in Nation Building: Transforming Dreams into Reality”, National Conference, G.B. Pant University of Agriculture & Technology',
    },
  ] satisfies Dated[],

  notwork: {
    greeting: 'Ru, off the clock.',
    photo: { src: '/me-life.jpg', alt: 'Arunima Shukla holding a camera by a stream' } satisfies Photo,
    intro: [
      "Away from data pipelines, I'm a curious generalist. I take photos, I write poetry about life and the technical ideas I can't stop thinking about, and I'm learning to surf.",
      "Long before code, I was a kids' show anchor on All India Radio (2008–2012). In college I drew concept art for a small gaming startup, debated, danced, and started a campus cycle-rental service.",
      'I run on good coffee, books, friends and a bit of adventure.',
    ],
    interests: ['photography', 'poetry', 'learning to surf', 'coffee', 'books', 'debating', 'dance', 'art'],
    links: [{ label: 'X (Twitter)', href: 'https://x.com/Arunima8Shukla' }] satisfies Link[],
  },
};
