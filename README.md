# Docker Image Analysis Research and tools

This repository holds the tools and experiments related to analyzing dockerhub at image filesystem level. It contains the following:

- `dockerhub_crawler`, A python tool that crawls dockerhub to retrieve data about images
- `minimal_libs`, A tiny tool to predict the native packages required by a given python package, based on the data from `dockerhub_crawler`
- `research`, notebooks of data exploration and applied machine learning experiments on the data from `dockerhub_crawler`
