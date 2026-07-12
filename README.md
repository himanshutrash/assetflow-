# AssetFlow

**Enterprise Asset & Resource Management System** — built for the Odoo Hackathon.

Track, allocate, and audit organizational assets — from procurement to retirement —
in one unified platform. Handles departments, employees, asset lifecycles,
allocations/transfers, shared resource bookings, maintenance approvals, and
structured audit cycles.

## Stack

- **Backend:** Flask, Flask-SQLAlchemy, Flask-Login
- **Database:** SQLite (swap `DATABASE_URL` for Postgres in production)
- **Frontend:** Server-rendered Jinja templates, no JS framework — kept lean for
  hackathon speed

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # edit SECRET_KEY
python run.py
```

Visit `http://127.0.0.1:5000`. A default Admin account is seeded on first run:

- **Email:** admin@assetflow.local
- **Password:** admin123

Change this immediately in any shared/demo environment.

## Status

**Built so far:**
- [x] Data models for all core entities (departments, users, assets, allocations,
      transfers, bookings, maintenance requests, audit cycles, notifications, activity log)
- [x] Auth: signup (Employee-only, no self-assigned roles), login, logout
- [x] Dashboard with live KPIs, overdue/upcoming returns
- [x] Design system (`app/static/css/style.css`) — see design notes below

**Not yet built:**
- [ ] Organization Setup (Admin: departments / categories / employee directory + role promotion)
- [ ] Asset Registration & Directory
- [ ] Asset Allocation & Transfer (with double-allocation conflict handling)
- [ ] Resource Booking (with overlap validation)
- [ ] Maintenance Management workflow
- [ ] Asset Audit cycles
- [ ] Reports & Analytics
- [ ] Activity Logs & Notifications UI

## Design notes

Visual identity is grounded in the asset tag itself (`AF-0001`) — the one artifact
every screen revolves around. The signature UI element is a "tag-chip": a small
rectangle with a punched circle on the left, echoing a physical hang-tag. It's
used for asset codes, status badges, and the sidebar brand mark, so the interface
itself looks tagged the same way the assets it tracks are.

- **Color:** paper `#F6F5F1`, ink `#1A1F23`, teal `#24575C` (primary), amber `#E7A23B`
  (accent/warnings), plus status colors for success/danger/info
- **Type:** Space Grotesk (headings), IBM Plex Sans (body/UI), IBM Plex Mono
  (asset tags/codes)

All tokens live at the top of `app/static/css/style.css` — change them there and
the whole app updates.
