# fix_scaling_factors_correctly.py
import numpy as np
import os
from tqdm import tqdm

def compute_and_save_correct_scaling_factors():
    """Compute and save scaling factors in the CORRECT order [min, max]"""
    
    train_dir = "/workspace/outputs/processed/surface_fine/train/"
    output_dir = "/workspace/outputs/ahmed_baseline/"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    files = [f for f in os.listdir(train_dir) if f.endswith('.npy')]
    print(f"Computing scaling factors from {len(files)} files...")
    
    global_min = None
    global_max = None
    
    # Process first 20 files (as the original function does)
    for i, file in enumerate(tqdm(files[:20], desc="Processing files")):
        data = np.load(os.path.join(train_dir, file), allow_pickle=True).item()
        
        if 'surface_fields' in data and data['surface_fields'] is not None:
            surf_fields = data['surface_fields']
            
            # Remove outliers (similar to mean_std_sampling in original)
            mean = np.mean(surf_fields, axis=0)
            std = np.std(surf_fields, axis=0)
            # Keep points within 12 std deviations
            mask = np.all(np.abs(surf_fields - mean) < 12 * std, axis=1)
            surf_fields_filtered = surf_fields[mask]
            
            if i == 0:
                global_min = np.min(surf_fields_filtered, axis=0)
                global_max = np.max(surf_fields_filtered, axis=0)
            else:
                global_min = np.minimum(global_min, np.min(surf_fields_filtered, axis=0))
                global_max = np.maximum(global_max, np.max(surf_fields_filtered, axis=0))
    
    print(f"\nComputed scaling factors:")
    print(f"  Global min: {global_min}")
    print(f"  Global max: {global_max}")
    
    # Save in CORRECT format - [min, max] as rows
    surface_factors_correct = np.array([global_min, global_max])
    
    surf_path = os.path.join(output_dir, "surface_scaling_factors.npy")
    np.save(surf_path, surface_factors_correct)
    print(f"\nSaved CORRECT factors to: {surf_path}")
    
    # Verify
    loaded = np.load(surf_path)
    print(f"\nVerification:")
    print(f"  Shape: {loaded.shape}")
    print(f"  Row 0 (min): {loaded[0]}")
    print(f"  Row 1 (max): {loaded[1]}")
    
    # Check each component
    all_correct = True
    for i in range(loaded.shape[1]):
        if loaded[0][i] >= loaded[1][i]:
            print(f"  ❌ Component {i}: min >= max!")
            all_correct = False
        else:
            print(f"  ✅ Component {i}: min < max ✓")
    
    if all_correct:
        print("\n✅ All scaling factors are correct!")
    else:
        print("\n❌ Some scaling factors are still wrong!")
    
    return surface_factors_correct

if __name__ == "__main__":
    factors = compute_and_save_correct_scaling_factors()
