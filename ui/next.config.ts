import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  // Enable output line if stuff gets bricked
  // output: 'export', // Outputs a Single-Page Application (SPA)
  distDir: 'build', // Changes the build output directory to `build`

  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://humanize.live/api/:path*', // Flask's address
      },
    ];
  },
}

export default nextConfig
