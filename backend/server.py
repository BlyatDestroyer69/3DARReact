from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List, Optional
import base64
import uuid
from datetime import datetime

# Import models
from models import *

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(title="AR Adventure API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize default data
async def initialize_default_data():
    """Initialize the database with default plants, checkpoints, and trails"""
    
    # Check if data already exists
    existing_plants = await db.plants.count_documents({})
    if existing_plants > 0:
        logger.info("Default data already exists, skipping initialization")
        return
    
    # Default plants
    default_plants = [
        Plant(
            id="plant_1",
            name="Bird's Nest Fern",
            scientific_name="Asplenium nidus",
            description="A large epiphytic fern native to tropical regions. Its distinctive nest-like shape helps collect water and organic debris.",
            facts=["Can grow up to 1.5 meters wide", "Epiphytic - grows on other plants", "Popular as houseplant"],
            rarity=PlantRarity.COMMON,
            habitat="Tropical rainforests, epiphytic on trees",
            conservation_status="Least Concern"
        ),
        Plant(
            id="plant_2",
            name="Giant Bamboo",
            scientific_name="Dendrocalamus giganteus",
            description="One of the largest bamboo species in the world. It can grow extremely fast and is used for construction.",
            facts=["Can grow up to 3 feet per day", "Reaches heights of 100+ feet", "Stronger than steel in tensile strength"],
            rarity=PlantRarity.UNCOMMON,
            habitat="Tropical and subtropical regions",
            conservation_status="Stable"
        ),
        Plant(
            id="plant_3",
            name="Wild Orchid",
            scientific_name="Vanda hookeriana",
            description="A beautiful epiphytic orchid species endemic to Southeast Asia. Known for its fragrant flowers.",
            facts=["Blooms year-round", "Requires high humidity", "Protected species"],
            rarity=PlantRarity.RARE,
            habitat="Tropical forests, epiphytic on trees",
            conservation_status="Vulnerable"
        ),
        Plant(
            id="plant_4",
            name="Meranti Tree",
            scientific_name="Shorea sp.",
            description="A tall tropical hardwood tree, part of the dipterocarp family. Important for timber and ecosystem.",
            facts=["Can live over 100 years", "Provides canopy shelter", "Seeds have wing-like structures"],
            rarity=PlantRarity.COMMON,
            habitat="Tropical rainforests, lowland areas",
            conservation_status="Near Threatened"
        ),
        Plant(
            id="plant_5",
            name="Tropical Pitcher Plant",
            scientific_name="Nepenthes rafflesiana",
            description="A carnivorous plant with modified leaves that form pitcher-shaped traps to catch insects.",
            facts=["Carnivorous plant", "Pitchers can hold 200ml of water", "Endemic to Southeast Asia"],
            rarity=PlantRarity.RARE,
            habitat="Tropical peat swamps and forests",
            conservation_status="Vulnerable"
        )
    ]
    
    # Insert plants
    for plant in default_plants:
        await db.plants.insert_one(plant.dict())
    
    # Default trail
    default_trail = Trail(
        id="trail_1",
        name="Bukit Kiara Main Trail",
        difficulty=TrailDifficulty.EASY,
        distance="2.5 km",
        duration="1-2 hours",
        description="The main trail loop suitable for all fitness levels",
        checkpoint_ids=["checkpoint_1", "checkpoint_2", "checkpoint_3", "checkpoint_4", "checkpoint_5"]
    )
    
    await db.trails.insert_one(default_trail.dict())
    
    # Default checkpoints
    default_checkpoints = [
        Checkpoint(
            id="checkpoint_1",
            name="Fern Valley",
            position=CheckpointPosition(x=20, y=25),
            plant_id="plant_1",
            color="#22c55e",
            trail_id="trail_1"
        ),
        Checkpoint(
            id="checkpoint_2",
            name="Bamboo Grove",
            position=CheckpointPosition(x=70, y=40),
            plant_id="plant_2",
            color="#eab308",
            trail_id="trail_1"
        ),
        Checkpoint(
            id="checkpoint_3",
            name="Orchid Point",
            position=CheckpointPosition(x=45, y=15),
            plant_id="plant_3",
            color="#a855f7",
            trail_id="trail_1"
        ),
        Checkpoint(
            id="checkpoint_4",
            name="Dipterocarp Trail",
            position=CheckpointPosition(x=35, y=60),
            plant_id="plant_4",
            color="#dc2626",
            trail_id="trail_1"
        ),
        Checkpoint(
            id="checkpoint_5",
            name="Pitcher Plant Bog",
            position=CheckpointPosition(x=80, y=70),
            plant_id="plant_5",
            color="#f59e0b",
            trail_id="trail_1"
        )
    ]
    
    for checkpoint in default_checkpoints:
        await db.checkpoints.insert_one(checkpoint.dict())
    
    # Default achievements
    default_achievements = [
        Achievement(
            id="achievement_1",
            name="First Discovery",
            description="Discover your first plant checkpoint",
            icon="🌱",
            condition="discover_plants",
            condition_value=1,
            points=10
        ),
        Achievement(
            id="achievement_2",
            name="Plant Expert",
            description="Discover 5 different plant species",
            icon="🌿",
            condition="discover_plants",
            condition_value=5,
            points=50
        ),
        Achievement(
            id="achievement_3",
            name="Rare Collector",
            description="Find all rare plant species",
            icon="🌺",
            condition="discover_rare_plants",
            condition_value=2,
            points=100
        ),
        Achievement(
            id="achievement_4",
            name="Trail Master",
            description="Complete all available trails",
            icon="🏆",
            condition="complete_trails",
            condition_value=1,
            points=200
        )
    ]
    
    for achievement in default_achievements:
        await db.achievements.insert_one(achievement.dict())
    
    logger.info("Default data initialized successfully")

# Startup event
@app.on_event("startup")
async def startup_event():
    await initialize_default_data()

# Basic routes
@api_router.get("/")
async def root():
    return {"message": "AR Adventure API is running"}

@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# User Session Management
@api_router.post("/sessions", response_model=UserSession)
async def create_session(device_id: str):
    """Create a new user session"""
    session = UserSession(device_id=device_id)
    await db.sessions.insert_one(session.dict())
    
    # Create initial user progress
    progress = UserProgress(session_id=session.id, total_checkpoints=5)
    await db.user_progress.insert_one(progress.dict())
    
    return session

@api_router.get("/sessions/{session_id}", response_model=UserSession)
async def get_session(session_id: str):
    """Get session details"""
    session = await db.sessions.find_one({"id": session_id})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return UserSession(**session)

# Plant Management
@api_router.get("/plants", response_model=List[Plant])
async def get_plants():
    """Get all plant species"""
    plants = await db.plants.find().to_list(100)
    return [Plant(**plant) for plant in plants]

@api_router.get("/plants/{plant_id}", response_model=Plant)
async def get_plant(plant_id: str):
    """Get specific plant details"""
    plant = await db.plants.find_one({"id": plant_id})
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return Plant(**plant)

@api_router.post("/plants", response_model=Plant)
async def create_plant(plant: PlantCreate):
    """Create a new plant species"""
    new_plant = Plant(**plant.dict())
    await db.plants.insert_one(new_plant.dict())
    return new_plant

# Checkpoint Management
@api_router.get("/checkpoints", response_model=List[CheckpointWithPlant])
async def get_checkpoints(trail_id: Optional[str] = None, session_id: Optional[str] = None):
    """Get all checkpoints with plant information"""
    query = {}
    if trail_id:
        query["trail_id"] = trail_id
    
    checkpoints = await db.checkpoints.find(query).to_list(100)
    
    # Get user discoveries if session_id provided
    discovered_checkpoints = []
    if session_id:
        discoveries = await db.user_discoveries.find({"session_id": session_id}).to_list(100)
        discovered_checkpoints = [d["checkpoint_id"] for d in discoveries]
    
    # Enhance with plant data
    result = []
    for checkpoint in checkpoints:
        plant = await db.plants.find_one({"id": checkpoint["plant_id"]})
        if plant:
            checkpoint_with_plant = CheckpointWithPlant(
                **checkpoint,
                plant=Plant(**plant),
                discovered=(checkpoint["id"] in discovered_checkpoints)
            )
            result.append(checkpoint_with_plant)
    
    return result

@api_router.get("/checkpoints/{checkpoint_id}", response_model=CheckpointWithPlant)
async def get_checkpoint(checkpoint_id: str, session_id: Optional[str] = None):
    """Get specific checkpoint with plant information"""
    checkpoint = await db.checkpoints.find_one({"id": checkpoint_id})
    if not checkpoint:
        raise HTTPException(status_code=404, detail="Checkpoint not found")
    
    plant = await db.plants.find_one({"id": checkpoint["plant_id"]})
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    
    # Check if discovered
    discovered = False
    if session_id:
        discovery = await db.user_discoveries.find_one({
            "session_id": session_id,
            "checkpoint_id": checkpoint_id
        })
        discovered = discovery is not None
    
    return CheckpointWithPlant(
        **checkpoint,
        plant=Plant(**plant),
        discovered=discovered
    )

# Discovery System
@api_router.post("/discoveries", response_model=DiscoveryResponse)
async def discover_checkpoint(session_id: str, checkpoint_id: str):
    """Record a plant discovery"""
    
    # Check if already discovered
    existing_discovery = await db.user_discoveries.find_one({
        "session_id": session_id,
        "checkpoint_id": checkpoint_id
    })
    
    if existing_discovery:
        return DiscoveryResponse(
            success=False,
            message="Already discovered this checkpoint"
        )
    
    # Get checkpoint and plant info
    checkpoint = await db.checkpoints.find_one({"id": checkpoint_id})
    if not checkpoint:
        raise HTTPException(status_code=404, detail="Checkpoint not found")
    
    plant = await db.plants.find_one({"id": checkpoint["plant_id"]})
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    
    # Create discovery record
    discovery = UserDiscovery(
        session_id=session_id,
        checkpoint_id=checkpoint_id,
        plant_id=checkpoint["plant_id"],
        location=CheckpointPosition(**checkpoint["position"])
    )
    
    await db.user_discoveries.insert_one(discovery.dict())
    
    # Update checkpoint discovery count
    await db.checkpoints.update_one(
        {"id": checkpoint_id},
        {"$inc": {"discovered_count": 1}}
    )
    
    # Update user progress
    await db.user_progress.update_one(
        {"session_id": session_id},
        {
            "$push": {"checkpoints_discovered": checkpoint_id},
            "$inc": {"plants_collected": 1},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    # Check for achievements
    achievement_unlocked = await check_achievements(session_id)
    
    # Get updated progress
    progress = await db.user_progress.find_one({"session_id": session_id})
    
    return DiscoveryResponse(
        success=True,
        message=f"Discovered {plant['name']}!",
        discovery=discovery,
        achievement_unlocked=achievement_unlocked,
        progress=UserProgress(**progress) if progress else None
    )

# Achievement System
async def check_achievements(session_id: str) -> Optional[Achievement]:
    """Check if user unlocked any achievements"""
    
    # Get user progress
    progress = await db.user_progress.find_one({"session_id": session_id})
    if not progress:
        return None
    
    # Get user's current achievements
    user_achievements = await db.user_achievements.find({"session_id": session_id}).to_list(100)
    unlocked_achievement_ids = [ua["achievement_id"] for ua in user_achievements]
    
    # Get all achievements
    all_achievements = await db.achievements.find().to_list(100)
    
    for achievement_data in all_achievements:
        achievement = Achievement(**achievement_data)
        
        # Skip if already unlocked
        if achievement.id in unlocked_achievement_ids:
            continue
        
        # Check conditions
        condition_met = False
        
        if achievement.condition == "discover_plants":
            condition_met = progress["plants_collected"] >= achievement.condition_value
        elif achievement.condition == "discover_rare_plants":
            # Count rare plants discovered
            discoveries = await db.user_discoveries.find({"session_id": session_id}).to_list(100)
            rare_count = 0
            for discovery in discoveries:
                plant = await db.plants.find_one({"id": discovery["plant_id"]})
                if plant and plant["rarity"] == "Rare":
                    rare_count += 1
            condition_met = rare_count >= achievement.condition_value
        elif achievement.condition == "complete_trails":
            condition_met = len(progress["completed_trails"]) >= achievement.condition_value
        
        if condition_met:
            # Unlock achievement
            user_achievement = UserAchievement(
                session_id=session_id,
                achievement_id=achievement.id
            )
            await db.user_achievements.insert_one(user_achievement.dict())
            
            # Update progress
            await db.user_progress.update_one(
                {"session_id": session_id},
                {"$push": {"achievements_unlocked": achievement.id}}
            )
            
            return achievement
    
    return None

@api_router.get("/achievements", response_model=List[Achievement])
async def get_achievements():
    """Get all available achievements"""
    achievements = await db.achievements.find().to_list(100)
    return [Achievement(**achievement) for achievement in achievements]

@api_router.get("/progress/{session_id}", response_model=ProgressSummary)
async def get_progress(session_id: str):
    """Get user progress summary"""
    progress = await db.user_progress.find_one({"session_id": session_id})
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    
    # Get discoveries for rarity breakdown
    discoveries = await db.user_discoveries.find({"session_id": session_id}).to_list(100)
    rarity_breakdown = {"Common": 0, "Uncommon": 0, "Rare": 0, "Legendary": 0}
    
    for discovery in discoveries:
        plant = await db.plants.find_one({"id": discovery["plant_id"]})
        if plant:
            rarity_breakdown[plant["rarity"]] += 1
    
    return ProgressSummary(
        session_id=session_id,
        total_discoveries=len(progress["checkpoints_discovered"]),
        total_checkpoints=progress["total_checkpoints"],
        completion_percentage=(len(progress["checkpoints_discovered"]) / progress["total_checkpoints"] * 100) if progress["total_checkpoints"] > 0 else 0,
        achievements_count=len(progress["achievements_unlocked"]),
        trails_completed=len(progress["completed_trails"]),
        time_spent=progress["time_spent"],
        plants_collected=progress["plants_collected"],
        rarity_breakdown=rarity_breakdown
    )

# Trail Management
@api_router.get("/trails", response_model=List[Trail])
async def get_trails():
    """Get all trails"""
    trails = await db.trails.find().to_list(100)
    return [Trail(**trail) for trail in trails]

@api_router.get("/trails/{trail_id}", response_model=Trail)
async def get_trail(trail_id: str):
    """Get specific trail details"""
    trail = await db.trails.find_one({"id": trail_id})
    if not trail:
        raise HTTPException(status_code=404, detail="Trail not found")
    return Trail(**trail)

# Map Image Management
@api_router.post("/maps", response_model=MapImage)
async def upload_map(
    name: str = Form(...),
    trail_id: str = Form(...),
    file: UploadFile = File(...)
):
    """Upload a map image"""
    
    # Read and encode image
    content = await file.read()
    image_data = base64.b64encode(content).decode('utf-8')
    
    map_image = MapImage(
        name=name,
        image_data=image_data,
        image_type=file.content_type,
        trail_id=trail_id
    )
    
    await db.maps.insert_one(map_image.dict())
    return map_image

@api_router.get("/maps/{trail_id}", response_model=Optional[MapImage])
async def get_map(trail_id: str):
    """Get map image for a trail"""
    map_image = await db.maps.find_one({"trail_id": trail_id})
    if not map_image:
        return None
    return MapImage(**map_image)

# Settings Management
@api_router.get("/settings/{session_id}", response_model=ARSettings)
async def get_settings(session_id: str):
    """Get AR settings for a session"""
    settings = await db.settings.find_one({"session_id": session_id})
    if not settings:
        # Create default settings
        default_settings = ARSettings(session_id=session_id)
        await db.settings.insert_one(default_settings.dict())
        return default_settings
    return ARSettings(**settings)

@api_router.put("/settings/{session_id}", response_model=ARSettings)
async def update_settings(session_id: str, settings_update: ARSettingsUpdate):
    """Update AR settings"""
    update_data = {k: v for k, v in settings_update.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    await db.settings.update_one(
        {"session_id": session_id},
        {"$set": update_data},
        upsert=True
    )
    
    settings = await db.settings.find_one({"session_id": session_id})
    return ARSettings(**settings)

# Include the router in the main app
app.include_router(api_router)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)