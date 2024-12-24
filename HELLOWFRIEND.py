import os
import subprocess
import socket
from colorama import Fore, Style, init

# Initialize colorama
init()

def banner():
    """
    عرض الشعار الخاص بالأداة.
    """
    print(Fore.CYAN + """
    مرحبا حمزة
    مرحبا حمزة
    مرحبا حمزة
                """ + Style.RESET_ALL)
    print(Fore.YELLOW + "               تم التطوير بواسطة: مُحَمَّد صَادِق أَحْمَد".center(85) + Style.RESET_ALL)
    print(Fore.MAGENTA + "--------------------------------------------------------------------------------".center(85) + Style.RESET_ALL)

def get_local_ip():
    """
    الحصول على عنوان IP المحلي للجهاز (LHOST).
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))  # عنوان وهمي للاتصال
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def save_payload_to_desktop(payload_name):
    """
    حفظ البايلود في سطح المكتب.
    """
    try:
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        payload_path = os.path.join(desktop_path, payload_name)

        # إنشاء بايلود فارغ على سطح المكتب
        with open(payload_path, 'wb') as f:
            # استخدام الترميز لكتابة البيانات غير ASCII
            f.write("محتويات البايلود الفعلي".encode('utf-8'))

        print(Fore.GREEN + f"تم حفظ البايلود في سطح المكتب: {payload_path}" + Style.RESET_ALL)
        return payload_path
    except Exception as e:
        print(Fore.RED + f"فشل حفظ البايلود: {e}" + Style.RESET_ALL)
        return None

def main():
    """
    الوظيفة الرئيسية لتشغيل الأداة.
    """
    while True:
        banner()
        print(Fore.YELLOW + """
        1. إنشاء حمولة ويندوز
        2. إنشاء حمولة أندرويد
        3. إنشاء حمولة iOS
        4. إنشاء حمولة لينكس
        5. إنشاء حمولة macOS
        6. تشفير الحمولة
        7. التحكم في الجهاز
        8. دمج البايلود مع الصورة
        9. الخروج
        """ + Style.RESET_ALL)

        choice = input(Fore.CYAN + "أدخل خيارك: " + Style.RESET_ALL)

        if choice == '1':
            # طلب اسم البايلود
            payload_name = input(Fore.YELLOW + "أدخل اسم البايلود (مثال: payload.exe): " + Style.RESET_ALL)
            payload_path = save_payload_to_desktop(payload_name)
            if payload_path:
                print(Fore.GREEN + f"تم إنشاء البايلود وحفظه في {payload_path}" + Style.RESET_ALL)

        elif choice == '2':
            # طلب اسم البايلود
            payload_name = input(Fore.YELLOW + "أدخل اسم البايلود (مثال: payload.apk): " + Style.RESET_ALL)
            payload_path = save_payload_to_desktop(payload_name)
            if payload_path:
                print(Fore.GREEN + f"تم إنشاء البايلود وحفظه في {payload_path}" + Style.RESET_ALL)

        elif choice == '3':
            # طلب اسم البايلود
            payload_name = input(Fore.YELLOW + "أدخل اسم البايلود (مثال: payload.ipa): " + Style.RESET_ALL)
            payload_path = save_payload_to_desktop(payload_name)
            if payload_path:
                print(Fore.GREEN + f"تم إنشاء البايلود وحفظه في {payload_path}" + Style.RESET_ALL)

        elif choice == '4':
            # طلب اسم البايلود
            payload_name = input(Fore.YELLOW + "أدخل اسم البايلود (مثال: payload): " + Style.RESET_ALL)
            payload_path = save_payload_to_desktop(payload_name)
            if payload_path:
                print(Fore.GREEN + f"تم إنشاء البايلود وحفظه في {payload_path}" + Style.RESET_ALL)

        elif choice == '5':
            # طلب اسم البايلود
            payload_name = input(Fore.YELLOW + "أدخل اسم البايلود (مثال: payload.macho): " + Style.RESET_ALL)
            payload_path = save_payload_to_desktop(payload_name)
            if payload_path:
                print(Fore.GREEN + f"تم إنشاء البايلود وحفظه في {payload_path}" + Style.RESET_ALL)

        elif choice == '6':
            print(Fore.CYAN + "فتح قائمة التشفير..." + Style.RESET_ALL)

        elif choice == '7':
            print(Fore.GREEN + "فتح قائمة التحكم بالجهاز..." + Style.RESET_ALL)

        elif choice == '8':
            print(Fore.CYAN + "فتح قائمة دمج البايلود مع الصورة..." + Style.RESET_ALL)

        elif choice == '9':
            print(Fore.RED + "إغلاق البرنامج..." + Style.RESET_ALL)
            break

if __name__ == "__main__":
    main()
