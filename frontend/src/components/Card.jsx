import React from 'react';

export function Card({ children, className = '', ...props }) {
    return (
      <div
        className={`rounded-lg shadow-md border border-gray-300 p-4 bg-white hover:shadow-lg transition-shadow ${className}`}
        {...props}
      >
        {children}
      </div>
    );
  }

  export function CardContent({ children, className = '', ...props }) {
    return (
      <div className={`mt-2 text-gray-700 ${className}`} {...props}>
        {children}
      </div>
    );
  }
