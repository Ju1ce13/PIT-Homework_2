
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, mannwhitneyu

st.title("Исследование датасета")
st.subheader("Загрузите CSV файл с датасетом")
st.write("Программа позволяет выбирать две переменные из датасета, визуализировать их распределение и применять проверочные алгоритмы на выбор.")
st.write("Допустимые файлы: .csv")

def load_dataset(file):
    try:
        dataset = pd.read_csv(file)
        return dataset
    except Exception as e:
        return str(e)

file = st.file_uploader("Загрузите CSV файл")
dataset = load_dataset(file)
if isinstance(dataset, pd.DataFrame):
    st.success("Датасет загружен успешно!")
else:
    st.error(dataset)

if isinstance(dataset, pd.DataFrame):
    columns = dataset.columns.tolist()
    column1 = st.selectbox("Выберите первую переменную", columns)
    column2 = st.selectbox("Выберите вторую переменную", columns)

    # Визуализация распределения каждой переменной
    fig, ax = plt.subplots(figsize=(10, 6))
    if dataset[column1].dtype == 'object' or dataset[column1].nunique() <= 10:
        sns.countplot(data=dataset, x=column1, ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    else:
        sns.histplot(data=dataset, x=column1, ax=ax)
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    if dataset[column2].dtype == 'object' or dataset[column2].nunique() <= 10:
        sns.countplot(data=dataset, x=column2, ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    else:
        sns.histplot(data=dataset, x=column2, ax=ax)
    st.pyplot(fig)

methods = ['T-test', 'mann-whitney U-test']
method = st.selectbox("Выберите проверочный алгоритм", methods)

result = None
if method == 'T-test':
    try:
        print(dataset[column1], dataset[column2])
        result = ttest_ind(dataset[column1], dataset[column2])
    except Exception as e:
        result = "Вы выбрали столбец без числового значения"
elif method == 'mann-whitney U-test':
    try:
        result = mannwhitneyu(dataset[column1], dataset[column2])
    except Exception as e:
        result = "Вы выбрали столбец без числового значения"

st.write(f"Результат проверки гипотезы с помощью {method}:")
st.write(result)


if __name__ == "__main__":

    st.write("---")
    st.write("")

    load_dataset(file)