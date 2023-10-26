# Iconclass Extraction

This project contains code for extracting (possibly fragmented)
iconclass codes from text.

## Installation

## Prerequisites

The extraction uses a custom trained NER tagger based
on spacy. For that, the following steps are neccessary
to execute either by hand or in code:

1. Load texts containing iconclass codes and store them
   batchwise in text files. Within each file, the texts
   are separated by empty lines. To do so, adjust and
   run the [TBD] script.

2. Annotate the created text file using
   [this tool](https://tecoholic.github.io/ner-annotator/).

3. Adjust the format of the annotated data to match
   spacy's requirements. For that, execute the [TBD] script.

4. Create a config file for your training setup as described
   [here](https://spacy.io/usage/training#config).

5. Train your model by running
   `python -m spacy train config.cfg --output ./output --paths.train ./train.spacy --paths.dev ./dev.spacy`

For an external example of the described process,
see [this code](https://github.com/dreji18/NER-Training-Spacy-3.0/blob/main/NER%20Training%20with%20Spacy%20v3%20Notebook.ipynb).

## Usage

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
