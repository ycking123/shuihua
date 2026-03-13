from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import get_db
from ..security import verify_token
from ..services.meeting_service import MeetingServiceError, meeting_service


router = APIRouter(tags=["meetings"])


class MeetingCreateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration: Optional[str] = None
    room_id: Optional[str] = None
    room_name: Optional[str] = None
    site_name: Optional[str] = None
    location: Optional[str] = None
    participants: Optional[Any] = None
    meeting_url: Optional[str] = None
    transcript: Optional[str] = None
    summary: Optional[str] = None
    audio_file_key: Optional[str] = None
    source_type: Optional[str] = None
    channel: Optional[str] = None
    status: Optional[str] = None
    sync_status: Optional[str] = None


class MeetingUpdateRequest(MeetingCreateRequest):
    meeting_id: Optional[str] = None


class MeetingLinkImportRequest(BaseModel):
    meeting_id: Optional[str] = None
    title: Optional[str] = None
    meeting_url: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    summary: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    location: Optional[str] = None
    participants: Optional[Any] = None
    channel: Optional[str] = None


class MeetingTranscribeRequest(BaseModel):
    meeting_id: Optional[str] = None
    title: Optional[str] = None
    transcript: Optional[str] = None
    text: Optional[str] = None
    summary: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    location: Optional[str] = None
    participants: Optional[Any] = None
    description: Optional[str] = None
    audio_file_key: Optional[str] = None
    channel: Optional[str] = None
    sync_status: Optional[str] = None


class MeetingRoomCreateRequest(BaseModel):
    room_name: str
    site_name: str
    location_text: str
    building_name: Optional[str] = None
    floor_label: Optional[str] = None
    capacity: Optional[int] = 0
    seat_layout: Optional[str] = None
    manager_name: Optional[str] = None
    sort_order: Optional[int] = None
    is_enabled: Optional[bool] = True
    source_file: Optional[str] = None
    source_sheet: Optional[str] = None


class MeetingRoomUpdateRequest(MeetingRoomCreateRequest):
    room_name: Optional[str] = None
    site_name: Optional[str] = None
    location_text: Optional[str] = None


def get_current_user_id(http_request: Request) -> Optional[str]:
    auth_header = http_request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ", 1)[1]
    payload = verify_token(token)
    if payload and "user_id" in payload:
        return str(payload["user_id"])
    return None


def raise_service_error(exc: MeetingServiceError) -> None:
    detail: Dict[str, Any] = {"message": exc.message}
    if exc.code:
        detail["code"] = exc.code
    if exc.extra:
        detail["extra"] = exc.extra
    raise HTTPException(status_code=exc.status_code, detail=detail)


@router.get("/api/meetings")
def get_meetings(
    skip: int = 0,
    limit: int = 100,
    sort_by: str = Query("start_time"),
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db),
):
    try:
        return meeting_service.list_meetings(
            db=db,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            status=status,
            keyword=keyword,
        )
    except MeetingServiceError as exc:
        raise_service_error(exc)


@router.post("/api/meetings")
def create_meeting(
    payload: MeetingCreateRequest,
    http_request: Request,
    db: Session = Depends(get_db),
):
    try:
        return meeting_service.create_meeting(
            db=db,
            payload=payload.model_dump(exclude_none=True),
            current_user_id=get_current_user_id(http_request),
        )
    except MeetingServiceError as exc:
        raise_service_error(exc)


@router.patch("/api/meetings")
def patch_meeting_by_body(
    payload: MeetingUpdateRequest,
    http_request: Request,
    db: Session = Depends(get_db),
):
    meeting_id = payload.meeting_id
    if not meeting_id:
        raise HTTPException(status_code=400, detail={"message": "缺少 meeting_id"})
    try:
        return meeting_service.update_meeting(
            db=db,
            meeting_id=meeting_id,
            payload=payload.model_dump(exclude_unset=True, exclude={"meeting_id"}),
            current_user_id=get_current_user_id(http_request),
        )
    except MeetingServiceError as exc:
        raise_service_error(exc)


@router.post("/api/meetings/import-link")
def import_meeting_link(
    payload: MeetingLinkImportRequest,
    http_request: Request,
    db: Session = Depends(get_db),
):
    try:
        return meeting_service.import_link(
            db=db,
            payload=payload.model_dump(exclude_none=True),
            current_user_id=get_current_user_id(http_request),
        )
    except MeetingServiceError as exc:
        raise_service_error(exc)


@router.post("/api/meetings/transcribe")
def transcribe_meeting(
    payload: MeetingTranscribeRequest,
    http_request: Request,
    db: Session = Depends(get_db),
):
    try:
        return meeting_service.transcribe_meeting(
            db=db,
            payload=payload.model_dump(exclude_none=True),
            current_user_id=get_current_user_id(http_request),
        )
    except MeetingServiceError as exc:
        raise_service_error(exc)


@router.get("/api/meeting-rooms")
def get_meeting_rooms(
    keyword: Optional[str] = None,
    site_name: Optional[str] = None,
    building_name: Optional[str] = None,
    floor_label: Optional[str] = None,
    is_enabled: Optional[bool] = None,
    min_capacity: Optional[int] = None,
    db: Session = Depends(get_db),
):
    try:
        return meeting_service.list_rooms(
            db=db,
            keyword=keyword,
            site_name=site_name,
            building_name=building_name,
            floor_label=floor_label,
            is_enabled=is_enabled,
            min_capacity=min_capacity,
        )
    except MeetingServiceError as exc:
        raise_service_error(exc)


@router.post("/api/meeting-rooms")
def create_meeting_room(
    payload: MeetingRoomCreateRequest,
    db: Session = Depends(get_db),
):
    try:
        return meeting_service.create_room(db, payload.model_dump(exclude_none=True))
    except MeetingServiceError as exc:
        raise_service_error(exc)


@router.get("/api/meeting-rooms/usage")
def get_meeting_room_usage(
    date: Optional[str] = None,
    room_id: Optional[str] = None,
    site_name: Optional[str] = None,
    db: Session = Depends(get_db),
):
    try:
        return meeting_service.get_room_usage(
            db=db,
            usage_date=date,
            room_id=room_id,
            site_name=site_name,
        )
    except MeetingServiceError as exc:
        raise_service_error(exc)


@router.get("/api/meetings/{meeting_id}")
def get_meeting(meeting_id: str, db: Session = Depends(get_db)):
    try:
        return meeting_service.get_meeting(db, meeting_id)
    except MeetingServiceError as exc:
        raise_service_error(exc)


@router.patch("/api/meetings/{meeting_id}")
def patch_meeting(
    meeting_id: str,
    payload: MeetingUpdateRequest,
    http_request: Request,
    db: Session = Depends(get_db),
):
    try:
        return meeting_service.update_meeting(
            db=db,
            meeting_id=meeting_id,
            payload=payload.model_dump(exclude_unset=True, exclude={"meeting_id"}),
            current_user_id=get_current_user_id(http_request),
        )
    except MeetingServiceError as exc:
        raise_service_error(exc)


@router.get("/api/meetings/{meeting_id}/todos")
def get_meeting_todos(meeting_id: str, db: Session = Depends(get_db)):
    try:
        return meeting_service.get_meeting_todos(db, meeting_id)
    except MeetingServiceError as exc:
        raise_service_error(exc)


@router.post("/api/meetings/{meeting_id}/summary")
def generate_meeting_summary(meeting_id: str, db: Session = Depends(get_db)):
    try:
        return meeting_service.generate_summary(db, meeting_id)
    except MeetingServiceError as exc:
        raise_service_error(exc)


@router.patch("/api/meeting-rooms/{room_id}")
def patch_meeting_room(
    room_id: str,
    payload: MeetingRoomUpdateRequest,
    db: Session = Depends(get_db),
):
    try:
        return meeting_service.update_room(db, room_id, payload.model_dump(exclude_unset=True))
    except MeetingServiceError as exc:
        raise_service_error(exc)


@router.delete("/api/meeting-rooms/{room_id}")
def delete_meeting_room(room_id: str, db: Session = Depends(get_db)):
    try:
        return meeting_service.delete_room(db, room_id)
    except MeetingServiceError as exc:
        raise_service_error(exc)
