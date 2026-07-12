from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Department, ROLE_EMPLOYEE

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    departments = Department.query.filter_by(status="Active").order_by(Department.name).all()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        department_id = request.form.get("department_id") or None

        if not name or not email or not password:
            flash("All fields are required.", "error")
            return render_template("auth/signup.html", departments=departments)

        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "error")
            return render_template("auth/signup.html", departments=departments)

        # Signup always creates an Employee account. No role selection at signup —
        # role changes only happen through Admin > Organization Setup > Employee Directory.
        user = User(name=name, email=email, role=ROLE_EMPLOYEE, department_id=department_id)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Account created. You can now sign in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/signup.html", departments=departments)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            flash("Incorrect email or password.", "error")
            return render_template("auth/login.html")

        if user.status != "Active":
            flash("This account has been deactivated. Contact your Admin.", "error")
            return render_template("auth/login.html")

        login_user(user)
        return redirect(url_for("dashboard.home"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been signed out.", "info")
    return redirect(url_for("auth.login"))
