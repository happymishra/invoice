import os
from datetime import datetime
from uuid import uuid4


def get_file_path(instance, filename):
    """
    Dynamically provides a file name where the upload files are stored
    Format: /{user_id}/{date}/{filename using uuid}.pdf
    :param instance: Model instance
    :param filename: Name of the file i.e. upload
    :return: File name at which the upload invoice will be stored
    """
    new_path = f"{instance.user_id}/{datetime.strftime(instance.creation_date, '%Y-%m-%d')}"
    ext = filename.split('.')[-1]

    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)

    return os.path.join(new_path, filename)
