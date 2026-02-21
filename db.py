"""
Best Buy Scraper - SQLite Database Setup
Run this once to initialize the DB, then use the helper functions to insert/update records.
"""

import sqlite3
from datetime import datetime

DB_PATH = "bestbuy_scraper.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create all tables. Safe to run multiple times."""
    conn = get_conn()
    c = conn.cursor()

    # Core product info — one row per product
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            sku           TEXT UNIQUE NOT NULL,   -- Best Buy SKU / product ID
            url           TEXT,
            name          TEXT,
            price         TEXT,
            wanted_price  TEXT,
            created_at    TEXT DEFAULT (datetime('now')),
            updated_at    TEXT DEFAULT (datetime('now'))
        )
    """)

    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")


# ── Helper functions ──────────────────────────────────────────────────────────

def insert_product(sku, name=None, url=None, category=None, brand=None, model_number=None):
    conn = get_conn()
    conn.execute("""
        INSERT INTO products (sku, name, url, category, brand, model_number)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(sku) DO UPDATE SET
            name         = COALESCE(excluded.name, name),
            url          = COALESCE(excluded.url, url),
            price        = COALESCE(excluded.price, price),
            updated_at   = datetime('now')
    """, (sku, name, url, category, brand, model_number))
    conn.commit()
    conn.close()


def get_latest_price(sku):
    conn = get_conn()
    row = conn.execute("""
        SELECT * FROM price_history
        WHERE sku = ?
        ORDER BY scraped_at DESC
        LIMIT 1
    """, (sku,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_products():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM products ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Example usage ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()

    insert_product(
        sku="6575391",
        name='Samsung 65" 4K QLED TV',
        url="https://www.bestbuy.com/product/lenovo-legion-7i-16-2-5k-lcd-gaming-laptop-intel-14th-gen-core-i7-with-16gb-memory-nvidia-geforce-rtx-4060-8gb-1tb-ssd-glacier-white/JJGYCCVGWJ/sku/6575391/openbox?condition=fair",
        category="TVs",
        brand="Samsung",
        model_number="QN65Q80C"
    )
    print(get_latest_price("6575391"))
    print(get_all_products())