"""add_creationDate_column

Revision ID: 61b4509b19fe
Revises: 
Create Date: 2023-09-07 09:43:53.165393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61b4509b19fe'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('songs', sa.Column('creationDate', sa.Date(), nullable=True))


def downgrade():
    # Define how to downgrade the migration if needed
    op.drop_column('songs', 'creationDate')

