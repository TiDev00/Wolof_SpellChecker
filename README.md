# Automatic SpellChecking and Correction for Wolof Language

![Wolof Language](https://img.shields.io/badge/language-Wolof-red)

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

This project is licensed under the [MIT License](https://github.com/TiDev00/Wolof_SpellChecker/blob/master/LICENSE).

## Acknowledgments

- The tool is based on the concepts of trie node, weighted Levenshtein distance, lexicon lookup and
dynamic programming.
- Thanks to the open-source community for the packages used in this project.

## Citation

If you use these resources in your research or project, please cite the paper :
```
@inproceedings{cisse-sadat-2023-automatic,
    title = "Automatic Spell Checker and Correction for Under-represented Spoken Languages: Case Study on {W}olof",
    author = "Ciss{\'e}, Thierno Ibrahima  and
      Sadat, Fatiha",
    booktitle = "Proceedings of the Fourth workshop on Resources for African Indigenous Languages (RAIL 2023)",
    month = may,
    year = "2023",
    address = "Dubrovnik, Croatia",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.rail-1.1",
    pages = "1--10",
    abstract = "This paper presents a spell checker and correction tool specifically designed for Wolof, an under-represented spoken language in Africa. The proposed spell checker leverages a combination of a trie data structure, dynamic programming, and the weighted Levenshtein distance to generate suggestions for misspelled words. We created novel linguistic resources for Wolof, such as a lexicon and a corpus of misspelled words, using a semi-automatic approach that combines manual and automatic annotation methods. Despite the limited data available for the Wolof language, the spell checker{'}s performance showed a predictive accuracy of 98.31{\%} and a suggestion accuracy of 93.33{\%}.Our primary focus remains the revitalization and preservation of Wolof as an Indigenous and spoken language in Africa, providing our efforts to develop novel linguistic resources. This work represents a valuable contribution to the growth of computational tools and resources for the Wolof language and provides a strong foundation for future studies in the automatic spell checking and correction field.",
}
```
