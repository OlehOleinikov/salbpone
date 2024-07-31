import datetime
import os
import sys
sys.path.insert(0, os.path.abspath('../salbpone'))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Пакет вирішення задачі збиральної лінії SALBP-1'
copyright = '2024, Олег Олейніков'
author = 'Олег Олейніков'
release = '24.7.4'
today = datetime.date.today().strftime('%d.%m.%Y')

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

# Додає розширення для вимірювання часу, який витрачається на побудову документації
extensions.append('sphinx.ext.duration')

# Дозволяє інтеграцію з doctest для перевірки прикладів коду в документації
extensions.append('sphinx.ext.doctest')

# Дозволяє створювати посилання на документацію інших проектів
extensions.append('sphinx.ext.intersphinx')

# Підтримка роботи з markdown розміткою (не тільки RST)
# extensions.append('myst_parser')

# Можливість використання розмітки - "Google-style docstrings"
extensions.append('sphinx.ext.napoleon')
napoleon_include_private_with_doc = True
napoleon_include_private = True

# Додає до сторінок документації посилання, за допомогою яких можна переглянути первинний код.
extensions.append('sphinx.ext.viewcode')

# Дозволяє автоматично генерувати документацію з докстрінгів та анотацій коду
extensions.append('sphinx.ext.autodoc')
autodoc_dumb_docstring = True  # Дозволяє генерувати документацію для об'єктів, які не мають докстрінгів.
"""
autodoc_typehints: 

'signature': Якщо встановлено 'signature', то інформація про типи буде додана до підпису (signature) об'єкта 
у документації. Це означає, що типи будуть відображені безпосередньо у вигляді підпису функції чи методу.

'description': Якщо встановлено 'description', то інформація про типи буде додана до розділу з описом (description) 
об'єкта у документації. Це означає, що типи будуть вказані у текстовому описі об'єкта.
"""
autodoc_typehints = 'description'

# Спрощує генерацію автоматичних зведених звітів для класів та функцій
extensions.append('sphinx.ext.autosummary')
autosummary_generate = True  # дозволяє автоматично генерувати зведені звіти

# Кнопка copy у фрагментах коду:
extensions.append('sphinx_copybutton')

# Кнопка вимкнення виводу у фрагментах коду:
extensions.append('sphinx_toggleprompt')
toggleprompt_offset_right = 35

# Зміст модулів та класів (заміна аутосаммарі)
# - автоматично збирає інформацію про класи, функції та методи, що містяться в цьому модулі
extensions.append('sphinx_automodapi.automodapi')
# - допомагає коректно розрізняти об'єкти з однаковими іменами, такі як методи класу та функції
extensions.append('sphinx_automodapi.smart_resolver')
# - чи слід показувати члени класу в документації:
numpydoc_show_class_members = False

# Налаштування пошуку
#extensions.append('sphinx_search.extension')
#html_search_language = 'ru'

# Додаткові налаштування:
todo_include_todos = True
#source_suffix = '.rst'
master_doc = 'index'
add_function_parentheses = True
add_module_names = True

templates_path = ['_templates']
exclude_patterns = []

language = 'uk_UA'


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


# -- Options for LaTeX output ---------------------------------------------
latex_toplevel_sectioning = 'part'

latex_additional_files = [
    '_static/logo_latex.jpg',
    '_static/MyChapterStyle.sty'
]

# Налаштування формату LaTeX-документу
latex_elements = {
    # Налаштування титульної сторінки
    'papersize': 'a4paper',
    'pointsize': '12pt',
    'preamble':
                '\\usepackage{fancyhdr}\n'
                '\\usepackage{tabularx}\n'
                '\\usepackage{verbatim}\n'
                '\\usepackage{MyChapterStyle}\n'
                '\\makeatletter\n'
                '\\makeatother\n'
                '\\usepackage{setspace}\n'
                '\\singlespacing\n' 
                '\\usepackage{enumitem}\n'
                '\\setlist{noitemsep}\n'
                '\\usepackage{graphicx}\n'
                '\\graphicspath{{_static/}}\n'
                '\\renewcommand{\\releasename}{вер.}\n',
                # '\\let\\part\\chapter\n'
                # '\\let\\chapter\\section\n'
                # '\\let\\section\\subsection\n'
                # '\\let\\pivotpart\\part\n',


    'figure_align': 'htbp',  # Розташування зображень

    # Налаштування інтервалу між рядками
    'babel': '\\usepackage[ukrainian]{babel}',  # Використана мова: українська
    'maketitle': r'''
        \begin{titlepage}
        	\vspace*{-5em}
            \centering
           	{\textsc{МІНІСТЕРСТВО ОСВІТИ І НАУКИ УКРАЇНИ} \par}
           	\vspace{-0.5em}
            {\textsc{НАЦІОНАЛЬНИЙ ТЕХНІЧНИЙ УНІВЕРСИТЕТ УКРАЇНИ } \par}
            \vspace{-0.75em}
            {\textsc{«КИЇВСЬКИЙ ПОЛІТЕХНІЧНИЙ ІНСТИТУТ ІМЕНІ ІГОРЯ СІКОРСЬКОГО»} \par}
            \vspace{-0.75em}
            {\textsc{Навчально-науковий інститут прикладного системного аналізу} \par}
            \vspace{-0.75em}
            {\textsc{Кафедра математичних методів системного аналізу} \par}
            \vspace{-1em}
            {\rule{15cm}{0.4pt}\par}
            \vspace{3cm}
            {\Large\textsc{ДОДАТОК \_ }\par}
            {\large\textsc{до курсової роботи з дисципліни «Теорія прийняття рішень» }}
            {\large\textsc{тема №11: «Завдання визначення оптимальної кількості робочих місць» }\par}
            {\normalsize\textsc{(посібник та документація первинного коду розробленого програмного продукту)} \par}
			\vfill
			\begin{list}{}{\leftmargin=8cm}
				\item Виконав: студент 4 курсу групи ІС-21зп
				\vspace{-0.5em}
				\item Спеціальність 122 «Комп'ютерні науки»
				\vspace{-0.5em}
				\item Олейніков Олег Анатолійович
				\vspace{-0.5em}
				\item Керівник: професор Зайченко Юрій Петрович
			\end{list}
			\vfill
            {\large Київ – 2024 \par}
        \end{titlepage}
    ''',

    # Налаштування розміру полів документа
    'sphinxsetup': 'hmargin={1in,1.5cm}, vmargin={2cm,2cm}, marginpar=0in',
    'releasename': 'вер.'

}


# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'main_doc_course.tex', 'SALBP-1',
     'Олег ОЛЕЙНІКОВ', 'book')
]
