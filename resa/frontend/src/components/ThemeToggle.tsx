"use client";
import React from 'react';

export default function ThemeToggle() {
  return (
    <button 
      onClick={() => {
        document.documentElement.classList.toggle('dark');
        if (document.documentElement.getAttribute('data-theme') === 'dark') {
          document.documentElement.setAttribute('data-theme', 'light');
        } else {
          document.documentElement.setAttribute('data-theme', 'dark');
        }
      }}
      className="neo-input"
      style={{ cursor: 'pointer', padding: '0.5rem 1rem', width: 'auto' }}
    >
      Toggle Theme
    </button>
  );
}
