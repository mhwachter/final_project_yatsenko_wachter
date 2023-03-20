import zipfile

with zipfile.ZipFile("../data/rta.zip", "r") as zip_ref:
    zip_ref.extractall("../data")
