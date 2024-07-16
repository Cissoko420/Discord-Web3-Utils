# Copy wallets from discord channels copying also the usernames and so
#
# Ex: "@User - Today 8:50 PM
#      Adlsj3242nolashd45klsadjsldasjkgklsdg"
#
# Bot will remove "@User - Today 8:50 PM" and get wallet seperatly
# 2 files will be generated. 1 with all the wallets (no duplicates) and another with each duplicate and their username

# Read the content of the file in binary mode
with open('text.txt', 'rb') as file:
    content = file.read().decode('utf-8', errors='replace')

# Split the content by lines
lines = content.split('\n')

# Create a dictionary to store the names and their respective next lines
name_dict = {}
repeated_names = set()
duplicate_values = {}

# Iterate through the lines
for i in range(len(lines) - 1):
    # Check if the line contains a name (ends with ' —')
    if ' —' in lines[i]:
        # Extract the name
        name = lines[i].split(' —')[0]
        # Extract the specific value
        value = lines[i + 1]

        # Check for duplicates
        if name in name_dict:
            repeated_names.add(name)
            if (name, value) in duplicate_values:
                duplicate_values[(name, value)] += 1
            else:
                duplicate_values[(name, value)] = 2
        else:
            name_dict[name] = [value]

# Write duplicates to a file
duplicates_file_path = 'duplicates.txt'
with open(duplicates_file_path, 'w', encoding='utf-8') as duplicates_file:
    for (name, value), count in duplicate_values.items():
        duplicates_file.write(f"{name}: {value} (Duplicated {count} times)\n")

# Write the result to a text file
output_file_path = 'results.txt'
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for name, values in name_dict.items():
        for value in values:
            cleaned_value = value.strip()
            output_file.write(f'{cleaned_value},\n')

print(f"Results (values only) written to {output_file_path}")
print(f"Duplicates written to {duplicates_file_path}")
