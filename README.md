# Welree Django Project #

# Pre-requisites:
* python
* pip
 * sudo easy_install pip
* [optional] virtualenv
 * pip install virtualenv
* [homebrew](http://brew.sh/)
* brew install libmemcached memcached nginx libxml2
* prepare Solr (our search backend)
  * download and extract http://archive.apache.org/dist/lucene/solr/4.7.2/solr-4.7.2.zip
  * specify the location in a line in your ~/.bashrc such as `export SOLR_EXAMPLE="$HOME/Downloads/solr-4.7.2/example"`
  * don't forget to `source ~/.bashrc`

# Installation:
From the directory of the repository:

1. virtualenv env && source env/bin/activate
1. pip install -r requirements.txt
1. cd website
1. pbdeploy [starts/restarts application, performing any necessary bootstrapping]
1. open http://local.welree.com:33100
1. pbdeploy stop
