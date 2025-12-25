# Quickstart Guide: Docusaurus Documentation Site

## Prerequisites

- Node.js (version 18.0 or higher)
- npm (version 8.0 or higher) or yarn

## Installation

### 1. Create a new Docusaurus project

```bash
npx create-docusaurus@latest my-website classic
cd my-website
```

### 2. Install additional dependencies (if needed)

```bash
npm install
```

### 3. Create the module directory structure

```bash
mkdir -p docs/module1
```

### 4. Create Module 1 with 3 chapters

Create the following files in the `docs/module1/` directory:

- `docs/module1/chapter1.md`
- `docs/module1/chapter2.md`
- `docs/module1/chapter3.md`

## Configuration

### 1. Update `docusaurus.config.js`

```javascript
// docusaurus.config.js
module.exports = {
  title: 'Technical Book Documentation',
  tagline: 'Comprehensive guide to technical topics',
  url: 'https://your-username.github.io',
  baseUrl: '/my-website/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'your-username', // Usually your GitHub org/user name
  projectName: 'my-website', // Usually your repo name
  trailingSlash: false,

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/your-username/my-website/edit/main/',
        },
        blog: false, // Disable blog if not needed
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Technical Book',
        logo: {
          alt: 'My Site Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Documentation',
          },
          {
            href: 'https://github.com/your-username/my-website',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Documentation',
                to: '/docs/module1/chapter1',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/your-username/my-website',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Technical Book. Built with Docusaurus.`,
      },
      prism: {
        theme: require('prism-react-renderer/themes/github'),
        darkTheme: require('prism-react-renderer/themes/dracula'),
      },
    }),
};
```

### 2. Configure sidebar navigation in `sidebars.js`

```javascript
// sidebars.js
/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1',
      items: [
        'module1/chapter1',
        'module1/chapter2',
        'module1/chapter3',
      ],
    },
  ],
};

module.exports = sidebars;
```

### 3. Create sample chapter files

#### `docs/module1/chapter1.md`
```markdown
---
title: Chapter 1 - Introduction
sidebar_label: Chapter 1
---

# Chapter 1: Introduction

This is the first chapter of Module 1.
```

#### `docs/module1/chapter2.md`
```markdown
---
title: Chapter 2 - Core Concepts
sidebar_label: Chapter 2
---

# Chapter 2: Core Concepts

This is the second chapter of Module 1.
```

#### `docs/module1/chapter3.md`
```markdown
---
title: Chapter 3 - Advanced Topics
sidebar_label: Chapter 3
---

# Chapter 3: Advanced Topics

This is the third chapter of Module 1.
```

## Development

### Start the development server

```bash
npm run start
```

This command starts a local development server and opens a browser window. Most changes are reflected live without having to restart the server.

### Build the static site

```bash
npm run build
```

The build command generates static HTML files in the `build/` directory, ready for deployment.

### Deploy to GitHub Pages

```bash
GIT_USER=<Your GitHub username> npm run deploy
```

## Customization

### Adding more modules

To add more modules:

1. Create a new directory in `docs/` (e.g., `docs/module2/`)
2. Add your chapter files to the new module directory
3. Update `sidebars.js` to include the new module in the navigation

### Adding custom styles

Custom styles can be added to `src/css/custom.css` to override default Docusaurus styling.

## Directory Structure

After setup, your project should look like:

```
my-website/
├── docs/
│   ├── intro.md
│   └── module1/
│       ├── chapter1.md
│       ├── chapter2.md
│       └── chapter3.md
├── src/
│   ├── components/
│   ├── css/
│   │   └── custom.css
│   └── pages/
│       └── index.js
├── static/
│   └── img/
├── docusaurus.config.js
├── package.json
├── sidebars.js
└── yarn.lock (or package-lock.json)
```