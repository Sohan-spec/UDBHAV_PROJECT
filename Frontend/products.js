// products.js
const PRODUCTS = [
  {
    id: 1,
    name: "Aether Wireless Headphones",
    category: "electronics",
    price: 329,
    rating: 4.7,
    image: "https://picsum.photos/seed/headphones/600/400",
    description: "Premium wireless headphones with adaptive noise cancellation and a sculpted, neutral sound signature.",
    longDescription:
      "Aether Wireless Headphones blend sculpted audio with a soft-touch finish and memory foam ear cushions. With up to 30 hours of playback, adaptive noise cancellation, and intuitive on-ear controls, they are designed for long-listening comfort in any environment.",
    reviews: [
      { user: "Alex", rating: 5, comment: "Incredible detail and separation. Easily rivals my studio pair." },
      { user: "Sam", rating: 4, comment: "Very comfortable — I can wear them all day." }
    ]
  },
  {
    id: 2,
    name: "Silk-Lined Wool Overcoat",
    category: "clothing",
    price: 540,
    rating: 4.8,
    image: "https://picsum.photos/seed/coat/600/400",
    description: "Tailored wool overcoat with silk lining and hidden horn buttons.",
    longDescription:
      "Cut from double-faced Italian wool and finished with a full silk lining, this overcoat drapes cleanly over both tailoring and casual layers. Hidden horn buttons, hand-finished seams, and a subtle collar roll keep the silhouette refined yet understated.",
    reviews: [
      { user: "Jordan", rating: 5, comment: "The drape is flawless. It feels bespoke." },
      { user: "Taylor", rating: 4, comment: "Warm without feeling heavy. Timeless shape." }
    ]
  },
  {
    id: 3,
    name: "Orbit Desk Lamp",
    category: "home",
    price: 189,
    rating: 4.4,
    image: "https://picsum.photos/seed/lamp/600/400",
    description: "Dimmable LED desk lamp with brass accents and a satin finish.",
    longDescription:
      "Orbit Desk Lamp combines a slender stem with a balanced circular head for focused, glare-free light. A brass dimmer dial lets you set the perfect level, while the weighted base keeps the profile minimal yet stable.",
    reviews: [
      { user: "Mara", rating: 4, comment: "Soft, warm light. Perfect for late work sessions." },
      { user: "Elias", rating: 5, comment: "The brass detail feels genuinely premium." }
    ]
  },
  {
    id: 4,
    name: "Mirage Smart Watch",
    category: "electronics",
    price: 410,
    rating: 4.6,
    image: "https://picsum.photos/seed/watch/600/400",
    description: "Minimalist smart watch with sapphire glass and customizable faces.",
    longDescription:
      "Mirage Smart Watch hides a high-resolution display under curved sapphire glass. With health tracking, discreet notifications, and a selection of monochrome faces, it complements tailoring as easily as activewear.",
    reviews: [
      { user: "Noah", rating: 5, comment: "Looks like a dress watch, behaves like a smartwatch." },
      { user: "Lena", rating: 4, comment: "Battery comfortably lasts the week." }
    ]
  },
  {
    id: 5,
    name: "Carbon Fiber Card Holder",
    category: "accessories",
    price: 120,
    rating: 4.3,
    image: "https://picsum.photos/seed/cardholder/600/400",
    description: "Slim carbon fiber card holder with suede interior and RFID shield.",
    longDescription:
      "This ultra-slim card holder pairs carbon fiber outer panels with a soft suede interior. It holds up to eight cards securely while maintaining a pocket-friendly profile, and includes discreet RFID shielding.",
    reviews: [
      { user: "Riley", rating: 4, comment: "Feels weightless in the pocket." },
      { user: "Devon", rating: 4, comment: "The weave catches light beautifully." }
    ]
  },
  {
    id: 6,
    name: "Cashmere Lounge Set",
    category: "clothing",
    price: 365,
    rating: 4.9,
    image: "https://picsum.photos/seed/cashmere/600/400",
    description: "Two-piece cashmere lounge set with relaxed, tailored lines.",
    longDescription:
      "Spun from long-staple cashmere, this lounge set features a gentle taper through the leg and a clean, sculpted crew neckline. Designed for travel and off-duty days when comfort is non-negotiable.",
    reviews: [
      { user: "Isla", rating: 5, comment: "The softest set I own. Worth every cent." },
      { user: "Kai", rating: 5, comment: "Elevates staying in. Beautifully made." }
    ]
  },
  {
    id: 7,
    name: "Echo Wireless Speaker",
    category: "electronics",
    price: 260,
    rating: 4.2,
    image: "https://picsum.photos/seed/speaker/600/400",
    description: "Compact wireless speaker with 360° sound and fabric wrap.",
    longDescription:
      "Echo Wireless Speaker projects 360° sound from a compact, fabric-wrapped column. Tuned for warm, room-filling audio with subtle bass, it connects instantly to your devices and blends quietly into any interior.",
    reviews: [
      { user: "Aria", rating: 4, comment: "Perfect for living-room ambience." },
      { user: "Leo", rating: 4, comment: "Rich, detailed sound for the size." }
    ]
  },
  {
    id: 8,
    name: "Marble Catchall Tray",
    category: "home",
    price: 145,
    rating: 4.5,
    image: "https://picsum.photos/seed/marble/600/400",
    description: "Hand-carved marble tray for keys, watches, and daily essentials.",
    longDescription:
      "Each Marble Catchall Tray is carved from a single block of stone, with gentle bevels and a honed finish. Ideal for entry tables or bedside, it keeps keys, watches, and jewelry quietly contained.",
    reviews: [
      { user: "Sophie", rating: 5, comment: "Heavy, substantial, and beautifully veined." },
      { user: "Owen", rating: 4, comment: "Feels like a gallery object." }
    ]
  },
  {
    id: 9,
    name: "Matte Leather Weekender",
    category: "accessories",
    price: 580,
    rating: 4.8,
    image: "https://picsum.photos/seed/weekender/600/400",
    description: "Matte full-grain leather weekender with hidden shoe compartment.",
    longDescription:
      "Crafted from full-grain leather with a matte, almost paper-like finish, this weekender hides a ventilated shoe compartment and multiple internal pockets. Designed to sit comfortably in overhead cabins.",
    reviews: [
      { user: "Mila", rating: 5, comment: "Looks better with each trip." },
      { user: "Theo", rating: 4, comment: "Thoughtful internal organisation." }
    ]
  },
  {
    id: 10,
    name: "Obsidian Espresso Set",
    category: "home",
    price: 210,
    rating: 4.6,
    image: "https://picsum.photos/seed/espresso/600/400",
    description: "Porcelain espresso set with obsidian glaze and gold detailing.",
    longDescription:
      "The Obsidian Espresso Set includes four porcelain cups and matching saucers finished in a deep black glaze with hand-applied gold rims. The weight and lip curvature have been tuned for an ideal sip.",
    reviews: [
      { user: "Nico", rating: 5, comment: "Makes every coffee feel intentional." },
      { user: "Ada", rating: 4, comment: "The glaze is mesmerizing in daylight." }
    ]
  },
  {
    id: 11,
    name: "Monolith Floor Mirror",
    category: "home",
    price: 720,
    rating: 4.7,
    image: "https://picsum.photos/seed/mirror/600/400",
    description: "Oversized floor mirror with brushed metal frame.",
    longDescription:
      "Monolith Floor Mirror stands nearly two meters tall with a slim brushed metal frame. The low-iron glass delivers a true reflection without green tint, adding depth to any bedroom or hallway.",
    reviews: [
      { user: "Ivy", rating: 5, comment: "Transforms the space instantly." },
      { user: "Jules", rating: 4, comment: "Subtle yet dramatic presence." }
    ]
  },
  {
    id: 12,
    name: "Shadow Frame Sunglasses",
    category: "accessories",
    price: 195,
    rating: 4.3,
    image: "https://picsum.photos/seed/sunglasses/600/400",
    description: "Acetate sunglasses with gradient lenses and sculpted bridge.",
    longDescription:
      "Shadow Frame Sunglasses use a custom acetate blend with a soft, gradient lens. The sculpted bridge and slender arms ensure a secure, barely-there fit that works from city streets to coastal drives.",
    reviews: [
      { user: "Rae", rating: 4, comment: "Lightweight and understated. Exactly what I wanted." },
      { user: "Ethan", rating: 4, comment: "Compliments every outfit I own." }
    ]
  }
];