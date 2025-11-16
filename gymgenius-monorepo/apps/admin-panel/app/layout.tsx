import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'GymGenius Admin Panel',
  description: 'System administration and analytics',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
