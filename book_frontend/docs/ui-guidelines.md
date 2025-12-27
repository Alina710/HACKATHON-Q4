---
title: UI Guidelines
---

# UI Guidelines

This document provides guidelines for maintaining consistency with the new UI design system.

## Color System

### Primary Colors
Use the primary color for main actions and important elements:
- Primary: `#2563eb` (Modern blue)
- Dark variant: `#1d4ed8`
- Light variant: `#3b82f6`

### Color Usage
- **Primary**: Primary buttons, links, and important interactive elements
- **Secondary**: Secondary buttons and supporting elements
- **Success**: Positive feedback and success states
- **Warning**: Warnings and cautionary information
- **Danger**: Errors and destructive actions

## Typography

### Font Stack
The system uses a modern, system font stack:
```
system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, sans-serif, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif
```

### Hierarchy
- **H1**: 2.3rem (Page titles)
- **H2**: 1.8rem (Section headings)
- **H3**: 1.5rem (Subsection headings)
- **H4**: 1.25rem (Minor headings)
- **Body**: 17px base size with 1.65 line height

## Components

### Buttons
Use buttons for actions:

```md
[Primary Button](/link) <!-- Creates primary button -->
[Secondary Button](/link) <!-- Creates secondary button -->
```

### Admonitions
Use admonitions for special content:

```md
:::note
Use this for general notes.
:::

:::tip
Use this for helpful tips.
:::

:::info
Use this for informational content.
:::

:::caution
Use this for warnings.
:::

:::danger
Use this for critical warnings.
:::
```

### Code Blocks
- Use syntax highlighting: ` ```js ` for JavaScript
- Add titles: ` ```js title="filename.js" `
- Highlight lines: ` ```js {2,4-6} `

## Layout Guidelines

### Spacing
- Use consistent spacing with the provided defaults
- Maintain visual hierarchy with appropriate margins
- Respect responsive design on all screen sizes

### Images
- Use the figure class for images with captions:
```
<div class="figure figure--center">
  <img src="/path/to/image.jpg" alt="Description" />
  <div class="figure__caption">Caption text</div>
</div>
```

## Accessibility

### Color Contrast
- All text meets WCAG 2.1 AA contrast requirements
- Use high-contrast combinations for readability

### Focus States
- All interactive elements have visible focus indicators
- Focus states are 2px solid primary color with 2px offset

### Navigation
- Maintain logical tab order
- Use skip links for main content
- Ensure all functionality is keyboard accessible

## Responsive Design

### Breakpoints
- **Mobile**: Up to 996px
- **Tablet**: 768px - 996px
- **Desktop**: Above 996px

### Mobile-First Approach
- Design for mobile first, then enhance for larger screens
- Ensure touch targets are at least 44px
- Use appropriate spacing for touch interactions

## Dark Mode

The design automatically adapts to dark mode preferences:
- All color schemes have appropriate dark mode alternatives
- Text remains readable in both modes
- Images and media adapt appropriately

## Best Practices

### Consistency
- Maintain consistent styling across all pages
- Use components as intended for consistency
- Follow established patterns

### Performance
- Images should be optimized for web
- Use lazy loading where appropriate
- Minimize custom CSS additions

### Testing
- Test on multiple devices and screen sizes
- Verify accessibility with keyboard navigation
- Check contrast ratios with tools