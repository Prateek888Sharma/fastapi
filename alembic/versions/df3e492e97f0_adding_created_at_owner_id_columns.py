"""adding created_at, owner_id columns

Revision ID: df3e492e97f0
Revises: 0b928cdf72c1
Create Date: 2024-07-20 22:17:49.513543

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df3e492e97f0'
down_revision: Union[str, None] = '0b928cdf72c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id",sa.Integer(),primary_key=True, nullable=False)                    
                    )
    op.add_column("posts",sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("now()")))
    op.add_column("posts",sa.Column("owner_id",sa.Integer(),sa.ForeignKey("users.id",ondelete="CASCADE"),nullable=False))
    
def downgrade() -> None:
    op.drop_column("posts","created_at")
    op.drop_column("posts","owner_id")
    op.drop_table("users")


