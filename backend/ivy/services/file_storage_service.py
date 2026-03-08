import os
import uuid

from fastapi import UploadFile

from common_constants import FILE_STORAGE_PATH
from models.attachment_model import AttachmentModel


class FileStorageService:
    """
    Service for storing files. This is used for attachments and images of items.
    1. Files are first staged in a temporary location.
    2. Once the item is created, the files are moved to their final location based on the item ID.
    This is because:
    - We want to avoid storing files for items that are never created because of failur during creation
    - We do not know the item id before the db ntry is crated
    """

    def stage_uploads(self, uploads: list[UploadFile]):
        """
        Uploads a list of files to a staging area.
        :param uploads: List of UploadFile instances to be staged.
        :return: List of AttachmentModel instances with paths to the staged files.
        """
        staged_files = []
        for file in uploads:
            file_location = f"{FILE_STORAGE_PATH}/.staged/{uuid.uuid4()}.{file.filename.split('.')[-1]}"
            os.makedirs(os.path.dirname(file_location), exist_ok=True)
            with open(file_location, "wb+") as file_object:
                file_object.write(file.file.read())
            staged_files.append(AttachmentModel(path=file_location))
        return staged_files

    def stage_image_upload(self, upload: UploadFile | None):
        """
        Uploads a single file to a staging area.
        :param upload: An UploadFile instance to be staged, or None if no file is provided.
        :return: An AttachmentModel instance with the path to the staged file, or None if no file is provided.
        """
        file_location = f"{FILE_STORAGE_PATH}/.staged/{uuid.uuid4()}.{upload.filename.split('.')[-1]}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)
        with open(file_location, "wb+") as file_object:
            file_object.write(upload.file.read())
        return file_location

    def finalize_upload(self, staged_file_paths: list[AttachmentModel], item_id: int):
        """
        Moves the staged files to their final location based on the item ID.
        :param staged_file_paths: List of AttachmentModel instances with paths to the staged files.
        :param item_id: The ID of the item the files are associated with.
        :return: List of AttachmentModel instances with paths to the finalized files.
        """
        finalized_paths = []
        for staged_path in staged_file_paths:
            filename = os.path.basename(staged_path.path)
            final_path = f"{FILE_STORAGE_PATH}/items/{item_id}/{filename}"
            os.makedirs(os.path.dirname(final_path), exist_ok=True)
            os.rename(staged_path.path, final_path)
            finalized_paths.append(AttachmentModel(path=final_path))
        return finalized_paths

    def finalize_image_upload(self, staged_file_path: str, item_id: int):
        """
        Moves the staged files to their final location based on the item ID.
        :param staged_file_path: path to the staged files.
        :param item_id: The ID of the item the file is associated with.
        :return: path to the finalized file.
        """
        filename = os.path.basename(staged_file_path)
        final_path = f"{FILE_STORAGE_PATH}/items/{item_id}/{filename}"
        os.makedirs(os.path.dirname(final_path), exist_ok=True)
        os.rename(staged_file_path, final_path)
        return final_path.strip(".")
