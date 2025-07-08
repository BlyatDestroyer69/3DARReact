// Mock data for AR Adventure app
export const mockCheckpoints = [
  {
    id: 1,
    name: "Fern Valley",
    position: { x: -2, y: 0, z: -3 },
    plant: {
      name: "Bird's Nest Fern",
      scientific: "Asplenium nidus",
      description: "A large epiphytic fern native to tropical regions. Its distinctive nest-like shape helps collect water and organic debris from the tree canopy.",
      facts: [
        "Can grow up to 1.5 meters wide",
        "Epiphytic - grows on other plants without harming them",
        "Popular as houseplant due to its unique appearance",
        "Leaves unfurl from center like a bird's nest"
      ],
      rarity: "Common",
      habitat: "Tropical rainforests, epiphytic on trees",
      conservationStatus: "Least Concern"
    },
    color: "#22c55e",
    discovered: false
  },
  {
    id: 2,
    name: "Bamboo Grove",
    position: { x: 2, y: 0, z: -2 },
    plant: {
      name: "Giant Bamboo",
      scientific: "Dendrocalamus giganteus",
      description: "One of the largest bamboo species in the world. Known for its incredible growth rate and strength, making it valuable for construction and environmental benefits.",
      facts: [
        "Can grow up to 3 feet (1 meter) per day",
        "Reaches heights of 100+ feet (30+ meters)",
        "Stronger than steel in tensile strength",
        "Produces 35% more oxygen than trees"
      ],
      rarity: "Uncommon",
      habitat: "Tropical and subtropical regions",
      conservationStatus: "Stable"
    },
    color: "#eab308",
    discovered: false
  },
  {
    id: 3,
    name: "Orchid Point",
    position: { x: 0, y: 0, z: -5 },
    plant: {
      name: "Wild Orchid",
      scientific: "Vanda hookeriana",
      description: "A beautiful epiphytic orchid species endemic to Southeast Asia. Known for its fragrant purple flowers and ability to bloom year-round in suitable conditions.",
      facts: [
        "Blooms year-round in tropical climates",
        "Requires high humidity (70-80%)",
        "Protected species in many countries",
        "Flowers are used in traditional medicine"
      ],
      rarity: "Rare",
      habitat: "Tropical forests, epiphytic on trees",
      conservationStatus: "Vulnerable"
    },
    color: "#a855f7",
    discovered: false
  },
  {
    id: 4,
    name: "Dipterocarp Trail",
    position: { x: -3, y: 0, z: -1 },
    plant: {
      name: "Meranti Tree",
      scientific: "Shorea sp.",
      description: "A tall tropical hardwood tree, part of the dipterocarp family. These trees are crucial for the rainforest ecosystem and are highly valued for timber.",
      facts: [
        "Can live over 100 years",
        "Provides canopy shelter for many species",
        "Seeds have distinctive wing-like structures",
        "Important source of sustainable timber"
      ],
      rarity: "Common",
      habitat: "Tropical rainforests, lowland areas",
      conservationStatus: "Near Threatened"
    },
    color: "#dc2626",
    discovered: false
  },
  {
    id: 5,
    name: "Pitcher Plant Bog",
    position: { x: 3, y: 0, z: -4 },
    plant: {
      name: "Tropical Pitcher Plant",
      scientific: "Nepenthes rafflesiana",
      description: "A fascinating carnivorous plant with modified leaves that form pitcher-shaped traps. These pitchers are filled with digestive fluid to break down insects.",
      facts: [
        "Carnivorous plant that catches insects",
        "Pitchers can hold up to 200ml of water",
        "Endemic to Southeast Asian rainforests",
        "Different pitcher shapes for different prey"
      ],
      rarity: "Rare",
      habitat: "Tropical peat swamps and forests",
      conservationStatus: "Vulnerable"
    },
    color: "#f59e0b",
    discovered: false
  },
  {
    id: 6,
    name: "Strangler Fig Grove",
    position: { x: 1, y: 0, z: -1 },
    plant: {
      name: "Strangler Fig",
      scientific: "Ficus benjamina",
      description: "A remarkable tree that begins life as an epiphyte, eventually growing around and sometimes killing its host tree. It's a keystone species in tropical forests.",
      facts: [
        "Starts life growing on other trees",
        "Can eventually kill the host tree",
        "Provides food for over 1,200 species",
        "Can live for hundreds of years"
      ],
      rarity: "Common",
      habitat: "Tropical rainforests worldwide",
      conservationStatus: "Least Concern"
    },
    color: "#8b5cf6",
    discovered: false
  }
];

export const mockTrails = [
  {
    id: 1,
    name: "Main Trail",
    difficulty: "Easy",
    distance: "2.5 km",
    duration: "1-2 hours",
    checkpoints: [1, 2, 3, 4],
    description: "The main trail loop suitable for all fitness levels"
  },
  {
    id: 2,
    name: "Advanced Trail",
    difficulty: "Moderate",
    distance: "4.2 km",
    duration: "2-3 hours",
    checkpoints: [1, 2, 3, 4, 5, 6],
    description: "Extended trail with more challenging terrain and rare plant discoveries"
  }
];

export const mockUserProgress = {
  checkpointsDiscovered: [],
  totalCheckpoints: mockCheckpoints.length,
  completedTrails: [],
  totalDistance: 0,
  timeSpent: 0,
  plantsCollected: 0,
  achievements: []
};

export const mockAchievements = [
  {
    id: 1,
    name: "First Discovery",
    description: "Discover your first plant checkpoint",
    icon: "🌱",
    unlocked: false
  },
  {
    id: 2,
    name: "Plant Expert",
    description: "Discover 5 different plant species",
    icon: "🌿",
    unlocked: false
  },
  {
    id: 3,
    name: "Rare Collector",
    description: "Find all rare plant species",
    icon: "🌺",
    unlocked: false
  },
  {
    id: 4,
    name: "Trail Master",
    description: "Complete all available trails",
    icon: "🏆",
    unlocked: false
  }
];

export const mockARSettings = {
  cameraEnabled: true,
  soundEnabled: true,
  vibrationEnabled: true,
  showHints: true,
  markerDetectionSensitivity: 0.7,
  renderQuality: 'high'
};