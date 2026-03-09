"""adicionando coluna id_usuario na tabela financas

Revision ID: c2d089301c94
Revises: 98e89563bc44
Create Date: 2026-03-07 14:13:56.428281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2d089301c94'
down_revision: Union[str, Sequence[str], None] = '98e89563bc44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Usamos o batch_alter_table para o SQLite conseguir recriar a tabela
    with op.batch_alter_table('financas', schema=None) as batch_op:
        # 1. Adicionamos a coluna 'id_usuario' (inteiro)
        batch_op.add_column(sa.Column('id_usuario', sa.Integer(), nullable=True))
        
        # 2. Criamos a Chave Estrangeira com o nome e apontando para 'id_usuario'
        batch_op.create_foreign_key('fk_financas_usuario', 'usuario', ['id_usuario'], ['id'])


def downgrade() -> None:
    with op.batch_alter_table('financas', schema=None) as batch_op:
        batch_op.drop_constraint('fk_financas_usuario', type_='foreignkey')
        batch_op.drop_column('id_usuario')
