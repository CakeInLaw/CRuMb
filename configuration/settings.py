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
        'models': {
            'models': [
                'aerich.models',
                'configuration.accum_registers.models',
                'configuration.directories.models',
                'configuration.documents.models',
                'configuration.info_registers.models',
            ]
        }
    },
    'use_tz': False,
    'timezone': 'Europe/Moscow'
}
