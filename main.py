# import os
# import socket
# import zipfile
# import urllib.request
# import subprocess
# import time
# import mysql.connector
# import urllib.error
#
# # ---------------- CONFIG ----------------
# MYSQL_SERVER_URL = "https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-8.0.43-winx64.zip"
# MYSQL_WORKBENCH_URL = "https://cdn.mysql.com/Downloads/MySQLGUITools/mysql-workbench-community-8.0.43-winx64.msi"
# MYSQL_SHELL_URL = "https://cdn.mysql.com/Downloads/MySQL-Shell/mysql-shell-9.4.0-windows-x86-64bit.msi"
#
# MYSQL_DIR = "C:\\mysql"
# MYSQL_ROOT_PASSWORD = "SPI12345"
# DB_NAME = "ChemChef"
#
# ADMIN_USER = "chemchef_user"
# ADMIN_PASS = "spi12345"
# ERP_USER = "erp_user"
# ERP_PASS = "erp123"
#
# # Connection details for normal use
# HOST = socket.gethostbyname(socket.gethostname())
# CONNECT_USER = ADMIN_USER
# CONNECT_PASS = ADMIN_PASS
# # ----------------------------------------
#
# MYSQL_VERSION = "8.0.43"
# BIN_DIR = os.path.join(MYSQL_DIR, f"mysql-{MYSQL_VERSION}-winx64", "bin")
#
# DATADIR = os.path.join(MYSQL_DIR, "data")
#
# # ---------------- Helper Functions ----------------
#
# def download_file(url, filename):
#     try:
#         print(f"⬇️ Downloading {filename} …")
#         urllib.request.urlretrieve(url, filename)
#         print(f"✅ Downloaded {filename}")
#         return True
#     except urllib.error.HTTPError as e:
#         print(f"❌ Failed to download {filename}: HTTP Error {e.code} — {e.reason}")
#         return False
#     except Exception as e:
#         print(f"❌ Failed to download {filename}: {e}")
#         return False
#
# def install_msi(filename):
#     try:
#         print(f"📦 Installing {filename} ...")
#         subprocess.run(["msiexec", "/i", filename, "/quiet", "/norestart"], check=True)
#         print(f"✅ {filename} installed.")
#     except subprocess.CalledProcessError as e:
#         print(f"❌ Error installing {filename}: {e}")
#
# # ---------------- MySQL Setup ----------------
#
# def setup_mysql_server():
#     if not os.path.exists(BIN_DIR):
#         print("MySQL Server not found. Installing...")
#         zip_path = "mysql_server.zip"
#         if not download_file(MYSQL_SERVER_URL, zip_path):
#             print("❌ Failed to download MySQL server. Please download manually from:")
#             print("   https://dev.mysql.com/downloads/mysql/")
#             exit()
#         with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#             zip_ref.extractall(MYSQL_DIR)
#         os.remove(zip_path)
#         print("✅ MySQL Server extracted.")
#
#         # Initialize database
#         if not os.path.exists(DATADIR):
#             os.makedirs(DATADIR)
#         subprocess.run([os.path.join(BIN_DIR, "mysqld.exe"),
#                         "--initialize-insecure", f"--datadir={DATADIR}"], check=True)
#         print("✅ MySQL initialized with no root password.")
#     else:
#         print("ℹ️ MySQL Server already exists. Skipping install.")
#
# def start_mysql():
#     if not os.path.exists(BIN_DIR):
#         print("❌ MySQL binaries not found. Cannot start server.")
#         exit()
#     print("🚀 Starting MySQL server...")
#     proc = subprocess.Popen([os.path.join(BIN_DIR, "mysqld.exe"), f"--datadir={DATADIR}"])
#     time.sleep(12)  # give server time to start
#     return proc
#
# def setup_database_and_users():
#     # Try connecting with no password first, then with root password
#     try:
#         conn = mysql.connector.connect(user="root", password="", host="127.0.0.1")
#     except:
#         conn = mysql.connector.connect(user="root", password=MYSQL_ROOT_PASSWORD, host="127.0.0.1")
#     cursor = conn.cursor()
#
#     # Set root password and allow remote access
#     try:
#         cursor.execute(f"ALTER USER 'root'@'localhost' IDENTIFIED BY '{MYSQL_ROOT_PASSWORD}'")
#     except:
#         print("ℹ️ Root password already set for localhost.")
#     try:
#         cursor.execute(f"CREATE USER IF NOT EXISTS 'root'@'%' IDENTIFIED BY '{MYSQL_ROOT_PASSWORD}'")
#     except:
#         print("ℹ️ Root user for all hosts already exists.")
#     cursor.execute(f"GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION")
#
#     # Create database
#     cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
#
#     # Create admin user with full privileges on DB
#     cursor.execute(f"CREATE USER IF NOT EXISTS '{ADMIN_USER}'@'%' IDENTIFIED BY '{ADMIN_PASS}'")
#     cursor.execute(f"GRANT ALL PRIVILEGES ON {DB_NAME}.* TO '{ADMIN_USER}'@'%'")
#
#     # Create insert-only user
#     cursor.execute(f"CREATE USER IF NOT EXISTS '{ERP_USER}'@'%' IDENTIFIED BY '{ERP_PASS}'")
#     cursor.execute(f"GRANT INSERT ON {DB_NAME}.* TO '{ERP_USER}'@'%'")
#
#     cursor.execute("FLUSH PRIVILEGES")
#     conn.commit()
#     cursor.close()
#     conn.close()
#     print("✅ Database and users configured (root, admin, ERP with '%' host access).")
#
# # ---------------- Table Check ----------------
#
# def check_and_create_table():
#     """Check if any tables exist in DB, if not create one default table."""
#     conn = mysql.connector.connect(user=CONNECT_USER, password=CONNECT_PASS, host=HOST, database=DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute("SHOW TABLES;")
#     tables = cursor.fetchall()
#
#     if tables:
#         print(f"ℹ️ Tables already exist in {DB_NAME}: {[t[0] for t in tables]}")
#     else:
#         print(f"⚠️ No tables found in {DB_NAME}. Creating default table...")
#         cursor.execute("""
#             CREATE TABLE BatchChemical (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 BatchName VARCHAR(255) NOT NULL,
#                 MachineName VARCHAR(255) NOT NULL,
#                 FabricWt REAL NOT NULL,
#                 MLR REAL NOT NULL,
#                 Operator VARCHAR(255) NOT NULL,
#                 GroupNo INT NOT NULL,
#                 SeqNo INT NOT NULL,
#                 ChemID INT NOT NULL,
#                 TargetWt REAL NOT NULL,
#                 AfterWash TINYINT NOT NULL,
#                 TargetTank VARCHAR(255) NOT NULL,
#                 RequestType VARCHAR(255) NOT NULL,
#                 DispenseMachine VARCHAR(255) NOT NULL,
#                 UserName VARCHAR(255) NOT NULL
#             )
#         """)
#         conn.commit()
#         print("✅ Default table `BatchChemical` created.")
#
#     cursor.close()
#     conn.close()
#
# # ---------------- Optional Workbench & Shell ----------------
#
# def install_workbench():
#     dest_folder = r"C:\Program Files\MySQL\MySQL Workbench 8.0 CE"
#     if os.path.exists(dest_folder):
#         print("ℹ️ Workbench already exists. Skipping.")
#         return
#     print("📥 Installing Workbench...")
#     if download_file(MYSQL_WORKBENCH_URL, "mysql_workbench.msi"):
#         install_msi("mysql_workbench.msi")
#     else:
#         print("❌ Workbench installation skipped.")
#
# def install_shell():
#     dest_folder = r"C:\Program Files\MySQL\MySQL Shell 8.0"
#     if os.path.exists(dest_folder):
#         print("ℹ️ MySQL Shell already exists. Skipping.")
#         return
#     print("📥 Installing MySQL Shell...")
#     if download_file(MYSQL_SHELL_URL, "mysql_shell.msi"):
#         install_msi("mysql_shell.msi")
#     else:
#         print("❌ MySQL Shell installation skipped.")
#
# # ---------------- Main Execution ----------------
#
# if __name__ == "__main__":
#     setup_mysql_server()
#     proc = start_mysql()
#     setup_database_and_users()
#     check_and_create_table()
#     install_workbench()
#     install_shell()
#
#     print("\n Setup finished:")
#     print(f"   Database: {DB_NAME}")
#     print(f"   Admin: {ADMIN_USER}/{ADMIN_PASS}")
#     print(f"   ERP: {ERP_USER}/{ERP_PASS}")
#     print(f"   Host: {HOST}")
#
#     # Give a short delay then stop server (or remove to keep running)
#     time.sleep(5)
#     proc.terminate()
import os
import socket
import zipfile
import urllib.request
import subprocess
import time
import mysql.connector
from mysql.connector import Error
import ctypes

# ---------------- CONFIG ----------------
MYSQL_SERVER_URL = "https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-8.0.43-winx64.zip"
MYSQL_WORKBENCH_URL = "https://cdn.mysql.com/Downloads/MySQLGUITools/mysql-workbench-community-8.0.43-winx64.msi"
MYSQL_SHELL_URL = "https://cdn.mysql.com/Downloads/MySQL-Shell/mysql-shell-9.4.0-windows-x86-64bit.msi"

MYSQL_DIR = r"C:\mysql"
DATADIR = os.path.join(MYSQL_DIR, "data")
MY_INI = os.path.join(MYSQL_DIR, "my.ini")
SERVICE_NAME = "MySQL_ChemChef"

MYSQL_ROOT_PASSWORD = "SPI12345"
DB_NAME = "ChemChef"
ADMIN_USER = "chemchef_user"
ADMIN_PASS = "spi12345"
ERP_USER = "erp_user"
ERP_PASS = "erp123"

# LAN IP
HOST = socket.gethostbyname(socket.gethostname())
print(f"ℹ LAN IP detected: {HOST}")

# ---------------- Admin Check ----------------
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print(" Please run this script as Administrator (right-click → Run as Administrator).")
    exit(1)

# ---------------- Helper Functions ----------------
def download_file(url, filename):
    try:
        print(f" Downloading {filename} …")
        urllib.request.urlretrieve(url, filename)
        print(f" Downloaded {filename}")
        return True
    except Exception as e:
        print(f" Failed to download {filename}: {e}")
        return False

def install_msi(filename):
    try:
        print(f" Installing {filename} ...")
        subprocess.run(["msiexec", "/i", filename, "/quiet", "/norestart"], check=True)
        print(f" {filename} installed.")
        os.remove(filename)
    except subprocess.CalledProcessError as e:
        print(f" Error installing {filename}: {e}")

def find_mysqld(mysql_dir):
    for root, dirs, files in os.walk(mysql_dir):
        if "mysqld.exe" in files:
            return os.path.join(root, "mysqld.exe")
    return None

# ---------------- MySQL Setup ----------------
def setup_mysql_server():
    bin_path = find_mysqld(MYSQL_DIR)
    if not bin_path:
        print(" MySQL Server not found. Downloading & extracting...")
        zip_path = "mysql_server.zip"
        if not download_file(MYSQL_SERVER_URL, zip_path):
            print(" Failed to download MySQL server. Please download manually.")
            exit(1)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(MYSQL_DIR)
        os.remove(zip_path)
        bin_path = find_mysqld(MYSQL_DIR)

    if not bin_path:
        print(" mysqld.exe not found after extraction.")
        exit(1)

    MYSQL_BIN = bin_path
    os.makedirs(DATADIR, exist_ok=True)

    if not os.listdir(DATADIR):
        subprocess.run([MYSQL_BIN,
                        "--initialize-insecure",
                        f"--datadir={DATADIR}"], check=True)
        print(" MySQL data directory initialized (no root password).")
    else:
        print(" Data directory already initialized. Skipping.")

    return MYSQL_BIN

# ---------------- my.ini ----------------
def create_my_ini():
    datadir_fixed = DATADIR.replace("\\", "/")
    content = f"""
[mysqld]
datadir={datadir_fixed}
port=3306
bind-address=0.0.0.0
sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES
"""
    with open(MY_INI, "w") as f:
        f.write(content.strip())
    print(" my.ini created with bind-address = 0.0.0.0 (LAN + localhost enabled).")

# ---------------- Windows Service ----------------
def install_mysql_service(MYSQL_BIN):
    print(f" Installing MySQL service '{SERVICE_NAME}' ...")
    subprocess.run(["sc", "stop", SERVICE_NAME], check=False, capture_output=True)
    subprocess.run(["sc", "delete", SERVICE_NAME], check=False, capture_output=True)

    cmd_install = [
        MYSQL_BIN,
        "--install",
        SERVICE_NAME,
        f"--defaults-file={MY_INI}"
    ]
    result = subprocess.run(cmd_install, capture_output=True, text=True)
    if result.returncode != 0:
        print(f" Failed to install service:\n{result.stderr or result.stdout}")
        return False

    print(f" Service '{SERVICE_NAME}' installed.")
    subprocess.run(["sc", "config", SERVICE_NAME, "start=", "auto"], capture_output=True)
    subprocess.run(["sc", "start", SERVICE_NAME], capture_output=True)
    print(f" MySQL service '{SERVICE_NAME}' started.")
    return True

# ---------------- Firewall ----------------
def allow_mysql_port():
    print(" Allowing MySQL port 3306 through Windows Firewall ...")
    subprocess.run([
        "netsh", "advfirewall", "firewall", "add", "rule",
        "name=MySQL", "dir=in", "action=allow", "protocol=TCP", "localport=3306"
    ], capture_output=True)
    print(" Firewall rule added.")

# ---------------- Database & Users ----------------
def setup_database_and_users():
    # Wait for MySQL to be ready
    for _ in range(10):
        try:
            conn = mysql.connector.connect(user="root", password="", host="127.0.0.1")
            conn.close()
            break
        except:
            time.sleep(2)
    else:
        print(" MySQL did not start in time.")
        exit(1)

    # Connect as root
    conn = mysql.connector.connect(user="root", password="", host="127.0.0.1")
    cursor = conn.cursor()

    # Root user
    try:
        cursor.execute(f"ALTER USER 'root'@'localhost' IDENTIFIED BY '{MYSQL_ROOT_PASSWORD}'")
    except:
        pass
    try:
        cursor.execute(f"CREATE USER IF NOT EXISTS 'root'@'%' IDENTIFIED BY '{MYSQL_ROOT_PASSWORD}'")
    except:
        pass
    cursor.execute("GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION")

    # Database
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")

    # Admin user
    for host in ["localhost", "%"]:
        cursor.execute(f"CREATE USER IF NOT EXISTS '{ADMIN_USER}'@'{host}' IDENTIFIED BY '{ADMIN_PASS}'")
        cursor.execute(f"GRANT ALL PRIVILEGES ON {DB_NAME}.* TO '{ADMIN_USER}'@'{host}'")

    # ERP user
    for host in ["localhost", "%"]:
        cursor.execute(f"CREATE USER IF NOT EXISTS '{ERP_USER}'@'{host}' IDENTIFIED BY '{ERP_PASS}'")
        cursor.execute(f"GRANT INSERT, SELECT ON {DB_NAME}.* TO '{ERP_USER}'@'{host}'")


    cursor.execute("FLUSH PRIVILEGES")
    conn.commit()
    cursor.close()
    conn.close()
    print(" Database and users configured for localhost + remote LAN")

# ---------------- Table ----------------
def check_and_create_table():
    conn = mysql.connector.connect(user=ADMIN_USER, password=ADMIN_PASS, host=HOST, database=DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS BatchChemical (
            id INT AUTO_INCREMENT PRIMARY KEY,
            BatchName VARCHAR(255) NOT NULL,
            MachineName VARCHAR(255) NOT NULL,
            FabricWt REAL NOT NULL,
            MLR REAL NOT NULL,
            Operator VARCHAR(255) NOT NULL,
            GroupNo INT NOT NULL,
            SeqNo INT NOT NULL,
            ChemID INT NOT NULL,
            TargetWt REAL NOT NULL,
            TargetTank VARCHAR(255) NOT NULL,
            DispenseMachine VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Table `BatchChemical` ensured.")

#  Installs
def install_workbench():
    if download_file(MYSQL_WORKBENCH_URL, "mysql_workbench.msi"):
        install_msi("mysql_workbench.msi")

def install_shell():
    if download_file(MYSQL_SHELL_URL, "mysql_shell.msi"):
        install_msi("mysql_shell.msi")

# ---------------- Main ----------------
if __name__ == "__main__":
    MYSQL_BIN = setup_mysql_server()
    create_my_ini()
    install_mysql_service(MYSQL_BIN)
    allow_mysql_port()
    setup_database_and_users()
    check_and_create_table()
    install_workbench()
    install_shell()

    print("\n Setup finished successfully!")
    print(f"   Database: {DB_NAME}")
    print(f"   Admin: {ADMIN_USER}/{ADMIN_PASS}")
    print(f"   ERP: {ERP_USER}/{ERP_PASS}")
    print(f"   Root: root/{MYSQL_ROOT_PASSWORD}")
    print(f"   LAN IP: {HOST}")
    input("\nPress Enter to exit...")

