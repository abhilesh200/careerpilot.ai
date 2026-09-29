import os
import bcrypt
import psycopg2
from psycopg2.extras import RealDictCursor


DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable is not set.")

    connection = psycopg2.connect(DATABASE_URL)
    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS career_profiles (
            id SERIAL PRIMARY KEY,
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
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()


def create_user(name, email, password_hash):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users (name, email, password_hash)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (name, email, password_hash)
    )

    user_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return user_id


def get_user_by_email(email):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = %s
        """,
        (email,)
    )

    user = cursor.fetchone()

    cursor.close()
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
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
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

    profile_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return profile_id


def get_career_profile(user_id):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        """
        SELECT *
        FROM career_profiles
        WHERE user_id = %s
        ORDER BY id DESC
        LIMIT 1
        """,
        (user_id,)
    )

    profile = cursor.fetchone()

    cursor.close()
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
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (user_id, role, content)
    )

    message_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return message_id


def get_chat_history(user_id, limit=50):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        """
        SELECT id, user_id, role, content, created_at
        FROM chat_messages
        WHERE user_id = %s
        ORDER BY id ASC
        LIMIT %s
        """,
        (user_id, limit)
    )

    messages = cursor.fetchall()

    cursor.close()
    connection.close()

    return messages


def clear_chat_history(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM chat_messages
        WHERE user_id = %s
        """,
        (user_id,)
    )

    connection.commit()
    cursor.close()
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
    print("CareerPilot PostgreSQL database created successfully.")