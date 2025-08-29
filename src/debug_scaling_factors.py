# debug_scaling_factors.py
import numpy as np
import os
import sys
sys.path.append('/workspace/domino/src')

# Let's trace through the actual function
from physicsnemo.datapipes.cae.domino_datapipe import compute_scaling_factors
import hydra
from omegaconf import DictConfig, OmegaConf

# Load the config
@hydra.main(version_base="1.3", config_path="conf", config_name="config")
def debug_scaling(cfg: DictConfig):
    print("="*60)
    print("DEBUGGING SCALING FACTOR COMPUTATION")
    print("="*60)
    
    # Check what the function actually does
    print("\n1. Calling compute_scaling_factors...")
    print(f"   Input path: {cfg.data.input_dir}")
    print(f"   Use cache: {cfg.data_processor.use_cache}")
    
    # Let's manually check what's in the scaling factors file
    vol_save_path = os.path.join("outputs", cfg.project.name, "volume_scaling_factors.npy")
    surf_save_path = os.path.join("outputs", cfg.project.name, "surface_scaling_factors.npy")
    
    print(f"\n2. Checking existing scaling factor files:")
    print(f"   Volume path: {vol_save_path}")
    print(f"   Surface path: {surf_save_path}")
    
    if os.path.exists(surf_save_path):
        surf_factors = np.load(surf_save_path)
        print(f"\n   Loaded surface factors shape: {surf_factors.shape}")
        print(f"   Row 0 (should be min): {surf_factors[0]}")
        print(f"   Row 1 (should be max): {surf_factors[1]}")
        
        # Check if they're swapped
        if np.any(surf_factors[0] > surf_factors[1]):
            print("\n   ❌ FACTORS ARE INVERTED! Min > Max")
        else:
            print("\n   ✅ Factors look correct")
    
    # Let's also manually compute to compare
    print("\n3. Manually computing from data files...")
    data_dir = cfg.data.input_dir
    files = [f for f in os.listdir(data_dir) if f.endswith('.npy')][:10]  # Just check 10 files
    
    global_min = None
    global_max = None
    
    for file in files:
        data = np.load(os.path.join(data_dir, file), allow_pickle=True).item()
        if 'surface_fields' in data and data['surface_fields'] is not None:
            surf_fields = data['surface_fields']
            file_min = np.min(surf_fields, axis=0)
            file_max = np.max(surf_fields, axis=0)
            
            print(f"\n   File {file}:")
            print(f"      Min: {file_min}")
            print(f"      Max: {file_max}")
            
            if global_min is None:
                global_min = file_min
                global_max = file_max
            else:
                global_min = np.minimum(global_min, file_min)
                global_max = np.maximum(global_max, file_max)
    
    print(f"\n   Computed global min: {global_min}")
    print(f"   Computed global max: {global_max}")
    
    return surf_factors, global_min, global_max

if __name__ == "__main__":
    debug_scaling()
