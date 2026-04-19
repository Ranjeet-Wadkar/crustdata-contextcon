import './globals.css';
import { Inter } from 'next/font/google';
import ThemeToggle from '@/components/ThemeToggle';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'Resa | Research-to-Startup Swarm',
  description: 'Turn research papers into pitch decks using ContextCon agents.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
          <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3rem' }}>
            <h1 style={{ fontSize: '2rem', fontWeight: 900, margin: 0 }}>
              <span style={{ color: 'var(--primary)' }}>Resa</span> Agent Swarm
            </h1>
            <nav style={{ display: 'flex', gap: '1rem' }}>
              <ThemeToggle />
            </nav>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}
