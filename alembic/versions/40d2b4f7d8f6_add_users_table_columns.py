"""add users table columns

Revision ID: 40d2b4f7d8f6
Revises: df3e492e97f0
Create Date: 2024-07-21 08:51:19.673505

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40d2b4f7d8f6'
down_revision: Union[str, None] = 'df3e492e97f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users",
                  sa.Column("email",sa.String(), nullable = False, unique = True)

                  )
    op.add_column("users",
                  sa.Column("password",sa.String(), nullable = False)

                  )

    op.add_column("users",
                  sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()'))

                  )
    
def downgrade() -> None:
    op.drop_column("users","email")
    op.drop_column("users","password")
    op.drop_column("users","created_at")

