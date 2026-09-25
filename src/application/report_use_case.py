import pandas as pd

from infrastructure.database.sql_server_service import (
    SqlServerService,
)
from infrastructure.logging.logger_service import (
    LoggerService,
)
from services.date_service import DateService
from services.email_service import EmailService
from services.excel_service import ExcelService


class ReportUseCase:
    """
    Caso de uso principal.
    """

    def __init__(
        self,
        date_service: DateService,
        sql_server_service: SqlServerService,
        excel_service: ExcelService,
        email_service: EmailService,
        logger: LoggerService,
    ) -> None:

        self.__date_service = date_service
        self.__sql_server_service = sql_server_service
        self.__excel_service = excel_service
        self.__email_service = email_service
        self.__logger = logger

    def execute(self) -> pd.DataFrame:
        """
        Ejecuta el flujo completo V3.
        """

        self.__logger.info("Inicio ReportUseCase.")

        start_date, end_date = self.__date_service.get_previous_month_period()

        with self.__sql_server_service as database:

            dataframe = database.execute_stored_procedure(
                start_date=start_date,
                end_date=end_date,
            )

        self.__logger.info(f"Registros obtenidos: " f"{len(dataframe)}")

        if dataframe.empty:

            self.__logger.warning("DataFrame vacío. " "No se genera Excel.")

            return dataframe

        excel_path = self.__excel_service.export(
            dataframe=dataframe,
            period_start_date=start_date,
        )

        email_sent = self.__email_service.send_email(excel_path)

        if email_sent:

            self.__logger.info("Proceso de correo " "finalizado correctamente.")

        else:

            self.__logger.error("No fue posible enviar " "el correo.")

        return dataframe
