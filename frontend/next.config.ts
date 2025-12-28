import type { NextConfig } from "next";

const nextConfig: any = {
  // output: 'export',  <--- YEH LINE HATA DEIN (Delete it)
  // images: { unoptimized: true }, <--- Isey bhi hata sakte hain agar chahain
  eslint: { ignoreDuringBuilds: true },
};

export default nextConfig;