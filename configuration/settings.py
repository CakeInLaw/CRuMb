DATABASE = {
    'connections': {
        'default': {
            "engine": 'tortoise.backends.asyncpg',
            'credentials': {
                'host': '127.0.0.1',
                'port': '5432',
                'user': 'postgres',
                'password': 'postgres',
                'database': 'CRuMb',
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
