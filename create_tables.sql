CREATE TABLE employers (
    employer_id int PRIMARY KEY,
    employer_name varchar(255),
    open_vacancies int
);

CREATE TABLE vacancies (
    vacancy_id serial PRIMARY KEY,
    vacancy_name varchar(255),
    employer_id int REFERENCES employers(employer_id),
    salary varchar(255),
    vacancy_url varchar(255)
);