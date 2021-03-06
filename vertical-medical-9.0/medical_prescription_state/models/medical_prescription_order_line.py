# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import models


class MedicalPrescriptionOrderLine(models.Model):
    """ Add Kanban functionality to MedicalPrescriptionOrderLine """
    _inherit = ['medical.prescription.order.line', 'base.kanban.abstract']
    _name = 'medical.prescription.order.line'
