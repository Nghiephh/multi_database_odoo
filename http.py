import odoo.service.db
from odoo import http
from odoo.http import request
from odoo.tools import config
from contextlib import closing
import re
import logging

_logger = logging.getLogger(__name__)


def db_filter_custom(dbs, host=None):
    """
    Return the subset of ``dbs`` that match the dbfilter or the dbname
    server configuration. In case neither are configured, return ``dbs``
    as-is.

    :param Iterable[str] dbs: The list of database names to filter.
    :param host: The Host used to replace %h and %d in the dbfilters
        regexp. Taken from the current request when omitted.
    :returns: The original list filtered.
    :rtype: List[str]
    """

    if config['dbfilter']:
        #        host
        #     -----------
        # www.example.com:80
        #     -------
        #     domain
        if host is None:
            host = request.httprequest.environ.get('HTTP_HOST', '')
        host = host.partition(':')[0]
        if host.startswith('www.'):
            host = host[4:]
        domain = host.partition('.')[0]

        id_db = 0
        db = odoo.sql_db.db_connect(config['dbmain'])
        with closing(db.cursor()) as cr:
            try:
                cr.execute("select id from res_users as db where db.login = %s", ([str(re.escape(domain))]))
                id_db = cr.fetchall()
            except Exception:
                _logger.exception('Select databases failed!')

        dbfilter_re = re.compile(
            config["dbfilter"].replace("%h", re.escape(host))
                              .replace("%d", re.escape(domain))
                              .replace("%u", "db_" + str(id_db))
        )
        return [db for db in dbs if dbfilter_re.match(db)]

    if config['db_name']:
        # In case --db-filter is not provided and --database is passed, Odoo will
        # use the value of --database as a comma separated list of exposed databases.
        exposed_dbs = {db.strip() for db in config['db_name'].split(',')}
        return sorted(exposed_dbs.intersection(dbs))

    return list(dbs)

http.db_filter = db_filter_custom
