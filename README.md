# Wikipedia - Perennial sources

This repository contains a list of sources drawn from the Wikipedia article [Wikipedia:Reliable sources/Perennial sources](https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources/Perennial_sources) in the crawler script used to generate the list.

> This is a non-exhaustive list of sources whose reliability and use on Wikipedia are frequently discussed. This list summarizes prior consensus and consolidates links to the most in-depth and recent discussions from the reliable sources noticeboard and elsewhere on Wikipedia. [-- About](https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources/Perennial_sources)

The file `perennial-sources.csv` contains all entries from the above list, including a field for the source’s name (`name`), the reliability status(es) of the source (`status`), the link to the corresponding Wikipedia article (`wiki_url`), a list of urls that link to the source (`urls`) , and the summary info from the original list (`info`). The `urls` field is drawn from the infobox and the “External links” section of the source’s Wikipedia article. For some sources there a multiple urls (not necessarily to the sources homepage) and for some there are none.

This should be seen as a staring point and should be validated by human coders before use. Please see the [article](https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources/Perennial_sources) for an explanation of the different reliability statuses. An “unreliable” source might not exclusively contain misinformation or be operated by malicious actors. For example, the Wikipedia itself is categorized as unreliable (“Wikipedia is not a reliable source because open wikis are self-published sources”).

The list was generated on 2021-03-17 and is shared under [Creative Commons Attribution-ShareAlike](https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License).

## Usage example

```
# Dependencies
library(readr)
library(dplyr)
library(jsonlite)

# Read data
perennial_sources <- read_csv("perennial-sources.csv") %>% 
    mutate(urls = lapply(urls, jsonlite::fromJSON)) %>% 
    mutate(status = lapply(status, jsonlite::fromJSON))

# Get list of sources
list_of_sources <- perennial_sources %>% 
    slice(rep(1:n(), urls_n)) %>% 
    mutate(url = unlist(perennial_sources$urls))

list_of_sources <- list_of_sources %>% 
    slice(rep(1:n(), status_n)) %>% 
    mutate(status = unlist(list_of_sources$status)) %>% 
    select(name, status, url, info, wiki_url)
list_of_sources <- split(list_of_sources, list_of_sources$status)

> head(list_of_sources["Generally unreliable"], 5)
$`Generally unreliable`
# A tibble: 140 x 5
   name      status     url               info                     wiki_url         
   <chr>     <chr>      <chr>             <chr>                    <chr>            
 1 112 Ukra… Generally… 112ua.tv          "112 Ukraine was deprec… https://en.wikip…
 2 Ad Fonte… Generally… www.adfontesmedi… "There is consensus tha… https://en.wikip…
 3 Advameg … Generally… www.city-data.com "Advameg operates conte… https://en.wikip…
 4 AllGov.c… Generally… allgov.com        "There is consensus tha… https://en.wikip…
 5 AlterNet  Generally… www.alternet.org  "There is consensus tha… https://en.wikip…
```