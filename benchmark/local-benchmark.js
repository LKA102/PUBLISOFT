require('dotenv').config(); // Lee .env en raíz del proyecto
const { Client } = require('pg');
const fs = require('fs');

const config = {
  host: process.env.DB_HOST || 'localhost',
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || '1234',
  database: process.env.DB_NAME || 'publisoft_benchmark',
  port: process.env.DB_PORT || 5432
};

async function benchmarkPostsLoadLocal() {
  const client = new Client(config);
  const batchSizes = [100, 500, 1000, 2000, 3000, 4000, 5000];
  const metrics = [];

  try {
    await client.connect();
    console.log('📥 Conectado a PostgreSQL local');

    for (const size of batchSizes) {
      const start = performance.now();

      const result = await client.query(`SELECT * FROM posts LIMIT ${size}`);

      const end = performance.now();
      const elapsed = (end - start) / 1000;

      console.log(`✅ ${size} registros cargados en ${elapsed.toFixed(2)} s`);

      metrics.push({ size, time: elapsed });
    }

    console.table(metrics);

    // Guardar resultados si deseas graficar luego
    fs.writeFileSync('./benchmark/local-results.json', JSON.stringify(metrics, null, 2));
    console.log('📊 Resultados guardados en benchmark/local-results.json');

  } catch (err) {
    console.error('❌ Error al medir:', err);
  } finally {
    await client.end();
  }
}

benchmarkPostsLoadLocal();
