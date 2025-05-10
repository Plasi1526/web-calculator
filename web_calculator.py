import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Стили для веб-приложения
st.markdown("""
<style>
    body {
        backgrounf-color: #1e1e1e;
        color: white;
    }
    .stButtom button {
        backgrounf-color: #4CAF50:
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 5px;
    }
    .stNumberInput input {
        background-color: #333333;
        color: white;
    }
    .stDataFrame {
        border: 1px solid #4CAF50;
    }        
>/style>
""", unsafe_allow_html=True)

#Инициализация истории
if "история" not in st.session_state:
    st.session_state["история"] = []

class ВебКалькулятор:
    def __init__(self):
        st.title("Веб-калькулятор")

    def запустить(self):
        число1 = st.number_input("Первое число", format="%f")
        число2 = st.number_input("Второе число", format="%f")

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        if col1.button("Сложить"):
            результат = self.сложить(число1, число2)
            st.success(f"Результат: {результат}")
            st.session_state["история"].append(f"{число1} + {число2} = {результат}")

        if col2.button("Вычесть"):
            результат = self.вычесть(число1, число2)
            st.success(f"Результат: {результат}")
            st.session_state["история"].append(f"{число1} - {число2} = {результат}")

        if col3.button("Умножить"):
            результат = self.умножить(число1, число2)
            st.success(f"Результат: {результат}")
            st.session_state["история"].append(f"{число1} * {число2} = {результат}")

        if col4.button("Разделить"):
            результат = self.разделить(число1, число2)
            if "Ошибка" in str(результат):
                st.error(результат)
            else:
                st.success(f"Результат: {результат}")
            st.session_state["история"].append(f"{число1} / {число2} = {результат}")

        if col5.button("Очистить историю"):
            self.очистить_историю()

        if col6.button("Загрузить историю"):
            self.загрузить_историю()

        st.markdown("---")
        if st.button("Показать историю"):
            if st.session_state["история"]:
                st.write("### 📜 История операций:")
                for запись in st.session_state["история"]:
                    if "Ошибка" in запись:
                        st.markdown(f"<p style='color:red;'>{запись}</p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='color:#4CAF50;'>{запись}</p>", unsafe_allow_html=True)
            else:
                st.markdown("История пуста")

        #Грифик истории
        if st.button("Показать график"):
            if st.session_state["история"]:
                import matplotlib.pyplot as plt
                import seaborn as sns

                сложение = [запись for запись in st.session_state["история"] if "+" in запись]
                значения = [float(запись.split("=")[1].strip()) for запись in сложение]

                if значения:
                    st.write("###📊 График результатов сложения")
                    fig, ax = plt.subplots()
                    sns.lineplot(y=значения, x=range(1, len(значения)+1), ax=ax, marker="o", color="#4CAF50")
                    ax.set_xlabel("Операция")
                    ax.set_ylabel("Результат")
                    st.pyplot(fig)
                else:
                    st.info("Нет данных для построения графика")
            else:
                st.warning("История пуста - нечего отображать")

        #Сохранение истории
        if st.button("Сохранить историю в CSV"):
            self.сохранить_историю()

        #Отладка
        if st.checkbox("DEBUG: Показать историю в сыром виде"):
            st.write("###DEBUG:", st.session_state["история"])

    def сложить(self, a, b):
        return a + b

    def вычесть(self, a, b):
        return a - b

    def умножить(self, a, b):
        return a * b

    def разделить(self, a, b):
        if b != 0:
            return a / b
        else:
            return "Ошибка: деление на ноль!"

    def сохранить_историю(self, файл="history.csv"):
        if st.session_state["история"]:
            df = pd.DataFrame({"История": st.session_state["история"]})
            df.to_csv(файл, index=False)
            st.success(f"История сохранена в {файл}")
        else:
            st.warning("История пуста - нечего сохранять")

    def очистить_историю(self):
        st.session_state["история"] = []
        st.info("История очищена")

    def загрузить_историю(self, файл="history.csv"):
        try:
            df = pd.read_csv(файл)
            if "История" in df.columns:
                st.session_state["история"] = df["История"].tolist()
                st.success("История загружена из файла")
            else:
                st.warning("Файл не содержит историю операций")
        except FileNotFoundError:
            st.warning("Файл истории не найден")
        except Exception as e:
            st.error(f"Ошибка загрузки: {e}")

        # Запуск веб-приложения
if __name__ == "__main__":
    calc = ВебКалькулятор()
    calc.запустить()

