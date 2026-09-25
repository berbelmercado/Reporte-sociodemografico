from dataclasses import dataclass
from dotenv import load_dotenv
import os

from config.path_resolver import PathResolver


@dataclass(frozen=True)
class Settings:
    """
    Lee y valida configuración desde .env
    """

    server: str
    database: str
    username: str
    password: str

    smtp_server: str
    smtp_port: int

    sender_email: str
    recipient_emails: str
    email_body: str

    @classmethod
    def load(cls) -> "Settings":
        env_path = PathResolver.get_env_path()

        load_dotenv(dotenv_path=env_path)

        values = {
            "SERVIDOR_SQL": os.getenv("SERVIDOR_SQL"),
            "BASE_DE_DATOS": os.getenv("BASE_DE_DATOS"),
            "USUARIO_SQL": os.getenv("USUARIO_SQL"),
            "CONTRASENA_SQL": os.getenv("CONTRASENA_SQL"),
            "SERVIDOR_SMTP": os.getenv("SERVIDOR_SMTP"),
            "PUERTO_SERVIDOR_SMTP": os.getenv("PUERTO_SERVIDOR_SMTP"),
            "CORREO_REMITENTE": os.getenv("CORREO_REMITENTE"),
            "EMAIL_DESTINATARIOS": os.getenv("EMAIL_DESTINATARIOS"),
            "EMAIL_BODY": os.getenv("EMAIL_BODY"),
        }

        missing = [key for key, value in values.items() if not value]

        if missing:
            raise ValueError("Variables obligatorias faltantes: " + ", ".join(missing))

        return cls(
            server=values["SERVIDOR_SQL"],
            database=values["BASE_DE_DATOS"],
            username=values["USUARIO_SQL"],
            password=values["CONTRASENA_SQL"],
            smtp_server=values["SERVIDOR_SMTP"],
            smtp_port=int(values["PUERTO_SERVIDOR_SMTP"]),
            sender_email=values["CORREO_REMITENTE"],
            recipient_emails=values["EMAIL_DESTINATARIOS"],
            email_body=values["EMAIL_BODY"],
        )
