from datetime import datetime
from typing import Optional
from pydantic import BaseModel, constr

from .models import TaskStatus, TaskPriority

# Category schemas
class CategoryBase(BaseModel):
    name: constr(min_length=1, max_length=50)
    color: Optional[str] = "#6D28D9"

class CategoryCreate(CategoryBase):
    description: Optional[str] = None
    is_default: bool = False

class Category(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True  # Added for Pydantic v2

# Task schemas
class TaskBase(BaseModel):
    title: constr(min_length=1, max_length=255)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    category_id: Optional[int] = None

class TaskCreate(TaskBase):
    tags: Optional[list[str]] = None
    reminder: Optional[datetime] = None

class TaskUpdate(BaseModel):
    title: Optional[constr(min_length=1, max_length=255)] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    category_id: Optional[int] = None
    tags: Optional[list[str]] = None
    reminder: Optional[datetime] = None

class Task(TaskBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True
        from_attributes = True  # Added for Pydantic v2

class TaskWithCategory(Task):
    category: Optional[Category] = None