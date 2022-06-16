def generate_csv(rows, file_name):
    if len(rows) <= 0:
        print("No rows to generate a csv")
        return

    data = []

    for row in rows:
        data.append(row.__dict__)

    df = pd.DataFrame(data)
    df = df.drop(['_sa_instance_state'], axis=1)
    df.to_csv(file_name)