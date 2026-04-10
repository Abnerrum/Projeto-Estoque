from app import db
from datetime import datetime


class Movimentacao(db.Model):
    __tablename__ = "movimentacoes"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10), nullable=False)          # 'entrada' ou 'saida'
    quantidade = db.Column(db.Integer, nullable=False)
    justificativa = db.Column(db.String(255))
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Movimentacao {self.tipo} {self.quantidade} - produto {self.produto_id}>"
