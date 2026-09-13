/** @type {import('next').NextConfig} */
const nextConfig = {
  sassOptions: {
    // Carbon's published Sass still uses some patterns the latest dart-sass
    // flags as deprecated. Silence those warnings; they are upstream noise.
    silenceDeprecations: [
      'mixed-decls',
      'global-builtin',
      'import',
      'if-function',
    ],
    quietDeps: true,
  },
  experimental: {
    cpus: 1,
    workerThreads: false,
  },
}

export default nextConfig
