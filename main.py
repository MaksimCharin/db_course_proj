from config import get_db_config
from src.db_manager import DBManager
from src.init_db import initialize_database


def user_interface(user_manager: DBManager) -> None:
    """Интерфейс взаимодействия с пользователем"""
    while True:
        print("1. Показать компании и количество вакансий")
        print("2. Показать среднюю зарплату")
        print("3. Показать вакансии с зарплатой выше средней")
        print("4. Показать вакансии по ключевому слову")

        choice = input("Выберите опцию (или 'exit' для выхода): ")

        if choice == "1":
            companies = user_manager.get_companies_and_vacancies_count()
            if companies:
                for company in companies:
                    print(f"Компания: {company[0]}, Вакансий: {company[1]}")
            else:
                print("Нет доступных компаний.")

        elif choice == "2":
            avg_salary = user_manager.get_avg_salary()
            print(f"Средняя зарплата: {avg_salary}")

        elif choice == "3":
            higher_salary_vacancies = user_manager.get_vacancies_with_higher_salary()
            if higher_salary_vacancies:
                for vacancy in higher_salary_vacancies:
                    print(vacancy)
            else:
                print("Нет вакансий с зарплатой выше средней.")

        elif choice == "4":
            keyword = input("Введите ключевое слово: ")
            keyword_vacancies = user_manager.get_vacancies_with_keyword(keyword)
            if keyword_vacancies:
                for vacancy in keyword_vacancies:
                    print(vacancy)
            else:
                print(f"Нет вакансий по ключевому слову '{keyword}'.")

        elif choice.lower() == "exit":
            break


def main() -> None:
    """Точка входа в программу"""
    # Получение конфигурации базы данных
    db_config = get_db_config()

    # Инициализация базы данных
    initialize_database(db_config)

    # Запуск интерфейса пользователя
    user_manager = DBManager(db_config)
    user_interface(user_manager)
    user_manager.close()


if __name__ == "__main__":
    main()
