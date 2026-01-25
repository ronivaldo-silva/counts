# Technical Memory - Counts2 Project

## Environment Metadata
- **Operating System**: Windows
- **Virtual Environment**: `.venv` (located in project root)
- **Primary Language**: Python (Object-Oriented)
- **Architecture**: MVC (Model-View-Controller)
- **Deployment Platform**: Render

## Library Versions (Active)
- **Flet**: `0.80.4` (Note: User rules mentioned 0.28.3, but environment is 0.80.4)
- **SQLAlchemy**: `2.0.45`
- **FastAPI**: `0.128.0`

## Flet 0.80.0+ Migration Notes
Starting from Flet version 0.80.0, several methods and components were renamed or deprecated.

### Dialogs & Overlays
- **Opening Dialogs**: Use `page.show_dialog(control)` instead of `page.open(control)`.
- **Closing Dialogs**: Use `page.pop_dialog()` for simple dismissal or `page.close(dialog)` for specific controls.
- **SnackBars**: Property `.open = True` still works, but focus on current page methods.

### Component Deprecations
- **ElevatedButton**: Deprecated in version 0.80.0. Use `ft.Button` or `ft.FilledButton` instead.
- **Icons & Colors**: Use snake_case format (e.g., `ft.Colors.BLACK_87` instead of `ft.Colors.BLACK87`).
- **Styles**: Use direct constructors like `ft.Border.all()` instead of `ft.border.all()` and `ft.Margin.only()` instead of `ft.margin.only()`.

## Documentation Reference
- **Main Catalog**: `https://docs.flet.dev/controls/`
- **Specific Controls**: `https://docs.flet.dev/controls/<control_name>/`
  - Example: `https://docs.flet.dev/controls/alertdialog/`
  - Example: `https://docs.flet.dev/controls/page/`

## Internal Workflow
- Always verify available methods via documentation when encounter `AttributeError` on common Flet attributes.
- Use `.venv\Scripts\python.exe` for running commands to ensure correct library context.
