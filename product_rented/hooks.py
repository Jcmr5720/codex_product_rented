import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)

_RAW_TO_CODE = {
    "1 mes": "1m",
    "un mes": "1m",
    "1m": "1m",
    "2 meses": "2m",
    "dos meses": "2m",
    "2m": "2m",
    "3 meses": "3m",
    "tres meses": "3m",
    "3m": "3m",
    "6 meses": "6m",
    "seis meses": "6m",
    "6m": "6m",
    "1 año": "1y",
    "un año": "1y",
    "1y": "1y",
    "2 años": "2y",
    "dos años": "2y",
    "2y": "2y",
}


def _normalize_raw_value(raw_value):
    if not raw_value:
        return False
    normalized = raw_value.strip().lower()
    return _RAW_TO_CODE.get(normalized)


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    option_model = env["product.rented.time.option"]
    options = option_model.search([])
    option_by_code = {opt.code: opt.id for opt in options if opt.code}

    if not option_by_code:
        _logger.info("No hay opciones de tiempo de renta preconfiguradas; se omite la migración de datos")
        return

    cr.execute(
        "SELECT id, rented_time FROM product_template WHERE rented_time IS NOT NULL AND rented_time != ''"
    )
    rows = cr.fetchall()
    if not rows:
        return

    assignments = {}
    for product_id, raw_value in rows:
        code = _normalize_raw_value(raw_value)
        if not code:
            _logger.debug(
                "Valor de renta '%s' en producto %s no coincide con ninguna opción predefinida", raw_value, product_id
            )
            continue
        option_id = option_by_code.get(code)
        if not option_id:
            _logger.debug(
                "No se encontró una opción configurada para el código '%s' en el producto %s", code, product_id
            )
            continue
        assignments.setdefault(product_id, set()).add(option_id)

    if not assignments:
        return

    product_model = env["product.template"].with_context(active_test=False)
    for product_id, option_ids in assignments.items():
        product_model.browse(product_id).write({
            "rented_time_option_ids": [(6, 0, list(option_ids))],
        })
