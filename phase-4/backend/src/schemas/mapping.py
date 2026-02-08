"""
Display Mapping Schemas for AI Task Display Mapping Feature

These Pydantic schemas support the runtime mapping between display indices
(user-facing) and internal task IDs (database).
"""
from pydantic import BaseModel, Field
from typing import Union, Optional, List
from datetime import datetime


class DisplayMapping(BaseModel):
    """Single display mapping entry linking a display index to a task ID"""
    display_index: int = Field(..., ge=1, description="1-based sequential index shown to user")
    task_id: Union[str, int] = Field(..., description="Internal task identifier")


class DisplayMappingState(BaseModel):
    """Complete display mapping state for a user session"""
    mappings: List[DisplayMapping]
    user_id: Union[str, int]
    last_updated: datetime
    is_valid: bool = Field(default=True)


class MappingRefreshRequest(BaseModel):
    """Request to refresh display mapping"""
    user_id: Union[str, int] = Field(..., description="User identifier for mapping context")
    tasks: List[dict] = Field(..., description="List of task objects with id, title, completed")


class MappingRefreshResponse(BaseModel):
    """Response from mapping refresh endpoint"""
    mapping_updated: bool
    total_mappings: int
    display_mapping: List[DisplayMapping]
    refreshed_at: datetime


class ResolveDisplayIndexRequest(BaseModel):
    """Request to resolve display index to task ID"""
    display_index: int = Field(..., ge=1, description="Display index to resolve (1-based)")
    user_id: Union[str, int] = Field(..., description="User identifier")


class ResolveDisplayIndexResponse(BaseModel):
    """Response from display index resolution"""
    task_id: Union[str, int]
    display_index: int
    valid: bool
    error: Optional[str] = None
