from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# =====================================================
# SCHÉMAS POUR LES CATÉGORIES DU FORUM
# =====================================================

class ForumCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    subject: Optional[str] = None
    level: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: bool = True

class ForumCategoryCreate(ForumCategoryBase):
    pass

class ForumCategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    subject: Optional[str] = None
    level: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: Optional[bool] = None

class ForumCategoryResponse(ForumCategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# =====================================================
# SCHÉMAS POUR LES THREADS DU FORUM
# =====================================================

class ForumThreadCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    category_id: int
    tags: Optional[str] = None

class ForumThreadResponse(BaseModel):
    id: int
    title: str
    content: str
    category_id: int
    author_id: int
    tags: Optional[str] = None
    is_pinned: bool = False
    is_locked: bool = False
    view_count: int = 0
    reply_count: int = 0
    last_reply_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# =====================================================
# SCHÉMAS POUR LES TAGS DU FORUM
# =====================================================

class ForumTagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None

class ForumTagCreate(ForumTagBase):
    pass

class ForumTagResponse(ForumTagBase):
    id: int
    usage_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# =====================================================
# SCHÉMAS POUR LES TAGS DE THREAD
# =====================================================

class ThreadTagBase(BaseModel):
    thread_id: int
    tag_id: int

class ThreadTagCreate(ThreadTagBase):
    pass

class ThreadTagResponse(ThreadTagBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# =====================================================
# SCHÉMAS POUR LES VOTES DU FORUM
# =====================================================

class ForumVoteBase(BaseModel):
    message_id: int
    vote_type: str = Field(..., pattern="^(up|down)$")

class ForumVoteCreate(ForumVoteBase):
    pass

class ForumVoteResponse(ForumVoteBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# =====================================================
# SCHÉMAS POUR LES SIGNALEMENTS DU FORUM
# =====================================================

class ForumReportBase(BaseModel):
    thread_id: Optional[int] = None
    message_id: Optional[int] = None
    reason: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class ForumReportCreate(ForumReportBase):
    pass

class ForumReportResponse(ForumReportBase):
    id: int
    reporter_id: int
    status: str
    moderator_id: Optional[int] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# =====================================================
# SCHÉMAS POUR LA MODÉRATION DU FORUM
# =====================================================

class ForumModerationBase(BaseModel):
    thread_id: Optional[int] = None
    message_id: Optional[int] = None
    action: str = Field(..., pattern="^(hide|delete|warn|ban)$")
    reason: Optional[str] = None

class ForumModerationCreate(ForumModerationBase):
    pass

class ForumModerationResponse(ForumModerationBase):
    id: int
    moderator_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# =====================================================
# SCHÉMAS POUR LES STATISTIQUES DU FORUM
# =====================================================

class ForumStats(BaseModel):
    thread_id: int
    title: str
    message_count: int
    unique_users: int
    last_activity: Optional[datetime]
    total_votes: int
    up_votes: int
    down_votes: int
    
    class Config:
        from_attributes = True

# =====================================================
# SCHÉMAS POUR LES RECHERCHES DU FORUM
# =====================================================

class ForumSearchParams(BaseModel):
    query: Optional[str] = None
    category_id: Optional[int] = None
    subject: Optional[str] = None
    level: Optional[str] = None
    tags: Optional[List[str]] = None
    author_id: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    sort_by: str = "created_at"
    sort_order: str = "desc"
    page: int = 1
    limit: int = 20

class ForumSearchResponse(BaseModel):
    threads: List[dict]
    total_count: int
    page: int
    total_pages: int
    has_next: bool
    has_prev: bool 