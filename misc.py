from collections import defaultdict

# Define the two package lists
first_list = """
beautifulsoup4==4.12.3
bs4==0.0.2
certifi==2024.8.30
charset-normalizer==3.4.0
idna==3.10
importlib_metadata==8.5.0
inflect==7.4.0
joblib==1.4.2
more-itertools==10.5.0
numpy==2.0.2
requests==2.32.3
scikit-learn==1.5.2
scipy==1.13.1
soupsieve==2.6
threadpoolctl==3.5.0
typeguard==4.4.1
typing_extensions==4.12.2
urllib3==2.2.3
zipp==3.21.0
"""

second_list = """
annotated-types==0.7.0
blis==1.0.1
catalogue==2.0.10
certifi==2024.8.30
charset-normalizer==3.4.0
click==8.1.7
cloudpathlib==0.20.0
colorama==0.4.6
confection==0.1.5
cymem==2.0.10
filelock==3.16.1
fsspec==2024.10.0
huggingface-hub==0.26.3
idna==3.10
ijson==3.3.0
inflect==7.4.0
Jinja2==3.1.4
joblib==1.4.2
langcodes==3.5.0
language_data==1.3.0
marisa-trie==1.2.1
markdown-it-py==3.0.0
MarkupSafe==3.0.2
mdurl==0.1.2
more-itertools==10.5.0
mpmath==1.3.0
murmurhash==1.0.11
networkx==3.4.2
numpy==2.0.2
packaging==24.2
pillow==11.0.0
preshed==3.0.9
PuLP==2.9.0
pydantic==2.10.2
pydantic_core==2.27.1
Pygments==2.18.0
PyYAML==6.0.2
RapidFuzz==3.10.1
regex==2024.11.6
requests==2.32.3
rich==13.9.4
safetensors==0.4.5
scikit-learn==1.5.2
scipy==1.14.1
sentence-transformers==3.3.1
shellingham==1.5.4
smart-open==7.0.5
spacy==3.8.2
spacy-legacy==3.0.12
spacy-loggers==1.0.5
srsly==2.4.8
sympy==1.13.1
thinc==8.3.2
threadpoolctl==3.5.0
tokenizers==0.20.3
torch==2.5.1
tqdm==4.67.1
transformers==4.46.3
typeguard==4.4.1
typer==0.14.0
typing_extensions==4.12.2
urllib3==2.2.3
wasabi==1.1.3
weasel==0.4.1
wrapt==1.17.0
"""


# Parse the lists into dictionaries
def parse_package_list(package_list):
    packages = defaultdict(str)
    for line in package_list.strip().split("\n"):
        if "==" in line:
            name, version = line.split("==")
            packages[name.strip()] = version.strip()
    return packages


first_packages = parse_package_list(first_list)
second_packages = parse_package_list(second_list)

# Overwrite versions from the second list
resolved_packages = {**first_packages, **second_packages}

# Write resolved packages to a new requirements.txt file
with open("resolved_requirements.txt", "w") as f:
    for package, version in sorted(resolved_packages.items()):
        f.write(f"{package}=={version}\n")

print("Resolved requirements saved to 'resolved_requirements.txt'.")
