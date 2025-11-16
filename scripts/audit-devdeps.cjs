const fs = require('fs');
const path = require('path');

function readJson(p) {
  try {
    return JSON.parse(fs.readFileSync(p, 'utf8'));
  } catch (e) {
    return null;
  }
}

const repoRoot = path.resolve(__dirname, '..');
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
  apps.forEach((a) => {
    const p = path.join(appsDir, a, 'package.json');
    if (fs.existsSync(p)) {
      places.push({ name: `monorepo/apps/${a}`, pkg: readJson(p) });
    }
  });
}

console.log('DevDeps version matrix for selected packages:');
const matrix = {};
places.forEach((pl) => {
  matrix[pl.name] = {};
  keys.forEach((k) => {
    matrix[pl.name][k] =
      (pl.pkg.devDependencies && pl.pkg.devDependencies[k]) ||
      (pl.pkg.dependencies && pl.pkg.dependencies[k]) ||
      null;
  });
});
console.table(matrix);

// Report mismatches
console.log('\nMismatches detected:');
let mismatchFound = false;
for (const k of keys) {
  const versions = new Set();
  for (const p of places) {
    if (matrix[p.name][k]) versions.add(matrix[p.name][k]);
  }
  if (versions.size > 1) {
    mismatchFound = true;
    console.log(
      `- ${k}: differs across packages (${Array.from(versions).join(', ')})`
    );
  }
}

if (mismatchFound) {
  console.error('\nDev dependencies mismatch found.');
  process.exit(1);
}

console.log('\nAudit complete — no mismatches found.');
