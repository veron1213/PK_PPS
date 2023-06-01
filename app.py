import pandas as pd
import re
import datetime
from tabulate import tabulate

link_dataset = {
"Информация о местных администрациях внутригородских муниципальных образований Санкт-Петербурга (Версия №15 от 17.03.2021)":
        ["https://classif.gov.spb.ru/irsi/7842140523-informaciya-o-mestnyh-administraciyah-vnutrigorodskih-municipalnyh-obrazovanij-sankt-peterburga/structure_version/218/",
         "dataset/informaciya-o-mestnyh-administraciyah-vnutrigorodskih-municipalnyh-obrazovanij-sankt-peterburga.csv",
         "Телефон"],
"Информация о муниципальных советах внутригородских муниципальных образований Санкт-Петербурга (Версия №14 от 17.03.2021)":
        ["https://classif.gov.spb.ru/irsi/7842140523-informaciya-o-municipalnyh-sovetah-vnutrigorodskih-municipalnyh-obrazovanij-sankt-peterburga/structure_version/220/",
         "dataset/informaciya-o-municipalnyh-sovetah-vnutrigorodskih-municipalnyh-obrazovanij-sankt-peterburga.csv",
         "телефон"],
"Информация о спортивной подготовке детей и молодежи в Санкт-Петербурге (Версия №11 от 02.03.2021)":
        ["https://classif.gov.spb.ru/irsi/7830002078-Informaciya-o-sportivnoj-podgotovke-detej-i-molodezhi-v-Sankt-Peterburge/structure_version/350/?page=3&per_page=50",
         "dataset/Informaciya-o-sportivnoj-podgotovke-detej-i-molodezhi-v-Sankt-Peterburge.csv",
         "Телефон"],
"Перечень государственных учреждений по делам молодежи в Санкт-Петербурге (Версия №11 от 02.03.2021)":
        ["https://classif.gov.spb.ru/irsi/7830002078-Perechen-gosudarstvennyh-uchrezhdenij-po-delam-molodezhi-v-Sankt-Peterburge/structure_version/357/?page=1&per_page=50",
         "dataset/Perechen-gosudarstvennyh-uchrezhdenij-po-delam-molodezhi-v-Sankt-Peterburge.csv",
         "Телефон"],
"Перечень государственных учреждений, подведомственных Комитету по социальной политике Санкт-Петербурга (Версия №11 от 16.03.2021)":
        ["https://classif.gov.spb.ru/irsi/7825675663-perechen-gosudarstvennyh-uchrezhdenij-podvedomstvennyh-Komitetu-po-socialnoj-politike-Sankt-Peterburga/structure_version/171/?page=1&per_page=50",
         "dataset/perechen-gosudarstvennyh-uchrezhdenij-podvedomstvennyh-Komitetu-po-socialnoj-politike-Sankt-Peterburga.csv",
         "Телефон"],
"Перечень государственных учреждений культуры на территории района Санкт-Петербурга (Версия №14 от 12.03.2021)":
        ["https://classif.gov.spb.ru/irsi/7830002078-Perechen-gosudarstvennyh-uchrezhdenij-kultury-na-territorii-rajona-Sankt-Peterburga/structure_version/324/?page=5&per_page=50",
         "dataset/Perechen-gosudarstvennyh-uchrezhdenij-kultury-na-territorii-rajona-Sankt-Peterburga.csv",
         "Телефон"],
"Точки продаж билетов для проезда на наземном городском пассажирском транспорте (Версия №24 от 19.03.2021)":
        ["https://classif.gov.spb.ru/irsi/7830001067-tochki-prodazh-biletov-dlya-proezda-na-nazemnom-gorodskom-passazhirskom-transporte/structure_version/619/?page=1&per_page=50",
         "dataset/tochki-prodazh-biletov-dlya-proezda-na-nazemnom-gorodskom-passazhirskom-transporte.csv",
         "Телефон"],
"Образовательные учреждения в сфере культуры (Версия №11 от 02.03.2021)":
        [
            "https://classif.gov.spb.ru/irsi/7808025993-education/structure_version/342/?page=1&per_page=50",
            "dataset/education.csv",
            "Телефон"],
"Катки и лыжные трассы Санкт-Петербурга (Версия №25 от 08.12.2022)":
        ["https://classif.gov.spb.ru/irsi/7814348015-Katki-i-lyzhnye-trassy-SPbtwo/structure_version/618/?page=5&per_page=50",
         "dataset/Katki-i-lyzhnye-trassy-Sankt-Peterburga.csv",
         "Телефон(ы)"],
"Информация о лечебно-профилактических учреждениях Санкт-Петербурга (Версия №10 от 15.03.2021)":
        ["https://classif.gov.spb.ru/irsi/7808043833-info_health_service/structure_version/327/?page=4&per_page=50",
         "dataset/info_health_service.csv",
         "Телефон"],
"Сведения о судебных участках мировых судей Санкт-Петербурга (Версия №1 от 18.03.2021)":
        ["https://classif.gov.spb.ru/irsi/7842005651-svedeniya-o-sudebnyh-uchastkah-mirovyh-sudej-sankt-peterburga/structure_version/438/?page=5&per_page=50",
         "dataset/svedeniya-o-sudebnyh-uchastkah-mirovyh-sudej-sankt-peterburga.csv",
         "Телефон / факс"],
"Перечень ресурсоснабжающих организаций - владельцев сетей инженерно-технического обеспечения и электрических сетей в Санкт-Петербурге (Версия №10 от 16.03.2021)":
        ["https://classif.gov.spb.ru/irsi/7825363978-perechen-resursosnabzhayushih-organizacij-vladelcev-setej-inzhenerno-tehnicheskogo-obespecheniya-i-elektricheskih-setej-v-sankt-peterburge/structure_version/387/?page=1&per_page=50",
         "dataset/perechen-resursosnabzhayushih-organizacij-vladelcev-setej-inzhenerno-tehnicheskogo-obespecheniya-i-elektricheskih-setej-v-sankt-peterburge.csv",
         "Телефон для справок"],
"Перечень образовательных организаций (школ, гимназий, лицеев) на территории района Санкт-Петербурга (Версия №10 от 02.03.2021)":
        ["https://classif.gov.spb.ru/irsi/7830002078-Perechen-obrazovatelnyh-organizacij/structure_version/361/?page=10&per_page=50",
         "dataset/Perechen-obrazovatelnyh-organizacij-na-territorii-rajona-Sankt-Peterburga.csv",
         "Телефон"],
"Государственные бюджетные образовательные учреждения Санкт-Петербурга, находящиеся в ведении Комитета по образованию (Версия №10 от 02.03.2021)":
        ["https://classif.gov.spb.ru/irsi/7830002053-State_educational_institutions_of_Saint_Petersburg_under_control_of_the_Committee/structure_version/328/?page=1&per_page=50",
         "dataset/Gosudarstvennye-byudzhetnye-obrazovatelnye-uchrezhdeniya-Sankt-Peterburga-nahodyashiesya-v-vedenii-Komiteta-po-obrazovaniyu.csv",
         "Телефон"],
"Информация о кладбищах Санкт-Петербурга, на которых предоставляются участки земли для погребения (Версия №10 от 02.03.2021)":
        ["https://classif.gov.spb.ru/irsi/7838482852-Informaciya-o-kladbishah-Sankt-Peterburga-na-kotoryh-predostavlyayutsya-uchastki-zemli-dlya-pogrebeniya/structure_version/504/?page=2&per_page=50",
         "dataset/Informaciya-o-kladbishah-Sankt-Peterburga-na-kotoryh-predostavlyayutsya-uchastki-zemli-dlya-pogrebeniya.csv",
         "Телефон"],

}

class Analitic_Phone():
    def __init__(self, path: str, colum:str):
        self.path = path
        self.colum = colum

        # Возвращает датафрейм по столбцу телефона
    def read_csv_colum(self):
        col = pd.read_csv(self.path, delimiter=',')
        return col[self.colum]

        # количество записей в наборе
    def count_csv(self):
        count_csv = pd.read_csv(self.path).count()
        return count_csv[0]

    # количество не пустых номеров
    def count_not_null_phone(self):
        cnt=0
        for i in self.read_csv_colum():
            if isinstance(i, str):
                if re.sub(r'\D', "", i) != "":
                    cnt=cnt+1
        return cnt

    #количество городских телефонных номеров
    def count_gor_phone(self):
        count_phone = 0
        for phone in self.read_csv_colum():
            if isinstance(phone, str):
                if re.search(",", phone):
                    phone=phone.split(",")
                elif re.search(";", phone):
                    phone = phone.split(";")
                elif re.search("/", phone):
                    phone = phone.split("/")
                elif re.search("[\s][+]", phone):
                    phone = phone.split("+")
                else:
                    phone=re.sub(r'\D',"",phone)
                if type(phone) is list:
                    for i in phone:
                        i = re.sub(r'\D', "", i)
                        if re.search("^.812", i) or re.search("^812", i) or len(i) == 7:
                            count_phone = count_phone + 1
                            #print(i)
                elif re.search("^.812", phone) or re.search("^812", phone) or len(phone) == 7:
                    count_phone = count_phone + 1
                    #print(phone)
        return count_phone

    # количество мобильных телефонных номеров
    def count_mobile_phone(self):
        count_phone = 0
        for phone in self.read_csv_colum():
            if isinstance(phone, str):
                if re.search(",", phone):
                    phone = phone.split(",")
                elif re.search(";", phone):
                    phone = phone.split(";")
                elif re.search("/", phone):
                    phone = phone.split("/")
                else:
                    phone = re.sub(r'\D', "", phone)
                if type(phone) is list:
                    for i in phone:
                        i = re.sub(r'\D', "", i)
                        if re.search(r"^.9", i) and  len(i) == 11:
                            #print(i)
                            count_phone = count_phone + 1
                elif re.search(r"^.9", phone) and len(phone) == 11:
                    #print(phone)
                    count_phone = count_phone + 1
        return count_phone

    # количество телефонных номеров, с указанием кода страны"" (напр., +7-..., но не 8-...)
    def cont_code_country(self):
        count_phone = 0
        for phone in self.read_csv_colum():
            if isinstance(phone, str):
                cnt=phone.count("+7")
                count_phone = count_phone + cnt
        return count_phone

    # количество телефонных номеров с указанием кода города или кода оператора сотовой связи
    def cont_operator_mobile(self):
        count_phone = 0
        for phone in self.read_csv_colum():
            if isinstance(phone, str):
                if re.search(",", phone):
                    phone = phone.split(",")
                elif re.search(";", phone):
                    phone = phone.split(";")
                elif re.search("/", phone):
                    phone = phone.split("/")
                elif re.search("[\s][+]", phone):
                    phone = phone.split("+")
                else:
                    phone = re.sub(r'\D', "", phone)
                if type(phone) is list:
                    for i in phone:
                        i = re.sub(r'\D', "", i)
                        if re.search("^.812", i)  or re.search("^812", i) or (re.search("^.9[0-9][0-9]", i) and len(i)==11):
                            count_phone = count_phone + 1
                elif re.search("^.812", phone) or re.search("^812", phone) or (re.search("^.9[0-9][0-9]", phone) and len(phone)==11):
                    count_phone = count_phone + 1
        return count_phone

    # количество телефонных номеров, в записи которых используются пробелы
    def space_number(self):
        count_phone = 0
        for phone in self.read_csv_colum():
            if isinstance(phone, str):
                if re.search(",", phone):
                    phone = phone.split(",")
                elif re.search(";", phone):
                    phone = phone.split(";")
                elif re.search("/", phone):
                    phone = phone.split("/")
                elif re.search("[\s][+]", phone):
                    phone = phone.split("+")
                if type(phone) is list:
                    for i in phone:
                        i = i.strip()
                        i = re.sub("^[А-Яа-я]+([\W]+)?[\s]", "", i)

                        if re.search(" ", i):
                            count_phone = count_phone + 1
                else:
                    phone = re.sub("^[А-Яа-я]+([\W]+)?[\s]", "", phone)
                    if re.search(" ", phone):
                        count_phone = count_phone + 1
        return count_phone

    # количество телефонных номеров, в записи которых используются скобки
    def scop_number(self):
        count_phone = 0
        for phone in self.read_csv_colum():
            if isinstance(phone, str):
                if re.search(",", phone):
                    phone = phone.split(",")
                elif re.search(";", phone):
                    phone = phone.split(";")
                elif re.search("/", phone):
                    phone = phone.split("/")
                elif re.search("[\s][+]", phone):
                    phone = phone.split("+")
                if type(phone) is list:
                    for i in phone:
                        i = i.strip()
                        if re.search("[()]", i):
                            count_phone = count_phone + 1
                elif re.search("[()]", phone):
                    count_phone = count_phone + 1
        return count_phone

    # количество телефонных номеров, в записи которых используются дефисы
    def dash_number(self):
        count_phone = 0
        for phone in self.read_csv_colum():
            if isinstance(phone, str):
                if re.search(",", phone):
                    phone = phone.split(",")
                elif re.search(";", phone):
                    phone = phone.split(";")
                elif re.search("/", phone):
                    phone = phone.split("/")
                elif re.search("[\s][+]", phone):
                    phone = phone.split("+")
                if type(phone) is list:
                    for i in phone:
                        i = i.strip()
                        if re.search("[-]", i):
                            #print(i)
                            count_phone = count_phone + 1
                elif re.search("[-]", phone):
                   # print(phone)
                    count_phone = count_phone + 1
        return count_phone

    def view_table(self, namedataset, linkdataset ):
        newdata = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        data = [{'Название набора данных': namedataset, 'Ссылка на набор данных': linkdataset, 'Количество записей в наборе': self.count_csv(),
                 "Название столбца с телефонным номером":self.colum, 'Количество не пустых телефонных номеров':self.count_not_null_phone(),
                 'Количество городских телефонных номеров':self.count_gor_phone(),'Количество мобильных телефонных номеров':self.count_mobile_phone(),
                 'Количество телефонных номеров, с указанием кода страны':self.cont_code_country(),'Количество телефонных номеров с указанием кода города или кода оператора сотовой связи':self.cont_operator_mobile(),
                 'Количество телефонных номеров, в записи которых используются пробелы':self.space_number(), 'Количество телефонных номеров, в записи которых используются скобки':self.scop_number(),
                 'Количество телефонных номеров, в записи которых используются дефисы':self.dash_number(),
                 }]
        view = pd.DataFrame(data)
        view.to_csv(f"{namedataset}_{newdata}.csv", index=False)
        print(tabulate(view, headers=view.keys(), tablefmt="grid", showindex="always"))







if __name__=="__main__":
    for name, link in link_dataset.items():
        dt = Analitic_Phone(link[1], link[2], )
        dt.view_table(name, link[0])
