from tortoise.functions import Sum

from core.entities.accum_registers import AccumRegisterRepository, AccumRegisterResultRepository

from .model import NomenclatureStock, NomenclatureStockResult


class NomenclatureStockRepository(AccumRegisterRepository[NomenclatureStock]):
    model = NomenclatureStock

    async def recalc_results(self, records: list[NomenclatureStock]):
        nomenclatures_to_recalc: list[int] = []
        for rec in records:
            nomenclatures_to_recalc.append(rec.nomenclature_id)
        results = await self.model\
            .annotate(result=Sum('count'))\
            .filter(nomenclature_id__in=nomenclatures_to_recalc)\
            .group_by('nomenclature_id')\
            .values('nomenclature_id', 'result')
        await NomenclatureStockResultRepository().update_results(
            [(res['nomenclature_id'], res['result']) for res in results]
        )


class NomenclatureStockResultRepository(AccumRegisterResultRepository[NomenclatureStockResult]):
    model = NomenclatureStockResult

    async def update_results(self, results: list[tuple[int, float]]):
        existing_instances = await self.model\
            .filter(nomenclature_id__in=[res[0] for res in results])
        existing_instances_map: dict[int, NomenclatureStockResult] = {
            instance.nomenclature_id: instance for instance in existing_instances
        }
        new_instances = []
        for nomenclature_id, res_count in results:
            if instance := existing_instances_map.get(nomenclature_id):
                instance.count = res_count
            else:
                new_instances.append(self.model(
                    nomenclature_id=nomenclature_id,
                    count=res_count
                ))
        if existing_instances:
            await self.model.bulk_update(
                objects=existing_instances,
                fields=('count', 'dt'),
                batch_size=100,
            )
        if new_instances:
            await self.model.bulk_create(
                objects=new_instances,
                batch_size=100,
            )
