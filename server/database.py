import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session, declarative_base, sessionmaker


load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "shuihua")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


def init_db() -> None:
    """确保数据库存在。"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as exc:
        if "1049" in str(exc) or "Unknown database" in str(exc):
            root_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?charset=utf8mb4"
            root_engine = create_engine(root_url)
            with root_engine.connect() as conn:
                conn.execute(
                    text(
                        f"CREATE DATABASE IF NOT EXISTS {DB_NAME} "
                        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                    )
                )
            engine.dispose()
        else:
            raise exc


def ensure_schema_updates() -> None:
    """为已有数据库补齐会议域所需字段与索引。"""
    with engine.begin() as conn:
        def has_table(table_name: str) -> bool:
            return inspect(conn).has_table(table_name)

        def column_names(table_name: str) -> set:
            return {column["name"] for column in inspect(conn).get_columns(table_name)}

        def index_names(table_name: str) -> set:
            inspector = inspect(conn)
            names = {item["name"] for item in inspector.get_indexes(table_name)}
            names.update({item["name"] for item in inspector.get_unique_constraints(table_name) if item.get("name")})
            return names

        if has_table("sys_user"):
            cols = column_names("sys_user")
            idxs = index_names("sys_user")
            if "wecom_userid" not in cols:
                conn.execute(
                    text(
                        "ALTER TABLE sys_user "
                        "ADD COLUMN wecom_userid VARCHAR(64) NULL COMMENT '企微用户ID'"
                    )
                )
            if "uk_sys_user_wecom_userid" not in idxs:
                conn.execute(
                    text(
                        "CREATE UNIQUE INDEX uk_sys_user_wecom_userid "
                        "ON sys_user (wecom_userid)"
                    )
                )

        if has_table("shjl_meetings"):
            cols = column_names("shjl_meetings")
            idxs = index_names("shjl_meetings")
            meeting_columns = {
                "organizer_user_id": "ALTER TABLE shjl_meetings ADD COLUMN organizer_user_id BIGINT NULL",
                "organizer_id": "ALTER TABLE shjl_meetings ADD COLUMN organizer_id VARCHAR(36) NULL",
                "status": "ALTER TABLE shjl_meetings ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'scheduled'",
                "channel": "ALTER TABLE shjl_meetings ADD COLUMN channel VARCHAR(20) NOT NULL DEFAULT 'web'",
                "source_type": "ALTER TABLE shjl_meetings ADD COLUMN source_type VARCHAR(30) NOT NULL DEFAULT 'manual'",
                "room_id": "ALTER TABLE shjl_meetings ADD COLUMN room_id CHAR(36) NULL",
                "participants_json": "ALTER TABLE shjl_meetings ADD COLUMN participants_json JSON NULL",
                "meeting_url": "ALTER TABLE shjl_meetings ADD COLUMN meeting_url VARCHAR(500) NULL",
                "wecom_schedule_id": "ALTER TABLE shjl_meetings ADD COLUMN wecom_schedule_id VARCHAR(100) NULL",
                "audio_file_key": "ALTER TABLE shjl_meetings ADD COLUMN audio_file_key VARCHAR(255) NULL",
                "sync_status": "ALTER TABLE shjl_meetings ADD COLUMN sync_status VARCHAR(20) NOT NULL DEFAULT 'none'",
            }
            for name, ddl in meeting_columns.items():
                if name not in cols:
                    conn.execute(text(ddl))

            meeting_indexes = {
                "idx_meeting_start_time": "CREATE INDEX idx_meeting_start_time ON shjl_meetings (start_time)",
                "idx_meeting_room": "CREATE INDEX idx_meeting_room ON shjl_meetings (room_id)",
                "idx_meeting_organizer": "CREATE INDEX idx_meeting_organizer ON shjl_meetings (organizer_user_id)",
                "idx_meeting_status": "CREATE INDEX idx_meeting_status ON shjl_meetings (status)",
            }
            for name, ddl in meeting_indexes.items():
                if name not in idxs:
                    conn.execute(text(ddl))

        if has_table("shjl_meeting_rooms"):
            cols = column_names("shjl_meeting_rooms")
            idxs = index_names("shjl_meeting_rooms")
            room_columns = {
                "room_name": "ALTER TABLE shjl_meeting_rooms ADD COLUMN room_name VARCHAR(120) NOT NULL DEFAULT ''",
                "site_name": "ALTER TABLE shjl_meeting_rooms ADD COLUMN site_name VARCHAR(100) NOT NULL DEFAULT ''",
                "location_text": "ALTER TABLE shjl_meeting_rooms ADD COLUMN location_text VARCHAR(200) NOT NULL DEFAULT ''",
                "building_name": "ALTER TABLE shjl_meeting_rooms ADD COLUMN building_name VARCHAR(100) NULL",
                "floor_label": "ALTER TABLE shjl_meeting_rooms ADD COLUMN floor_label VARCHAR(50) NULL",
                "capacity": "ALTER TABLE shjl_meeting_rooms ADD COLUMN capacity INT NOT NULL DEFAULT 0",
                "seat_layout": "ALTER TABLE shjl_meeting_rooms ADD COLUMN seat_layout VARCHAR(50) NULL",
                "manager_name": "ALTER TABLE shjl_meeting_rooms ADD COLUMN manager_name VARCHAR(50) NULL",
                "manager_user_id": "ALTER TABLE shjl_meeting_rooms ADD COLUMN manager_user_id BIGINT NULL",
                "sort_order": "ALTER TABLE shjl_meeting_rooms ADD COLUMN sort_order INT NULL",
                "is_enabled": "ALTER TABLE shjl_meeting_rooms ADD COLUMN is_enabled TINYINT(1) NOT NULL DEFAULT 1",
                "source_file": "ALTER TABLE shjl_meeting_rooms ADD COLUMN source_file VARCHAR(100) NULL",
                "source_sheet": "ALTER TABLE shjl_meeting_rooms ADD COLUMN source_sheet VARCHAR(50) NULL",
            }
            for name, ddl in room_columns.items():
                if name not in cols:
                    conn.execute(text(ddl))

            room_indexes = {
                "uk_room_site_name": "CREATE UNIQUE INDEX uk_room_site_name ON shjl_meeting_rooms (site_name, room_name)",
                "idx_room_enabled": "CREATE INDEX idx_room_enabled ON shjl_meeting_rooms (is_enabled)",
                "idx_room_site": "CREATE INDEX idx_room_site ON shjl_meeting_rooms (site_name)",
                "idx_room_capacity": "CREATE INDEX idx_room_capacity ON shjl_meeting_rooms (capacity)",
                "idx_room_manager_user": "CREATE INDEX idx_room_manager_user ON shjl_meeting_rooms (manager_user_id)",
            }
            for name, ddl in room_indexes.items():
                if name not in idxs:
                    conn.execute(text(ddl))


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
