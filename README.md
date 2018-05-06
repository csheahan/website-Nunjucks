# Website-Nunjucks
My website built using Nunjucks.
Currently hosted at [https://www.csheahan.com](https://www.csheahan.com).
The website has been using Nunjucks from 5/6/2018 to present.

## Setup
There are a few gulp packages and plugins required, all of which should be installed with `npm install`.

## Gulp
The following gulp commands can be used to generate and validate the html.

| Command | Description |
|---------|-------------|
| `gulp` | Builds the website, outputting to public_html. Same as `gulp website`. |
| `gulp website` | Builds the website to public_html. |
| `gulp clean` | Cleans the public_html folder. |
| `gulp validate` | Checks html in public_html folder for 404's in <a> tags and for spelling errors. |

There are other gulp commands, but they are all run through the above commands.