import os
from datetime import datetime
from uuid import uuid4


def get_file_path(instance, filename):
    new_path = f"{instance.user_id}/{datetime.strftime(instance.creation_date, '%Y-%m-%d')}"
    ext = filename.split('.')[-1]

    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)

    return os.path.join(new_path, filename)
