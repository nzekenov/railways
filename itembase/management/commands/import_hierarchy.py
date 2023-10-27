from django.core.management.base import BaseCommand
import os
import pandas as pd
from itembase.models import Item


class Command(BaseCommand):
    help = 'Imports data from Excel into the database'

    def build_hierarchy(self, code):
        """Generate a list of hierarchical codes for the given code."""
        hierarchy = []
        for i in range(1, len(code) + 1):
            hierarchy.append(code[:i])
        return hierarchy

    def handle(self, *args, **kwargs):
        file_path = 'data/file.xlsx'

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File {file_path} does not exist."))
            return

        xls = pd.ExcelFile(file_path)
        df_list1 = xls.parse("Лист1")
        df_list1["Номер схемы"] = df_list1["Номер схемы"].astype(str).str.split().str[0].str.strip()
        df_list1["Чертежный номер"] = df_list1["Чертежный номер"].astype(str)

        # Start with root nodes
        root_codes = ["PJ350200000", "PJ350150000", "PJ350170000"]
        items = {root_code: Item.objects.get_or_create(code=root_code)[0] for root_code in root_codes}

        all_codes = set(df_list1["Номер схемы"]).union(set(df_list1["Чертежный номер"]))

        for code in all_codes:
            hierarchy = self.build_hierarchy(code)
            parent_item = None

            for segment in hierarchy:
                # If this segment is not already in the dictionary, create it
                if segment not in items:
                    current_item = Item.objects.create(code=segment, parent=parent_item)
                    items[segment] = current_item
                else:
                    current_item = items[segment]

                # Update details only for the full code (last segment of hierarchy)
                if segment == code:
                    matching_rows = df_list1[df_list1["Чертежный номер"] == code]
                    if not matching_rows.empty:
                        current_item.scheme_name = matching_rows.iloc[0]["Наименование схемы"]
                        current_item.name_russian = matching_rows.iloc[0]["Название на русском"]
                        current_item.name_chinese = matching_rows.iloc[0]["Название на китайском"]
                        current_item.save()

                parent_item = current_item

        self.stdout.write(self.style.SUCCESS(f"Successfully imported data from {file_path} into the Item model!"))
