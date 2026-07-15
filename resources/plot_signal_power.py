import time
import os
import glob
import shutil
from collections import deque

VALUE_MIN = -10
VALUE_MAX = 50
# ROW_STEP and PLOT_HEIGHT will be updated dynamically

# History length will be set dynamically based on terminal width
history = deque()

def find_latest_power_log():
    files = sorted(
        glob.glob("/root/Results/*_power_log.txt"),
        key=lambda f: os.path.getmtime(f)
    )
    return files[-1] if files else None

def get_new_values(filepath, last_pos):
    values = []
    with open(filepath, "r") as f:
        f.seek(last_pos)
        lines = f.readlines()
        for line in lines:
            try:
                parts = line.strip().split()
                value = float(parts[-1])
                values.append(value)
            except (ValueError, IndexError):
                continue
        new_pos = f.tell()
    return values, new_pos

def get_color(value):
    if value < 0:
        return "\033[91m"       # Red
    elif value < 10:
        return "\033[38;5;208m" # Orange
    elif value < 20:
        return "\033[93m"       # Yellow
    elif value < 30:
        return "\033[92m"       # Green
    else:
        return "\033[32m"       # Dark Green

def draw_plot(history, file_path):
    terminal_height = shutil.get_terminal_size((80, 20)).lines
    min_height = 10
    max_height = 30
    usable_height = max(min_height, min(max_height, terminal_height - 6))
    row_step = max(1, int((VALUE_MAX - VALUE_MIN) / usable_height))
    plot_height = int((VALUE_MAX - VALUE_MIN) / row_step) + 1
    plot = [[" " for _ in range(len(history))] for _ in range(plot_height)]
    colors = ["\033[0m" for _ in range(len(history))]

    for col, value in enumerate(history):
        row = int((VALUE_MAX - value) / row_step)
        row = max(0, min(plot_height - 1, row))
        plot[row][col] = "█"
        colors[col] = get_color(value)

    os.system("clear")
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    title = f"{os.path.basename(file_path)} - Received signal power"
    print(title.center(terminal_width))

    for i, line in enumerate(plot):
        label_value = VALUE_MAX - i * row_step
        color = get_color(label_value)
        label = f"{color}{label_value: >3}\033[0m | "
        row_str = ""
        for col, char in enumerate(line):
            color = colors[col] if char == "█" else "\033[0m"
            row_str += f"{color}{char}\033[0m"
        print(label + row_str)
    print("    +" + "-" * (len(history) + 2))

def main():
    global history
    file_path = find_latest_power_log()
    if not file_path:
        print("No *_power_log.txt file found in Results/")
        return

    print(f"Reading from: {file_path}")
    last_pos = 0

    try:
        while True:
            # Check if a newer file appeared
            latest_file = find_latest_power_log()
            if latest_file != file_path:
                print(f"Switching to new file: {latest_file}")
                file_path = latest_file
                last_pos = 0
                history.clear()

            # Dynamically update history length based on terminal width
            terminal_width = shutil.get_terminal_size((80, 20)).columns
            history_length = max(10, terminal_width - 10)
            if history.maxlen != history_length:
                history = deque(history, maxlen=history_length)

            new_values, last_pos = get_new_values(file_path, last_pos)

            for value in new_values:
                clamped = max(VALUE_MIN, min(VALUE_MAX, value))
                history.append(clamped)

            if new_values:
                draw_plot(history, file_path)

            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()
