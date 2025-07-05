require('dotenv').config({ path: '../../.env' }); // Ajusta la ruta según tu estructura

const { Client } = require('pg');
const { faker } = require('@faker-js/faker');

const config = {
  host: process.env.DB_HOST || 'localhost',
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || '1234',
  database: process.env.DB_NAME || 'publisoft_benchmark',
  port: process.env.DB_PORT || 5432
};

async function seed() {
  const client = new Client(config);
  
  try {
    await client.connect();
    console.log('✅ Conectado a PostgreSQL');

    // Resetear la base de datos
    await client.query('DROP TABLE IF EXISTS posts, ratings CASCADE');
    
    await client.query(`
      CREATE TABLE posts (
        id SERIAL PRIMARY KEY,
        user_id UUID NOT NULL,
        title TEXT NOT NULL,
        course VARCHAR(100),
        cycle INTEGER,
        file_url TEXT,
        file_type VARCHAR(10),
        created_at TIMESTAMP DEFAULT NOW()
      )
    `);

    console.log('🔄 Insertando datos...');

    // Insertar 5000 posts de ejemplo
    for (let i = 1; i <= 5000; i++) {
      await client.query({
        text: `INSERT INTO posts (user_id, title, course, cycle, file_url, file_type)
               VALUES ($1, $2, $3, $4, $5, $6)`,
        values: [
          '5f8d3a5e-743b-4a7c-93a2-0f3a8d5b2e1f', // UUID fijo para pruebas
          faker.lorem.sentence(),
          faker.helpers.arrayElement(['Matemáticas', 'Ciencia', 'Historia']),
          faker.number.int({ min: 1, max: 10 }),
          `https://example.com/file${i}.pdf`,
          'pdf'
        ]
      });

      if (i % 500 === 0) console.log(`📌 ${i} registros insertados`);
    }

    console.log('🎉 Base de datos poblada exitosamente');
  } catch (err) {
    console.error('🚨 Error:', err);
  } finally {
    await client.end();
  }
}

seed();