from pathlib import Path
import glob
from doit.tools import config_changed

SPHINX_SOURCE = "docs"
SPHINX_BUILD = "docs/buld"
MODULE_PATH = "src"
LANGUAGES = ["ru_RU.UTF-8"]
DOMAIN = "window-domain"
POT_FILE = f"{DOMAIN}.pot"
LOCALE_DIR = "l10n"
SOURCE_DIR = "src"

DOIT_CONFIG = {
    'default tasks': ['docs'],
    'clean': ['clean_targets'],
}

def task_all():
    """Generate main generators."""
    return {
        'actions': [],
        'task_dep': ['html', 'i18n', 'docstyle', "codstyle"],
    }

def task_wheel():
    """Generate wheel."""
    return {
        'actions': ['python -m build --wheel']
    }

def task_test():
    """Run all tests from the tests directory"""
    test_files = glob.glob("tests/*.py")
    print(test_files)
    return {
        'actions': [f"python -m unittest {file}" for file in test_files]
    }

def task_docstyle():
    """Check dos style."""
    return {
        'actions': ['pydocstyle ./src']
    }
    
def task_codstyle():
    """Check code style."""
    return {
        'actions': ['flake8 ./src']
    }

def task_html():
    """Generate API documentation with sphinx-apidoc."""
    return {
        'actions': ['cd docs && make html'],
    }

def task_extract_strings():
    """Extract strings to .pot file."""
    return {
        'actions': [f"pybabel extract -o {POT_FILE} {SOURCE_DIR}"],
        'targets': [POT_FILE],
    }

def task_init_translations():
    """Initial .po files."""
    for lang in LANGUAGES:
        yield {
            'name':
            f"init_{lang}",
            'actions': [
                f"pybabel init -i {POT_FILE} -d {LOCALE_DIR} -l {lang} -D {DOMAIN}"
            ],
            'file_dep': [POT_FILE],
        }

def task_update_translations():
    """Update .po files."""
    return {
        'actions':
        [f"pybabel update -i {POT_FILE} -d {LOCALE_DIR} -D {DOMAIN}"],
        'file_dep': [POT_FILE],
        'task_dep': ['extract_strings']
    }

def task_i18n():
    """Compile .po files to .mo files."""
    po_files = [
        Path(f"{LOCALE_DIR}/{lang}/LC_MESSAGES/{DOMAIN}.po")
        for lang in LANGUAGES
    ]
    
    actions = []
    if not all(p.exists() for p in po_files):
        actions.extend([
            f"pybabel init -i {POT_FILE} -d {LOCALE_DIR} -l {lang} -D {DOMAIN}"
            for lang in LANGUAGES
        ])
    else:
        actions.append(
            f"pybabel update -i {POT_FILE} -d {LOCALE_DIR} -D {DOMAIN}"
        )
    
    actions.append(f"pybabel compile -d {LOCALE_DIR} -D {DOMAIN}")
    
    return {
        'actions': actions,
        'file_dep': [POT_FILE],
        'targets': [
            f"{LOCALE_DIR}/{lang}/LC_MESSAGES/{DOMAIN}.mo"
            for lang in LANGUAGES
        ],
    }