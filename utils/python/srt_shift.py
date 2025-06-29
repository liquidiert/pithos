#!/usr/bin/env python3
"""
SRT Subtitle Timestamp Shifter

This script shifts all timestamps in an SRT subtitle file by a given amount of seconds.
The shifted file is saved as a copy next to the original file.

Usage:
    python srt_shift.py <input_file> <seconds> [--subtract]

Examples:
    python srt_shift.py "movie-en.srt" 2.5          # Add 2.5 seconds
    python srt_shift.py "movie-en.srt" 1.5 --subtract  # Subtract 1.5 seconds
    python srt_shift.py "movie-en.srt" -0.5         # Subtract 0.5 seconds
"""

import argparse
import re
import os
from datetime import datetime, timedelta


def parse_timestamp(timestamp_str):
    """Parse SRT timestamp format (HH:MM:SS,mmm) to total seconds."""
    # Remove any leading/trailing whitespace
    timestamp_str = timestamp_str.strip()
    
    # Split by comma to separate seconds and milliseconds
    time_part, ms_part = timestamp_str.split(',')
    
    # Parse hours, minutes, seconds
    hours, minutes, seconds = map(int, time_part.split(':'))
    
    # Convert to total seconds
    total_seconds = hours * 3600 + minutes * 60 + seconds + int(ms_part) / 1000
    
    return total_seconds


def format_timestamp(total_seconds):
    """Convert total seconds back to SRT timestamp format (HH:MM:SS,mmm)."""
    # Handle negative timestamps by setting to 0
    if total_seconds < 0:
        total_seconds = 0
    
    # Convert to hours, minutes, seconds, milliseconds
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int((total_seconds % 1) * 1000)
    
    # Format as HH:MM:SS,mmm
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def shift_srt_timestamps(input_file, shift_seconds, output_file=None):
    """
    Shift all timestamps in an SRT file by the given number of seconds.
    
    Args:
        input_file (str): Path to the input SRT file
        shift_seconds (float): Number of seconds to shift (positive = add, negative = subtract)
        output_file (str): Path to the output file (optional, auto-generated if not provided)
    
    Returns:
        str: Path to the output file
    """
    # Generate output filename if not provided
    if output_file is None:
        base_name, ext = os.path.splitext(input_file)
        shift_str = f"{shift_seconds:+g}".replace('+', 'plus_').replace('-', 'minus_')
        output_file = f"{base_name}_shifted_{shift_str}s{ext}"
    
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content into subtitle blocks
    blocks = content.strip().split('\n\n')
    
    shifted_blocks = []
    
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3:  # Invalid block, skip
            shifted_blocks.append(block)
            continue
        
        # First line should be sequence number
        sequence_number = lines[0]
        
        # Second line should be timestamp
        timestamp_line = lines[1]
        
        # Check if this looks like a timestamp line
        timestamp_pattern = r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})'
        match = re.match(timestamp_pattern, timestamp_line)
        
        if not match:
            # Not a timestamp line, keep as is
            shifted_blocks.append(block)
            continue
        
        # Parse start and end timestamps
        start_time = parse_timestamp(match.group(1))
        end_time = parse_timestamp(match.group(2))
        
        # Apply shift
        new_start_time = start_time + shift_seconds
        new_end_time = end_time + shift_seconds
        
        # Format new timestamps
        new_start_str = format_timestamp(new_start_time)
        new_end_str = format_timestamp(new_end_time)
        
        # Create new timestamp line
        new_timestamp_line = f"{new_start_str} --> {new_end_str}"
        
        # Reconstruct block
        new_lines = [sequence_number, new_timestamp_line] + lines[2:]
        shifted_blocks.append('\n'.join(new_lines))
    
    # Write the shifted content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(shifted_blocks))
    
    return output_file


def main():
    parser = argparse.ArgumentParser(
        description="Shift SRT subtitle timestamps by a given amount of seconds",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        'input_file',
        help='Path to the input SRT file'
    )
    
    parser.add_argument(
        'seconds',
        type=float,
        help='Number of seconds to shift (positive = add, negative = subtract)'
    )
    
    parser.add_argument(
        '--subtract',
        action='store_true',
        help='Subtract the seconds instead of adding (alternative to negative values)'
    )
    
    parser.add_argument(
        '--output',
        '-o',
        help='Output file path (auto-generated if not specified)'
    )
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.")
        return 1
    
    # Determine shift amount
    shift_seconds = args.seconds
    if args.subtract:
        shift_seconds = -args.seconds
    
    try:
        # Perform the shift
        output_file = shift_srt_timestamps(
            args.input_file, 
            shift_seconds, 
            args.output
        )
        
        print(f"Successfully shifted timestamps by {shift_seconds:+g} seconds")
        print(f"Output saved to: {output_file}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main()) 
