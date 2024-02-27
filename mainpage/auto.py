import os
import random
import tempfile
from os.path import exists

from faker import Faker

from mainpage.models import Article, Tag
from users.models import Userc, compress
from users.models import Region
from django.core.files import  File
from city_country.models import Country, City



class Snippet:
    def __init__(self):
        pass
    def register_with_email_verification(self, data_u):
        # register the new user
        user = Userc.objects.create(email = data_u.get('user_data').get('email'),
                             username =data_u.get('user_data').get('username'),
                             password = data_u.get('user_data').get('password'),
                             region = data_u.get('user_data').get('region'),
                             city = data_u.get('user_data').get('city'),
                             is_active =True
                             )

        return user

    def create_full_user(self, data_u):
        fake = Faker(['ru_RU',])
        i = random.randint(1, 348)

        user = Snippet.register_with_email_verification(self, data_u)
        id = user.id
        data_u['user_data'].update({
            "first_name": fake.name().split(" ")[0],
            "bio": fake.text(),
        })
        user.first_name = data_u.get('user_data').get('first_name')
        user.bio = data_u.get('user_data').get('bio')
        file_name = str(i)+'.jpg'
        EXT_FILE_PATH = 'images/avs/'
        lf = self.tmpf(file_name,EXT_FILE_PATH)
        user.profile_img = lf.name
        user.save()
        os.remove(lf.name)

        return id

    def auto_user(self):
        fake = Faker(['ru_RU', ])
        country = fake.country()
        # creating countries
        i = random.randint(1, 363)
        file_name = str(i)+'.jpg'
        EXT_FILE_PATH = 'images/country/'
        lf = self.tmpf(file_name,EXT_FILE_PATH)
        country_id = Country.objects.create(title=country,
                                            content=fake.text(),
                                            img=lf.name
                                            ).id
        for j in range(20):
            country = fake.country()
            while Country.objects.filter(title=country).exists():
                country = fake.country()
            i = random.randint(1, 363)
            file_name = str(i) + '.jpg'
            EXT_FILE_PATH = 'images/country/'
            lf = self.tmpf(file_name, EXT_FILE_PATH)
            country = Country.objects.create(title=country,
                                             content=fake.text(),
                                             img=lf.name
                                             )
        # creating cities
        city = fake.city()
        i = random.randint(1, 363)
        file_name = str(i)+'.jpg'
        EXT_FILE_PATH = 'images/country/'
        lf = self.tmpf(file_name,EXT_FILE_PATH)
        city_id = City.objects.create(title=city,
                                      content=fake.text(),
                                      img=lf.name,
                                      country=Country.objects.get(id=random.randint(country_id, country_id + 19))
                                      ).id
        for j in range(100):
            city = fake.city()
            while City.objects.filter(title=city).exists():
                city = fake.city()
            i = random.randint(1, 363)
            file_name = str(i) + '.jpg'
            EXT_FILE_PATH = 'images/country/'
            lf = self.tmpf(file_name, EXT_FILE_PATH)
            City.objects.create(title=city,
                                content=fake.text(),
                                img=lf.name,
                                country=Country.objects.get(id=random.randint(country_id, country_id + 19))
                                )
        # creating regions
        regions = ["Европа", "Азия", "Океания", "Америка", "Африка", "Австаралия"]
        i = random.randint(1, 399)
        file_name = str(i)+'.jpg'
        EXT_FILE_PATH = 'images/region/'
        lf = self.tmpf(file_name,EXT_FILE_PATH)
        region_id = Region.objects.create(title='Холодные зоны',
                                          background_img=lf.name,
                                          logo_outline=lf.name).id
        for j in range(6):
            region = regions[j]
            i = random.randint(1, 399)
            file_name = str(i) + '.jpg'
            EXT_FILE_PATH = 'images/region/'
            lf = self.tmpf(file_name, EXT_FILE_PATH)
            Region.objects.create(title=region,
                                  background_img=lf.name,
                                  logo_outline=lf.name)
        Faker.seed(0)
        # creating users
        id = 0
        for j in range(50):
            username = fake.simple_profile()['username']
            email = fake.email()
            password = fake.password()
            fake_data = {
                'user_data': {
                    "email": email,
                    "username": username,
                    "password": password,
                    "region": Region.objects.get(id=random.randint(region_id, region_id + 5)),
                    "city": City.objects.get(id=random.randint(city_id, city_id + 100)),
                },
                'login_data': {
                    "email": email,
                    "password": password
                }, }
            id = Snippet.create_full_user(self,fake_data)
        Faker.seed(0)
        i = random.randint(1, 399)
        tags_names= ["Пляж","Горы","Пустыни","Комфорт","Холод","Жара","Дорого","Дёшево","Экзотично","Острова","Опасно","Безопасно"]
        tag_id = Tag.objects.create(name="Казино").id
        for j in tags_names:
            Tag.objects.create(name=j)
        text = fake.text();
        for j in range(10):
            text+=fake.text()
        for ii in range(100):
            for j in range(10):
                text += fake.text()
            i = random.randint(1, 363)
            file_name = str(i) + '.jpg'
            EXT_FILE_PATH = 'images/country/'
            lf = self.tmpf(file_name, EXT_FILE_PATH)
            post = Article.objects.create(title=fake.text()[:100],
                                   description=fake.text()[:200],
                                   content=text,
                                   author_id=random.randint(id-49, id),
                                    img =lf.name
                                   )
            count = random.randint(0, 10)
            for k in range(count):
                post.city.add(City.objects.get(id=random.randint(city_id, city_id + 100)))
            count = random.randint(0, 10)
            for k in range(count):
                post.country.add(Country.objects.get(id=random.randint(country_id, country_id + 20)))
            count = random.randint(0, 10)
            for k in range(count):
                post.tags.add(Tag.objects.get(id=random.randint(tag_id, tag_id + 10)))
        users = Userc.objects.all()
        for u in users:
            u.save()
    def tmpf(self, file_name,EXT_FILE_PATH ):
        file_path = EXT_FILE_PATH + file_name
            # create a named temporary file within the project base , here in media
        lf = tempfile.NamedTemporaryFile(dir='media', delete=False, suffix='.jpg')
        f = open(file_path, 'rb')
        lf.write(f.read())
        lf.close()
        return lf

def run():
    s = Snippet()
    s.auto_user()

