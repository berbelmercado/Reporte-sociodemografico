import logging
from pathlib import Path

from config.path_resolver import PathResolver


class LoggerService:
    """
    Servicio centralizado de logging.
    """

    def __init__(self) -> None:
        log_file: Path = PathResolver.get_log_file_path()

        self.__logger = logging.getLogger("ReporteSociodemografico")
        self.__logger.setLevel(logging.INFO)

        if not self.__logger.handlers:
            formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

            file_handler = logging.FileHandler(filename=log_file, encoding="utf-8")

            file_handler.setFormatter(formatter)

            self.__logger.addHandler(file_handler)

    def info(self, message: str) -> None:
        self.__logger.info(message)

    def warning(self, message: str) -> None:
        self.__logger.warning(message)

    def error(self, message: str) -> None:
        self.__logger.error(message)
