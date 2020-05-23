#!/usr/bin/python
#*- coding: utf-8 -*-

try:
	import lxml.html
	import requests
	import urllib
	import re
	from selenium import webdriver
	import time
	from os import system

	gflag = True

	while gflag:
		flag = True

		while True:
			system('cls')
			print('\r\n\r\n\r\n')
			print('         _   _   _   _   _   _   _     _   _     _   _   _   _   _   _  ')
			print('        / \ / \ / \ / \ / \ / \ / \   / \ / \   / \ / \ / \ / \ / \ / \ ')
			print('       ( v | k | s | p | i | e | r ) ( b | y ) ( N | i | k | i | t | a )')
			print('        \_/ \_/ \_/ \_/ \_/ \_/ \_/   \_/ \_/   \_/ \_/ \_/ \_/ \_/ \_/ ')
			print('                             _   _   _   _   _   _  ')
			print('                            / \ / \ / \ / \ / \ / \ ')
			print('                           ( K | l | i | m | o | v )')
			print('                            \_/ \_/ \_/ \_/ \_/ \_/ ')


			print('                         ─╔╗──────────')
			print('                         ╔╝║╔═╗╔══╗╔═╗')
			print('                         ║╬║║╩╣║║║║║╬║')
			print('                         ╚═╝╚═╝╚╩╩╝╚═╝')
			print('\r\n\r\n\r\n\r\n\r\n')

			print('1. Запустить парсер')
			print('2. Задать логин и пароль')
			print('3. Выход')

			menu = input('Выберите действие: ')

			if menu == '1':
				break
			elif menu == '2':
				st = open('settings.cfg', 'w+')
				login = input('Введите логин: ')
				password = input('Введите пароль: ')
				while True:
					try:
						interval = int(input('Задайте интервал(рекомендуемый 2): '))
					except TypeError:
						print('[-] Значение должно быть числом!')
						continue
					except ValueError:
						print('[-] Значение должно быть целым числом!')
						continue
					break
				st.write(login+'***')
				st.write(password+'***')
				st.write(str(interval))
				st.close()
				continue
			elif menu == '3':
				flag = False
				gflag = False
				break
			else:
				print('Неверный ввод!')
				continue
			
		url = 'https://vk.com'


		if flag:
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				'Accept-Language':'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
				'Accept-Encoding':'gzip, deflate',
				'Connection':'keep-alive',
				'DNT':'1'
			}
			session = requests.session()
			data = session.get(url, headers=headers)
			page = lxml.html.fromstring(data.content)
			  
			form = page.forms[0]

			s = open('settings.cfg','r')
			st = s.read()
			sts = st.split('***')

			form.fields['email'] = str(sts[0])
			form.fields['pass'] = str(sts[1])
			  
			response = session.post(form.action, data=form.form_values())
			print('onLoginDone' in response.text)
			if ('onLoginDone' in response.text) == True:
				text = input("Введите запрос: ")

				request = 'https://vk.com/groups?act=catalog&c%5Bper_page%5D=40&c%5Bq%5D='+text+'&c%5Bsection%5D=communities'

				driver = webdriver.Firefox(executable_path='./geckodriver.exe')

				link = driver.get(request)

				time.sleep(4)

				b_login = driver.find_element_by_id('email')
				p_pass  = driver.find_element_by_id('pass')
				l_btn = driver.find_element_by_id('login_button')

				b_login.send_keys(str(sts[0]))
				p_pass.send_keys(str(sts[1]))
				l_btn.click()

				print('[!] Залогиньтесь в VK через браузер и прокрутите ленту в самый низ. \r\n')
				waiting = input("Готовы? Начинаем? Когда будете готовы, нажмите Enter.")

				source = driver.page_source
				find = re.findall(r'(?<=\bclass="labeled title"><a href=")[^"\?]+', source)
				system('cls')
				for k in range(len(find)):
					link = session.get(url+find[k])
					print('[*] Просмотр группы('+url+find[k]+')['+str(k+1)+' из '+str(len(find))+']...')
					time.sleep(int(sts[2]))
					txt = re.findall(r'(\<span class\="new_post_placeholder"\>Написать сообщение\<\/span\>)', str(link.text))
					if txt:
						print('[+] Открытая стена:'+url+find[k])
						f = open('results.'+text+'.txt', 'a')
						f.write(url+find[k]+'\r\n')
						f.close()
				flag = False
				s.close()
				print('[*] Спасибо за использование скрипта! :)')
				input("Press Enter to continue...")
			else:
				print('[-] Неверные данные конфигурации!')
				input("Press Enter to continue...")
		else:
			system('cls')
			print('[*] Спасибо за использование скрипта! :)')
			input("Press Enter to continue...")
			break
except KeyboardInterrupt:
	print('[!] Процесс прерван пользователем')
except Exception as e:
	print('[!] Ошибка: %s' % str(e))
