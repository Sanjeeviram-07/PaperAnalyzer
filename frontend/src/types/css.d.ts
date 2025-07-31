// CSS property declarations for custom utilities
declare module 'react' {
  interface CSSProperties {
    // Standard line-clamp property
    lineClamp?: string | number;
    
    // Webkit line-clamp properties
    WebkitLineClamp?: string | number;
    WebkitBoxOrient?: 'horizontal' | 'vertical' | 'inline-axis' | 'block-axis' | 'inherit';
  }
}

// Global CSS custom properties
declare global {
  namespace JSX {
    interface IntrinsicAttributes {
      className?: string;
    }
  }
}

export {}; 