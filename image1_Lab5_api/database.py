
import sqlite3
from pathlib import Path
from contextlib import contextmanager

DATABASE = Path(__file__).resolve().parent / "database.db"

USER_FIELDS = ("name", "email", "phone", "address", "country")


def connect_to_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def db_session():
    conn = connect_to_db()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# CREATE THE USERS TABLE
def create_db_table():
    with db_session() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                country TEXT NOT NULL
            )
        """)


# INSERT A NEW USER
def insert_user(user):
    with db_session() as conn:
        cursor = conn.execute("""
            INSERT INTO users (name, email, phone, address, country)
            VALUES (?, ?, ?, ?, ?)
        """, (
            user["name"],
            user["email"],
            user["phone"],
            user["address"],
            user["country"]
        ))

        user_id = cursor.lastrowid

    return get_user_by_id(user_id)


# GET ALL USERS
def get_users():
    with db_session() as conn:
        rows = conn.execute(
            "SELECT * FROM users ORDER BY user_id"
        ).fetchall()

        return [dict(row) for row in rows]


# GET ONE USER BY ID
def get_user_by_id(user_id):
    with db_session() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        return dict(row) if row else None


# UPDATE ALL FIELDS OF A USER
def update_user(user):
    with db_session() as conn:
        cursor = conn.execute("""
            UPDATE users
            SET name = ?, email = ?, phone = ?, address = ?, country = ?
            WHERE user_id = ?
        """, (
            user["name"],
            user["email"],
            user["phone"],
            user["address"],
            user["country"],
            user["user_id"]
        ))

        if cursor.rowcount == 0:
            return None

    return get_user_by_id(user["user_id"])


# UPDATE ONLY SELECTED FIELDS
def patch_user(user_id, changes):
    fields = [field for field in changes if field in USER_FIELDS]

    if not fields:
        return None

    set_clause = ", ".join(f"{field} = ?" for field in fields)
    values = [changes[field] for field in fields]
    values.append(user_id)

    with db_session() as conn:
        cursor = conn.execute(
            f"UPDATE users SET {set_clause} WHERE user_id = ?",
            values
        )

        if cursor.rowcount == 0:
            return None

    return get_user_by_id(user_id)


# DELETE A USER
def delete_user(user_id):
    with db_session() as conn:
        cursor = conn.execute(
            "DELETE FROM users WHERE user_id = ?",
            (user_id,)
        )

        return cursor.rowcount > 0


if __name__ == "__main__":
    create_db_table()
    print("Database and users table created successfully!")
