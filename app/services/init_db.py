from app.services.database import check_database_connection, create_tables

def main() -> None:
    print("Checking PostgreSQL connection...")

    if not check_database_connection():
        raise RuntimeError(
            "Unable to connect to PostgreSQL. "
            "Make sure Docker PostgreSQL is running."
        )

    print("PostgreSQL connection: OK")

    print("Creating database tables...")
    create_tables()

    print("Database tables: OK")
    print("Database initialization completed successfully.")

if __name__ == "__main__":
    main()