from django.http import JsonResponse
from django.shortcuts import render, redirect
from app.models import Member, Record
import datetime
import smtplib
from email.message import EmailMessage


def index(request):
    return render(request, 'app/index.html', {})


def home(request):
    return render(request, 'app/home.html', {})


def query_result(request):
    return render(request, 'app/query_result.html', {})


def record(request):
    if request.method == 'GET':
        return render(request, 'app/record.html', {})
    else:
        result_dict = {}
        member_id = request.session['user_id']
        name = request.POST['name']                 #점검자
        address = request.POST['address']           #건물주소
        buildingname = request.POST['buildingname'] #건물이름
        own = request.POST['own']                   #건물주
        num1 = request.POST['num1']
        num2 = request.POST['num2']
        num3 = request.POST['num3']
        num4 = request.POST['num4']
        num5 = request.POST['num5']
        num6 = request.POST['num6']
        num7 = request.POST['num7']
        num8 = request.POST['num8']
        num9 = request.POST['num9']
        num10 = request.POST['num10']
        if member_id == '' or address == '' or name == '' or buildingname == '' or own == '' or num1 == '' or num2 == '' or num3 == '' or num4 == '' or num5 == '' or num6 == '' or num7 == '' or num8 == '' or num9 == '' or num10 == '':
            result_dict['result'] = '공백은 사용할 수 없습니다.'
            return JsonResponse(result_dict)
        else:
            try:
                record = Record(member_id=member_id, address=address, name=name, buildingname=buildingname, own=own, num1=num1, num2=num2,
                                num3=num3,
                                num4=num4, num5=num5, num6=num6, num7=num7, num8=num8, num9=num9, num10=num10, )
                record.save()
                result_dict['result'] = '등록완료'
            except:
                pass
            return JsonResponse(result_dict)


def register(request):
    if request.method == 'GET':
        return render(request, 'app/register.html', {})
    else:
        result_dict = {}
        user_email = request.POST['user_email']
        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']
        user_name = request.POST['user_name']
        user_confirm_pw = request.POST['user_confirm_pw']
        if user_email == '' or user_id == '' or user_name == '' or user_pw == '' or user_confirm_pw == '':
            result_dict['result'] = '공백은 사용할 수 없습니다.'
            return JsonResponse(result_dict)

        elif user_pw != user_confirm_pw:
            result_dict['result'] = '비밀번호 매치 실패'
            return JsonResponse(result_dict)

        else:
            try:
                Member.objects.get(user_id=user_id)
                result_dict['result'] = '이미 가입된 아이디가 있습니다.'
            except Member.DoesNotExist:
                member = Member(user_id=user_id, user_pw=user_pw, user_email=user_email, user_name=user_name,
                                )
                member.save()
                result_dict['result'] = '가입완료'
            return JsonResponse(result_dict)


def login(request):
    if request.method == 'GET':
        return render(request, 'app/login.html', {})
    else:
        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']
        result_dict = {}
        try:
            Member.objects.get(user_id=user_id, user_pw=user_pw)
            result_dict['result'] = 'success'
            request.session['user_id'] = user_id
        except Member.DoesNotExist:
            result_dict['result'] = 'fail'
        return JsonResponse(result_dict)


def doc(request):
    if request.method == 'GET':
        return render(request, 'app/doc.html', {})
    else:
        try:
            user_id = request.session['user_id']
            print(user_id)
            record = Record.objects.get(member_id=user_id)
            print(record)
            return render(request, 'app/doc.html', {'records': record})
        except Exception as e:
            print(e)
            return redirect('doc')

def query(request):
    return render(request, 'app/query.html', {})

def email(request):
    smtp_gmail = smtplib.SMTP('smtp.gmail.com', 587)

    # 서버 연결을 설정하는 단계
    smtp_gmail.ehlo()
    # 연결을 암호화
    smtp_gmail.starttls()
    # 로그인
    smtp_gmail.login('saidtherapy23@gmail.com', 'erff8653!')
    msg = EmailMessage()
    # 제목 입력
    msg['Subject'] = "소방 관리 시설"
    # 내용 입력
    msg.set_content("점검표가 첨부되어 있습니다.")
    # 보내는 사람
    msg['From'] = 'saidtherapy23@gmail.com'
    # 받는 사람
    email = Member.objects.filter(email='email')
    msg['To'] = ('%s' % email)
    # file = './test.csv'
    # fp = open(file, 'rb')
    # file_data = fp.read()
    # msg.add_attachment(file_data, maintype='text', subtype='plain', filename="test.csv")

    smtp_gmail.send_message(msg)

    return render(request, 'app/email.html', {})


def logout(request):
    try:
        result_dict= {}
        del request.session['user_id']
        del request.session['user_pw']
        result_dict['result'] = '로그아웃 되었습니다.'
        return JsonResponse(result_dict)
    except KeyError:
        pass

    return redirect('login')