ALTER TABLE sys_user
ADD COLUMN IF NOT EXISTS wecom_userid VARCHAR(64) NULL COMMENT '企微用户ID';

CREATE UNIQUE INDEX uk_sys_user_wecom_userid ON sys_user (wecom_userid);

CREATE TABLE IF NOT EXISTS shjl_meeting_rooms (
  id CHAR(36) NOT NULL PRIMARY KEY,
  room_name VARCHAR(120) NOT NULL,
  site_name VARCHAR(100) NOT NULL,
  location_text VARCHAR(200) NOT NULL,
  building_name VARCHAR(100) NULL,
  floor_label VARCHAR(50) NULL,
  capacity INT NOT NULL DEFAULT 0,
  seat_layout VARCHAR(50) NULL,
  manager_name VARCHAR(50) NULL,
  manager_user_id BIGINT NULL,
  sort_order INT NULL,
  is_enabled TINYINT(1) NOT NULL DEFAULT 1,
  source_file VARCHAR(100) NULL,
  source_sheet VARCHAR(50) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uk_room_site_name (site_name, room_name),
  KEY idx_room_enabled (is_enabled),
  KEY idx_room_site (site_name),
  KEY idx_room_capacity (capacity),
  KEY idx_room_manager_user (manager_user_id)
);

CREATE TABLE IF NOT EXISTS shjl_meetings (
  id CHAR(36) NOT NULL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT NULL,
  organizer_user_id BIGINT NULL,
  organizer_id VARCHAR(36) NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'scheduled',
  channel VARCHAR(20) NOT NULL DEFAULT 'web',
  source_type VARCHAR(30) NOT NULL DEFAULT 'manual',
  start_time DATETIME NOT NULL,
  end_time DATETIME NOT NULL,
  room_id CHAR(36) NULL,
  location VARCHAR(255) NULL,
  participants_json JSON NULL,
  meeting_url VARCHAR(500) NULL,
  wecom_schedule_id VARCHAR(100) NULL,
  audio_file_key VARCHAR(255) NULL,
  summary TEXT NULL,
  transcript LONGTEXT NULL,
  sync_status VARCHAR(20) NOT NULL DEFAULT 'none',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY idx_meeting_start_time (start_time),
  KEY idx_meeting_room (room_id),
  KEY idx_meeting_organizer (organizer_user_id),
  KEY idx_meeting_status (status)
);
