# coding: utf-8
# Copyright 2020 GRAP
from openupgradelib import openupgrade


def populate_sale_order_effective_date(cr):
    openupgrade.logged_query(
        cr, "ALTER TABLE sale_order ADD effective_date date;")
    cr.execute("""
        UPDATE sale_order
        SET effective_date = sub_request.min_date
        FROM(
            SELECT so.id, min(sp.date) min_date
            FROM sale_order so
            INNER JOIN procurement_group pg
            on so.procurement_group_id = pg.id
            INNER JOIN stock_picking sp
            on sp.group_id = pg.id
            group by so.id
            ) sub_request
        WHERE sale_order.id = sub_request.id;
    """)


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    cr = env.cr
    populate_sale_order_effective_date(cr)
