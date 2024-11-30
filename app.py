from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import json


val = 20
sale_down = 0

# Загружаем данные
def load_data():
    pdf_source = pd.read_excel('НГ2.xlsx', engine='openpyxl', sheet_name='Склад')
    pdf_source = (pdf_source[['ID', 'Название норм', 'Остаток', 'Закупка', 'Реализация']]
                    .rename(columns={
                        'ID':'id',
                        'Название норм':'name',
                        'Остаток':'balance',
                        'Закупка':'buying',
                        'Реализация':'realization'
                    })
                )

    pdf_source_filtered = pdf_source.loc[pdf_source['name'].notna()]

    return pdf_source_filtered


def price_product(pdf, val_up, sale_down):

    buying_total = pdf.buying_total.sum()
    realization_total = pdf.realization_total.sum()

    nadb_source = (realization_total - buying_total)
    nadb_source_pr = (nadb_source/buying_total)*100
    final_price = realization_total * (1 + val_up/100)
    sale_value = final_price * (sale_down/100)
    final_price_sale = final_price - sale_value
    margin = final_price_sale - buying_total
    margin_pr = (margin/buying_total)*100

    dictpr = {'buying_total':f'{buying_total: .1f}',
            'nadb_source':f'{nadb_source: .1f}',
            'nadb_source_pr':f'{nadb_source_pr:,.0f}%',
            'realization_total':f'{realization_total: .1f}',
            'val_up':f'{val_up:,.0f}%',
            'final_price':f'{final_price: .1f}',
            'sale':f'{sale_down:,.0f}%',
            'sale_value':f'{sale_value: .1f}',
            'final_price_sale':f'{final_price_sale: .1f}',
            'margin':f'{margin: .1f}',
            'margin_pr':f'{margin_pr:,.0f}%'
            }

    return dictpr

app = Flask(__name__)


@app.route('/')
def index():

    pdf_data = load_data()
    product_names = pdf_data['name'].to_list()

    return render_template('products.html',
                            yourListOfValues=json.dumps(product_names, ensure_ascii=False),
                            product_names=product_names)


@app.route('/save_product', methods=['POST'])
def save_product():
    global data
    data = request.get_json()

    return 'Success save as product'


@app.route('/save_val', methods=['POST'])
def save_val():
    global val, sale_down
    req_data = request.get_json()

    val = float(req_data[0].get('nadbprice'))
    sale_down = float(req_data[0].get('salenadb'))
    return 'Success save as product'

@app.route('/final_info')
def thank_you():


    pdf = load_data()
    pdf['cnt'] = 0.0

    for i in data:
        filtered = (pdf.name == i.get('product'))
        pdf.loc[filtered, 'cnt'] = float(i.get('quantity'))

    pdf_filtered = pdf.loc[pdf.cnt > 0]

    pdf_filtered['buying_total'] = pdf_filtered.buying * pdf_filtered.cnt
    pdf_filtered['realization_total'] = pdf_filtered.realization * pdf_filtered.cnt

    price_prod = price_product(pdf_filtered, val, sale_down)

    # try:
    #     print(val)
    #     price_prod = price_product(pdf_filtered, val)
    # except:
    #     price_prod = price_product(pdf_filtered, 20)

    return render_template('product_info.html', table_data=pdf_filtered.to_dict('records'), price_prod=price_prod)


if __name__ == '__main__':
    app.run(debug=True)


