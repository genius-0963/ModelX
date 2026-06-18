import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// Note: Next.js middleware runs on the Edge runtime and doesn't have access to localStorage
// We only check for basic authentication cookie if we use cookies, but here we're using localStorage
// For a robust implementation, we would set a cookie during login and check it here.

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  
  // Public paths that don't require authentication
  const publicPaths = ['/login', '/register', '/api', '/_next']
  const isPublicPath = publicPaths.some(path => pathname.startsWith(path)) || pathname === '/'
  
  // As localStorage is not accessible in Edge Middleware, real protection happens via:
  // 1. React Query error handler intercepting 401s and redirecting
  // 2. Client-side layout checks
  // However, we can handle the home page redirect here
  if (pathname === '/') {
    return NextResponse.redirect(new URL('/dashboard', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}
