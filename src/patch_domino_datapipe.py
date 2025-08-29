# patch_domino_datapipe.py
"""
Temporary patch for the bug in compute_scaling_factors
This monkey-patches the function to fix the min/max order
"""

import sys
import os

def patch_compute_scaling_factors():
    """Monkey patch to fix the bug"""
    
    filepath = "/usr/local/lib/python3.12/dist-packages/physicsnemo/datapipes/cae/domino_datapipe.py"
    
    # Read the file
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # Find and fix the bug
    fixed = False
    for i, line in enumerate(lines):
        # Fix surface factors
        if "surf_scaling_factors = [surf_fields_max, surf_fields_min]" in line:
            lines[i] = line.replace(
                "[surf_fields_max, surf_fields_min]",
                "[surf_fields_min, surf_fields_max]"  # CORRECT ORDER
            )
            print(f"Fixed line {i+1}: surface scaling factors order")
            fixed = True
        
        # Fix volume factors
        if "vol_scaling_factors = [vol_fields_max, vol_fields_min]" in line:
            lines[i] = line.replace(
                "[vol_fields_max, vol_fields_min]",
                "[vol_fields_min, vol_fields_max]"  # CORRECT ORDER
            )
            print(f"Fixed line {i+1}: volume scaling factors order")
            fixed = True
    
    if fixed:
        # Back up original
        backup_path = filepath + ".backup"
        if not os.path.exists(backup_path):
            os.system(f"cp {filepath} {backup_path}")
            print(f"Backed up original to {backup_path}")
        
        # Write fixed version
        with open(filepath, 'w') as f:
            f.writelines(lines)
        print(f"✅ Patched {filepath}")
        return True
    else:
        print("❌ Could not find the lines to patch")
        return False

if __name__ == "__main__":
    if patch_compute_scaling_factors():
        print("\n✅ PhysicsNeMo library patched successfully!")
        print("The compute_scaling_factors function will now save [min, max] in the correct order")
    else:
        print("\n❌ Failed to patch. Use the manual computation instead.")
