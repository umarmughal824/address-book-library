# Create your views here.
from django.shortcuts import render
from django.core.serializers import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from address_book.models import *
from address_book.serializers import *


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def person_list(request):
    """
    List all code persons, or create a new person.
    """
    if request.method == 'GET':
        persons = Persons.objects.all()
        serializer = PersonsSerializer(persons, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        # data = JSONParser().parse(request)
        data = request.POST.copy()
        # check for presence of email_address, street_address, phone_number
        # give group_id
        try:
            if (data['group0']):
                group = Groups.objects.get(id=int(data['group0']))
                try:
                    if (data['phone_no0'] and data['country_code0']):
                        try:
                            Person_Phone_Numbers.objects.get(country_code=data['country_code0'],
                                                             phone_no=data['phone_no0'])
                            return JSONResponse({'error': 'you phone no already found in the system'}, status=400)
                        except:
                            pass
                except:
                    return JSONResponse({'error': 'no phone no found'}, status=400)

                try:
                    if (data['email0']):
                        try:
                            Person_Email_Addresses.objects.get(email=data['email0'])
                            return JSONResponse({'error': 'you email already found in the system'}, status=400)
                        except:
                            pass
                except:
                    return JSONResponse({'error': 'no email found'}, status=400)

                try:
                    if (data['country0'] and data['city0'] and data['state0'] and data['area0']):
                        pass
                except:
                    return JSONResponse({'error': 'no street address found'}, status=400)

                serializer = PersonsSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()

                    # person = serializer.ModelField(model_field=Persons())
                    # person = serializer.ReadOnlyField()
                    # id = serializer.ModelField(model_field=Persons()._meta.get_field('id'))
                    # id = serializer.ReadOnlyField()
                    person = Persons.objects.latest('id')

                    # add person to a group as a member
                    # data1 = {'person': person, 'group':group , 'created':'nn'}

                    i = 0
                    while (True):
                        try:
                            # data1 ={'person': person, 'phone_no': data['phone_no'+str(i)], 'country_code': data['country_code'+str(i)]}
                            if (i > 0):
                                try:
                                    Groups.objects.get(person_id=person.id, group_id=data['group' + str(i)])
                                    continue
                                except:
                                    pass
                            member = Members()
                            member.group = Groups.objects.get(id=data['group' + str(i)])
                            member.person = person
                            member.save()
                        except:
                            break
                        i = i + 1

                    # one or more phone_no
                    i = 0
                    while (True):
                        try:
                            # data1 ={'person': person, 'phone_no': data['phone_no'+str(i)], 'country_code': data['country_code'+str(i)]}
                            if (i > 0):
                                try:
                                    Person_Phone_Numbers.objects.get(country_code=data['country_code' + str(i)],
                                                                     phone_no=data['phone_no' + str(i)])
                                    continue
                                except:
                                    pass
                            ppn = Person_Phone_Numbers()
                            ppn.person = person
                            ppn.country_code = data['country_code' + str(i)]
                            ppn.phone_no = data['phone_no' + str(i)]
                            ppn.save()
                        except:
                            break
                        i = i + 1

                    # one or more email addresses
                    i = 0
                    while (True):
                        try:
                            # data1 ={'person': person, 'phone_no': data['phone_no'+str(i)], 'country_code': data['country_code'+str(i)]}
                            if (i > 0):
                                try:
                                    Person_Email_Addresses.objects.get(email=data['email' + str(i)])
                                    continue
                                except:
                                    pass
                            pea = Person_Email_Addresses()
                            pea.person = person
                            pea.email = data['email' + str(i)]
                            pea.save()
                        except:
                            break
                        i = i + 1

                    # one or more street addresses
                    i = 0
                    while (True):
                        try:
                            # data1 ={'person': person, 'phone_no': data['phone_no'+str(i)], 'country_code': data['country_code'+str(i)]}
                            try:
                                sa = Street_Addresses.objects.get(country=data['country' + str(i)],
                                                                  state=data['state' + str(i)],
                                                                  city=data['city' + str(i)])
                            except Street_Addresses.DoesNotExist:
                                sa = Street_Addresses()
                                sa.country = data['country' + str(i)]
                                sa.state = data['state' + str(i)]
                                sa.city = data['city' + str(i)]
                                sa.save()
                            psa = Person_Street_Addresses()
                            psa.person = person
                            psa.street_address = sa
                            psa.area = data['area' + str(i)]
                            psa.save()
                        except:
                            break
                        i = i + 1
                    return JSONResponse(serializer.data, status=201)
                else:
                    return JSONResponse(serializer.errors, status=400)
        except:
            return JSONResponse({'error': 'no group found'}, status=400)


@csrf_exempt
def person_detail(request, id):
    """
    Retrieve, update or delete a code person.
    """
    try:
        person = Persons.objects.get(id=id)
    except Persons.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PersonsSerializer(person)
        data = serializer.data.copy()
        mems = Members.objects.filter(person_id=person.id)

        emails = Person_Email_Addresses.objects.filter(person_id=person.id)
        i = 0
        for email in emails:
            data['email' + str(i)] = email.email

        cells = Person_Phone_Numbers.objects.filter(person_id=person.id)
        for cell in cells:
            data['cell#' + str(i)] = cell.country_code + cell.phone_no

        # categry_fields_list = Fieldset.objects.select_related('fieldset_label', 'field').filter(
        #     fieldset_label__label=request.session.get('fieldset_label')).values('field_id')
        addrs = Person_Street_Addresses.objects.filter(person_id=person.id)
        for addr in addrs:
            data['address#' + str(
                i)] = addr.area + ', ' + addr.street_address.city + ', ' + addr.street_address.state + ', ' + addr.street_address.country

        i = 0
        for email in emails:
            data['email#' + str(i)] = email.email

        i = 0
        groups = []
        for mem in mems:
            group = {}
            group["group" + str(i) + "_id"] = mem.group_id
            group["group" + str(i) + "_name"] = Groups.objects.get(id=mem.group_id).name

            groups.append(group)
            i = i + 1
        data['Members'] = groups

        return JSONResponse(data)

    elif request.method == 'PUT':
        body = request.body
        datalist = body.split('&')
        data = {}
        for litem in datalist:
            item = litem.split('=')
            data[item[0]] = item[1]

        serializer = PersonsSerializer(person, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        person.delete()
        return HttpResponse(status=204)


@csrf_exempt
def group_list(request):
    """
    List all code persons, or create a new group.
    """
    if request.method == 'GET':
        groups = Groups.objects.all()
        serializer = GroupsSerializer(groups, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        # data = JSONParser().parse(request)
        data = request.POST.copy()
        # data = json.loads(request.body)
        # data = json.loads(request)
        # data = request.body
        serializer = GroupsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def group_detail(request, id):
    """
    Retrieve, update or delete a code person.
    """
    try:
        group = Groups.objects.get(id=id)
    except Groups.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = GroupsSerializer(group)
        data = serializer.data.copy()
        mems = Members.objects.filter(group_id=group.id)
        members = []
        for mem in mems:
            member= {}
            member['person_id']=mem.person.id
            member['first_name']=mem.person.first_name
            member['last_name']=mem.person.last_name
            members.append(member)

        data['Members'] = members


        return JSONResponse(data)

    elif request.method == 'PUT':
        body = request.body
        datalist = body.split('&')
        data = {}
        for litem in datalist:
            item = litem.split('=')
            data[item[0]] = item[1]

        serializer = GroupsSerializer(group, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        group.delete()
        return HttpResponse(status=204)

@csrf_exempt
def person_find(request, first_name, last_name):
    try:
        persons = Persons.objects.filter(first_name__icontains=first_name, last_name__icontains=last_name)
    except Persons.DoesNotExist:
        return HttpResponse('Such name does not exits',status=404)

    data = {}
    personss = []
    if request.method == 'GET':
        i = 0
        for person in persons:
            serializer = PersonsSerializer(person)
            pers = serializer.data.copy()
            personss.append(pers)
            i = i+1

        data['Persons'] = personss
        return JSONResponse(data)
    else:
        return JSONResponse(status=400)

@csrf_exempt
def person_find1(request, first_name):
    try:
        persons = Persons.objects.filter(first_name__icontains=first_name)
    except Persons.DoesNotExist:
        return HttpResponse('Such name does not exits',status=404)

    data = {}
    personss = []
    if request.method == 'GET':
        i = 0
        for person in persons:
            serializer = PersonsSerializer(person)
            pers = serializer.data.copy()
            personss.append(pers)
            i = i+1

        data['Persons'] = personss
        return JSONResponse(data)
    else:
        return JSONResponse(status=400)

@csrf_exempt
def person_find2(request, last_name):
    try:
        persons = Persons.objects.filter(last_name__icontains=last_name)
    except Persons.DoesNotExist:
        return HttpResponse('Such name does not exits',status=404)

    data = {}
    personss = []
    if request.method == 'GET':
        i = 0
        for person in persons:
            serializer = PersonsSerializer(person)
            pers = serializer.data.copy()
            personss.append(pers)
            i = i+1

        data['Persons'] = personss
        return JSONResponse(data)
    else:
        return JSONResponse(status=400)

@csrf_exempt
def person_find3(request, email):
    try:
        emails = Person_Email_Addresses.objects.filter(email__icontains=email)
    except Persons.DoesNotExist:
        return HttpResponse('Such name does not exits',status=404)

    data = {}
    personss = []
    if request.method == 'GET':
        i = 0
        for email in emails:
            serializer = Person_Email_AddressesSerializer(email)
            pers = {}
            person = Persons.objects.get(id=email.person_id)
            pers['id']=person.id
            pers['first_name']=person.first_name
            pers['last_name']=person.last_name
            pers['email']=email.email
            personss.append(pers)
            i = i+1

        data['Persons'] = personss
        return JSONResponse(data)
    else:
        return JSONResponse(status=400)
