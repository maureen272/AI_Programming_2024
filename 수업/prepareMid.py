def get_asian_countries(file_path):
    lst = []
    with open(file_path, 'r') as infile:
        for line in infile:
            word = line.rstrip().split(",")  # .strip()으로 줄바꿈 및 공백 제거
            if len(word) == 3:  # 나라이름, 대륙, 면적이 모두 존재하는지 확인
                country = word[0].strip()
                continent = word[1].strip()
                area = word[2].strip()
                if continent.lower() == "asia":  # 'Asia' 비교를 소문자로 통일
                    lst.append((country, area))  # 튜플로 저장
    return lst

file_path = 'Nations.txt'
asian_countries = get_asian_countries(file_path)

if asian_countries:  # 리스트에 값이 있는지 확인
    for country, area in asian_countries:
        print("Country: {0}, Area: {1}".format(country, area))
else:
    print("No Asian countries found.")
