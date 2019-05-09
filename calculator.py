
"""
For your homework this week, you'll be creating a wsgi application of
your own.
You'll create an online calculator that can perform several operations.
You'll need to support:
  * Addition
  * Subtractions
  * Multiplication
  * Division
Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.
Consider the following URL/Response body pairs as tests:
```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```
To submit your homework:
  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!
"""

def homepage():
    """ Returns the html format for the landing page"""
    page = '''
<!DOCTYPE html>
<html>
<body>
<h1 align="center">WSGI Calculator App</h1>
<br><br>
<h4 align="center">Landing page for the WSGI Calculator App. Here you will find
instructions for how to use the app.</h4>
<h3>Instructions for use:</h3>
<p>
<ul>
<li>Enter the general URL 'http://localhost:8080/' (this will bring you to this landing page if you do nothing else)
<li>The app has four use options of 'add', subtract', 'multiply', or 'divide'; one of these options must be placed at the end of the general URL to direct the app to its function.
<li>Place your function selection on the end of the URL: 'http://localhost:8080/add' for example.
<li>Each of the four functions needs two integer arguments to be passed in for the function to evaluate (and each argument is separated by a '/').
<li>The final URL should look like this 'http://localhost:8080/add/3/7/' which will yield a result of '10'
</ul>
</body>
</html>
'''
    return page


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    x,y = args[0], args[1]
    add = int(x + y)
    # test output
    print("{} + {} = {}".format(x, y, add))
    # format as str()
    string_sum = str(add)
    # test format
    print("Sum: {}".format(string_sum))
    return string_sum

def subtract(*args):
    """ Returns a STRING with the difference of the arguments """
    x,y = args[0], args[1]
    diff = int(x - y)
    print("{} - {} = {}".format(x, y, diff))
    string_diff = str(diff)
    print("Difference: {}".format(string_diff))
    return string_diff

def multiply(*args):
    """ Returns a STRING with the product of the arguments """
    x,y = args[0], args[1]
    prod = int(x * y)
    print("{} * {} = {}".format(x, y, prod))
    string_prod = str(prod)
    print("Product: {}".format(string_prod))
    return string_prod

def divide(*args):
    """ Returns a STRING with the quotient of the arguments """
    x,y = args[0], args[1]
    if y <= 0:
        raise ZeroDivisionError
        string_quot = "ZeroDivisionError:  Cannot divide a number by 0!"
    else:
        quotient = int(x / y)
        print("{} / {} = {}".format(x, y, quotient))
        string_quot = str(quotient)
        print("Quotient: {}".format(string_quot))
        return string_quot

def resolve_path(path):
    funcs = {
        "": homepage,
        "homepage": homepage,
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide,
    }
    
    path = path.strip("/").split("/")
    args = path[1:]
    args = [int(arg) for arg in args]
    func_name = path[0]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get("PATH_INFO", None)
        print("path {}".format(path))
        if path is None:
            print("None")
            status = "404 Error"
            raise NameError
        
        elif path == "/":
            print("Redirecting to homepage...")

        status = "200 OK"
        func, args = resolve_path(path)
        body = func(*args)

    except NameError:
        status = "404 Not Found"
        body = "<h1>404 - Path or Args(s) Not Found</h1> \
        <br><h4 align='center'>Re-check the URL's path and/or arguments for errors<h4>\
        <br>\
        <br><h4 align='center'>If problems persist see: <a href='https://en.wikipedia.org/wiki/HTTP_404'>https://en.wikipedia.org/wiki/HTTP_404</a></h4>"

    except ZeroDivisionError:
        print("ZeroDivisionError")
        status = "ZeroDivisionError"
        body = "<h1>Fatal Error - Attempt to divide by zero</h1> \
        <br><h4 align='center'>The last integer in your args cannot be zero!<h4>"

    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>500 - Internal Server Error</h1> \
        <br><h4 align='center'>Re-check the URL's path and/or arguments for errors<h4>\
        <br>\
        <br><h4 align='center'>If problems persist see: <a href='https://www.lifewire.com/500-internal-server-error-explained-2622938'>lifewire.com</a></h4>"

    finally:
        headers.append(("Content-length", str(len(str(body)))))
        start_response(status, headers)

        return [str(body).encode("utf8")]



if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    srv = make_server("localhost", 8080, application)
    srv.serve_forever()