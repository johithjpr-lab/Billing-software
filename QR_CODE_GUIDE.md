# 🎯 QR Code & Scan Number Feature Guide

## Overview
Your billing system now includes automatic QR code generation and scan number creation when adding new products to stock. This makes product tracking and inventory management much more efficient.

---

## ✨ Features Added

### 1. **Automatic Scan Number Generation**
- Each product gets a unique scan number format: `SC-[TIMESTAMP]-[RANDOM]`
- Example: `SC-1706729200000-ABC12`
- Scan number is unique and includes timestamp for tracking

### 2. **QR Code Generation**
- Generates QR codes that contain:
  - Product Name
  - Product Code/Barcode
  - Rate (Price)
  - Unit of Measurement
  - Unique Scan Number
  - Shop Name
  - Timestamp

### 3. **QR Code Modal Display**
- Beautiful popup showing:
  - Large QR Code
  - Scan Number prominently displayed
  - Product Details (Name, Code, Rate, Unit)
  - Action buttons for printing, downloading, and copying

---

## 📝 How to Use

### Step 1: Open Stock Manager
1. Click the **"Stock Manager"** button in the left panel
2. Or go to the **"Quick Stock Snapshot"** card on the right and click **"Open Stock"**

### Step 2: Add Product Details
Fill in the product information:
- **Barcode / Code**: Unique product code (required)
- **Item Name**: Product name (required)
- **Unit**: pcs, kg, liter, or box
- **Rate**: Price per unit
- **Disc %**: Default discount percentage
- **Qty**: Quantity in stock
- **Min Alert**: Minimum quantity alert threshold

### Step 3: Generate QR Code & Scan Number
1. After filling product details, click the blue **"Generate QR & Scan#"** button
2. A modal will pop up showing:
   - QR Code
   - Unique Scan Number
   - Product Details

### Step 4: Use the QR Code
You can now:

#### **Print QR Code**
- Click **"Print QR & Scan#"** button
- Opens print preview with formatted QR code and scan number
- Print it and paste on the product/packaging

#### **Download QR Code**
- Click **"Download QR"** button
- Saves QR code as PNG image to your computer
- File name: `Product_QR_[SCAN_NUMBER].png`

#### **Copy Scan Number**
- Click **"Copy Scan#"** button
- Copies the scan number and product details to clipboard
- Use for records or sharing with team

### Step 5: Save Product to Stock
1. Click **"Add / Update"** button to save product to stock
2. Product will be added with all the QR/Scan info embedded

---

## 🔍 Scan Number Format Explanation

**Example**: `SC-1706729200000-ABC12`

- **SC**: Stands for "Scan Code"
- **1706729200000**: Timestamp (milliseconds) when QR was generated
- **ABC12**: 5-character random alphanumeric code

This ensures **100% uniqueness** for each product QR code.

---

## 📊 QR Code Data Structure

When someone scans the QR code, they get this JSON data:
```json
{
  "product": "Product Name",
  "code": "PROD-001",
  "rate": "500",
  "unit": "pcs",
  "scanNumber": "SC-1706729200000-ABC12",
  "timestamp": "2024-01-31T12:30:45.123Z",
  "shop": "NOW100 SUPERMART"
}
```

---

## 💡 Use Cases

### 1. **Product Labeling**
- Print QR codes and stick on product packages
- Customers can scan to verify product details
- Great for brand authenticity

### 2. **Inventory Tracking**
- Unique scan number for each product variant
- Easy tracking in your records
- Quick lookup using scan number

### 3. **POS Integration**
- Scan QR during billing to fetch product details
- Automatic price and stock information
- Faster checkout process

### 4. **Customer Trust**
- Customers can verify product authenticity
- Access to product details via QR scan
- Professional product presentation

### 5. **Barcode Alternative**
- If products don't have barcodes
- Create custom QR codes with scan numbers
- Works on any printed label

---

## 🎨 Customization Options

### Print Layout
The print preview shows:
- Product QR Code (280x280 px)
- Scan Number (Large, Bold)
- Product Details Table
- Shop Name
- Timestamp

### QR Code Settings
Current configuration:
- **Size**: 280x280 pixels
- **Color**: Green (#0b6b3a) on White
- **Error Correction**: High Level (can recover 30% damaged data)
- **Format**: PNG image

---

## 🔐 Data Security

- QR codes are generated on your browser (no server upload)
- All data stored in your browser's local storage
- No sensitive information in QR codes
- Scan numbers are unique but not sequential (harder to guess)

---

## 📱 Mobile Scanning

### Using Built-in Phone Camera
1. Open Camera app on mobile
2. Point at QR code
3. Tap notification to open data
4. See all product information

### Using QR Scanner Apps
- Google Lens
- QR Scanner
- Any barcode reader app
- Will extract the JSON product data

---

## 🚀 Advanced Tips

### Tip 1: Batch Generate QR Codes
1. Add multiple products one by one
2. Generate QR for each product
3. Print all QR codes in bulk
4. Distribute to different sections

### Tip 2: QR Code Management
- Download all QR codes and organize by category
- Store digital copies for reprinting
- Create QR code inventory spreadsheet

### Tip 3: Integration with Billing
- When scanning product QR during billing, it auto-fills details
- Scan number helps track which products were sold
- Great for analytics and reporting

### Tip 4: Mobile-Friendly
- QR codes are mobile optimized
- Works with any smartphone camera
- No app installation needed

---

## ⚙️ Technical Details

### Functions Available
- `generateProductQRCode()` - Generate QR and scan number
- `printProductQR()` - Open print preview
- `downloadProductQR()` - Download QR as PNG
- `copyToClipboard()` - Copy scan number info
- `generateScanNumber()` - Create unique scan number

### Storage
- QR data embedded in product stock item
- Stored in browser's localStorage
- Persists across sessions
- Export/Import with stock data

---

## ❓ FAQ

**Q: Can I regenerate QR code for existing product?**
A: Yes! Edit the product in Stock Manager and click "Generate QR & Scan#" again.

**Q: What if QR code is damaged/torn?**
A: The high-level error correction allows recovery of up to 30% damaged data.

**Q: Can I use QR on multiple products?**
A: Each QR has unique scan number, but you can reprint it multiple times.

**Q: What if I forget the scan number?**
A: Check your Stock Manager or exported stock files - scan number is saved with product.

**Q: Can I track sales by QR code?**
A: Yes! When billing, the product code (linked to QR) is stored in the bill.

---

## 🎯 Quick Workflow

```
1. Open Stock Manager
   ↓
2. Fill Product Details
   ↓
3. Click "Generate QR & Scan#"
   ↓
4. View/Print/Download QR
   ↓
5. Click "Add / Update" to save
   ↓
6. Label products with QR codes
   ↓
7. Scan during billing process
```

---

## 📞 Support

For issues or questions:
1. Check product is saved to stock first
2. Ensure browser supports QR generation
3. Try refreshing the page
4. Check browser console for errors

---

**Version**: 1.0  
**Last Updated**: 2024-01-31  
**Feature Status**: ✅ Active & Tested

