import pandas as pd
import os

# Resolve dataset paths relative to this file so the server works
# regardless of which directory uvicorn is launched from.
_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dataset Paths
DONORS_FILE    = os.path.join(_BASE, "datasets", "donors.csv")
HOSPITALS_FILE = os.path.join(_BASE, "datasets", "hospitals.csv")
NGOS_FILE      = os.path.join(_BASE, "datasets", "ngos.csv")
REQUESTS_FILE  = os.path.join(_BASE, "datasets", "requests.csv")


# -------------------------
# Read CSV Functions
# -------------------------

def get_donors():
    return pd.read_csv(DONORS_FILE)


def get_hospitals():
    return pd.read_csv(HOSPITALS_FILE)


def get_ngos():
    return pd.read_csv(NGOS_FILE)


def get_requests():
    return pd.read_csv(REQUESTS_FILE)


# -------------------------
# Generic CSV Reader
# -------------------------

def read_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return pd.DataFrame()


# -------------------------
# Generic CSV Writer
# -------------------------

def write_csv(df, file_path):
    try:
        df.to_csv(file_path, index=False)
        return True
    except Exception as e:
        print(f"Error writing {file_path}: {e}")
        return False


# -------------------------
# Add Record
# -------------------------

def add_record(file_path, record):

    df = read_csv(file_path)

    df = pd.concat(
        [df, pd.DataFrame([record])],
        ignore_index=True
    )

    write_csv(df, file_path)

    return record


# -------------------------
# Delete Record
# -------------------------

def delete_record(
    file_path,
    id_column,
    record_id
):

    df = read_csv(file_path)

    index = df[
        df[id_column] == record_id
    ].index

    if len(index) == 0:
        return False

    df = df.drop(index)

    write_csv(df, file_path)

    return True


# -------------------------
# Update Record
# -------------------------

def update_record(
    file_path,
    id_column,
    record_id,
    updates
):

    df = read_csv(file_path)

    index = df[
        df[id_column] == record_id
    ].index

    if len(index) == 0:
        return False

    for key, value in updates.items():

        if key in df.columns:

            df.loc[index, key] = value

    write_csv(df, file_path)

    return True


# -------------------------
# Search Records
# -------------------------

def search_records(
    file_path,
    column,
    value
):

    df = read_csv(file_path)

    if column not in df.columns:
        return []

    result = df[
        df[column]
        .astype(str)
        .str.lower()
        == str(value).lower()
    ]

    return result.to_dict(
        orient="records"
    )


# -------------------------
# Dashboard Stats Helper
# -------------------------

def count_rows(file_path):

    df = read_csv(file_path)

    return len(df)


# -------------------------
# Blood Group Statistics
# -------------------------

def blood_group_stats():

    df = get_donors()

    return (
        df["bloodGroup"]
        .value_counts()
        .to_dict()
    )


# -------------------------
# Request Status Statistics
# -------------------------

def request_status_stats():

    df = get_requests()

    return (
        df["status"]
        .value_counts()
        .to_dict()
    )