import os

from data_classes import load_course_from_json
from data_keys import download_links_key
from dmc.data_minig_custom import load_json_data, write_json_data

courses_folder = "data/courses"
dl_links_folder = 'data/dl_links'
out_folder = "data/courses_complete"


class DownloadLinkData:
    def __init__(self, course_id: str, lecture_id: str, download_links: list):
        self.course_id = course_id
        self.lecture_id = lecture_id
        self.download_links = download_links


def collect_all_pages():
    out_dict = {}
    for file in os.listdir(courses_folder):
        file_path = courses_folder + "/" + file
        course = load_course_from_json(file_path)
        title = course.title
        lectures = course.get_lecture_urls()
        out_dict[title] = lectures

    return out_dict


def write_all_pages():
    lf = '\n'
    tab = ' ' * 4
    comma = ','

    data = collect_all_pages()
    s = '[' + lf
    for key, value in data.items():
        s += tab + str(value) + comma + lf

    s += ']'
    print(s)


def load_dl_links():
    out_dict = {}
    for file in os.listdir(dl_links_folder):
        file_path = dl_links_folder + "/" + file
        data = load_json_data(file_path)

        parts = file.split('-')
        course_id = parts[0].strip()
        lecture_id = parts[1].strip()
        download_links = data[download_links_key]

        obj = DownloadLinkData(course_id, lecture_id, download_links)
        container = out_dict.get(course_id, [])
        container.append(obj)
        out_dict[course_id] = container

    return out_dict


def set_dl_links():
    all_links = load_dl_links()

    for file in os.listdir(courses_folder):
        file_path = courses_folder + "/" + file
        out_file_path = out_folder + "/" + file
        course = load_course_from_json(file_path)

        course_id = course.id
        links = all_links.get(course_id, None)

        if links is None:
            continue

        for section in course.sections:
            for lecture in section.lectures:
                lecture_id = lecture.id
                for ii in links:
                    if isinstance(ii, DownloadLinkData):
                        if ii.lecture_id == lecture_id:
                            lecture.download_links = ii.download_links

        complete_course_data = course.get_as_dict()
        write_json_data(out_file_path, complete_course_data,add_extension=False)


set_dl_links()


