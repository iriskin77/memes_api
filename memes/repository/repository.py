from abc import abstractmethod, ABC
from typing import Generic, Type, TypeVar, Union, Sequence
from pydantic import BaseModel
from minio import Minio


client = Minio("localhost:9000", access_key="WXGJn6Wg7G5iLvkpHr4N", secret_key="m41C12gRTuQ3QopR2tApv69qNAi8KJegbSLIHcKC", secure=False)


class Repository(ABC):

    @abstractmethod
    def get(self, bucket_name: str, object_name: str, file_path: str):
        raise NotImplementedError

    @abstractmethod
    def get_list_files(self, bucket_name: str):
        raise NotImplementedError

    @abstractmethod
    def create(self, bucket_name: str, object_name: str, file_path: str):
        raise NotImplementedError

    @abstractmethod
    def put(self):
        raise NotImplementedError

    @abstractmethod
    def patch(self):
        raise NotImplementedError

    @abstractmethod
    def delete(self, bucket_name: str, object_name: str):
        raise NotImplementedError


ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class FileRepository(Repository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, client_minio: Minio):
        self._client = client_minio

    async def get(self, bucket_name: str, object_name: str, file_path: str):
        path_download_tmp_dir = file_path + object_name
        file = self._client.fget_object(bucket_name=bucket_name,
                                        object_name=object_name,
                                        file_path=path_download_tmp_dir)

        return file

    async def get_list_files(self, bucket_name: str):
        files = self._client.list_objects(bucket_name=bucket_name, recursive=True)
        print(files)
        return files

    async def create(self, bucket_name: str, object_name: str, file_path: str):

        bucket_name1 = "python-test-bucket"

        found = client.bucket_exists(bucket_name1)
        if not found:
            client.make_bucket(bucket_name1)

        self._client.fput_object(bucket_name=bucket_name1,
                                 object_name=object_name,
                                 file_path=file_path)
        return True

    async def put(self):
        pass

    async def patch(self):
        pass

    async def delete(self, bucket_name: str, object_name: str):
        self._client.remove_object(bucket_name=bucket_name,
                                   object_name=object_name)
        return True


# initialize repository
repo = FileRepository(client)
