"""added example locations and projects

Revision ID: e08d91f9e081
Revises: c2bdf99dcb8b
Create Date: 2023-05-31 17:09:16.387802

"""
from alembic import op
from sqlalchemy import MetaData, Table

revision = "e08d91f9e081"
down_revision = "c2bdf99dcb8b"
branch_labels = None
depends_on = None

LOCATIONS = ["Colombia", "Poland", "GUKKA"]
PROJECTS = [{"name": "EPM-XYZ", "type_id": 1}, {"name": "EPM-ZYX", "type_id": 2}]
LOCATIONS_PROJECTS = [
    {"location_id": 1, "project_id": 1},
    {"location_id": 2, "project_id": 1},
    {"location_id": 1, "project_id": 2},
]


def upgrade() -> None:
    # get metadata from current connection
    meta = MetaData()

    # pass in tuple with tables we want to reflect, otherwise whole database will get reflected
    meta.reflect(
        bind=op.get_bind(), only=("locations", "projects", "project_locations")
    )

    # define table representation
    locations_table = Table("locations", meta)
    projects_table = Table("projects", meta)
    project_locations_table = Table("project_locations", meta)

    location_data = [{"name": location} for location in LOCATIONS]
    op.bulk_insert(locations_table, location_data)

    project_data = [project for project in PROJECTS]
    op.bulk_insert(projects_table, project_data)

    project_location_data = [
        project_location for project_location in LOCATIONS_PROJECTS
    ]
    op.bulk_insert(project_locations_table, project_location_data)


def downgrade() -> None:
    pass
