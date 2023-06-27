"""added test users

Revision ID: 423d879dbefa
Revises: e08d91f9e081
Create Date: 2023-06-01 15:09:52.039251

"""
from alembic import op
from sqlalchemy import MetaData, Table

# revision identifiers, used by Alembic.
revision = "423d879dbefa"
down_revision = "e08d91f9e081"
branch_labels = None
depends_on = None

USERS_DATA = [
    {
        "id": 1000000000000000001,
        "name": "admin",
        "surname": "admin",
        "email": "admin_admin@example.com",
        "role": "admin",
    },
    {
        "id": 1000000000000000002,
        "name": "user",
        "surname": "user",
        "email": "user_user@example.com",
        "role": "user",
    },
    {
        "id": 1000000000000000003,
        "name": "approver",
        "surname": "approver",
        "email": "approver_approver@example.com",
        "role": "approver",
    },
]


def upgrade() -> None:
    # get metadata from current connection
    meta = MetaData()

    # pass in tuple with tables we want to reflect, otherwise whole database will get reflected
    meta.reflect(bind=op.get_bind(), only=("users",))

    # define table representation
    users_table = Table("users", meta)

    op.bulk_insert(users_table, USERS_DATA)


def downgrade() -> None:
    op.execute(
        "DELETE FROM users WHERE id in (1000000000000000001, 1000000000000000002, 1000000000000000003);"
    )
