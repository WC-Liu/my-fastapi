"""password_hashd->password_hashed

Revision ID: 820dc630c68a
Revises: e3693a4e0499
Create Date: 2026-05-15 14:06:42.239368

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "820dc630c68a"
down_revision: Union[str, Sequence[str], None] = "e3693a4e0499"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column("users", "password_hashd", new_column_name="password_hashed")


def downgrade():
    op.alter_column("users", "password_hashed", new_column_name="password_hashd")
