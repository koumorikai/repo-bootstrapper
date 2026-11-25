from pathlib import Path

# Твои рабочие разделы внутри D:\projects
WORKSPACE_DIRS: dict[str, str] = {
    "apps": "apps",
    "bots": "bots",
    "scripts": "scripts",
    "www": "www",
    "algo": "алгоритмы",
    "practice": "practical assignment",
}

STACK_META: dict[str, dict[str, str]] = {
    "python": {
        "title": "Python",
        "default_type": "scripts",
        "setup": "py -m pip install -r requirements.txt",
        "run": "py src/main.py",
        "tree": (
            "├── src/\n"
            "│   └── main.py          # Точка входа и основная логика\n"
            "├── .env.example         # Шаблон переменных окружения\n"
            "├── requirements.txt     # Зависимости проекта\n"
            "└── README.md            # Документация проекта"
        ),
    },
    "bot": {
        "title": "Python Telegram Bot (aiogram)",
        "default_type": "bots",
        "setup": "py -m pip install -r requirements.txt",
        "run": "py src/main.py",
        "tree": (
            "├── src/\n"
            "│   └── main.py          # Запуск бота и обработчики\n"
            "├── .env.example         # Токен бота и ID для алертов об ошибках\n"
            "├── requirements.txt     # Зависимости проекта\n"
            "└── README.md            # Документация проекта"
        ),
    },
    "react": {
        "title": "React + Vite",
        "default_type": "www",
        "setup": "npm install",
        "run": "npm run dev",
        "tree": (
            "├── src/\n"
            "│   ├── App.jsx          # Главный компонент интерфейса\n"
            "│   └── main.jsx         # Точка монтирования React\n"
            "├── index.html           # HTML-шаблон страницы\n"
            "└── README.md            # Документация проекта"
        ),
    },
    "flutter": {
        "title": "Flutter / Dart",
        "default_type": "apps",
        "setup": "flutter pub get",
        "run": "flutter run",
        "tree": (
            "├── lib/\n"
            "│   └── main.dart        # Точка входа приложения и главный экран\n"
            "└── README.md            # Документация проекта"
        ),
    },
    "cpp": {
        "title": "C++ (MinGW-w64 g++)",
        "default_type": "algo",
        "setup": "# Компилятор g++ (MSYS2 / MinGW-w64) должен быть в PATH",
        "run": "g++ -std=c++17 -O2 src/main.cpp -o build/app.exe && .\\build\\app.exe",
        "tree": (
            "├── src/\n"
            "│   └── main.cpp         # Исходный код программы\n"
            "├── build/               # Скомпилированные бинарники (в .gitignore)\n"
            "└── README.md            # Документация проекта"
        ),
    },
}

TEMPLATES: dict[str, dict[str, str]] = {
    "python": {
        ".gitignore": "__pycache__/\n*.py[cod]\n.venv/\nvenv/\n.env\nservice_account.json\ndist/\nbuild/\n",
        "requirements.txt": "python-dotenv\nrequests\n",
        ".env.example": "# Скопируй в .env и заполни ключи\nAPP_ENV=dev\nAPI_KEY=\n",
        "src/main.py": (
            "import os\n"
            "from dotenv import load_dotenv\n\n"
            "load_dotenv()\n\n\n"
            "# Главная точка входа скрипта\n"
            "def main() -> None:\n"
            '    env = os.getenv("APP_ENV", "dev")\n'
            '    print(f"Script started (env: {env})")\n\n\n'
            'if __name__ == "__main__":\n'
            "    main()\n"
        ),
    },
    "bot": {
        ".gitignore": "__pycache__/\n*.py[cod]\n.venv/\nvenv/\n.env\n",
        "requirements.txt": "aiogram>=3.0.0\npython-dotenv\n",
        ".env.example": "BOT_TOKEN=\nADMIN_CHAT_ID=\n",
        "src/main.py": (
            "import asyncio\n"
            "import logging\n"
            "import os\n"
            "from aiogram import Bot, Dispatcher\n"
            "from aiogram.filters import CommandStart\n"
            "from aiogram.types import Message\n"
            "from dotenv import load_dotenv\n\n"
            "load_dotenv()\n"
            "dp = Dispatcher()\n\n\n"
            "@dp.message(CommandStart())\n"
            "async def cmd_start(message: Message) -> None:\n"
            '    await message.answer("Bot is active.")\n\n\n'
            "# Запуск поллинга и тихое уведомление админа только при критической ошибке\n"
            "async def main() -> None:\n"
            '    token = os.environ["BOT_TOKEN"]\n'
            '    admin_id = os.getenv("ADMIN_CHAT_ID")\n'
            "    bot = Bot(token=token)\n"
            "    try:\n"
            "        await dp.start_polling(bot)\n"
            "    except Exception as err:\n"
            "        if admin_id:\n"
            '            await bot.send_message(admin_id, f"[ERROR] Bot crashed: {err}", disable_notification=True)\n'
            "        raise\n\n\n"
            'if __name__ == "__main__":\n'
            "    logging.basicConfig(level=logging.ERROR)\n"
            "    asyncio.run(main())\n"
        ),
    },
    "react": {
        ".gitignore": "node_modules/\ndist/\n.env\n.env.local\n.vite/\n",
        ".env.example": "VITE_API_URL=http://localhost:8000\n",
        "index.html": (
            '<!doctype html>\n<html lang="ru">\n  <head>\n    <meta charset="UTF-8" />\n'
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
            "    <title>App</title>\n  </head>\n"
            '  <body style="margin:0;background:#121212;">\n'
            '    <div id="root"></div>\n'
            '    <script type="module" src="/src/main.jsx"></script>\n'
            "  </body>\n</html>\n"
        ),
        "src/main.jsx": (
            'import React from "react";\n'
            'import ReactDOM from "react-dom/client";\n'
            'import App from "./App.jsx";\n\n'
            'ReactDOM.createRoot(document.getElementById("root")).render(\n'
            "  <React.StrictMode>\n    <App />\n  </React.StrictMode>\n"
            ");\n"
        ),
        "src/App.jsx": (
            "export default function App() {\n"
            "  return (\n"
            '    <main style={{ background: "#121212", color: "#f4f4f5", minHeight: "100vh", padding: "2rem", fontFamily: "sans-serif" }}>\n'
            '      <div style={{ background: "#18181b", border: "1px solid #a855f7", borderRadius: "12px", padding: "1.5rem", maxWidth: "640px" }}>\n'
            '        <h1 style={{ color: "#a855f7", marginTop: 0 }}>Project Ready</h1>\n'
            "        <p>Отредактируй <code>src/App.jsx</code>, чтобы начать разработку.</p>\n"
            "      </div>\n"
            "    </main>\n"
            "  );\n"
            "}\n"
        ),
    },
    "flutter": {
        ".gitignore": ".dart_tool/\nbuild/\n.env\n*.iml\n",
        "lib/main.dart": (
            'import "package:flutter/material.dart";\n\n'
            "void main() => runApp(const App());\n\n"
            "class App extends StatelessWidget {\n"
            "  const App({super.key});\n\n"
            "  @override\n"
            "  Widget build(BuildContext context) {\n"
            "    return MaterialApp(\n"
            "      debugShowCheckedModeBanner: false,\n"
            "      theme: ThemeData.dark().copyWith(\n"
            "        scaffoldBackgroundColor: const Color(0xFF121212),\n"
            "        colorScheme: const ColorScheme.dark(primary: Color(0xFFA855F7)),\n"
            "      ),\n"
            "      home: const Scaffold(\n"
            '        body: Center(child: Text("Project Ready")),\n'
            "      ),\n"
            "    );\n"
            "  }\n"
            "}\n"
        ),
    },
    "cpp": {
        ".gitignore": "build/\n*.o\n*.exe\n*.out\n",
        "src/main.cpp": (
            "#include <iostream>\n\n"
            "int main() {\n"
            '    std::cout << "Project Ready" << std::endl;\n'
            "    return 0;\n"
            "}\n"
        ),
    },
}


def build_readme(name: str, stack: str, description: str) -> str:
    """Формирует структурированный README.md под выбранный стек."""
    meta = STACK_META[stack]
    about = description.strip() or f"Проект `{name}` на базе **{meta['title']}**."
    return (
        f"# {name}\n\n"
        f"{about}\n\n"
        "---\n\n"
        "## Стек и структура\n\n"
        f"* **Стек:** {meta['title']}\n\n"
        "```text\n"
        f"{name}/\n"
        f"{meta['tree']}\n"
        "```\n\n"
        "---\n\n"
        "## Быстрый старт\n\n"
        "1. Клонируй репозиторий и перейди в папку проекта:\n"
        "   ```powershell\n"
        f"   git clone [https://github.com/koumorikai/](https://github.com/koumorikai/){name}.git\n"
        f"   cd {name}\n"
        "   ```\n\n"
        "2. Установи зависимости / подготовь окружение:\n"
        "   ```powershell\n"
        f"   {meta['setup']}\n"
        "   ```\n\n"
        "3. Запусти проект:\n"
        "   ```powershell\n"
        f"   {meta['run']}\n"
        "   ```\n"
    )


def write_project_files(project_dir: Path, name: str, stack: str, description: str) -> None:
    """Создаёт файлы проекта по пресету и генерирует README.md."""
    if stack not in TEMPLATES:
        raise ValueError(f"Неизвестный стек '{stack}'. Доступно: {', '.join(TEMPLATES)}")

    for rel_path, content in TEMPLATES[stack].items():
        target = project_dir / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    (project_dir / "README.md").write_text(
        build_readme(name=name, stack=stack, description=description),
        encoding="utf-8",
    )