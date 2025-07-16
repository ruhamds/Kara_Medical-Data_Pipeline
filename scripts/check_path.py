import os

media_path = r"C:\Users\Antifragile\Desktop\Kara_Medical Data_Pipeline\data\raw\telegram_messages\2025-07-12\lobelia4cosmetics\media_18523.jpg"

print(f"🖼 Checking if exists: {media_path}")
print("✅ Exists" if os.path.exists(media_path) else "❌ Missing")
