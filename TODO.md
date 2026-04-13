# TODO: Sistema (ex-Definições) Redesign
Status: [IN PROGRESS]

## Steps:
- [x] 1. Update sidebar in artemis/templates/layout.html (rename Definições → Sistema, update urlname check to 'sistema')
- [x] 2. Update artemis/definicoes/urls.py (rename name='sistema', add path('create-user/', ...))
- [ ] 3. Update artemis/definicoes/views.py (rename view to sistemaPage, add users context, add create_user POST handler)
- [x] 4. Overhaul artemis/definicoes/templates/definicoes/definicoes.html (2 tabs: Geral=form+list, Integrações; modern design)
- [ ] 5. Test: Create user, list updates, no errors
- [ ] 6. Mark complete, runserver verify

Next step: #5 Test

