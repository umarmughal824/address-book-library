Address Book Library 
REST API

Dependencies
Django==1.10.1
djangorestframework==3.4.6

First Install django and django restframework

Download the entire directory with that name AddressLibrary (https://github.com/umarmughal824/address-book-library/tree/master/AddressLibrary)

then run "python manage.py makemigrations"
then after that it will create a migrate which we will migrate it by running the following command
"python manage.py migrate"


Design Only Questions:
Find person by email address (can supply any substring, ie. "comp" should work assuming "alexander@company.com" is an email address in the address book) - discuss how you would implement this without coding the solution.

  I will write the query is sucha a way that column_name__icontains="value". It will read it anywhere in the email with case insensitive string having "value" anywhere in the email.


Note:
You can download the address_book.docx file in order to see it running state which includes all the use cases screenshots in running state.
