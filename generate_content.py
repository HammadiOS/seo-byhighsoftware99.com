import os
import glob
import json
import shutil
import re

ARTIFACT_DIR = "/Users/macbookpro/.gemini/antigravity-ide/brain/8b04f05d-4026-4e2e-bb79-881086261567"
TARGET_DIR = "/Users/macbookpro/Documents/GitHub/seo-byhighsoftware99.com"
IMG_DIR = os.path.join(TARGET_DIR, "images")

# 1. Copy generated images to images/
image_mappings = {
    "blog_ai_overviews_2026": "blog-ai-overviews-2026.png",
    "blog_llm_search_2026": "blog-llm-search-2026.png",
    "blog_geo_optimization_2026": "blog-geo-optimization-2026.png",
    "blog_ai_content_quality_2026": "blog-ai-content-quality-2026.png",
    "blog_agentic_ai_seo_2026": "blog-agentic-ai-seo-2026.png",
    "blog_multimodal_visual_search_2026": "blog-multimodal-visual-search-2026.png",
    "blog_semantic_entity_graph_2026": "blog-semantic-entity-graph-2026.png",
    "blog_programmatic_seo_ai_2026": "blog-programmatic-seo-ai-2026.png",
    "blog_realtime_llm_crawling_2026": "blog-realtime-llm-crawling-2026.png",
    "blog_predictive_seo_analytics_2026": "blog-predictive-seo-analytics-2026.png"
}

for key, dest_name in image_mappings.items():
    matches = glob.glob(os.path.join(ARTIFACT_DIR, f"{key}_*.png"))
    if matches:
        latest = sorted(matches)[-1]
        dest_path = os.path.join(IMG_DIR, dest_name)
        shutil.copy(latest, dest_path)
        print(f"Copied {latest} -> {dest_path}")

print("Image copy complete.")
