import os
import shutil
import re
import time

folder_path = "C:/greenfield_bugs"
target_folder = "C:/Greenfield"

while True:
    # Get all files in the folder
    files = os.listdir(folder_path)

    for file_name in files:
        if "sales_preeod" in file_name.lower() or "inv" in file_name.lower():
            file_path = os.path.join(folder_path, file_name)
            target_file_path = os.path.join(target_folder, file_name)

            # Remove the destination file if it already exists
            if os.path.exists(target_file_path):
                os.remove(target_file_path)
                print(f"Removed existing file: {target_file_path}")

            # Move the file to C:/Greenfield without checking content
            shutil.move(file_path, target_folder)
            print(f"File {file_name} moved to C:/Greenfield.")
        elif "sales" in file_name.lower():
            file_path = os.path.join(folder_path, file_name)
            print(f"Processing file: {file_path}")
            with open(file_path, 'r') as file:
                content = file.read()
                print(f"Original content:\n{content}")

                # Extract disccnt value
                disccnt_match = re.search(r'<disccnt>(\d+)</disccnt>', content)
                if disccnt_match:
                    disccnt = int(disccnt_match.group(1))
                    print(f"Disccnt value: {disccnt}")

                    # Extract seniorcnt and pwdcnt values
                    seniorcnt_match = re.search(r'<seniorcnt>(\d+)</seniorcnt>', content)
                    pwdcnt_match = re.search(r'<pwdcnt>(\d+)</pwdcnt>', content)

                    if seniorcnt_match and pwdcnt_match:
                        seniorcnt_total = int(seniorcnt_match.group(1))
                        pwdcnt_total = int(pwdcnt_match.group(1))

                        print(f"Seniorcnt total: {seniorcnt_total}, Pwdcnt total: {pwdcnt_total}")

                        # Calculate disccnt based on seniorcnt and pwdcnt
                        disccnt = seniorcnt_total + pwdcnt_total
                        print(f"New Disccnt value: {disccnt}")

                        # Replace disccnt with total value
                        content = content.replace(f'<disccnt>{disccnt_match.group(1)}</disccnt>', f'<disccnt>{disccnt}</disccnt>')

                        # Write back to the file
                        with open(file_path, 'w') as modified_file:
                            modified_file.write(content)
                            print("File modified and saved.")
                    else:
                        print("Error: Could not find seniorcnt or pwdcnt in file.")
                else:
                    print(f"Error: Could not find disccnt in file {file_name}")

            # Move the processed file to C:/Greenfield
            target_file_path = os.path.join(target_folder, file_name)
            if os.path.exists(target_file_path):
                os.remove(target_file_path)  # Remove existing file
            shutil.move(file_path, target_folder)
            print(f"File {file_name} moved to C:/Greenfield.")
        else:
            print("Non-sales file found, skipping.")

    time.sleep(10)  # Sleep for 10 seconds before running again
