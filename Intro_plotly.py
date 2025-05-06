import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import Dash, html, dcc

# ler o csv
df = pd.read_csv('C:/Users/william/Desktop/Curso/ecommerce_estatistica.csv')
print(df.head().to_string())
print(df.columns.tolist())


def cria_graficos(df):
    # Grafico de histograma
    fig1 = px.histogram(df, x='Gênero', color='Gênero')
    fig1.update_layout(
        title='Produtos por Gênero'
    )

    # grafico de dispersão
    fig2 = px.scatter(df, x='Qtd_Vendidos_Cod', y='Desconto', color='Desconto', hover_data=['Marca'])
    fig2.update_layout(
        title='Quantidade de vendas com descontos',
        xaxis_title='Quantidade de vendas',
        yaxis_title='Desconto'
    )

    # Mapa de calor
    fig3 = px.density_heatmap(df, x='Nota', y='N_Avaliações', z='N_Avaliações', color_continuous_scale='Turbo')

    fig3.update_layout(
        title='Densidade entre Nota e numero de avaliações',
        xaxis_title='Nota',
        yaxis_title='Numero de avaliações'
    )

    # Grafico de barra
    vendas_por_marca = df.groupby('Marca')['Qtd_Vendidos_Cod'].sum().sort_values(ascending=False)
    vendas_por_marca = vendas_por_marca.head(10)

    fig4 = px.bar(vendas_por_marca)
    fig4.update_layout(
        title='Top 10 marcas mais vendidas',
        xaxis_title='Marca',
        yaxis_title='Quantidade de vendas',
        showlegend=False)

    # Grafico de pizza
    vendas_por_marca = df.groupby('Marca')['Qtd_Vendidos_Cod'].sum().sort_values(ascending=False)
    vendas_por_marca = vendas_por_marca.head(10).reset_index()

    # Cria o gráfico de pizza
    fig5 = px.pie(
        vendas_por_marca,
        names='Marca',
        values='Qtd_Vendidos_Cod',
        title='Top 10 Marcas com Mais Vendas (Codificadas)'
    )

    fig5.update_traces(textinfo='percent+label')

    # grafico de densidade
    fig6 = px.density_contour(df, x="Qtd_Vendidos_Cod", y="Marca", title="Gráfico de Densidade")
    # grafico de dispersão
    x = df["Qtd_Vendidos_Cod"]
    y = df["Nota"]

    # Remove valores ausentes
    mask = (~np.isnan(x)) & (~np.isnan(y))
    x = x[mask]
    y = y[mask]

    # Calcula os coeficientes da regressão linear: y = m*x + b
    m, b = np.polyfit(x, y, 1)

    # Cria os pontos da linha de regressão
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = m * x_line + b

    # Cria o gráfico de dispersão + linha de regressão
    fig7 = go.Figure()
    fig7.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Dados'))
    fig7.add_trace(go.Scatter(x=x_line, y=y_line, mode='lines', name='Regressão Linear', line=dict(color='red')))

    fig7.update_layout(
        title="Regressão Linear entre Qtd_Vendidos_Cod e Nota",
        xaxis_title="Qtd_Vendidos_Cod",
        yaxis_title="Nota"
    )

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7


# criar app
def cria_app(df):
    app = Dash(__name__)
    fig1, fig2, fig3, fig4, fig5, fig6, fig7 = cria_graficos(df)

    app.layout = html.Div([
        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2),
        dcc.Graph(figure=fig3),
        dcc.Graph(figure=fig4),
        dcc.Graph(figure=fig5),
        dcc.Graph(figure=fig6),
        dcc.Graph(figure=fig7),
    ])
    return app


if __name__ == '__main__':
    app = cria_app(df)
    app.run(debug=True, port=8050)
