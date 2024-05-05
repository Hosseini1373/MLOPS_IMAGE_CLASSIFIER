import sys
import pkg_resources

REQUIRED_PYTHON = "python3"
# REQUIRED_PACKAGES = {
#     'numpy': '1.25.2',
#     'pandas': '1.5.3',
#     'matplotlib': '3.7.1',
#     'scikit-learn': '1.2.2',
#     'seaborn': '0.13.1',
#     'pyarrow': '14.0.2',
#     'flake8': None,  # No version specified; will only check for presence
#     'pytest': '8.0.2',
#     'torch': '2.2.1',
#     'tqdm': None,
#     'ray': '2.10.0',
#     'mlflow': '2.11.3',
#     'deepchecks': '0.18.1',
#     'dvc': '3.49.0',
#     'python-dotenv': '1.0.1',
# }

def main():
    system_major = sys.version_info.major
    required_major = 3 if REQUIRED_PYTHON == "python3" else 2

    if system_major != required_major:
        raise TypeError(
            "This project requires Python {}. Found: Python {}".format(
                required_major, sys.version))
    else:
        print(">>> Development environment passes Python version test.")

    # missing_packages = []
    # for package, version in REQUIRED_PACKAGES.items():
    #     try:
    #         if version:
    #             pkg_resources.require(f"{package}=={version}")
    #         else:
    #             pkg_resources.require(package)
    #         print(f"Package {package} (version {version}) is installed.")
    #     except pkg_resources.DistributionNotFound:
    #         print(f"Package {package} (version {version}) is MISSING.")
    #         missing_packages.append(package)
    #     except pkg_resources.VersionConflict as e:
    #         print(f"Version conflict for package {package}: {e}")
    #         missing_packages.append(package)

    # if missing_packages:
    #     print(">>> Some required packages are missing or have incorrect versions.")
    #     sys.exit(1)
    # else:
    #     print(">>> All required packages are installed with correct versions.")

if __name__ == '__main__':
    main()
