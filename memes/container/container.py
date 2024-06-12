from memes.repository.repository import FileRepository, repo
from memes.core.services.services import FileService


class Container:

    def __init__(self, file_repo: FileRepository):
        self._file_repo = file_repo

    def get_file_service(self) -> FileService:
        return FileService(self._file_repo)


container = Container(repo)
