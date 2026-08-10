"""add prompt version to insights

Revision ID: 0001_add_prompt_version
Revises:
Create Date: 2026-08-10
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0001_add_prompt_version"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Add prompt version tracking to generated insights."""

    op.execute(
        """
        ALTER TABLE insights
        ADD COLUMN IF NOT EXISTS
        prompt_version VARCHAR(100)
        NOT NULL
        DEFAULT 'insight_generation:v1'
        """
    )

def downgrade() -> None:
    """Remove prompt version tracking from generated insights."""

    op.execute(
        """
        ALTER TABLE insights
        DROP COLUMN IF EXISTS prompt_version
        """
    )