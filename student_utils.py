import pandas as pd
import json
from fuzzywuzzy import process

def load_student_data():
    datasets = []
    for file_name in ['student_data/4th Year.json', 'student_data/2st Year.json', 'student_data/3rd Year.json']:
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)
                df = pd.DataFrame(data["Sheet1"])
                datasets.append(df)
        except Exception as e:
            print(f"Error loading {file_name}: {e}")
    return pd.concat(datasets, ignore_index=True)

def get_student_data(name, reg_no):
    df = load_student_data()
    if df is not None:
        student = df[df['REG NO'] == reg_no]
        if not student.empty:
            return student.iloc[0]

        # Fuzzy name match
        df['NAME'] = df['NAME'].str.lower()
        best_match_data = process.extractOne(name.lower(), df['NAME'].tolist())

        if best_match_data:
            best_match, score = best_match_data
            if score >= 70:
                student = df[df['NAME'] == best_match]
                if not student.empty:
                    return student.iloc[0]
    return None
