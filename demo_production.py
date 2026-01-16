#!/usr/bin/env python3
"""
Demo: Complete Entertainment Production Workflow
Generates a short-form video production package from concept to post-production advisory.
"""

import os
from src.workflow.entertainment_workflow import EntertainmentWorkflow
from src.models.script import Platform

def main():
    """Execute a complete entertainment production workflow demonstration."""
    
    # Define production parameters
    title = "The Coffee Shop Catastrophe"
    genre = "comedy"
    platform = Platform.TIKTOK
    duration = 60  # seconds
    audience = "Gen Z, 18-24, humor-focused"
    
    print("=" * 80)
    print("ENTERTAINMENT PRODUCTION AGENT - DEMO")
    print("=" * 80)
    print(f"\nTitle: {title}")
    print(f"Genre: {genre}")
    print(f"Platform: {platform.value}")
    print(f"Duration: {duration}s")
    print(f"Audience: {audience}")
    print("\n" + "=" * 80)
    
    # Create workflow instance
    workflow = EntertainmentWorkflow()
    
    # Execute complete workflow
    print("\n[1/5] Generating script...")
    success, errors, output_files = workflow.execute_full_workflow(
        title=title,
        genre=genre,
        platform=platform,
        target_duration_seconds=duration,
        target_audience=audience,
        output_dir="demo_output"
    )
    
    if success:
        print("✓ Script generated")
        print("\n[2/5] Creating script breakdown...")
        print("✓ Breakdown complete")
        print("\n[3/5] Generating storyboard and shot list...")
        print("✓ Storyboard complete")
        print("\n[4/5] Creating production advisory...")
        print("✓ Production notes ready")
        print("\n[5/5] Creating post-production advisory...")
        print("✓ Post-production notes ready")
        
        print("\n" + "=" * 80)
        print("WORKFLOW COMPLETE")
        print("=" * 80)
        print(f"\nOutput directory: demo_output")
        print("\nGenerated files:")
        for filename, filepath in output_files.items():
            print(f"  - {filename}: {filepath}")
        
        if errors:
            print("\nValidation warnings:")
            for error in errors:
                print(f"  ⚠ {error}")
        else:
            print("\n✓ All validation checks passed")
        
        print("\n" + "=" * 80)
        print("PRODUCTION PACKAGE READY FOR REVIEW")
        print("=" * 80)
    else:
        print("\n✗ Workflow failed")
        if errors:
            print("\nValidation errors:")
            for error in errors:
                print(f"  - {error}")

if __name__ == "__main__":
    main()
