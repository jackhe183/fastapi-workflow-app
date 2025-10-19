from importlib.util import source_hash

from fastapi import APIRouter

from app.apis.schemas import InputOutputPaths,SingleInputPath
from app.apis.schemas import StatusResponse
from app.workers.pre_process_script.schemas import DecompressRequest
from app.workers.pre_process_script.decompress_recursively import decompress_recursively

router = APIRouter(
    prefix="/pre_process",
)

@router.post("/decompress_recursively",response_model=StatusResponse)
def decompress_recursively(request: DecompressRequest):
    decompress_recursively(
    source_path = request.source_path,
    destination_path = request.destination_path
    )

    return StatusResponse(message=f"已成功从{request.source_path}解压到{request.destination_path}.")



