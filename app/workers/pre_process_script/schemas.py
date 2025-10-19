from pydantic import BaseModel, Field, DirectoryPath, FilePath
from typing import Optional, Any, List

from app.apis.schemas import InputOutputPaths

class DecompressRequest(InputOutputPaths):
    pass


class MoveUnwantedFilesRequest(InputOutputPaths):
    keep_extensions : List[str] = Field(..., description="要保留的文件名后缀列表")