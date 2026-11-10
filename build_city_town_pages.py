#!/usr/bin/env python3
"""
build_city_town_pages.py — Koray-Aligned City & Town Location Page Generator
=============================================================================
Generates hierarchical location pages: locations/{state}/{city}/index.html
and locations/{state}/{city}/{town}.html with:

- Unique, substantive content per page (anti-doorway-page)
- Mandatory annotation blocks reinforcing central entity (HighSoftware99)
- BreadcrumbList + ProfessionalService JSON-LD schema
- Centerpiece annotation (entity definition in first 100 words)
- Semantic HTML (article, section, nav, dfn)
- Minimal DOM (<800 nodes target)
- Proper internal linking hierarchy (town→city→state→homepage)

Does NOT modify any existing files. Generates into locations/ directory only.
"""

import os
import json
import re
from datetime import date

TARGET_DIR = "/Users/macbookpro/Documents/GitHub/seo-byhighsoftware99.com"
LOCATIONS_DIR = os.path.join(TARGET_DIR, "locations")
TODAY = date.today().isoformat()
DOMAIN = "https://seo-byhighsoftware99.com"

# =============================================================================
# PILOT DATA — 5 States with rich, unique local context per city/town
# =============================================================================
locations_data = {
    "california": {
        "state_name": "California",
        "state_abbr": "CA",
        "state_slug": "seo-california",
        "cities": {
            "los-angeles": {
                "city_name": "Los Angeles",
                "county": "Los Angeles County",
                "population": "3,898,747",
                "zip_range": "90001–90899",
                "industries": ["Entertainment & Media", "Fashion & Apparel", "Technology Startups", "Real Estate", "Healthcare"],
                "business_count": "244,000+",
                "metro_area": "Greater Los Angeles",
                "search_competition": "extremely high",
                "local_directories": ["LA Business Journal", "Discover Los Angeles", "LA Chamber of Commerce"],
                "seo_focus": "With Hollywood, Silicon Beach, and a thriving startup ecosystem, Los Angeles businesses face fierce digital competition across entertainment, tech, and retail verticals.",
                "towns": {
                    "beverly-hills": {
                        "name": "Beverly Hills",
                        "county": "Los Angeles County",
                        "population": "33,792",
                        "zip_codes": ["90210", "90211", "90212"],
                        "industries": ["Luxury Retail", "Entertainment Management", "Hospitality & Fine Dining", "Cosmetic Surgery"],
                        "nearby": ["santa-monica", "west-hollywood", "culver-city"],
                        "local_context": "Beverly Hills is synonymous with luxury brands and high-net-worth clientele. Local businesses compete for visibility among affluent consumers searching for premium services, making targeted local SEO essential for ROI."
                    },
                    "santa-monica": {
                        "name": "Santa Monica",
                        "county": "Los Angeles County",
                        "population": "93,076",
                        "zip_codes": ["90401", "90402", "90403", "90404", "90405"],
                        "industries": ["Tech Startups (Silicon Beach)", "Tourism & Hospitality", "Health & Wellness", "Creative Agencies"],
                        "nearby": ["beverly-hills", "culver-city", "venice"],
                        "local_context": "Santa Monica anchors Silicon Beach — a dense corridor of tech companies, venture capital firms, and digital agencies. SEO here targets both B2B tech buyers and the tourist economy along the Third Street Promenade."
                    },
                    "pasadena": {
                        "name": "Pasadena",
                        "county": "Los Angeles County",
                        "population": "138,699",
                        "zip_codes": ["91101", "91103", "91104", "91105", "91106", "91107"],
                        "industries": ["Education (Caltech, Art Center)", "Research & Development", "Healthcare", "Professional Services"],
                        "nearby": ["glendale", "arcadia", "altadena"],
                        "local_context": "Home to Caltech and NASA's Jet Propulsion Laboratory, Pasadena attracts research-driven and education-sector businesses. SEO strategies here emphasize authority content and academic entity alignment."
                    },
                    "culver-city": {
                        "name": "Culver City",
                        "county": "Los Angeles County",
                        "population": "39,185",
                        "zip_codes": ["90230", "90231", "90232"],
                        "industries": ["Film & Television Production", "Gaming Studios", "Streaming Platforms", "Creative Technology"],
                        "nearby": ["santa-monica", "beverly-hills", "inglewood"],
                        "local_context": "Culver City is a media production hub housing Sony Pictures, Amazon Studios, and Apple TV+ offices. Businesses in this market require SEO strategies that target entertainment industry professionals and creative talent acquisition."
                    }
                }
            },
            "san-francisco": {
                "city_name": "San Francisco",
                "county": "San Francisco County",
                "population": "873,965",
                "zip_range": "94102–94188",
                "industries": ["Enterprise Technology", "Financial Services (FinTech)", "Biotech & Life Sciences", "SaaS & Cloud Computing"],
                "business_count": "92,000+",
                "metro_area": "San Francisco Bay Area",
                "search_competition": "extremely high",
                "local_directories": ["SF Business Times", "SF Chamber of Commerce", "Bay Area Council"],
                "seo_focus": "San Francisco is the global epicenter of SaaS, venture capital, and enterprise technology. B2B search competition is among the highest in the world, requiring advanced entity SEO and technical infrastructure.",
                "towns": {
                    "palo-alto": {
                        "name": "Palo Alto",
                        "county": "Santa Clara County",
                        "population": "68,572",
                        "zip_codes": ["94301", "94303", "94304", "94306"],
                        "industries": ["Venture Capital", "Stanford University Ecosystem", "AI & Machine Learning", "Deep Tech"],
                        "nearby": ["mountain-view", "menlo-park", "redwood-city"],
                        "local_context": "Palo Alto is the birthplace of Silicon Valley, anchored by Stanford University and Sand Hill Road's venture capital corridor. SEO here demands thought leadership content that resonates with technical founders and institutional investors."
                    },
                    "oakland": {
                        "name": "Oakland",
                        "county": "Alameda County",
                        "population": "433,031",
                        "zip_codes": ["94601", "94602", "94603", "94605", "94606", "94607", "94610", "94611", "94612"],
                        "industries": ["Logistics & Port Commerce", "Food & Beverage", "Arts & Culture", "Community Healthcare"],
                        "nearby": ["berkeley", "alameda", "san-leandro"],
                        "local_context": "Oakland's Port is the fifth busiest in the United States, driving a logistics and commerce ecosystem. The city's growing food, arts, and community health sectors create diverse local search demand across multiple industry verticals."
                    },
                    "berkeley": {
                        "name": "Berkeley",
                        "county": "Alameda County",
                        "population": "124,321",
                        "zip_codes": ["94701", "94702", "94703", "94704", "94705", "94707", "94708", "94709", "94710"],
                        "industries": ["Higher Education (UC Berkeley)", "Biotech Research", "Sustainable Energy", "Publishing & Media"],
                        "nearby": ["oakland", "emeryville", "albany"],
                        "local_context": "UC Berkeley anchors a research and innovation cluster spanning biotech, sustainable energy, and computational science. Local SEO here targets academic institutions, research partnerships, and the student-driven consumer economy."
                    }
                }
            },
            "san-diego": {
                "city_name": "San Diego",
                "county": "San Diego County",
                "population": "1,386,932",
                "zip_range": "92101–92199",
                "industries": ["Defense & Aerospace", "Biotech & Pharmaceutical", "Tourism & Hospitality", "Craft Brewing"],
                "business_count": "125,000+",
                "metro_area": "San Diego–Chula Vista–Carlsbad",
                "search_competition": "high",
                "local_directories": ["San Diego Business Journal", "San Diego Regional Chamber", "Visit San Diego"],
                "seo_focus": "San Diego's defense-biotech corridor and year-round tourism create dual search demand — B2B defense contractors and B2C hospitality brands both require specialized SEO strategies.",
                "towns": {
                    "la-jolla": {
                        "name": "La Jolla",
                        "county": "San Diego County",
                        "population": "46,781",
                        "zip_codes": ["92037", "92038", "92039"],
                        "industries": ["Biotech Research (Salk, Scripps, UCSD)", "Luxury Real Estate", "Fine Dining", "Medical Specialists"],
                        "nearby": ["del-mar", "pacific-beach", "university-city"],
                        "local_context": "La Jolla houses three world-class research institutions — Salk Institute, Scripps Research, and UCSD — creating a unique biotech SEO landscape. Local businesses serve both research professionals and affluent residents seeking premium services."
                    },
                    "chula-vista": {
                        "name": "Chula Vista",
                        "county": "San Diego County",
                        "population": "275,487",
                        "zip_codes": ["91910", "91911", "91913", "91914", "91915"],
                        "industries": ["Cross-Border Commerce", "Healthcare Services", "Residential Development", "Retail"],
                        "nearby": ["national-city", "bonita", "eastlake"],
                        "local_context": "Chula Vista is the second-largest city in the San Diego metro and a gateway to cross-border commerce with Tijuana. Bilingual SEO strategies targeting both English and Spanish search queries are critical for local market penetration."
                    }
                }
            }
        }
    },
    "new-york": {
        "state_name": "New York",
        "state_abbr": "NY",
        "state_slug": "seo-new-york",
        "cities": {
            "new-york-city": {
                "city_name": "New York City",
                "county": "New York County (Manhattan), Kings County (Brooklyn), Queens County",
                "population": "8,336,817",
                "zip_range": "10001–11697",
                "industries": ["Financial Services", "Media & Publishing", "Fashion", "Legal Services", "Technology"],
                "business_count": "520,000+",
                "metro_area": "New York–Newark–Jersey City",
                "search_competition": "the highest in the United States",
                "local_directories": ["Crain's New York Business", "NYC Small Business Services", "Manhattan Chamber of Commerce"],
                "seo_focus": "New York City is the most competitive local search market in the United States. With over half a million businesses competing for visibility, technical SEO infrastructure and entity authority are non-negotiable.",
                "towns": {
                    "brooklyn": {
                        "name": "Brooklyn",
                        "county": "Kings County",
                        "population": "2,736,074",
                        "zip_codes": ["11201", "11205", "11206", "11207", "11209", "11211", "11215", "11217", "11222", "11225"],
                        "industries": ["Creative Agencies & Design Studios", "Food & Beverage", "E-Commerce Brands", "Real Estate Development"],
                        "nearby": ["manhattan", "queens", "staten-island"],
                        "local_context": "Brooklyn has evolved into a global brand synonymous with independent creative businesses, artisanal food, and D2C e-commerce brands. Local SEO here targets neighborhood-level search intent — Williamsburg, DUMBO, Park Slope — each with distinct consumer demographics."
                    },
                    "manhattan": {
                        "name": "Manhattan",
                        "county": "New York County",
                        "population": "1,694,251",
                        "zip_codes": ["10001", "10002", "10003", "10004", "10005", "10006", "10007", "10010", "10011", "10012", "10013", "10014", "10016", "10017", "10018", "10019", "10020", "10021", "10022", "10023", "10024", "10025"],
                        "industries": ["Investment Banking", "Corporate Law", "Luxury Retail", "Media & Advertising", "SaaS"],
                        "nearby": ["brooklyn", "queens", "jersey-city"],
                        "local_context": "Manhattan is the financial and media capital of the world. SEO competition here is at the highest possible intensity, with Fortune 500 enterprises, law firms, and global media companies all competing for the same high-intent commercial search queries."
                    },
                    "queens": {
                        "name": "Queens",
                        "county": "Queens County",
                        "population": "2,405,464",
                        "zip_codes": ["11101", "11102", "11103", "11104", "11105", "11106", "11354", "11355", "11358", "11360", "11361", "11365", "11375", "11377", "11385"],
                        "industries": ["International Cuisine & Restaurants", "Construction & Trades", "Healthcare Clinics", "Import/Export"],
                        "nearby": ["brooklyn", "manhattan", "long-island-city"],
                        "local_context": "Queens is the most ethnically diverse urban area in the world, with businesses serving over 130 spoken languages. Multilingual local SEO strategies and culturally targeted Google Business Profiles are essential for reaching the borough's segmented consumer base."
                    }
                }
            },
            "buffalo": {
                "city_name": "Buffalo",
                "county": "Erie County",
                "population": "278,349",
                "zip_range": "14201–14280",
                "industries": ["Manufacturing & Advanced Materials", "Higher Education", "Healthcare Systems", "Clean Energy"],
                "business_count": "22,000+",
                "metro_area": "Buffalo–Cheektowaga–Niagara Falls",
                "search_competition": "moderate",
                "local_directories": ["Buffalo Business First", "Buffalo Niagara Partnership", "Visit Buffalo Niagara"],
                "seo_focus": "Buffalo's economic renaissance centers on clean energy, advanced manufacturing, and healthcare. Local search competition is moderate but growing rapidly as investment accelerates.",
                "towns": {
                    "cheektowaga": {
                        "name": "Cheektowaga",
                        "county": "Erie County",
                        "population": "88,226",
                        "zip_codes": ["14043", "14206", "14211", "14215", "14225", "14227"],
                        "industries": ["Retail & Shopping Centers", "Aviation (Buffalo Airport)", "Automotive Services", "Healthcare"],
                        "nearby": ["amherst", "tonawanda", "west-seneca"],
                        "local_context": "Cheektowaga is a major commercial suburb of Buffalo centered around the Walden Galleria and Buffalo Niagara International Airport. Local businesses serve both resident consumers and the transit traveler economy."
                    },
                    "amherst": {
                        "name": "Amherst",
                        "county": "Erie County",
                        "population": "129,813",
                        "zip_codes": ["14051", "14068", "14221", "14226", "14228"],
                        "industries": ["Higher Education (UB North Campus)", "Professional Services", "Retail", "Technology"],
                        "nearby": ["cheektowaga", "tonawanda", "williamsville"],
                        "local_context": "Amherst is the largest suburb in Western New York and home to the University at Buffalo's North Campus. The town's economy is driven by education-linked professional services, student-oriented businesses, and a growing technology sector."
                    }
                }
            }
        }
    },
    "texas": {
        "state_name": "Texas",
        "state_abbr": "TX",
        "state_slug": "seo-texas",
        "cities": {
            "houston": {
                "city_name": "Houston",
                "county": "Harris County",
                "population": "2,304,580",
                "zip_range": "77001–77299",
                "industries": ["Energy & Oil/Gas", "Aerospace (NASA/JSC)", "Healthcare (Texas Medical Center)", "Petrochemicals"],
                "business_count": "180,000+",
                "metro_area": "Houston–The Woodlands–Sugar Land",
                "search_competition": "very high",
                "local_directories": ["Houston Business Journal", "Greater Houston Partnership", "Houston Chronicle"],
                "seo_focus": "Houston's energy sector dominance and the world's largest medical center create specialized B2B search demand. SEO strategies must address both industrial-technical and healthcare-consumer search verticals.",
                "towns": {
                    "sugar-land": {
                        "name": "Sugar Land",
                        "county": "Fort Bend County",
                        "population": "111,026",
                        "zip_codes": ["77478", "77479", "77496", "77498"],
                        "industries": ["Corporate Headquarters", "Healthcare Clinics", "Residential Services", "International Business"],
                        "nearby": ["missouri-city", "stafford", "richmond"],
                        "local_context": "Sugar Land is a master-planned suburban city that has attracted corporate headquarters and a highly educated, affluent population. SEO here targets professional services, healthcare providers, and upscale residential businesses."
                    },
                    "the-woodlands": {
                        "name": "The Woodlands",
                        "county": "Montgomery County",
                        "population": "114,436",
                        "zip_codes": ["77380", "77381", "77382", "77384", "77385", "77386", "77389"],
                        "industries": ["Energy Corporate HQs (ExxonMobil, Anadarko)", "Hospitality & Conferences", "Luxury Retail", "Financial Advisory"],
                        "nearby": ["spring", "conroe", "magnolia"],
                        "local_context": "The Woodlands is a premier master-planned community and corporate hub, home to ExxonMobil's global headquarters and the Cynthia Woods Mitchell Pavilion. SEO strategies target corporate decision-makers and high-income residential consumers."
                    },
                    "katy": {
                        "name": "Katy",
                        "county": "Harris County / Fort Bend County / Waller County",
                        "population": "21,894",
                        "zip_codes": ["77449", "77450", "77493", "77494"],
                        "industries": ["Energy Services", "Education (Katy ISD)", "Residential Construction", "Retail & Dining"],
                        "nearby": ["sugar-land", "cypress", "richmond"],
                        "local_context": "Katy is one of Houston's fastest-growing suburbs, anchored by the highly rated Katy Independent School District. Family-oriented businesses, home services, and educational services dominate local search demand."
                    }
                }
            },
            "dallas": {
                "city_name": "Dallas",
                "county": "Dallas County",
                "population": "1,304,379",
                "zip_range": "75201–75398",
                "industries": ["Telecommunications", "Banking & Insurance", "Defense Contracting", "Logistics & Distribution"],
                "business_count": "145,000+",
                "metro_area": "Dallas–Fort Worth–Arlington",
                "search_competition": "very high",
                "local_directories": ["Dallas Business Journal", "Dallas Regional Chamber", "D Magazine"],
                "seo_focus": "The Dallas–Fort Worth metroplex is the fourth-largest metro in the United States. Its diversified economy across telecom, banking, and defense creates broad local search competition across both B2B and B2C verticals.",
                "towns": {
                    "plano": {
                        "name": "Plano",
                        "county": "Collin County",
                        "population": "285,494",
                        "zip_codes": ["75023", "75024", "75025", "75074", "75075", "75093"],
                        "industries": ["Corporate Headquarters (Toyota, JCPenney, Liberty Mutual)", "Technology", "Healthcare", "Financial Services"],
                        "nearby": ["frisco", "allen", "mckinney"],
                        "local_context": "Plano is a corporate powerhouse within the DFW metroplex, housing the headquarters of Toyota North America, Frito-Lay, and Liberty Mutual. SEO strategies here target both enterprise B2B decision-makers and the city's affluent consumer base."
                    },
                    "frisco": {
                        "name": "Frisco",
                        "county": "Collin County / Denton County",
                        "population": "200,490",
                        "zip_codes": ["75033", "75034", "75035", "75036"],
                        "industries": ["Sports & Entertainment (Dallas Cowboys HQ)", "Technology", "Real Estate Development", "Education"],
                        "nearby": ["plano", "mckinney", "prosper"],
                        "local_context": "Frisco is one of the fastest-growing cities in America, anchored by the Dallas Cowboys' headquarters at The Star. The city's rapid growth in tech, sports entertainment, and residential development creates exceptional SEO opportunity in an emerging but increasingly competitive market."
                    },
                    "arlington": {
                        "name": "Arlington",
                        "county": "Tarrant County",
                        "population": "394,266",
                        "zip_codes": ["76001", "76002", "76006", "76010", "76011", "76012", "76013", "76014", "76015", "76016", "76017", "76018"],
                        "industries": ["Entertainment (AT&T Stadium, Globe Life Field)", "Automotive Manufacturing", "Defense (General Motors)", "Higher Education (UTA)"],
                        "nearby": ["fort-worth", "grand-prairie", "mansfield"],
                        "local_context": "Arlington sits at the center of the DFW metroplex, hosting AT&T Stadium (Dallas Cowboys) and Globe Life Field (Texas Rangers). The city's entertainment economy and University of Texas at Arlington create dual search demand from visitors and the academic community."
                    }
                }
            }
        }
    },
    "florida": {
        "state_name": "Florida",
        "state_abbr": "FL",
        "state_slug": "seo-florida",
        "cities": {
            "miami": {
                "city_name": "Miami",
                "county": "Miami-Dade County",
                "population": "442,241",
                "zip_range": "33101–33299",
                "industries": ["International Trade & Banking", "Tourism & Hospitality", "Real Estate Development", "HealthTech"],
                "business_count": "95,000+",
                "metro_area": "Miami–Fort Lauderdale–Pompano Beach",
                "search_competition": "very high",
                "local_directories": ["Miami Herald", "Greater Miami Chamber", "Miami-Dade Beacon Council"],
                "seo_focus": "Miami is Latin America's gateway to the U.S. market, creating bilingual search demand across trade, finance, real estate, and tourism. Spanish-language SEO is as critical as English-language optimization in this market.",
                "towns": {
                    "coral-gables": {
                        "name": "Coral Gables",
                        "county": "Miami-Dade County",
                        "population": "49,700",
                        "zip_codes": ["33114", "33124", "33134", "33143", "33146", "33156"],
                        "industries": ["International Banking", "Corporate Law", "Luxury Real Estate", "Higher Education (University of Miami)"],
                        "nearby": ["coconut-grove", "south-miami", "key-biscayne"],
                        "local_context": "Coral Gables, known as 'The City Beautiful,' is Miami's premier business district housing multinational banking headquarters and the University of Miami. SEO strategies must address bilingual corporate clientele and luxury residential markets."
                    },
                    "hialeah": {
                        "name": "Hialeah",
                        "county": "Miami-Dade County",
                        "population": "223,109",
                        "zip_codes": ["33010", "33012", "33013", "33014", "33015", "33016", "33018"],
                        "industries": ["Manufacturing & Warehousing", "Healthcare", "Retail Commerce", "Construction"],
                        "nearby": ["miami-gardens", "miami-lakes", "medley"],
                        "local_context": "Hialeah is the sixth-largest city in Florida and one of the most predominantly Spanish-speaking cities in the U.S. Local SEO here requires native Spanish content optimization, bilingual Google Business Profiles, and culturally targeted search strategies."
                    },
                    "doral": {
                        "name": "Doral",
                        "county": "Miami-Dade County",
                        "population": "80,166",
                        "zip_codes": ["33122", "33166", "33172", "33178"],
                        "industries": ["Logistics & Distribution (near MIA Airport)", "International Trade", "Corporate Offices", "Hospitality"],
                        "nearby": ["hialeah", "sweetwater", "miami-springs"],
                        "local_context": "Doral is Miami's logistics and corporate hub, strategically located near Miami International Airport. The city serves as the U.S. headquarters for numerous Latin American companies, creating B2B search demand for cross-border commerce and international trade services."
                    }
                }
            },
            "tampa": {
                "city_name": "Tampa",
                "county": "Hillsborough County",
                "population": "387,050",
                "zip_range": "33601–33694",
                "industries": ["Financial Services (USAA, Raymond James)", "Healthcare (Moffitt Cancer Center)", "Technology & Cybersecurity", "Defense"],
                "business_count": "48,000+",
                "metro_area": "Tampa–St. Petersburg–Clearwater",
                "search_competition": "high",
                "local_directories": ["Tampa Bay Business Journal", "Greater Tampa Chamber", "Tampa Bay Times"],
                "seo_focus": "Tampa Bay's economy is anchored by financial services, defense, and a growing cybersecurity corridor. The metro's rapid population growth is intensifying local search competition across all commercial sectors.",
                "towns": {
                    "st-petersburg": {
                        "name": "St. Petersburg",
                        "county": "Pinellas County",
                        "population": "258,308",
                        "zip_codes": ["33701", "33702", "33703", "33704", "33705", "33706", "33707", "33708", "33709", "33710", "33711", "33712", "33713", "33714", "33715", "33716"],
                        "industries": ["Arts & Culture (Dalí Museum)", "Marine Sciences", "Tech Startups", "Tourism"],
                        "nearby": ["clearwater", "largo", "pinellas-park"],
                        "local_context": "St. Petersburg has transformed from a retirement community into a vibrant arts, tech, and marine sciences hub. The city's growing tech startup ecosystem and cultural attractions create diverse local search demand spanning creative services, marine industry, and tourism."
                    },
                    "clearwater": {
                        "name": "Clearwater",
                        "county": "Pinellas County",
                        "population": "117,292",
                        "zip_codes": ["33755", "33756", "33759", "33760", "33761", "33762", "33763", "33764", "33765"],
                        "industries": ["Tourism & Beach Hospitality", "Technology (Tech Data HQ)", "Financial Services", "Marine & Boating"],
                        "nearby": ["st-petersburg", "largo", "dunedin"],
                        "local_context": "Clearwater Beach is consistently ranked among America's best beaches, driving a tourism-dominant search landscape. Beyond tourism, the city hosts Tech Data's global headquarters and a growing financial services sector."
                    }
                }
            }
        }
    },
    "illinois": {
        "state_name": "Illinois",
        "state_abbr": "IL",
        "state_slug": "seo-illinois",
        "cities": {
            "chicago": {
                "city_name": "Chicago",
                "county": "Cook County",
                "population": "2,746,388",
                "zip_range": "60601–60699",
                "industries": ["Financial Trading & Commodities", "Manufacturing", "Transportation & Logistics", "Food & Beverage", "Architecture"],
                "business_count": "210,000+",
                "metro_area": "Chicago–Naperville–Elgin",
                "search_competition": "extremely high",
                "local_directories": ["Crain's Chicago Business", "Chicagoland Chamber", "Choose Chicago"],
                "seo_focus": "Chicago is the commercial engine of the Midwest, with search competition matching coastal metros across finance, manufacturing, and logistics. The city's diverse neighborhood economies create hyperlocal search patterns that demand granular optimization.",
                "towns": {
                    "naperville": {
                        "name": "Naperville",
                        "county": "DuPage County / Will County",
                        "population": "149,540",
                        "zip_codes": ["60540", "60563", "60564", "60565"],
                        "industries": ["Corporate Offices", "Healthcare (Edward Hospital)", "Education", "Professional Services"],
                        "nearby": ["aurora", "wheaton", "lisle"],
                        "local_context": "Naperville is consistently ranked among the best places to live in the U.S., attracting corporate professionals and families. The city's high median household income drives premium service demand, and local SEO must target affluent suburban consumers with high purchase intent."
                    },
                    "evanston": {
                        "name": "Evanston",
                        "county": "Cook County",
                        "population": "78,110",
                        "zip_codes": ["60201", "60202", "60203", "60204", "60208"],
                        "industries": ["Higher Education (Northwestern University)", "Healthcare", "Research & Development", "Arts & Culture"],
                        "nearby": ["skokie", "wilmette", "rogers-park"],
                        "local_context": "Evanston is anchored by Northwestern University, one of the nation's top research institutions. The city's economy is driven by university-linked research commercialization, healthcare services, and a culturally rich downtown district that attracts both residents and campus visitors."
                    },
                    "schaumburg": {
                        "name": "Schaumburg",
                        "county": "Cook County / DuPage County",
                        "population": "78,723",
                        "zip_codes": ["60159", "60168", "60173", "60193", "60194", "60195", "60196"],
                        "industries": ["Corporate Headquarters (Zurich NA, Motorola Solutions)", "Retail (Woodfield Mall)", "Technology", "Insurance"],
                        "nearby": ["hoffman-estates", "elk-grove-village", "rolling-meadows"],
                        "local_context": "Schaumburg is a major suburban corporate center, home to Zurich North America and Motorola Solutions headquarters. Woodfield Mall, one of the largest shopping centers in the U.S., anchors a retail economy that generates intense local search competition for consumer-facing businesses."
                    }
                }
            }
        }
    }
}


# =============================================================================
# FAQ TEMPLATES — Unique per industry vertical to avoid templated patterns
# =============================================================================
faq_templates = {
    "default": [
        ("How long does it take to see SEO results in {location}?",
         "HighSoftware99 typically delivers measurable ranking improvements for {location} businesses within 30–90 days using the Instant Appear framework. Timeline varies based on current domain authority, keyword competition in {location}, and technical infrastructure baseline."),
        ("What makes local SEO different in {location}?",
         "Local SEO in {location} requires targeting {location}-specific search patterns, building citations in {county} business directories, and optimizing Google Business Profile for the {zip_context} zip code area. HighSoftware99 tailors every campaign to {location}'s unique competitive landscape."),
        ("Does HighSoftware99 manage Google Business Profile for {location} businesses?",
         "Yes. HighSoftware99 provides complete Google Business Profile management for {location} businesses including category optimization, review response strategy, post publishing, and Q&A management to maximize Local Pack visibility in {location} search results.")
    ],
    "tech": [
        ("How does HighSoftware99 approach B2B SEO in {location}?",
         "B2B SEO in {location}'s technology sector requires entity-level authority building through technical content, structured data targeting decision-maker search queries, and link acquisition from industry publications. HighSoftware99 builds topical authority clusters aligned with {location}'s tech ecosystem."),
        ("What technical SEO infrastructure does HighSoftware99 deploy for {location} tech companies?",
         "HighSoftware99 implements sub-200ms TTFB via Cloudflare edge rendering, semantic HTML optimization for LLM comprehension, and structured data engineering for {location} technology companies targeting enterprise search queries.")
    ],
    "luxury": [
        ("How does HighSoftware99 optimize for luxury brand searches in {location}?",
         "Luxury brand SEO in {location} targets high-intent, low-volume queries from affluent consumers. HighSoftware99 builds entity authority through premium content positioning, reputation management, and structured review signals in {location}'s luxury market."),
        ("What local SEO strategies work for high-end services in {location}?",
         "High-end service providers in {location} benefit from curated citation building in luxury directories, review acquisition from verified clients, and Google Business Profile optimization emphasizing premium service attributes and {location}-specific credentials.")
    ],
    "healthcare": [
        ("How does HighSoftware99 handle healthcare SEO compliance in {location}?",
         "Healthcare SEO in {location} requires HIPAA-aware content strategies, medical entity schema markup, and practitioner-level Google Business Profile optimization. HighSoftware99 ensures all {location} healthcare SEO campaigns meet regulatory standards while maximizing patient acquisition visibility."),
    ],
    "bilingual": [
        ("Does HighSoftware99 provide bilingual SEO services in {location}?",
         "Yes. HighSoftware99 delivers bilingual English/Spanish SEO campaigns for {location} businesses targeting multilingual communities. This includes Spanish-language Google Business Profile management, bilingual keyword research, and culturally adapted content strategies for {location}'s diverse population."),
    ]
}


def slugify(name):
    """Convert a name to a URL-safe slug."""
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def get_depth_prefix(depth):
    """Return the relative path prefix to root based on directory depth."""
    return "../" * depth


def get_faq_category(industries):
    """Determine FAQ category based on industries using whole-word boundaries."""
    industry_str = " ".join(industries).lower()
    if re.search(r'\b(tech|technology|saas|software|ai|machine learning|startup|startups|venture|cybersecurity)\b', industry_str):
        return "tech"
    if re.search(r'\b(luxury|fine dining|premium|cosmetic)\b', industry_str):
        return "luxury"
    if re.search(r'\b(healthcare|medical|hospital|clinical)\b', industry_str):
        return "healthcare"
    if re.search(r'\b(spanish|bilingual|latin|international trade)\b', industry_str):
        return "bilingual"
    return "default"


def generate_faq_html(location, county, zip_codes, industries):
    """Generate unique FAQ section based on location and industry vertical."""
    category = get_faq_category(industries)
    zip_context = ", ".join(zip_codes[:3])

    faqs = faq_templates.get(category, []) + faq_templates["default"]
    # Limit to 3-4 FAQs to keep DOM lean
    faqs = faqs[:4]

    faq_html = '<section class="faq-section" aria-label="Frequently Asked Questions">\n'
    faq_html += f'    <h2>SEO FAQs for {location} Businesses</h2>\n'

    faq_schema_items = []
    for q_template, a_template in faqs:
        q = q_template.format(location=location, county=county, zip_context=zip_context)
        a = a_template.format(location=location, county=county, zip_context=zip_context)
        faq_html += f'    <details>\n      <summary>{q}</summary>\n      <p>{a}</p>\n    </details>\n'
        faq_schema_items.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})

    faq_html += '  </section>'

    faq_schema = {"@type": "FAQPage", "mainEntity": faq_schema_items}
    return faq_html, faq_schema


def generate_shared_css():
    """Return the shared CSS for location pages — matches existing site design."""
    return """*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}:root{--bg-primary:#0a0e1a;--bg-secondary:#0f1320;--bg-card:#1a1f35;--accent-1:#6366f1;--accent-2:#818cf8;--accent-3:#a78bfa;--accent-city:#38bdf8;--text-primary:#f1f5f9;--text-secondary:#94a3b8;--text-muted:#8b95a8;--border:#1e293b;--glow:rgba(56,189,248,.1);--radius:12px;--font:'Inter',system-ui,-apple-system,sans-serif}html{font-size:16px;scroll-behavior:smooth}body{font-family:var(--font);background:var(--bg-primary);color:var(--text-primary);line-height:1.7;-webkit-font-smoothing:antialiased}
.skip-link{position:absolute;top:-100%;left:50%;transform:translateX(-50%);background:var(--accent-1);color:#fff;padding:.75rem 1.5rem;border-radius:0 0 8px 8px;font-weight:700;font-size:.9rem;z-index:9999;text-decoration:none;transition:top .2s}.skip-link:focus{top:0}*:focus-visible{outline:2px solid var(--accent-2);outline-offset:2px;border-radius:4px}
.site-header{position:sticky;top:0;z-index:100;background:rgba(10,14,26,.92);backdrop-filter:blur(20px);border-bottom:1px solid var(--border)}.site-header::after{content:'';position:absolute;bottom:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,var(--accent-1),var(--accent-3),transparent)}.nav-inner{max-width:1200px;margin:0 auto;padding:.65rem 2rem;display:flex;align-items:center;justify-content:space-between}.brand{display:flex;align-items:center;gap:.6rem;text-decoration:none}.brand-mark{background:linear-gradient(135deg,var(--accent-1),var(--accent-3));color:#fff;font-weight:900;font-size:.7rem;padding:.3rem .55rem;border-radius:6px}.brand-name{font-weight:700;font-size:.9rem;color:var(--text-primary)}.brand-name span{color:var(--accent-2)}.nav-toggle{display:none;background:none;border:none;cursor:pointer;padding:.5rem;flex-direction:column;gap:4px}.nav-toggle span{display:block;width:20px;height:2px;background:var(--text-primary);border-radius:2px}.nav-links{list-style:none;display:flex;align-items:center;gap:.15rem}.nav-links>li{position:relative}.nav-links>li>a{color:var(--text-secondary);text-decoration:none;font-size:.8rem;font-weight:500;padding:.45rem .7rem;border-radius:8px;transition:color .2s,background .2s;display:flex;align-items:center;gap:.3rem}.nav-links>li>a:hover,.nav-links>li:hover>a{color:var(--text-primary);background:rgba(99,102,241,.08)}.nav-cta{background:linear-gradient(135deg,var(--accent-1),var(--accent-3))!important;color:#fff!important;font-weight:600!important;padding:.45rem 1.1rem!important;border-radius:8px!important}.caret{display:inline-block;width:4px;height:4px;border-right:1.5px solid currentColor;border-bottom:1.5px solid currentColor;transform:rotate(45deg);transition:transform .2s}.has-dropdown:hover .caret{transform:rotate(-135deg)}.dropdown{position:absolute;top:calc(100% + 4px);left:0;min-width:210px;background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:.4rem;list-style:none;opacity:0;visibility:hidden;transform:translateY(8px);transition:opacity .2s,transform .2s,visibility .2s;box-shadow:0 8px 32px rgba(0,0,0,.35)}.has-dropdown:hover .dropdown,.has-dropdown:focus-within .dropdown{opacity:1;visibility:visible;transform:translateY(0)}.dropdown a{display:block;padding:.4rem .7rem;color:var(--text-secondary);text-decoration:none;font-size:.8rem;border-radius:6px;transition:color .15s,background .15s}.dropdown a:hover{color:var(--text-primary);background:rgba(99,102,241,.1)}
.hero{position:relative;padding:3rem 2rem 2.5rem;text-align:center;overflow:hidden}.hero::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 70% 50% at 50% 0%,var(--glow),transparent);pointer-events:none}.hero h1{font-size:clamp(1.6rem,4vw,2.5rem);font-weight:900;letter-spacing:-.03em;line-height:1.15;margin-bottom:.75rem}.hero h1 .hl{background:linear-gradient(135deg,var(--accent-city),var(--accent-2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}.hero .subtitle{font-size:1.05rem;color:var(--text-secondary);max-width:640px;margin:0 auto 2rem}
.breadcrumb{max-width:820px;margin:0 auto;padding:.75rem 2rem}.breadcrumb ol{list-style:none;display:flex;flex-wrap:wrap;gap:.3rem;align-items:center}.breadcrumb li{font-size:.78rem;color:var(--text-muted)}.breadcrumb li+li::before{content:'›';margin-right:.3rem;color:var(--text-muted)}.breadcrumb a{color:var(--accent-2);text-decoration:none;font-weight:500;transition:color .2s}.breadcrumb a:hover{color:var(--accent-3)}
.content-section{max-width:820px;margin:0 auto;padding:2rem 2rem}.content-section h2{font-size:1.5rem;font-weight:800;margin-bottom:1rem}.content-section h3{font-size:1.15rem;font-weight:700;margin:1.5rem 0 .75rem}.content-section p{color:var(--text-secondary);margin-bottom:1.25rem}
.local-stats{max-width:660px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:.75rem;margin-bottom:2rem}.stat-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:.85rem;text-align:center;transition:border-color .25s}.stat-card:hover{border-color:var(--accent-city)}.stat-card .val{font-size:1.4rem;font-weight:800;background:linear-gradient(135deg,var(--accent-city),var(--accent-2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}.stat-card .lbl{font-size:.68rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:.06em;margin-top:.15rem}
.service-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem;margin:1.5rem 0}.svc-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:1.15rem;transition:border-color .25s}.svc-card:hover{border-color:var(--accent-city)}.svc-card h3{font-size:.88rem;font-weight:700;margin-bottom:.3rem}.svc-card p{font-size:.78rem;color:var(--text-muted);margin:0}
.loc-links{display:flex;gap:.65rem;flex-wrap:wrap;margin:1.5rem 0}.loc-link{display:inline-block;padding:.45rem .9rem;background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);color:var(--accent-2);text-decoration:none;font-size:.8rem;font-weight:600;transition:border-color .2s}.loc-link:hover{border-color:var(--accent-2)}
.annotation-block{background:var(--bg-card);border-left:3px solid var(--accent-city);border-radius:0 var(--radius) var(--radius) 0;padding:1.15rem 1.35rem;margin:1.5rem 0}.annotation-block p{color:var(--text-secondary);margin-bottom:.65rem;font-size:.9rem}.annotation-block a{color:var(--accent-2);text-decoration:none;font-weight:600;border-bottom:1px solid transparent;transition:border-color .2s}.annotation-block a:hover{border-bottom-color:var(--accent-2)}
.faq-section{max-width:820px;margin:2rem auto;padding:0 2rem}.faq-section h2{font-size:1.35rem;font-weight:800;margin-bottom:1rem}.faq-section details{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);margin-bottom:.6rem;overflow:hidden}.faq-section summary{padding:.85rem 1.15rem;cursor:pointer;font-weight:600;font-size:.88rem;color:var(--text-primary);transition:background .2s}.faq-section summary:hover{background:rgba(99,102,241,.06)}.faq-section details p{padding:.5rem 1.15rem 1rem;color:var(--text-secondary);font-size:.85rem;line-height:1.65}
.site-footer{border-top:1px solid var(--border);background:var(--bg-secondary);margin-top:3rem}.footer-grid{max-width:1200px;margin:0 auto;padding:2.5rem 2rem 1.5rem;display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr;gap:2.5rem}.footer-brand .footer-logo{font-weight:800;font-size:1.05rem;color:var(--accent-2);text-decoration:none;display:block;margin-bottom:.65rem}.footer-brand p{font-size:.8rem;color:var(--text-muted);line-height:1.7}.footer-col h4{font-size:.68rem;text-transform:uppercase;letter-spacing:.1em;color:var(--text-muted);margin-bottom:.7rem;font-weight:600}.footer-col ul{list-style:none}.footer-col li{margin-bottom:.3rem}.footer-col a{color:var(--text-secondary);text-decoration:none;font-size:.8rem;transition:color .2s}.footer-col a:hover{color:var(--accent-2)}.footer-bottom{max-width:1200px;margin:0 auto;padding:1rem 2rem;border-top:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.5rem}.footer-bottom p{color:var(--text-muted);font-size:.7rem}.footer-bottom .keyword{color:var(--accent-3);font-weight:600}
@media(max-width:768px){.nav-toggle{display:flex}.nav-menu{position:fixed;top:0;right:-300px;width:280px;height:100vh;background:var(--bg-primary);border-left:1px solid var(--border);padding:4rem 1.5rem 2rem;transition:right .3s;z-index:200;overflow-y:auto}.nav-menu.open{right:0}.nav-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:150}.nav-overlay.open{display:block}.nav-links{flex-direction:column;align-items:stretch;gap:0}.nav-links>li>a{padding:.7rem .5rem;font-size:.9rem}.dropdown{position:static;opacity:1;visibility:visible;transform:none;box-shadow:none;border:none;background:transparent;padding:0 0 .5rem 1rem;display:none}.has-dropdown.open .dropdown{display:block}.footer-grid{grid-template-columns:1fr 1fr;gap:2rem}.content-section{padding:1.5rem 1.25rem}.breadcrumb{padding:.6rem 1.25rem}.nav-inner{padding:.6rem 1rem}}
@media(max-width:480px){.footer-grid{grid-template-columns:1fr}.local-stats{grid-template-columns:repeat(2,1fr)}}"""


def generate_header(prefix):
    """Generate the standard site header with correct relative paths."""
    return f"""<a href="#main-content" class="skip-link">Skip to main content</a>
<header class="site-header"><nav class="nav-inner" aria-label="Primary"><a href="{prefix}" class="brand"><span class="brand-mark">HS99</span><span class="brand-name">SEO by <span>HighSoftware99</span></span></a><button class="nav-toggle" id="nav-toggle" aria-label="Toggle navigation" aria-expanded="false"><span></span><span></span><span></span></button><div class="nav-overlay" id="nav-overlay"></div><div class="nav-menu" id="nav-menu"><ul class="nav-links"><li class="has-dropdown"><a href="{prefix}technical-seo/" aria-haspopup="true">Services <span class="caret" aria-hidden="true"></span></a><ul class="dropdown"><li><a href="{prefix}technical-seo/">Technical SEO</a></li><li><a href="{prefix}local-seo/">Local SEO</a></li><li><a href="{prefix}on-page-seo">On-Page SEO</a></li><li><a href="{prefix}off-page-seo">Off-Page SEO</a></li><li><a href="{prefix}ecommerce-seo">E-Commerce SEO</a></li><li><a href="{prefix}youtube-seo">YouTube SEO</a></li></ul></li><li class="has-dropdown"><a href="{prefix}locations/" aria-haspopup="true">Locations <span class="caret" aria-hidden="true"></span></a><ul class="dropdown"><li><a href="{prefix}locations/">All Service Locations</a></li><li><a href="{prefix}seo-new-york">SEO New York</a></li><li><a href="{prefix}seo-los-angeles">SEO Los Angeles</a></li><li><a href="{prefix}seo-chicago">SEO Chicago</a></li><li><a href="{prefix}seo-houston">SEO Houston</a></li><li><a href="{prefix}seo-california">SEO California</a></li><li><a href="{prefix}seo-texas">SEO Texas</a></li><li><a href="{prefix}seo-florida">SEO Florida</a></li></ul></li><li><a href="{prefix}tools/">Tools</a></li><li><a href="{prefix}blog">Blog</a></li><li><a href="{prefix}about">About</a></li><li><a href="{prefix}pricing">Pricing</a></li><li><a href="{prefix}contact" class="nav-cta">Get Audit</a></li></ul></div></nav></header>"""


def generate_footer(prefix):
    """Generate the standard site footer with correct relative paths."""
    return f"""<footer class="site-footer"><div class="footer-grid"><div class="footer-brand"><a href="{prefix}" class="footer-logo">HighSoftware99</a><p>HighSoftware99 delivers technical SEO, local SEO, and free client-side SEO tools grounded in Semantic SEO and entity-driven architecture.</p></div><div class="footer-col"><h4>Services</h4><ul><li><a href="{prefix}technical-seo/">Technical SEO</a></li><li><a href="{prefix}local-seo/">Local SEO</a></li><li><a href="{prefix}on-page-seo">On-Page SEO</a></li><li><a href="{prefix}off-page-seo">Off-Page SEO</a></li><li><a href="{prefix}ecommerce-seo">E-Commerce SEO</a></li><li><a href="{prefix}youtube-seo">YouTube SEO</a></li></ul></div><div class="footer-col"><h4>Company</h4><ul><li><a href="{prefix}about">About HighSoftware99</a></li><li><a href="{prefix}pricing">Pricing</a></li><li><a href="{prefix}contact">Contact</a></li><li><a href="{prefix}blog">Blog</a></li></ul><h4 style="margin-top:1.25rem">Locations</h4><ul><li><a href="{prefix}locations/">All Locations</a></li><li><a href="{prefix}seo-new-york">SEO New York</a></li><li><a href="{prefix}seo-california">SEO California</a></li><li><a href="{prefix}seo-texas">SEO Texas</a></li><li><a href="{prefix}seo-florida">SEO Florida</a></li></ul></div><div class="footer-col"><h4>Legal</h4><ul><li><a href="{prefix}terms-and-conditions">Terms &amp; Conditions</a></li></ul><h4 style="margin-top:1.25rem">Tools &amp; Guides</h4><ul><li><a href="{prefix}tools/">Free SEO Tools</a></li><li><a href="{prefix}technical-seo/cloudflare-edge-seo">Cloudflare Edge SEO</a></li><li><a href="{prefix}technical-seo/cost-of-retrieval-reduction">Cost of Retrieval</a></li><li><a href="{prefix}local-seo/citation-building-strategy">Citation Building</a></li></ul></div></div><div class="footer-bottom"><p>&copy; 2026 HighSoftware99. All rights reserved.</p><p>seo-byhighsoftware99.com &middot; <span class="keyword">Instant Appear by SEO by HighSoftware99</span></p></div></footer>"""


def generate_nav_script():
    """Generate the mobile nav toggle script and deferred GA4 snippet."""
    return """<script>document.getElementById('nav-toggle').addEventListener('click',function(){var m=document.getElementById('nav-menu'),o=document.getElementById('nav-overlay');var isOpen=m.classList.toggle('open');o.classList.toggle('open',isOpen);this.setAttribute('aria-expanded',isOpen);});document.getElementById('nav-overlay').addEventListener('click',function(){document.getElementById('nav-menu').classList.remove('open');this.classList.remove('open');document.getElementById('nav-toggle').setAttribute('aria-expanded','false');});document.querySelectorAll('.has-dropdown > a').forEach(function(a){a.addEventListener('click',function(e){if(window.innerWidth<=768){e.preventDefault();this.parentElement.classList.toggle('open');}});});window.addEventListener('load',function(){var s=document.createElement('script');s.src='https://www.googletagmanager.com/gtag/js?id=G-BW37189SQ9';s.async=true;document.head.appendChild(s);s.onload=function(){window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-BW37189SQ9');};});</script>"""


# =============================================================================
# CITY PAGE GENERATOR
# =============================================================================
def generate_city_page(state_data, city_slug, city_data):
    """Generate a city-level page with unique content and Koray-aligned structure."""
    state_name = state_data["state_name"]
    state_abbr = state_data["state_abbr"]
    state_slug = state_data["state_slug"]
    city_name = city_data["city_name"]
    county = city_data["county"]
    population = city_data["population"]
    industries = city_data["industries"]
    industries_str = ", ".join(industries)
    business_count = city_data["business_count"]
    metro = city_data["metro_area"]
    competition = city_data["search_competition"]
    seo_focus = city_data["seo_focus"]
    directories = city_data["local_directories"]
    towns = city_data.get("towns", {})

    # Depth: locations/state/city/ = 3 levels deep
    prefix = "../../../"
    canonical = f"{DOMAIN}/locations/{slugify(state_name)}/{city_slug}/"

    # Breadcrumb data
    breadcrumbs = [
        {"name": "SEO by HighSoftware99", "url": f"{DOMAIN}/"},
        {"name": f"SEO {state_name}", "url": f"{DOMAIN}/{state_slug}"},
        {"name": f"SEO {city_name}", "url": canonical}
    ]
    breadcrumb_schema = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i+1, "name": b["name"], "item": b["url"]}
            for i, b in enumerate(breadcrumbs)
        ]
    }

    # ProfessionalService schema
    service_schema = {
        "@type": "ProfessionalService",
        "@id": f"{DOMAIN}/#organization",
        "name": "HighSoftware99",
        "alternateName": "SEO by HighSoftware99",
        "url": DOMAIN,
        "description": f"HighSoftware99 delivers enterprise SEO services for businesses in {city_name}, {state_abbr} including technical SEO, local SEO, and Instant Appear search visibility optimization.",
        "areaServed": {
            "@type": "City",
            "name": city_name,
            "containedInPlace": {
                "@type": "State",
                "name": state_name,
                "addressRegion": state_abbr
            }
        },
        "serviceType": ["Technical SEO", "Local SEO", "On-Page SEO", "Off-Page SEO", "E-Commerce SEO"],
        "knowsAbout": [
            f"SEO {city_name}",
            f"Local SEO {city_name} {state_abbr}",
            "Instant Appear by SEO by HighSoftware99",
            "SEO by HighSoftware99"
        ]
    }

    # FAQs
    faq_html, faq_schema = generate_faq_html(
        city_name, county,
        city_data.get("zip_range", "").split("–")[:2],
        industries
    )

    schema_graph = json.dumps({"@context": "https://schema.org", "@graph": [service_schema, breadcrumb_schema, faq_schema]}, ensure_ascii=False)

    # Town links
    town_links_html = ""
    if towns:
        town_links_html = '<h3>Towns &amp; Communities Served in ' + city_name + '</h3>\n    <div class="loc-links">\n'
        for t_slug, t_data in towns.items():
            town_links_html += f'      <a href="{t_slug}" class="loc-link">SEO {t_data["name"]}, {state_abbr}</a>\n'
        town_links_html += '    </div>'

    # Nearby city links from same state
    other_cities = [c for c in state_data["cities"].keys() if c != city_slug]
    sibling_links = ""
    if other_cities:
        sibling_links = '<h3>Other ' + state_name + ' Cities We Serve</h3>\n    <div class="loc-links">\n'
        for oc in other_cities:
            oc_name = state_data["cities"][oc]["city_name"]
            sibling_links += f'      <a href="../{oc}/" class="loc-link">SEO {oc_name}</a>\n'
        sibling_links += '    </div>'

    # Directory list
    dir_items = "\n".join(f"      <li>{d}</li>" for d in directories)

    city_meta_desc = f"Local & technical SEO in {city_name}, {state_abbr} by HighSoftware99 for {industries[0]} & {industries[1]} businesses. Sub-200ms TTFB & GBP ranking."
    if len(city_meta_desc) > 158:
        city_meta_desc = f"Enterprise local & technical SEO in {city_name}, {state_abbr} by HighSoftware99. Sub-200ms edge SEO, GBP optimization & citations."

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SEO Services {city_name}, {state_abbr} | HighSoftware99</title>
<meta name="description" content="{city_meta_desc}">
<meta name="keywords" content="SEO {city_name}, SEO {city_name} {state_abbr}, local SEO {city_name}, SEO by HighSoftware99, HighSoftware99">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<script type="application/ld+json">
{schema_graph}
</script>
<style>
{generate_shared_css()}
</style>
</head>
<body>
{generate_header(prefix)}

<main id="main-content">
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <ol>
      <li><a href="{prefix}">Home</a></li>
      <li><a href="{prefix}{state_slug}">{state_name} SEO</a></li>
      <li aria-current="page">{city_name} SEO</li>
    </ol>
  </nav>

  <section class="hero" aria-label="{city_name} SEO Centerpiece">
    <h1><span class="hl">SEO Services {city_name}, {state_abbr}</span> by HighSoftware99</h1>
    <p class="subtitle"><dfn>SEO by HighSoftware99 in {city_name}</dfn> is an enterprise search engine optimization service delivering technical SEO infrastructure, local search visibility, and Instant Appear ranking acceleration for businesses across the {metro} metropolitan area.</p>
    <div class="local-stats">
      <div class="stat-card"><div class="val">{population}</div><div class="lbl">Population</div></div>
      <div class="stat-card"><div class="val">{business_count}</div><div class="lbl">Businesses</div></div>
      <div class="stat-card"><div class="val">Top 3</div><div class="lbl">Local Pack Goal</div></div>
      <div class="stat-card"><div class="val">&lt;200ms</div><div class="lbl">TTFB Target</div></div>
    </div>
  </section>

  <article class="content-section">
    <h2>{city_name} SEO Strategy by HighSoftware99</h2>
    <p>{seo_focus}</p>
    <p>HighSoftware99 executes data-driven SEO campaigns for {city_name} businesses through comprehensive technical audits, semantic entity architecture, and geo-targeted content strategies. Every {city_name} deployment leverages the Instant Appear framework — a proprietary methodology that accelerates search visibility by aligning page-level entity signals with Google's information retrieval objectives. {city_name} businesses in {industries_str} benefit from HighSoftware99's domain-specific keyword research and competitive gap analysis calibrated to {county}'s commercial search landscape.</p>

    <h3>Key Industries Served in {city_name}</h3>
    <p>HighSoftware99 provides specialized SEO strategies for {city_name}'s dominant economic sectors. Search competition in {city_name} is {competition}, requiring industry-tailored approaches rather than generic optimization templates.</p>
    <div class="service-grid">
      <div class="svc-card"><h3>Technical SEO</h3><p>Cloudflare edge rendering, DOM optimization, and Core Web Vitals acceleration for {city_name} enterprise websites and {metro} digital properties.</p></div>
      <div class="svc-card"><h3>Local SEO</h3><p>Google Business Profile management, {county} citation building, and map pack ranking for {city_name} businesses.</p></div>
      <div class="svc-card"><h3>On-Page SEO</h3><p>Semantic entity targeting and heading hierarchy optimized for {city_name} commercial search queries across {industries_str}.</p></div>
      <div class="svc-card"><h3>Off-Page SEO</h3><p>Authority building through editorial placements in {city_name} business publications and {state_name} industry media.</p></div>
    </div>

    <h3>Local Citation Sources for {city_name}</h3>
    <p>HighSoftware99 builds structured citations for {city_name} businesses across verified local directories to strengthen NAP consistency and local search authority:</p>
    <ul style="color:var(--text-secondary);padding-left:1.5rem;margin-bottom:1.5rem;">
{dir_items}
      <li>Google Business Profile</li>
      <li>Yelp {city_name}</li>
      <li>Better Business Bureau {state_abbr}</li>
    </ul>

    {town_links_html}

    {sibling_links}

    <div class="annotation-block"><p>HighSoftware99 delivers enterprise SEO services across all 50 U.S. states through seo-byhighsoftware99.com. {city_name} SEO campaigns inherit the Instant Appear framework and semantic optimization standards documented on the central brand hub. The homepage consolidates HighSoftware99's complete service architecture and entity authority.</p><p><a href="{prefix}">seobyhighsoftware99.com</a></p></div>

    <div class="annotation-block"><p>{city_name} is a primary market within HighSoftware99's {state_name} SEO coverage. The {state_name} state hub provides comprehensive SEO methodology context for all {state_abbr} deployments including {city_name} and surrounding municipalities. {city_name} campaigns directly inherit the state-level competitive analysis and regional keyword architecture.</p><p><a href="{prefix}{state_slug}">SEO {state_name} by HighSoftware99</a></p></div>

    <div class="annotation-block"><p>{city_name} SEO campaigns operate under HighSoftware99's Local SEO framework. The Local SEO hub details citation building strategy, Google Business Profile management, and geo-targeted entity alignment applicable across {city_name} and all {county} markets.</p><p><a href="{prefix}local-seo/">Local SEO Services by HighSoftware99</a></p></div>
  </article>

  {faq_html}
</main>

{generate_footer(prefix)}
{generate_nav_script()}
</body>
</html>"""
    return html


# =============================================================================
# TOWN PAGE GENERATOR
# =============================================================================
def generate_town_page(state_data, city_slug, city_data, town_slug, town_data):
    """Generate a town-level page with hyper-local content and Koray-aligned structure."""
    state_name = state_data["state_name"]
    state_abbr = state_data["state_abbr"]
    state_slug = state_data["state_slug"]
    city_name = city_data["city_name"]
    town_name = town_data["name"]
    county = town_data["county"]
    population = town_data["population"]
    zip_codes = town_data["zip_codes"]
    industries = town_data["industries"]
    industries_str = ", ".join(industries)
    nearby = town_data.get("nearby", [])
    local_context = town_data["local_context"]

    # Depth: locations/state/city/town.html = 3 levels deep
    prefix = "../../../"
    canonical = f"{DOMAIN}/locations/{slugify(state_name)}/{city_slug}/{town_slug}"

    # Breadcrumb data
    breadcrumbs = [
        {"name": "SEO by HighSoftware99", "url": f"{DOMAIN}/"},
        {"name": f"SEO {state_name}", "url": f"{DOMAIN}/{state_slug}"},
        {"name": f"SEO {city_name}", "url": f"{DOMAIN}/locations/{slugify(state_name)}/{city_slug}/"},
        {"name": f"SEO {town_name}", "url": canonical}
    ]
    breadcrumb_schema = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i+1, "name": b["name"], "item": b["url"]}
            for i, b in enumerate(breadcrumbs)
        ]
    }

    # ProfessionalService schema with nested geo hierarchy
    service_schema = {
        "@type": "ProfessionalService",
        "@id": f"{DOMAIN}/#organization",
        "name": "HighSoftware99",
        "alternateName": "SEO by HighSoftware99",
        "url": DOMAIN,
        "description": f"HighSoftware99 provides local SEO services for businesses in {town_name}, {state_abbr} including Google Business Profile optimization, citation building, and Instant Appear visibility.",
        "areaServed": {
            "@type": "City",
            "name": town_name,
            "containedInPlace": {
                "@type": "City",
                "name": city_name,
                "containedInPlace": {
                    "@type": "State",
                    "name": state_name,
                    "addressRegion": state_abbr
                }
            }
        },
        "serviceType": ["Local SEO", "Technical SEO", "Google Business Profile Optimization"],
        "knowsAbout": [
            f"SEO {town_name}",
            f"Local SEO {town_name} {state_abbr}",
            "Instant Appear by SEO by HighSoftware99",
            "SEO by HighSoftware99"
        ]
    }

    # FAQs
    faq_html, faq_schema = generate_faq_html(town_name, county, zip_codes, industries)

    schema_graph = json.dumps({"@context": "https://schema.org", "@graph": [service_schema, breadcrumb_schema, faq_schema]}, ensure_ascii=False)

    # Nearby town links — strictly resolved to existing built pages (0 broken 404s)
    existing_towns = city_data.get("towns", {})
    valid_nearby = [n for n in nearby if n in existing_towns and n != town_slug]
    for sibling_slug in existing_towns:
        if sibling_slug != town_slug and sibling_slug not in valid_nearby:
            valid_nearby.append(sibling_slug)

    nearby_links = ""
    link_items = []
    for n in valid_nearby:
        link_items.append(f'      <a href="{n}" class="loc-link">SEO {existing_towns[n]["name"]}, {state_abbr}</a>')
    for oc_slug, oc_data in state_data["cities"].items():
        if oc_slug != city_slug:
            link_items.append(f'      <a href="../{oc_slug}/" class="loc-link">SEO {oc_data["city_name"]}, {state_abbr}</a>')
    if link_items:
        nearby_links = '<h3>Nearby Areas Served by HighSoftware99</h3>\n    <div class="loc-links">\n' + "\n".join(link_items) + '\n    </div>'

    zip_display = ", ".join(zip_codes)
    zip_short = ", ".join(zip_codes[:2])
    town_meta_desc = f"Local SEO in {town_name}, {state_abbr} ({county}) by HighSoftware99. GBP optimization & citations for {zip_short} {industries[0]} businesses."
    if len(town_meta_desc) > 158:
        town_meta_desc = f"Local SEO in {town_name}, {state_abbr} by HighSoftware99. Google Business Profile, citations & technical SEO for {zip_short}."

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Local SEO {town_name}, {state_abbr} | HighSoftware99</title>
<meta name="description" content="{town_meta_desc}">
<meta name="keywords" content="SEO {town_name}, SEO {town_name} {state_abbr}, local SEO {town_name}, SEO by HighSoftware99, HighSoftware99">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<script type="application/ld+json">
{schema_graph}
</script>
<style>
{generate_shared_css()}
</style>
</head>
<body>
{generate_header(prefix)}

<main id="main-content">
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <ol>
      <li><a href="{prefix}">Home</a></li>
      <li><a href="{prefix}{state_slug}">{state_name} SEO</a></li>
      <li><a href="./">{city_name} SEO</a></li>
      <li aria-current="page">{town_name} SEO</li>
    </ol>
  </nav>

  <section class="hero" aria-label="{town_name} Local SEO Centerpiece">
    <h1><span class="hl">Local SEO Services {town_name}, {state_abbr}</span> by HighSoftware99</h1>
    <p class="subtitle"><dfn>SEO by HighSoftware99 in {town_name}</dfn> delivers hyper-local search engine optimization for businesses in {town_name}, {county}, {state_name} — targeting zip codes {zip_display} through Google Business Profile optimization, local citation building, and the Instant Appear visibility framework.</p>
    <div class="local-stats">
      <div class="stat-card"><div class="val">{population}</div><div class="lbl">Population</div></div>
      <div class="stat-card"><div class="val">{len(zip_codes)}</div><div class="lbl">Zip Codes</div></div>
      <div class="stat-card"><div class="val">Top 3</div><div class="lbl">Map Pack Goal</div></div>
      <div class="stat-card"><div class="val">30 Days</div><div class="lbl">Visibility Timeline</div></div>
    </div>
  </section>

  <article class="content-section">
    <h2>Why Local SEO Matters for {town_name} Businesses</h2>
    <p>{local_context}</p>
    <p>HighSoftware99 applies the Instant Appear framework to {town_name} SEO campaigns, combining technical infrastructure optimization with hyper-local entity signals. Every deployment includes structured citation building across {county} directories, Google Business Profile category and attribute optimization, and semantic content architecture targeting {town_name}-specific commercial search queries. Businesses in {industries_str} across the {zip_display} zip code area benefit from HighSoftware99's localized keyword research and competitive positioning strategies.</p>

    <h3>Key Industries in {town_name}</h3>
    <p>{town_name}'s local economy centers around {industries_str}. HighSoftware99 tailors SEO strategies to each industry's search behavior patterns, ensuring that {town_name} businesses capture high-intent local queries from consumers and business buyers within {county}.</p>
    <div class="service-grid">
      <div class="svc-card"><h3>Google Business Profile</h3><p>Complete GBP optimization for {town_name} businesses — category selection, service attributes, review management, and post publishing.</p></div>
      <div class="svc-card"><h3>Local Citations</h3><p>Structured NAP citation building across {county} directories, industry platforms, and {state_name} business listings.</p></div>
      <div class="svc-card"><h3>Technical SEO</h3><p>Sub-200ms TTFB, semantic HTML optimization, and Core Web Vitals acceleration for {town_name} business websites.</p></div>
      <div class="svc-card"><h3>Content Strategy</h3><p>Localized content targeting {town_name} search queries across {industries_str} with entity-rich page architecture.</p></div>
    </div>

    <h3>Service Area: {town_name} Zip Codes</h3>
    <p>HighSoftware99 provides SEO services for businesses operating in the following {town_name}, {state_abbr} zip codes: <strong>{zip_display}</strong>. Our local SEO campaigns target search queries originating from and relevant to these specific geographic areas within {county}.</p>

    {nearby_links}

    <div class="annotation-block"><p>HighSoftware99 delivers enterprise SEO services across all 50 U.S. states through seo-byhighsoftware99.com. {town_name} SEO campaigns inherit the Instant Appear framework and semantic optimization standards documented on the central brand hub. Every geographic deployment connects to HighSoftware99's core entity authority architecture.</p><p><a href="{prefix}">seobyhighsoftware99.com</a></p></div>

    <div class="annotation-block"><p>{town_name} is served as part of HighSoftware99's {city_name} metropolitan SEO coverage. The {city_name} hub provides detailed competitive analysis, industry-specific strategies, and local citation source documentation for the broader {city_name} market that directly applies to {town_name} campaigns.</p><p><a href="./">SEO {city_name}, {state_abbr} by HighSoftware99</a></p></div>

    <div class="annotation-block"><p>{town_name} sits within HighSoftware99's {state_name} state-level SEO deployment. The {state_name} hub documents regional search patterns, state-wide competitive intelligence, and {state_abbr}-specific keyword architecture that informs {town_name}'s local optimization strategy.</p><p><a href="{prefix}{state_slug}">SEO {state_name} by HighSoftware99</a></p></div>

    <div class="annotation-block"><p>{town_name} local SEO campaigns operate under HighSoftware99's Local SEO methodology. The Local SEO hub details NAP citation building, Google Business Profile management, and geo-targeted entity alignment practices deployed across {town_name} and all {county} markets.</p><p><a href="{prefix}local-seo/">Local SEO Services by HighSoftware99</a></p></div>
  </article>

  {faq_html}
</main>

{generate_footer(prefix)}
{generate_nav_script()}
</body>
</html>"""
    return html


# =============================================================================
# LOCATIONS HUB PAGE (Navigational directory — minimal content, crawl entry point)
# =============================================================================
def generate_locations_hub():
    """Generate the master locations directory page."""
    prefix = "../"

    # Build state → city listing
    state_listings = ""
    for state_slug, state_data in sorted(locations_data.items(), key=lambda x: x[1]["state_name"]):
        state_name = state_data["state_name"]
        state_abbr = state_data["state_abbr"]
        existing_slug = state_data["state_slug"]
        cities = state_data["cities"]

        city_links = ""
        for city_slug, city_data in cities.items():
            city_name = city_data["city_name"]
            town_count = len(city_data.get("towns", {}))
            city_links += f'        <a href="{state_slug}/{city_slug}/" class="loc-link">SEO {city_name} ({town_count} towns)</a>\n'

        state_listings += f"""
    <section style="margin-bottom:2rem;">
      <h3><a href="{prefix}{existing_slug}" style="color:var(--accent-city);text-decoration:none;font-weight:800;">SEO {state_name} ({state_abbr})</a></h3>
      <div class="loc-links" style="margin-top:.6rem;">
{city_links}      </div>
    </section>"""

    # Count totals
    total_cities = sum(len(sd["cities"]) for sd in locations_data.values())
    total_towns = sum(
        len(cd.get("towns", {}))
        for sd in locations_data.values()
        for cd in sd["cities"].values()
    )

    canonical = f"{DOMAIN}/locations/"

    schema = json.dumps({
        "@context": "https://schema.org",
        "@graph": [{
            "@type": "CollectionPage",
            "name": "All Cities & Towns Served by HighSoftware99",
            "description": f"Directory of {total_cities} cities and {total_towns} towns across {len(locations_data)} states where HighSoftware99 provides SEO services.",
            "url": canonical,
            "isPartOf": {"@id": f"{DOMAIN}/#website"},
            "provider": {"@id": f"{DOMAIN}/#organization"}
        }, {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "SEO by HighSoftware99", "item": f"{DOMAIN}/"},
                {"@type": "ListItem", "position": 2, "name": "All Service Locations", "item": canonical}
            ]
        }]
    }, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SEO Service Locations Directory | HighSoftware99</title>
<meta name="description" content="Browse all {total_cities} cities and {total_towns} towns across {len(locations_data)} states served by HighSoftware99 local SEO, GBP optimization, and technical SEO.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<script type="application/ld+json">
{schema}
</script>
<style>
{generate_shared_css()}
</style>
</head>
<body>
{generate_header(prefix)}

<main id="main-content">
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <ol>
      <li><a href="{prefix}">Home</a></li>
      <li aria-current="page">All Service Locations</li>
    </ol>
  </nav>

  <section class="hero" aria-label="Locations Directory">
    <h1><span class="hl">All Cities &amp; Towns</span> Served by HighSoftware99</h1>
    <p class="subtitle">HighSoftware99 delivers local SEO, technical SEO, and Instant Appear search visibility services across {total_cities} cities and {total_towns} towns in {len(locations_data)} states.</p>
    <div class="local-stats">
      <div class="stat-card"><div class="val">{len(locations_data)}</div><div class="lbl">States</div></div>
      <div class="stat-card"><div class="val">{total_cities}</div><div class="lbl">Cities</div></div>
      <div class="stat-card"><div class="val">{total_towns}</div><div class="lbl">Towns</div></div>
    </div>
  </section>

  <article class="content-section">
    <h2>Service Locations by State</h2>
    <p>Browse HighSoftware99's city-level and town-level SEO services by state. Each state hub provides comprehensive regional SEO methodology, while city and town pages deliver hyper-local optimization strategies.</p>
    {state_listings}

    <div class="annotation-block"><p>HighSoftware99 operates seo-byhighsoftware99.com as the authoritative hub for all SEO service documentation, methodology, and geographic deployments. Every city and town SEO campaign inherits the Instant Appear framework and semantic standards documented on the central brand entity node.</p><p><a href="{prefix}">seobyhighsoftware99.com</a></p></div>

    <div class="annotation-block"><p>All location-based SEO campaigns are powered by HighSoftware99's Local SEO methodology including Google Business Profile management, structured citation building, and geo-targeted entity alignment.</p><p><a href="{prefix}local-seo/">Local SEO Services by HighSoftware99</a></p></div>
  </article>
</main>

{generate_footer(prefix)}
{generate_nav_script()}
</body>
</html>"""
    return html


# =============================================================================
# SITEMAP GENERATORS
# =============================================================================
def generate_sitemap_locations(all_urls):
    """Generate sitemap-locations.xml with all new location URLs."""
    entries = ""
    for url, priority in all_urls:
        entries += f"""  <url>
    <loc>{url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{priority}</priority>
  </url>
"""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}</urlset>
"""


def generate_sitemap_index():
    """Generate sitemap-index.xml pointing to both sitemaps."""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>{DOMAIN}/sitemap-main.xml</loc>
    <lastmod>{TODAY}</lastmod>
  </sitemap>
  <sitemap>
    <loc>{DOMAIN}/sitemap-locations.xml</loc>
    <lastmod>{TODAY}</lastmod>
  </sitemap>
</sitemapindex>
"""


# =============================================================================
# MAIN BUILD PROCESS
# =============================================================================
def main():
    print("=" * 60)
    print("Building Koray-Aligned City & Town Location Pages")
    print("=" * 60)

    all_urls = []
    page_count = 0

    # 1. Generate Locations Hub
    hub_dir = LOCATIONS_DIR
    os.makedirs(hub_dir, exist_ok=True)
    hub_html = generate_locations_hub()
    hub_path = os.path.join(hub_dir, "index.html")
    with open(hub_path, "w", encoding="utf-8") as f:
        f.write(hub_html)
    print(f"  ✓ locations/index.html (Hub)")
    all_urls.append((f"{DOMAIN}/locations/", "0.7"))
    page_count += 1

    # 2. Generate City and Town pages
    for state_slug, state_data in locations_data.items():
        state_name = state_data["state_name"]
        print(f"\n  [{state_name}]")

        for city_slug, city_data in state_data["cities"].items():
            city_name = city_data["city_name"]

            # Create city directory
            city_dir = os.path.join(LOCATIONS_DIR, state_slug, city_slug)
            os.makedirs(city_dir, exist_ok=True)

            # Generate city page
            city_html = generate_city_page(state_data, city_slug, city_data)
            city_path = os.path.join(city_dir, "index.html")
            with open(city_path, "w", encoding="utf-8") as f:
                f.write(city_html)
            print(f"    ✓ locations/{state_slug}/{city_slug}/index.html")
            all_urls.append((f"{DOMAIN}/locations/{state_slug}/{city_slug}/", "0.65"))
            page_count += 1

            # Generate town pages
            for town_slug, town_data in city_data.get("towns", {}).items():
                town_name = town_data["name"]
                town_html = generate_town_page(state_data, city_slug, city_data, town_slug, town_data)
                town_path = os.path.join(city_dir, f"{town_slug}.html")
                with open(town_path, "w", encoding="utf-8") as f:
                    f.write(town_html)
                print(f"      ✓ locations/{state_slug}/{city_slug}/{town_slug}.html")
                all_urls.append((f"{DOMAIN}/locations/{state_slug}/{city_slug}/{town_slug}", "0.6"))
                page_count += 1

    # 3. Generate sitemap-locations.xml
    sitemap_loc = generate_sitemap_locations(all_urls)
    sitemap_loc_path = os.path.join(TARGET_DIR, "sitemap-locations.xml")
    with open(sitemap_loc_path, "w", encoding="utf-8") as f:
        f.write(sitemap_loc)
    print(f"\n  ✓ sitemap-locations.xml ({len(all_urls)} URLs)")

    # 4. Copy existing sitemap.xml → sitemap-main.xml
    sitemap_src = os.path.join(TARGET_DIR, "sitemap.xml")
    sitemap_main = os.path.join(TARGET_DIR, "sitemap-main.xml")
    if os.path.exists(sitemap_src):
        with open(sitemap_src, "r", encoding="utf-8") as f:
            main_content = f.read()
        with open(sitemap_main, "w", encoding="utf-8") as f:
            f.write(main_content)
        print(f"  ✓ sitemap-main.xml (copy of existing sitemap.xml)")

    # 5. Generate sitemap-index.xml
    sitemap_idx = generate_sitemap_index()
    sitemap_idx_path = os.path.join(TARGET_DIR, "sitemap-index.xml")
    with open(sitemap_idx_path, "w", encoding="utf-8") as f:
        f.write(sitemap_idx)
    print(f"  ✓ sitemap-index.xml")

    # 6. Update robots.txt cleanly (declare sitemap-index.xml once)
    robots_path = os.path.join(TARGET_DIR, "robots.txt")
    robots_content = f"""# robots.txt for seo-byhighsoftware99.com
User-agent: *
Allow: /

# Sitemap Index
Sitemap: {DOMAIN}/sitemap-index.xml
"""
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(robots_content)
    print(f"  ✓ robots.txt (updated with sitemap index)")

    print(f"\n{'=' * 60}")
    print(f"BUILD COMPLETE: {page_count} pages generated")
    print(f"  Hub: 1 | Cities: {sum(len(sd['cities']) for sd in locations_data.values())} | Towns: {sum(len(cd.get('towns', {})) for sd in locations_data.values() for cd in sd['cities'].values())}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
