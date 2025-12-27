---
title: UI Upgrade Verification
---

# UI Upgrade Verification

This document verifies that all existing content types render correctly with the new UI styling.

## Typography Tests

### Headings
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6

### Text Elements
Normal text, **bold text**, *italic text*, ***bold italic text***, `inline code`.

### Lists
- Unordered item 1
- Unordered item 2
  - Nested item

1. Ordered item 1
2. Ordered item 2
   1. Nested ordered item

## Code Block Tests

### Simple Code Block
```js
function helloWorld() {
  console.log('Hello, world!');
}
```

### Code Block with Line Highlighting
```js title="src/components/HelloWorld.js" {2}
import React from 'react';

function HelloWorld() {
  return <div>Hello World!</div>;
}

export default HelloWorld;
```

## Admonitions (Callouts)

:::note
This is a note admonition.
:::

:::tip
This is a tip admonition.
:::

:::info
This is an info admonition.
:::

:::caution
This is a caution admonition.
:::

:::danger
This is a danger admonition.
:::

## Tables

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |

## Images

![Docusaurus Logo](/img/logo.svg)

## Links

[Documentation Home](/docs/intro)
[External Link](https://docusaurus.io/)

## Buttons

[Button Link Example](/docs/intro)

## Blockquotes

> This is a blockquote.
> It can span multiple lines.

## Horizontal Rule

---

## Math (if supported)

Inline math: $x = y + z$

Block math:
<!--
$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$
-->

## Tabs (if supported)

<Tabs>
  <TabItem value="js" label="JavaScript">
    ```js
    console.log('Hello, world!');
    ```
  </TabItem>
  <TabItem value="py" label="Python">
    ```py
    print('Hello, world!')
    ```
  </TabItem>
</Tabs>