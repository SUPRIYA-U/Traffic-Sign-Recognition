# debug_dataset.py
import os
import shutil

def debug_dataset():
    data_dir = r"C:\Users\likhitha\Downloads\traffic-sign-recognition\data"
    
    print("🔍 DEBUG: Dataset Structure Analysis")
    print("=" * 60)
    
    # Check Train folder structure in detail
    train_dir = os.path.join(data_dir, "Train")
    print(f"\n📁 Train Folder: {train_dir}")
    print("-" * 40)
    
    if not os.path.exists(train_dir):
        print("❌ Train folder does not exist!")
        return
    
    # List everything in Train folder
    train_items = os.listdir(train_dir)
    print(f"Items in Train folder: {len(train_items)}")
    
    class_folders = []
    other_items = []
    
    for item in train_items:
        item_path = os.path.join(train_dir, item)
        if os.path.isdir(item_path):
            # Check if this looks like a class folder (numeric name)
            if item.isdigit() or (len(item) == 5 and item.isdigit()):
                images = [f for f in os.listdir(item_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                class_folders.append((item, len(images)))
            else:
                other_items.append(f"📁 {item}/ (non-class folder)")
        else:
            # Check if it's an image file
            if item.lower().endswith(('.png', '.jpg', '.jpeg')):
                other_items.append(f"📄 {item} (loose image)")
            else:
                other_items.append(f"📄 {item} (other file)")
    
    print(f"\nClass folders found: {len(class_folders)}")
    for class_name, image_count in class_folders:
        print(f"  {class_name}: {image_count} images")
    
    print(f"\nOther items: {len(other_items)}")
    for item in other_items[:10]:  # Show first 10
        print(f"  {item}")
    
    if len(class_folders) == 0:
        print("\n🚨 CRITICAL: No class folders found in Train directory!")
        print("The Train folder should contain subfolders like: 00000/, 00001/, 00002/, etc.")
        print("Each containing images for that class.")
        
        # Check if there are any images that need to be organized
        all_images = []
        for root, dirs, files in os.walk(train_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    all_images.append(os.path.join(root, file))
        
        print(f"\nTotal images found anywhere in Train folder: {len(all_images)}")
        
        if len(all_images) > 0:
            print("\n🎯 Images found but not organized. Need to organize them into class folders!")
            organize_images(all_images, train_dir)

def organize_images(image_paths, train_dir):
    """Organize loose images into class folders"""
    print(f"\n🔧 Organizing {len(image_paths)} images...")
    
    for img_path in image_paths:
        filename = os.path.basename(img_path)
        
        # Try to extract class ID from filename (common GTSRB patterns)
        class_id = None
        
        # Pattern 1: 00000_00000_00000.png
        if '_' in filename:
            parts = filename.split('_')
            if parts[0].isdigit():
                class_id = parts[0]
        
        # Pattern 2: 00000.png
        if class_id is None and filename.split('.')[0].isdigit():
            class_id = filename.split('.')[0]
        
        # Pattern 3: Use folder name if image is in a class folder
        if class_id is None:
            parent_dir = os.path.basename(os.path.dirname(img_path))
            if parent_dir.isdigit():
                class_id = parent_dir
        
        if class_id:
            # Create class folder and move image
            class_folder = os.path.join(train_dir, class_id.zfill(5))
            os.makedirs(class_folder, exist_ok=True)
            
            dest_path = os.path.join(class_folder, filename)
            shutil.move(img_path, dest_path)
            print(f"✅ Moved {filename} to class {class_id.zfill(5)}")
        else:
            print(f"❓ Could not determine class for: {filename}")

def check_test_folder():
    data_dir = r"C:\Users\likhitha\Downloads\traffic-sign-recognition\data"
    test_dir = os.path.join(data_dir, "Test")
    
    print(f"\n📁 Test Folder: {test_dir}")
    print("-" * 40)
    
    if os.path.exists(test_dir):
        class_folders = [f for f in os.listdir(test_dir) if os.path.isdir(os.path.join(test_dir, f)) and (f.isdigit() or len(f) == 5)]
        total_images = 0
        
        print(f"Class folders in Test: {len(class_folders)}")
        for class_folder in sorted(class_folders)[:5]:
            class_path = os.path.join(test_dir, class_folder)
            images = [f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            total_images += len(images)
            print(f"  {class_folder}: {len(images)} images")
        
        print(f"Total test images: {total_images}")
    else:
        print("❌ Test folder not found!")

if __name__ == "__main__":
    debug_dataset()
    check_test_folder()
    
    print("\n" + "=" * 60)
    print("✅ Debug completed!")
    print("\nIf Train folder has images but no class folders,")
    print("they need to be organized into numeric subfolders.")