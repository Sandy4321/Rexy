"""Novel products for users."""

from UPeT.importer import pre_analyzed_importer
from datetime import datetime, timedelta
from .Rexy import config
from operator import itemgetter


class Novel:
    """Top new products."""

    def __init__(self, *args, **kwargs):
        self.top_n = kwargs['novel_number']
        self.days = kwargs['novel_days']
        pre_analyzed_db_name = kwargs['pre_analyzed_db_name']
        pre_importer = pre_analyzed_importer.PreImporter(db_name=pre_analyzed_db_name)
        self.all_products = pre_importer.import_products()

    def find_novels(self):
        products = [(p['id'],
                     p['metadata']['rate'],
                     p['metadata']['download_numbe'])
                    for p in self.all_products if self.validate_date(p['metadata']['submit_date'])]

        products = sorted(products, key=itemgetter(1, 2))
        return products[:self.top_n]

    def validate_date(self, date):
        date_format = config.date_format
        days = timedelta(days=self.days)
        return datetime.now() - datetime.strptime(date, date_format) < days
