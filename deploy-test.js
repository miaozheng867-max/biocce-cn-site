const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Read the credentials
const creds = fs.readFileSync(path.join(process.env.HOME, '.cloudflare_creds'), 'utf-8');
const tokenMatch = creds.match(/CLOUDFLARE_API_TOKEN="([^"]+)"/);
const accountMatch = creds.match(/CLOUDFLARE_ACCOUNT_ID="([^"]+)"/);

const token = tokenMatch ? tokenMatch[1] : null;
const accountId = accountMatch ? accountMatch[1] : null;

console.log(`Token length: ${token ? token.length : 0}`);
console.log(`Account ID: ${accountId}`);

if (token && accountId) {
  // Set env
  process.env.CLOUDFLARE_API_TOKEN = token;
  process.env.CLOUDFLARE_ACCOUNT_ID = accountId;
  
  try {
    const result = execSync('npx wrangler whoami', { 
      encoding: 'utf-8', 
      timeout: 30000,
      env: { ...process.env }
    });
    console.log('Wrangler result:', result);
  } catch (e) {
    console.log('Wrangler stderr:', e.stderr);
    console.log('Wrangler stdout:', e.stdout);
  }
}
