import type { NextConfig } from "next";

// Yahan hum ': any' laga rahe hain taake Red Lines khatam ho jayen
const nextConfig: any = {
  output: 'export',
  eslint: { ignoreDuringBuilds: true },
  images: { unoptimized: true },
};

export default nextConfig;