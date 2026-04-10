from flask import redirect, url_for
from app import create_app, db
from app.models import Usuario, Produto, Categoria, Movimentacao

app = create_app("development")


@app.route("/")
def index():
    return redirect(url_for("produtos.listar"))


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Usuario=Usuario, Produto=Produto,
                Categoria=Categoria, Movimentacao=Movimentacao)


@app.cli.command("seed")
def seed():
    """Popula o banco com dados de exemplo."""
    db.create_all()

    # Usuário admin
    if not Usuario.query.filter_by(email="admin@estoque.com").first():
        admin = Usuario(nome="Administrador", email="admin@estoque.com", admin=True)
        admin.set_senha("admin123")
        db.session.add(admin)
        db.session.commit()
        print("✓ Usuário admin criado: admin@estoque.com / admin123")

    admin = Usuario.query.first()

    # Categorias
    cats = {}
    for nome in ["Alimentos", "Limpeza", "Eletrônicos", "Escritório"]:
        c = Categoria.query.filter_by(nome=nome).first() or Categoria(nome=nome)
        db.session.add(c)
        db.session.flush()
        cats[nome] = c
    db.session.commit()
    print("✓ Categorias criadas")

    # Produtos
    produtos_data = [
        ("ALIM-001", "Arroz 5kg",        "kg",  cats["Alimentos"],   10, 50),
        ("ALIM-002", "Feijão 1kg",       "kg",  cats["Alimentos"],   5,  8),
        ("LIMP-001", "Detergente 500mL", "un",  cats["Limpeza"],     20, 30),
        ("LIMP-002", "Água Sanitária",   "L",   cats["Limpeza"],     10, 5),
        ("ELET-001", "Cabo USB-C",       "un",  cats["Eletrônicos"], 5,  15),
        ("ESCR-001", "Resma de Papel",   "cx",  cats["Escritório"],  3,  2),
    ]

    for codigo, nome, unidade, cat, minimo, qtd in produtos_data:
        if Produto.query.filter_by(codigo=codigo).first():
            continue
        p = Produto(nome=nome, codigo=codigo, unidade=unidade,
                    categoria=cat, estoque_minimo=minimo)
        db.session.add(p)
        db.session.flush()
        mov = Movimentacao(tipo="entrada", quantidade=qtd,
                           produto_id=p.id, usuario_id=admin.id,
                           justificativa="Estoque inicial")
        db.session.add(mov)

    db.session.commit()
    print("✓ Produtos e movimentações de exemplo criados")
    print("\n🚀 Pronto! Acesse http://localhost:5000")
    print("   Login: admin@estoque.com | Senha: admin123")


if __name__ == "__main__":
    app.run(debug=True)