suppressWarnings(suppressMessages(library("httr2", quietly = T)))
suppressWarnings(suppressMessages(library("rvest", quietly = T)))
suppressWarnings(suppressMessages(library("stringr", quietly = T)))
suppressWarnings(suppressMessages(library("tibble", quietly = T)))
suppressWarnings(suppressMessages(library("dplyr", quietly = T)))
suppressWarnings(suppressMessages(library("tidyr", quietly = T)))
suppressWarnings(suppressMessages(library("rio", quietly = T)))

message("Downloading table from wikipedia.org")
wiki_perennial_sources_raw <- request("https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources/Perennial_sources") |>
  req_headers(
    "User-Agent" = "Perennial_Sources_Check/1.0 (https://dr.schatto-eckrodt.de/; tim.schatto-eckrodt@uni-hamburg.de) generic-library/0.0"
  ) |> 
  req_perform() |>
  resp_body_string() |> 
  read_html() |>
  html_element("table.perennial-sources") |>
  html_elements("tbody tr")

message("Extracting domains")
domains <- wiki_perennial_sources_raw |>
  html_element("td:nth-child(6)") |>
  lapply(FUN = \(x) {
    x |>
      html_elements("a") |>
      html_attr("href") |>
      str_extract(
        pattern = "https:\\/\\/en.wikipedia.org\\/wiki\\/Special:Search\\/insource:\\\"(.*)\\\"$",
        group = 1
      ) |>
      na.omit() |>
      as.character() |>
      list()
  })
message("Extracting categories")
categories <- wiki_perennial_sources_raw |>
  html_element("td:nth-child(2)") |>
  html_element("a") |>
  html_attr("title")
message("Extracting titles")
titles <- wiki_perennial_sources_raw |>
  html_element("td:nth-child(1)") |>
  html_text()
message("Combine to data set and save")
wiki_perennial_sources <- cbind(
  titles,
  domains[!is.na(domains)],
  categories
) |>
  as.data.frame() |>
  rename(title = 1, domain = 2, wiki_cat = 3) |>
  mutate(across(-domain, unlist)) |>
  unnest(domain) |>
  unnest(domain) |>
  mutate(title = str_remove(title, " WP:.*$"))

wiki_perennial_sources |> export(file = "wiki_perennial_sources.csv")