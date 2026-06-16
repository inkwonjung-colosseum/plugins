# Web Admin UI Kit — Colosseum WMS Console

A click-thru recreation of the Colosseum web admin console (WMS / OMS view). Uses the tokens defined in `../../colors_and_type.css`.

## Structure
**LNB-only layout.** No top GNB / Top bar in the current product version. The left sidebar (`Sidebar.jsx`) contains the logo at the top, navigation in the middle, and the user area at the bottom.

## Components
- `Sidebar.jsx` — LNB: logo + navigation + user area (all-in-one)
- `StatCard.jsx` — KPI summary cards for dashboard
- `DataTable.jsx` — Order table with filters, status tags, row actions
- `FilterBar.jsx` — Search + filter chips (Empty-State-First pattern)
- `OrderDetailDrawer.jsx` — Side-drawer order detail
- `Toast.jsx` — Web subtle toast system

## Surfaces
- **Dashboard** — KPI summary (hero count, status breakdown, recent orders)
- **Orders list** — Empty state → search → table with tags
- **Order detail** — Drawer overlay with line items + status timeline
- **Inventory** — SKU listing with stock-level tags

Open `index.html` to use the interactive demo.
