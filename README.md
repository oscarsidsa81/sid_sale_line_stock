# sid_sale_line_stock

## Propósito
Añadir a `sale.order.line` el **stock pronosticado** (`virtual_available`) en las ubicaciones de stock del almacén localizado por:

- `base.state_es_m` (Madrid)
- `base.state_es_cr` (Ciudad Real / Puertollano)

## Campos

- `sid_qty_stock_mad`  
  Campo calculado (`compute`) no almacenado (`store=False`) que muestra el **stock pronosticado disponible en el almacén de Madrid**.

- `sid_qty_stock_ptllno`  
  Campo calculado (`compute`) no almacenado (`store=False`) que muestra el **stock pronosticado disponible en el almacén de Puertollano**.

## Dependencias

- `sale`
- `sale_stock`
- `stock`