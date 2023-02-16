# Arabic_NLP
This repository contain some scripts can process  the Arabic Language :

 - dataset_split.sh: useful to separate a data text into 3: train, test, and val.
 - cleaner_ar_data.py: useful to clean any Arabic data, also you can used to clean data for punctuattion task or for Language model (without punctuation marks)
### Clean data for punctation task:
  ```
  python3 cleaner_ar_data.py --punctuation --input=<path_to_input_text> --output=<path_to_output_text>
  ```
### Clean data for language model task:
  ```
  python3 cleaner_ar_data.py --forlm --input=<path_to_input_text> --output=<path_to_output_text>
  ```
