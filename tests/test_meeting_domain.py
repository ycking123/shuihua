import os
import sys
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from server.database import Base
from server.models import MeetingRoom
from server.services.meeting_service import MeetingService, MeetingServiceError
from server.services.session_state_manager import SessionStateManager


class MeetingServiceDbTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        TestingSessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = TestingSessionLocal()
        self.service = MeetingService()
        self.service.ensure_room_seeded_from_xlsx = lambda db: 0
        self.room = MeetingRoom(
            id="room-1",
            room_name="研发A会议室",
            site_name="总部",
            location_text="研发楼16F会议室A",
            building_name="研发楼",
            floor_label="16F",
            capacity=12,
            is_enabled=True,
        )
        self.db.add(self.room)
        self.db.commit()

    def tearDown(self):
        self.db.close()
        Base.metadata.drop_all(bind=self.engine)
        self.engine.dispose()

    def test_create_update_cancel_meeting_flow(self):
        created = self.service.create_meeting(
            self.db,
            {
                "title": "项目例会",
                "start_time": "2026-03-20 10:00",
                "duration": "60分钟",
                "room_id": self.room.id,
                "participants": "张三, 李四",
                "description": "同步排期"
            },
            current_user_id="1001",
        )
        self.assertEqual(created["title"], "项目例会")
        self.assertEqual(created["room_id"], self.room.id)
        self.assertEqual(created["participants"], ["张三", "李四"])

        updated = self.service.update_meeting(
            self.db,
            created["id"],
            {"start_time": "2026-03-20 11:00", "duration": "90分钟", "summary": "已同步事项"},
            current_user_id="1001",
        )
        self.assertEqual(updated["summary"], "已同步事项")
        self.assertIn("11:00", str(updated["start_time"]))

        cancelled = self.service.cancel_meeting(self.db, created["id"])
        self.assertEqual(cancelled["status"], "cancelled")

    def test_generate_summary_from_transcript(self):
        created = self.service.create_meeting(
            self.db,
            {
                "title": "纪要会",
                "start_time": "2026-03-21 09:00",
                "duration": "30分钟",
                "location": "线上会议",
                "transcript": "第一项讨论排期。第二项明确负责人。第三项确定下周复盘。"
            },
        )
        summary = self.service.generate_summary(self.db, created["id"])
        self.assertIn("会议要点", summary["summary"])

    def test_room_conflict_raises_error(self):
        self.service.create_meeting(
            self.db,
            {
                "title": "先占用",
                "start_time": "2026-03-22 14:00",
                "duration": "60分钟",
                "room_id": self.room.id,
            },
        )
        with self.assertRaises(MeetingServiceError):
            self.service.create_meeting(
                self.db,
                {
                    "title": "冲突会议",
                    "start_time": "2026-03-22 14:30",
                    "duration": "30分钟",
                    "room_id": self.room.id,
                },
            )


class TestMeetingServiceHelpers(unittest.TestCase):
    def setUp(self):
        self.service = MeetingService()

    def test_parse_datetime_value_supports_relative_cn_text(self):
        result = self.service.parse_datetime_value("明天下午3点开会")
        self.assertIsNotNone(result)
        self.assertEqual(result.hour, 15)

    def test_parse_datetime_value_supports_cn_date(self):
        result = self.service.parse_datetime_value("2026年3月20日下午2点")
        self.assertIsNotNone(result)
        self.assertEqual(result.year, 2026)
        self.assertEqual(result.month, 3)
        self.assertEqual(result.day, 20)
        self.assertEqual(result.hour, 14)

    def test_extract_location_parts(self):
        building_name, floor_label = self.service.extract_location_parts("研发楼16F会议室A")
        self.assertEqual(building_name, "研发楼")
        self.assertEqual(floor_label, "16F会议室A")

    def test_normalize_people(self):
        result = self.service.normalize_people("张三, 李四 王五")
        self.assertEqual(result, ["张三", "李四", "王五"])

    def test_build_summary(self):
        summary = self.service.build_summary("第一项讨论排期。第二项明确负责人。第三项确定下周复盘。")
        self.assertTrue(summary.startswith("会议要点"))
        self.assertIn("讨论排期", summary)


class TestSessionStateManager(unittest.TestCase):
    def setUp(self):
        self.manager = SessionStateManager()

    def test_meeting_create_required_params(self):
        session = self.manager.create_session("1001", "meeting_create")
        self.assertEqual(session.missing_params, ["title", "start_time", "location"])

    def test_merge_params_updates_status(self):
        session = self.manager.create_session("1001", "room_book")
        self.manager.merge_params(session.session_id, {"title": "预算会", "start_time": "明天上午10点"})
        state = self.manager.merge_params(session.session_id, {"room_name": "16F会议室A"})
        self.assertEqual(state.status, "ready")
        self.assertEqual(state.missing_params, [])


if __name__ == "__main__":
    unittest.main()
