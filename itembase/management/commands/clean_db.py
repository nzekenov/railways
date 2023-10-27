from django.core.management.base import BaseCommand
from itembase.models import Item

class Command(BaseCommand):
    help = 'Cleans all items from the database'

    def handle(self, *args, **kwargs):
        # Confirm with the user before deleting
        user_input = input("Are you sure you want to delete all items? (Y/N): ")
        if user_input.lower() == 'y':
            count = Item.objects.all().delete()[0]
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} items from the database!'))
        else:
            self.stdout.write(self.style.WARNING('Operation aborted. No items were deleted.'))
