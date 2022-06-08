# PUDL Utils for Zenodo storage and packaging

## Background on Zenodo

[Zenodo](https://zenodo.org/) is an open repository maintained by CERN that allows users to archive research-related digital artifacts for free. Catalyst uses Zenodo to archive raw datasets scraped from the likes of FERC, EIA, and the EPA to ensure reliable, versioned access to the data PUDL depends on. Take a look at our archives
[here](https://zenodo.org/communities/catalyst-cooperative/?page=1&size=20). In the
event that any of the publishers change the format or contents of their data, remove old years, or simply cease to exist, we will have a permanent record of the data. All data uploaded to Zenodo is assigned a DOI for streamlined access and citing.

Whenever the historical data changes substantially or new years are added, we make new Zenodo archives and build out new versions of PUDL that are compatible. Paring specific Zenodo archives with PUDL releases ensures a functioning ETL for users and developers.

Once created, Zenodo archives cannot be deleted. This is, in fact, their purpose! It
also means that one ought to be sparing with the information uploaded. We don't want
wade through tons of test uploads when looking for the most recent version of data. Luckily Zenodo has created a sandbox environment for testing API integration. Unlike
the regular environment, the sandbox can be wiped clean at any time. When testing
uploads, you'll want to upload to the sandbox first. Because we want to keep our Zenodo
as clean as possible, we keep the upload tokens internal to Catalyst. If there's data
you want to see integrated, and you're not part of the team, send us an email at
hello@catalyst.coop.

One last thing-- Zenodo archives for particular datasets are referred to as
"depositions". Each dataset is it's own deposition that gets created when the
dataset is first uploaded to Zenodo and versioned as the source releases new data that gets uploaded to Zenodo.

## Installation

We recommend using mamba to create and manage your environment.

In your terminal, run:
```
$ mamba env create -f environment.yml
$ mamba activate pudl-zenodo-storage
```

## Adding a New Data Source
When you're adding an entirely new dataset to the PUDL, your first course of action is building a scrapy script in the
[`pudl-scrapers`](https://github.com/catalyst-cooperative/pudl-scrapers) repo. Once
you've done that, you're ready to archive.

First, you'll need to fill in some metadata in the `pudl` repo. Start by adding a new
key value pair in the `SOURCE` dict in the `pudl/metadata/source.py` module. It's best
to keep the key (the source name) you choose simple and consistent across all repos that reference the data. Once you've done this, you'll need to install your local version
of pudl (rather than the default version from GitHub). Doing this will allow the Zenodo archiver script to process changes you made to the `pudl` repo.

While in the `pudl-zenodo-storage` environment, navigate to the `pudl` repo and run:
```
$ pip install -e ./
```

You don't need to worry about the `fields.py` module until you're ready to transform the
data in pudl.

Now, come back to this repo and create a module for the dataset in the `frictionless`
directory. Give it the same name as the key you made for the data in the SOURCE dict.
Use the existing modules as a model for your new one. The main function is called
`datapackager()` and it serves to produce a json for the Zenodo archival collection.

Lastly, you need to:
- Create archive metadata for the new dataset in the `zs/metadata.py` module.
- Add the chosen deposition name to this list of acceptable names output with the `zenodo_store --help` flag. See `parse_main()` in `zs.cli.py`.
- Add specifications for your new deposition in the `archive_selection()` function also in `zs.cli.py`.

## Updating an Existing Data Source
If updating an existing data source--say, one that as released a new year's worth of
data--you don't need to add any new metadata to the `pudl` repo. Simply run the scraper
for the data and then run the Zenodo script as described below. The code was built to
detect any changes in the data and automatically create a new version of the same deposition when uploaded.

## Running the Zenodo Archiver Script  
Before you can archive data, you'll need to run the scrapy script you just created in
the `pudl-scrapers` repo. Once you've scraped the data, then you can come back and run the archiver. This script, `zenodo_store` gets defined as an entry point in `setup.py`.

Next, you'll need to define `ZENODO_SANDBOX_TOKEN_UPLOAD` and `ZENODO_TOKEN_UPLOAD` environment variables on your local machine. As mentioned above, we keep these values
internal to Catalyst so as to maintain a clean and reliable archive.

The `zenodo_store` script requires you to include the name of the Zenodo deposition as
an argument. This is a string value that indicates which dataset you're going to upload. Use the `--help` flag to see a list of supported strings. You can also find a list of
the deposition names in the `archive_selection()` function in the `cli.py` module.

When you're testing an archive, you'll want to make sure you use the Zenodo
sandbox rather than the official Zenodo archive (see above for more info about the sandbox). Adding the `--verbose` flag will print out logging messages that are helpful for debugging. Adding the `--noop` flag will show you whether your the data you scraped
is any different from the data you already have uploaded to Zenodo without uploading anything (so long as there is an existing upload to compare it to).

If the dataset is brand new, you'll also need to add the `--initialize` flag so that it knows to create a new deposition for the data.

Make sure a new deposition knows where to grab scraped data:
```
$ zenodo_store newdata --noop --verbose
Archive would contain: path/to/scraped/data
```

Compare a newly scraped deposition to the currently archived deposition of the same
dataset. If you get the output depicted below then the archive data is the same as the
scraped data, and you don't need to make a new version!
```
$ zenodo_store newdata --noop
{
    "create": {},
    "delete": {},
    "update": {}
}
```

Test run a new deposition in the sandbox (the output link is fake!):
```
$ zenodo_store newdata --sandbox --verbose --initialize
Uploaded path/to/scraped/data
Your new deposition archive is ready for review at https://sandbox.zenodo.org/deposit/number
```

Once you're confident with your upload, you can go ahead and run the script without any
flags.
```
$ zenodo_store newdata
```

## Repo Contents

### zs

The zs.ZenodoStorage class provides an interface to create archives and upload
files to Zenodo.

### frictionless

Package metadata in dict formats, as necessary to support the frictionless
[datapackage library](https://frictionlessdata.io/docs/using-data-packages-in-python/)
specification.
