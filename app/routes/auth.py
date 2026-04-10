from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.usuario import Usuario

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("produtos.listar"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.check_senha(senha):
            login_user(usuario)
            next_page = request.args.get("next")
            flash(f"Bem-vindo, {usuario.nome}!", "success")
            return redirect(next_page or url_for("produtos.listar"))

        flash("Email ou senha incorretos.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    # Só permite registro se não houver nenhum usuário ainda (primeiro uso)
    if Usuario.query.count() > 0 and (not current_user.is_authenticated or not current_user.admin):
        flash("Contate o administrador para criar uma conta.", "warning")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")
        admin = Usuario.query.count() == 0  # primeiro usuário vira admin

        if Usuario.query.filter_by(email=email).first():
            flash("Email já cadastrado.", "danger")
            return render_template("auth/registro.html")

        usuario = Usuario(nome=nome, email=email, admin=admin)
        usuario.set_senha(senha)
        db.session.add(usuario)
        db.session.commit()
        flash("Conta criada com sucesso!", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/registro.html")
