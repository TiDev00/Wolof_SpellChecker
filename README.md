# Wolof_SpellChecker

This is a fast spell checker tool implemented in Python that uses a trie node data structure 
and weighted Levenshtein distance algorithm for efficient and accurate spelling correction. 
The tool takes a text file as input, identifies misspelled words, and generates a new file with corrected text.

## Features

- Trie node data structure for efficient word lookup and suggestion generation.
- Wolof Lexicon Lookup
- Weighted Levenshtein distance algorithm to calculate the similarity between words.
- Dynamic programming to optimize the Levenshtein distance calculation.
- Generates a new file with corrected text, preserving the original file's formatting.

## Installation

1. Clone the repository to your local machine or download the zip file
    ```
   git clone https://github.com/TiDev00/Wolof_SpellChecker.git
    ```
   
2. Navigate to the project directory and Create a virtual environment (optional but recommended)
    ```
    python -m venv env
    ```
   
3. Activate the virtual environment

   - For Windows:

     ```
     env\Scripts\activate
     ```

   - For Linux/macOS:

     ```
     source env/bin/activate
     ```

4. Install the required packages using pip:
    ```
    pip install -r requirements.txt
    ```


## Usage

1. Ensure that you have activated the virtual environment (if created).

2. Run the spell checker tool with the following command:

    ```
   python autocorrector.py /path/to/input_file.txt
   ```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, 
please create an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- The tool is based on the concepts of trie node, weighted Levenshtein distance, lexicon lookup and
dynamic programming.
- Thanks to the open-source community for the packages used in this project.

## Citation

If you use this spell checker tool in your research or project, please cite the paper :
```

```