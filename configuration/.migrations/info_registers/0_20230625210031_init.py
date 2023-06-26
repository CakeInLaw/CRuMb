from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "dir__nomenclature" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    "child_name" VARCHAR(50) NOT NULL,
    "full_name" VARCHAR(300) NOT NULL,
    "type" VARCHAR(1) NOT NULL,
    "is_group" BOOL NOT NULL,
    "units" VARCHAR(1) NOT NULL,
    "parent_id" BIGINT REFERENCES "dir__nomenclature" ("id") ON DELETE RESTRICT
);
COMMENT ON COLUMN "dir__nomenclature"."type" IS 'EQUIPMENT: E\nHOZ: H\nINVENTORY: I\nRAWS: R\nPROVISION: P\nDISHES: D';
COMMENT ON COLUMN "dir__nomenclature"."units" IS 'UNITS: U\nKILOGRAMS: K\nLITERS: L\nCENTIMETERS: C\nMETERS: M';
CREATE TABLE IF NOT EXISTS "accum_register__nomenclature_stock" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "document_ref" VARCHAR(20) NOT NULL,
    "count" DOUBLE PRECISION NOT NULL,
    "dt" TIMESTAMPTZ NOT NULL,
    "commit" TEXT NOT NULL,
    "nomenclature_id" BIGINT NOT NULL REFERENCES "dir__nomenclature" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "accum_register__nomenclature_stock__result" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "count" DOUBLE PRECISION NOT NULL,
    "dt" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "nomenclature_id" BIGINT NOT NULL UNIQUE REFERENCES "dir__nomenclature" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "dir__operation_reasons" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(40) NOT NULL,
    "operation" SMALLINT NOT NULL
);
COMMENT ON COLUMN "dir__operation_reasons"."operation" IS 'WRITE_OFF: 1';
CREATE TABLE IF NOT EXISTS "dir__positions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "dir__price_groups" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "dir__customers" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    "register_address" VARCHAR(200) NOT NULL,
    "price_group_id" INT NOT NULL REFERENCES "dir__price_groups" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "dir__providers" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    "register_address" VARCHAR(200) NOT NULL
);
CREATE TABLE IF NOT EXISTS "dir__recipe_cards" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "text" TEXT NOT NULL,
    "product_id" BIGINT NOT NULL UNIQUE REFERENCES "dir__nomenclature" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "dir__recipe_cards__ingredients" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "order" SMALLINT NOT NULL,
    "product_id" BIGINT NOT NULL REFERENCES "dir__nomenclature" ("id") ON DELETE RESTRICT,
    "recipe_id" INT NOT NULL REFERENCES "dir__recipe_cards" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_dir__recipe_product_36517b" UNIQUE ("product_id", "recipe_id")
);
CREATE TABLE IF NOT EXISTS "dir__users" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(40)  UNIQUE,
    "password_hash" VARCHAR(200) NOT NULL,
    "password_change_dt" TIMESTAMPTZ NOT NULL,
    "password_salt" VARCHAR(50) NOT NULL,
    "is_superuser" BOOL NOT NULL  DEFAULT False,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "dir__customer_locations" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "order" SMALLINT NOT NULL,
    "delivery_address" VARCHAR(200) NOT NULL,
    "customer_id" INT NOT NULL REFERENCES "dir__customers" ("id") ON DELETE RESTRICT,
    "user_id" BIGINT NOT NULL UNIQUE REFERENCES "dir__users" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "dir__employees" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "last_name" VARCHAR(40) NOT NULL,
    "first_name" VARCHAR(40) NOT NULL,
    "fathers_name" VARCHAR(40) NOT NULL,
    "position_id" INT NOT NULL REFERENCES "dir__positions" ("id") ON DELETE RESTRICT,
    "user_id" BIGINT  UNIQUE REFERENCES "dir__users" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "doc__nomenclature_write_offs" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "conducted" BOOL NOT NULL  DEFAULT False,
    "dt" TIMESTAMPTZ NOT NULL,
    "comment" TEXT NOT NULL,
    "owner_id" INT NOT NULL REFERENCES "dir__employees" ("id") ON DELETE RESTRICT,
    "reason_id" INT NOT NULL REFERENCES "dir__operation_reasons" ("id") ON DELETE RESTRICT,
    "responsible_employee_id" INT NOT NULL REFERENCES "dir__employees" ("id") ON DELETE RESTRICT
);
COMMENT ON TABLE "doc__nomenclature_write_offs" IS 'Документ списания номенклатуры (СП)';
CREATE TABLE IF NOT EXISTS "doc__nomenclature_write_offs__values" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "order" SMALLINT NOT NULL,
    "count" DOUBLE PRECISION NOT NULL,
    "price" DOUBLE PRECISION NOT NULL,
    "doc_id" BIGINT NOT NULL REFERENCES "doc__nomenclature_write_offs" ("id") ON DELETE CASCADE,
    "nomenclature_id" BIGINT NOT NULL REFERENCES "dir__nomenclature" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "doc__product_assemblies" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "conducted" BOOL NOT NULL  DEFAULT False,
    "dt" TIMESTAMPTZ NOT NULL,
    "comment" TEXT NOT NULL,
    "count" DOUBLE PRECISION NOT NULL,
    "owner_id" INT NOT NULL REFERENCES "dir__employees" ("id") ON DELETE RESTRICT,
    "product_id" BIGINT NOT NULL REFERENCES "dir__nomenclature" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "doc__product_assemblies" IS 'Документ сборки номенклатуры (СБ). Может быть собран по техкартам, а может и вручную';
CREATE TABLE IF NOT EXISTS "doc__product_assemblies__values" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "order" SMALLINT NOT NULL,
    "count" DOUBLE PRECISION NOT NULL,
    "doc_id" BIGINT NOT NULL REFERENCES "doc__product_assemblies" ("id") ON DELETE CASCADE,
    "nomenclature_id" BIGINT NOT NULL REFERENCES "dir__nomenclature" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "doc__receives" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "conducted" BOOL NOT NULL  DEFAULT False,
    "dt" TIMESTAMPTZ NOT NULL,
    "comment" TEXT NOT NULL,
    "provider_doc_id" VARCHAR(20) NOT NULL,
    "provider_doc_dt" TIMESTAMPTZ NOT NULL,
    "owner_id" INT NOT NULL REFERENCES "dir__employees" ("id") ON DELETE RESTRICT,
    "provider_id" INT NOT NULL REFERENCES "dir__providers" ("id") ON DELETE RESTRICT
);
COMMENT ON TABLE "doc__receives" IS 'Документ приобретения товаров (ПТ)';
CREATE TABLE IF NOT EXISTS "doc__provider_returns" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "conducted" BOOL NOT NULL  DEFAULT False,
    "dt" TIMESTAMPTZ NOT NULL,
    "comment" TEXT NOT NULL,
    "owner_id" INT NOT NULL REFERENCES "dir__employees" ("id") ON DELETE RESTRICT,
    "receive_id" BIGINT NOT NULL REFERENCES "doc__receives" ("id") ON DELETE RESTRICT
);
COMMENT ON TABLE "doc__provider_returns" IS 'Документ возврата приобретения товаров (ВПТ) поставщику';
CREATE TABLE IF NOT EXISTS "doc__provider_returns__values" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "order" SMALLINT NOT NULL,
    "count" DOUBLE PRECISION NOT NULL,
    "price" DOUBLE PRECISION NOT NULL,
    "doc_id" BIGINT NOT NULL REFERENCES "doc__provider_returns" ("id") ON DELETE CASCADE,
    "nomenclature_id" BIGINT NOT NULL REFERENCES "dir__nomenclature" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "doc__receives__values" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "order" SMALLINT NOT NULL,
    "count" DOUBLE PRECISION NOT NULL,
    "price" DOUBLE PRECISION NOT NULL,
    "doc_id" BIGINT NOT NULL REFERENCES "doc__receives" ("id") ON DELETE CASCADE,
    "nomenclature_id" BIGINT NOT NULL REFERENCES "dir__nomenclature" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "doc__sales" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "conducted" BOOL NOT NULL  DEFAULT False,
    "dt" TIMESTAMPTZ NOT NULL,
    "comment" TEXT NOT NULL,
    "customer_id" INT NOT NULL REFERENCES "dir__customers" ("id") ON DELETE RESTRICT,
    "owner_id" INT NOT NULL REFERENCES "dir__employees" ("id") ON DELETE RESTRICT
);
COMMENT ON TABLE "doc__sales" IS 'Документ продажи товаров (ПР)';
CREATE TABLE IF NOT EXISTS "doc__customer_returns" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "conducted" BOOL NOT NULL  DEFAULT False,
    "dt" TIMESTAMPTZ NOT NULL,
    "comment" TEXT NOT NULL,
    "owner_id" INT NOT NULL REFERENCES "dir__employees" ("id") ON DELETE RESTRICT,
    "sale_id" BIGINT NOT NULL REFERENCES "doc__sales" ("id") ON DELETE RESTRICT
);
COMMENT ON TABLE "doc__customer_returns" IS 'Документ возврата продажи товаров (ВПР) от покупателя';
CREATE TABLE IF NOT EXISTS "doc__customer_returns__values" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "order" SMALLINT NOT NULL,
    "count" DOUBLE PRECISION NOT NULL,
    "price" DOUBLE PRECISION NOT NULL,
    "doc_id" BIGINT NOT NULL REFERENCES "doc__customer_returns" ("id") ON DELETE CASCADE,
    "nomenclature_id" BIGINT NOT NULL REFERENCES "dir__nomenclature" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "doc__sales__values" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "order" SMALLINT NOT NULL,
    "count" DOUBLE PRECISION NOT NULL,
    "price" DOUBLE PRECISION NOT NULL,
    "doc_id" BIGINT NOT NULL REFERENCES "doc__sales" ("id") ON DELETE CASCADE,
    "nomenclature_id" BIGINT NOT NULL REFERENCES "dir__nomenclature" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "doc__stocktakes" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "conducted" BOOL NOT NULL  DEFAULT False,
    "dt" TIMESTAMPTZ NOT NULL,
    "comment" TEXT NOT NULL,
    "owner_id" INT NOT NULL REFERENCES "dir__employees" ("id") ON DELETE RESTRICT
);
COMMENT ON TABLE "doc__stocktakes" IS 'Документ инвентаризации (ИН).';
CREATE TABLE IF NOT EXISTS "doc__stocktakes__values" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "order" SMALLINT NOT NULL,
    "count" DOUBLE PRECISION NOT NULL,
    "doc_id" BIGINT NOT NULL REFERENCES "doc__stocktakes" ("id") ON DELETE CASCADE,
    "nomenclature_id" BIGINT NOT NULL REFERENCES "dir__nomenclature" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "info_register__nomenclature_costs" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "document_ref" VARCHAR(20),
    "cost" DOUBLE PRECISION NOT NULL,
    "count" DOUBLE PRECISION NOT NULL,
    "dt" TIMESTAMPTZ NOT NULL,
    "nomenclature_id" BIGINT NOT NULL REFERENCES "dir__nomenclature" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "reg_info__nomenclature_prices" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "document_ref" VARCHAR(20) NOT NULL,
    "price" DOUBLE PRECISION NOT NULL,
    "dt" TIMESTAMPTZ NOT NULL,
    "nomenclature_id" BIGINT NOT NULL REFERENCES "dir__nomenclature" ("id") ON DELETE RESTRICT,
    "price_group_id" INT NOT NULL REFERENCES "dir__price_groups" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
