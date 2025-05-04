import type { Metadata } from 'next';
import './globals.css'
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { Home } from "lucide-react"

export const metadata: Metadata = {
    title: 'Humanize',
    description: 'Humanize Web App',
}

export default function RootLayout({
    children,
  }: {
    children: React.ReactNode
  }) {
    return (
        <html lang="en">  
            <body className="bg-[#E7FFE4]">
                <div id="root">
                  <div className="fixed top-4 left-4 z-50">
                    <Link href="/home">
                      <Button variant="outline" size="sm" className="shadow-md gap-2 bg-[#44c4a1]">
                        <Home className="h-4 w-4" />
                        <span>Home</span>
                      </Button>
                    </Link>
                  </div>
                  {children}
                </div>
            </body>
        </html>
    )
  }