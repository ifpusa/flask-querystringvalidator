Query String Synch
==================

This library makes it easy to validate query string inputs to your Flask view functions. It has two components:

1. The query string validator
2. A view function decorator

## Query String Validator

You declare allowed field types for a given view function. If a view function is called without these query string variables included, the request is redirected to the same URL but now includes the default query string variables. This makes it easy for users to see which variables are allowed on each page.

The validator has a pluggable type system with built-in support for Integers, Strings, and Dates.

### Validator Usage

