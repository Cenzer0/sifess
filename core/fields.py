from django.db import models
from django.conf import settings
from cryptography.fernet import Fernet
import base64

class EncryptedTextField(models.TextField):
    description = "Text field that encrypts data before saving and decrypts on access"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fernet = Fernet(settings.SECRET_KEY_FERNET)

    def get_prep_value(self, value):
        if value is None:
            return None
        return self.fernet.encrypt(value.encode('utf-8')).decode('utf-8')

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        try:
            return self.fernet.decrypt(value.encode('utf-8')).decode('utf-8')
        except Exception:
            return value

    def to_python(self, value):
        if value is None:
            return None
        # If it's already a string and looks like basic text, we might not need to decrypt if it wasn't encrypted
        # But for this simple field, we assume flow is usually db -> python (decrypt) or user -> python (raw) -> db (encrypt)
        # However, to_python is called on assignment too.
        # This simple implementation relies on from_db_value for decryption from DB.
        return value
