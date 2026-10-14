# Read the pipeline's file paths from CONFIG.txt.
#
# CONFIG.txt has one KEY="value" per line (it is also valid bash, so the shell
# wrappers can `source` it). A value may use ${KEY} to refer to a key defined
# above it or to an environment variable.
#
# Scripts load it with the block below, which finds the repo root from the
# script's own location (Rscript) or the working directory (RStudio), and use
# cfg$KEY. Asking for a key that is not in CONFIG.txt is an error.
#
#   .repo <- normalizePath(c(gsub("~+~", " ", sub("^--file=", "", grep("^--file=", commandArgs(), value = TRUE)), fixed = TRUE), getwd())[1])
#   while (!file.exists(file.path(.repo, "pfn_config.R")) && dirname(.repo) != .repo) .repo <- dirname(.repo)
#   source(file.path(.repo, "pfn_config.R"))
#   cfg <- load_config(Sys.getenv("PFN_CONFIG", file.path(.repo, "CONFIG.txt")))

load_config <- function(path) {
  cfg <- list()
  for (line in trimws(readLines(path, warn = FALSE))) {
    if (line == "" || startsWith(line, "#")) next
    key <- trimws(sub("=.*", "", line))
    value <- gsub('^"|"$', "", trimws(sub("^[^=]*=", "", line)))
    for (ref in regmatches(value, gregexpr("\\$\\{[A-Za-z0-9_]+\\}", value))[[1]]) {
      name <- substr(ref, 3, nchar(ref) - 1)
      replacement <- if (!is.null(cfg[[name]])) cfg[[name]] else Sys.getenv(name, NA)
      if (is.na(replacement)) stop("${", name, "} is used before it is set in ", path)
      value <- gsub(ref, replacement, value, fixed = TRUE)
    }
    cfg[[key]] <- value
  }
  structure(cfg, class = "pfn_config", path = path)
}

`[[.pfn_config` <- function(x, name) {
  value <- unclass(x)[[name]]
  if (is.null(value)) stop(name, " is not set in ", attr(x, "path"))
  value
}

`$.pfn_config` <- function(x, name) x[[name]]
