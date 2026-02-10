def get_text(lang):
    translations = {
        "English": {
            "title": "Tailor Master Pro",
            "welcome": "Welcome",
            "dashboard": "📊 Dashboard",
            "new_order": "🧵 New Order",
            "all_orders": "📦 All Orders",
            "accounts": "💰 Accounts",
            "cust_name": "Customer Name",
            "phone": "Phone Number",
            "measure": "Measurements",
            "total": "Total Bill",
            "advance": "Advance",
            "rem": "Remaining",
            "save": "Save Order",
            "sync": "Sync to Cloud",
            "success": "Order Saved Successfully!",
            "offline": "Working Offline (Local Mode)",
            "role_admin": "Admin",
            "role_staff": "Staff"
        },
        "Roman Urdu": {
            "title": "Tailor Master Pro",
            "welcome": "Khush-Aamdeed",
            "dashboard": "📊 Dashboard",
            "new_order": "🧵 Naya Order",
            "all_orders": "📦 Tamam Orders",
            "accounts": "💰 Hisab Kitab",
            "cust_name": "Gahak ka Naam",
            "phone": "Mobile Number",
            "measure": "Paimaish (Measurements)",
            "total": "Kul Bill",
            "advance": "Advance Adaigi",
            "rem": "Baqi Raqam",
            "save": "Order Save Karein",
            "sync": "Cloud par bhejein",
            "success": "Order Save Ho Gaya!",
            "offline": "Internet nahi hai (Local Mode)",
            "role_admin": "Baray Sahab",
            "role_staff": "Karigar"
        },
        "Sindhi": {
            "title": "ٽيلر ماسٽر پرو",
            "welcome": "ڀلي ڪري آيا",
            "dashboard": "📊 ڊيش بورڊ",
            "new_order": "🧵 نئون آرڊر",
            "all_orders": "📦 سمورا آرڊر",
            "accounts": "💰 حساب ڪتاب",
            "cust_name": "گراهڪ جو نالو",
            "phone": "فون نمبر",
            "measure": "ماپ (Measurements)",
            "total": "ڪل بل",
            "advance": "ايڊوانس",
            "rem": "باقي رقم",
            "save": "آرڊر محفوظ ڪريو",
            "sync": "ڪلائوڊ تي موڪليو",
            "success": "آرڊر ڪاميابيءَ سان محفوظ ٿي ويو!",
            "offline": "انٽرنيٽ ناهي (لوڪل موڊ)",
            "role_admin": "ايڊمن",
            "role_staff": "اسٽاف"
        }
    }
    
    # Default English return karega agar lang na mile
    return translations.get(lang, translations["English"])
