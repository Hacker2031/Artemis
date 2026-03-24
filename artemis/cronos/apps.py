from django.apps import AppConfig


class CronosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cronos'

    def ready(self):
        """Inicializa a IA quando o Django está pronto"""
        try:
            from cronos.views import inicializar_ia
            print("Inicializando CRONOS IA...")
            if inicializar_ia():
                print("CRONOS IA inicializado com sucesso!")
            else:
                print("CRONOS IA não pôde ser inicializado completamente")
        except Exception as e:
            print(f"Erro ao inicializar CRONOS: {e}")
