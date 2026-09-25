from pathlib import Path
import sys


class PathResolver:
    """
    Resuelve rutas físicas compatibles con:
    - Desarrollo
    - PyInstaller
    - Windows Task Scheduler
    """

    @staticmethod
    def get_base_path() -> Path:
        if hasattr(sys, "_MEIPASS"):
            return Path(sys._MEIPASS)

        return Path(__file__).resolve().parent.parent.parent

    @classmethod
    def get_env_path(cls) -> Path:
        return cls.get_base_path() / ".env"

    @classmethod
    def get_log_file_path(cls) -> Path:
        logs_dir = cls.get_base_path() / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)

        return logs_dir / "log.txt"

    @classmethod
    def get_resource_path(cls) -> Path:
        """
        Retorna la ruta física de recurso/.
        """

        return cls.get_base_path() / "recurso"
