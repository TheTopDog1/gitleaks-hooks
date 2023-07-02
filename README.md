# gitleaks-hooks

#### На вашій системі повинні бути встановлені:
- cURL
- python3
- git

Для прикладу, аби встановити ці залежності на Linux або MacOS, варто виконати:
```shell
apt-get update && \
apt-get install -y python3 python3-pip git curl
```

## Як встановити та використовувати скрипт
1. Перейдіть у директорію вашого Git-репозиторію в якому бажаєте здійснити перевірку на наявність "секретів"
2. Виконайте команду:
```shell
curl -sL https://raw.githubusercontent.com/TheTopDog1/gitleaks-hooks/main/pre-commit-hook-implementation.py | python3 -
```
При цьому, автоматично:
- буде визначено, яка на хості операційна система та архітектура
- якщо бінарний файл GitLeaks не був скопійований в репозиторій раніше, його буде встановлено в `<git_root_directory>/.git/hooks/gitleaks-hooks/gitleaks`
- якщо раніше не було сконфігуровано `pre-commit`-хук -- відбудеться конфігурація

Скрипт автоматично виставляє опцію:
```shell
git config --bool devsecops.gitleaks.enabled true
```
Перед кожним коммітом, скрипт, який запускається `pre-commit`-хуком виконує GitLeaks-перевірку лише у випадку, якщо ця опція присутня та виставлена в `true`
Вимкнути перевірку перед комітом можна командою:
```shell
git config --bool devsecops.gitleaks.enabled false
```

Note: 
GitLeaks вставновлюється тільки один раз -- при першому запуску `pre-commit`-хуку.
Однак, якщо з якихось причин, його було видалено, наступний `pre-commit`-хук ініціює повторне вставновлення

## Як переконатись, що все працює:
1. Перейдіть в директорію будь-якого наявний Git-репозиторію:
```shell
git clone https://gitlab.com/TheTopDog1/kbot && cd kbot
```
2. Встановіть GitLeaks та сконфігуруйте Git виконавши команду
```shell
curl -sL https://raw.githubusercontent.com/TheTopDog1/gitleaks-hooks/main/pre-commit-hook-implementation.py | python3 -
```
Увага, перед виконанням команди, варто переконатись, що на хості присунті наступні пакети:
- cURL
- python3
- git

<br>
Для прикладу, аби встановити ці залежності на Linux або MacOS, варто виконати:
```shell
apt-get update && \
apt-get install -y python3 python3-pip git curl
```
3. У своєму препозиторій створіть новий файл, який відповідає шаблонам сканування GitLeaks, наприклад `secrets.txt` чи `config.ini` і т.п. Наповніть цей файл компрометуючими даними:
```shell
echo 'aws_key:ghp_S9YLct5NEuk59MgtW0b2COV1k_FOO_BAR' > secrets.txt && git add secrets.txt
```
4. Будь яка спроба зберегти компрометуючу інформацію в Git буде марною)
```shell
git commit -m "added secret"
```
5. Якщо Ви все ж хочете здійснити коміт, варто здійснити переконфігурацію Git (що дуже не рекомендується 🙂):
```shell
git config --bool devsecops.gitleaks.enabled false
```

# Running Demo:
[![asciicast](https://asciinema.org/a/nuXZ0C6QcRiXNTZbNoVNWDL2A.svg)](https://asciinema.org/a/nuXZ0C6QcRiXNTZbNoVNWDL2A?autoplay=1)