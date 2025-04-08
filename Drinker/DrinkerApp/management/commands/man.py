from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "options: \n --data\n --app \n --migrate"

    def add_arguments(self,parser):
        parser.add_argument('--data', action='store_true', help="czy pokazać jak załadować dane")
        parser.add_argument('--app', action='store_true', help="czy pokazać jak uruchomić aplikacje")
        parser.add_argument('--migrate', action='store_true', help="czy pokazać jak uruchomić migracje")
    
    def handle(self, *args, **options):
        dane=options['data']
        app = options['app']
        migrate = options['migrate']
        if dane:
            self.stdout.write(self.style.WARNING("żeby załadować dane potrzebny jest stworzony przynajmniej jeden user,\n komenda ładowania danych to 'python3 manage.py loaddata drinki.json'"))
        elif app:
            self.stdout.write(self.style.WARNING("uruchomienie aplikacji komenda 'python3 manage.py runserver'"))
        elif migrate:
            self.stdout.write(self.style.WARNING("żeby załadować migracje jest komenda 'python3 manage.py migrate'"))
        else:
            self.stdout.write(self.style.WARNING(self.help))