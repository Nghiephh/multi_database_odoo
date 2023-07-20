# -*- coding: utf-8 -*-
from odoo import models, fields, _
from odoo.exceptions import UserError
from odoo.tools import config
import requests
import odoo


class ResUser(models.Model):
    _inherit = 'res.users'

    database_id = fields.Many2one('manager.database', string="Database Name")

    def action_create_database(self):
        vals = {
            "db_name": "db_" + str(self.id),
            "user_id": self.id
        }
        self.database_id = self.env['manager.database'].create(vals)
        master_pwd: str = config['master_pwd'] or ""
        name: str = self.database_id.db_name or ""
        # name: str = self.env.user.name or ""
        login: str = self.env.user.login or ""
        password: str = self.env.user.password or "123"
        phone: str = self.env.user.phone or ""
        lang: str = self.env.user.lang or ""
        country_code: str = self.env.user.country_code or ""
        demo: str = "1" or "0"

        if name in odoo.service.db.list_dbs():
            raise UserError(_("Database creation error: Database " + name + " already exists!"))

        end_point = self.env['ir.config_parameter'].sudo().get_param('web.base.url') + \
                    '/web/database/create?master_pwd=' \
                    + master_pwd + "&name=" + name + "&login=" + login + "&password=" + password + "&phone=" + phone +\
                    "&lang=" + lang + "&country_code=" + country_code + "&demo=" + demo
        response = requests.post(end_point)
        if response.url != 'http://localhost:8069/web/login':
            raise UserError(_("Create Database Fail!!!"))


class ManagerDatabase(models.Model):
    _name = 'manager.database'
    _description = 'Manager Database Of Users'

    db_name = fields.Char(string="Database name")
    user_id = fields.Many2one('res.users', string="User")
