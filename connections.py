import os
import pandas as pd

folder_path = "CleanedLinkedInData"
csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

adj_list = {}
all_people = set()

# Build mutual connections
for filename in csv_files:
    owner = os.path.splitext(filename)[0]
    file_path = os.path.join(folder_path, filename)
    df = pd.read_csv(file_path)

    df["Full Name"] = df["First Name"].astype(str).str.strip() + " " + df["Last Name"].astype(str).str.strip()

    all_people.add(owner)
    all_people.update(df["Full Name"].values)

    if owner not in adj_list:
        adj_list[owner] = []

    for name in df["Full Name"]:
        if name == owner:
            continue

        if name not in adj_list[owner]:
            adj_list[owner].append(name)

        if name not in adj_list:
            adj_list[name] = []
        if owner not in adj_list[name]:
            adj_list[name].append(owner)

for person in adj_list:
    adj_list[person] = sorted(adj_list[person])

print(f"Total people: {len(adj_list)}\n")
print("{")
for person, connections in adj_list.items():
    print(f"    '{person}': {connections},")
print("}")






degree = {}
for person in adj_list:
    if person not in degree:
        degree[person] = 0
    degree[person] += len(adj_list[person])
    
for name, deg in sorted(degree.items(), key=lambda x: x[1], reverse=True):
    print(f"{name}: degree {deg}")

total_degrees = sum(len(friends) for friends in adj_list.values())
num_nodes = len(adj_list)
average_degree = total_degrees / num_nodes if num_nodes > 0 else 0


print(f" Average Degree: {average_degree: .2f}")





connections = degree
thresholds = [1000, 2000, 3000, 4000]
threshold_counts = {}

for t in thresholds:
    count = sum(1 for v in connections.values() if v > t)
    threshold_counts[f"> {t}"] = count

for label, count in threshold_counts.items():
    print(f"{label:>6}: {count}")



import json
import random
import statistics

json_file_path ="adjacency_list.json"

if not os.path.exists(json_file_path):
    print(f" File not found: {json_file_path}")
else:
    try:
        with open(json_file_path, "r", encoding="utf-8") as f:
            adjacency_list = json.load(f)
    except json.JSONDecodeError as e:
        print(f" JSON decode error: {e}")
        adjacency_list = {}

    students = [s for s, neighbors in adjacency_list.items() if neighbors]

    if len(students) < 2:
        print(" Not enough students with connections.")
    else:
        def random_walk(graph, start, end, max_steps=15):
            path = [start]
            current = start
            for _ in range(max_steps):
                neighbors = graph.get(current, [])
                if not neighbors:
                    break
                next_node = random.choice(neighbors)
                path.append(next_node)
                if next_node == end:
                    break
                current = next_node
            return path

        def prune_path(path):
            seen = set()
            pruned = []
            for node in path:
                if node not in seen:
                    pruned.append(node)
                    seen.add(node)
            return pruned

        num_examples = 50
        walk_lengths, pruned_lengths = [], []
        examples = []

        for _ in range(num_examples):
            start, end = random.sample(students, 2)
            walk = random_walk(adjacency_list, start, end)
            pruned = prune_path(walk)

            walk_lengths.append(len(walk))
            pruned_lengths.append(len(pruned))

            examples.append({
                "start": start,
                "end": end,
                "walk": walk,
                "pruned": pruned
            })


        for idx, ex in enumerate(examples, 1):
            print(f"\n Example {idx}: {ex['start']} to {ex['end']}")
            print("   Random Walk : " + " , ".join(ex['walk']))
            print("   Pruned Path : " + " , ".join(ex['pruned']))

        def safe_mode(data):
            try:
                return statistics.mode(data)
            except statistics.StatisticsError:
                return "No unique mode"

        print("\n" + "="*70)
        print(" STATISTICAL SUMMARY")
        print("="*70)

        summary = {
            "Total Examples"            : num_examples,
            "Average Walk Length"       : round(statistics.mean(walk_lengths), 2),
            "Average Pruned Path Length": round(statistics.mean(pruned_lengths), 2),
            "Minimum Walk Length"       : min(walk_lengths),
            "Maximum Walk Length"       : max(walk_lengths),
            "Minimum Pruned Path Length": min(pruned_lengths),
            "Maximum Pruned Path Length": max(pruned_lengths),
            "Median Walk Length"        : statistics.median(walk_lengths),
            "Median Pruned Path Length" : statistics.median(pruned_lengths),
            "Mode Walk Length"          : safe_mode(walk_lengths),
            "Mode Pruned Length"        : safe_mode(pruned_lengths),
            "Std Dev of Walk Length"       : round(statistics.stdev(walk_lengths), 2),
            "Std Dev of Pruned Length"     : round(statistics.stdev(pruned_lengths), 2),
        }

        for k, v in summary.items():
            print(f"{k:<30}: {v}")




def top_five_companies_from_folder(folder_path):
    # Create an empty dictionary to count company occurrences
    company_count = {}

    # List all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # Get the full file path
            file_path = os.path.join(folder_path, filename)

            # Read the CSV into a DataFrame
            df = pd.read_csv(file_path)

            # Drop rows where company is missing
            df = df.dropna(subset=["Company"])

            # Count company occurrences in this file
            for company in df["Company"]:
                if company in company_count:
                    company_count[company] += 1
                else:
                    company_count[company] = 1

    # Sort companies by count in descending order and get the top 5
    sorted_companies = sorted(company_count.items(), key=lambda x: x[1], reverse=True)[:10]

    # Print the Top 5 Companies
    print(" Top 10 Companies Across All CSVs:")
    for company, count in sorted_companies:
        print(f"- {company}: {count} connections")

    return sorted_companies

# Set your folder path containing the CSV files
folder_path = "CleanedLinkedInData"

# Run the function to extract company names from all CSVs in the folder
company_list = top_five_companies_from_folder(folder_path)

