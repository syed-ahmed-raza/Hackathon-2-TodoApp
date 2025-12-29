import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  async rewrites() {
    return [
      {
        
        source: '/api/proxy/:path*',
      
        destination: 'https://hackathon-2-todoapp.onrender.com/:path*',
      },
    ];
  },
};

export default nextConfig;