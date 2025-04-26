from typing import List, Optional, Tuple
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class DBManager:
    """Класс для управления базой данных"""

    def __init__(self, db_config: dict):
        """Инициализация базы данных"""
        try:
            self.connection = psycopg2.connect(**db_config)
            self.cursor = self.connection.cursor()
        except Exception as e:
            raise e

    @staticmethod
    def create_database(db_config: dict) -> None:
        """Создание базы данных, если она не существует"""
        dbname = db_config['dbname']
        conn = psycopg2.connect(dbname='postgres', user=db_config['user'],
                                password=db_config['password'], host=db_config['host'])
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM pg_database WHERE datname=%s", (dbname,))
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(f"CREATE DATABASE {dbname}")

        cursor.close()
        conn.close()

    def create_tables(self) -> None:
        """Создание таблиц в базе данных"""
        create_employers_table = """
        CREATE TABLE IF NOT EXISTS employers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            vacancies_count INTEGER DEFAULT 0
        );
        """

        create_vacancies_table = """
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            salary_min INTEGER,
            salary_max INTEGER,
            employer_id INTEGER REFERENCES employers(id),
            url VARCHAR(255)
        );
        """

        self.cursor.execute(create_employers_table)
        self.cursor.execute(create_vacancies_table)
        self.connection.commit()

    def insert_employer(self, name: str) -> int:
        """Вставка работодателя в базу данных"""
        self.cursor.execute("INSERT INTO employers (name) VALUES (%s) RETURNING id;", (name,))
        employer_id = self.cursor.fetchone()[0]
        self.connection.commit()
        return employer_id

    def insert_vacancy(
        self, title: str, salary_min: Optional[int], salary_max: Optional[int], employer_id: int, url: str
    ) -> None:
        """Вставка вакансии в базу данных"""
        self.cursor.execute(
            "INSERT INTO vacancies (title, salary_min, salary_max, employer_id, url) VALUES (%s, %s, %s, %s, %s);",
            (title, salary_min, salary_max, employer_id, url),
        )
        self.connection.commit()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """Получение списка всех компаний и количества вакансий у каждой компании"""
        query = """
        SELECT e.name, COUNT(v.id) AS vacancies_count
        FROM employers e
        LEFT JOIN vacancies v ON e.id = v.employer_id
        GROUP BY e.id;
        """

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        """Получение списка всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию"""
        query = """
        SELECT e.name AS company_name, v.title AS vacancy_title, v.salary_min AS min_salary,
               v.salary_max AS max_salary, v.url AS vacancy_url
        FROM vacancies v
        JOIN employers e ON v.employer_id = e.id;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_avg_salary(self) -> float:
        """Получение средней зарплаты по вакансиям"""
        query = "SELECT AVG((salary_min + salary_max) / 2) FROM vacancies;"

        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> List[Tuple[int, str, Optional[int], Optional[int], int, str]]:
        """Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        avg_salary = self.get_avg_salary()

        query = """
          SELECT * FROM vacancies WHERE (salary_min + salary_max) / 2 > %s;
          """
        self.cursor.execute(query, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(
        self, keyword: str
    ) -> List[Tuple[int, str, Optional[int], Optional[int], int, str]]:
        """Получение списка всех вакансий, по ключевому слову"""
        query = "SELECT * FROM vacancies WHERE title ILIKE %s;"
        self.cursor.execute(query, ("%" + keyword + "%",))
        return self.cursor.fetchall()

    def close(self) -> None:
        """Закрытие базы данных"""
        self.cursor.close()
        self.connection.close()
