#!/usr/bin/env bash

# Provided by ChatGPT for simplicity and testing since directory is deleted frequently.
# Randomly add files/folders inside existing class directories under CMU/20*

BASE_DIR="CMU"

# Example class names
CLASSES=("CSCI111" "MATH120" "HIST210" "ENGL101" "BIOL230" "CHEM115")

# Example random file/subdir names
FILES=("notes.txt" "syllabus.pdf" "todo.md" "assignment1.py" "readme.txt")
SUBDIRS=("homework" "projects" "lectures" "exams")

semester_dirs=$(find "$BASE_DIR" -mindepth 2 -maxdepth 2 -type d -path "$BASE_DIR/20*/*")

for semester_dir in $semester_dirs; do
    # Randomly skip some semesters
    if (( RANDOM % 2 == 0 )); then
        continue
    fi

    # Add 1 to 3 random classes
    num_classes=$(( RANDOM % 3 + 1 ))

    for (( i = 0; i < num_classes; i++ )); do
        class_name="${CLASSES[$RANDOM % ${#CLASSES[@]}]}"
        class_dir="$semester_dir/$class_name"

        mkdir -p "$class_dir"
        echo "Created class dir: $class_dir"

        # Add 1 to 3 files
        num_files=$(( RANDOM % 3 + 1 ))

        for (( j = 0; j < num_files; j++ )); do
            file_name="${FILES[$RANDOM % ${#FILES[@]}]}"
            echo "Random content for $file_name" > "$class_dir/$file_name"
        done

        # Sometimes add a subdir
        if (( RANDOM % 2 == 0 )); then
            subdir_name="${SUBDIRS[$RANDOM % ${#SUBDIRS[@]}]}"
            mkdir -p "$class_dir/$subdir_name"
            echo "Created class dir: $class_dir"
            echo "Random nested content" > "$class_dir/$subdir_name/info.txt"
            echo "Created class file: $class_dir/info.txt"
        fi
    done
done

