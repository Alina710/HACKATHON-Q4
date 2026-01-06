# UI Elements Documentation

## Overview
This document provides comprehensive documentation for all UI elements implemented in the Docusaurus UI upgrade.

## Color Palette

### Primary Colors
- **Primary**: #2563eb (Modern blue/indigo-600)
- **Dark variant**: #1d4ed8 (indigo-700)
- **Darker variant**: #1e40af (indigo-800)
- **Darkest variant**: #1e3a8a (indigo-900)
- **Light variant**: #3b82f6 (blue-500)
- **Lighter variant**: #60a5fa (blue-400)
- **Lightest variant**: #93c5fd (blue-300)

### Dark Mode Colors
- **Primary**: #60a5fa (blue-400)
- **Dark variant**: #3b82f6 (blue-500)
- **Darker variant**: #2563eb (blue-600)
- **Light variant**: #93c5fd (blue-300)
- **Lighter variant**: #bfdbfe (blue-200)
- **Lightest variant**: #dbeafe (blue-100)

## Typography

### Font Stack
- **Primary**: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, sans-serif, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif

### Font Sizes
- **Base size**: 17px
- **H1**: 2.3rem
- **H2**: 1.8rem
- **H3**: 1.5rem
- **H4**: 1.25rem
- **H5**: 1.1rem
- **H6**: 1rem

### Line Height
- **Base line height**: 1.65
- **Heading line height**: 1.25

## Components

### 1. Buttons
- **Primary Button**: `.button.button--primary` - Solid blue background with white text
- **Secondary Button**: `.button.button--secondary` - Light gray background with dark text
- **Hover Effects**: Subtle elevation and shadow for depth
- **Focus States**: 2px solid primary color outline

### 2. Callouts/Admonitions
- **Primary**: `.alert.alert--primary` - Blue accent border
- **Success**: `.alert.alert--success` - Green accent border
- **Info**: `.alert.alert--info` - Blue accent border
- **Warning**: `.alert.alert--warning` - Yellow accent border
- **Danger**: `.alert.alert--danger` - Red accent border

### 3. Code Blocks
- **Background**: Light gray in light mode, dark gray in dark mode
- **Border**: Subtle border with rounded corners
- **Line Highlighting**: Blue-tinted background for highlighted lines
- **Copy Button**: Hover-activated copy button in top-right corner

### 4. Tables
- **Responsive**: Auto-wraps in scrollable container on small screens
- **Striped**: Alternating row styling for readability
- **Bordered**: Clean border styling for clarity
- **Dark Mode**: Appropriate color adjustments

### 5. Images & Media
- **Rounded Corners**: Subtle 0.5rem border-radius
- **Shadow**: Soft box-shadow for depth
- **Captions**: Italicized, muted color text below images
- **Centering**: `.figure--center` class for centered images

### 6. Navigation
- **Navbar**: Subtle shadow with hover enhancement
- **Sidebar**: Improved hover states and active indicators
- **Breadcrumbs**: Better visual hierarchy and spacing
- **Mobile Menu**: Optimized for touch interaction

## Responsive Design

### Breakpoints
- **Mobile**: max-width: 996px
- **Extra small**: max-width: 575px
- **Tablet**: min-width: 768px and max-width: 996px

### Mobile Adjustments
- **Font sizes**: Reduced for better screen utilization
- **Spacing**: Adjusted for touch-friendly interaction
- **Navigation**: Collapsible and optimized for small screens

## Accessibility Features

### Color Contrast
- All color combinations meet WCAG 2.1 AA standards
- Minimum 4.5:1 contrast ratio for normal text

### Focus Indicators
- **Outline**: 2px solid primary color
- **Offset**: 2px for visibility
- **Applies to**: All interactive elements

### Keyboard Navigation
- Logical tab order following visual flow
- Visible focus states for all interactive elements
- Skip links for screen reader users

## Custom CSS Variables

### Available Variables
- `--ifm-color-primary`: Primary brand color
- `--ifm-font-family-base`: Base font family
- `--ifm-font-size-base`: Base font size
- `--ifm-line-height-base`: Base line height
- `--ifm-heading-font-weight`: Heading font weight

## Usage Examples

### Creating a Primary Button
```html
<a class="button button--primary" href="/link">Primary Action</a>
```

### Creating an Info Callout
```md
:::info
This is an informational callout with the new styling.
:::
```

### Centering an Image with Caption
```html
<div class="figure figure--center">
  <img class="figure__img" src="/path/to/image.jpg" alt="Description" />
  <div class="figure__caption">Image caption text</div>
</div>
```

## Integration Notes
- All changes are additive and don't break existing functionality
- Custom CSS is contained in `src/css/custom.css`
- All components maintain Docusaurus compatibility
- Dark mode support is automatic and complete