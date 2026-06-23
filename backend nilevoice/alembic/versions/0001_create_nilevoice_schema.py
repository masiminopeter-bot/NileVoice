"""Create initial NileVoice database schema

Revision ID: 0001_create_nilevoice_schema
Revises: 
Create Date: 2026-06-23 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_create_nilevoice_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("username", sa.String(length=80), nullable=False, unique=True),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("email_verified", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("verification_token", sa.String(length=128), nullable=True, unique=True),
        sa.Column("verification_sent_at", sa.DateTime(timezone=False), nullable=True),
        sa.Column("reset_password_token", sa.String(length=128), nullable=True, unique=True),
        sa.Column("reset_password_sent_at", sa.DateTime(timezone=False), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("is_superuser", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("last_login_at", sa.DateTime(timezone=False), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=False), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=False), nullable=False, server_default=sa.func.now()),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
    )
    op.create_index("ix_users_email", "users", ["email"], unique=False)
    op.create_index("ix_users_username", "users", ["username"], unique=False)

    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=80), nullable=False, unique=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("created_at", sa.DateTime(timezone=False), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=False), nullable=False, server_default=sa.func.now()),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
    )
    op.create_index("ix_roles_name", "roles", ["name"], unique=False)

    op.create_table(
        "languages",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("code", sa.String(length=16), nullable=False, unique=True),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("native_name", sa.String(length=128), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=False), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=False), nullable=False, server_default=sa.func.now()),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
    )
    op.create_index("ix_languages_code", "languages", ["code"], unique=False)

    op.create_table(
        "user_roles",
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True, nullable=False),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
    )

    op.create_table(
        "translation_submissions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_language_id", sa.Integer(), sa.ForeignKey("languages.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("target_language_id", sa.Integer(), sa.ForeignKey("languages.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("submission_type", sa.Enum("word", "phrase", "sentence", name="submission_type"), nullable=False, server_default="word"),
        sa.Column("original_text", sa.Text(), nullable=False),
        sa.Column("translated_text", sa.Text(), nullable=True),
        sa.Column("status", sa.Enum("pending", "approved", "rejected", name="submission_status"), nullable=False, server_default="pending"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=False), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=False), nullable=False, server_default=sa.func.now()),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
    )
    op.create_index("ix_translation_submissions_user_id", "translation_submissions", ["user_id"], unique=False)
    op.create_index("ix_translation_submissions_source_language_id", "translation_submissions", ["source_language_id"], unique=False)
    op.create_index("ix_translation_submissions_target_language_id", "translation_submissions", ["target_language_id"], unique=False)
    op.create_index("ix_translation_submissions_status", "translation_submissions", ["status"], unique=False)

    op.create_table(
        "dictionary_entries",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("language_id", sa.Integer(), sa.ForeignKey("languages.id", ondelete="CASCADE"), nullable=False),
        sa.Column("entry_type", sa.Enum("word", "phrase", "sentence", name="dictionary_entry_type"), nullable=False, server_default="word"),
        sa.Column("term", sa.String(length=255), nullable=False),
        sa.Column("translation", sa.String(length=255), nullable=False),
        sa.Column("part_of_speech", sa.String(length=50), nullable=True),
        sa.Column("example", sa.Text(), nullable=True),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_by_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=False), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=False), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("language_id", "term", "translation", name="uq_dictionary_entry_term_translation"),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
    )
    op.create_index("ix_dictionary_entries_language_id", "dictionary_entries", ["language_id"], unique=False)
    op.create_index("ix_dictionary_entries_entry_type", "dictionary_entries", ["entry_type"], unique=False)
    op.create_index("ix_dictionary_entries_term", "dictionary_entries", ["term"], unique=False)
    op.create_index("ix_dictionary_entries_translation", "dictionary_entries", ["translation"], unique=False)
    op.create_index("ix_dictionary_entries_created_by_id", "dictionary_entries", ["created_by_id"], unique=False)

    op.create_table(
        "contacts",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("subject", sa.String(length=255), nullable=True),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("is_resolved", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=False), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=False), nullable=False, server_default=sa.func.now()),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
    )
    op.create_index("ix_contacts_user_id", "contacts", ["user_id"], unique=False)

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("action", sa.Enum("create", "update", "delete", "login", "logout", "token_refresh", name="audit_action_type"), nullable=False),
        sa.Column("resource_type", sa.String(length=128), nullable=True),
        sa.Column("resource_id", sa.String(length=128), nullable=True),
        sa.Column("changes", sa.Text(), nullable=True),
        sa.Column("ip_address", sa.String(length=45), nullable=True),
        sa.Column("user_agent", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=False), nullable=False, server_default=sa.func.now()),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
    )
    op.create_index("ix_audit_logs_user_id", "audit_logs", ["user_id"], unique=False)
    op.create_index("ix_audit_logs_action", "audit_logs", ["action"], unique=False)

    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("token", sa.String(length=255), nullable=False, unique=True),
        sa.Column("issued_at", sa.DateTime(timezone=False), nullable=False, server_default=sa.func.now()),
        sa.Column("expires_at", sa.DateTime(timezone=False), nullable=False),
        sa.Column("revoked", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=False), nullable=False, server_default=sa.func.now()),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
    )
    op.create_index("ix_refresh_tokens_user_id", "refresh_tokens", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_table("refresh_tokens")
    op.drop_table("audit_logs")
    op.drop_table("contacts")
    op.drop_table("dictionary_entries")
    op.drop_table("translation_submissions")
    op.drop_table("user_roles")
    op.drop_table("languages")
    op.drop_table("roles")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS submission_status")
    op.execute("DROP TYPE IF EXISTS audit_action_type")
