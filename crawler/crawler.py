import requests
from bs4 import BeautifulSoup
import re

database = {}

def crawl(num):
    # 클래스가 증가할 때 마다 hidden body가 나타난다?
    url = f"https://www.purplesto.re/products/sales/{num}"
    data = requests.get(url)
    html = data.text
    soup = BeautifulSoup(html, 'html.parser')

    # 메모이제이션으로 중복 안되게 하기
    if soup.find('p', {'class':'productInfo__name'}):
        titles = soup.find('p', {'class':'productInfo__name'})
        # if titles in ##:
        #   pass
        # else:
        database['title'] = titles.text

    if soup.find('p', {'class':'breadcrumb__btn'}):
        category = soup.find('p', {'class':'breadcrumb__btn'}).getText(separator=u' ') # 고양이 만 나옴
        database['category'] = category

    if soup.find('p', {'class':'breadcrumb__path'}):
        category = soup.find('p', {'class':'breadcrumb__path'}).getText(separator=u' ') # 고양이 만 나옴
        #script = soup.find('script')
        #database['category'] = script
        database['category'] = category

    if soup.select_one('section > div > section.productInfo > div.productInfo__content > div.productInfo__title > span > a'):
        brand = soup.select_one('section > div > section.productInfo > div.productInfo__content > div.productInfo__title > span > a')
        database['brand'] = brand.text

    try:
        detail = soup.find('div', {'class':'productSubInfo__detail-table'}).getText(separator=u' ')
        age = detail.split('연령구분 ')[1].split(' 푸드타입 ')  # 정보 나옴 - 정규식으로 처리 해서 딕셔너리 넣을 수 있을듯
        database['age'] = age[0]
        classification = age[1].split(' 중량 ')
        database['classification'] = classification[0]
        gram = classification[1].split(' 주재료 ')
        database['gram'] = gram[0]
        ingredient = gram[1].split(' 식단정보 ')
        database['ingredient'] = ingredient[0]
        info = ingredient[1].split(' 칼로리 ')
        database['info'] = info[0]
        from_company = info[1].split(' 원산지/제조사 ')
        database['calory'] = from_company[0]
        database['from_company'] = from_company[1]
    except:
        detail = soup.find('div', {'class':'productSubInfo__detail-table'}).getText(separator=u' ')
        database['detail'] = detail

    img = soup.find('img'>'src', {'alt':'상품 이미지'})
    database['img'] = img['src']

    try:
        content = soup.find('div', {'class':'content'})
        database['content'] = content.text
    except:
        pass

    # 성분이 다양해서 이름으로 분리해야할듯한데...
    if soup.find('div', {'class':'registeredIngredient__grid'}):
        registeredIngredient__grid = soup.find('div', {'class':'registeredIngredient__grid'}).getText(separator=u' ')
        database['nutrient'] = registeredIngredient__grid
        if registeredIngredient__grid.startswith('성분등록번호'):
            regi_num = registeredIngredient__grid.split('성분등록번호 ')[1].split(' 조단백 ')  # 정보 나옴 - 정규식으로 처리 해서 딕셔너리 넣을 수 있을듯
            database['성분등록번호'] = regi_num[0]
        if registeredIngredient__grid.startswith('조단백'):
            protein = registeredIngredient__grid.split('조단백 ')[1].split(' 조지방 ')  # 정보 나옴 - 정규식으로 처리 해서 딕셔너리 넣을 수 있을듯
            database['조단백'] = protein[0]      
            #protein = regi_num[1].split(' 조지방 ')
            fat = protein[1].split(' 조섬유 ')
            database['조지방'] = fat[0]
            fiber = fat[1].split(' 조회분 ')
            database['조섬유'] = fiber[0]
            ash = fiber[1].split(' 수분 ')
            database['조회분'] = ash[0]
            database['수분'] = ash[1]
    elif soup.find('div', {'class':'nutritionCheck__grid'}):
        nutritionCheck__grid = soup.find('div', {'class':'nutritionCheck__grid'}).getText(separator=u' ')
        database['nutrient'] = nutritionCheck__grid

    #   if IndexError:
    #       print(f"{num}에서 에러")
    #       pass
    # if AttributeError:
    #     print(f"{num}에서 Attribution 에러")
    # 이걸 바로 클라우드 db에 저장??

    return database