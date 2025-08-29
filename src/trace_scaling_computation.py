# trace_scaling_computation.py
import numpy as np
import os
import sys
sys.path.append('/workspace/domino/src')

# Let's manually call compute_scaling_factors like train.py does
from physicsnemo.datapipes.cae.domino_datapipe import compute_scaling_factors
import hydra
from omegaconf import DictConfig, OmegaConf

@hydra.main(version_base="1.3", config_path="conf", config_name="config")
def trace_scaling(cfg: DictConfig):
    print("="*60)
    print("TRACING SCALING FACTOR COMPUTATION")
    print("="*60)
    
    print(f"\nConfig values:")
    print(f"  cfg.data.input_dir: {cfg.data.input_dir}")
    print(f"  cfg.data_processor.use_cache: {cfg.data_processor.use_cache}")
    print(f"  cfg.project.name: {cfg.project.name}")
    
    # This is what train.py calls
    print(f"\nCalling compute_scaling_factors...")
    compute_scaling_factors(
        cfg=cfg,
        input_path=cfg.data.input_dir,
        use_cache=cfg.data_processor.use_cache,
    )
    
    # Now check what was created
    vol_save_path = os.path.join("outputs", cfg.project.name, "volume_scaling_factors.npy")
    surf_save_path = os.path.join("outputs", cfg.project.name, "surface_scaling_factors.npy")
    
    print(f"\nChecking created files:")
    
    if os.path.exists(surf_save_path):
        surf_factors = np.load(surf_save_path)
        print(f"\n✓ Surface factors created:")
        print(f"  Shape: {surf_factors.shape}")
        print(f"  Row 0: {surf_factors[0]}")
        print(f"  Row 1: {surf_factors[1]}")
        
        # Check each component
        for i in range(surf_factors.shape[1]):
            if surf_factors[0][i] > surf_factors[1][i]:
                print(f"  ❌ Component {i}: min ({surf_factors[0][i]}) > max ({surf_factors[1][i]})")
            else:
                print(f"  ✓ Component {i}: min ({surf_factors[0][i]}) < max ({surf_factors[1][i]})")
    else:
        print(f"  ❌ Surface factors file NOT created at {surf_save_path}")
    
    if os.path.exists(vol_save_path):
        print(f"\n  Note: Volume factors also created (shouldn't be needed for Ahmed)")

if __name__ == "__main__":
    trace_scaling()
