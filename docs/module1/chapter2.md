---
title: Chapter 2 - Configuration and Customization
sidebar_label: Chapter 2
---

# Chapter 2: Configuration and Customization

## Overview

In this chapter, we'll explore how to configure and customize your Docusaurus site. Understanding the configuration options will allow you to tailor your documentation site to your specific needs.

## Configuration File

The main configuration file for Docusaurus is `docusaurus.config.js`. This file contains all the settings for your site, including metadata, themes, plugins, and more.

### Basic Configuration

Here's a breakdown of the key configuration options:

- **title**: The title of your site, displayed in the browser tab and navbar
- **tagline**: A short description of your site
- **url**: The URL of your site
- **baseUrl**: The base URL of your site
- **favicon**: Path to your site's favicon

### Theme Configuration

The `themeConfig` section allows you to customize the appearance and behavior of your site:

```javascript
themeConfig: {
  navbar: {
    title: 'My Site',
    logo: {
      alt: 'Logo',
      src: 'img/logo.svg',
    },
  },
  footer: {
    style: 'dark',
    links: [...],
    copyright: 'Copyright',
  },
}
```

## Navigation and Sidebars

Navigation in Docusaurus is handled through two main components:

1. **Navbar**: The top navigation bar
2. **Sidebar**: The navigation menu for documentation pages

### Sidebar Configuration

The sidebar structure is defined in `sidebars.js`. You can organize your documentation into categories and subcategories:

```javascript
module.exports = {
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
```

## Customizing the Layout

Docusaurus allows extensive customization of the layout through:

- **CSS**: Override default styles in `src/css/custom.css`
- **Components**: Create custom React components in `src/components/`
- **Pages**: Add custom pages in `src/pages/`

### Custom CSS

You can add custom styles to `src/css/custom.css`. Docusaurus uses CSS modules and supports both regular CSS and SCSS.

```css
/* Custom styles */
.hero__title {
  color: #25c2a0;
}

/* Override Docusaurus default styles */
.docusaurus-highlight-code-line {
  background-color: rgba(0, 0, 0, 0.1);
  display: block;
  margin: 0 calc(-1 * var(--ifm-pre-padding));
  padding: 0 var(--ifm-pre-padding);
}
```

## Adding Content

Docusaurus supports various content types:

- **Markdown files**: For documentation pages
- **MDX files**: Markdown with JSX components
- **Blog posts**: Articles with publication dates
- **Pages**: Standalone React components

### Frontmatter

Each Markdown file can include frontmatter at the top to specify metadata:

```yaml
---
title: Page Title
sidebar_label: Sidebar Text
description: SEO description
keywords: [keyword1, keyword2]
---
```

In the next chapter, we'll look at advanced features and deployment options.