---
title: Chapter 1 - Getting Started with Docusaurus
sidebar_label: Chapter 1
---

# Chapter 1: Getting Started with Docusaurus

## Introduction

Welcome to the first chapter of Module 1! This chapter will introduce you to Docusaurus and help you understand its core concepts.

Docusaurus is a modern static site generator that helps you build beautiful documentation websites. It's designed to make it easy for you to write and maintain documentation while providing a great experience for your readers.

## What is Docusaurus?

Docusaurus is an optimized site generator in React. It helps you build static websites that are fast, accessible, and SEO-friendly. The key features include:

- **Fast**: Docusaurus generates static HTML, CSS, and JavaScript that are highly optimized
- **Document-centric**: Designed specifically for documentation with built-in features like versioning and search
- **Customizable**: Easy to customize the layout, styling, and behavior
- **Developer-friendly**: Great tooling and development experience

## Why Choose Docusaurus?

Docusaurus offers several advantages for creating documentation:

1. **Built-in search**: Integration with Algolia for powerful search capabilities
2. **Versioning**: Easy to maintain multiple versions of your documentation
3. **Internationalization**: Built-in support for translating your documentation
4. **Pluggable architecture**: Extensible with plugins for additional functionality
5. **Markdown support**: Write your content in familiar Markdown format

## Installation

To create a new Docusaurus project, you can use the following command:

```bash
npx create-docusaurus@latest my-website classic
```

This command will set up a new Docusaurus project with the classic template, which includes a docs section, a blog, and a few example pages.

## Project Structure

A typical Docusaurus project looks like this:

```
my-website/
├── blog/
├── docs/
├── src/
│   ├── components/
│   ├── css/
│   └── pages/
├── static/
├── docusaurus.config.js
├── package.json
└── sidebars.js
```

In the next chapter, we'll explore the configuration options and customization possibilities in more detail.