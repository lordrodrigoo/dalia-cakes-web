# pylint: disable=unused-argument
from fastapi import Request
from fastapi.responses import JSONResponse


class ImageUploadException(Exception):
    def __init__(self, message="Falha ao enviar imagem. Tente novamente."):
        self.message = message
        super().__init__(self.message)


async def image_upload_exception_handler(request: Request, exc: ImageUploadException):
    return JSONResponse(
        status_code=503,
        content={"detail": exc.message},
    )


class InvalidUploadFolderException(Exception):
    def __init__(self, message="Pasta de upload inválida."):
        self.message = message
        super().__init__(self.message)


async def invalid_upload_folder_exception_handler(request: Request, exc: InvalidUploadFolderException):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message},
    )


class InvalidImageTypeException(Exception):
    def __init__(self, message="Tipo de imagem inválido. Use JPEG, PNG ou WebP."):
        self.message = message
        super().__init__(self.message)


async def invalid_image_type_exception_handler(request: Request, exc: InvalidImageTypeException):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message},
    )
