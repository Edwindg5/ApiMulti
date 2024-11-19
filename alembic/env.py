from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy import create_engine
from alembic import context
import sys
import os

# Agrega la ruta del proyecto principal para importar db.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

# Importa la configuración existente de la base de datos
from app.shared.config.db import Base, DATABASE_URL

# Configuración del archivo de logging
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Aquí defines el modelo Base
target_metadata = Base.metadata

# Función para configurar migraciones offline
def run_migrations_offline():
    """Ejecuta migraciones en modo 'offline'."""
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# Función para configurar migraciones online
def run_migrations_online():
    """Ejecuta migraciones en modo 'online'."""
    connectable = create_engine(DATABASE_URL)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Determina si ejecuta en modo 'online' u 'offline'
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
