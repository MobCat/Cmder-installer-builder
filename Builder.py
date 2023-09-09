#!/env/Python3.10.4
#/MobCat (2023)
'''
https://cmder.app/
https://github.com/cmderdev/cmder/releases/latest/
https://github.com/cmderdev/cmder/releases/latest/download/cmder_mini.zip
https://github.com/cmderdev/cmder/releases/latest/download/cmder.zip
'''

import requests
from tqdm import tqdm
import zipfile
import os
from datetime import datetime
import subprocess
import shutil

# Set where you have Inno Setup 6 installed
#TODO: Should error check this...
innoPath = 'C:/Program Files (x86)/Inno Setup 6/ISCC.exe'

# Check if we got someone to build to
os.makedirs('Build', exist_ok=True)
if not os.path.exists("Installer.iss"):
	print("!ERROR!\nInstaller.iss file is MISSING!\nPlease download a new one from...")
	exit()

# Get current version info of cmder 
responseVer = requests.head("https://github.com/cmderdev/cmder/releases/latest/", allow_redirects=True)
releasesURL = responseVer.url
verNum = responseVer.url.split("/")[-1]
print(f"Cmder {verNum} installer builder\n{releasesURL}\n")

# Get filesize for the releases
response = requests.head("https://github.com/cmderdev/cmder/releases/latest/download/cmder_mini.zip", allow_redirects=True)
if response.status_code == 200:
	miniSize = round(int(response.headers['Content-Length'])/1024/1024, 2)

	response = requests.head("https://github.com/cmderdev/cmder/releases/latest/download/cmder.zip", allow_redirects=True)
	fullSize = round(int(response.headers['Content-Length'])/1024/1024, 2)

else:
	print(f"Failed to retrieve file size info from GitHub. Status code: {response.status_code}\nPlease check your internet connection or the project page itself and try again.")
	exit()

########################################################################################################################
# Functions
########################################################################################################################
#
def Downloader(url, verNum, cmdertype):
	fileName = f"cmder_{cmdertype}_{verNum}.zip"
	print(f"Downloading {fileName}")
	response = requests.get(url, stream=True)
	total_size = int(response.headers.get('content-length', 0))
	block_size = 1024  # 1 Kilobyte
	downloaded = 0
	with open(f"cmder_{cmdertype}_{verNum}.zip", "wb") as file:
		for data in tqdm(response.iter_content(block_size), total=total_size//block_size, unit='MB', unit_scale=True):
			downloaded += len(data)
			file.write(data)
	
	print("Download complete!")
	return fileName

#
def ExtractZip(fileName):
	print(f"Extracting {fileName}")
	os.makedirs("Cmder")
	#
	with zipfile.ZipFile(fileName, 'r') as zip_ref:
		# Get the total number of files in the zip archive
		total_files = len(zip_ref.infolist())
		
		# Create a progress bar
		progress = tqdm(total=total_files, desc='Extracting files', unit='file')
		
		for file_info in zip_ref.infolist():
			zip_ref.extract(file_info, "Cmder")
			progress.update(1)  # Update progress bar
	
		progress.close()  # Close progress bar once extraction is complete
	os.remove(fileName)

# Fucking stupid get folder file size function inside a function
# Might scrap this.
def get_folder_size(folder_path):
	def convert_bytes(num):
		for x in ['bytes', 'KB', 'MB']:
			if num < 1024.0:
				return f"{num:.2f} {x}"
			num /= 1024.0

	total_size = 0

	for dirpath, dirnames, filenames in os.walk(folder_path):
		for f in filenames:
			fp = os.path.join(dirpath, f)
			total_size += os.path.getsize(fp)

	return convert_bytes(total_size)

# Rebuild the info.txt and Installer.iss files with the current version of Cmder we are building
def BuildInfo(verNum, installType):
	# Build info txt for the installer splash page
	print("Building installer info")
	with open('info.txt', 'w') as f:
		f.write(f'Cmder {verNum} {installType} installer\n')
		f.write(f'https://cmder.app/\n')
		f.write(f'{releasesURL}\n\n')
		f.write(f'This installer was automatically built with Cmder Installer Builder by MobCat\n')
		f.write(f'https://github.com/MobCat\n\n')
		f.write(f'This installer was built on {datetime.now().strftime("%Y-%d-%m")}\n')
		size = get_folder_size('Cmder')
		f.write(f'The Cmder installation will be {size} on disk')
	
	# Update the iss scrupt with our current versions and work dir.
	with open('Installer.iss', 'r') as file:
		lines = file.readlines()
	lines[4] = f'#define MyAppVersion "{verNum[1:]}"\n'
	lines[8] = f'#define InstallType "{installType}"\n' # The first edit offsets the line numbers? So we are editng line 9 here.
	
	with open('Installer.iss', 'w') as file:
		file.writelines(lines)


########################################################################################################################
# Do something with said functions.
########################################################################################################################

# Ask user which one they would like to download and build
print("Please note: This is just the download size.\nYour installer exe will be smaller then this,\nand the installed cmder folder will be larger then this.\nMore info will be generated in the installers info page.\n")
print(f"1) Mini Installer: {miniSize} MB")
print(f"2) Full Installer: {fullSize} MB")
print(f"3) Build Both Installers: {miniSize+fullSize} MB")

# "Logic" for setting which ver to download and build
inputChoice = input("Download? [1/2/3]: ")
if inputChoice == '1':
	installType = "mini"
	fileName = Downloader("https://github.com/cmderdev/cmder/releases/latest/download/cmder_mini.zip", verNum, installType)
	ExtractZip(fileName)
	BuildInfo(verNum, installType)
	# Run Command line Inno Setup Compiler with our updated scrupt
	# Dont really need a print for this as it has its own debug output.
	subprocess.run([innoPath, 'Installer.iss'])
	# Cleanup
	# Hate how os sucks at folders so I need yet another lib for this.
	print("Cleaning up...")
	shutil.rmtree('Cmder') 
	print("Done ^__^/")

elif inputChoice == '2':
	installType = "full"
	fileName = Downloader("https://github.com/cmderdev/cmder/releases/latest/download/cmder.zip", verNum, installType)
	ExtractZip(fileName)
	BuildInfo(verNum, installType)
	subprocess.run([innoPath, 'Installer.iss'])
	print("Cleaning up...")
	shutil.rmtree('Cmder') 
	print("Done ^__^/")

else:
	installType = "mini"
	fileName = Downloader("https://github.com/cmderdev/cmder/releases/latest/download/cmder_mini.zip", verNum, installType)
	ExtractZip(fileName)
	BuildInfo(verNum, installType)
	subprocess.run([innoPath, 'Installer.iss'])
	print("Cleaning up...")
	shutil.rmtree('Cmder') 

	installType = "full"
	fileName = Downloader("https://github.com/cmderdev/cmder/releases/latest/download/cmder.zip", verNum, installType)
	ExtractZip(fileName)
	BuildInfo(verNum, installType)
	subprocess.run([innoPath, 'Installer.iss'])
	print("Cleaning up...")
	shutil.rmtree('Cmder') 
	print("Done ^__^/")

