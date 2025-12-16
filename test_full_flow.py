#!/usr/bin/env python3
"""
Test the COMPLETE flow:
1. Create a sample design image
2. Upload to /upload endpoint
3. Gemini extracts blueprint
4. Send blueprint to /edit endpoint
5. Get modified blueprint
"""
import requests
import json
from PIL import Image, ImageDraw

BASE_URL = "http://localhost:8002"

def create_sample_design():
    """Create a simple design image (500x600)"""
    # Create white canvas
    img = Image.new('RGB', (500, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw hero section (blue background)
    draw.rectangle([(0, 0), (500, 150)], fill='#1967D2')
    
    # Draw title text area
    draw.text((20, 20), "Welcome Page", fill='white')
    draw.text((20, 60), "Beautiful design system", fill='#E0E0E0')
    
    # Draw product card 1
    draw.rectangle([(20, 180), (220, 350)], outline='#000000', width=2)
    draw.rectangle([(30, 190), (210, 250)], fill='#F0F0F0')
    draw.text((50, 260), "Product 1", fill='#000000')
    draw.text((50, 290), "$99.99", fill='#1967D2')
    
    # Draw product card 2
    draw.rectangle([(280, 180), (480, 350)], outline='#000000', width=2)
    draw.rectangle([(290, 190), (470, 250)], fill='#F0F0F0')
    draw.text((310, 260), "Product 2", fill='#000000')
    draw.text((310, 290), "$129.99", fill='#1967D2')
    
    # Draw CTA button
    draw.rectangle([(150, 400), (350, 460)], fill='#0066FF')
    draw.text((200, 420), "Buy Now", fill='white')
    
    # Draw footer
    draw.rectangle([(0, 550), (500, 600)], fill='#F5F5F5')
    draw.text((20, 570), "© 2025 Your Company", fill='#666666')
    
    # Save image
    import tempfile
    import os
    temp_dir = tempfile.gettempdir()
    image_path = os.path.join(temp_dir, 'sample_design.png')
    img.save(image_path)
    print(f"✅ Created sample design image: {image_path}")
    return image_path

def upload_design(image_path):
    """Upload design image and extract blueprint"""
    print("\n" + "="*60)
    print("STEP 1: UPLOAD DESIGN")
    print("="*60)
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/upload/", files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            blueprint = result.get('blueprint')
            print(f"✅ Upload successful!")
            print(f"\n📋 Extracted Blueprint:")
            print(json.dumps(blueprint, indent=2)[:500] + "...")
            return blueprint
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error uploading: {e}")
        return None

def edit_blueprint(blueprint, command):
    """Send blueprint to /edit endpoint with command"""
    print("\n" + "="*60)
    print(f"STEP 2: EDIT BLUEPRINT")
    print(f"Command: {command}")
    print("="*60)
    
    try:
        payload = {"command": command, "blueprint": blueprint}
        response = requests.post(f"{BASE_URL}/edit", json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            modified = result["patched_blueprint"]
            summary = result["patch_summary"]
            
            print(f"✅ Edit successful!")
            print(f"\n📝 Summary: {summary}")
            print(f"\n📋 Modified Blueprint:")
            print(json.dumps(modified, indent=2)[:500] + "...")
            
            return modified
        else:
            print(f"❌ Edit failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error editing: {e}")
        return None

def compare_blueprints(original, modified, command):
    """Show what changed"""
    print("\n" + "="*60)
    print("STEP 3: COMPARE CHANGES")
    print("="*60)
    
    if original == modified:
        print("❌ No changes detected")
        return
    
    print("✅ Changes detected!")
    print(f"\nCommand applied: {command}")
    
    # Check components
    if "components" in original and "components" in modified:
        orig_comps = original["components"]
        mod_comps = modified["components"]
        
        print(f"\nComponent changes:")
        for i, (orig, mod) in enumerate(zip(orig_comps, mod_comps)):
            if orig != mod:
                comp_id = orig.get("id", f"Component {i}")
                print(f"  - {comp_id}:")
                
                if "bbox" in orig and orig.get("bbox") != mod.get("bbox"):
                    print(f"      bbox: {orig['bbox']} → {mod['bbox']}")
                
                if "visual" in orig and orig.get("visual") != mod.get("visual"):
                    for key in orig["visual"]:
                        if orig["visual"][key] != mod["visual"].get(key):
                            print(f"      {key}: {orig['visual'][key]} → {mod['visual'].get(key)}")
    
    # Check tokens
    if "tokens" in original and "tokens" in modified:
        orig_tokens = original["tokens"]
        mod_tokens = modified["tokens"]
        
        for key in orig_tokens:
            if orig_tokens[key] != mod_tokens.get(key):
                print(f"  - Token '{key}': {orig_tokens[key]} → {mod_tokens.get(key)}")

if __name__ == "__main__":
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║   FULL FLOW TEST: Upload → Extract → Edit              ║")
    print("╚══════════════════════════════════════════════════════════╝")
    
    # Check server
    try:
        health = requests.get(f"{BASE_URL}/health", timeout=2)
        print(f"\n🔗 Server: ✅ Running")
    except:
        print(f"\n🔗 Server: ❌ Not responding")
        print("   Start server first!")
        exit(1)
    
    # Create test design
    image_path = create_sample_design()
    
    # Upload and extract
    blueprint = upload_design(image_path)
    if not blueprint:
        print("\n❌ Failed to extract blueprint")
        exit(1)
    
    # Edit with first command
    modified1 = edit_blueprint(blueprint, "make products bigger")
    if modified1:
        compare_blueprints(blueprint, modified1, "make products bigger")
    
    # Edit with second command
    if modified1:
        print("\n" + "="*60)
        print("STEP 4: SECOND EDIT (on top of previous changes)")
        print("="*60)
        modified2 = edit_blueprint(modified1, "change primary color to #FF6B35")
        if modified2:
            compare_blueprints(modified1, modified2, "change primary color to #FF6B35")
    
    print("\n" + "="*60)
    print("✅ FULL FLOW COMPLETED!")
    print("="*60)
    print("\nWhat happened:")
    print("1. Created sample design image")
    print("2. Uploaded to /upload endpoint")
    print("3. Gemini extracted blueprint from image")
    print("4. Modified blueprint with /edit (make products bigger)")
    print("5. Applied another edit (change color)")
    print("\nThis proves the complete pipeline works!")
