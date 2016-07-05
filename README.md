# OneLog
---
![Build Status](https://travis-ci.org/ghmeier/one-log.svg?branch=master)

## Overview
OneLog is a python class for simple, consistent logging throughout your application.

#### The Problem
Using default logging in python, your logg code can look like this:
```python
def foo():
    log.info({'msg': 'Starting f0oo',
              'path': 'mypackage',
              'method': 'foo',
              'state': 'begin',
              'name': user.name,
              'foos-done': user.foos_done,
              'user_id': user.id})
    try:
        // do something
        log.info({'msg': 'ended f0oo',
                  'path': 'mypackage',
                  'method': 'foo',
                  'state': 'SUCCESS',
                  'user_name': user.name,
                  'foos': user.foos_done,
                  'user_id': user.id})
    except Exception as e:
        log.info({'msg': 'failed at f0oo',
                  'path': 'mypackage',
                  'method': 'foo',
                  'state': 'fail',
                  'data': {
                      'name': user.name,
                      'foos-done': user.foos_done,
                      'user_id': user.id},
                  'error': str(e)})
```
What's so wrong with that you might ask?
  1. **Different naming conventions.** The value `user.name` is associated with `name`, `user_name`, and `data.name` throughout that snippet.
  2. **So much copying.** Since we want to avoid naming errors, let's just copy and paste, right? Well, then if we made a typo in the first instance, the last one has the same problem. What if we wanted to change `f0oo` to `foo`?
  3. **Redundancy.** In each one of these logs we have the same five variables repeated three times with similar values. That harms the readability of the function because we have to skip over 6 lines of logging each time we want to get to the acutal logic.
  4. **THE BIG ONE, Searchability.** Logs are most useful when you can search them to find the state of your application when something goes wrong. If we're encouraged to log less data because it takes up fewer lines and is less error prone, then we might not have enough information when the app DOES crash to debug the problem quickly.

####OneLog's Solution
Simple, concise logging, so you can log what you want, when you want:
```python
import one_log as OL
def foo():
  log_data = OL.get_log_data('mypackage', 'foo',
                             {'name': user.name,
                              'foos-done': user.foos_done,
                              'user_id': user.id})
  OL.info(log_data)
  try:
      //do something
      OL.info(succeed(log_data, {'state_msg': 'foo succeeded'})
  except Exception as e:
      OL.exception(fail(log_data, {'state_msg': 'foo failed',
                                   'error': str(e)}))
```
Logging the same info as in the problem example, we copy less, maintain consistent naming conventions, and save space. 

## Documentation
OneLog only has a few functions to worry about:

  * `get_log_data(path, method, data)`: Creates a LogData object with path, method, and state (as 'START') values as well as any extra data you pass in.
  * `update(log_data, data)`: updates or adds the data you provide to the given LogData instance.
  * `succeed(log_data, data)`: same function as update, but sets the state of log_data to 'SUCCESS'.
  * `fail(log_data, data)`: same as update, but sets the state to 'FAILURE'. 
  * `info(log_data)`: logs the LogData to the info stream.
  * `exception(log_data)`: logs the LogData to the exception stream.
  * `error(log_data)`: logs the LogData to the error stream.

OneLog's funcions are designed to mutate a single LogData object throughout the scope of a function, so each function returns the same LogData instance as was passed into it with the updates made. This means that you could do something like:
```python
OneLog.info(OneLog.fail(OneLog.get_log_data('mymodule', 'foo'), {'error': 'ERROR 500'}))
```
Just as well as this:
```python
log_data = OneLog.get_log_data('mymodule', 'foo')
OneLog.fail(log_data, {'error': 'ERROR 500'})
OneLog.info(log_data)
```

##Contribution
---
Feel free to comment, issue, fork, etc. this as you'd like. I'm happy to work to make this a more configurable library for multiple uses in the future.
