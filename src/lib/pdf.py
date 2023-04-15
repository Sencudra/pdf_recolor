import typing
import fitz
import os
import uuid

from pathlib import Path


class PDF:

    __CONTENTS_KEY = 'Contents'

    def __init__(self, file_path: Path) -> None:
        self.__file_path = file_path
        self.__document = fitz.Document(file_path)

        self.__page_xref = self.__get_page_xref()
        self.__content_xref = self.__get_content_xref()

    @property
    def raw_content(self) -> bytes:
        return self.__document.xref_stream(self.__content_xref)

    @raw_content.setter
    def raw_content(self, raw_steam: bytes):
        self.__document.update_stream(self.__content_xref, raw_steam)

    def save(self):
        dir_name = self.__file_path.parent
        temp_file_name = dir_name / str(uuid.uuid4())
        with open(temp_file_name, 'w') as fp:
            self.__document.save(fp, garbage=3, deflate=True, clean=True)
        os.rename(temp_file_name, self.__file_path)

    def __get_page_xref(self) -> int:
        return self.__document[0].xref

    def __get_content_xref(self) -> int:
        raw_xref = self.__document.xref_get_key(self.__page_xref, self.__CONTENTS_KEY)
        return self.__get_xref(raw_xref)

    def __get_xref(self, xref_object) -> typing.Optional[int]:
        _, ref = xref_object
        return int(ref.split()[0])