import json
from abc import abstractmethod

from data_keys import *
from variables import domain_url


class DictMixin:
    @abstractmethod
    def get_as_dict(self):
        return {}

    def __str__(self):
        return str(self.get_as_dict())


class Course(DictMixin):
    def __init__(self, title: str, url: str, sections: list):
        self.title = title
        self.url = url
        self.sections = sections

    def get_lecture_urls(self):
        out_list = []
        for ii in self.sections:
            if isinstance(ii, Section):
                out_list += ii.get_lecture_urls()
        return out_list

    def get_sections_as_dict(self):
        out_list = []
        for ii in self.sections:
            if isinstance(ii, Section):
                out_list.append(ii.get_as_dict())
        return out_list

    @property
    def id(self):
        return self.url.split('/')[-1].strip()

    def get_as_dict(self):
        return {title_key: self.title, url_key: self.url, sections_key: self.get_sections_as_dict()}


class Section(DictMixin):
    def __init__(self, title: str, lectures: list):
        self.title = title
        self.lectures = lectures

    def get_lecture_urls(self):
        out_list = []
        for ii in self.lectures:
            if isinstance(ii, Lecture):
                out_list.append(ii.url)
        return out_list

    def get_lectures_as_dict(self):
        out_list = []
        for ii in self.lectures:
            if isinstance(ii, Lecture):
                out_list.append(ii.get_as_dict())
        return out_list

    def get_as_dict(self):
        return {title_key: self.title, lectures_key: self.get_lectures_as_dict()}


class Lecture(DictMixin):
    def __init__(self, title: str, url: str, download_links: list):
        self.title = title
        self.url = url
        self.download_links = download_links

    @property
    def page_url(self):
        return domain_url + self.url

    @property
    def has_downloads(self):
        return self.download_links is not []

    @property
    def id(self):
        return self.url.split('/')[-1].strip()

    def get_as_dict(self):
        d = {title_key: self.title, url_key: self.url}
        if self.has_downloads:
            d.update({download_links_key: self.download_links})
        return d


def load_course_from_json(file_path: str):
    with open(file_path) as file:
        data = json.loads(file.read())
        return load_course_from_dict(data)


def load_course_from_dict(d: dict):
    title = d[title_key]
    url = d[url_key]
    sections_data = d[sections_key]
    section_list = []

    for ii in sections_data:
        section = load_section_from_dict(ii)
        section_list.append(section)

    return Course(title, url, section_list)


def load_section_from_dict(d: dict):
    title = d[title_key]
    lectures_data = d[lectures_key]
    lecture_list = []
    for ii in lectures_data:
        lecture = load_lecture_from_dict(ii)
        lecture_list.append(lecture)

    return Section(title, lecture_list)


def load_lecture_from_dict(d: dict):
    title = d[title_key]
    url = d[url_key]
    download_links = d.get(download_links_key, [])
    return Lecture(title, url, download_links)
