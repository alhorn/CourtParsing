import json
import sqlite3


def fill_db():
    connection = sqlite3.connect('cases.db')
    cursor = connection.cursor()

    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for case in data:
            case_values = []
            case_values.append(case.get('case_id', None))
            case_values.append(case.get('case_material_number', None))
            case_values.append(case.get('receipt_date', None))
            case_values.append(case.get('parties', None))
            case_values.append(case.get('judge', None))
            case_values.append(case.get('case_category', None))
            case_values.append(case.get('current_status', None))
            case_values.append(case.get('date_of_first_instance_case_review', None))
            case_values.append(case.get('first_instance_decision', None))
            case_values.append(case.get('date_of_entry_into_force_of_the_judgment', None))
            case_values.append(case.get('ground_of_judgment', None))
            case_values.append(case.get('superior_court_case_number', None))

            cursor.execute(
                '''INSERT INTO cases VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', tuple(case_values)
            )
            cursor.execute(
                '''SELECT id, case_id FROM cases WHERE case_id = ?''', (case.get('case_id', None),)
            )
            case_db_id = cursor.fetchall()[0][0]
            for state in case['state_history']:
                cursor.execute(
                    '''INSERT INTO state_history VALUES(NULL, ?, ?, ?, ?)''',
                    (state['date'], state['status'], state['foundation_document'], case_db_id)
                )
            for state in case['location_history']:
                cursor.execute(
                    '''INSERT INTO location_history VALUES(NULL, ?, ?, ?, ?)''',
                    (state['date'], state['location'], state['comment'], case_db_id)
                )
            for state in case['trial_sessions_and_interviews']:
                cursor.execute(
                    '''INSERT INTO trial_sessions_and_interviews VALUES(NULL, ?, ?, ?, ?)''',
                    (state['date_and_time'], state['hall'], state['stage'], case_db_id)
                )

    connection.commit()
    connection.close()
