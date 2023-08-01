import os.path

from django.core.exceptions import ValidationError


def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1]
    print(ext)
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Phần mở rộng tệp không được hỗ trợ. Phần mở rộng hợp lệ: ' + str(valid_extensions))
