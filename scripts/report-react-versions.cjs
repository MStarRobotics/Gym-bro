const fs = require('node:fs');
const path = require('node:path');

function readJson(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

const repoRoot = path.resolve(__dirname, '..');
const roots = [
  path.join(repoRoot, 'package.json'),
  path.join(repoRoot, 'gymgenius-monorepo', 'package.json'),
];
// gather monorepo apps
const appsDir = path.join(repoRoot, 'gymgenius-monorepo', 'apps');
if (fs.existsSync(appsDir)) {
  const apps = fs.readdirSync(appsDir);
  for (const a of apps) {
    const p = path.join(appsDir, a, 'package.json');
    if (fs.existsSync(p)) roots.push(p);
  }
}

const versionsMap = {};
for (const r of roots) {
  const pkg = readJson(r);
  const v =
    (pkg.dependencies && pkg.dependencies.react) ||
    (pkg.devDependencies && pkg.devDependencies.react) ||
    null;
  versionsMap[path.relative(repoRoot, r)] = v;
}

console.log('React versions across workspaces:');
console.table(versionsMap);

let mismatched = false;
const uniqueVersions = new Set(
  Object.values(versionsMap).filter((v) => v !== null)
);
const hasMultipleVersions = uniqueVersions.size > 1;
if (hasMultipleVersions) {
  mismatched = true;
  console.warn('React version mismatch detected across workspaces');
}

if (mismatched) process.exit(1);
