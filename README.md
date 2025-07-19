# web-autocorrector

web-autocorrector is a flask app based on the [fq-hll autocorrect algorithm](https://github.com/shun4midx/FQ-HyperLogLog-Autocorrect)

[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/import/project?template=https://github.com/ducky4life/web-autocorrector)

## hyperloglog

uses the extremely cool, [accurate, and low-memory-usage](https://github.com/shun4midx/FQ-HyperLogLog-Autocorrect/tree/main/fq_hll_py#results) autocorrect algorithm library which you can read more about [here](https://github.com/shun4midx/FQ-HyperLogLog-Autocorrect)!!! star the repository and `pip install fq-hll` or `pip install DyslexicLogLog` :D

https://github.com/shun4midx/FQ-HyperLogLog-Autocorrect

## Usage (Python)

make sure you have [python](https://www.python.org/downloads/) installed.

1. clone the repository
   ```
   git clone https://github.com/ducky4life/web-autocorrector.git
   ```
2. move into directory
   ```
   cd web-autocorrector
   ```
3. install dependencies
   ```
   pip install -r requirements.txt
   ```
4. run the app
   ```
   python app.py
   ```
5. go to http://localhost:8080/
