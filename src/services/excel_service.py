from datetime import date
from pathlib import Path
import locale

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font

from config.path_resolver import PathResolver
from infrastructure.logging.logger_service import LoggerService


class ExcelService:
    """
    Genera archivos Excel a partir de un DataFrame.
    """

    MONTH_NAMES = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre",
    }

    def __init__(
        self,
        path_resolver: PathResolver,
        logger: LoggerService,
    ) -> None:
        self.__path_resolver = path_resolver
        self.__logger = logger

    def create_output_directory(self) -> Path:
        """
        Garantiza la existencia de recurso/.
        """

        try:
            output_directory = self.__path_resolver.get_resource_path()

            output_directory.mkdir(
                parents=True,
                exist_ok=True,
            )

            return output_directory

        except Exception as ex:
            self.__logger.error(f"Error creando directorio recurso: {ex}")
            raise

    def build_file_name(
        self,
        period_start_date: date,
    ) -> str:
        """
        Construye el nombre del archivo.
        """

        month_name = self.MONTH_NAMES[period_start_date.month]

        return (
            f"Reporte Sociodemografico "
            f"{month_name} "
            f"{period_start_date.year}.xlsx"
        )

    def build_file_path(
        self,
        period_start_date: date,
    ) -> Path:
        """
        Construye la ruta completa del archivo.
        """

        output_directory = self.create_output_directory()

        file_name = self.build_file_name(period_start_date)

        return output_directory / file_name

    def export(
        self,
        dataframe: pd.DataFrame,
        period_start_date: date,
    ) -> Path:
        """
        Exporta un DataFrame a Excel.
        """

        try:
            file_path = self.build_file_path(period_start_date)

            clean_dataframe = dataframe.copy()

            clean_dataframe = clean_dataframe.where(
                pd.notnull(clean_dataframe),
                None,
            )

            with pd.ExcelWriter(
                file_path,
                engine="openpyxl",
                mode="w",
            ) as writer:

                clean_dataframe.to_excel(
                    writer,
                    sheet_name="Hoja1",
                    index=False,
                )

            workbook = load_workbook(file_path)

            worksheet = workbook["Hoja1"]

            for cell in worksheet[1]:
                cell.font = Font(bold=True)

            workbook.save(file_path)
            workbook.close()

            self.__logger.info(f"Archivo generado: {file_path.name}")

            self.__logger.info(f"Ruta completa: {file_path}")

            self.__logger.info(f"Filas exportadas: {len(dataframe)}")

            return file_path

        except Exception as ex:
            self.__logger.error(f"Error generando Excel: {ex}")
            raise
