# Iconclass Extraction

This project contains code for extracting (possibly fragmented)
iconclass codes from text.

## Installation

Create a [virtual environment](https://docs.python.org/3/library/venv.html)
by executing the following command:

```bash
python3 -m venv venv
```

To activate the virtual environment, execute:

```bash
source venv/bin/activate
```

Then, install all python libraries, the project relies on using
the package manager [pip](https://pip.pypa.io/en/stable/):

```bash
pip3 install -r requirements.txt
```

After installing all dependencies, install the pretrained
spacy you wish to use as base model.
For example:

```bash
python3 -m spacy download en_core_web_sm
```

## Model Training

The extraction uses a custom trained NER tagger based
on spacy. For that, the following steps are neccessary
to execute either by hand or in code:

0. Rename the .template.env-file to .env and fill in
   the corresponding file locations according to your
   setup.

1. Load texts containing iconclass codes and store them
   batchwise in text files. Within each file, the texts
   are separated by empty lines. To do so, run the
   script `extract_text_to_annotate.py`. If the source
   file format deviates from .nt, you might have to
   implement a custom load method.

2. Annotate the created text file through
   [this tool](https://tecoholic.github.io/ner-annotator/).
   Use the named entity tags "IC_START" and "IC_CONTD" to label new
   iconclass codes and continuations respectively.
   The names you assign to those labels are important,
   since as of now they are hard coded in downstream scripts.

3. Adjust the format of the annotated data to match
   spacy's requirements. For that, execute the `format_annotated_data.py` script.

4. Create a config file for your training setup as described
   [here](https://spacy.io/usage/training#quickstart).

5. Train your model by running
   `python -m spacy train config.cfg --output ./output --paths.train ./train.spacy --paths.dev ./dev.spacy`

For an external example of the described process,
see [this code](https://github.com/dreji18/NER-Training-Spacy-3.0/blob/main/NER%20Training%20with%20Spacy%20v3%20Notebook.ipynb).

## Usage

Once the required dependencies have been installed,
you can run the test server by executing

```bash
uvicorn server:app --reload
```

To include the extraction logic in other scripts,
load the trained nlp model and pass it to the
_extract_iconclass_codes_ function as follows:

```python
import spacy
from extract_iconclass_codes import extract_iconclass_codes

nlp = spacy.load("./data/output/model-last")

text = "..."
codes = extract_iconclass_codes(text, nlp=nlp)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
