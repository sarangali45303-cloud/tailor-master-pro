def get_text(lang):
    translations = {
        "English": {"title": "Main Menu", "new_order": "New Order", "save": "Save"},
        "Roman Urdu": {"title": "Asli Menu", "new_order": "Naya Order", "save": "Save Karein"},
        "Sindhi": {"title": "مين مينيو", "new_order": "نئون آرڊر", "save": "محفوظ ڪريو"}
    }
    return translations.get(lang, translations["English"])
    def get_translation(lang):
    translations = {
        "English": {
            "welcome": "Welcome", "new_order": "New Order", "cust_name": "Customer Name",
            "role_admin": "Admin", "role_staff": "Staff"
        },
        "Roman Urdu": {
            "welcome": "Khush-Aamdeed", "new_order": "Naya Order", "cust_name": "Gahak ka Naam",
            "role_admin": "Baray Sahab", "role_staff": "Karigar"
        },
        "Sindhi": {
            "welcome": "ڀلي ڪري آيا", "new_order": "نئون آرڊر", "cust_name": "گراهڪ جو نالو",
            "role_admin": "ايڊمن", "role_staff": "اسٽاف"
        }
    }
    return translations.get(lang, translations["English"])
def get_text(lang):
    translations = {
        "English": {
            "title": "Tailor Master Pro",
            "new_order": "🧵 New Order",
            "cust_name": "Customer Name",
            "phone": "Phone Number",
            "measure": "Measurements",
            "total": "Total Bill",
            "advance": "Advance",
            "rem": "Remaining",
            "save": "Save Order",
            "sync": "Sync to Cloud",
            "success": "Order Saved Successfully!",
            "offline": "Working Offline (Local Mode)"
        },
        "Roman Urdu": {
            "title": "Tailor Master Pro",
            "new_order": "🧵 Naya Order",
            "cust_name": "Gahak ka Naam",
            "phone": "Mobile Number",
            "measure": "Paimaish (Measurements)",
            "total": "Kul Bill",
            "advance": "Advance Adaigi",
            "rem": "Baqi Raqam",
            "save": "Order Save Karein",
            "sync": "Cloud par bhejein",
            "success": "Order Save Ho Gaya!",
            "offline": "Internet nahi hai (Local Kaam jari hai)"
        },
        "Sindhi": {
            "title": "ٽيلر ماسٽر پرو",
            "new_order": "🧵 نئون آرڊر",
            "cust_name": "گراهڪ جو نالو",
            "phone": "فون نمبر",
            "measure": "ماپ (Measurements)",
            "total": "ڪل بل",
            "advance": "ايڊوانس",
            "rem": "باقي رقم",
            "save": "آرڊر سيو ڪريو",
            "sync": "ڪلائوڊ تي موڪليو",
            "success": "آرڊر ڪاميابيءَ سان محفوظ ٿي ويو!",
            "offline": "انٽرنيٽ ناهي (لوڪل ڪم جاري آهي)"
        }
    }

    return translations.get(lang, translations["English"])
