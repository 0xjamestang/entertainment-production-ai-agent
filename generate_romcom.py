#!/usr/bin/env python3
"""Generate romantic comedy production package for TikTok."""

from src.workflow.entertainment_workflow import EntertainmentWorkflow
from src.models.script import Platform

# Production parameters
title = "The Wrong Coffee Order"
genre = "romantic comedy"
platform = Platform.TIKTOK
duration = 60
audience = "Female, 18-30, light romantic content"

print("=" * 80)
print("GENERATING PRODUCTION PACKAGE")
print("=" * 80)
print(f"\nTitle: {title}")
print(f"Genre: {genre}")
print(f"Platform: {platform.value}")
print(f"Duration: {duration}s")
print(f"Audience: {audience}")
print(f"Tone: Light, fast-paced, emotional hook in first 3 seconds")
print("\n" + "=" * 80)

# Execute workflow
workflow = EntertainmentWorkflow()

print("\n🎬 Generating script...")
success, errors, output_files = workflow.execute_full_workflow(
    title=title,
    genre=genre,
    platform=platform,
    target_duration_seconds=duration,
    target_audience=audience,
    output_dir="productions/the_wrong_coffee_order"
)

if success:
    print("✓ Script complete")
    print("✓ Breakdown complete")
    print("✓ Storyboard complete")
    print("✓ Production notes complete")
    print("✓ Post-production notes complete")
    
    print("\n" + "=" * 80)
    print("✅ PRODUCTION PACKAGE READY")
    print("=" * 80)
    print(f"\nOutput: productions/the_wrong_coffee_order/")
    print("\nGenerated files:")
    for name, path in output_files.items():
        print(f"  📄 {name}")
    
    if errors:
        print("\n⚠️  Validation notes:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\n✓ All validation checks passed")
else:
    print("\n❌ Generation failed")
    for error in errors:
        print(f"  - {error}")
