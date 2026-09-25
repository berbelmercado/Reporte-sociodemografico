from application.report_use_case import (
    ReportUseCase,
)
from config.path_resolver import PathResolver
from config.settings import Settings
from infrastructure.database.sql_server_service import (
    SqlServerService,
)
from infrastructure.logging.logger_service import (
    LoggerService,
)
from services.date_service import DateService
from services.email_service import EmailService
from services.excel_service import ExcelService


def main() -> None:

    settings = Settings.load()

    logger = LoggerService()

    logger.info("Inicio de aplicación.")

    date_service = DateService()

    sql_server_service = SqlServerService(
        settings=settings,
        logger=logger,
    )

    excel_service = ExcelService(
        path_resolver=PathResolver(),
        logger=logger,
    )

    email_service = EmailService(
        settings=settings,
        logger=logger,
    )

    report_use_case = ReportUseCase(
        date_service=date_service,
        sql_server_service=sql_server_service,
        excel_service=excel_service,
        email_service=email_service,
        logger=logger,
    )

    dataframe = report_use_case.execute()

    logger.info(f"Proceso finalizado. " f"Registros: {len(dataframe)}")


if __name__ == "__main__":
    main()
