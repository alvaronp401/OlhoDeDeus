'use client';

export const ScanlineOverlay = () => {
  return (
    <div 
      className="pointer-events-none fixed inset-0 z-50 pointer-events-none"
      style={{
        background: `linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.1) 50%),
                     linear-gradient(90deg, rgba(255, 0, 0, 0.03), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.03))`,
        backgroundSize: '100% 4px, 3px 100%'
      }}
    />
  );
};
