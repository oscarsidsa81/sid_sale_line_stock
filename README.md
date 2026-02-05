# sid_sale_line_stock

## PropÃ³sito
AÃ±adir a `sale.order.line` el **stock pronosticado** (`virtual_available`) en las ubicaciones de stock del almacÃ©n localizado por:
- `base.state_es_m` (Madrid)
- `base.state_es_cr` (Ciudad Real / Puertollano)

## Campos
- `sid_qty_stock_mad` (compute, no-store)
- `sid_qty_stock_ptllno` (compute, no-store)

## Dependencias
- `sale`, `sale_stock`, `stock`
