/* Regression test: tools/static-audit.py must scan THIS repo when run with no
   arguments — its documented invocation (see docs/AUDIT.md). Its default path
   used to be a hard-coded scratch directory, so the command reported
   "0 JS files" and looked like a clean pass. Pinned here so it cannot drift back.

   node test8.js
*/
'use strict';
const { execFileSync } = require('child_process');
const path = require('path');

let pass = 0, fail = 0;
const ok = (name, cond, extra) => {
  if (cond) { pass++; console.log('PASS  ' + name + (extra ? '  (' + extra + ')' : '')); }
  else { fail++; console.log('FAIL  ' + name + (extra ? '  (' + extra + ')' : '')); }
};

let out = '';
try {
  out = execFileSync('python3', ['tools/static-audit.py'], { cwd: __dirname, encoding: 'utf8' });
} catch (e) { out = String((e.stdout || '') + (e.stderr || '')); }

const fm = out.match(/FILES\s+(\d+)\s+JS files/);
const files = fm ? Number(fm[1]) : -1;
ok('static-audit.py scans the repo with no arguments', files > 0, 'files=' + files);

const fnm = out.match(/FUNCTIONS\s+(\d+)\s+defined/);
const fns = fnm ? Number(fnm[1]) : -1;
ok('static-audit.py finds the engine functions', fns > 100, 'functions=' + fns);

const sm = out.match(/SCRIPT WIRING\s+(\d+)\s+tags/);
ok('static-audit.py reads index.html script wiring', !!sm && Number(sm[1]) > 0, sm ? sm[1] + ' tags' : 'no tag count');

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
