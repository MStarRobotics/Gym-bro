/* eslint-disable no-console, @typescript-eslint/explicit-function-return-type */
import fs from 'node:fs';
import path from 'node:path';

/**
 * Read JSON file and return parsed object or null on error.
 * @param {string} p - Path to JSON file
 * @returns {Record<string, any> | null}
 */
function readJson(p) {
  try {
    return JSON.parse(fs.readFileSync(p, 'utf8'));
  } catch (err) {
    // Return null and log only at debug level to keep output clean
    if (process.env.DEBUG_AUDIT) {
      console.debug('readJson error', err);
    }
    return null;
  }
}

const repoRoot = process.cwd();
const rootPkg = readJson(path.join(repoRoot, 'package.json')) || {};
const monorepoPkg =
  readJson(path.join(repoRoot, 'gymgenius-monorepo', 'package.json')) || {};

const keys = [
  'vitest',
  'vitest-axe',
  '@testing-library/react',
  '@testing-library/jest-dom',
  '@testing-library/user-event',
  'axe-core',
  'eslint-plugin-jsx-a11y',
  'jsdom',
];

const places = [
  { name: 'root', pkg: rootPkg },
  { name: 'gymgenius-monorepo', pkg: monorepoPkg },
];

// Also gather apps in monorepo
const appsDir = path.join(repoRoot, 'gymgenius-monorepo', 'apps');
if (fs.existsSync(appsDir)) {
  const apps = fs.readdirSync(appsDir);
  for (const a of apps) {
    const p = path.join(appsDir, a, 'package.json');
    if (fs.existsSync(p)) {
      places.push({ name: `monorepo/apps/${a}`, pkg: readJson(p) });
    }
  }
}

console.log('DevDeps version matrix for selected packages:');
const matrix = {};
for (const pl of places) {
  matrix[pl.name] = {};
  for (const k of keys) {
    matrix[pl.name][k] =
      pl.pkg?.devDependencies?.[k] || pl.pkg?.dependencies?.[k] || null;
  }
}
console.table(matrix);

// Report mismatches
console.log('\nMismatches detected:');
for (const k of keys) {
  const versions = new Set();
  for (const p of places) {
    if (matrix[p.name][k]) versions.add(matrix[p.name][k]);
  }
  if (versions.size > 1) {
    console.log(
      `- ${k}: differs across packages (${Array.from(versions).join(', ')})`
    );
  }
}

console.log('\nAudit complete.');
