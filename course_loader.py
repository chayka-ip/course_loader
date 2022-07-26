import re
from time import sleep

import requests
from bs4 import BeautifulSoup

from dmc.data_minig_custom import write_json_data, load_json_data
from parsing_classes import CourseContainer, CourseSection, CourseParsed
from variables import domain_url


def get_courses_listing(page_url: str):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'lxml')
    courses_data = soup.find_all('div', class_='course-listing bundle')

    course_items = []

    for dd in courses_data:
        course = CourseContainer(dd)
        course_items.append(course.get_as_dict())

    return course_items


def get_course_content(domain_url: str, slug: str):
    course_url = domain_url + slug
    response = requests.get(course_url)

    data = BeautifulSoup(response.text, 'lxml')
    sections_data = data.find_all('div', 'col-sm-12 course-section')

    section_list = []

    for ss in sections_data:
        section = CourseSection(ss)
        section_list.append(section.get_as_dict())

    return section_list


def get_lecture_download_link(lecture_url: str):
    response = requests.get(lecture_url)

    data = BeautifulSoup(response.text, 'lxml')
    sections_data = data.find('a', 'download')
    return sections_data['href']


def get_all_links():
    data_root_folder = 'courses'

    full_access_url = domain_url + '/p/all-access'
    courses = get_courses_listing(full_access_url)

    parsed_courses = []

    for course in courses:
        id = course['id']
        title = course['title']

        content = get_course_content(domain_url=domain_url, slug=id)
        course_parsed = CourseParsed(title, id, content)

        parsed_courses.append(course_parsed.get_as_dict())

        title_cleaned = re.sub('\W+', '', title)
        tmp_file_path = f'{data_root_folder}\\{title_cleaned}'
        write_json_data(tmp_file_path, course_parsed.get_as_dict())

        print(f'INFO: {len(parsed_courses)} / {len(courses)} done')
        sleep(2)


def update_course_data_with_dl(json_pth: str):
    folder = 'courses_with_dl'
    course_name = json_pth.split('\\')
    save_pth = f'{folder}\\{course_name}'

    failed_downloads = []

    data = load_json_data(json_pth)
    for section in data['sections']:
        for lecture in section['lectures']:
            lecture_url = f'{domain_url}{lecture["url"]}'
            try:
                title_course = data['title']
                title_section = section['title']
                title_lecture = lecture['title']

                t = f'{title_course} | {title_section} | {title_lecture}'

                print(f'INFO: Handling {t}')
                dl_url = get_lecture_download_link(lecture_url)
                lecture['download'] = dl_url
                sleep(0.25)
            except Exception:
                failed_downloads.append(lecture_url)
                print(f'failed to get dl link for: {lecture_url}')

    print('failed to download:')
    print(failed_downloads)
    write_json_data(save_pth, data, indent=4, add_extension=False)

