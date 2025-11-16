# Development Tools Version Matrix

This file lists the recommended versions for development/test tooling to keep
consistent across the monorepo.

- vitest: ^4.0.9
- vitest-axe: ^0.1.0
- @testing-library/react: ^16.3.0
- @testing-library/jest-dom: ^6.9.1
- @testing-library/user-event: ^14.6.1
- axe-core: ^4.11.0
- eslint-plugin-jsx-a11y: ^6.10.2

Notes:

- The monorepo contains multiple web workspaces (Vite client and Next.js apps).
  Some apps may use different React versions (React 19 in the Vite workspace and
  React 18 in Next apps). Test tooling versions are chosen to be compatible with
  both React versions to avoid peer dependency conflicts.
- If you need to upgrade one of these dev tools, update this file and the
  package.json files in the root and `gymgenius-monorepo` accordingly.

How to use:

- Run `npm ci` in the root and `cd gymgenius-monorepo && npm ci` to install the
  dev tooling versions defined in each package.json.
- If you maintain a common tool version, consider adding a dedicated script to
  sync versions across package.json files.
