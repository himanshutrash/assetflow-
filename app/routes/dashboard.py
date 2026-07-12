from datetime import date
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import (
    Asset, Allocation, MaintenanceRequest, Booking, TransferRequest,
    ASSET_AVAILABLE, ASSET_ALLOCATED, ASSET_MAINTENANCE,
)

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def home():
    today = date.today()

    kpis = {
        "available": Asset.query.filter_by(status=ASSET_AVAILABLE).count(),
        "allocated": Asset.query.filter_by(status=ASSET_ALLOCATED).count(),
        "maintenance_today": MaintenanceRequest.query.filter(
            MaintenanceRequest.status.in_(["Approved", "TechnicianAssigned", "InProgress"])
        ).count(),
        "active_bookings": Booking.query.filter_by(status="Upcoming").count(),
        "pending_transfers": TransferRequest.query.filter_by(status="Requested").count(),
    }

    overdue = (
        Allocation.query.filter(
            Allocation.status == "Active",
            Allocation.expected_return_date.isnot(None),
            Allocation.expected_return_date < today,
        )
        .limit(10)
        .all()
    )

    upcoming = (
        Allocation.query.filter(
            Allocation.status == "Active",
            Allocation.expected_return_date.isnot(None),
            Allocation.expected_return_date >= today,
        )
        .order_by(Allocation.expected_return_date)
        .limit(10)
        .all()
    )

    return render_template(
        "dashboard.html", kpis=kpis, overdue=overdue, upcoming=upcoming, today=today
    )
