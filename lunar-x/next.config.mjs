import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/** @type {import('next').NextConfig} */
const nextConfig = {
  async headers() {
    return [{ source: '/:path*', headers: [
      { key: 'X-Content-Type-Options', value: 'nosniff' },
      { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
      { key: 'Strict-Transport-Security', value: 'max-age=63072000' },
    ] }];
  },
  sassOptions: {
    includePaths: [path.join(__dirname, 'node_modules')],
    silenceDeprecations: [
      'mixed-decls',
      'global-builtin',
      'import',
      'if-function',
    ],
    quietDeps: true,
  },
};

export default nextConfig;
