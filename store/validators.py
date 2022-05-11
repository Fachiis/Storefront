from django.core.exceptions import ValidationError


def validate_file_size(file):
    max_size_kb = 50

    # 1MB --> 1024KB 
    if file.size > max_size_kb * 1024:
        raise ValidationError(f"Image file can not be larger than {max_size_kb}KB!")
