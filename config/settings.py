"""
Configuración general del proyecto.
Lee variables de entorno desde .env
"""

import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig:
    HOST: str = os.getenv("DB_HOST", "localhost")
    PORT: int = int(os.getenv("DB_PORT", 5432))
    NAME: str = os.getenv("DB_NAME", "")
    USER: str = os.getenv("DB_USER", "")
    PASSWORD: str = os.getenv("DB_PASSWORD", "")

    @classmethod
    def dsn(cls) -> str:
        """Retorna el DSN de conexión a PostgreSQL."""
        return (
            f"postgresql://{cls.USER}:{cls.PASSWORD}"
            f"@{cls.HOST}:{cls.PORT}/{cls.NAME}"
        )


class AppConfig:
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "output")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
