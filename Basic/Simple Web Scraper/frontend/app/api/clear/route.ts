import { NextResponse } from 'next/server';
import { Pool } from 'pg';

const pool = new Pool({
  database: process.env.DB_NAME || 'scraped_data',
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || 'Scraper123',
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '5432'),
});

export async function POST() {
  try {
    const client = await pool.connect();
    await client.query('DELETE FROM scraped_data');
    client.release();
    return NextResponse.json({ message: 'Data cleared' }, { status: 200 });
  } catch (error: unknown) {
    const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred';
    return NextResponse.json({ error: `Database Error: ${errorMessage}` }, { status: 500 });
  }
}