"use client";
import React from 'react';

export default function NeoButton({ 
  children, 
  onClick, 
  disabled = false,
  fullWidth = false 
}: { 
  children: React.ReactNode; 
  onClick?: () => void; 
  disabled?: boolean;
  fullWidth?: boolean;
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        width: fullWidth ? '100%' : 'auto',
        position: 'relative',
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'var(--border-color)',
        borderRadius: '8px',
        border: 'none',
        padding: 0,
        cursor: disabled ? 'not-allowed' : 'pointer',
        opacity: disabled ? 0.5 : 1,
      }}
      className="group"
    >
      <span
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: 'var(--primary)',
          color: '#000',
          fontWeight: 'bold',
          padding: '0.6rem 1.2rem',
          borderRadius: '8px',
          border: '2px solid var(--border-color)',
          transform: 'translateY(-4px)',
          transition: 'transform 0.1s ease',
          width: '100%'
        }}
        onMouseOver={(e) => {
          if (!disabled) {
            e.currentTarget.style.transform = 'translateY(-6px)';
          }
        }}
        onMouseOut={(e) => {
          if (!disabled) {
            e.currentTarget.style.transform = 'translateY(-4px)';
          }
        }}
        onMouseDown={(e) => {
          if (!disabled) {
            e.currentTarget.style.transform = 'translateY(-2px)';
          }
        }}
        onMouseUp={(e) => {
          if (!disabled) {
            e.currentTarget.style.transform = 'translateY(-6px)';
          }
        }}
      >
        {children}
      </span>
    </button>
  );
}
