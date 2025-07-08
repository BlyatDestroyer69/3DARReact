import requests
import json
import uuid
import time
from typing import Dict, Any, List, Optional

# Get the backend URL from the frontend .env file
with open('/app/frontend/.env', 'r') as f:
    for line in f:
        if line.startswith('REACT_APP_BACKEND_URL='):
            BACKEND_URL = line.strip().split('=')[1].strip('"\'')
            break

# Ensure the URL doesn't have quotes
if BACKEND_URL.startswith('"') and BACKEND_URL.endswith('"'):
    BACKEND_URL = BACKEND_URL[1:-1]
elif BACKEND_URL.startswith("'") and BACKEND_URL.endswith("'"):
    BACKEND_URL = BACKEND_URL[1:-1]

API_URL = f"{BACKEND_URL}/api"
print(f"Using API URL: {API_URL}")

class ARAdventureTestClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session_id = None
        self.device_id = str(uuid.uuid4())
        
    def _make_request(self, method: str, endpoint: str, params: Dict[str, Any] = None, 
                     data: Dict[str, Any] = None, json_data: Dict[str, Any] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        response = requests.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json_data
        )
        
        try:
            return {
                "status_code": response.status_code,
                "data": response.json() if response.text else None,
                "success": response.status_code >= 200 and response.status_code < 300
            }
        except json.JSONDecodeError:
            return {
                "status_code": response.status_code,
                "data": response.text,
                "success": response.status_code >= 200 and response.status_code < 300
            }
    
    def health_check(self) -> Dict[str, Any]:
        return self._make_request("GET", "/health")
    
    def create_session(self) -> Dict[str, Any]:
        response = self._make_request("POST", f"/sessions?device_id={self.device_id}")
        if response["success"]:
            self.session_id = response["data"]["id"]
        return response
    
    def get_session(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        session_id = session_id or self.session_id
        return self._make_request("GET", f"/sessions/{session_id}")
    
    def get_plants(self) -> Dict[str, Any]:
        return self._make_request("GET", "/plants")
    
    def get_plant(self, plant_id: str) -> Dict[str, Any]:
        return self._make_request("GET", f"/plants/{plant_id}")
    
    def get_checkpoints(self, trail_id: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if trail_id:
            params["trail_id"] = trail_id
        if self.session_id:
            params["session_id"] = self.session_id
            
        return self._make_request("GET", "/checkpoints", params=params)
    
    def get_checkpoint(self, checkpoint_id: str) -> Dict[str, Any]:
        params = {}
        if self.session_id:
            params["session_id"] = self.session_id
            
        return self._make_request("GET", f"/checkpoints/{checkpoint_id}", params=params)
    
    def discover_checkpoint(self, checkpoint_id: str) -> Dict[str, Any]:
        return self._make_request(
            "POST", 
            f"/discoveries?session_id={self.session_id}&checkpoint_id={checkpoint_id}"
        )
    
    def get_achievements(self) -> Dict[str, Any]:
        return self._make_request("GET", "/achievements")
    
    def get_progress(self) -> Dict[str, Any]:
        return self._make_request("GET", f"/progress/{self.session_id}")
    
    def get_trails(self) -> Dict[str, Any]:
        return self._make_request("GET", "/trails")
    
    def get_trail(self, trail_id: str) -> Dict[str, Any]:
        return self._make_request("GET", f"/trails/{trail_id}")
    
    def get_settings(self) -> Dict[str, Any]:
        return self._make_request("GET", f"/settings/{self.session_id}")
    
    def update_settings(self, settings_update: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request("PUT", f"/settings/{self.session_id}", json_data=settings_update)


def run_tests():
    print("=" * 80)
    print("AR Adventure Backend API Tests")
    print("=" * 80)
    
    client = ARAdventureTestClient(API_URL)
    
    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    health_response = client.health_check()
    assert health_response["success"], f"Health check failed: {health_response}"
    print("✅ Health check successful")
    
    # Test 2: Session Management
    print("\n2. Testing Session Management...")
    
    # 2.1 Create a new session
    print("  2.1 Creating a new user session...")
    session_response = client.create_session()
    assert session_response["success"], f"Session creation failed: {session_response}"
    assert "id" in session_response["data"], "Session ID not found in response"
    session_id = session_response["data"]["id"]
    print(f"✅ Session created successfully with ID: {session_id}")
    
    # 2.2 Get session information
    print("  2.2 Retrieving session information...")
    get_session_response = client.get_session(session_id)
    assert get_session_response["success"], f"Session retrieval failed: {get_session_response}"
    assert get_session_response["data"]["id"] == session_id, "Session ID mismatch"
    assert get_session_response["data"]["device_id"] == client.device_id, "Device ID mismatch"
    print("✅ Session information retrieved successfully")
    
    # Test 3: Plant Management
    print("\n3. Testing Plant Management...")
    
    # 3.1 Get all plants
    print("  3.1 Getting all plants...")
    plants_response = client.get_plants()
    assert plants_response["success"], f"Plants retrieval failed: {plants_response}"
    assert len(plants_response["data"]) == 5, f"Expected 5 plants, got {len(plants_response['data'])}"
    print(f"✅ Retrieved {len(plants_response['data'])} plants successfully")
    
    # 3.2 Get specific plant
    print("  3.2 Getting specific plant details...")
    plant_id = plants_response["data"][0]["id"]
    plant_response = client.get_plant(plant_id)
    assert plant_response["success"], f"Plant retrieval failed: {plant_response}"
    assert plant_response["data"]["id"] == plant_id, "Plant ID mismatch"
    print(f"✅ Retrieved plant '{plant_response['data']['name']}' successfully")
    
    # Test 4: Checkpoint Management
    print("\n4. Testing Checkpoint Management...")
    
    # 4.1 Get all checkpoints
    print("  4.1 Getting all checkpoints...")
    checkpoints_response = client.get_checkpoints()
    assert checkpoints_response["success"], f"Checkpoints retrieval failed: {checkpoints_response}"
    assert len(checkpoints_response["data"]) == 5, f"Expected 5 checkpoints, got {len(checkpoints_response['data'])}"
    print(f"✅ Retrieved {len(checkpoints_response['data'])} checkpoints successfully")
    
    # 4.2 Get specific checkpoint
    print("  4.2 Getting specific checkpoint details...")
    checkpoint_id = checkpoints_response["data"][0]["id"]
    checkpoint_response = client.get_checkpoint(checkpoint_id)
    assert checkpoint_response["success"], f"Checkpoint retrieval failed: {checkpoint_response}"
    assert checkpoint_response["data"]["id"] == checkpoint_id, "Checkpoint ID mismatch"
    print(f"✅ Retrieved checkpoint '{checkpoint_response['data']['name']}' successfully")
    
    # Test 5: Trail Management
    print("\n5. Testing Trail Management...")
    
    # 5.1 Get all trails
    print("  5.1 Getting all trails...")
    trails_response = client.get_trails()
    assert trails_response["success"], f"Trails retrieval failed: {trails_response}"
    assert len(trails_response["data"]) > 0, "No trails found"
    trail_id = trails_response["data"][0]["id"]
    print(f"✅ Retrieved {len(trails_response['data'])} trails successfully")
    
    # 5.2 Get specific trail
    print("  5.2 Getting specific trail details...")
    trail_response = client.get_trail(trail_id)
    assert trail_response["success"], f"Trail retrieval failed: {trail_response}"
    assert trail_response["data"]["id"] == trail_id, "Trail ID mismatch"
    print(f"✅ Retrieved trail '{trail_response['data']['name']}' successfully")
    
    # 5.3 Get checkpoints for a specific trail
    print("  5.3 Getting checkpoints for a specific trail...")
    trail_checkpoints_response = client.get_checkpoints(trail_id)
    assert trail_checkpoints_response["success"], f"Trail checkpoints retrieval failed: {trail_checkpoints_response}"
    assert len(trail_checkpoints_response["data"]) > 0, "No checkpoints found for trail"
    print(f"✅ Retrieved {len(trail_checkpoints_response['data'])} checkpoints for trail successfully")
    
    # Test 6: Discovery System
    print("\n6. Testing Discovery System...")
    
    # 6.1 Discover a checkpoint
    print("  6.1 Discovering a checkpoint...")
    checkpoint_id = checkpoints_response["data"][0]["id"]
    discovery_response = client.discover_checkpoint(checkpoint_id)
    assert discovery_response["success"], f"Checkpoint discovery failed: {discovery_response}"
    assert discovery_response["data"]["success"], f"Discovery unsuccessful: {discovery_response['data']['message']}"
    print(f"✅ Discovered checkpoint successfully: {discovery_response['data']['message']}")
    
    # 6.2 Try to discover the same checkpoint again
    print("  6.2 Attempting to discover the same checkpoint again...")
    rediscovery_response = client.discover_checkpoint(checkpoint_id)
    assert rediscovery_response["success"], f"Rediscovery request failed: {rediscovery_response}"
    assert not rediscovery_response["data"]["success"], "Rediscovery should not be successful"
    assert "Already discovered" in rediscovery_response["data"]["message"], "Expected 'Already discovered' message"
    print(f"✅ Rediscovery correctly rejected: {rediscovery_response['data']['message']}")
    
    # 6.3 Discover another checkpoint
    print("  6.3 Discovering another checkpoint...")
    checkpoint_id_2 = checkpoints_response["data"][1]["id"]
    discovery_response_2 = client.discover_checkpoint(checkpoint_id_2)
    assert discovery_response_2["success"], f"Second checkpoint discovery failed: {discovery_response_2}"
    assert discovery_response_2["data"]["success"], f"Second discovery unsuccessful: {discovery_response_2['data']['message']}"
    print(f"✅ Discovered second checkpoint successfully: {discovery_response_2['data']['message']}")
    
    # Test 7: Progress Tracking
    print("\n7. Testing Progress Tracking...")
    
    # 7.1 Get user progress
    print("  7.1 Getting user progress...")
    progress_response = client.get_progress()
    assert progress_response["success"], f"Progress retrieval failed: {progress_response}"
    assert progress_response["data"]["session_id"] == client.session_id, "Session ID mismatch in progress"
    assert progress_response["data"]["total_discoveries"] == 2, f"Expected 2 discoveries, got {progress_response['data']['total_discoveries']}"
    assert progress_response["data"]["completion_percentage"] == 40.0, f"Expected 40% completion, got {progress_response['data']['completion_percentage']}%"
    print(f"✅ Progress tracking working correctly: {progress_response['data']['completion_percentage']}% complete")
    
    # 7.2 Check rarity breakdown
    print("  7.2 Checking rarity breakdown...")
    rarity_breakdown = progress_response["data"]["rarity_breakdown"]
    print(f"    Rarity breakdown: {rarity_breakdown}")
    assert sum(rarity_breakdown.values()) == 2, f"Expected 2 total plants in rarity breakdown, got {sum(rarity_breakdown.values())}"
    print("✅ Rarity breakdown working correctly")
    
    # Test 8: Achievement System
    print("\n8. Testing Achievement System...")
    
    # 8.1 Get all achievements
    print("  8.1 Getting all achievements...")
    achievements_response = client.get_achievements()
    assert achievements_response["success"], f"Achievements retrieval failed: {achievements_response}"
    assert len(achievements_response["data"]) > 0, "No achievements found"
    print(f"✅ Retrieved {len(achievements_response['data'])} achievements successfully")
    
    # 8.2 Check if any achievements were unlocked during discoveries
    print("  8.2 Checking for unlocked achievements...")
    if discovery_response["data"].get("achievement_unlocked") or discovery_response_2["data"].get("achievement_unlocked"):
        print("✅ Achievement system working correctly - achievement unlocked during discovery")
    else:
        # Discover remaining checkpoints to trigger achievement
        print("    No achievements unlocked yet. Discovering remaining checkpoints...")
        for i in range(2, min(5, len(checkpoints_response["data"]))):
            checkpoint_id = checkpoints_response["data"][i]["id"]
            discovery_response = client.discover_checkpoint(checkpoint_id)
            if discovery_response["data"].get("achievement_unlocked"):
                print(f"✅ Achievement unlocked after discovering checkpoint {i+1}: {discovery_response['data']['achievement_unlocked']['name']}")
                break
        else:
            print("⚠️ No achievements unlocked after discovering multiple checkpoints")
    
    # Test 9: Settings Management
    print("\n9. Testing Settings Management...")
    
    # 9.1 Get default settings
    print("  9.1 Getting default AR settings...")
    settings_response = client.get_settings()
    assert settings_response["success"], f"Settings retrieval failed: {settings_response}"
    assert settings_response["data"]["session_id"] == client.session_id, "Session ID mismatch in settings"
    print("✅ Default settings retrieved successfully")
    
    # 9.2 Update settings
    print("  9.2 Updating AR settings...")
    settings_update = {
        "sound_enabled": False,
        "show_hints": False,
        "render_quality": "medium"
    }
    update_settings_response = client.update_settings(settings_update)
    assert update_settings_response["success"], f"Settings update failed: {update_settings_response}"
    assert update_settings_response["data"]["sound_enabled"] == False, "Sound setting not updated"
    assert update_settings_response["data"]["show_hints"] == False, "Show hints setting not updated"
    assert update_settings_response["data"]["render_quality"] == "medium", "Render quality setting not updated"
    print("✅ Settings updated successfully")
    
    # 9.3 Verify settings persistence
    print("  9.3 Verifying settings persistence...")
    settings_response_2 = client.get_settings()
    assert settings_response_2["success"], f"Settings retrieval failed: {settings_response_2}"
    assert settings_response_2["data"]["sound_enabled"] == False, "Sound setting not persisted"
    assert settings_response_2["data"]["show_hints"] == False, "Show hints setting not persisted"
    assert settings_response_2["data"]["render_quality"] == "medium", "Render quality setting not persisted"
    print("✅ Settings persistence verified")
    
    print("\n" + "=" * 80)
    print("All tests completed successfully!")
    print("=" * 80)
    
    return {
        "session_management": True,
        "plant_data": True,
        "checkpoint_data": True,
        "discovery_system": True,
        "progress_tracking": True,
        "trail_management": True,
        "settings_management": True
    }

if __name__ == "__main__":
    run_tests()