# pylint: disable=unused-argument
from fastapi import Request
from fastapi.responses import JSONResponse


class ImageUploadException(Exception):
    def __init__(self, message="Failed to upload image. Please try again later."):
        self.message = message
        super().__init__(self.message)


async def image_upload_exception_handler(request: Request, exc: ImageUploadException):
    return JSONResponse(
        status_code=503,
        content={"message": exc.message},
    )


class InvalidUploadFolderException(Exception):
    def __init__(self, message="Invalid upload folder. Please check the configuration."):
        self.message = message
        super().__init__(self.message)


async def invalid_upload_folder_exception_handler(request: Request, exc: InvalidUploadFolderException):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message},
    )


class InvalidImageTypeException(Exception):
    def __init__(self, message="Invalid image type. Only JPEG and PNG are allowed."):
        self.message = message
        super().__init__(self.message)


async def invalid_image_type_exception_handler(request: Request, exc: InvalidImageTypeException):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message},
    )
