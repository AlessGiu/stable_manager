# 🐴 Stable Manager - Odoo Equestrian Management Module

**Stable Manager** is a complete equestrian management module for Odoo, designed for horse owners, riders, stable managers, and equestrian centers.  
It helps track your horses' essential data, organize competitions, manage feeding routines, and ensure up-to-date veterinary care.

---

## 🚀 Features

### 🐎 Horse Management
- Complete horse profiles (age, sex, breed, coat, height, weight)
- SIRE number, microchip status, photo
- Owner assignment
- Automatic age calculation
- Smart dashboard with "In Competition" ribbon and statistical buttons

### 🧾 Feeding & Nutrition
- Link horses to feeding plans (Odoo MRP compatibility)
- Track feed stock through Odoo Inventory

### 🏆 Competition Tracking
- Log competition date, level, discipline, result, penalties, time
- Emotional feedback, performance review, improvement notes
- Attach photos or documents
- View yearly statistics
- Competitions automatically linked to horses with activity messages

### 🩺 Health & Care
- Veterinary, osteopathy, dentistry, farrier, vaccines
- History per horse
- Tabs for quick access to medical data

### 📁 Reporting & Attachments
- Export horse profile as PDF
- Upload competition media and veterinary documents

### 📊 User Interface
- Clean form views with tabs and groups
- Kanban, list, and form views for horses and competitions
- Filters for in-competition horses, feed type, health status

---

## 📸 Screenshots

*(Add images to `static/description/` and uncomment in manifest)*

---

## 🔧 Installation

1. Copy the `stable_manager/` folder into your Odoo `addons` directory.
2. Make sure your database has the required modules installed:
   - `base`, `mail`, `stock`, `mrp`, `sale`
3. Restart Odoo and activate developer mode.
4. Go to **Apps**, click **Update Apps List**, then install **Stable Manager**.

---

## 🛠 Dependencies

This module depends on the following Odoo core modules:

- `base`
- `mail`
- `stock`
- `mrp`
- `sale`

---

## 🧪 Testing & Usage Tips

- Use the included sample data to test the module.
- Create a few horses, competitions, and vet records to explore features.
- Use filters in kanban/list views to find horses with no microchip, or only those in competition.

---

## 🌐 Website & Support

**Author:** Alessandro Pollice  
**Website:** [lesecuriesdelm.be](https://www.lesecuriesdelm.be)  
**Support:** support@lesecuriesdelm.be *(or customize this line)*

---

## 📄 License

Licensed under the **LGPL-3.0**. See [LICENSE](https://www.gnu.org/licenses/lgpl-3.0.en.html) for details.

---

## ❤️ Contribution

Pull requests, feedback and feature requests are welcome!  
Feel free to fork this project, improve it or adapt it to your stable's specific needs.

