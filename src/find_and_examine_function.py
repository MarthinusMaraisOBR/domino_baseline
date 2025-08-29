# find_and_examine_function.py
import inspect
import sys
sys.path.append('/workspace/domino/src')

try:
    from physicsnemo.datapipes.cae.domino_datapipe import compute_scaling_factors
    
    print("="*60)
    print("FOUND compute_scaling_factors")
    print("="*60)
    
    # Get the source code
    source = inspect.getsource(compute_scaling_factors)
    print("\nFunction source code:")
    print(source)
    
    # Get the file location
    import physicsnemo.datapipes.cae.domino_datapipe as module
    print(f"\nFunction location: {module.__file__}")
    
except Exception as e:
    print(f"Error: {e}")
    
    # Try alternative import
    print("\nTrying to locate manually...")
    import os
    for root, dirs, files in os.walk("/workspace"):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r') as f:
                        if "def compute_scaling_factors" in f.read():
                            print(f"Found in: {filepath}")
                            # Read and print the function
                            f.seek(0)
                            lines = f.readlines()
                            for i, line in enumerate(lines):
                                if "def compute_scaling_factors" in line:
                                    print("\nFunction content:")
                                    # Print function (up to 50 lines)
                                    for j in range(i, min(i+50, len(lines))):
                                        print(lines[j], end='')
                                        if lines[j].strip() and not lines[j].startswith(' ') and j > i+5:
                                            break
                                    break
                            break
                except:
                    continue
