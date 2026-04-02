from django.apps import AppConfig


class FuncionariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'funcionarios'
    
    def ready(self):
        """Registar os signals quando a app estiver pronta"""
        import funcionarios.signals
