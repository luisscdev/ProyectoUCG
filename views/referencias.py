"""Vista 'Referencias' — bibliografía en formato APA 7."""

import streamlit as st
from src.ui.helpers import hero, section_title, divider, footer


def render() -> None:
    hero(
        title="Referencias",
        subtitle=(
            "Bibliografía utilizada para sustentar el marco teórico y la metodología "
            "del proyecto. Formato APA 7ma edición."
        ),
        badges=["APA 7", "Bibliografía"],
    )

    referencias = [
        ("Booch, G., Maksimchuk, R. A., Engle, M. W., Young, B. J., Conallen, J., y Houston, "
         "K. A. (2007). *Object-oriented analysis and design with applications* (3.ª ed.). Addison-Wesley."),

        ("Breiman, L. (2001). Random forests. *Machine Learning, 45*(1), 5–32. "
         "https://doi.org/10.1023/A:1010933404324"),

        ("Chen, T., y Guestrin, C. (2016). XGBoost: A scalable tree boosting system. En *Proceedings "
         "of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* "
         "(pp. 785–794). ACM. https://doi.org/10.1145/2939672.2939785"),

        ("Hastie, T., Tibshirani, R., y Friedman, J. (2009). *The elements of statistical learning: "
         "Data mining, inference, and prediction* (2.ª ed.). Springer."),

        ("Hughes, J. (1989). Why functional programming matters. *The Computer Journal, 32*(2), "
         "98–107. https://doi.org/10.1093/comjnl/32.2.98"),

        ("Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science and "
         "Engineering, 9*(3), 90–95. https://doi.org/10.1109/MCSE.2007.55"),

        ("Lutz, M. (2013). *Learning Python* (5.ª ed.). O’Reilly Media."),

        ("McKinney, W. (2010). Data structures for statistical computing in Python. En *Proceedings "
         "of the 9th Python in Science Conference* (pp. 56–61). "
         "https://doi.org/10.25080/Majora-92bf1922-00a"),

        ("McKinney, W. (2017). *Python for data analysis: Data wrangling with Pandas, NumPy and "
         "IPython* (2.ª ed.). O’Reilly Media."),

        ("Mertz, D. (2015). *Functional programming in Python*. O’Reilly Media."),

        ("Monburinon, N., Chertchom, P., Kaewkiriya, T., Rungpheung, S., Buya, S., y Boonpou, P. "
         "(2018). Prediction of prices for used car by using regression models. En *2018 5th "
         "International Conference on Business and Industrial Research (ICBIR)* (pp. 115–119). IEEE. "
         "https://doi.org/10.1109/ICBIR.2018.8391177"),

        ("Pandala, S. R. (2019). *Lazy Predict* [Software]. GitHub. "
         "https://github.com/shankarpandala/lazypredict"),

        ("Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., "
         "Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., "
         "Cournapeau, D., Brucher, M., Perrot, M., y Duchesnay, É. (2011). Scikit-learn: Machine "
         "learning in Python. *Journal of Machine Learning Research, 12*, 2825–2830."),

        ("Pudaruth, S. (2014). Predicting the price of used cars using machine learning techniques. "
         "*International Journal of Information and Computation Technology, 4*(7), 753–764."),

        ("Ramalho, L. (2022). *Fluent Python: Clear, concise, and effective programming* (2.ª ed.). "
         "O’Reilly Media."),

        ("Russell, S., y Norvig, P. (2021). *Artificial intelligence: A modern approach* (4.ª ed.). "
         "Pearson."),

        ("Sebesta, R. W. (2019). *Concepts of programming languages* (12.ª ed.). Pearson."),

        ("Streamlit Inc. (2024). *Streamlit documentation*. https://docs.streamlit.io"),

        ("Van Roy, P., y Haridi, S. (2004). *Concepts, techniques, and models of computer programming*. "
         "MIT Press."),

        ("Wirth, R., y Hipp, J. (2000). CRISP-DM: Towards a standard process model for data mining. "
         "En *Proceedings of the 4th International Conference on the Practical Applications of "
         "Knowledge Discovery and Data Mining* (pp. 29–39). Practical Application Company."),
    ]

    section_title(f"Bibliografía ({len(referencias)} fuentes)")
    for ref in referencias:
        st.markdown(
            f"""
            <div style="padding: 8px 0; padding-left: 24px; text-indent: -24px; line-height: 1.7;">
                {ref}
            </div>
            """,
            unsafe_allow_html=True,
        )

    divider()
    footer()
