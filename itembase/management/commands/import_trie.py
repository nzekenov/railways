from django.core.management.base import BaseCommand
import os
import pandas as pd
from itembase.models import Item

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.code = None

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, code):
        node = self.root
        for char in code:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.code = code

    def find_closest_parent(self, code):
        node = self.root
        for char in code:
            if char in node.children:
                node = node.children[char]
            else:
                break
        while node and not node.is_end_of_word:
            # Traverse up the trie to find the closest parent
            node = next(iter(node.children.values()), None)
        return node.code if node else None

class Command(BaseCommand):
    help = 'Imports data from Excel into the database using Trie for orphans'

    def handle(self, *args, **kwargs):
        file_path = 'data/file.xlsx'

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File {file_path} does not exist."))
            return

        xls = pd.ExcelFile(file_path)
        df_list1 = xls.parse("Лист1")
        df_list1["Номер схемы"] = df_list1["Номер схемы"].astype(str).str.split().str[0].str.strip()
        df_list1["Чертежный номер"] = df_list1["Чертежный номер"].astype(str).str.strip()
        df_list1 = df_list1.sort_values(by="Номер схемы")

        trie = Trie()
        parents_track = []
        child_track = []
        items = {}

        for _, row in df_list1.iterrows():
            parent_code, child_code = row["Номер схемы"], row["Чертежный номер"]
            if parent_code not in items:
                parent_item, _ = Item.objects.get_or_create(code=parent_code)
                parents_track.append(parent_code)
                parent_item.scheme_name = row["Наименование схемы"]
                parent_item.name_russian = row["Название на русском"]
                parent_item.name_chinese = row["Название на китайском"]
                parent_item.quantity = row["Количество"]
                parent_item.save()
                items[parent_code] = parent_item
                trie.insert(parent_code)

            if child_code not in items:
                child_item, _ = Item.objects.get_or_create(code=child_code)
                child_track.append(child_code)
                child_item.scheme_name = row["Наименование схемы"]
                child_item.name_russian = row["Название на русском"]
                child_item.name_chinese = row["Название на китайском"]
                child_item.quantity = row["Количество"]
                child_item.parent = items[parent_code]
                child_item.save()
                items[child_code] = child_item
                trie.insert(child_code)

        parents = set(parents_track)
        children = set(child_track)
        roots = set(["PJ350200000", "PJ350150000", "PJ350170000"])

        orphans = parents - children - roots
        for orphan in orphans:
            closest_parent_code = trie.find_closest_parent(parent_code)
            if closest_parent_code:
                orphan_item, _ = Item.objects.get_or_create(code=orphan)
                orphan_item.parent = items[closest_parent_code]
                orphan_item.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully imported data from {file_path} into the Item model!"))
