from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Используем лёгкую версию LLaMA 2
model_name = "NousResearch/Llama-2-7b-chat-hf"

# Загружаем токенизатор и модель
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

# Создаём пайплайн для генерации текста
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_length=100)

# Вопросы и правильные ответы
questions = [
    {"question": "Что будет, если бросить камень в воду?", "answer": "Он утонет"},
    {"question": "Что тяжелее: килограмм пуха или килограмм железа?", "answer": "Они весят одинаково"},
    {"question": "Если мама старше дочери на 25 лет, то на сколько лет дочь будет младше мамы через 5 лет?", "answer": "На 25 лет"}
]

score = 0

for q in questions:
    user_answer = input(q["question"] + "\nВаш ответ: ").strip()

    # Формируем промпт для модели
    prompt = (f"Правильный ответ: '{q['answer']}'.\n"
              f"Ответ пользователя: '{user_answer}'.\n"
              "Оцени, насколько ответ похож по смыслу (1 - полностью правильный, 0 - совсем неправильный), и объясни различия.")

    # Получаем ответ от модели
    response = pipe(prompt)[0]["generated_text"]

    # Оцениваем результат
    if "1" in response:
        print("✅ Отлично! Ваш ответ по смыслу очень близок.")
        score += 1
    elif "0.5" in response:
        print(f"🟡 Почти верно! Ваш ответ похож, но немного не точен.\nОтвет модели: {response}")
    else:
        print(f"❌ Неверно! Правильный ответ: {q['answer']}\nОтвет модели: {response}")

print(f"\n🎯 Тест завершен! Ваш результат: {score}/{len(questions)}")
