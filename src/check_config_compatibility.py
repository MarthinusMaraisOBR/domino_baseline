# check_config_compatibility.py
import yaml
import sys
sys.path.append('/workspace/domino/src')

# Load config
with open('conf/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

print("Checking config compatibility...")

# Check for surface-only model specific settings
model_type = config['model']['model_type']
print(f"\n1. Model type: {model_type}")

if model_type == 'surface':
    # For surface-only, we shouldn't need volume-specific configs
    print("   ✓ Surface-only model detected")
    
    # Check if volume variables are properly excluded
    if 'volume' in config['variables']:
        if config['variables']['volume'] is None or not config['variables']['volume']:
            print("   ✓ Volume variables properly set to None/empty")
        else:
            print("   ⚠ Warning: Volume variables defined but model is surface-only")
    
    # Check volume sampling is 0
    if config['model']['volume_points_sample'] == 0:
        print("   ✓ Volume points sampling set to 0")
    else:
        print(f"   ⚠ Warning: volume_points_sample is {config['model']['volume_points_sample']}, should be 0 for surface-only")
        config['model']['volume_points_sample'] = 0

# Check required fields for geometry_rep
required_geo_fields = ['hops', 'base_neurons', 'activation']
geo_config = config['model']['geometry_rep']['geo_conv']

print("\n2. Checking geometry_rep.geo_conv fields:")
for field in required_geo_fields:
    if field in geo_config:
        print(f"   ✓ {field}: {geo_config.get(field, 'NOT FOUND')}")
    else:
        print(f"   ✗ Missing: {field}")
        # Add default values
        if field == 'hops':
            geo_config['hops'] = 1
            print(f"     Added default: {field} = 1")

# Save corrected config
with open('conf/config_corrected.yaml', 'w') as f:
    yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
print("\n✓ Corrected config saved to conf/config_corrected.yaml")
print("\nTo use it, run:")
print("  python train.py --config-name=config_corrected")
