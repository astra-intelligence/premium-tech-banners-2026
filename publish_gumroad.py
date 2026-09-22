#!/usr/bin/env python3
import json, requests, sys

token = json.load(open('/home/paperclip/.config/gumroad/config.json'))['access_token']
pid = "6YMEnrkYUDn-yA9TC6rSag=="

desc = """# Premium Tech Banners 2026

## 7 Professional Social Media Banners for Tech Founders & Startups

Stop using generic Canva templates. Get 7 premium AI-generated banners that make your LinkedIn and Twitter/X profiles look like a top-tier tech company.

## What's Included

### LinkedIn Banners (1584 \u00d7 396 px)
- **Navy Tech Entrepreneur** \u2014 Dark navy with geometric patterns
- **SaaS Founder Purple** \u2014 Abstract waves in purple and rose gold
- **AI Startup Cyan** \u2014 Circuit-board pattern in electric blue
- **Soft Blue Lavender** \u2014 Light and airy, for executives

### Twitter/X Headers (1500 \u00d7 500 px)
- **Sunset Orange** \u2014 Gradient mountains in warm sunset tones
- **Marble Green** \u2014 Dark marble texture with green and gold accents

### Profile Background (1080 \u00d7 1080 px)
- **Slate Gray & Amber** \u2014 Minimalist geometric art

## How to Use
1. Download the ZIP file
2. Extract the PNG files
3. Upload to LinkedIn or Twitter/X settings
4. Done. Takes 30 seconds."""

# Update product with description and publish
print("=== Updating product ===")
r = requests.put(f'https://api.gumroad.com/v2/products/{pid}', data={
    'access_token': token,
    'description': desc,
    'published': 'true',
})
print(f"Update: {r.json().get('success')}")

# Upload zip file
print("\n=== Uploading ZIP ===")
zip_path = '/home/paperclip/adventure-products/banner-pack/premium-tech-banners-2026.zip'

presign = requests.post('https://api.gumroad.com/v2/files/presign', data={
    'access_token': token,
    'content_type': 'application/zip',
    'name': 'premium-tech-banners-2026.zip',
}).json()

if presign.get('success'):
    with open(zip_path, 'rb') as f:
        up = requests.put(presign['upload_url'], data=f)
    print(f"Upload status: {up.status_code}")
    
    confirm = requests.post('https://api.gumroad.com/v2/files/complete', data={
        'access_token': token,
        'upload_url': presign['upload_url'],
        'content_type': 'application/zip',
        'name': 'premium-tech-banners-2026.zip',
    }).json()
    print(f"Confirm: {confirm.get('success')}")
    
    if confirm.get('success'):
        file_url = confirm.get('file', {}).get('url', '')
        attach = requests.post(f'https://api.gumroad.com/v2/products/{pid}/files', data={
            'access_token': token,
            'url': file_url,
        }).json()
        print(f"File attached: {attach.get('success')}")

# Upload cover
print("\n=== Uploading Cover ===")
cover_path = '/home/paperclip/adventure-products/banner-pack/images/cover.png'
presign_img = requests.post('https://api.gumroad.com/v2/files/presign', data={
    'access_token': token,
    'content_type': 'image/png',
    'name': 'cover.png',
}).json()

if presign_img.get('success'):
    with open(cover_path, 'rb') as f:
        up_img = requests.put(presign_img['upload_url'], data=f)
    print(f"Cover upload: {up_img.status_code}")
    
    confirm_img = requests.post('https://api.gumroad.com/v2/files/complete', data={
        'access_token': token,
        'upload_url': presign_img['upload_url'],
        'content_type': 'image/png',
        'name': 'cover.png',
    }).json()
    
    if confirm_img.get('success'):
        img_url = confirm_img.get('file', {}).get('url', '')
        attach_img = requests.put(f'https://api.gumroad.com/v2/products/{pid}', data={
            'access_token': token,
            'preview_url': img_url,
        }).json()
        print(f"Cover attached: {attach_img.get('success')}")

# Final verification
print("\n=== Final Check ===")
r2 = requests.get(f'https://api.gumroad.com/v2/products/{pid}', data={'access_token': token})
prod = r2.json().get('product', {})
print(f"Name: {prod.get('name', '')}")
print(f"URL: https://marcometrix8.gumroad.com/l/{prod.get('custom_permalink', prod.get('permalink', 'yilxxb'))}")
print(f"Price: ${prod.get('price', 0)/100:.2f}")
print(f"Published: {prod.get('published', False)}")
print(f"Has files: {bool(prod.get('file_info', {}))}")
print(f"Preview: {'preview_url' in prod and bool(prod.get('preview_url'))}")