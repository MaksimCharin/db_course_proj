from typing import Dict
from src.api import APIManager
from src.db_manager import DBManager

def initialize_database(db_config: Dict[str, str]):
    """Инициализация базы данных и заполнение её данными"""
    DBManager.create_database(db_config)
    user_manager = DBManager(db_config)
    user_manager.create_tables()

    company_ids = [1740, 3529, 15478, 3776, 1122462, 1057, 3127, 78638, 4934, 4181]

    companies = APIManager.get_companies(company_ids)
    for company in companies:
        employer_id = user_manager.insert_employer(company["name"])
        vacancies = APIManager.get_vacancies(company["id"])
        for vacancy in vacancies:
            user_manager.insert_vacancy(
                title=vacancy["name"],
                salary_min=vacancy["salary"]["from"] if vacancy["salary"] else None,
                salary_max=vacancy["salary"]["to"] if vacancy["salary"] else None,
                employer_id=employer_id,
                url=vacancy['alternate_url']
            )
    user_manager.close()

