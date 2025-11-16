const fs = require('node:fs');
const path = require('node:path');

function readJson(p) {
  const raw = fs.readFileSync(p, 'utf8');
  return JSON.parse(raw);
}

function writeJson(p, obj) {
  fs.writeFileSync(p, JSON.stringify(obj, null, 2) + '\n', 'utf8');
}

const repoRoot = path.resolve(__dirname, '..');
const versionFile = path.join(repoRoot, 'dev_tool_versions.json');
if (!fs.existsSync(versionFile)) {
  console.error('dev_tool_versions.json not found; abort');
  process.exit(1);
}
const versions = readJson(versionFile);
if (!versions) {
  console.error('Invalid dev_tool_versions.json');
  process.exit(1);
}

const apply = process.argv.includes('--apply');

function tryUpdate(pkgPath) {
  const pkg = readJson(pkgPath);
  if (!pkg) return;
  let changed = false;
  if (!pkg.devDependencies) pkg.devDependencies = {};
  for (const [name, ver] of Object.entries(versions)) {
    if (pkg.devDependencies[name] !== ver) {
      console.log(
        `Will update ${path.relative(repoRoot, pkgPath)}: ${name} ${pkg.devDependencies[name] || ''} -> ${ver}`
      );
      changed = true;
      if (apply) pkg.devDependencies[name] = ver;
    }
  }
  if (apply && changed) writeJson(pkgPath, pkg);
  return changed;
}

const roots = [
  path.join(repoRoot, 'package.json'),
  path.join(repoRoot, 'gymgenius-monorepo', 'package.json'),
];
// include monorepo apps
const appsDir = path.join(repoRoot, 'gymgenius-monorepo', 'apps');
if (fs.existsSync(appsDir)) {
  const apps = fs.readdirSync(appsDir);
  for (const a of apps) {
    const p = path.join(appsDir, a, 'package.json');
    if (fs.existsSync(p)) roots.push(p);
  }
}

let any = false;
for (const r of roots) {
  const changed = tryUpdate(r);
  if (changed) any = true;
}

if (apply) {
  console.log('\nApplied updates to the package.json files');
} else {
  if (any) {
    console.warn(
      '\nMismatches detected. Re-run with --apply to update the package.json files.'
    );
    process.exit(1);
  }
  console.log('\nAll devDeps match dev_tool_versions.json');
}
