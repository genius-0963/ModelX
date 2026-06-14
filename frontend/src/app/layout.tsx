import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import Link from 'next/link'
import { 
  LayoutDashboard, 
  BrainCircuit, 
  AlertTriangle, 
  Target, 
  Wrench, 
  Dna, 
  FileText, 
  Activity 
} from 'lucide-react'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'ModelX Dashboard',
  description: 'Autonomous Agent Platform',
}

const navItems = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Reflections', href: '/reflections', icon: BrainCircuit },
  { name: 'Failures', href: '/failures', icon: AlertTriangle },
  { name: 'Strategies', href: '/strategies', icon: Target },
  { name: 'Skills', href: '/skills', icon: Wrench },
  { name: 'Meta Learning', href: '/meta-learning', icon: Dna },
  { name: 'Reports', href: '/reports', icon: FileText },
  { name: 'System Health', href: '/system-health', icon: Activity },
]

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gray-50 text-gray-900 flex h-screen overflow-hidden`}>
        {/* Sidebar */}
        <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
          <div className="h-16 flex items-center px-6 border-b border-gray-200">
            <h1 className="text-xl font-bold text-indigo-600 flex items-center gap-2">
              <BrainCircuit className="w-6 h-6" />
              ModelX
            </h1>
          </div>
          <nav className="flex-1 overflow-y-auto py-4">
            <ul className="space-y-1 px-3">
              {navItems.map((item) => {
                const Icon = item.icon
                return (
                  <li key={item.name}>
                    <Link
                      href={item.href}
                      className="flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md text-gray-700 hover:text-indigo-600 hover:bg-gray-50"
                    >
                      <Icon className="w-5 h-5 text-gray-400" />
                      {item.name}
                    </Link>
                  </li>
                )
              })}
            </ul>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto">
          {children}
        </main>
      </body>
    </html>
  )
}
