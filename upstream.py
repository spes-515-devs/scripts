import subprocess
import os
import shutil

repos = [
    "android_kernel_xiaomi_sm6225-modules",
    "android_kernel_xiaomi_sm6225-devicetrees",
    "android_device_xiaomi_spes-5.15",
    "android_vendor_xiaomi_spes-5.15",
    "android_kernel_xiaomi_sm6225-5.15",
    "device_xiaomi_spes-twrp-5.15"
]

source_org = "https://github.com/muralivijay/"
target_org = "https://github.com/spes-515-devs/"

if os.path.exists("repos"):
    shutil.rmtree("repos")
os.makedirs("repos")
os.chdir("repos")

for repo in repos:
    print(f"\nCloning {repo} (mirror)...")
    subprocess.run(["git", "clone", "--mirror", f"{source_org}{repo}.git"])

    os.chdir(f"{repo}.git")
    print(f"Reconfiguring remote for {repo}...")
    subprocess.run(["git", "remote", "remove", "origin"])
    subprocess.run(["git", "remote", "add", "origin", f"{target_org}{repo}.git"])

    print(f"Determining default branch for {repo}...")
    result = subprocess.run(
        ["git", "symbolic-ref", "HEAD"],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        default_branch = result.stdout.strip().split("/")[-1]
        print(f"Default branch: {default_branch}. Force pushing...")
        subprocess.run(["git", "push", "--force", "origin", f"refs/heads/{default_branch}"])
    else:
        print("Could not determine default branch. Skipping force push.")

    os.chdir("..")

print("\nAll done!")
