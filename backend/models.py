from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

class PlantRarity(str, Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    LEGENDARY = "Legendary"

class TrailDifficulty(str, Enum):
    EASY = "Easy"
    MODERATE = "Moderate"
    HARD = "Hard"
    EXPERT = "Expert"

# Plant Species Models
class Plant(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    scientific_name: str
    description: str
    facts: List[str]
    rarity: PlantRarity
    habitat: str
    conservation_status: str
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PlantCreate(BaseModel):
    name: str
    scientific_name: str
    description: str
    facts: List[str]
    rarity: PlantRarity
    habitat: str
    conservation_status: str
    image_url: Optional[str] = None

# Checkpoint Models
class CheckpointPosition(BaseModel):
    x: float
    y: float
    z: Optional[float] = 0

class Checkpoint(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    position: CheckpointPosition
    plant_id: str
    color: str
    trail_id: str
    discovered_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CheckpointCreate(BaseModel):
    name: str
    position: CheckpointPosition
    plant_id: str
    color: str
    trail_id: str

class CheckpointWithPlant(BaseModel):
    id: str
    name: str
    position: CheckpointPosition
    plant: Plant
    color: str
    trail_id: str
    discovered_count: int
    discovered: bool = False

# Trail Models
class Trail(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    difficulty: TrailDifficulty
    distance: str
    duration: str
    description: str
    checkpoint_ids: List[str]
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TrailCreate(BaseModel):
    name: str
    difficulty: TrailDifficulty
    distance: str
    duration: str
    description: str
    checkpoint_ids: List[str]
    image_url: Optional[str] = None

# User Progress Models
class UserSession(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    device_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_active: datetime = Field(default_factory=datetime.utcnow)

class UserDiscovery(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    checkpoint_id: str
    plant_id: str
    discovered_at: datetime = Field(default_factory=datetime.utcnow)
    location: Optional[CheckpointPosition] = None

class UserProgress(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    checkpoints_discovered: List[str] = []
    total_checkpoints: int = 0
    completed_trails: List[str] = []
    total_distance: float = 0.0
    time_spent: int = 0  # in minutes
    plants_collected: int = 0
    achievements_unlocked: List[str] = []
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserProgressCreate(BaseModel):
    session_id: str

# Achievement Models
class Achievement(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    icon: str
    condition: str  # e.g., "discover_5_plants", "complete_trail"
    condition_value: int = 1
    points: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AchievementCreate(BaseModel):
    name: str
    description: str
    icon: str
    condition: str
    condition_value: int = 1
    points: int = 0

class UserAchievement(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    achievement_id: str
    unlocked_at: datetime = Field(default_factory=datetime.utcnow)

# Map Models
class MapImage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    image_data: str  # base64 encoded image
    image_type: str  # MIME type
    trail_id: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

class MapImageCreate(BaseModel):
    name: str
    image_data: str
    image_type: str
    trail_id: str

# Response Models
class DiscoveryResponse(BaseModel):
    success: bool
    message: str
    discovery: Optional[UserDiscovery] = None
    achievement_unlocked: Optional[Achievement] = None
    progress: Optional[UserProgress] = None

class ProgressSummary(BaseModel):
    session_id: str
    total_discoveries: int
    total_checkpoints: int
    completion_percentage: float
    achievements_count: int
    trails_completed: int
    time_spent: int
    plants_collected: int
    rarity_breakdown: Dict[str, int]

# Settings Models
class ARSettings(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    camera_enabled: bool = True
    sound_enabled: bool = True
    vibration_enabled: bool = True
    show_hints: bool = True
    marker_detection_sensitivity: float = 0.7
    render_quality: str = "high"
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ARSettingsCreate(BaseModel):
    session_id: str
    camera_enabled: bool = True
    sound_enabled: bool = True
    vibration_enabled: bool = True
    show_hints: bool = True
    marker_detection_sensitivity: float = 0.7
    render_quality: str = "high"

class ARSettingsUpdate(BaseModel):
    camera_enabled: Optional[bool] = None
    sound_enabled: Optional[bool] = None
    vibration_enabled: Optional[bool] = None
    show_hints: Optional[bool] = None
    marker_detection_sensitivity: Optional[float] = None
    render_quality: Optional[str] = None