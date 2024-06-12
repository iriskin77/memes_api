from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from memes.container.container import container
from fastapi.responses import JSONResponse, FileResponse
from config.config import FILE_PATH_DOWNLOAD_TMP


router = APIRouter()


@router.post("/save_file")
async def create_file(file: UploadFile = File(...),
                      file_service=Depends(container.get_file_service)):

    if file_service.is_file_exists(file.filename) is None:
        raise HTTPException(status_code=500, detail="file already exists")

    try:
        res = await file_service.add_file_to_bucket(file=file)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"database error: {ex}")
    return res


@router.get("/download_file")
async def get_file(filename: str,
                   file_service=Depends(container.get_file_service)):
    try:
        file = await file_service.get_file_from_bucket(bucket_name=filename, object_name=filename)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"database error: {ex}")
    return FileResponse(FILE_PATH_DOWNLOAD_TMP + file.object_name, media_type=file.content_type, filename=file.object_name)


@router.get("/get_list_files")
async def get_list_files(user_uuid: str,
                         file_service=Depends(container.get_file_service)):

    files = await file_service.get_list_files_from_bucket(bucket_name=user_uuid)
    return files


@router.delete("/delete_dile")
async def delete_file(user_uuid: str,
                      filename: str,
                      file_service=Depends(container.get_file_service)):

    try:
        res = await file_service.delete_file_from(bucket_name=user_uuid, object_name=filename)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"database error: {ex}")
    return res


@router.put("/update_file")
async def update_file():
    pass
