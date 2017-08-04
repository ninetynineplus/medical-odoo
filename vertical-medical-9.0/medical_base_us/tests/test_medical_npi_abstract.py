# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp.tests.common import TransactionCase
from openerp import api, fields, models
from openerp.exceptions import ValidationError


class MedicalNpiAbstractTestMixer(TransactionCase):

    def setUp(self):
        super(MedicalNpiAbstractTestMixer, self).setUp()

        MedicalTestNpi._build_model(self.registry, self.cr)
        self.model_obj = self.env[MedicalTestNpi._name]
        self.model_obj._prepare_setup()
        self.model_obj._setup_base(False)
        self.model_obj._setup_fields(False)
        self.model_obj._setup_complete()

        self.valid = [
            1538596788,
            1659779064,
        ]
        self.invalid = [
            1659779062,
            1538696788,
            4949558680,
        ]
        self.country_us = self.env['res.country'].search([
            ('code', '=', 'US'),
        ],
            limit=1,
        )


class MedicalTestNpi(models.Model):
    _name = 'medical.test.npi'
    _inherit = 'medical.abstract.npi'
    ref = fields.Char()
    country_id = fields.Many2one('res.country')

    @api.multi
    @api.constrains('ref')
    def _check_ref(self):
        self._npi_constrains_helper('ref')


class TestMedicalNpiAbstract(MedicalNpiAbstractTestMixer):

    def test_valid_int(self):
        """ Test _npi_is_valid returns True if valid int input """
        for i in self.valid:
            self.assertTrue(
                self.model_obj._npi_is_valid(i),
                'Npi validity check on int %s did not pass for valid' % i,
            )

    def test_valid_str(self):
        """ Test _npi_is_valid returns True if valid str input """
        for i in self.valid:
            self.assertTrue(
                self.model_obj._npi_is_valid(str(i)),
                'Npi validity check on str %s did not pass for valid' % i,
            )

    def test_invalid_int(self):
        """ Test _npi_is_valid returns False if invalid int input """
        for i in self.invalid:
            self.assertFalse(
                self.model_obj._npi_is_valid(i),
                'Npi validity check on int %s did not fail for invalid' % i,
            )

    def test_invalid_str(self):
        """ Test _npi_is_valid returns False if invalid str input """
        for i in self.invalid:
            self.assertFalse(
                self.model_obj._npi_is_valid(str(i)),
                'Npi validity check on str %s did not fail for invalid' % i,
            )

    def test_false(self):
        """ Test _npi_is_valid fails greacefully if given no/Falsey input """
        self.assertFalse(
            self.model_obj._npi_is_valid(False),
            'Npi validity check on False did not fail gracefully',
        )

    def test_constrain_valid_us(self):
        """ Test _npi_constrains_helper no ValidationError if valid ref """
        test_model = self.env['medical.test.npi'].new({
            'ref': self.valid[0],
            'country_id': self.country_us.id,
        })

        try:
            test_model._check_ref()
        except ValidationError:
            self.fail('A ValidationError was raised and should not have been.')

    def test_constrain_invalid_us(self):
        """ Test _npi_constrains_helper raise ValidationError invalid ref """
        test_model = self.env['medical.test.npi'].new({
            'ref': self.invalid[0],
            'country_id': self.country_us.id,
        })

        with self.assertRaises(ValidationError):
            test_model._check_ref()

    def test_constrain_invalid_non_us(self):
        """ Test _npi_constrains_helper skips validation if not US """
        test_model = self.env['medical.test.npi'].new({
            'ref': self.invalid[0],
            'country_id': self.country_us.id + 1,
        })

        try:
            test_model._check_ref()
        except ValidationError:
            self.fail('A ValidationError was raised and should not have been.')
