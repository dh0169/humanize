import type { Metadata } from 'next';
import './globals.css'

export const metadata: Metadata = {
    title: 'React App',
    description: 'Website created with Next.js.',
}

export default function RootLayout({
    children,
  }: {
    children: React.ReactNode
  }) {
    return (
        <html lang="en">  
            <body className="bg-[#E7FFE4]">
                <div id="root">{children}</div>
            </body>
        </html>
    )
  }