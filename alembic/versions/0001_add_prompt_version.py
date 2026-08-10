"""initial database schema

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
    """Create the complete application database schema."""

    # Brands

    op.create_table(
        "brands",
        sa.Column(
            "id",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "category",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "configuration",
            sa.JSON(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_brands_name",
        "brands",
        ["name"],
        unique=False,
    )

    op.create_index(
        "ix_brands_category",
        "brands",
        ["category"],
        unique=False,
    )

    # Sources
    
    op.create_table(
        "sources",
        sa.Column(
            "id",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "source_type",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "url",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "title",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "published_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "content_hash",
            sa.String(length=128),
            nullable=False,
        ),
        sa.Column(
            "ingested_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_sources_source_type",
        "sources",
        ["source_type"],
        unique=False,
    )

    op.create_index(
        "ix_sources_content_hash",
        "sources",
        ["content_hash"],
        unique=False,
    )

    # Signals

    op.create_table(
        "signals",
        sa.Column(
            "id",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "source_id",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "signal_type",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "category",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "title",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "text",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "metadata_json",
            sa.JSON(),
            nullable=False,
        ),
        sa.Column(
            "confidence",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["source_id"],
            ["sources.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_signals_source_id",
        "signals",
        ["source_id"],
        unique=False,
    )

    op.create_index(
        "ix_signals_signal_type",
        "signals",
        ["signal_type"],
        unique=False,
    )

    op.create_index(
        "ix_signals_category",
        "signals",
        ["category"],
        unique=False,
    )

    # Insights

    op.create_table(
        "insights",
        sa.Column(
            "id",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "brand_id",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "signal_id",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "summary",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "observation",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "interpretation",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "opportunity",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "risk",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "recommendation",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "impact_score",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "relevance_score",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "confidence_score",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "priority",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "evidence",
            sa.JSON(),
            nullable=False,
        ),
        sa.Column(
            "prompt_version",
            sa.String(length=100),
            nullable=False,
            server_default=sa.text(
                "'insight_generation:v1'"
            ),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["brand_id"],
            ["brands.id"],
        ),
        sa.ForeignKeyConstraint(
            ["signal_id"],
            ["signals.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_insights_brand_id",
        "insights",
        ["brand_id"],
        unique=False,
    )

    op.create_index(
        "ix_insights_signal_id",
        "insights",
        ["signal_id"],
        unique=False,
    )

    op.create_index(
        "ix_insights_priority",
        "insights",
        ["priority"],
        unique=False,
    )

    op.create_index(
        "ix_insights_status",
        "insights",
        ["status"],
        unique=False,
    )

    # Human reviews

    op.create_table(
        "human_reviews",
        sa.Column(
            "id",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "insight_id",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "reviewer_action",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "comment",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["insight_id"],
            ["insights.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_human_reviews_insight_id",
        "human_reviews",
        ["insight_id"],
        unique=False,
    )

def downgrade() -> None:
    """Drop the complete application database schema."""

    op.drop_index(
        "ix_human_reviews_insight_id",
        table_name="human_reviews",
    )

    op.drop_table("human_reviews")

    op.drop_index(
        "ix_insights_status",
        table_name="insights",
    )

    op.drop_index(
        "ix_insights_priority",
        table_name="insights",
    )

    op.drop_index(
        "ix_insights_signal_id",
        table_name="insights",
    )

    op.drop_index(
        "ix_insights_brand_id",
        table_name="insights",
    )

    op.drop_table("insights")

    op.drop_index(
        "ix_signals_category",
        table_name="signals",
    )

    op.drop_index(
        "ix_signals_signal_type",
        table_name="signals",
    )

    op.drop_index(
        "ix_signals_source_id",
        table_name="signals",
    )

    op.drop_table("signals")

    op.drop_index(
        "ix_sources_content_hash",
        table_name="sources",
    )

    op.drop_index(
        "ix_sources_source_type",
        table_name="sources",
    )

    op.drop_table("sources")

    op.drop_index(
        "ix_brands_category",
        table_name="brands",
    )

    op.drop_index(
        "ix_brands_name",
        table_name="brands",
    )

    op.drop_table("brands")