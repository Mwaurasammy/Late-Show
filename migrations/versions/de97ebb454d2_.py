"""empty message

Revision ID: de97ebb454d2
Revises: 173c2f574c68
Create Date: 2024-10-12 13:32:12.515207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de97ebb454d2'
down_revision = '173c2f574c68'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('episode', schema=None) as batch_op:
        batch_op.alter_column(
            'date',
            type_=sa.DateTime(),
            postgresql_using="date::timestamp without time zone"
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('episode', schema=None) as batch_op:
        batch_op.alter_column('date',
                              existing_type=sa.DateTime(),
                              type_=sa.VARCHAR(),
                              existing_nullable=True)

    # ### end Alembic commands ###
