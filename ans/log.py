import replicate

# Инициализация клиента с вашим API-ключом
client = replicate.Client(api_token="r8_SEoZimJ6StbuwIktU4mjk6kEZuLAGCx4F2TAg")

# Определение модели и входных данных
model = "meta/meta-llama-3-70b-instruct"
prompt = "Объясни квантовую механику простыми словами."

# Генерация ответа
output = client.run(model, input={"prompt": prompt})

# Вывод результата
print(output)
