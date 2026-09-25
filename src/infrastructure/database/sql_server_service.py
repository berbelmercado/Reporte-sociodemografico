from datetime import date
from time import sleep

import pandas as pd
import pyodbc

from config.settings import Settings
from infrastructure.logging.logger_service import LoggerService


class SqlServerService:
    """
    Gestiona conexión y ejecución de procedimientos almacenados.
    """

    STORED_PROCEDURE_NAME = "SN2_REPORTE_SOCIODEMOGRAFICO"
    MAX_RETRIES = 3

    def __init__(self, settings: Settings, logger: LoggerService) -> None:
        self.__settings = settings
        self.__logger = logger
        self.__connection: pyodbc.Connection | None = None

        self.__server = settings.server
        self.__database = settings.database
        self.__username = settings.username
        self.__password = settings.password

    def __enter__(self) -> "SqlServerService":
        self.__connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.__connection is not None:
            self.__connection.close()
            self.__logger.info("Conexión SQL Server cerrada.")

    def __connect(self) -> None:
        last_exception: Exception | None = None

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                self.__logger.info(
                    f"Intento de conexión SQL Server {attempt}/{self.MAX_RETRIES}"
                )

                self.__connection = pyodbc.connect(
                    (
                        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                        f"SERVER={self.__server};"
                        f"DATABASE={self.__database};"
                        f"UID={self.__username};"
                        f"PWD={self.__password}"
                    )
                )

                self.__logger.info("Conexión SQL Server establecida.")

                return

            except Exception as ex:
                last_exception = ex

                self.__logger.error(
                    f"Fallo de conexión. Intento {attempt}. Error: {ex}"
                )

                if attempt < self.MAX_RETRIES:
                    sleep(2)

        raise ConnectionError(
            "No fue posible conectarse a SQL Server."
        ) from last_exception

    def execute_stored_procedure(
        self, start_date: date, end_date: date
    ) -> pd.DataFrame:

        if self.__connection is None:
            raise ConnectionError("No existe una conexión activa.")

        query = f"EXEC {self.STORED_PROCEDURE_NAME} " "@INICIO=?, " "@FIN=?"

        self.__logger.info(
            f"Ejecutando {self.STORED_PROCEDURE_NAME}. "
            f"Inicio={start_date} Fin={end_date}"
        )

        dataframe = pd.read_sql(
            sql=query, con=self.__connection, params=[start_date, end_date]
        )

        self.__logger.info(f"DataFrame obtenido con {len(dataframe)} registros.")

        return dataframe
