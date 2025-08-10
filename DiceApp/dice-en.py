<<<<<<< HEAD
"""
Dice Roller GUI with Tkinter and Matplotlib.

This application allows the user to define multiple sets of dice. Each set can have a specified number of dice and a chosen number of sides per dice. The user can roll each set individually. For dice with 2 to 6 sides, the result is shown with traditional pip dots; for dice with more than 6 sides, the numerical result is displayed.

The code uses Tkinter for the user interface, Matplotlib for rendering dice faces, and a custom IntEntry widget (from number_entry module) to ensure numeric input within valid ranges.
"""
import tkinter as tk                               # Tkinter for GUI elements
from tkinter import Frame, Label, Button, Entry, messagebox, colorchooser  # Common Tkinter widgets and dialogs
import random                                      # Random for dice rolls
import math                                        # Math for calculations (e.g. ceil)
import matplotlib.pyplot as plt                    # Matplotlib for drawing dice faces
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # To embed Matplotlib figures in Tkinter

# Try to import the custom integer entry widget (IntEntry) for numeric inputs
try:
    from number_entry import IntEntry
except ImportError:
    # If the module is missing, show an error and exit
    messagebox.showerror("Error", "Required module 'number_entry' is missing.")
    exit()

# Global variables for cell dimensions (used when drawing dice faces in result frames)
cell_width = 0
cell_height = 0
# Factors defining what portion of each cell's width and height is used for drawing the dice
dice_area_width_factor = 0.9    # use 90% of cell width for dice graphics
dice_area_height_factor = 0.5   # use 50% of cell height for dice graphics

def draw_dice_face(ax, number, dice_color, text_color, use_dots=False):
    """
    Draw a single dice face on the given Matplotlib axis.

    Parameters:
        ax         - Matplotlib axis on which to draw
        number     - The rolled number to display
        dice_color - Background color of the dice face
        text_color - Color for the number or the pips (dots)
        use_dots   - If True, draw a pip pattern (standard dice pips) instead of a number
    """
    # Clear any previous content on this axis
    ax.clear()
    # Remove ticks for a cleaner look
    ax.set_xticks([])
    ax.set_yticks([])
    # Fix the axis limits to a 0.5x0.5 square (for consistent scaling)
    ax.set_xlim(0, 0.5)
    ax.set_ylim(0, 0.5)
    # Set the background color of the dice face
    ax.set_facecolor(dice_color)

    if use_dots:
        # Pip layouts for dice faces 1 through 6
        pip_positions = {
            1: [(0.25, 0.25)],  # center pip
            2: [(0.1, 0.4), (0.4, 0.1)],  # two pips (diagonal)
            3: [(0.1, 0.4), (0.25, 0.25), (0.4, 0.1)],  # three pips (two diagonal + center)
            4: [(0.1, 0.4), (0.4, 0.4), (0.1, 0.1), (0.4, 0.1)],  # four corner pips
            5: [(0.1, 0.4), (0.4, 0.4), (0.1, 0.1), (0.4, 0.1), (0.25, 0.25)],  # four corners + center
            6: [(0.1, 0.4), (0.4, 0.4), (0.1, 0.25), (0.4, 0.25), (0.1, 0.1), (0.4, 0.1)]  # six pips (three per column)
        }
        # Get the pip layout for the rolled number (default to single center pip if number not in dict)
        dots = pip_positions.get(number, [(0.25, 0.25)])
        # Draw each pip as a small filled circle
        for (x, y) in dots:
            circle = plt.Circle((x, y), 0.04, color=text_color)
            ax.add_artist(circle)
    else:
        # If not using pips, display the number as text in the center of the face
        ax.text(0.25, 0.25, str(number), fontsize=16, ha='center', va='center',
                fontweight='bold', color=text_color)

def roll_single_set(result_frame, dice_count, dice_sides, set_name, dice_color, number_color):
    """
    Roll a single set of dice and display the results in the UI.

    Parameters:
        result_frame - The Tkinter frame where the dice images will be displayed
        dice_count   - IntEntry widget for the number of dice to roll
        dice_sides   - IntEntry widget for the number of sides on each die
        set_name     - Name of the set (string used for labeling purposes)
        dice_color   - Background color for the dice faces
        number_color - Color for the numbers or pips on the dice
    """
    # Remove any previous results from this frame
    for widget in result_frame.winfo_children():
        widget.destroy()
    try:
        # Retrieve the user-specified number of sides and dice count
        sides_val = dice_sides.get()
        count_val = dice_count.get()
        # Validate the input ranges (Sides must be 2-50, Dice Count 1-12)
        if not (2 <= sides_val <= 50) or not (1 <= count_val <= 12):
            raise ValueError
        # Generate random rolls for the given number of dice and sides
        rolls = [random.randint(1, sides_val) for _ in range(count_val)]
    except ValueError:
        # If inputs are invalid, show an error dialog and abort rolling
        messagebox.showerror("Input Error", "Please enter valid values for sides (2-50) and dice count (1-12).")
        return

    # Determine layout for dice faces: up to 6 dice per row
    dice_cols = min(6, count_val)
    # Number of rows needed based on how many dice (6 per row maximum)
    dice_rows = math.ceil(count_val / 6)

    # Calculate an appropriate dice image size (in pixels) based on current window size and defined factors
    die_size_pixels = min((cell_width * dice_area_width_factor) / dice_cols,
                          (cell_height * dice_area_height_factor) / dice_rows)
    # Convert pixel size to inches for Matplotlib (assuming 100 dpi for simplicity: 1 inch = 100 pixels)
    fig_width = (die_size_pixels * dice_cols) / 100
    fig_height = (die_size_pixels * dice_rows) / 100

    # Create a Matplotlib figure with a grid of subplots to represent dice faces
    fig, axes = plt.subplots(dice_rows, dice_cols, figsize=(fig_width, fig_height), dpi=100)
    # Flatten the axes array into a simple list for easy iteration
    if dice_rows * dice_cols == 1:
        axes = [axes]
    elif dice_rows == 1 or dice_cols == 1:
        axes = list(axes)
    else:
        axes = [ax for row in axes for ax in row]

    # Use pip (dot) representation if the dice have 6 or fewer sides, otherwise use numeric
    use_dots = (sides_val <= 6)
    # Draw each rolled dice face on its corresponding subplot
    for ax, roll in zip(axes, rolls):
        draw_dice_face(ax, roll, dice_color, number_color, use_dots=use_dots)
    # If there are more subplot axes than dice (which can happen if count_val is not a multiple of dice_cols), hide the extras
    for ax in axes[len(rolls):]:
        ax.set_visible(False)

    # Embed the Matplotlib figure (dice images) into the Tkinter result frame
    canvas = FigureCanvasTkAgg(fig, master=result_frame)
    canvas.get_tk_widget().pack(pady=5)
    canvas.draw()

    # If more than one die was rolled, also display the sum of all dice at the bottom
    if count_val > 1:
        total = sum(rolls)
        Label(result_frame, text=f"Total: {total}", font=("Arial", 12, "bold")).pack(pady=5)

def confirm_sets():
    """
    Read the number of sets from user input, validate it, 
    create a configuration panel for each set, and saves the configurations in a global list.
    """
    try:
        # Get the desired number of sets from the entry field
        num_sets = enter_set.get()
        # Validate that the number is within allowed range (1-12)
        if not (1 <= num_sets <= 12):
            raise ValueError
    except ValueError:
        # If input is invalid, show an error message and return early
        messagebox.showerror("Error", "Please enter a valid number of sets (1-12).")
        return

    # Reinitialize the global sets list
    global sets
    sets = []
    # Clear any existing set configuration frames
    for widget in grid_frame.winfo_children():
        widget.destroy()

    # Create configuration frames for each set
    # Sets will be arranged in a grid with a maximum of 4 rows per column
    for i in range(num_sets):
        # Create a frame for this set's configuration (with border and padding for visibility)
        set_frame = Frame(grid_frame, bd=1, relief="groove", padx=5, pady=5)
        # Position frames in a grid: 4 rows per column (new column after every 4 sets)
        set_frame.grid(row=i % 4, column=i // 4, padx=10, pady=10, sticky="nsew")

        # Entry for the set name
        Label(set_frame, text=f"Set {i+1} Name:").grid(row=0, column=0, sticky="w")
        set_name = Entry(set_frame, width=15)
        set_name.grid(row=0, column=1, padx=5, pady=2)

        # Entry for the dice count in this set
        Label(set_frame, text="Dice Count (max. 12):").grid(row=1, column=0, sticky="w")
        # Use IntEntry for numeric input fields with bounds
        dice_count = IntEntry(set_frame, width=5, lower_bound=1, upper_bound=12)
        dice_count.grid(row=1, column=1, padx=5, pady=2)

        # Entry for the number of sides per die
        Label(set_frame, text="Dice Sides (max. 50):").grid(row=2, column=0, sticky="w")
        dice_sides = IntEntry(set_frame, width=5, lower_bound=2, upper_bound=50)
        dice_sides.grid(row=2, column=1, padx=5, pady=2)

        # Color selection for the dice face
        Label(set_frame, text="Dice Color:").grid(row=3, column=0, sticky="w")
        dice_color_label = Label(set_frame, text=" ", width=8, relief="solid", bg="white")
        dice_color_label.grid(row=3, column=1, padx=5, pady=2)
        Button(set_frame, text="Choose",
               command=lambda lbl=dice_color_label: lbl.config(bg=colorchooser.askcolor()[1] or "white")
        ).grid(row=3, column=2, padx=5, pady=2)

        # Color selection for the pip/number color
        Label(set_frame, text="Number Color:").grid(row=4, column=0, sticky="w")
        text_color_label = Label(set_frame, text=" ", width=8, relief="solid", bg="black")
        text_color_label.grid(row=4, column=1, padx=5, pady=2)
        Button(set_frame, text="Choose",
               command=lambda lbl=text_color_label: lbl.config(bg=colorchooser.askcolor()[1] or "black")
        ).grid(row=4, column=2, padx=5, pady=2)

        # Add this set's widget references to the global list for later use
        sets.append((set_name, dice_count, dice_sides, dice_color_label, text_color_label))

    # After creating all set frames, adjust the main window size for the configurations
    root.update_idletasks()  # Update geometry calculations
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    # Calculate required size to show all set frames (with some margin)
    req_width = settings_frame.winfo_reqwidth()
    req_height = settings_frame.winfo_reqheight()
    # Limit window size to screen dimensions (with small margins)
    desired_w = min(screen_w - 50, req_width + 20)
    desired_h = min(screen_h - 100, req_height + 20)
    if req_width > (screen_w - 50):
        desired_w = screen_w - 20  # use almost full width if needed
    if req_height > (screen_h - 100):
        desired_h = screen_h - 50  # use almost full height if needed
    root.geometry(f"{int(desired_w)}x{int(desired_h)}")
    # If multiple columns of sets, distribute extra space evenly
    cols = math.ceil(num_sets / 4)
    for c in range(cols):
        grid_frame.grid_columnconfigure(c, weight=1)
    # (Optionally, one could also add a scrollbar if content exceeds screen, but we avoid extra complexity)

def show_dice_results():
    """
    Switch to the results view: hide the settings view and show the results for each set.
    """
    # If no sets have been configured, do not proceed to results
    if len(sets) == 0:
        messagebox.showerror("Error", "No sets configured. Click 'Next' to set up dice sets first.")
        return
    # Hide the settings frame
    settings_frame.pack_forget()
    # Clear any previous result widgets
    for widget in results_menu.winfo_children():
        widget.destroy()

    # Determine layout of result frames based on number of sets
    n_sets = len(sets)
    # Use 3 rows if we have 3 or more sets, otherwise use one row per set
    n_rows = 3 if n_sets >= 3 else n_sets
    # Calculate the number of columns needed (3 sets per column)
    n_columns = math.ceil(n_sets / 3)
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # Define window size for results (full screen minus a small margin)
    desired_width = screen_width - 50
    desired_height = screen_height - 100
    # Calculate cell dimensions for each set's result area
    global cell_width, cell_height
    cell_width = desired_width / n_columns
    cell_height = desired_height / n_rows
    # Resize the main window to fit the results
    root.geometry(f"{desired_width}x{desired_height}")

    # Create a header frame with a back button to return to settings
    header_frame = Frame(results_menu)
    header_frame.pack(side="top", fill="x", pady=5)
    # Back button to return to settings view
    Button(header_frame, text="Back to Settings", command=show_settings).pack(padx=5, pady=5)

    # Create a content frame to hold each set's result section
    content_frame = Frame(results_menu)
    content_frame.pack(fill="both", expand=True)

    # Create a result display frame for each set of dice
    for i, (set_name, dice_count, dice_sides, dice_color_label, text_color_label) in enumerate(sets):
        # Create a fixed-size frame for this set's results
        set_frame = Frame(content_frame, bd=1, relief="groove",
                          width=int(cell_width), height=int(cell_height))
        set_frame.grid_propagate(False)  # prevent the frame from shrinking to fit its content
        set_frame.grid(row=i % 3, column=i // 3, padx=10, pady=10, sticky="nsew")

        # Within each set frame, a sub-frame will hold the Matplotlib canvas for dice
        result_frame = Frame(set_frame)
        result_frame.pack(fill="both", expand=True)
        # Button to roll this set's dice (capturing current parameters via lambda)
        Button(set_frame, text=f"{set_name.get()} - Roll Dice",
               command=lambda rf=result_frame, dc=dice_count, ds=dice_sides, sn=set_name,
                              dc_lbl=dice_color_label, tc_lbl=text_color_label: roll_single_set(
                                  rf, dc, ds, sn.get(), dc_lbl["bg"], tc_lbl["bg"])
        ).pack(side="bottom", pady=2)

    # Show the results frame
    results_menu.pack(fill="both", expand=True)

def show_settings():
    """
    Return to the settings view, hiding the results view.
    """
    results_menu.pack_forget()
    settings_frame.pack(fill="both", expand=True)

# Create the main application window
root = tk.Tk()
root.option_add("*Font", "Arial 12")            # Use a pleasant default font for all widgets
root.title("Dice Roller with Adaptive Sizes")   # Set window title

# Global list to store each set's widgets/configuration
sets = []

# Set up the settings frame (for configuring dice sets)
settings_frame = Frame(root)
settings_frame.pack(fill="both", expand=True)

# Top section of settings: input for number of sets
top_frame = Frame(settings_frame)
top_frame.pack(side="top", fill="x", pady=5)
Label(top_frame, text="How many sets do you want to roll? (1-12)").grid(row=0, column=0, padx=5)
enter_set = IntEntry(top_frame, width=5, lower_bound=1, upper_bound=12)
enter_set.grid(row=0, column=1, padx=5)
# Buttons to proceed or finish configuration:
Button(top_frame, text="Next", command=confirm_sets).grid(row=0, column=2, padx=5)
Button(top_frame, text="Confirm Settings", command=show_dice_results).grid(row=0, column=3, padx=5)

# Frame that will contain the dynamic set configuration frames
grid_frame = Frame(settings_frame)
grid_frame.pack(fill="both", expand=True)

# Frame (initially hidden) that will display the dice roll results for all sets
results_menu = Frame(root)

# Start the Tkinter main loop
root.mainloop()
=======
"""
Dice Roller GUI with Tkinter and Matplotlib.

This application allows the user to define multiple sets of dice. Each set can have a specified number of dice and a chosen number of sides per dice. The user can roll each set individually. For dice with 2 to 6 sides, the result is shown with traditional pip dots; for dice with more than 6 sides, the numerical result is displayed.

The code uses Tkinter for the user interface, Matplotlib for rendering dice faces, and a custom IntEntry widget (from number_entry module) to ensure numeric input within valid ranges.
"""
import tkinter as tk                               # Tkinter for GUI elements
from tkinter import Frame, Label, Button, Entry, messagebox, colorchooser  # Common Tkinter widgets and dialogs
import random                                      # Random for dice rolls
import math                                        # Math for calculations (e.g. ceil)
import matplotlib.pyplot as plt                    # Matplotlib for drawing dice faces
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # To embed Matplotlib figures in Tkinter

# Try to import the custom integer entry widget (IntEntry) for numeric inputs
try:
    from number_entry import IntEntry
except ImportError:
    # If the module is missing, show an error and exit
    messagebox.showerror("Error", "Required module 'number_entry' is missing.")
    exit()

# Global variables for cell dimensions (used when drawing dice faces in result frames)
cell_width = 0
cell_height = 0
# Factors defining what portion of each cell's width and height is used for drawing the dice
dice_area_width_factor = 0.9    # use 90% of cell width for dice graphics
dice_area_height_factor = 0.5   # use 50% of cell height for dice graphics

def draw_dice_face(ax, number, dice_color, text_color, use_dots=False):
    """
    Draw a single dice face on the given Matplotlib axis.

    Parameters:
        ax         - Matplotlib axis on which to draw
        number     - The rolled number to display
        dice_color - Background color of the dice face
        text_color - Color for the number or the pips (dots)
        use_dots   - If True, draw a pip pattern (standard dice pips) instead of a number
    """
    # Clear any previous content on this axis
    ax.clear()
    # Remove ticks for a cleaner look
    ax.set_xticks([])
    ax.set_yticks([])
    # Fix the axis limits to a 0.5x0.5 square (for consistent scaling)
    ax.set_xlim(0, 0.5)
    ax.set_ylim(0, 0.5)
    # Set the background color of the dice face
    ax.set_facecolor(dice_color)

    if use_dots:
        # Pip layouts for dice faces 1 through 6
        pip_positions = {
            1: [(0.25, 0.25)],  # center pip
            2: [(0.1, 0.4), (0.4, 0.1)],  # two pips (diagonal)
            3: [(0.1, 0.4), (0.25, 0.25), (0.4, 0.1)],  # three pips (two diagonal + center)
            4: [(0.1, 0.4), (0.4, 0.4), (0.1, 0.1), (0.4, 0.1)],  # four corner pips
            5: [(0.1, 0.4), (0.4, 0.4), (0.1, 0.1), (0.4, 0.1), (0.25, 0.25)],  # four corners + center
            6: [(0.1, 0.4), (0.4, 0.4), (0.1, 0.25), (0.4, 0.25), (0.1, 0.1), (0.4, 0.1)]  # six pips (three per column)
        }
        # Get the pip layout for the rolled number (default to single center pip if number not in dict)
        dots = pip_positions.get(number, [(0.25, 0.25)])
        # Draw each pip as a small filled circle
        for (x, y) in dots:
            circle = plt.Circle((x, y), 0.04, color=text_color)
            ax.add_artist(circle)
    else:
        # If not using pips, display the number as text in the center of the face
        ax.text(0.25, 0.25, str(number), fontsize=16, ha='center', va='center',
                fontweight='bold', color=text_color)

def roll_single_set(result_frame, dice_count, dice_sides, set_name, dice_color, number_color):
    """
    Roll a single set of dice and display the results in the UI.

    Parameters:
        result_frame - The Tkinter frame where the dice images will be displayed
        dice_count   - IntEntry widget for the number of dice to roll
        dice_sides   - IntEntry widget for the number of sides on each die
        set_name     - Name of the set (string used for labeling purposes)
        dice_color   - Background color for the dice faces
        number_color - Color for the numbers or pips on the dice
    """
    # Remove any previous results from this frame
    for widget in result_frame.winfo_children():
        widget.destroy()
    try:
        # Retrieve the user-specified number of sides and dice count
        sides_val = dice_sides.get()
        count_val = dice_count.get()
        # Validate the input ranges (Sides must be 2-50, Dice Count 1-12)
        if not (2 <= sides_val <= 50) or not (1 <= count_val <= 12):
            raise ValueError
        # Generate random rolls for the given number of dice and sides
        rolls = [random.randint(1, sides_val) for _ in range(count_val)]
    except ValueError:
        # If inputs are invalid, show an error dialog and abort rolling
        messagebox.showerror("Input Error", "Please enter valid values for sides (2-50) and dice count (1-12).")
        return

    # Determine layout for dice faces: up to 6 dice per row
    dice_cols = min(6, count_val)
    # Number of rows needed based on how many dice (6 per row maximum)
    dice_rows = math.ceil(count_val / 6)

    # Calculate an appropriate dice image size (in pixels) based on current window size and defined factors
    die_size_pixels = min((cell_width * dice_area_width_factor) / dice_cols,
                          (cell_height * dice_area_height_factor) / dice_rows)
    # Convert pixel size to inches for Matplotlib (assuming 100 dpi for simplicity: 1 inch = 100 pixels)
    fig_width = (die_size_pixels * dice_cols) / 100
    fig_height = (die_size_pixels * dice_rows) / 100

    # Create a Matplotlib figure with a grid of subplots to represent dice faces
    fig, axes = plt.subplots(dice_rows, dice_cols, figsize=(fig_width, fig_height), dpi=100)
    # Flatten the axes array into a simple list for easy iteration
    if dice_rows * dice_cols == 1:
        axes = [axes]
    elif dice_rows == 1 or dice_cols == 1:
        axes = list(axes)
    else:
        axes = [ax for row in axes for ax in row]

    # Use pip (dot) representation if the dice have 6 or fewer sides, otherwise use numeric
    use_dots = (sides_val <= 6)
    # Draw each rolled dice face on its corresponding subplot
    for ax, roll in zip(axes, rolls):
        draw_dice_face(ax, roll, dice_color, number_color, use_dots=use_dots)
    # If there are more subplot axes than dice (which can happen if count_val is not a multiple of dice_cols), hide the extras
    for ax in axes[len(rolls):]:
        ax.set_visible(False)

    # Embed the Matplotlib figure (dice images) into the Tkinter result frame
    canvas = FigureCanvasTkAgg(fig, master=result_frame)
    canvas.get_tk_widget().pack(pady=5)
    canvas.draw()

    # If more than one die was rolled, also display the sum of all dice at the bottom
    if count_val > 1:
        total = sum(rolls)
        Label(result_frame, text=f"Total: {total}", font=("Arial", 12, "bold")).pack(pady=5)

def confirm_sets():
    """
    Read the number of sets from user input, validate it, 
    create a configuration panel for each set, and saves the configurations in a global list.
    """
    try:
        # Get the desired number of sets from the entry field
        num_sets = enter_set.get()
        # Validate that the number is within allowed range (1-12)
        if not (1 <= num_sets <= 12):
            raise ValueError
    except ValueError:
        # If input is invalid, show an error message and return early
        messagebox.showerror("Error", "Please enter a valid number of sets (1-12).")
        return

    # Reinitialize the global sets list
    global sets
    sets = []
    # Clear any existing set configuration frames
    for widget in grid_frame.winfo_children():
        widget.destroy()

    # Create configuration frames for each set
    # Sets will be arranged in a grid with a maximum of 4 rows per column
    for i in range(num_sets):
        # Create a frame for this set's configuration (with border and padding for visibility)
        set_frame = Frame(grid_frame, bd=1, relief="groove", padx=5, pady=5)
        # Position frames in a grid: 4 rows per column (new column after every 4 sets)
        set_frame.grid(row=i % 4, column=i // 4, padx=10, pady=10, sticky="nsew")

        # Entry for the set name
        Label(set_frame, text=f"Set {i+1} Name:").grid(row=0, column=0, sticky="w")
        set_name = Entry(set_frame, width=15)
        set_name.grid(row=0, column=1, padx=5, pady=2)

        # Entry for the dice count in this set
        Label(set_frame, text="Dice Count (max. 12):").grid(row=1, column=0, sticky="w")
        # Use IntEntry for numeric input fields with bounds
        dice_count = IntEntry(set_frame, width=5, lower_bound=1, upper_bound=12)
        dice_count.grid(row=1, column=1, padx=5, pady=2)

        # Entry for the number of sides per die
        Label(set_frame, text="Dice Sides (max. 50):").grid(row=2, column=0, sticky="w")
        dice_sides = IntEntry(set_frame, width=5, lower_bound=2, upper_bound=50)
        dice_sides.grid(row=2, column=1, padx=5, pady=2)

        # Color selection for the dice face
        Label(set_frame, text="Dice Color:").grid(row=3, column=0, sticky="w")
        dice_color_label = Label(set_frame, text=" ", width=8, relief="solid", bg="white")
        dice_color_label.grid(row=3, column=1, padx=5, pady=2)
        Button(set_frame, text="Choose",
               command=lambda lbl=dice_color_label: lbl.config(bg=colorchooser.askcolor()[1] or "white")
        ).grid(row=3, column=2, padx=5, pady=2)

        # Color selection for the pip/number color
        Label(set_frame, text="Number Color:").grid(row=4, column=0, sticky="w")
        text_color_label = Label(set_frame, text=" ", width=8, relief="solid", bg="black")
        text_color_label.grid(row=4, column=1, padx=5, pady=2)
        Button(set_frame, text="Choose",
               command=lambda lbl=text_color_label: lbl.config(bg=colorchooser.askcolor()[1] or "black")
        ).grid(row=4, column=2, padx=5, pady=2)

        # Add this set's widget references to the global list for later use
        sets.append((set_name, dice_count, dice_sides, dice_color_label, text_color_label))

    # After creating all set frames, adjust the main window size for the configurations
    root.update_idletasks()  # Update geometry calculations
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    # Calculate required size to show all set frames (with some margin)
    req_width = settings_frame.winfo_reqwidth()
    req_height = settings_frame.winfo_reqheight()
    # Limit window size to screen dimensions (with small margins)
    desired_w = min(screen_w - 50, req_width + 20)
    desired_h = min(screen_h - 100, req_height + 20)
    if req_width > (screen_w - 50):
        desired_w = screen_w - 20  # use almost full width if needed
    if req_height > (screen_h - 100):
        desired_h = screen_h - 50  # use almost full height if needed
    root.geometry(f"{int(desired_w)}x{int(desired_h)}")
    # If multiple columns of sets, distribute extra space evenly
    cols = math.ceil(num_sets / 4)
    for c in range(cols):
        grid_frame.grid_columnconfigure(c, weight=1)
    # (Optionally, one could also add a scrollbar if content exceeds screen, but we avoid extra complexity)

def show_dice_results():
    """
    Switch to the results view: hide the settings view and show the results for each set.
    """
    # If no sets have been configured, do not proceed to results
    if len(sets) == 0:
        messagebox.showerror("Error", "No sets configured. Click 'Next' to set up dice sets first.")
        return
    # Hide the settings frame
    settings_frame.pack_forget()
    # Clear any previous result widgets
    for widget in results_menu.winfo_children():
        widget.destroy()

    # Determine layout of result frames based on number of sets
    n_sets = len(sets)
    # Use 3 rows if we have 3 or more sets, otherwise use one row per set
    n_rows = 3 if n_sets >= 3 else n_sets
    # Calculate the number of columns needed (3 sets per column)
    n_columns = math.ceil(n_sets / 3)
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # Define window size for results (full screen minus a small margin)
    desired_width = screen_width - 50
    desired_height = screen_height - 100
    # Calculate cell dimensions for each set's result area
    global cell_width, cell_height
    cell_width = desired_width / n_columns
    cell_height = desired_height / n_rows
    # Resize the main window to fit the results
    root.geometry(f"{desired_width}x{desired_height}")

    # Create a header frame with a back button to return to settings
    header_frame = Frame(results_menu)
    header_frame.pack(side="top", fill="x", pady=5)
    # Back button to return to settings view
    Button(header_frame, text="Back to Settings", command=show_settings).pack(padx=5, pady=5)

    # Create a content frame to hold each set's result section
    content_frame = Frame(results_menu)
    content_frame.pack(fill="both", expand=True)

    # Create a result display frame for each set of dice
    for i, (set_name, dice_count, dice_sides, dice_color_label, text_color_label) in enumerate(sets):
        # Create a fixed-size frame for this set's results
        set_frame = Frame(content_frame, bd=1, relief="groove",
                          width=int(cell_width), height=int(cell_height))
        set_frame.grid_propagate(False)  # prevent the frame from shrinking to fit its content
        set_frame.grid(row=i % 3, column=i // 3, padx=10, pady=10, sticky="nsew")

        # Within each set frame, a sub-frame will hold the Matplotlib canvas for dice
        result_frame = Frame(set_frame)
        result_frame.pack(fill="both", expand=True)
        # Button to roll this set's dice (capturing current parameters via lambda)
        Button(set_frame, text=f"{set_name.get()} - Roll Dice",
               command=lambda rf=result_frame, dc=dice_count, ds=dice_sides, sn=set_name,
                              dc_lbl=dice_color_label, tc_lbl=text_color_label: roll_single_set(
                                  rf, dc, ds, sn.get(), dc_lbl["bg"], tc_lbl["bg"])
        ).pack(side="bottom", pady=2)

    # Show the results frame
    results_menu.pack(fill="both", expand=True)

def show_settings():
    """
    Return to the settings view, hiding the results view.
    """
    results_menu.pack_forget()
    settings_frame.pack(fill="both", expand=True)

# Create the main application window
root = tk.Tk()
root.option_add("*Font", "Arial 12")            # Use a pleasant default font for all widgets
root.title("Dice Roller with Adaptive Sizes")   # Set window title

# Global list to store each set's widgets/configuration
sets = []

# Set up the settings frame (for configuring dice sets)
settings_frame = Frame(root)
settings_frame.pack(fill="both", expand=True)

# Top section of settings: input for number of sets
top_frame = Frame(settings_frame)
top_frame.pack(side="top", fill="x", pady=5)
Label(top_frame, text="How many sets do you want to roll? (1-12)").grid(row=0, column=0, padx=5)
enter_set = IntEntry(top_frame, width=5, lower_bound=1, upper_bound=12)
enter_set.grid(row=0, column=1, padx=5)
# Buttons to proceed or finish configuration:
Button(top_frame, text="Next", command=confirm_sets).grid(row=0, column=2, padx=5)
Button(top_frame, text="Confirm Settings", command=show_dice_results).grid(row=0, column=3, padx=5)

# Frame that will contain the dynamic set configuration frames
grid_frame = Frame(settings_frame)
grid_frame.pack(fill="both", expand=True)

# Frame (initially hidden) that will display the dice roll results for all sets
results_menu = Frame(root)

# Start the Tkinter main loop
root.mainloop()
>>>>>>> 7f9cce714ad0d44fa1f11403ef413a51d9dc890d
