require('dotenv').config();
const { Client } = require('pg');
const fs = require('fs');

const config = {
  host: process.env.DB_HOST || 'localhost',
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || '1234',
  database: process.env.DB_NAME || 'publisoft_benchmark',
  port: process.env.DB_PORT || 5432
};

async function benchmarkLocalPostgres() {
  const client = new Client(config);
  const batchSizes = [100, 500, 1000, 2000, 3000, 4000, 5000];
  const metrics = [];

  try {
    await client.connect();
    console.log('📥 Conectado a PostgreSQL local');

    for (const size of batchSizes) {
      const start = performance.now();
      const res = await client.query(`SELECT * FROM posts LIMIT $1`, [size]);
      const end = performance.now();

      const time = (end - start) / 1000; // en segundos
      const dataSizeBytes = Buffer.byteLength(JSON.stringify(res.rows));
      const dataSizeMB = dataSizeBytes / (1024 * 1024);
      const speedMBps = dataSizeMB / time;

      console.log(`✅ ${size} registros cargados en ${time.toFixed(3)} s (${dataSizeMB.toFixed(2)} MB)`);

      metrics.push({
        size,
        time: Number(time.toFixed(5)),
        dataSizeMB: Number(dataSizeMB.toFixed(5)),
        speedMBps: Number(speedMBps.toFixed(5))
      });
    }

    console.table(metrics);

    // Guardar resultados
    fs.writeFileSync('benchmark/local-results.json', JSON.stringify(metrics, null, 2));
    console.log('📊 Resultados guardados en benchmark/local-results.json');
  } catch (err) {
    console.error('❌ Error durante el benchmark:', err);
  } finally {
    await client.end();
  }
}

benchmarkLocalPostgres(); // <<== ¡Esto faltaba al final!
