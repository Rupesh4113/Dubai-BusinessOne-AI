/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  ...(process.env.BUILD_STANDALONE === "true" ? { output: "standalone" } : {}),
  ...(process.env.BACKEND_URL
    ? {
        async rewrites() {
          return [
            {
              source: "/api/:path*",
              destination: `${process.env.BACKEND_URL}/api/:path*`,
            },
          ];
        },
      }
    : {}),
};

module.exports = nextConfig;
