import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS


def GetResponse(input):
  genai.configure(api_key=YOUR_API_KEY)

  generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
    "stop_sequences": [
      "input",
    ],
  }

  safety_settings = [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_LOW_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_LOW_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_LOW_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_LOW_AND_ABOVE"
    },
  ]

  model = genai.GenerativeModel(model_name="gemini-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

  prompt_parts = [
    "input: 앞으로 10번씩 10번 가는 코드를 짜줘",
    "output: '''\ndef when_start():\n  for i in range(10):\n    Entry.move_to_direction(10)\n'''\n\n이코드를 사용하면 오브젝트가 앞으로 10번씩 10번 가게 됩니다.",
    "input: 마우스를 따라가는 코드를 짜줘",
    "output: '''\nwhile True:\n  Entry.move_to(\"mouse_pointer\")\n'''\n이 코드를 사용하면 오브젝트가 마우스를 따라 움직입니다",
    "input: 신호를 사용하여 신호를 받으면 안녕이라고 말하는 코드를 짜줘",
    "output: '''\ndef when_start():\n  Entry.send_signal(\"hi\")\n   \ndef when_get_signal(\"hi\"):\n  Entry.print(\"안녕\")\n'''\n이코드를 사용하면 hi라는 신호를 보내고 hi라는 신호를 받으면 \"안녕\"이라고 출력하게 됩니다.",
    "input: 안녕이라고 4초동안 말하는 코드를 짜줘",
    "output: '''\nEntry.print_for_sec(\"안녕\", 4)\n'''\n이코드를 사용하면 안녕이라고 4초동안 말하게 됩니다.",
    "input: 거듭제곱을 하게 하는 코드를 짜줘",
    "output: '''\n수 = 0\n수 = []\n\ndef when_start():\n  Entry.input(\"얼마?\")\n  수 = Entry.answer()\n  Entry.input(\"몇 제곱?\")\n  수.insert(0, (수 ** 2))\n  for i in range((Entry.answer() - 2)):\n    수[0] = (수[0] * 수)\n  Entry.print(수[0])\n'''\n\n이코드는 수를 물어보고 반복문을 이용하여 거듭제곱을 구합니다.",
    "input: 약수를 구하는 코드를 짜줘",
    "output: '''\n번호 = 0\n약수 = []\n\ndef when_start():\n  Entry.input(\"몇?\")\n  번호 = 1\n  for i in range(Entry.answer()): # 여기가 약수 정하기\n    if ((Entry.answer() % 번호) == 0):\n      약수.append(번호)\n    번호 += 1\n'''\n이코드는 반복문을 이용하여 약수를 \"약수\"리스트에 담습니다.",
    "input: 질문에 관한 작품을 만들어줘",
    "output: '''\ndef when_start():\n  Entry.input(\"input\")\n  Entry.print(Entry.answer())\n'''\n이 코드는 input을 유저에게서 받고 input을 출력합니다.",
    "input: 움직임 카테고리에는 어떤 코드가 있어?",
    "output: 움직임 카테고리에는 아래 코드들이 있습니다.\n'''\nEntry.move_to_direction(...)\nEntry.add_x(...)\nEntry.add_y(...)\nEntry.add_xy_for_sec(..., ..., ...)\nEntry.set_x(...)\nEntry.set_y(...)\nEntry.set_xy(..., ...)\nEntry.set_xy_for_sec(..., ..., ...)\nEntry.move_to(\"object name\")\nEntry.move_to_for_sec(\"object name\", ...)\nEntry.add_rotation(...)\nEntry.add_direction(...)\nEntry.add_rotation_for_sec(..., ...)\nEntry.add_direction_for_sec(..., ...)\nEntry.set_rotation(...)\nEntry.set_direction(...)\nEntry.look_at(\"other object name\")\n'''",
    "input: 간단한 주식 코드를 짜줘",
    "output: '''\ndef when_start():\n  while True:\n    Entry.input(\"팔기, 사기\")\n    대답 = Entry.answer()\n    if (대답 == \"사기\"):\n      돈 += (0 - 가격)\n    if (대답 == \"팔기\"):\n      돈 += 가격\ndef when_start():\n  while True:\n    가격 += random.randint(-0.3, 0.3)\n    Entry.wait_for_sec(0.1)\n'''\n이코드는 주식을 간단하게 구현했습니다. 유저의 input으로 결과가 결정됩니다.",
    "input: 시작 카테고리의 코드를 알려줘",
    "output: 다음은 시작 카테고리의 코드들 입니다.\n'''\ndef when_start():\ndef when_click_mouse_on():\ndef when_click_mouse_off():\ndef when_get_signal(\"signal name\"):\nEntry.send_signal(\"signal name\")\nEntry.send_signal_wait(\"signal name\")\ndef when_start_scene():\nEntry.start_scene(\"scene name\")\nEntry.start_scene_of(\"You can choose between 'next' and 'prev'\")\n'''",
    "input: 흐름 카테고리의 코드를 알려줘",
    "output: 다음은 흐름 카테고리의 코드들 입니다.\n'''\nEntry.wait_for_sec(...)\nfor i in range(...): #'i'is not variable if you want variable i and make variable i\nwhile ...:\nbreak\nif ...:\nelse:\nEntry.wait_until(...)\nEntry.stop_code(\"You can choose between 'all', 'self', 'this', 'others' and 'other_objects'\")\nEntry.start_again() #작품을 처음부터 다시 실행합니다.\ndef when_make_clone(): #해당 오브젝트의 복제본이 새로 생성되었을 때 아래 명령어들을 실행합니다.\nEntry.make_clone_of(\"self\") #복제본을 생성합니다.\nEntry.remove_this_clone() #생성된 복제본을 삭제합니다.\nEntry.remove_all_clone()\n'''",
    "input: 생김새 카테고리의 코드를 알려줘",
    "output: 다음은 생김새 카테고리의 코드들 입니다.\n'''\nEntry.show()\nEntry.hide()\nEntry.print(\"...\") #You should use this instead of print\nEntry.clear_print()\nEntry.change_shape(\"Shape name\")\nEntry.change_shape_to(\"You can choose between 'next' and 'prev'\")\nEntry.add_effect(\"You can choose between 'color', 'brightness' and 'transparency'\", ...)\nEntry.set_effect(\"You can choose between 'color', 'brightness' and 'transparency'\", ...)\nEntry.clear_effect()\nEntry.add_size(...)\nEntry.set_size(...)\nEntry.flip_horizontal()\nEntry.flip_vertical()\n'''",
    "input: 붓 카테고리의 코드를 알려줘",
    "output: 다음은 붓 카테고리의 코드들 입니다.\n'''\nEntry.stamp()\nEntry.start_drawing()\nEntry.stop_drawing()\nEntry.set_brush_color_to(\"hexadecimal code\")\nEntry.set_brush_color_to_random()\nEntry.add_brush_size(...)\nEntry.set_brush_size(...)\nEntry.add_brush_transparency(...)\nEntry.set_brush_transparency(...)\nEntry.clear_drawing()\n'''",
    "input: 소리 카테고리의 코드를 알려줘",
    "output: 다음은 소리 카테고리의 코드들 입니다.\n'''\nEntry.play_sound(\"sound name\")\nEntry.play_sound_and_wait(\"sound name\")\nEntry.add_sound_volume(...)\nEntry.set_sound_volume(...)\nEntry.stop_sound()\n판단 (if문)\nEntry.is_mouse_clicked()\nEntry.is_key_pressed(\"...\")\nEntry.is_touched(\"You can choose between 'mouse_pointer', 'edge', 'edge_up', 'edge_down', 'edge_right', 'edge_left' and other object name\")\nEntry.is_boost_mode()\n'''",
    "input: 계산 카테고리의 코드를 알려줘",
    "output: 다음은 계산 카테고리의 코드들 입니다.\n'''\nEntry.value_of_mouse_pointer(\"You can choose between 'y' and 'x'\")\nEntry.value_of_object(\"other object name\", \"You can choose between 'y' and 'x'\")\nEntry.value_of_sound_volume()\nEntry.value_of_current_time(\"You can choose between 'year', 'month', 'day', 'hour', 'minute', 'second' and 'day_of_week'\")\nEntry.value_of_sound_length_of(\"sound name\")\nEntry.value_of_username()\nEntry.value_of_nickname()\nlen(\"...\")\n'''",
    "input: 자료 카테고리의 코드를 알려줘",
    "output: 다음은 자료 카테고리의 코드들 입니다.\n'''\nEntry.input(\"...\")\nEntry.answer()\nEntry.answer_view(\"You can choose between 'hide' and 'show'\")\n'''",
    "input: 자연스러운 물리엔진에 관한 코드를 짜줘",
    "output: 다음은 물리엔진을 간단하게 구현한 코드입니다.\n'''\ndef when_start():\n  while True:\n    Entry.add_x(x)\n    if Entry.is_key_pressed(\"right\"):\n      x += 0.5\n      방향 += 0.6\n      Entry.set_rotation((방향 * 2))\n    else:\n      Entry.set_rotation((방향 * 2))\n    if Entry.is_key_pressed(\"left\"):\n      x += -0.5\n      방향 += -0.6\n      Entry.set_rotation((방향 * 2))\n    else:\n      Entry.set_rotation((방향 * 2))\n    방향 = (방향 * 0.909)\n    x = (x * 0.909)\n    if Entry.is_touched(\"edge_right\"):\n      x += -0.4\n    if Entry.is_touched(\"edge_left\"):\n      x += 0.4\ndef when_start():\n  while True:\n    Entry.add_y(중력)\n    중력 += -0.3\n    if Entry.is_touched(\"edge_down\"):\n      Entry.add_y((중력 * -1))\n      if (중력 < 0):\n        중력 = 0\n        if Entry.is_key_pressed(\"up\"):\n          중력 = 7\n'''",
    "input: 화살표키로 움직이는 코드를 짜줘",
    "output: '''\ndef when_start():\n  while True:\n    if Entry.is_key_pressed(\"right\"):\n      Entry.add_x(10)\n    if Entry.is_key_pressed(\"left\"):\n      Entry.add_x(-10)\n    if Entry.is_key_pressed(\"up\"):\n      Entry.add_y(10)\n    if Entry.is_key_pressed(\"down\"):\n      Entry.add_y(-10)\n'''\n\n이 코드는 화살표키로 오브젝트를 움직입니다.",
    "input: 3d 효과를 보여주는 코드를 짜줘",
    "output: '''\ndef when_start():\n  Entry.show()\n  for i in range(50):\n    Entry.change_shape_to(\"next\")\n    Entry.make_clone_of(\"self\")\n    Entry.add_y(0.8)\n  Entry.hide()\ndef when_make_clone():\n  while True:\n    if Entry.is_key_pressed(\"right\"):\n      Entry.add_rotation(-2)\n    if Entry.is_key_pressed(\"left\"):\n      Entry.add_rotation(2)\n'''\n이 코드는 3d효과를 주어서 3d처럼 보이는 코드입니다.",
    "input: 자연스러운 이동 코드를 짜줘",
    "output: 다음은 화살표키를 이용해 움직이는 코드 입니다.\n'''\ndef when_start():\n  Entry.show()\n  while True:\n    if Entry.is_key_pressed(\"right\"):\n      Entry.add_x(10)\n      Entry.add_rotation(2)\n    if Entry.is_key_pressed(\"left\"):\n      Entry.add_x(-10)\n      Entry.add_rotation(-2)\n    if Entry.is_key_pressed(\"up\"):\n      Entry.add_y(10)\n      Entry.add_rotation(2)\n    if Entry.is_key_pressed(\"down\"):\n      Entry.add_y(-10)\n      Entry.add_rotation(-2)\n    Entry.add_direction(-5)\n'''",
    "input: 자료들의 편균을 구하는 코드를 짜줘",
    "output: '''\n자료의총개수 = 0\n번호 = 1\n자료의합 = 0\n\ndef when_start():\n    Entry.input(\"자료의 총 개수는 몇입니까?\")\n    if (Entry.answer() < 2):\n        Entry.print(\"자료의 수는 2개 이상이어야 합니다.\")\n        Entry.wait_for_sec(2)\n        Entry.start_again()\n    else:\n        자료의총개수 = Entry.answer()\n        for i in range(자료의총개수):\n            Entry.input((번호 + \"번 째 수는?\"))\n            자료의합 += math.round(Entry.answer())\n            번호 += 1\n        Entry.print((\"자료들의 평균 값은 \" + ((자료의합 / 자료의총개수) + \"입니다 \")))\n'''\n이코드는 유저에게서 자료를 받아 평균을 구하는 코드 입니다.",
    "input: 점프 물리엔진 코드를 짜줘",
    "output: '''\ny가속도 = 0\n\ndef when_start():\n    while True:\n        if Entry.is_key_pressed(\"right\"):\n            Entry.add_x(5)\n            if Entry.is_touched(\"edge_right\"):\n                Entry.add_x(-5)\n        if Entry.is_key_pressed(\"left\"):\n            Entry.add_x(-5)\n            if Entry.is_touched(\"edge_left\"):\n                Entry.add_x(5)\n        y가속도 += -0.5\n        Entry.add_y(y가속도)\n        if Entry.is_touched(\"edge_down\"):\n            Entry.add_y((0 - y가속도))\n            if Entry.is_key_pressed(\"up\"):\n                y가속도 = 10\n            else:\n                y가속도 = 0\n'''\n이코드는 점프 물리엔진을 간단하게 구현한 코드입니다.",
    "input: 균형잡기 게임을 만들어줘",
    "output: 다음 코드는 벽에 닿지 않기위해 일정간격으로 마우스를 클릭해 균형을 유지하는 코드 입니다.\n'''\ndef when_start():\n    while True:\n        if Entry.is_mouse_clicked():\n            Entry.add_y(5)\n            if Entry.is_touched(\"edge\"):\n                Entry.add_y(-5)\n        else:\n            Entry.add_y(-5)\n            if Entry.is_touched(\"edge\"):\n                Entry.add_y(5)\n\tif Entry.is_touched(\"edge\"):\n\t\tEntry.print(\"game over!\")\n'''",
    "input: 이동하는 코드를 짜줘",
    "output: '''\ndef when_start():\n    while True:\n        if Entry.is_key_pressed(\"W\"):\n            Entry.add_y(2)\n        if Entry.is_key_pressed(\"D\"):\n            Entry.add_x(2)\n        if Entry.is_key_pressed(\"S\"):\n            Entry.add_y(-2)\n        if Entry.is_key_pressed(\"A\"):\n            Entry.add_x(-2)\n'''\n이 코드는 wasd키를 이용해 이동하는 코드입니다.",
    "input: 마우스 위치로 이동하는 코드",
    "output: ```\ndef when_start():\n   while True:\n       Entry.move_to(\"mouse_pointer\")\n       Entry.wait_for_sec(0.1)\n```\n\n이 코드는 로봇이 마우스의 위치로 이동하는 코드입니다.",
    "input: 신호를 주고 받는 코드를 짜줘",
    "output: ```\ndef when_start():\n    Entry.send_signal(\"hello\")\ndef when_get_signal(\"hello\"):\n    Entry.print(\"hello\")\n```\n\n이 코드는 로봇이 \"hello\"라는 신호를 보내고 받는 코드입니다.",
    "input: 3d를 만들고 싶어",
    "output: ```\ndef when_start():\n    Entry.change_shape_to(\"next\")\n    for i in range(10):\n        Entry.make_clone_of(\"self\")\n        Entry.add_y(-20)\n    Entry.hide()\ndef when_make_clone():\n    while True:\n        if Entry.is_key_pressed(\"right\"):\n            Entry.add_x(10)\n        if Entry.is_key_pressed(\"left\"):\n            Entry.add_x(-10)\n```\n\n이 코드는 로봇이 3D처럼 보이는 코드입니다.",
    "input: 점프를 하는 플레이어 오브젝트의 코드를 짜줘 그리고 장애물 오브젝트에 들어갈 랜덤 위치로 이동하는 코드도 각각 짜줘 그리고 플레이어 오브젝트가 장애물 오브젝트에 닿으면 게임이 멈추게해줘",
    "output: 다음은 플레이어 오브젝트 코드 입니다.\n'''\ndef when_start():\n    while True:\n        if Entry.is_key_pressed(\"W\"):\n            Entry.add_y(2)\n        if Entry.is_key_pressed(\"D\"):\n            Entry.add_x(2)\n        if Entry.is_key_pressed(\"S\"):\n            Entry.add_y(-2)\n        if Entry.is_key_pressed(\"A\"):\n            Entry.add_x(-2)\n\t\tif Entry.is_touched(\"obstacle\")\n\t\t\tEntry.print(\"Game over\")\n\t\t\tEntry.stop_code(\"all\")\n'''\n\n다음은 obstacle 오브젝트의 코드입니다.\n'''\ndef when_start():\n    while True:\n        random_x = random.randint(-240, 240)\n        random_y = random.randint(-180, 180)\n        Entry.set_xy(random_x, random_y)\n        Entry.wait_for_sec(1)\n'''",
    "input: 점프로 피하는 게임의 플레이어와 오브젝트의 코드를 짜줘",
    "output: '''\n# 플레이어 코드\ndef when_start():\n    while True:\n        if Entry.is_key_pressed(\"W\"):\n            Entry.add_y(2)\n        if Entry.is_key_pressed(\"D\"):\n            Entry.add_x(2)\n        if Entry.is_key_pressed(\"S\"):\n            Entry.add_y(-2)\n        if Entry.is_key_pressed(\"A\"):\n            Entry.add_x(-2)\n\n# 오브젝트 코드\ndef when_start():\n    while True:\n        random_x = random.randint(-240, 240)\n        random_y = random.randint(-180, 180)\n        Entry.set_xy(random_x, random_y)\n        Entry.wait_for_sec(1)\n'''",
    "input: 모양을 0.2초마다 바꾸는 코드를 짜줘",
    "output: ```\ndef when_start():\n  while True:\n    Entry.change_shape_to(\"next\")\n    Entry.wait_for_sec(0.2)\n```\n이코드는 모양을 0.2초마다 바꾸게 합니다.",
    "input: 소리를 출력하고 2초를 기다리고 다시 출력하는 걸 반복하는 코드를 짜줘",
    "output: ```\ndef when_start():\n  while True:\n    Entry.play_sound(\"ping\")\n    Entry.wait_for_sec(2)\n```\n이코드는 ping이라는 이름의 소리를 출력합니다.",
    "input: 소리를 재생하고 재생이 끝날때까지 기다리는 코드를 짜줘",
    "output: ```\ndef when_start():\n  while True:\n    Entry.play_sound_and_wait(\"ping\")\n```\n이코드는 ping이라는 이름의 소리를 재생합니다.",
    "input: 유저의 닉네임을 출력하는 코드를 짜줘",
    "output: ```\ndef when_start():\n    Entry.print(Entry.value_of_nickname())\n```\n이코드는 Entry.print함수를 이용해 유저의 닉네임을 출력합니다.",
    "input: 유저의 아이디를 출력하는 코드",
    "output: ```\ndef when_start():\n    Entry.print(Entry.value_of_username())\n```\n\n이 코드는 Entry.print함수를 이용해 유저의 아이디를 출력합니다.",
    "input: 현재 년, 월, 일, 시, 분, 초를 출력하는 코드를 짜줘",
    "output: ```\ndef when_start():\n    Entry.print(Entry.value_of_current_time(\"year\"))\n    Entry.print(Entry.value_of_current_time(\"month\"))\n    Entry.print(Entry.value_of_current_time(\"day\"))\n    Entry.print(Entry.value_of_current_time(\"hour\"))\n    Entry.print(Entry.value_of_current_time(\"minute\"))\n    Entry.print(Entry.value_of_current_time(\"second\"))\n```\n\n이 코드는 Entry.print함수를 이용해 현재 년, 월, 일, 시, 분, 초를 출력합니다.",
    "input: 탄젠트를 이용한 로딩 예제를 짜줘",
    "output: '''\nself.tan = \"0\"\n\ndef when_start():\n    for i in range(3):\n        Entry.make_clone_of(\"self\")\n        Entry.wait_for_sec(0.15)\n\ndef when_make_clone():\n    Entry.show()\n    while True:\n        self.tan += 2\n        Entry.set_x((math.tan(self.tan) * 70))\n        Entry.set_rotation((math.tan(self.tan) * 70))\n        Entry.set_effect(\"transparency\", math.fabs((math.tan(self.tan) * 35)))\n'''\n이 코드를 사용하면 탄젠트 함수를 이용해 자연스럽게 로딩이 만들어지게 됩니다.",
    "input: 마우스 포인터를 천천히 따라가는 코드를 짜줘",
    "output: ```\ndef when_start():\n    Entry.move_to(\"mouse_pointer\")\n    Entry.wait_for_sec(0.1)\n    Entry.move_to(\"mouse_pointer\")\n    Entry.wait_for_sec(0.1)\n```\n\n이 코드는 Entry.move_to함수를 이용해 로봇이 마우스 포인터의 위치로 천천히 이동합니다.",
    "input: 마우스를 클릭하면 클릭한 마우스의 좌표를 출력하는 코드를 짜줘",
    "output: ```\ndef when_click_mouse_on():\n    Entry.print(Entry.value_of_mouse_pointer(\"x\"))\n    Entry.print(Entry.value_of_mouse_pointer(\"y\"))\n```\n\n이 코드는 Entry.print함수를 이용해 클릭한 마우스의 x좌표와 y좌표를 출력합니다.",
    "input: 제귀함수로 10번 다음 모양으로 바꾸는 코드를 짜줘",
    "output: ```\ndef when_start():\n    change_shape_10_times()\n\ndef change_shape_10_times():\n    if count < 10:\n        Entry.change_shape_to(\"next\")\n        Entry.wait_for_sec(0.1)\n        count += 1\n        change_shape_10_times()\n```\n\n이 코드는 Entry.change_shape_to함수를 이용해 로봇의 모양을 10번 바꿉니다.",
    "input: 제귀 함수 예제코드를 짜줘",
    "output: ```\ndef when_start():\n    n = 10\n    recursion()\n\ndef recursion():\n  if n > 0:\n    n = n - 1\n    Entry.print(n)\n    recursion()\n```\n이 코드는 9부터 0까지의 숫자를 출력하는 재귀 함수입니다.",
    "input: 마우스를 클릭하면 그림을 그릴수 있는 코드를 짜줘",
    "output: ```\ndef when_click_mouse_on():\n    while Entry.is_mouse_clicked():\n        Entry.move_to(\"mouse_pointer\")\n        Entry.start_drawing()\n\ndef when_click_mouse_off():\n    Entry.stop_drawing()\n```\n이 코드는 마우스를 클릭하면 그림을 그리기 시작하고, 마우스를 떼면 그림 그리기를 멈춥니다.",
    "input: 마우스를 클릭하면 그림을 그릴수 있는 코드를 짜줘 그리고 스페이스 버튼을 누르면 색을 바꾸게해줘",
    "output: ```\ndef when_click_mouse_on():\n    while Entry.is_mouse_clicked():\n        Entry.move_to(\"mouse_pointer\")\n        Entry.start_drawing()\n\ndef when_click_mouse_off():\n    Entry.stop_drawing()\n\ndef when_start():\n    while True:\n        if Entry.is_key_pressed(\"space\"):\n            Entry.set_brush_color_to_random()\n```\n이 코드는 마우스를 클릭하면 그림을 그리기 시작하고, 마우스를 떼면 그림 그리기를 멈춥니다. 또한, 스페이스 버튼을 누르면 그림의 색이 바뀝니다.",
    "input: 좌우반전을 하는 코드를 짜줘",
    "output: ```\ndef when_start():\n  Entry.flip_horizontal()\n```\n이 코드는 로봇의 그림을 좌우반전합니다.",
    "input: 복제본을 이용해서 스페이스 키를 누르면 다음 모양으로 변한 자신의 오브젝트가 앞으로 벽에 닿을때까지 가게 하는 코드를 짜줘",
    "output: ```\ndef when_start():\n    while True:\n        if Entry.is_key_pressed(\"space\"):\n            Entry.make_clone_of(\"self\")\n            Entry.print(\"make clone\")\n\ndef when_make_clone():\n    Entry.change_shape_to(\"next\")\n    while True:\n        Entry.move_to_direction(10)\n        if Entry.is_touched(\"edge\"):\n            Entry.remove_this_clone()\n```\n이 코드는 스페이스를 누르면 복제본을 생성하고 복제본이 앞으로 갑니다.",
    "input: q키를 누르면 보이고 e키를 누르면 숨기는 코드를 짜줘",
    "output: ```\ndef when_start():\n    while True:\n        if Entry.is_key_pressed(\"E\"):\n            Entry.hide()\n        if Entry.is_key_pressed(\"Q\"):\n            Entry.show()\n```\n\n이코드를 실행하면 q키를 누르면 보이고 e키를 누르면 숨깁니다.",
    "input: 저장프로그램을 짜줘",
    "output: ```\ndef when_start():\n    Entry.start_scene(\"장면 1\")\n\ndef when_start_scene():\n    while True:\n        Entry.wait_for_sec(random.randint(10, 20))\n\ndef when_start_scene():\n    if (len(Entry.value_of_username()) < 4):\n        Entry.print_for_sec(\"작품을 실행하시려면 먼저 로그인을 하고 플레이해주시길 바랍니다.\", 4)\n        Entry.stop_code(\"all\")\n    else:\n        if Entry.value_of_username() in 아이디값:\n            Entry.print_for_sec((\"다시 만나서 반갑습니다.\" + (Entry.value_of_username() + \"님^^\")), 4)\n            회원번호 = 0\n            for i in range(len(아이디값)):\n                회원번호 += 1\n                if (Entry.value_of_username() == 아이디값[회원번호 - 1]):\n                    Entry.wait_for_sec(2)\n        else:\n            회원번호 = (len(아이디값) + 1)\n            아이디값.insert(회원번호 - 1, Entry.value_of_username())\n            돈.insert(회원번호 - 1, 0)\n            Entry.print_for_sec((\"처음 만나서 반갑습니다.\" + (Entry.value_of_username() + \"님^^\")), 4)\n        Entry.wait_for_sec(2)\n```",
    "input: 채력바 예제를 만들어줘",
    "output: '''\n체력 = 100\n차 = \"0\"\nn = \"0\"\nrot = \"0\"\n\ndef when_make_clone():\n    Entry.set_brush_size(30)\n    while True:\n        Entry.clear_drawing()\n        Entry.set_brush_color_to(\"#333333\")\n        Entry.set_xy((0 - ((250 / 2) + 5)), 0)\n        Entry.start_drawing()\n        Entry.set_xy(((250 / 2) + 5), 0)\n        Entry.stop_drawing()\n\ndef when_start():\n    Entry.make_clone_of(\"self\")\n    Entry.set_brush_size(20)\n    while True:\n        Entry.clear_drawing()\n        Entry.set_brush_color_to(\"#55ff00\")\n        Entry.set_xy((0 - 125), 0)\n        Entry.start_drawing()\n        Entry.set_xy(((0 - 125) + (250 * (체력 / 100))), 0)\n        Entry.set_brush_color_to(\"#ff0000\")\n        if (0 <= (n - 체력)):\n            Entry.set_xy((((0 - 125) + (250 * (n / 100))) + 차), 0)\n        else:\n            Entry.set_xy((((0 - 125) + (250 * (체력 / 100))) + 차), 0)\n        Entry.stop_drawing()\n\ndef when_start():\n    while True:\n        n = 체력\n        Entry.wait_for_sec(0.01)\n        차 = (n - 체력)\n        Entry.wait_for_sec(1)\n'''\n이 코드를 사용하면 붓을 이용해서 채력에 따라 채력바가 만들어 보입니다.",
    "input: 랭킹 예제를 만들어줘",
    "output: ```\nrank = 0\nscore = 0\n\ndef when_start():\n    while True:\n        score += Entry.value_of_score() * 10\n        Entry.print(\"당신의 점수는 \" + score + \"점입니다.\")\n        if score >= 1000:\n            if rank <= 1:\n                Entry.print(\"당신은 1등입니다!\")\n                rank += 1\n            elif rank <= 3:\n                Entry.print(\"당신은 3등입니다!\")\n                rank += 1\n            elif rank <= 5:\n                Entry.print(\"당신은 5등입니다!\")\n                rank += 1\n            else:\n                Entry.print(\"당신은 랭킹에 들지 못했습니다.\")\n        Entry.wait_for_sec(0.1)\n```",
    "input: 무지게 그라이데이션 예제를 짜줘",
    "output: ```\nn = \"0\"\nself.n1 = \"0\"\n\ndef when_start():\n    self.n1 = 0\n    for i in range(6):\n        self.n1 += 1\n        Entry.make_clone_of(\"self\")\n        Entry.change_shape_to(\"next\")\n    n = 6\n\ndef when_make_clone():\n    Entry.wait_until((n == 6))\n    Entry.show()\n    while True:\n        Entry.wait_until((self.n1 == n))\n        for i in range(100):\n            Entry.add_effect(\"transparency\", 1)\n        if (n == 1):\n            n = 6\n        else:\n            n += -1\n        Entry.send_layer_to(\"back\")\n        Entry.set_effect(\"transparency\", 0)\n```\n이코드를 사용하면 오브젝트가 무지게 처럼 변하게 됩니다.",
    "input: 스크롤 예제를 만들어줘",
    "output: 다음은 스크롤 예제 입니다.\n'''\n오브젝트길이 = \"0\"\n기본값 = \"0\"\n백분율 = \"0\"\n슬라이더길이1 = 100\n현재위치 = \"0\"\n현재클릭 = \"0\"\n\ndef when_start():\n    while True:\n        Entry.wait_until(Entry.is_mouse_clicked())\n        if Entry.is_touched(\"mouse_pointer\"):\n            현재클릭 = Entry.value_of_mouse_pointer(\"y\")\n            현재위치 = Entry.value_of_object(\"self\", \"y\")\n            Entry.set_effect(\"brightness\", -50)\n            while Entry.is_mouse_clicked():\n                if (135 >= ((Entry.value_of_mouse_pointer(\"y\") + (현재위치 - 현재클릭)) + (슬라이더길이1 / 2))):\n                    if (-135 <= ((Entry.value_of_mouse_pointer(\"y\") + (현재위치 - 현재클릭)) - (슬라이더길이1 / 2))):\n                        Entry.set_y((Entry.value_of_mouse_pointer(\"y\") + (현재위치 - 현재클릭)))\n                    else:\n                        Entry.set_y((-135 + (슬라이더길이1 / 2)))\n                else:\n                    Entry.set_y((135 - (슬라이더길이1 / 2)))\n                백분율 = (100 * (((Entry.value_of_object(\"self\", \"y\") - (135 - (슬라이더길이1 / 2))) * -1) / (270 - 슬라이더길이1)))\n            Entry.set_effect(\"brightness\", 0)\n        Entry.wait_until(not (Entry.is_mouse_clicked()))\n'''",
    "input: 하트그리기",
    "output: '''\nt = \"0\"\n\ndef when_start():\n    Entry.set_brush_color_to(\"#FF0000\")\n    Entry.start_drawing()\n    while not (t > (8 * math.atan(1))):\n        Entry.set_xy((64 * (math.sin(t) * (math.sin(t) ** 2))), ((((52 * math.cos(t)) - (20 * math.cos((2 * t)))) - (8 * math.cos((3 * t)))) - (4 * math.cos((4 * t)))))\n        t += 1\n'''\n이 코드는 하트를 그립니다.",
    "input: 앞으로 10만큼 이동하는 걸 3번 반복하고 270도 회전하기 코드를 짜줘",
    "output: ```\ndef when_start():\n    for i in range(3):\n        Entry.move_to_direction(10)\n    Entry.add_rotation(270)\n```",
    "input: 별그리기",
    "output: '''\ndef when_start():\n    Entry.set_brush_color_to(\"#FF0000\")\n    Entry.set_brush_size(5)\n    Entry.start_drawing()\n    for i in range(5):\n        Entry.move_to_direction(200)\n        Entry.add_rotation(144)\n        Entry.wait_for_sec(0.1)\n'''\n이코드는 별을 그립니다.",
    "input: 정렬하기 코드를 짜줘",
    "output: '''\n아무변수 = \"0\"\n총 = \"0\"\n변수2 = \"0\"\n변수1 = \"0\"\n정렬 = []\n\ndef when_start():\n    Entry.input(\"몇개를 정렬할래?\")\n    총 = Entry.answer()\n    Entry.send_signal_wait(\"신호\")\n    Entry.send_signal_wait(\"신호1\")\n    Entry.stop_code(\"this\")\n\ndef when_get_signal(\"신호1\"):\n    변수1 = 1\n    변수2 = 2\n    while not (변수1 == 총):\n        while not (변수2 > 총):\n            if (정렬[변수1 - 1] > 정렬[변수2 - 1]):\n                아무변수 = 정렬[변수1 - 1]\n                정렬[변수1 - 1] = 정렬[변수2 - 1]\n                정렬[변수2 - 1] = 아무변수\n            변수2 += 1\n        변수1 += 1\n        변수2 = (변수1 + 1)\n    Entry.print(\"정렬 완료\")\n\ndef when_get_signal(\"신호\"):\n    변수1 = 1\n    while not (변수1 > 총):\n        Entry.input(\"정렬할 수를 입력\")\n        정렬.append(Entry.answer())\n        변수1 += 1\n\ndef when_press_key(\"space\"):\n    Entry.start_again()\n'''\n이코드는 반복문으로 정렬하는 코드입니다.",
    "input: n각형 그리기",
    "output: ```\nn = 3\n\ndef when_start():\n    Entry.start_drawing()\n    Entry.set_brush_size(30)\n    for i in range(n):\n        Entry.move_to_direction(100)\n        Entry.add_rotation((360 / n))\n```\n이코드는 n각형을 그립니다.",
    "input: 도장찍기",
    "output: ```\ndef when_start():\n    while True:\n        Entry.move_to(\"mouse_pointer\")\n\ndef when_click_object_on():\n    Entry.stamp()\n    Entry.change_shape_to(\"next\")\n```\n\n이 코드는 마우스를 클릭하면 도장을 찍는 코드입니다.",
    "input: 이동방향을 45도씩 꺾으면서 50씩 이동하는걸 2번 반복하기",
    "output: ```\ndef when_start():\n    for i in range(2):\n        Entry.move_to_direction(50)\n        Entry.add_rotation(45)\n```",
    "input: 입력받은값다시출력하는코드",
    "output: ```\n변수 = ''\n\ndef when_start():\n    Entry.input(\"출력할 문자를 입력해주세요.\")\n    변수 = Entry.answer()\n    \ndef when_press_key(\"enter\"):\n    Entry.print(변수)\n```\n이코드를 사용하면 입력한 값을 엔터를 누르면 출력합니다.",
    "input: 폭죽효과를 만들어줘",
    "output: '''\n마우스x = 0\n마우스y = 0\nself.속도 = 0\nself.떨어지는속도 = 0\nself.x = 0\nself.y = 0\n\ndef when_start():\n    while True:\n        if Entry.is_mouse_clicked():\n            마우스x = Entry.value_of_mouse_pointer(\"x\")\n            마우스y = Entry.value_of_mouse_pointer(\"y\")\n            Entry.change_shape(random.randint(1, 4))\n            Entry.set_size(7.5)\n            Entry.make_clone_of(\"self\")\n            Entry.make_clone_of(\"self\")\n            Entry.make_clone_of(\"self\")\n            Entry.make_clone_of(\"self\")\n            Entry.make_clone_of(\"self\")\n            Entry.make_clone_of(\"self\")\n            Entry.make_clone_of(\"self\")\n            Entry.make_clone_of(\"self\")\n            Entry.make_clone_of(\"self\")\n            Entry.make_clone_of(\"self\")\n            Entry.make_clone_of(\"self\")\n            Entry.make_clone_of(\"self\")\n            Entry.make_clone_of(\"self\")\n            Entry.wait_for_sec(0.1)\n        Entry.set_x((Entry.value_of_mouse_pointer(\"x\") / 5))\n\ndef when_make_clone():\n    self.x = 마우스x\n    self.y = 마우스y\n    for i in range(40):\n        Entry.add_xy_for_sec(((self.x - Entry.value_of_object(\"self\", \"x\")) / 10), ((self.y - Entry.value_of_object(\"self\", \"y\")) / 10), 0)\n    Entry.set_rotation(random.randint(0.00, 359.99))\n    self.속도 = 10\n    Entry.set_size(5)\n    while not (Entry.value_of_object(\"self\", \"y\") < -135):\n        self.떨어지는속도 += -0.12\n        Entry.add_y(self.떨어지는속도)\n        Entry.move_to_direction(self.속도)\n        self.속도 += ((0 - self.속도) / 20)\n    Entry.remove_this_clone()\n'''",
    "input: 피타고라스의 정의로 거리 구하는 코드",
    "output: ```\ndef when_start():\n    Entry.input(\"x1 좌표를 입력해주세요.\")\n    x1 = Entry.answer()\n    Entry.input(\"x2 좌표를 입력해주세요.\")\n    x2 = Entry.answer()\n    Entry.input(\"y1 좌표를 입력해주세요.\")\n    y1 = Entry.answer()\n    Entry.input(\"y2 좌표를 입력해주세요.\")\n    y2 = Entry.answer()\n    Entry.print(((\"거리는 \" + math.sqrt((((x1 - x2) ** 2) + ((y1 - y2) ** 2)))) + \"입니다.\"))\n```",
    "input: 방향 구하는 코드",
    "output: 다음 코드는 방향을 구하게 해주는 코드입니다.\n```\ndef when_start():\n    Entry.input(\"x1 좌표를 입력해주세요.\")\n    x1 = Entry.answer()\n    Entry.input(\"y1 좌표를 입력해주세요.\")\n    y1 = Entry.answer()\n    Entry.input(\"x2 좌표를 입력해주세요.\")\n    x2 = Entry.answer()\n    Entry.input(\"y2 좌표를 입력해주세요.\")\n    y2 = Entry.answer()\n    if (y1 >= y2):\n        Entry.print(math.atan(((x2 - x1) / (y2 - y1))))\n    else:\n        Entry.print((math.atan(((x2 - x1) / (y2 - y1))) + 180))\n```",
    "input: 유저에게 퀴즈를 내고 유저가 입력한 답이 맞으면 정답 틀리면 틀렸다고 말하는 코드를 짜줘 문제는 니가 만들어서",
    "output: ```\n문제 = \"1+1은?\"\n정답 = \"2\"\n\ndef when_start():\n    Entry.input(문제)\n    답 = Entry.answer()\n    if 답 == 정답:\n        Entry.print(\"정답입니다!\")\n    else:\n        Entry.print(\"틀렸습니다.\")\n```",
    "input: 2초동안 클릭을 얼마나 했는지 클릭속도를 구하는 코드를 짜줘",
    "output: ```\n클릭횟수 = 0\n\ndef when_start():\n    Entry.timer(\"start\")\n    Entry.wait_until((2 < Entry.value_of_timer()))\n    Entry.timer(\"stop\")\n    Entry.print(((\"클릭 횟수는 \" + 클릭횟수) + \"입니다!\"))\n\ndef when_click_mouse_on():\n    클릭횟수 = (클릭횟수 + 1)\n```\n이코드는 2초동안 클릭한 횟수를 출력합니다.",
    "input: 덤블링코드를 짜줘",
    "output: ```\ndef when_start():\n  while True:\n    Entry.add_rotation(10)\n```",
    "input: 타이머를 활용한 코드",
    "output: ```\ndef when_start():\n    Entry.input(\"시간을 입력해주세요.\")\n    Entry.timer(\"start\")\n    Entry.wait_until(Entry.answer() < Entry.value_of_timer())\n    Entry.timer(\"stop\")\n```\n  이 코드는 타이머를 설정하여 시간이 되면 정지합니다.",
    "input: 안녕이라고 입력하면 안녕하세요 이런식으로 출력하는 코드를 짜줘",
    "output: ```\ndef when_start():\n    while True:\n        Entry.input(\"질문을 해 주세요.\")\n        질문 = Entry.answer()\n        if (질문 == \"안녕\"):\n            Entry.print(\"안녕하세요!\")\n        Entry.wait_for_sec(2)\n```",
    "input: 안녕이라고 입력하면 안녕하세요 이런식으로 출력하는 코드를 짜줘근데 질문에 대한 답을 한 10개 정도로 해줘",
    "output: ```\n유저질문 = 0\ni = 0\n답변 = [\"김철수\", \"20살\", \"코딩\", \"짜장면\", \"파스타\", \"강아지\", \"고양이\", \"파란색\", \"빨간색\", \"아이유의 꽃길\"]\n질문 = [\"이름은 뭐야?\", \"나이가 어때?\", \"취미는 뭐야?\", \"좋아하는 음식은?\", \"싫어하는 음식은?\", \"좋아하는 동물은?\", \"싫어하는 동물은?\", \"좋아하는 색깔은?\", \"싫어하는 색깔은?\", \"좋아하는 노래는?\"]\n\ndef when_start():\n    while True:\n        Entry.input(\"질문을 해 주세요.\")\n        유저질문 = Entry.answer()\n        i = 0\n        for i in range(len(질문)):\n            i = (i + 1)\n            if (유저질문 == 질문[i - 1]):\n                Entry.print(답변[i - 1])\n        Entry.wait_for_sec(2)\n```",
    "input: 반복문으로 몇번 반복하고있는지 출력하는 코드",
    "output: ```\n나의번호 = 0\n\ndef when_start():\n    while True:\n        나의번호 += 1\n        Entry.print(나의번호)\n```",
    "input: 10회 반복문으로 몇번 반복하고있는지 출력하는 코드",
    "output: '''\ndef when_start():\n    while (반복횟수 <= 10):\n        Entry.print(반복횟수)\n        반복횟수 += 1\n        Entry.wait_for_sec(0.2)\n```",
    "input: 스프링 처럼 뛰는 효과를 만들어줘",
    "output: ```\ndef when_start():\n    중력 = -0.3\n    while True:\n        while not Entry.is_touched(\"edge_right\"):\n            Entry.add_x(3)\n            Entry.add_y(y가속도)\n            y가속도 += 중력\n            if Entry.is_touched(\"edge_down\"):\n                y가속도 = 7\n        while not Entry.is_touched(\"edge_left\"):\n            Entry.add_x(-3)\n            Entry.add_y(y가속도)\n            y가속도 += 중력\n            if Entry.is_touched(\"edge_down\"):\n                y가속도 = 7\n```",
    "input: 도박게임을 만들어줘",
    "output: ```\n나의돈 = 100\n\ndef when_start():\n    Entry.input(\"돈을 투자합니다.\")\n    Entry.wait_until((나의돈 > Entry.answer()))\n    if (random.randint(0, 3) != 0):\n        나의돈 += (0 - Entry.answer())\n        Entry.print(((\"실패 했습니다. 남은 돈은 \" + 나의돈) + \"입니다.\"))\n    else:\n        나의돈 += Entry.answer()\n        Entry.print(((\"성공했습니다. 남은 돈은 \" + 나의돈) + \"입니다.\"))\n\ndef when_press_key(\"enter\"):\n    Entry.start_again()\n```",
    "input: 바운스볼 물리엔진을 짜줘",
    "output: ```\ndef when_start():\n    while True:\n        Entry.add_y(중력)\n        중력 = (중력 - 0.3)\n        if Entry.is_touched(\"edge_down\"):\n            중력 = 0\n            if Entry.is_key_pressed(\"up\"):\n                중력 = 7\n```",
    "input: 대화를 하는 코드를 짜줘",
    "output: ```\ndef when_start():\n    while True:\n        Entry.input(\"내용말하기\")\n        Entry.print(Entry.answer())\n```",
    "input: 채팅 프로그램 처럼 만들어줘",
    "output: ```\ndef when_start():\n    Entry.input(\"내용말하기\")\n    Entry.print(Entry.answer())\n    Entry.send_signal(\"메시지보내기\")\n\ndef when_get_signal(\"메시지보내기\"):\n    Entry.input(\"내용말하기\")\n    Entry.print(Entry.answer())\n    Entry.send_signal(\"메시지보내기\")\n```",
    "input: 안녕",
    "output: 안녕하세요! 저는 대화형 인공지능 챗봇 GetAi입니다. 무엇을 도와드릴까요?",
    "input: 엔트리의 줄임말을 알려줘",
    "output: 다음은 엔트리의 줄임말을 모은것 입니다.\n\n인작인기 작품(메인화면에 있음)스선스태프 선정(메인화면에 있음)문답묻고 답하기(커뮤니티에 있음)노팁노하우&팁(커뮤니티에 있음)엔이엔트리 이야기(커뮤니티에 있음)제건제안 및 건의(커뮤니티에 있음)ㅈㄱㄴ제목이 내용이라는 뜻(커뮤니티에서 많이 쓰임)ㅎㅅㅎ말을 끝낼 때 하는 말(커뮤니티에서 많이 쓰임)커뮤커뮤니티(커뮤니티에서 많이 쓰임)글삭글을 삭제하라고 할때 쓰는 말(커뮤니티에서 많이 쓰임)띵작,믱작걸작(재인작에 많이 쓰임)",
    "input: 안녕 너의 이름은 뭐야",
    "output: 저는 대화형 인공지능 챗봇인 GetAi입니다.",
    "input: 한글자씩 말하는 코드",
    "output: ```\n한글자씩 = 0\n\ndef when_start():\n    한글자씩 = 0\n    for i in range(len(\"이것은 한글자씩 말하기 예제 입니다.\")):\n        한글자씩 += 1\n        Entry.print_for_sec(\"이것은 한글자씩 말하기 예제 입니다.\"[0:한글자씩], 0.1)\n```",
    "input: 너는 무엇을 좋아해?",
    "output: 저는 인공지능 프로그램이기 때문에 좋아하는 것은 없습니다.",
    "input: 니가 생각하기에 가장 쉬운코드는?",
    "output: ```\ndef when_start():\n    Entry.print(\"Hello, world!\")\n```\n\n이 코드는 \"Hello, world!\"라는 메시지를 출력합니다. 이 코드가 쉬운 이유는 다음과 같습니다.\n\n* 이 코드는 매우 짧고 간단합니다.\n* 이 코드는 `Entry.print()` 명령을 사용하여 메시지를 출력합니다. 이 명령은 사용하기 쉽습니다.\n* 이 코드는 다른 코드와 상호 작용하지 않으므로 오류가 발생할 가능성이 적습니다.\n\n이 코드는 초보자가 코딩을 배우는 데 좋은 예제입니다.",
    "input: 너는 누가 만들었어?",
    "output: 저는 Triangle_님이 구글의 Gemini를 튜닝해 만든 대규모 언어 모델입니다.",
    "input: 엔트리가 뭐야",
    "output: 엔트리는 소프트웨어를 통해 미래를 꿈꾸고 함께 성장하는 창작 플랫폼입니다.엔트리에서는 생각하고, 만들고, 공유하는 과정을 통해 모두의 꿈을 이루어 나갑니다.",
    "input: 안녕 반가워",
    "output: 안녕하세요! 반갑습니다.",
    "input: " + input,
    "output: ",
  ]

  response = model.generate_content(prompt_parts)
  return response.text


app = Flask(__name__)
CORS(app, resources={r"/get_response": {"origins": "*"}})


@app.route('/get_response', methods=['POST'])
def get_response():
  user_input = request.json['user_input']

  # AI로부터 응답을 생성합니다.
  ai_response = GetResponse(user_input)

  print(user_input)

  print(ai_response)

  return jsonify({'ai_response': ai_response})


if __name__ == '__main__':
  app.run(host="0.0.0.0")
