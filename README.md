# web-autocorrector

web-autocorrector is a flask app based on the [fq-hll autocorrection algorithm](https://github.com/shun4midx/FQ-HyperLogLog-Autocorrect) with [queryable api](https://github.com/ducky4life/web-autocorrector?tab=readme-ov-file#api-usage), one-click deploy to vercel:

[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/import/project?template=https://github.com/ducky4life/web-autocorrector)

## hyperloglog

uses the extremely cool, [accurate, and low-memory-usage](https://github.com/shun4midx/FQ-HyperLogLog-Autocorrect/tree/main/fq_hll_py#results) autocorrect algorithm library which you can read more about [here](https://github.com/shun4midx/FQ-HyperLogLog-Autocorrect)!!! star the repository and `pip install fq-hll` or `pip install DyslexicLogLog` :D

https://github.com/shun4midx/FQ-HyperLogLog-Autocorrect

## api usage

by default, the api is started from app.py. you can host the api as standalone app by adding the stuff in app.py before and after `main_route()` to api.py

only query is a required argument. the rest is optional and can be excluded.

note that dictionaries from web url or uploads would be treated as if it's from most to least frequently used. this is also true for the web ui. host the app locally and provide local file path to custom dictionary to avoid this

### arguments

`query` (required) - input text or raw txt file link to be processed

`number` - the number of possible autocorrected words to output for each word. defaults to 1.

`dictionary` - a raw txt file link with one word on each line to be used as the custom dictionary for the algorithm

`separator` - a string that separates each word in the input. defaults to spaces. you should use `separator=\n` for most txt files.

`prettify` - whether to prettify the json output into human readable form or leave it as one line. defaults to False.

### api examples

example query with all arguments:

`curl -d 'query=wwo/htis/alogirthm/so/coolo' -d 'number=3' -d 'dictionary=https://raw.githubusercontent.com/shun4midx/FQ-HyperLogLog-Autocorrect/refs/heads/main/fq_hll_py/src/fq_hll/test_files/20k_shun4midx.txt' -d 'separator=/' -d 'prettify=False' https://web-autocorrector.vercel.app/api`

returns:

> {"alogirthm":["algorithm","algorithms","triathlon"],"coolo":["cool","color","colon"],"htis":["tits","this","hits"],"so":["so","sos","soo"],"wwo":["wow","two","www"]}

`query` also supports text file links like with the dictionary in the example

example query with file input:

`curl -d 'query=https://raw.githubusercontent.com/ducky4life/web-autocorrector/refs/heads/main/requirements.txt' -d 'separator=\n' https://web-autocorrector.vercel.app/api`

returns:

> {"DyslexicLogLog":["toxicology"],"flask":["alaska"],"flask-restful":["breakfasts"],"requests":["requests"],"waitress":["treaties"]}

## features

- queryable api using curl
- custom dictionary file from uploads or web url or local file path
- export to file as json object/python dictionary
- import input file from uploads or web url or input textbox

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

## Usage (Docker)

make sure you have [docker](https://www.docker.com) installed.

[building from source](https://github.com/ducky4life/web-autocorrector#building-the-images-from-source-recommended) is recommended since it is how i mainly test the packages and you get the most up to date dependencies.

amd64 packages are not tested since i only have an arm64 rasp pi with docker.

### Using pre-built images

1. get the correct package for your archetecture

   [amd64](https://github.com/ducky4life/web-autocorrector/pkgs/container/web-autocorrector%2Fweb-fqhll-amd64):
   ```
   docker pull ghcr.io/ducky4life/web-autocorrector/web-fqhll-amd64:latest
   ```
   [arm64](https://github.com/ducky4life/web-autocorrector/pkgs/container/web-autocorrector%2Fweb-fqhll-arm64):
   ```
   docker pull ghcr.io/ducky4life/web-autocorrector/web-fqhll-arm64:latest
   ```
2. run the docker container

   amd64:
   ```
   docker run -p 8080:8080 --name web-fqhll ghcr.io/ducky4life/web-autocorrector/web-fqhll-amd64:latest
   ```
   arm64:
   ```
   docker run -p 8080:8080 --name web-fqhll ghcr.io/ducky4life/web-autocorrector/web-fqhll-arm64:latest
   ```
3. go to http://localhost:8080/

### Building the images from source (recommended)

1. clone the repository
   ```
   git clone https://github.com/ducky4life/web-autocorrector.git
   ```
2. move into directory
   ```
   cd web-autocorrector
   ```
3. build the docker image for your archetecture

   amd64:
   ```
   docker build -t web-fqhll:latest -f amd64.Dockerfile .
   ```
   arm64:
   ```
   docker build -t web-fqhll:latest -f arm64.Dockerfile .
   ```
4. run the docker container
   ```
   docker run -p 8080:8080 --name web-fqhll web-fqhll:latest
   ```
5. go to http://localhost:8080/


## to do list

- [x] import from/export to file
- [x] import from url
- [x] custom dictionary support
- [x] queryable api
- [x] separate by both spaces and newlines instead of commas
- [x] make prettify_autocorrector renders in br tags/new lines
- [ ] toggle button for raw output in web
- [x] make json output prettier
- [x] add toggle pretty json output to api
- [ ] export to file option for api
