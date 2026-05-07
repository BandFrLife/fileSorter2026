from pathlib import Path
import runpy


def run_sorter_gui() -> None:
    """Run src/gui2.py."""
    print("Running Sorter Explorer.")
    gui_path = Path(__file__).resolve().parent / "gui2.py"
    runpy.run_path(str(gui_path), run_name="__main__")


def run_explorer_gui() -> None:
    """Run src/explorer/gui2.py."""
    print("Running File Explorer.")
    gui_path = Path(__file__).resolve().parent / "explorer" / "gui2.py"
    runpy.run_path(str(gui_path), run_name="__main__")


def main() -> None:
    print("Choose GUI version:")
    print("1. Sorter GUI")
    print("2. Explorer GUI")

    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        run_sorter_gui()
    elif choice == "2":
        run_explorer_gui()
    else:
        print("Invalid choice. Use 1 or 2.")


if __name__ == "__main__":
    main()
