import requests
from dotenv import dotenv_values
from terminaltables import AsciiTable


MOST_POPULAR_LANGUAGES = ["JavaScript", "Java", "Python", "Ruby", "PHP", "C++", "C#", "C", "Go", "Shell", "Objective-C", "Scala", "Swift", "TypeScript"]


def predict_salary_fork(salary_from, salary_to):
    if(not salary_from):
        return salary_to * 0.8
    elif(not salary_to):
        return salary_from * 1.2
    else:
        return (salary_from + salary_to) / 2


def get_sj_salaries_statistics(token, languages):
    sj_vacancies = [["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]]
    for language in languages:
        sj_vacancies.append(predict_sj_avarage_salary(token=token, language=language))
    return AsciiTable(sj_vacancies, "SuperJob Moscow")


def predict_sj_avarage_salary(token, language="Python"):
    is_more = True
    pages_count = 0
    all_salaries_sum = 0
    vacancies_processed_count = 0
    while(is_more):
        response = get_sj_vacancies_page(token=token, language=language, page=pages_count).json()
        vacancies = response["objects"]
        for vacancy in vacancies:
            prediction = predict_sj_rub_salary(vacancy=vacancy)
            if prediction:
                all_salaries_sum += prediction
                vacancies_processed_count += 1
        pages_count += 1
        is_more = response["more"]
    avarage_salary = int(all_salaries_sum / vacancies_processed_count) if vacancies_processed_count > 0 else 0
    return [f"{language}", f"{response['total']}", f"{vacancies_processed_count}", f"{avarage_salary}"]


def predict_sj_rub_salary(vacancy):
    if(vacancy["currency"] != "rub" or (vacancy["payment_from"] == 0 and vacancy["payment_to"] == 0)):
        return None
    return predict_salary_fork(vacancy["payment_from"], vacancy["payment_to"])


def get_sj_vacancies_page(token, language="Python", page=0):
    base_url = "https://api.superjob.ru/2.0/"
    rest_api = "vacancies/"
    where_search_keyword = {"position": 1}
    params = {
        "town": "Москва",
        "keywords[0][srws]": f"{where_search_keyword['position']}",
        "keywords[0][skwc]": "or",
        "keywords[0][keys]": "программист",
        "keywords[1][srws]": f"{where_search_keyword['position']}",
        "keywords[1][skwc]": "or",
        "keywords[1][keys]": f"{language}",
        "page": page,
        }
    headers = {
        "X-Api-App-Id": token
    }
    response = requests.get(url = f"{base_url}{rest_api}", headers=headers, params=params)
    response.raise_for_status()
    return response


def get_hh_salaries_statistics(languages):
    hh_statistics = [["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]]
    for language in languages:
        hh_statistics.append(predict_hh_avarage_salary(language=language))
    return AsciiTable(hh_statistics, "HH Moscow")


def predict_hh_avarage_salary(language="Python"):
    all_salaries_sum = 0
    vacancies_processed_count = 0
    current_page_number = 0
    more_pages_ahead = True
    while(more_pages_ahead):
        response = get_hh_vacancies_page(language=language, page=current_page_number).json()
        vacancies = response["items"]
        if(current_page_number==0):
            pages_count = int(response["pages"])
            vacancies_count = int(response["found"])
        for vacancy in vacancies:
            prediction = predict_hh_rub_salary(vacancy=vacancy)
            if prediction:
                all_salaries_sum += prediction
                vacancies_processed_count += 1
        if(current_page_number==pages_count-1):
            more_pages_ahead = False
        current_page_number += 1
    avarage_salary = int(all_salaries_sum / vacancies_processed_count) if vacancies_processed_count > 0 else 0
    return [f"{language}", f"{vacancies_count}", f"{vacancies_processed_count}", f"{avarage_salary}"]


def predict_hh_rub_salary(vacancy):
    vacancy_salary = vacancy["salary"]
    if(vacancy_salary["currency"] != "RUR"):
        return None
    return predict_salary_fork(vacancy_salary["from"], vacancy_salary["to"])


def get_hh_vacancies_page(language="Python", last_month=False, page=0):
    base_url = "https://api.hh.ru/"
    rest_api = "vacancies"
    rest_api_moscow_id = 1
    params = {
        "text": f"{language}",
        "area": f"{rest_api_moscow_id}",
        "only_with_salary": "true",
        "page": page,
        "per_page": "100",
        }
    if last_month:
        params["period"] = "30"
    response = requests.get(url = f"{base_url}{rest_api}", params=params)
    response.raise_for_status()
    return response


def main():
    sj_api_token = dotenv_values(".env")["SUPERJOB_API_SECRET_KEY"]
    print(get_hh_salaries_statistics(languages=MOST_POPULAR_LANGUAGES).table)
    print(get_sj_salaries_statistics(token=sj_api_token, languages=MOST_POPULAR_LANGUAGES).table)


if __name__ == '__main__':
    main()
