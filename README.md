# Автоматическая классификация жанров в текстах

Этот репозиторий реализует жанровый классификатор, который различает научные тексты и художественную литературу на русском и немецком языках, используя наивный Байес и набор простых и формальных признаков текста.

---

## 1. Идея и цели проекта

- **Задача:** бинарная классификация документов (science vs. fiction).  
- **Языки:** немецкий (de) и русский (ru), сбалансированные корпуса по жанрам.  
- **Модель:** наивный Байес с гауссовским распределением по 7 статистическим признакам.  
- **Цель:** показать, что жанры можно разделять на основе простых, интерпретируемых признаков, а также продемонстрировать навыки в области NLP, классического ML и обработки текстовых корпусов.

---

## Какие умения показаны в этом проекте

- **Создание языкового корпуса и работа с мультиязычными данными**
- Создание сбалансированного корпуса для немецкого и русского языков.
- Согласование научных тем и использование одинаковых художественных произведений на обоих языках.

- **Предварительная обработка текста**  
  - Сегментация предложений с помощью токенизатора Punkt и настраиваемых правил для аббревиатур и кавычек.  
  - Ручная очистка документов для сохранения только «голого текста» (без таблиц, рисунков, верхних и нижних колонтитулов или ссылок).

- **Разработка функций для классического NLP**  
  - Разработка и реализация семи формальных интерпретируемых параметров:  
    1. Средняя длина слова.  
    2. Средняя доля длинных слов (≥ 6 символов) в предложении.  
    3. Соотношение типа и токена (TTR).  
    4. Относительная доля [hapax legomena](https://ru.wikipedia.org/wiki/%D0%93%D0%B0%D0%BF%D0%B0%D0%BA%D1%81 "Википедия").  
    5. Среднее количество слов в предложении.  
    6. Среднее количество запятых в предложении.  
    7. Относительная доля личных местоимений.

- **Моделирование и оценивание (evaluation)**  
  - Обучение [Гауссовского байесовского классификатора](https://en.wikipedia.org/wiki/Naive_Bayes_classifier "Википедия") на 7-мерных векторах текстовых параметров.  
  - 4-кратная кросс-валидация (24 текста для обучения и 8 текстов для тестирования на каждую часть, всего 64 текста) для обоих языков.
  - Критическая оценка точности классификатора (100%-ная точность).
    <details>
    <summary>(идеальная точность?)</summary>
    Такой результат не должен вводить в заблуждение. Все 64 текста были подготовлены вручную, что требует определенных временных затрат. Кроме того, все тексты были достаточно длинными и, следовательно, имели качественные и сбалансированные наборы признаков (как для обучения классификатора, так и для самой классификации).
  
    100%-ная точность соответствует поставленным задачам:
    1) Было показано, что выбранный классификатор работает правильно и точно.
    2) Было доказано, что выбранные жанры имеют четкие формальные различия.
  
    Если бы целью было внедрение максимально точного и эффективного классификатора, то сначала было бы логично проанализировать характеристики и ограничиться только эффективными параметрами. В этом случае следует провести оценку с использованием неподходящих (неидеальных) тестовых данных и сравнить классификатор с конкурирующими системами.
    </details>


- **Анализ и лингвистические выводы**  
  - Анализ разделения жанров по признакам с помощью статистических диаграмм (между жанрами и между языками).  
  - Идентификация надежных параметров, применимых вне зависимости от языка.  
  - Обсуждение языковых особенностей (например, влияние артиклей в немецком).

---

## Data

The original experiments use 64 long-form documents:

- 16 German scientific texts across diverse disciplines (biology, chemistry, philosophy, law, etc.)  
- 16 German fictional texts (novels from different authors, epochs, and genres)  
- 16 Russian scientific texts in matching disciplines  
- 16 Russian fictional texts corresponding to the German novel list (same works or parallel passages)  

All documents were:

- Cleaned to remove non-textual elements (page numbers, captions, tables, block quotes, lists, references)  
- Trimmed and normalized in length (e.g. chapter-wise cuts) without breaking sentences  

For licensing reasons, the original texts used for training cannot be included directly in this repository, because they are protected by copyright. Instead, this repository provides:

- A list of all documents used for training in the section “Source texts” below (with titles and authors, optionally linked to publicly available editions where possible).  
- Pre-extracted, anonymized training representations in the files `dataset_de` and `dataset_ru`, which contain the feature vectors and labels but not the raw text.

---

## Method

### Features

Each document is represented by a 7-dimensional feature vector:

| # | Feature                              | Intuition                                                                 |
|---|--------------------------------------|---------------------------------------------------------------------------|
| 1 | Average word length                  | Scientific texts use more long / technical words.                         |
| 2 | Long-word proportion per sentence    | Longer words are more typical for scientific style.                       |
| 3 | Type–Token Ratio (TTR)               | Measures lexical diversity per text.                                      |
| 4 | Hapax proportion                     | Fiction tends to vary its vocabulary more.                                |
| 5 | Average words per sentence           | Proxy for syntactic complexity.                                           |
| 6 | Average commas per sentence          | Additional (but noisy) syntactic indicator.                               |
| 7 | Personal pronoun proportion          | Fiction uses many more pronouns (I, you, he, she, etc.).                  |

### Model

- **Classifier:** Gaussian Naive Bayes.  
- **Input:** 7-dimensional continuous feature vectors per document.  
- **Assumptions:**  
  - Features are conditionally independent given genre (the “naive” assumption).  
  - Feature values follow a normal distribution per class.

### Evaluation

- **Setup:** 4-fold cross-validation, 75% training / 25% test in each fold, with disjoint document sets.  
- **Result:** No misclassified documents across all folds (100% accuracy under these controlled conditions).  
- **Interpretation:**  
  - Confirms that shallow features are sufficient to separate the two genres in this dataset.  
  - Highlights the importance of realistic evaluation and the limits of small, curated corpora.

---

## Repository Structure (Suggested)

