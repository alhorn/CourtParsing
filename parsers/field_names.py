import json


def print_name():
    with open('../data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        names = []
        for obj in data:
            names.extend(list(obj.keys()))
        names = list(dict.fromkeys(names))
        d = {}
        for name in names:
            d[name] = ''
        print(d)


titles = {
    'Уникальный идентификатор дела': 'case_id',
    'Номер дела ~ материала': 'case_material_number',
    'Дата поступления': 'receipt_date',
    'Стороны': 'parties',
    'Cудья': 'judge',
    'Категория дела': 'case_category',
    'Текущее состояние': 'current_status',
    'Дата рассмотрения дела в первой инстанции': 'date_of_first_instance_case_review',
    'Решение первой инстанции': 'first_instance_decision',
    'Дата вступления решения в силу': 'date_of_entry_into_force_of_the_judgment',
    'Основание решения суда': 'ground_of_judgment',
    'Номер дела в суде вышестоящей инстанции': 'superior_court_case_number',

    'Дата': 'date',
    'Состояние': 'status',
    'Документ-основание': 'foundation_document',
    'Местонахождение': 'location',
    'Комментарий': 'comment',
    'Дата и время': 'date_and_time',
    'Зал': 'hall',
    'Стадия': 'stage',

    'История состояний': 'state_history',
    'История местонахождения': 'location_history',
    'Судебные заседания и беседы': 'trial_sessions_and_interviews',
}
