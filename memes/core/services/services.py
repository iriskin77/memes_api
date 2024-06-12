import os
import random
import aiofiles
from fastapi import File
import string
from abc import abstractmethod, ABC
from memes.repository.repository import FileRepository
from config.config import FILE_PATH_UPLOAD_TMP, FILE_PATH_DOWNLOAD_TMP


class Service(ABC):

    @abstractmethod
    def get_file_from_bucket(self, bucket_name: str, object_name: str):
        raise NotImplementedError

    def get_list_files_from_bucket(self, bucket_name: str):
        raise NotImplementedError

    @abstractmethod
    def add_file_to_bucket(self, file: File):
        raise NotImplementedError

    @abstractmethod
    def delete_file_from(self, bucket_name: str, object_name: str):
        raise NotImplementedError


class FileService(Service):

    def __init__(self, repo: FileRepository):
        self._repo = repo

    async def get_file_from_bucket(self, bucket_name: str, object_name: str):
        file = await self._repo.get(bucket_name=bucket_name, object_name=object_name, file_path=FILE_PATH_DOWNLOAD_TMP)
        return file

    async def get_list_files_from_bucket(self, bucket_name: str):
        files = await self._repo.get_list_files(bucket_name=bucket_name)
        return files

    async def add_file_to_bucket(self, file: File):

        if not os.path.isdir(FILE_PATH_UPLOAD_TMP):
            os.mkdir(FILE_PATH_UPLOAD_TMP)

        filename_path = FILE_PATH_UPLOAD_TMP + file.filename

        async with aiofiles.open(filename_path, "wb") as buffer:
            data = await file.read()
            await buffer.write(data)

        res = await self._repo.create(bucket_name=file.filename,
                                      object_name=file.filename,
                                      file_path=filename_path)

        return res

    async def delete_file_from(self, bucket_name: str, object_name: str):
        res = await self._repo.delete(bucket_name=bucket_name, object_name=object_name)
        return res

    def is_file_exists(self, filename: str) -> bool:
        if not os.path.isfile(FILE_PATH_UPLOAD_TMP + filename):
            return True
