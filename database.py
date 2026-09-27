import sqlite3
import bcrypt

DATABASE_NAME = "careerpilot.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS career_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            resume_skills TEXT,
            missing_skills TEXT,
            career_roles TEXT,
            roadmap TEXT,
            resume_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    connection.commit()
    connection.close()


def create_user(name, email, password_hash):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users (name, email, password_hash)
        VALUES (?, ?, ?)
        """,
        (name, email, password_hash)
    )

    connection.commit()
    user_id = cursor.lastrowid
    connection.close()

    return user_id


def get_user_by_email(email):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()
    connection.close()

    return user


def save_career_profile(
    user_id,
    resume_skills,
    missing_skills,
    career_roles,
    roadmap,
    resume_text
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO career_profiles (
            user_id,
            resume_skills,
            missing_skills,
            career_roles,
            roadmap,
            resume_text
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            resume_skills,
            missing_skills,
            career_roles,
            roadmap,
            resume_text
        )
    )

    connection.commit()
    profile_id = cursor.lastrowid
    connection.close()

    return profile_id


def get_career_profile(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM career_profiles
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (user_id,)
    )

    profile = cursor.fetchone()
    connection.close()

    return profile


def save_chat_message(user_id, role, content):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO chat_messages (
            user_id,
            role,
            content
        )
        VALUES (?, ?, ?)
        """,
        (user_id, role, content)
    )

    connection.commit()
    message_id = cursor.lastrowid
    connection.close()

    return message_id


def get_chat_history(user_id, limit=50):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, user_id, role, content, created_at
        FROM chat_messages
        WHERE user_id = ?
        ORDER BY id ASC
        LIMIT ?
        """,
        (user_id, limit)
    )

    messages = cursor.fetchall()
    connection.close()

    return messages


def clear_chat_history(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM chat_messages
        WHERE user_id = ?
        """,
        (user_id,)
    )

    connection.commit()
    connection.close()


def hash_password(password):
    password_bytes = password.encode("utf-8")

    hashed = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed.decode("utf-8")


def verify_password(password, password_hash):
    password_bytes = password.encode("utf-8")
    hash_bytes = password_hash.encode("utf-8")

    return bcrypt.checkpw(
        password_bytes,
        hash_bytes
    )


if __name__ == "__main__":
    create_tables()
    print("CareerPilot database created successfully.")
