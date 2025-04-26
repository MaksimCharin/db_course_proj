from src.db_manager import DBManager


def user_interface(user_manager: DBManager) -> None:
    """Интерфейс взаимодействия с пользователем"""
    while True:
        print("1. Показать компании и количество вакансий")
        print("2. Показать среднюю зарплату")
        print("3. Показать вакансии с зарплатой выше средней")
        print("4. Показать вакансии по ключевому слову")
        print("5. Показать все вакансии")

        choice = input("Выберите опцию (или 'exit' для выхода): ")

        if choice == "1":
            companies = user_manager.get_companies_and_vacancies_count()
            if companies:
                print("Список компаний и количество вакансий:")
                for company in companies:
                    print(f"Компания: {company[0]}, Вакансий: {company[1]}")
            else:
                print("Нет доступных компаний.")

        elif choice == "2":
            avg_salary = user_manager.get_avg_salary()
            print(f"Средняя зарплата: {avg_salary:.2f}")

        elif choice == "3":
            higher_salary_vacancies = user_manager.get_vacancies_with_higher_salary()
            if higher_salary_vacancies:
                print("Вакансии с зарплатой выше средней:")
                for vacancy in higher_salary_vacancies:
                    min_salary = vacancy[2] if vacancy[2] is not None else "Не указана"
                    max_salary = vacancy[3] if vacancy[3] is not None else "Не указана"
                    print(f"Вакансия: {vacancy[1]}, Зарплата: {min_salary} - {max_salary}, Ссылка: {vacancy[5]}")
            else:
                print("Нет вакансий с зарплатой выше средней.")

        elif choice == "4":
            keyword = input("Введите ключевое слово: ")
            keyword_vacancies = user_manager.get_vacancies_with_keyword(keyword)
            if keyword_vacancies:
                print(f"Вакансии по ключевому слову '{keyword}':")
                for vacancy in keyword_vacancies:
                    min_salary = vacancy[2] if vacancy[2] is not None else "Не указана"
                    max_salary = vacancy[3] if vacancy[3] is not None else "Не указана"
                    print(f"Вакансия: {vacancy[1]}, Зарплата: {min_salary} - {max_salary}, Ссылка: {vacancy[5]}")
            else:
                print(f"Нет вакансий по ключевому слову '{keyword}'.")

        elif choice == "5":
            all_vacancies = user_manager.get_all_vacancies()
            if all_vacancies:
                print("Все вакансии:")
                for vacancy in all_vacancies:
                    min_salary = vacancy[2] if vacancy[2] is not None else "Не указана"
                    max_salary = vacancy[3] if vacancy[3] is not None else "Не указана"
                    print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {min_salary} - {max_salary}, Ссылка: {vacancy[4]}")
            else:
                print("Нет доступных вакансий.")

        elif choice.lower() == "exit":
            break