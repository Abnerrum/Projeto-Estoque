from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models.produto import Produto, Categoria

produtos_bp = Blueprint("produtos", __name__, url_prefix="/produtos")


@produtos_bp.route("/")
@login_required
def listar():
    busca = request.args.get("q", "")
    categoria_id = request.args.get("categoria", type=int)
    apenas_criticos = request.args.get("criticos", False)

    query = Produto.query.filter_by(ativo=True)
    if busca:
        query = query.filter(
            (Produto.nome.ilike(f"%{busca}%")) | (Produto.codigo.ilike(f"%{busca}%"))
        )
    if categoria_id:
        query = query.filter_by(categoria_id=categoria_id)

    produtos = query.order_by(Produto.nome).all()

    if apenas_criticos:
        produtos = [p for p in produtos if p.abaixo_minimo]

    categorias = Categoria.query.order_by(Categoria.nome).all()
    return render_template("produtos/listar.html", produtos=produtos,
                           categorias=categorias, busca=busca,
                           categoria_id=categoria_id)


@produtos_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    categorias = Categoria.query.order_by(Categoria.nome).all()

    if request.method == "POST":
        codigo = request.form.get("codigo", "").strip().upper()
        nome = request.form.get("nome", "").strip()
        descricao = request.form.get("descricao", "").strip()
        unidade = request.form.get("unidade", "un")
        estoque_minimo = request.form.get("estoque_minimo", 0, type=int)
        categoria_id = request.form.get("categoria_id", type=int) or None

        if Produto.query.filter_by(codigo=codigo).first():
            flash("Já existe um produto com este código.", "danger")
            return render_template("produtos/form.html", categorias=categorias)

        produto = Produto(nome=nome, codigo=codigo, descricao=descricao,
                          unidade=unidade, estoque_minimo=estoque_minimo,
                          categoria_id=categoria_id)
        db.session.add(produto)
        db.session.commit()
        flash(f'Produto "{nome}" cadastrado com sucesso!', "success")
        return redirect(url_for("produtos.listar"))

    return render_template("produtos/form.html", categorias=categorias, produto=None)


@produtos_bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar(id):
    produto = Produto.query.get_or_404(id)
    categorias = Categoria.query.order_by(Categoria.nome).all()

    if request.method == "POST":
        produto.nome = request.form.get("nome", "").strip()
        produto.descricao = request.form.get("descricao", "").strip()
        produto.unidade = request.form.get("unidade", "un")
        produto.estoque_minimo = request.form.get("estoque_minimo", 0, type=int)
        produto.categoria_id = request.form.get("categoria_id", type=int) or None
        db.session.commit()
        flash("Produto atualizado!", "success")
        return redirect(url_for("produtos.detalhe", id=produto.id))

    return render_template("produtos/form.html", produto=produto, categorias=categorias)


@produtos_bp.route("/<int:id>")
@login_required
def detalhe(id):
    produto = Produto.query.get_or_404(id)
    historico = sorted(produto.movimentacoes, key=lambda m: m.criado_em, reverse=True)[:20]
    return render_template("produtos/detalhe.html", produto=produto, historico=historico)


@produtos_bp.route("/<int:id>/desativar", methods=["POST"])
@login_required
def desativar(id):
    produto = Produto.query.get_or_404(id)
    produto.ativo = False
    db.session.commit()
    flash(f'Produto "{produto.nome}" desativado.', "info")
    return redirect(url_for("produtos.listar"))


# ── Categorias ──────────────────────────────────────────────────────────────

@produtos_bp.route("/categorias")
@login_required
def categorias():
    cats = Categoria.query.order_by(Categoria.nome).all()
    return render_template("produtos/categorias.html", categorias=cats)


@produtos_bp.route("/categorias/nova", methods=["POST"])
@login_required
def nova_categoria():
    nome = request.form.get("nome", "").strip()
    if nome and not Categoria.query.filter_by(nome=nome).first():
        db.session.add(Categoria(nome=nome))
        db.session.commit()
        flash(f'Categoria "{nome}" criada!', "success")
    else:
        flash("Nome inválido ou já existente.", "danger")
    return redirect(url_for("produtos.categorias"))
