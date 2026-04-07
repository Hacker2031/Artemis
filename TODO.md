# TODO: Implementar Promoção de Candidatos Apurados para Funcionários

## Plano Aprovado
✅ Usar **ALL 5 fases aprovadas** em ProcessoSeletivo  
✅ Gerar **conta_bancaria = "AO" + f"{f_id:06d}"** (único)  
✅ **Modal preview** antes de promover  

## Passos Lógicos (Em Ordem)

### ✅ 1. Backend - rh/views.py
```
- Import: from funcionarios.models import Funcionarios, Controlo
- from django.db.models import Count, Q
- from datetime import date
- Add view: promover_candidatos_apurados(request)
  - Query candidatos com 5 etapas TODAS aprovadas
  - Bulk create Funcionarios + Controlo
  - Update Candidatos.estado='contratado'
  - Return JsonResponse({'criados':N, 'total':T, 'lista':[...]} )
```

### ✅ 2. URLs - artemis/rh/urls.py
```
path('api/promover-apurados/', views.promover_candidatos_apurados, name='promover_apurados'),
```

### ✅ 3. Preview Modal + Button - rh/templates/rh/rh.html
```
- Button no header: " Promover Apurados (X)"
- Modal: Lista candidatos preview → Confirmar
- JS fetch → POST → Show toast + reload
```

### [ ] 4. Testes
```
python manage.py shell → Test query candidatos_apurados
- Execute promote → Verify Funcionarios created
- Run `python manage.py migrate` if needed (unlikely)
```

### [ ] 5. Completion
```
attempt_completion
```

**Status: 3/5 passos completos**

