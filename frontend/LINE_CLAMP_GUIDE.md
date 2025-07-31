# Line Clamp Implementation Guide

This document explains the comprehensive line-clamp implementation in the Research Summary Frontend, supporting both standard and webkit properties for maximum browser compatibility.

## Overview

Line-clamp utilities truncate text at a specific number of lines with an ellipsis. This implementation supports both the standard `line-clamp` property and the `-webkit-line-clamp` property for maximum browser compatibility.

## Available Classes

| Class | Lines | Description |
|-------|-------|-------------|
| `.line-clamp-1` | 1 | Single line truncation |
| `.line-clamp-2` | 2 | Two line truncation |
| `.line-clamp-3` | 3 | Three line truncation |
| `.line-clamp-4` | 4 | Four line truncation |
| `.line-clamp-5` | 5 | Five line truncation |
| `.line-clamp-6` | 6 | Six line truncation |

## Browser Compatibility

### Modern Browsers (Chrome 120+, Firefox 120+, Safari 17+, Edge 120+)
- **Primary**: Standard `line-clamp` property
- **Fallback**: `-webkit-line-clamp` property
- **Result**: Multi-line truncation with ellipsis

### Legacy Browsers (Chrome <120, Firefox <120, Safari <17, Edge <120)
- **Primary**: `-webkit-line-clamp` property
- **Result**: Multi-line truncation with ellipsis

### Very Old Browsers (IE, older versions)
- **Fallback**: Single-line truncation with ellipsis
- **Result**: `text-overflow: ellipsis` and `white-space: nowrap`

## Implementation Details

### CSS Implementation

The line-clamp utilities are defined in `src/index.css`:

```css
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;                    /* Standard property */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}
```

### Progressive Enhancement

The implementation uses progressive enhancement:

1. **Standard `line-clamp`** (modern browsers)
2. **`-webkit-line-clamp`** (legacy browsers)
3. **Single-line fallback** (very old browsers)

```css
/* Standard line-clamp support */
@supports (line-clamp: 1) {
  .line-clamp-2 {
    display: block;
    line-clamp: 2;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

/* Fallback for older browsers */
@supports not (line-clamp: 1) {
  @supports not (-webkit-line-clamp: 1) {
    .line-clamp-2 {
      display: block;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
  }
}
```

## Usage Examples

### Paper Title (2 lines)
```tsx
<h4 className="text-white font-semibold mb-2 line-clamp-2">
  {paper.title}
</h4>
```

### Paper Summary (3 lines)
```tsx
<p className="text-purple-200 text-sm line-clamp-3">
  {paper.summary}
</p>
```

### Single Line Truncation
```tsx
<p className="text-purple-200 line-clamp-1">
  {longText}
</p>
```

### Responsive Text Truncation
```tsx
<div className="space-y-2">
  <p className="line-clamp-1 md:line-clamp-2 lg:line-clamp-3">
    {responsiveText}
  </p>
</div>
```

## TypeScript Support

TypeScript declarations are provided in `src/types/css.d.ts`:

```typescript
declare module 'react' {
  interface CSSProperties {
    lineClamp?: string | number;
    WebkitLineClamp?: string | number;
    WebkitBoxOrient?: 'horizontal' | 'vertical' | 'inline-axis' | 'block-axis' | 'inherit';
  }
}
```

## Browser Support Matrix

| Browser | Standard `line-clamp` | `-webkit-line-clamp` | Fallback |
|---------|----------------------|---------------------|----------|
| Chrome 120+ | ✅ | ✅ | - |
| Firefox 120+ | ✅ | ✅ | - |
| Safari 17+ | ✅ | ✅ | - |
| Edge 120+ | ✅ | ✅ | - |
| Chrome <120 | ❌ | ✅ | - |
| Firefox <120 | ❌ | ✅ | - |
| Safari <17 | ❌ | ✅ | - |
| Edge <120 | ❌ | ✅ | - |
| IE 11 | ❌ | ❌ | Single-line |
| Very old browsers | ❌ | ❌ | Single-line |

## Performance Considerations

- **No JavaScript required**: Pure CSS implementation
- **No layout shifts**: Consistent text truncation
- **Fast rendering**: Browser-optimized properties
- **Minimal CSS**: Efficient utility classes

## Best Practices

1. **Use appropriate line counts**: Don't over-truncate important content
2. **Provide full text access**: Consider tooltips or expandable sections
3. **Test across browsers**: Verify fallback behavior
4. **Consider accessibility**: Ensure truncated text doesn't lose meaning

## Troubleshooting

### Common Issues

1. **Text not truncating**
   - Check container width
   - Verify `overflow: hidden` is applied
   - Ensure text is long enough to truncate

2. **Ellipsis not showing**
   - Verify `text-overflow: ellipsis` is applied
   - Check browser compatibility
   - Ensure proper CSS cascade

3. **Multiple lines not working**
   - Check browser support for `-webkit-line-clamp`
   - Verify `-webkit-box-orient: vertical` is set
   - Test with different line counts

### Debug Steps

1. **Browser Developer Tools**
   - Inspect computed styles
   - Check which properties are applied
   - Verify CSS cascade order

2. **Test with Different Browsers**
   - Chrome DevTools device simulation
   - Firefox Responsive Design Mode
   - Safari Web Inspector

3. **Validate CSS**
   - Check for syntax errors
   - Verify property values
   - Test with minimal example

## Future Enhancements

- **CSS Container Queries**: For more responsive line-clamp
- **Custom Properties**: Dynamic line counts via CSS variables
- **JavaScript Fallback**: For very old browsers if needed
- **Accessibility Improvements**: Better screen reader support 