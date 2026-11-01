import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

#Ruta de los logs

CARPETA_LOGS = Path("log")
CARPETA_LOGS.mkdir(exist_ok=True)

CARPETA_DATA_LOGS = CARPETA_LOGS / "data_log"
CARPETA_DATA_LOGS.mkdir(exist_ok=True)

ARCHIVO_LOGS = CARPETA_LOGS / "gestor.log"

def configurar_logger():
    "configurar y producir un log rotativo"
    logger = logging.getLogger("GestorVentas")
    logger.setLevel(logging.INFO)


    #Para evitar duplicados en multiples llamadas
    if not logger.handlers:
        handler = RotatingFileHandler(
            ARCHIVO_LOGS,
            maxBytes=1_000_000,
            backupCount=5,
            encoding="utf-8"
        )

    #Redirigir el archivo a data_logs
        handler.namer = lambda name: str(CARPETA_DATA_LOGS / Path(name).name)

        formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)


    return logger