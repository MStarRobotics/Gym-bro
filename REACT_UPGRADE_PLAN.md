# React Version Alignment Plan

Goal: Align React versions across monorepo workspaces to avoid dev/test tooling
and runtime mismatches (root Vite app uses React 19 while Next.js apps use React
18).

Option A: Upgrade Next.js apps to React 19 (recommended if feasible)

- Pros: Keep the latest features and allow root Vite app to use React 19 without
  workarounds.
- Cons: Need to validate Next.js support; ensure all dependencies support
  React 19.

Option B: Downgrade Vite app to React 18

- Pros: Smaller change in Next apps; many libs still support React 18.
- Cons: Loses ability to use React 19 features in Vite app.

Steps to evaluate Option A (upgrade Next apps to React 19):

1. Check Next.js compatibility: confirm `next@14` is compatible with React 19;
   check Next.js release notes.
2. Identify relevant dependency updates: `@types/react`, `@types/react-dom`,
   `lucide-react` and others; pin to versions supporting React 19.
3. Update `gymgenius-monorepo/apps/admin-panel/package.json` and
   `.../nutritionist-panel/package.json` to `react@^19` and `react-dom@^19`, and
   update `@types/react` accordingly.
4. Run `npm ci` and `npm run type-check` `npm run lint` & `npm run build` for
   the Next apps to surface compile/time issues.
5. Run unit tests and e2e tests; fix runtime or type errors caused by breaking
   changes.

Steps to evaluate Option B (downgrade Vite app to React 18):

1. Update root `package.json` to `react@^18` and `react-dom@^18`.
2. Run `npm ci`, run `npx tsc -p tsconfig.json` and `npm run test` and fix any
   regressions.
3. If third-party libs used rely on React 19, update or pin them to compatible
   versions.

Fallback plan:

- If Next.js or third-party packages cannot be upgraded to React 19 easily,
  consider temporarily pinning dev test libs to versions that support both React
  18/19 (like the current `dev_tool_versions.json`) and add a longer-term plan
  to align the versions.

Recommendation:

- Perform Option A (upgrade Next apps to React 19) in a separate PR with a
  migration branch and CI run: run `report-react-versions` and `audit-devtools`
  in PR to confirm changes.
