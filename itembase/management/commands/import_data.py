from django.core.management.base import BaseCommand
import os
import pandas as pd
from itembase.models import Item

class Command(BaseCommand):
    help = 'Imports data from Excel into the database'

    def handle(self, *args, **kwargs):
        file_path = 'data/file.xlsx'

        # Ensure the file exists
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File {file_path} does not exist."))
            return

        # Load the Excel data
        xls = pd.ExcelFile(file_path)
        df_list1 = xls.parse("Лист1")

        # Split the values in column C by comma and take the first part
        df_list1["Номер схемы"] = df_list1["Номер схемы"].str.split().str[0].str.strip()

        # Populate the Django model
        items = {}
        for _, row in df_list1.iterrows():
            parent_code, child_code = row["Номер схемы"], row["Чертежный номер"]
            if parent_code not in items:
                parent_item, _ = Item.objects.get_or_create(code=parent_code)
                parent_item.scheme_name = row["Наименование схемы"]
                parent_item.name_russian = row["Название на русском"]
                parent_item.name_chinese = row["Название на китайском"]
                parent_item.quantity = row["Количество"]
                parent_item.save()
                items[parent_code] = parent_item

            if child_code not in items:
                child_item, _ = Item.objects.get_or_create(code=child_code)
                child_item.scheme_name = row["Наименование схемы"]
                child_item.name_russian = row["Название на русском"]
                child_item.name_chinese = row["Название на китайском"]
                child_item.quantity = row["Количество"]
                child_item.parent = items[parent_code]
                child_item.save()
                items[child_code] = child_item

        self.stdout.write(self.style.SUCCESS(f"Successfully imported data from {file_path} into the Item model!"))
