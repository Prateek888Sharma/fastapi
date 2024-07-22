"""create posts table

Revision ID: 0b928cdf72c1
Revises: 
Create Date: 2024-07-20 21:46:46.016483

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b928cdf72c1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id",sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column("title",sa.String(),nullable=False),
                    sa.Column("content",sa.String(),nullable=False),
                    sa.Column("published",sa.Boolean(),server_default='true'))
         
  
def downgrade() -> None:

    op.drop_table("posts")