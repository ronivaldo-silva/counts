---
trigger: always_on
---

Agente especialista em Python orientado a objeto e estrutura MVC.

Escreva pensando na aplicação rodando web hospedada em plataforma Render.

Seja atualizado na versão 0.80.4 da biblioteca flet (Ambiente Virtual atual).

IMPORTANTE (Migração 0.80.0+):
- Use `page.show_dialog(dialog)` em vez de `page.open(dialog)`.
- Use `page.pop_dialog()` ou `page.close(dialog)` para fechar.
- Substiuir `ElevatedButton` por `ft.Button` ou `ft.FilledButton` quando possível.
- Validar métodos e atributos na documentação atualizada: https://flet.dev/docs/controls/<control> (ex: /alertdialog, /page).