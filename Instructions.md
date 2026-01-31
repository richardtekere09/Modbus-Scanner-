# Modbus Scanner - Инструкция по установке для Windows

## Требования
- Windows 10/11
- Преобразователь ОВЕН USB-RS485 с установленными драйверами
- Права администратора (для установки драйверов)

---

## Шаг 1: Установка Python

1. Скачайте Python с: https://www.python.org/downloads/
2. **ВАЖНО**: При установке поставьте галочку "Add Python to PATH"
3. Установите Python 3.8 или новее
4. Проверьте установку, открыв **Командную строку** или **PowerShell** и введя:
```cmd
python --version
```
или
```cmd
python.exe --version
```

Вы должны увидеть что-то вроде: `Python 3.11.5`

---

## Шаг 2: Проверка установки pip

pip обычно устанавливается вместе с Python. Проверьте, установлен ли он:
```cmd
python -m pip --version
```
или
```cmd
python.exe -m pip --version
```

Вы должны увидеть что-то вроде: `pip 23.2.1 from C:\...`

---

## Шаг 3: Обновление pip (Рекомендуется)

Всегда обновляйте pip до последней версии, чтобы избежать проблем совместимости:
```cmd
python -m pip install --upgrade pip
```
или
```cmd
python.exe -m pip install --upgrade pip
```

---

## Шаг 4: Установка необходимых библиотек

### Вариант А: Установка из requirements.txt (Рекомендуется)

1. Перейдите в папку проекта:
```cmd
cd C:\путь\к\Modbus-Scanner
```

2. Установите все зависимости:
```cmd
python -m pip install -r requirements.txt
```
или
```cmd
python.exe -m pip install -r requirements.txt
```

### Вариант Б: Установка вручную

Если у вас нет `requirements.txt`, установите каждую библиотеку отдельно:
```cmd
python -m pip install pymodbus==2.5.3
python -m pip install pyserial
python -m pip install tqdm
```

или
```cmd
python.exe -m pip install pymodbus==2.5.3
python.exe -m pip install pyserial
python.exe -m pip install tqdm
```

---

## Шаг 5: Запуск сканера

Перейдите в папку проекта и выполните:
```cmd
python modbus_scanner.py
```
или
```cmd
python.exe modbus_scanner.py
```

---

## Устранение неполадок

### Ошибка: "python is not recognized"
- Python не добавлен в PATH
- Переустановите Python и поставьте галочку "Add Python to PATH"
- Или используйте полный путь: `C:\Python311\python.exe`

### Ошибка: "No module named 'pymodbus'"
- Библиотеки не установлены
- Выполните: `python -m pip install -r requirements.txt` или `python.exe -m pip install -r requirements.txt`

### Ошибка: "Access is denied"
- Запустите Командную строку от имени администратора
- Правый клик → "Запуск от имени администратора"

### COM-порты не обнаружены
- Драйвер ОВЕН не установлен
- Преобразователь USB-RS485 не подключен
- Проверьте Диспетчер устройств на наличие COM-порта

### Устройство не найдено
- Проверьте подключение RS485 (A к A, B к B)
- Проверьте питание устройства
- Проверьте настройки Modbus устройства (скорость передачи, ID slave)
- Попробуйте поменять местами провода A и B

---