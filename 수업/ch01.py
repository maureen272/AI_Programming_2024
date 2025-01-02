# ch01. Basics of Python

# Values and Types
# type을 알고싶으면 type() 함수를 사용

# Numbers
# Strings
# Concatenation and Repetition

# String functions and Methods
# function -> fun이름() 꼴 // method -> 변수.메소드이름() 꼴
# eval(): expression을 계산해주는 함수(안에 연산이 들어가야함) // exec(): statement를 실행해주는 함수(단순실행)

# Indices and Slices
''''
print("Python")
print("Python"[1], "Python"[5], 'Python'[2:4])
str1 = 'Hello World!'
print(str1.find('W')) # find()는 index를 리턴
print(str1.find('x')) # 없는 문자를 찾으면 -1을 리턴
print(str1.find('l'))
'
print('Python')
print('Python'[-1], 'Python'[-4], 'Python'[-5:-2])
str1 = 'spam & eggs'
print(str1[-2])
print(str1[-8:-3])
print(str1[0:-1])
'''
# optional print arguments
# format method
'''
age = 20
name = "Kim"
print('Why is {0} playing with that python?'.format(name))
print("{0:^5}{1:<5},{2:>3}".format("Kim", 20, 100))
'''
'''
print('{0:10.2f}'.format(1234.5678))
print('{0:10,.2f}'.format(1234.5678))
print('{0:10,.3f}'.format(1234.5678))
print('{0:10,.2%}'.format(1234.5678))
print('{0:10,.3%}'.format(1234.5678))
print('{0:10,}'.format(12345678))
'''
'''
fullName = input("Enter your full name: ")
n = fullName.rfind(' ')
print("Last name:", fullName[n+1:])
print("First name:", fullName[:n])
'''


print('The area of {0} is {1:,} square miles'.format('Texas', 256984))
print('The population of {0} is {1:,.2%} of the U.S. population'.format('Texas', 6244800000/30900000))
