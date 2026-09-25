from email.message import EmailMessage
from pathlib import Path
from time import sleep
import smtplib

from config.settings import Settings
from infrastructure.logging.logger_service import (
    LoggerService,
)


class EmailService:
    """
    Gestiona el envío de correos electrónicos.
    """

    MAX_RETRIES = 3

    def __init__(
        self,
        settings: Settings,
        logger: LoggerService,
    ) -> None:

        self.__settings = settings
        self.__logger = logger

    def build_recipients(self) -> list[str]:
        """
        Construye lista válida de destinatarios.
        """

        recipients = [
            email.strip()
            for email in self.__settings.recipient_emails.split(";")
            if email.strip()
        ]

        return recipients

    def build_subject(
        self,
        attachment_path: Path,
    ) -> str:
        """
        Genera asunto usando el nombre del archivo.
        """

        return attachment_path.stem

    def build_message(
        self,
        attachment_path: Path,
    ) -> EmailMessage:
        """
        Construye EmailMessage completo.
        """

        recipients = self.build_recipients()

        if not recipients:
            raise ValueError("No existen destinatarios configurados.")

        message = EmailMessage()

        message["From"] = self.__settings.sender_email

        message["To"] = ", ".join(recipients)

        message["Subject"] = self.build_subject(attachment_path)

        message.set_content(self.__settings.email_body)

        with open(attachment_path, "rb") as file:
            file_content = file.read()

        message.add_attachment(
            file_content,
            maintype=("application"),
            subtype=("vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            filename=attachment_path.name,
        )

        return message

    def send_email(
        self,
        attachment_path: Path,
    ) -> bool:
        """
        Envía correo mediante SMTP.
        """

        if not attachment_path.exists():

            self.__logger.error(f"Archivo no encontrado: " f"{attachment_path}")

            return False

        try:
            message = self.build_message(attachment_path)

        except Exception as ex:

            self.__logger.error(f"Error construyendo mensaje: " f"{ex}")

            return False

        for attempt in range(
            1,
            self.MAX_RETRIES + 1,
        ):

            try:

                self.__logger.info(f"Intento SMTP " f"{attempt}/{self.MAX_RETRIES}")

                with smtplib.SMTP(
                    self.__settings.smtp_server,
                    self.__settings.smtp_port,
                ) as smtp:

                    smtp.send_message(message)

                self.__logger.info("Correo enviado correctamente.")

                self.delete_attachment(attachment_path)

                return True

            except Exception as ex:

                self.__logger.error(f"Error SMTP intento " f"{attempt}: {ex}")

                if attempt < self.MAX_RETRIES:
                    sleep(2)

        self.__logger.error("No fue posible enviar el correo.")

        return False

    def delete_attachment(
        self,
        attachment_path: Path,
    ) -> None:
        """
        Elimina el Excel después de envío exitoso.
        """

        try:

            if not attachment_path.exists():

                self.__logger.error(f"Archivo ya eliminado: " f"{attachment_path}")

                return

            attachment_path.unlink()

            self.__logger.info(f"Archivo eliminado: " f"{attachment_path}")

        except Exception as ex:

            self.__logger.error(f"Error eliminando archivo: " f"{ex}")
