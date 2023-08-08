from os import getenv


DATABASE = {
    'connections': {
        'default': {
            "engine": 'tortoise.backends.asyncpg',
            'credentials': {
                'host': getenv('DB_HOST', '127.0.0.1'),
                'port': getenv('DB_PORT', '5432'),
                'user': getenv('DB_USER', 'postgres'),
                'password': getenv('DB_PWD', 'postgres'),
                'database': getenv('DB_NAME', 'CRuMb'),
            },
        }
    },
    'apps': {
        'aerich': {'models': ['aerich.models']},
        'accum_registers': {'models': ['configuration.accum_registers.models']},
        'directories': {'models': ['configuration.directories.models']},
        'documents': {'models': ['configuration.documents.models']},
        'info_registers': {'models': ['configuration.info_registers.models']},
    },
    'use_tz': True,
    'timezone': 'Europe/Moscow'
}
