import sqlite3


def setup_db():
    connection = sqlite3.connect('cases.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id TEXT,
        case_material_number TEXT,
        receipt_date TEXT,
        parties TEXT,
        judge TEXT,
        case_category TEXT,
        current_status TEXT,
        date_of_first_instance_case_review TEXT,
        first_instance_decision TEXT,
        date_of_entry_into_force_of_the_judgment TEXT,
        ground_of_judgment TEXT,
        superior_court_case_number TEXT
    );
    ''')
    cursor.execute('''
    CREATE TABLE state_history
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        status TEXT,
        foundation_document TEXT,
        case_id TEXT,
        FOREIGN KEY (case_id)  REFERENCES cases (id) ON DELETE CASCADE
    );
    ''')
    cursor.execute('''
    CREATE TABLE location_history
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        location TEXT,
        comment TEXT,
        case_id TEXT,
        FOREIGN KEY (case_id)  REFERENCES cases (id) ON DELETE CASCADE
    );
    ''')
    cursor.execute('''
    CREATE TABLE trial_sessions_and_interviews
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_and_time TEXT,
        hall TEXT,
        stage TEXT,
        case_id TEXT,
        FOREIGN KEY (case_id)  REFERENCES cases (id) ON DELETE CASCADE
    );
    ''')

    connection.commit()
    connection.close()
