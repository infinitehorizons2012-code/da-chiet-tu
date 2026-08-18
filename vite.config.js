import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'fs'
import path from 'path'
import { exec } from 'child_process'

function saveExcelPlugin() {
  return {
    name: 'save-excel',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        if (req.url === '/api/save' && req.method === 'POST') {
          let body = '';
          req.on('data', chunk => {
            body += chunk.toString();
          });
          req.on('end', () => {
            try {
              const data = JSON.parse(body);
              
              // 1. Update research_data.json directly for immediate UI update
              const jsonPath = path.resolve(__dirname, 'src/data/research_data.json');
              if (fs.existsSync(jsonPath)) {
                const jsonData = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
                const charObj = jsonData.find(c => c['Chữ Trung Quốc'] === data.char);
                if (charObj) {
                  for (const [k, v] of Object.entries(data.comps)) {
                    charObj[k] = v;
                  }
                  fs.writeFileSync(jsonPath, JSON.stringify(jsonData, null, 2), 'utf8');
                }
              }

              // 2. Call python script to update Excel
              const pythonScript = path.resolve('C:\\Users\\DT.HANG\\.gemini\\antigravity\\brain\\9845be2f-b523-4b6b-ac52-eff1c0ade0c7\\scratch\\update_excel.py');
              // use spawn or exec
              const child = exec(`python "${pythonScript}"`, { env: { ...process.env, PYTHONIOENCODING: 'utf-8' } }, (error, stdout, stderr) => {
                if (error) {
                  console.error(`exec error: ${error}`);
                  res.statusCode = 500;
                  res.end(JSON.stringify({ success: false, error: error.message }));
                  return;
                }
                res.setHeader('Content-Type', 'application/json');
                res.end(stdout);
              });
              
              child.stdin.write(body);
              child.stdin.end();
            } catch (err) {
              res.statusCode = 500;
              res.end(JSON.stringify({ success: false, error: err.message }));
            }
          });
        } else {
          next();
        }
      });
    }
  }
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), saveExcelPlugin()],
  base: '/da-chiet-tu/',
})
