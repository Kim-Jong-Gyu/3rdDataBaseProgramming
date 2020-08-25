from bs4 import BeautifulSoup
import requests
import urllib.request
import re

#get categroy name
def get_cat_li():
    cat_li = []
    response = requests.get('https://apps.apple.com/kr/genre/ios/id36')
    
    soup = BeautifulSoup(response.text, 'html.parser')
    for a in soup.select('a.top-level-genre'):
        cat_li.append(a.get('href'))
    return cat_li

#alpha_list     
alpha_list = ['A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O','P', 'Q','R','S','T','U','V','W','X','Y','Z','*']

#get app link
def move_page(cat_link, alpha):
    link = cat_link+'?letter='+alpha
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    a= None
    for ul in soup.select('ul.list.paginate'):
       a = ul.select('a')
    if a is not None:
        this_ = a[0].get('href')    
        get_app_list(this_) #get app list on this page
        #move to next page
        next_ = get_next_page(this_)
        while next_ != this_:
            get_app_list(next_)
            this_ = next_
            next_ = get_next_page(this_)
    else:
        get_app_list(link)
        
def get_next_page(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    res = soup.select('a.paginate-more')
    if res == []:
        return link
    return res[0].get('href')
    

def get_app_list(link):
    col = ['column.first', 'column', 'column.last']
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    for c in col:
        for div in soup.select('div.'+c + ' > ul > li > a'):
            app = div.get('href')
            get_app_info(app)

def get_app_info(link):
    url= str(link)
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')


    list_P_CR_V = soup.find_all(class_='information-list__item__definition l-column medium-9 large-6')
    Price=0
    content_rating = 0
    Volume=0
    for i in range(len(list_P_CR_V)):
        temp = str(list_P_CR_V[i].get_text().strip())
    #가격 뽑기
        if temp =="":
            pass
        elif temp[0] == '￦':
           Price =  list_P_CR_V[i].get_text().strip()    
        elif temp == '무료':
            Price = '무료'        
    #연령 제한 뽑기    
        elif temp[-1] =='+':
            content_rating = list_P_CR_V[i].get_text().strip()
    ##앱 용량 뽑기    
        elif temp[-2:] == 'MB' or temp[-2:] == 'GB' or temp[-2:]=='KB':
            Volume =  list_P_CR_V[i].get_text().strip()  
    ##별점 뽑기
    rating_before = soup.find_all(class_='we-customer-ratings__averages__display')
    if not rating_before:
        rating = 0
    else:
        rating = rating_before[0].get_text()
    ##리뷰 수 뽑기
    review_before = soup.find_all(class_='we-customer-ratings__count medium-hide')
    if not review_before:
        review = 0
    else:
        review_middle = re.sub('개의 평가','',str(review_before[0].get_text()))
        if review_middle[-1] =='만':
            review =int(float(review_middle[:-1]) * 10000)
        elif review_middle[-1] =='천':
            review = int(float(review_middle[:-1]) * 1000)
        else:
            review = int(review_middle)        
    name_before = soup.find_all(class_='product-header__subtitle app-header__subtitle')
    if not name_before:
        name_before = soup.find_all(class_='product-header__title app-header__title')
        if not name_before:
            name = str('my_error')
        else:
            name = str(name_before[0].get_text().strip())[:-3].strip()
    else:
        name = name_before[0].get_text().strip()
    ##카테고리 값 넣기
    category_before = soup.find_all(class_='link')
    for i in range(len(category_before)):
        if str(category_before[i].get('href'))[8:14]:
            category = str(category_before[i].get_text().strip())
    data = open("/Users/kimjong-gyu/Desktop/DB_DATA/utility/e.txt",'a',encoding='utf-8') #각자 파일 만들어 적기
    data.write(str(name)+'\t'+ str(category) +'\t'+str(rating)+'\t'+str(review)+'\t'+str(Price)+'\t'+str(content_rating)+'\t'+str(Volume)+'\n')
    data.close()
    print(1)
    
    
cat_li = get_cat_li()
move_page(cat_li[25], alpha_list[4])






