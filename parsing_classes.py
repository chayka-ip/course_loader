from abc import abstractmethod

from bs4 import BeautifulSoup
from data_keys import *


class ParsingItem:
    def __init__(self, data: BeautifulSoup):
        self.data = data

    @abstractmethod
    def get_as_dict(self):
        return {}


class CourseContainer(ParsingItem):

    @property
    def id(self):
        return self.data.get('data-course-url')

    @property
    def title(self):
        return self.data.findChild('div', class_='course-listing-title').text.strip()

    def get_as_dict(self):
        return {id_key: self.id, title_key: self.title}


class CourseSection(ParsingItem):

    @property
    def title(self):
        raw_text = self.data.findChild('div', class_='section-title').text.strip()
        return raw_text.split('\n')[0].strip()

    @property
    def lectures(self):
        lectures_data = self.data.findChildren('li', 'section-item')
        lecture_list = []
        for ii in lectures_data:
            lecture = CourseLecture(ii)
            lecture_list.append(lecture.get_as_dict())
        return lecture_list

    def get_as_dict(self):
        return {title_key: self.title, lectures_key: self.lectures}


class CourseLecture(ParsingItem):
    def __init__(self, data: BeautifulSoup):
        super().__init__(data)
        self.download_links = []

    def add_download_link(self, link: str):
        self.download_links.append(link)

    @property
    def has_downloads(self):
        return self.download_links is not None

    @property
    def title(self):
        raw_t = self.data.findChild('a', 'item').text.strip().split('\n')
        raw_t = [i.strip() for i in raw_t if i.strip()]
        raw_t.pop(0)
        return ' '.join(raw_t)

    @property
    def url(self):
        return self.data.findChild('a', 'item')['href']

    def get_as_dict(self):
        d = {title_key: self.title, url_key: self.url}
        if self.has_downloads:
            d.update({download_links_key: self.download_links})
        return d


class CourseParsed:
    def __init__(self, title: str, url: str, sections: list):
        self.title = title
        self.url = url
        self.sections = sections

    def get_as_dict(self):
        return {title_key: self.title, url_key: self.url, sections_key: self.sections}
