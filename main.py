import argparse
import os
from pathlib import Path
import subprocess
from github_api import create_github_repo
from templates import STACK_META, TEMPLATES, WORKSPACE_DIRS, write_project_files

BASE_WORKSPACE = Path(r"D:\projects")


def run_git(args: list[str], cwd: Path) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True)


def resolve_target_dir(name: str, stack: str, folder_type: str | None) -> Path:
    """Определяет папку внутри D:\\projects строго по структуре пользователя."""
    if folder_type:
        return BASE_WORKSPACE / WORKSPACE_DIRS[folder_type] / name

    default_key = STACK_META[stack]["default_type"]
    default_folder = WORKSPACE_DIRS[default_key]
    print(f"Куда положить проект '{name}'?")
    print(f"  [Enter] -> D:\\projects\\{default_folder}\\{name} (по умолчанию для {stack})")
    for key, folder in WORKSPACE_DIRS.items():
        print(f"  {key:<8} -> D:\\projects\\{folder}\\{name}")

    choice = input("Выбор раздела: ").strip().lower()
    if not choice:
        return BASE_WORKSPACE / default_folder / name
    if choice in WORKSPACE_DIRS:
        return BASE_WORKSPACE / WORKSPACE_DIRS[choice] / name
    raise ValueError(f"Неизвестный раздел '{choice}'. Доступно: {', '.join(WORKSPACE_DIRS)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="gh-init",
        description="Создание проекта в структуре D:\\projects и синхронизация с GitHub (koumorikai)",
        epilog=(
            "Примеры:\n"
            '  gh-init tg-alert bot -d "Бот уведомлений"\n'
            '  gh-init promo-site react -t www --public -d "Новый сайт"\n'
            '  gh-init lab-3 cpp -t practice -d "Лабораторная №3"\n'
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("name", help="Имя репозитория и папки проекта")
    parser.add_argument(
        "stack",
        nargs="?",
        default="python",
        choices=list(TEMPLATES.keys()),
        help="Стек проекта (python, bot, react, flutter, cpp)",
    )
    parser.add_argument(
        "-t",
        "--type",
        dest="folder_type",
        choices=list(WORKSPACE_DIRS.keys()),
        help="Папка назначения: apps | bots | scripts | www | algo | practice",
    )
    parser.add_argument("--public", action="store_true", help="Сделать репозиторий публичным (по умолчанию приватный)")
    parser.add_argument("-d", "--desc", default="", help="Описание проекта для GitHub и README.md")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError(
            "Не найден GITHUB_TOKEN в переменных среды.\n"
            'Выполни в PowerShell: setx GITHUB_TOKEN "ghp_твой_токен" и перезапусти терминал.'
        )

    project_dir = resolve_target_dir(name=args.name, stack=args.stack, folder_type=args.folder_type)

    if project_dir.exists():
        raise FileExistsError(f"Папка уже существует: {project_dir}")

    print(f"\n[1/4] Создаю каркас ({args.stack}) в {project_dir}...")
    project_dir.mkdir(parents=True)
    write_project_files(project_dir, name=args.name, stack=args.stack, description=args.desc)

    print(f"[2/4] Создаю {'публичный' if args.public else 'приватный'} репозиторий на GitHub...")
    clone_url = create_github_repo(
        name=args.name,
        token=token,
        private=not args.public,
        description=args.desc,
    )

    print("[3/4] Инициализирую Git и делаю первый коммит...")
    run_git(["init", "-b", "main"], cwd=project_dir)
    run_git(["add", "."], cwd=project_dir)
    run_git(["commit", "-m", "chore: initial project structure and README"], cwd=project_dir)
    run_git(["remote", "add", "origin", clone_url], cwd=project_dir)

    print("[4/4] Отправляю в origin/main...")
    run_git(["push", "-u", "origin", "main"], cwd=project_dir)

    meta = STACK_META[args.stack]
    print("\nГотово!")
    print(f"  Папка:       {project_dir}")
    print(f"  Репозиторий: {clone_url.removesuffix('.git')}")
    print("\nЧто дальше:")
    print(f'  cd "{project_dir}"')
    print(f"  {meta['setup']}")
    print(f"  {meta['run']}")
    print("  code .")


if __name__ == "__main__":
    main()