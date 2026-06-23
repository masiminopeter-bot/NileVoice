"""
Alembic migration script.
"""

from alembic import op
import sqlalchemy as sa


revision = "${up_revision or ""}"
down_revision = "${down_revision or ""}"
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
