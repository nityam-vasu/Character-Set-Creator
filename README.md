
# Character Set Creator

A Python-based Tkinter application for drawing Hindi characters on a dynamic grid, saving them as PNG images for machine learning datasets. Features continuous drawing, undo, resume functionality, and a standalone executable. Includes a sample character file and automated tests for reliability.
Features


## Features

Draw characters on a dynamic 32x32 grid (or user-specified size).
Continuous drawing with click-and-drag.
Save drawings as PNGs in character-specific subdirectories.
Undo up to 10 recent grid changes.
Pause and resume drawing with a "Close (Draw Later)" button, saving remaining characters to a resume file.

Input characters via a .txt file and specify drawing frequency.

 Sample Character File:\
[See example](See example)


## Features

- Light/dark mode toggle
- Changable Grid Size
- Fullscreen mode
- Cross platform


## Screenshots

![Main](https://github.com/nityam-vasu/Character-Set-Creator/blob/main/screenshots/Main.png)

![Grid](https://github.com/nityam-vasu/Character-Set-Creator/blob/main/screenshots/Drawing.png)

![a](https://github.com/nityam-vasu/Character-Set-Creator/blob/main/screenshots/a.png)

![b](https://github.com/nityam-vasu/Character-Set-Creator/blob/main/screenshots/b.png)


## Installation


Clone the repository:

```bash
  git clone https://github.com/nityam-vasu/character-set-creator.git
  cd character-set-creator
  ```


### Requirements

- Python 3.6 or higher
- Tkinter (included with Python)
- Pillow

- Create a virtual environment (optional but recommended):
  ```bash
  python -m venv venv
  source venv/bin/activate  
  
  # On Windows: 
  venv\Scripts\activate
  ```

- Install Required Library  
  ```bash
    pip install -r requirements.txt
  ```    
## Usage/Examples

### Initial Screen:

- Select a base output folder for saving drawings.
- Choose a .txt file with Characters (each line) ( See Example).
- Enter the frequency (number of drawings per character).
- Click "Start Drawing".


### Drawing Interface:

Draw on the grid by clicking and dragging.
  #### Use buttons:
    - Save: Save the drawing as a PNG (or press Enter).
    - Clear: Reset the grid.
    - Undo: Revert up to 10 recent changes.
    - Save Remaining: Save remaining characters and return to the initial screen.


- Change grid size (4-100) via the input field.

_Note - Resize the window to adjust the canvas dynamically._


## Output:

Drawings are saved in base_folder/character/character_number.png\
 _(e.g., output/a/a_1.png)_


If paused or closed early, a *resume_<original_txt_name>.txt* file is created with remaining characters.


Sample Character File: [See example](See example)

## License
This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/) . See the LICENSE file for details.


#### Contact
For issues or suggestions, open an issue on GitHub
