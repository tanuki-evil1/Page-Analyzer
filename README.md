### Hexlet tests and linter status:
[![Actions Status](https://github.com/tanuki-evil1/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/tanuki-evil1/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/c5fed685d52fa7f5cd7e/maintainability)](https://codeclimate.com/github/tanuki-evil1/python-project-83/maintainability)
# Page Analyzer

Page Analyzer is a Flask web application that allows users to analyze web pages for SEO effectiveness. The application checks the availability of websites and analyzes elements such as headers, descriptions, and H1 tags.

## Features

- URL availability check.
- Analysis of title and description tags.
- Display of check results on the user interface.

## Demo

You can view the application in action at this link:
[Page Analyzer Demo](https://python-project-83-dsjd.onrender.com)

## Stack

- Python, Flask, PostgreSQL, HTML/CSS, Bootstrap3, Poetry

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Ensure you have Python, Poetry, and PostgreSQL installed.

### Installation and Running

Use the `Makefile` to simplify the installation and startup process:

```bash
git clone https://github.com/tanuki-evil1/Page-Analyzer.git
cd Page-Analyzer

## Configuration
Before running the application, you need to set up your environment variables. Duplicate the `.env.example` file and rename it to `.env`. Then, modify it with your actual data for the following variables:
- `SECRET_KEY`: a secret key for your application.
- `DATABASE_URL`: the connection string for your PostgreSQL database, formatted as `postgresql://username:password@localhost:5432/database_name`.

# Install dependencies
make install

# Run the local development server
make dev

# Run the production server
make start
```

### Testing

To run tests, use the following command:

```bash
make lint  # Code linting
```
