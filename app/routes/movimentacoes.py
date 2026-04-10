from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.produto import Produto
from app.models.movimentacao import Movimentacao

mov_bp = Blueprint("movimentacoes", __name__, url_prefix="/movimentacoes")


@mov_bp.route("/")
@login_required
def listar():
    page = request.args.get("page", 1, type=int)
    produto_id = request.args.get("produto_id", type=int)
    tipo = request.args.get("tipo", "")

    query = Movimentacao.query
    if produto_id:
        query = query.filter_by(produto_id=produto_id)
    if tipo in ("entrada", "saida"):
        query = query.filter_by(tipo=tipo)

    movs = query.order_by(Movimentacao.criado_em.desc()).paginate(page=page, per_page=30)
    produtos = Produto.query.filter_by(ativo=True).order_by(Produto.nome).all()
    return render_template("movimentacoes/listar.html", movimentacoes=movs,
                           produtos=produtos, produto_id=produto_id, tipo=tipo)


@mov_bp.route("/nova", methods=["GET", "POST"])
@login_required
def nova():
    produtos = Produto.query.filter_by(ativo=True).order_by(Produto.nome).all()
    produto_id = request.args.get("produto_id", type=int)

    if request.method == "POST":
        tipo = request.form.get("tipo")
        quantidade = request.form.get("quantidade", 0, type=int)
        produto_id = request.form.get("produto_id", type=int)
        justificativa = request.form.get("justificativa", "").strip()

        produto = Produto.query.get_or_404(produto_id)

        if tipo not in ("entrada", "saida"):
            flash("Tipo inválido.", "danger")
            return render_template("movimentacoes/form.html", produtos=produtos)

        if quantidade <= 0:
            flash("Quantidade deve ser maior que zero.", "danger")
            return render_template("movimentacoes/form.html", produtos=produtos)

        if tipo == "saida" and produto.saldo_atual < quantidade:
            flash(f"Saldo insuficiente. Disponível: {produto.saldo_atual} {produto.unidade}.", "danger")
            return render_template("movimentacoes/form.html", produtos=produtos,
                                   produto_id=produto_id)

        mov = Movimentacao(
            tipo=tipo,
            quantidade=quantidade,
            produto_id=produto_id,
            usuario_id=current_user.id,
            justificativa=justificativa,
        )
        db.session.add(mov)
        db.session.commit()

        icone = "+" if tipo == "entrada" else "-"
        flash(f'{icone}{quantidade} {produto.unidade} de "{produto.nome}" registrado!', "success")

        if produto.abaixo_minimo:
            flash(f'Atenção: "{produto.nome}" está abaixo do estoque mínimo ({produto.estoque_minimo}).', "warning")

        return redirect(url_for("produtos.detalhe", id=produto_id))

    return render_template("movimentacoes/form.html", produtos=produtos, produto_id=produto_id)
