"""basic structure

Revision ID: c2bdf99dcb8b
Revises: 128411c0b2c8
Create Date: 2023-05-18 13:13:04.073137

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
from sqlalchemy.dialects import postgresql

revision = "c2bdf99dcb8b"
down_revision = "128411c0b2c8"
branch_labels = None
depends_on = None

SKILLS = [
    "Java",
    ".NET",
    "Performance Testing",
    "Android",
    "BA",
    "Data (DI/BI/DQE)",
    "UX design",
    "Automated Testing",
    "Frontend/JavaScript",
    "C++",
    "Functional Testing",
    "Data Science",
    "Python",
    "DevOps/Cloud",
    "iOS",
    "SAP",
    "RPA",
    "SalesForce",
    "PHP",
    "Ruby",
    "Security Testing",
    "Scala",
    "ServiceNow",
    "Data & Analytics",
    "Other",
]

ACTIVITY_TYPES = [
    "chair affiliate",
    "materials",
    "coordination",
    "event",
    "consultation",
    "project education contribution",
    "group Q&A session",
    "lecture (webinar)",
    "workshop (practice)",
    "assessment stage (TI)",
    "task for review/code review",
    "individual Q&A session",
]

PROJECT_TYPES = [
    "Location project",
    "Global",
]


def upgrade() -> None:
    activity_types_table = op.create_table(
        "activity_types",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_activity_types_id"), "activity_types", ["id"], unique=False
    )
    op.create_table(
        "locations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_locations_id"), "locations", ["id"], unique=False)
    project_types_table = op.create_table(
        "project_types",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_project_types_id"), "project_types", ["id"], unique=False)
    skills_table = op.create_table(
        "skills",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_skills_id"), "skills", ["id"], unique=False)
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("surname", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column(
            "role", sa.Enum("user", "approver", "admin", name="userrole"), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["type_id"],
            ["project_types.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_projects_id"), "projects", ["id"], unique=False)
    op.create_table(
        "trainer_levels",
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("trainer_level", sa.String(), nullable=False),
        sa.CheckConstraint("trainer_level IN ('R1', 'R2', 'R3', 'R4', 'R5')"),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "trainer_level"),
    )
    op.create_table(
        "compensation_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "draft",
                "pending",
                "confirmed",
                "denied",
                name="compensationrequeststatuses",
            ),
            nullable=True,
        ),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("created_by_id", sa.BigInteger(), nullable=True),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.Column("trainer_id", sa.BigInteger(), nullable=True),
        sa.Column(
            "training_type",
            sa.Enum(
                "internal_training", "external_training", "other", name="trainingtypes"
            ),
            nullable=True,
        ),
        sa.Column("course_id", sa.String(), nullable=False),
        sa.Column("activity_date", sa.Date(), nullable=False),
        sa.Column("activity_type_id", sa.Integer(), nullable=True),
        sa.Column(
            "trainer_employment_type",
            sa.Enum(
                "internal", "external", "subcontractor", name="traineremploymenttype"
            ),
            nullable=True,
        ),
        sa.Column("is_rewarded", sa.Boolean(), nullable=False),
        sa.Column("request_initiator_id", sa.BigInteger(), nullable=True),
        sa.Column("rd_point", sa.Float(), nullable=False),
        sa.Column("skill_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["activity_type_id"],
            ["activity_types.id"],
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
        ),
        sa.ForeignKeyConstraint(
            ["request_initiator_id"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["skill_id"],
            ["skills.id"],
        ),
        sa.ForeignKeyConstraint(
            ["trainer_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_compensation_requests_id"),
        "compensation_requests",
        ["id"],
        unique=False,
    )
    op.create_table(
        "project_locations",
        sa.Column("location_id", sa.Integer(), nullable=True),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["location_id"],
            ["locations.id"],
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
        ),
    )

    skill_data = [{"name": skill} for skill in SKILLS]
    op.bulk_insert(skills_table, skill_data)

    activity_type_data = [{"name": activity_type} for activity_type in ACTIVITY_TYPES]
    op.bulk_insert(activity_types_table, activity_type_data)

    project_type_data = [{"name": project_type} for project_type in PROJECT_TYPES]
    op.bulk_insert(project_types_table, project_type_data)


def downgrade() -> None:
    op.drop_table("project_locations")
    op.drop_index(
        op.f("ix_compensation_requests_id"), table_name="compensation_requests"
    )
    op.drop_table("compensation_requests")
    op.drop_table("trainer_levels")
    op.drop_index(op.f("ix_projects_id"), table_name="projects")
    op.drop_table("projects")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_skills_id"), table_name="skills")
    op.drop_table("skills")
    op.drop_index(op.f("ix_project_types_id"), table_name="project_types")
    op.drop_table("project_types")
    op.drop_index(op.f("ix_locations_id"), table_name="locations")
    op.drop_table("locations")
    op.drop_index(op.f("ix_activity_types_id"), table_name="activity_types")
    op.drop_table("activity_types")
