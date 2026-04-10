from app import db
from datetime import datetime


class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    produtos = db.relationship("Produto", backref="categoria", lazy=True)

    def __repr__(self):
        return f"<Categoria {self.nome}>"


class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    descricao = db.Column(db.Text)
    unidade = db.Column(db.String(20), default="un")
    estoque_minimo = db.Column(db.Integer, default=0)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"))
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    movimentacoes = db.relationship("Movimentacao", backref="produto", lazy=True)

    @property
    def saldo_atual(self):
        """Calcula o saldo somando entradas e subtraindo saídas."""
        from app.models.movimentacao import Movimentacao
        entradas = db.session.query(
            db.func.coalesce(db.func.sum(Movimentacao.quantidade), 0)
        ).filter(
            Movimentacao.produto_id == self.id,
            Movimentacao.tipo == "entrada"
        ).scalar()

        saidas = db.session.query(
            db.func.coalesce(db.func.sum(Movimentacao.quantidade), 0)
        ).filter(
            Movimentacao.produto_id == self.id,
            Movimentacao.tipo == "saida"
        ).scalar()

        return int(entradas) - int(saidas)

    @property
    def abaixo_minimo(self):
        return self.saldo_atual < self.estoque_minimo

    def __repr__(self):
        return f"<Produto {self.codigo} - {self.nome}>"
