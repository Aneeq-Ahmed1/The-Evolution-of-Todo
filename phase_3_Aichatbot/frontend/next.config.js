/** @type {import('next').NextConfig} */
const nextConfig = {
  // Standard Next.js configuration for Vercel deployment
  distDir: '.next', // Default build directory
  // Remove output: 'export' since this app likely needs server functionality
}

module.exports = nextConfig