# -*- coding: utf-8 -*-
# Copyright 2015 ACSONE SA/NV
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_medicament = fields.Boolean(
        readonly=True,
        help='Check if the product is a medicament',
    )
    is_vaccine = fields.Boolean(
        string='Vaccine',
        help='Check if the product is a vaccine',
    )
