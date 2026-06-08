"""Change image_url to images array

Revision ID: 2026_06_08_001
Revises: 472135f8ff9d
Create Date: 2026-06-08 19:14:44.131057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2026_06_08_001'
down_revision: Union[str, Sequence[str], None] = '472135f8ff9d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop old image_url column
    op.drop_column('products', 'image_url')

    # Add new images column as ARRAY of strings
    op.add_column('products', sa.Column('images', sa.ARRAY(sa.String()), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Drop new images column
    op.drop_column('products', 'images')

    # Restore old image_url column
    op.add_column('products', sa.Column('image_url', sa.String(length=500), nullable=True))
