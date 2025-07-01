/** @type {import('next').NextConfig} */
const nextConfig = {
  rewrites: async () => {
    return [
      {
        source: "/api/:path*",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://127.0.0.1:8000/api/:path*"
            : "https://dearmandi-backend-git-staging-rahulg-infiswifts-projects.vercel.app/api/:path*", // Production environment
      },
      {
        source: "/docs",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://127.0.0.1:8000/docs"
            : "https://dearmandi-backend-git-staging-rahulg-infiswifts-projects.vercel.app/docs",
      },
      {
        source: "/openapi.json",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://127.0.0.1:8000/openapi.json"
            : "https://dearmandi-backend-git-staging-rahulg-infiswifts-projects.vercel.app/openapi.json",
      },
    ];
  },
};

module.exports = nextConfig;
