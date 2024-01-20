import uuid
import os
from datetime import datetime


def custom_file_name(instance, filename):
    _, extension = os.path.splitext(filename)
    if not extension:
        raise ValueError("File must have an extension.")
    
    unique_id = uuid.uuid4().hex
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    new_filename = f'{timestamp}_{unique_id}_{instance.FILENAME_WORD}{extension}'
    return os.path.join(instance.DIR_NAME, new_filename)
