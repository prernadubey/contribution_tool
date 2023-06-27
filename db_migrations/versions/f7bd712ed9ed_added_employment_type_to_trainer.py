"""added employment_type to trainer

Revision ID: f7bd712ed9ed
Revises: 423d879dbefa
Create Date: 2023-06-03 14:49:34.207855

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
from sqlalchemy import MetaData, Table

revision = "f7bd712ed9ed"
down_revision = "423d879dbefa"
branch_labels = None
depends_on = None


TRAINERS_USER_DATA = [
    {
        "id": 1000000000000000004,
        "name": "trainer_1",
        "surname": "trainer_1",
        "email": "trainer_1_r1@example.com",
        "role": "user",
    },
    {
        "id": 1000000000000000005,
        "name": "trainer_2",
        "surname": "trainer_2",
        "email": "trainer_2_r5@example.com",
        "role": "user",
    },
    {
        "id": 1000000000000000006,
        "name": "trainer_3",
        "surname": "trainer_3",
        "email": "trainer_3_r3@example.com",
        "role": "user",
    },
]

TRAINERS_DATA = [
    {
        "user_id": 1000000000000000004,
        "trainer_level": "R1",
        "employment_type": "internal",
    },
    {
        "user_id": 1000000000000000005,
        "trainer_level": "R5",
        "employment_type": "external",
    },
    {
        "user_id": 1000000000000000006,
        "trainer_level": "R3",
        "employment_type": "subcontractor",
    },
]


def upgrade() -> None:
    trainers_table = op.create_table(
        "trainers",
        sa.Column("user_id", sa.BigInteger(), nullable=True),
        sa.Column("trainer_level", sa.String(), nullable=False),
        sa.Column(
            "employment_type",
            sa.Enum(
                "internal", "external", "subcontractor", name="traineremploymenttype"
            ),
            nullable=True,
        ),
        sa.CheckConstraint("trainer_level IN ('R1', 'R2', 'R3', 'R4', 'R5')"),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "trainer_level"),
    )
    op.drop_table("trainer_levels")

    meta = MetaData()
    meta.reflect(bind=op.get_bind(), only=("users",))
    users_table = Table("users", meta)

    op.bulk_insert(users_table, TRAINERS_USER_DATA)
    op.bulk_insert(trainers_table, TRAINERS_DATA)


def downgrade() -> None:
    op.create_table(
        "trainer_levels",
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("trainer_level", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.CheckConstraint(
            "trainer_level::text = ANY (ARRAY['R1'::character varying, 'R2'::character varying, 'R3'::character varying, 'R4'::character varying, 'R5'::character varying]::text[])",
            name="trainer_levels_trainer_level_check",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="trainer_levels_user_id_fkey"
        ),
        sa.PrimaryKeyConstraint("user_id", "trainer_level", name="trainer_levels_pkey"),
    )
    op.drop_table("trainers")

    op.execute(
        "DELETE FROM users WHERE id in (1000000000000000004, 1000000000000000005, 1000000000000000006);"
    )
    op.execute(
        "DELETE FROM trainers WHERE user_id in (1000000000000000004, 1000000000000000005, 1000000000000000006);"
    )
