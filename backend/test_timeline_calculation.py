#!/usr/bin/env python3
"""
Test timeline calculation logic
"""

def calculate_timeline(total_components):
    duration_weeks = max(8, total_components * 2)
    duration_months = round(duration_weeks / 4.3, 1)
    
    # Calculate phase durations that add up to total duration
    phase1_duration = max(3, round(duration_weeks * 0.25))
    phase2_duration = max(4, round(duration_weeks * 0.4))
    phase3_duration = max(4, round(duration_weeks * 0.25))
    phase4_duration = max(2, duration_weeks - phase1_duration - phase2_duration - phase3_duration)
    
    # Adjust if total doesn't match
    total_calculated = phase1_duration + phase2_duration + phase3_duration + phase4_duration
    if total_calculated != duration_weeks:
        # Adjust the largest phase to match
        phase2_duration += (duration_weeks - total_calculated)
    
    print(f"Total components: {total_components}")
    print(f"Duration weeks: {duration_weeks}")
    print(f"Duration months: {duration_months}")
    print(f"Phase 1 (Assessment): weeks 1-{phase1_duration} (duration: {phase1_duration})")
    print(f"Phase 2 (Infrastructure): weeks {phase1_duration + 1}-{phase1_duration + phase2_duration} (duration: {phase2_duration})")
    print(f"Phase 3 (Data): weeks {phase1_duration + phase2_duration + 1}-{phase1_duration + phase2_duration + phase3_duration} (duration: {phase3_duration})")
    print(f"Phase 4 (Cutover): weeks {phase1_duration + phase2_duration + phase3_duration + 1}-{duration_weeks} (duration: {phase4_duration})")
    print(f"Total phase durations: {phase1_duration + phase2_duration + phase3_duration + phase4_duration}")
    print("-" * 50)

# Test with different component counts
calculate_timeline(5)  # 10 weeks
calculate_timeline(10) # 20 weeks  
calculate_timeline(12) # 24 weeks
