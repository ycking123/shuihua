# 水花精灵会议域实现说明

## 已落地内容

- Web 新增统一会议页 `MeetingView`
- 前端新增会议导航入口 `ViewType.MEETING`
- 后端新增统一会议服务 `server/services/meeting_service.py`
- 聊天会议意图统一走 `意图识别 -> 参数抽取 -> SessionState -> MeetingService`
- 会议接口已收敛到：
  - `GET /api/meetings`
  - `POST /api/meetings`
  - `PATCH /api/meetings`
  - `PATCH /api/meetings/{meeting_id}`
  - `GET /api/meetings/{meeting_id}`
  - `GET /api/meetings/{meeting_id}/todos`
  - `POST /api/meetings/import-link`
  - `POST /api/meetings/transcribe`
  - `POST /api/meetings/{meeting_id}/summary`
  - `GET /api/meeting-rooms`
  - `POST /api/meeting-rooms`
  - `PATCH /api/meeting-rooms/{room_id}`
  - `DELETE /api/meeting-rooms/{room_id}`
  - `GET /api/meeting-rooms/usage`

## 数据模型

### `sys_user`

- 新增 `wecom_userid varchar(64) null`
- 新增唯一索引 `uk_sys_user_wecom_userid`

### `shjl_meeting_rooms`

- 主键：`id char(36)`
- 唯一键：`uk_room_site_name(site_name, room_name)`
- 关键字段：
  - `room_name`
  - `site_name`
  - `location_text`
  - `building_name`
  - `floor_label`
  - `capacity`
  - `seat_layout`
  - `manager_name`
  - `manager_user_id`
  - `sort_order`
  - `is_enabled`
  - `source_file`
  - `source_sheet`

### `shjl_meetings`

- 主键：`id char(36)`
- 关键字段：
  - `title`
  - `description`
  - `organizer_user_id`
  - `organizer_id`
  - `status`
  - `channel`
  - `source_type`
  - `start_time`
  - `end_time`
  - `room_id`
  - `location`
  - `participants_json`
  - `meeting_url`
  - `wecom_schedule_id`
  - `audio_file_key`
  - `summary`
  - `transcript`
  - `sync_status`

## Excel 导入规则

- 数据源目录：`xlsx/`
- 优先级：
  1. `会议室列表(4).xlsx`
  2. `帝王会议室列表.xlsx`
  3. `会议室列表.xlsx`
- 去重键：`site_name + room_name`
- 规则：
  - 高优先级文件优先
  - 低优先级文件只补空值
  - `是否有效 / 未来是否开放使用` 统一映射为 `is_enabled`
  - `会议室分类` 统一映射为园区归属 `site_name`

## 前端说明

- `MeetingView` 已接真实接口：
  - 会议总览
  - 预约会议
  - 会议室与占用
  - 听记纪要列表与详情
  - 会议链接导入
  - 转写文本保存
- `TodoView` 已兼容 `meeting_url`
- `ChatView` 继续复用统一会议执行链路

## 启动时结构补齐

- `server/main.py` 启动时会执行：
  - `init_db()`
  - `Base.metadata.create_all(...)`
  - `ensure_schema_updates()`

`ensure_schema_updates()` 只负责补列和补索引，不包含删表、清表、危险写操作。

## 待后续接入

- 企业微信自建应用渠道适配
- 真正的 ASR 上传与音频对象存储
- 企业微信日程同步
- 企微 / openclaw sender 到 `sys_user.wecom_userid` 的统一身份映射
