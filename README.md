# top_test
Test for Top Agency

## Prototype v1.0

MySQL 8+
jQuery 3+
HTML5
CSS
Flask

This is the first prototype of contact managment system as a test for TOP AGENCY, this needs more work in some areas.

- No session is working or login system, may need a session and redis option for cookie persistance
- Validation on forms, it needs enforcement on some not null fields that return error on SQL query
- Error handling on every step, some queries return error on SQL validation like mail uniqueness
- Universal filtering and search engine, right now filter are based on views, but work on pandas-jinja2 filtering may return better results
- Style uplifting and more interactivity may be necessary
- Better SQL constraints, right now I erased the some of the referencing on database for test purposes, mainly because every deletion returned an error on index reference

## API v1.0

Flask

It needs key input to work, api key example is delivered inside API/api.py

- It does MySQL queries, in every case, elements vary in every request kind
- Table input is needed in some cases, please refer to api.py 
- GET | elems: column elements, table: table reference
- POST | elems: value reference, table: table reference, vals: the values to add
- PATCH | table: table reference, elem: element to patch, val: value to change, id: id of the element
- DELETE | table: table reference, id: id of the element
