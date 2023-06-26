rmdir /s /q .\configuration\.migrations
docker exec -it default-pg dropdb -U postgres CRuMb
docker exec -it default-pg createdb -U postgres CRuMb
aerich --app aerich init-db
aerich --app accum_registers init-db
aerich --app directories init-db
aerich --app documents init-db
aerich --app info_registers init-db
