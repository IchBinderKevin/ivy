import os

import aiosqlite

DATABASE_MIGRATIONS_PATH = "./migrations"

async def run_migrations(db: aiosqlite.Connection):
    """
    Inserts or updates the schema_version table and applies migrations as needed.
    Migrations are applied in order of their version number in the filename (001 before 002 and so on)
    """
    try:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS schema_version (
                version TEXT PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor = await db.execute("SELECT * FROM schema_version ORDER BY applied_at DESC, version DESC LIMIT 1;")
        mig_info = await cursor.fetchone()
        if mig_info is None:
            print("No schema version found, starting with an empty database.")
        else:
            print(f"Current schema version: {mig_info[0]}; applied at: {mig_info[1]}")
        migration_files = sorted([f for f in os.listdir(DATABASE_MIGRATIONS_PATH) if f.endswith(".sql")])
        any_migration_applied = False
        for mig_file in migration_files:
            mig_version = mig_file.split("_")[0]
            if mig_info is None or mig_version > mig_info[0]:
                print(f"Applying migration {mig_file}...")
                with open(f"{DATABASE_MIGRATIONS_PATH}/{mig_file}", "r") as f:
                        await db.executescript(f.read())
                await db.execute("INSERT INTO schema_version (version) VALUES (?);", (mig_version,))
                await db.commit()
                print(f"Migration {mig_file} applied successfully.")
                any_migration_applied = True
        if any_migration_applied:
            print("Migrations applied successfully.")
            return
        print("Migrations are up to date, no action taken.")
    except Exception as e:
        print(f"Error checking or applying migrations: {e}")
