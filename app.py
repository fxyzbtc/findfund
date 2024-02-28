'''
语料：基金数据，每月更新一次
输入: 选择指数，输入指数代码或名称，输入基金代码或名称
    1. 选择指数时，按照指数规模排序了
    2. 只搜索ticker、名称关键字
输出：展示所有相关基金
    1. 默认按规模排序
    2. 点击header，可以按照该列排序
过滤器：指数名称，基金管理类别（混合、股票、债券、QDI等），证监会基金类别（指数、量化、增强等）

'''


import gradio as gr
import pandas as pd
from pathlib import Path

DATA_FP =  'data/cnfunds.csv'

def prepare_data():
    def get_header():
        with open(DATA_FP, encoding="utf8") as fp:
            return fp.readline().strip().split(',')
        
    def load_csv():
        with open(DATA_FP, encoding="utf8") as fp:
            return pd.read_csv(fp, dtype=dict(zip(get_header(), ['str']*len(get_header()))))

    etf = load_csv()

    etf.replace('--', '0', inplace=True)
    etf['assetalNet'] = etf['assetalNet'].astype(float)
    etf['establishYears'] = etf['establishYears'].astype(float)
    etf['price'] = etf['price'].astype(float)
    etf['navChangeRatio'] = etf['navChangeRatio'].astype(float)
    etf['indexName'].fillna(value='无', inplace=True)
    etf['indexTicker'].fillna(value='无', inplace=True)
    etf['csrcFundCategory'].fillna(value='无', inplace=True)
    etf['fundManageCategory'].fillna(value='无', inplace=True)
    etf['fundOrganizationFormCategory'].fillna(value='无', inplace=True)
    etf['fundAssetalCategory'].fillna(value='无', inplace=True)
    etf['fundCategoryName'].fillna(value='无', inplace=True)
    etf['fundInvestAreaCategory'].fillna(value='无', inplace=True)
    etf['indexInfo.industry'].fillna(value='无', inplace=True)


    cols_left = ['tickerName', 'assetalNet', 'etfListTradeAmount', 
                'indexInfo.name', 'indexInfo.ticker',
                'indexInfo.industry','fundOrganizationFormCategory', 
                'fundManageCategory', 'fundAssetalCategory', 
                'navChangeAnnualRatio', 'navChangeAnnualRatio3m',
                'establishYears', 'fundManageCategory', 
                'peAvg', 'pbAvg','fundCategoryName', 'fundInvestAreaCategory', ]

    cols_right = set(etf.columns)-set(cols_left)
    columns = cols_left + list(cols_right)
    return etf[columns]


DATA_HEADER_i18n = {
    'myOptions': '我的期权',
    'myPositions': '我的持仓',
    'isSuspend': '是否暂停',
    'redemption': '赎回',
    'subscripation': '认购',
    'positionDate': '持仓日期',
    'positionPubDate': '持仓发布日期',
    'isEnd': '是否结束',
    'ticker': '股票代码',
    'name': '名称',
    'tickerName': '股票名称',
    'fundAssetalCategory': '基金资产类别',
    'fundExchangeMarketCategory': '基金交易市场类别',
    'listed': '是否上市',
    'fundInvestAreaCategory': '基金投资领域类别',
    'fundManageCategory': '基金管理类别',
    'fundOrganizationFormCategory': '基金组织形式类别',
    'csrcFundCategory': '证监会基金类别',
    'indexName': '指数名称',
    'indexTicker': '指数代码',
    'indexStartDate': '指数开始日期',
    'indexInfo.ticker': '指数信息.代码',
    'indexInfo.name': '指数信息.名称',
    'indexInfo.marketStyle': '指数信息.市场风格',
    'indexInfo.valueStyle': '指数信息.价值风格',
    'indexInfo.motif': '指数信息.主题',
    'indexInfo.term': '指数信息.期限',
    'indexInfo.industry': '指数信息.行业',
    'indexInfo.marketBasis': '指数信息.市场基础',
    'indexInfo.investArea': '指数信息.投资领域',
    'indexInfo.credit': '指数信息.信用',
    'fundCategoryName': '基金类别名称',
    'stockCategoryName': '股票类别名称',
    'minHoldPeriod': '最短持有期',
    'targetYear': '目标年份',
    'targetRiskLevel': '目标风险等级',
    'unitConvertType': '单位转换类型',
    'valueTypes.r3m': '价值类型.r3m',
    'marketTypes.r3m': '市场类型.r3m',
    'peAvg': '平均市盈率',
    'pbAvg': '平均市净率',
    'annualReturns': '年度回报率',
    'cur10000Returns': '当前10000元回报率',
    'fundGuarantor': '基金担保人',
    'guaranteedPeriod': '担保期限',
    'periodLeft': '剩余期限',
    'convertibleInConvertibleRatio': '可转换比例',
    'convertibleRatio': '转换比例',
    'listDate': '上市日期',
    'establishYears': '成立年限',
    'assetalNet': '资产净值',
    'nav': '净值',
    'fundShareType': '基金份额类型',
    'navUnit': '净值单位',
    'price': '价格',
    'navChangeRatio': '净值变化比率',
    'navChangeAnnualRatio': '净值年度变化比率',
    'navChangeAnnualRatio3m': '净值年度变化比率3m',
    'priceChangeRatio': '价格变化比率',
    'priceChangeAnnualRatio': '价格年度变化比率',
    'priceChangeAnnualRatio3m': '价格年度变化比率3m',
    'etfListTradeAmount': 'ETF列表交易金额',
    'etfListFundAvgTradeAmount.tradeAmount3': 'ETF列表基金平均交易金额.交易金额3',
    'etfListFundAvgTradeAmount.tradeAmount5': 'ETF列表基金平均交易金额.交易金额5',
    'etfListFundAvgTradeAmount.tradeAmount10': 'ETF列表基金平均交易金额.交易金额10',
    'etfListFundAvgTradeAmount.tradeAmount30': 'ETF列表基金平均交易金额.交易金额30',
    'tradeAsset': '交易资产',
    'navFcst': '净值预测',
    'navFcstDr': '净值预测Dr',
    'priceNavRatioReal': '价格净值比实际',
    'priceNavRatioRealDate': '价格净值比实际日期',
    'navDate': '净值日期',
    'navChangeDate': '净值变化日期',
    'navPeriodChangeDate': '净值期间变化日期',
    'priceNavRatio': '价格净值比',
    'priceNavRatioDate': '价格净值比日期',
    'companyCode': '公司代码',
    'companyName': '公司名称',
    'managers': '经理人',
    'pe': '市盈率',
    'pb': '市净率',
    'isAhFund': '是否AH基金'
}

ETF = prepare_data()

# groupby index name with sum of assetalNet, and sort by assetalNet
# output as values of multiselect
INDEXES = (ETF.groupby('indexName').sum().
           sort_values(by=['assetalNet'], ascending=False).
           index.tolist())

# to display the agg of sum by default
INDEX_GRP_SUM = ETF.groupby(['indexName', 'indexTicker']).sum()
INDEX_GRP_SUM = INDEX_GRP_SUM.add_suffix('_sum').reset_index().sort_values(by=['assetalNet_sum'], ascending=False)
INDEX_GRP_SUM = INDEX_GRP_SUM[['indexName', 'indexTicker', 'assetalNet_sum']]
INDEX_GRP_SUM.columns = ['指数名称', '指数代码', '指数规模(亿)']

# INDEX_INDUSTRY = ETF['indexInfo.industry'].unique().tolist()
# display the index_industry by the groupby sum result
INDEX_INDUSTRY = (ETF.groupby('indexInfo.industry').sum().
                  sort_values(by=['assetalNet'], ascending=False).
                  index.tolist())
FUNDORGANIZATIONFORMCATEGORY = ETF['fundOrganizationFormCategory'].unique().tolist()
FUNDASSETALCATEGORY = ETF['fundAssetalCategory'].unique().tolist()
INVESTAREACATEGORY = ETF['fundInvestAreaCategory'].unique().tolist()

# filters

with gr.Blocks() as main:
    # input the index/fund tiker or name
    # in one row, two columns
    with gr.Tab(label='搜基金') as gr_tab_fund:

        # user input
        gr_tb_search_by = gr.Textbox(label='输入代码或名称')
        gr_dd_indexName = gr.Dropdown(INDEXES, label='选择指数', multiselect=True)

        # filters    
        gr_cbg_indexindustry = gr.CheckboxGroup(INDEX_INDUSTRY, label='指数行业')
        gr_cbg_fundorganizationformcategory = gr.CheckboxGroup(FUNDORGANIZATIONFORMCATEGORY, label='基金组织形式类别')
        gr_cbg_fundassetalcategory = gr.CheckboxGroup(FUNDASSETALCATEGORY, label='基金资产类别')
        gr_cbg_investareacategory = gr.CheckboxGroup(INVESTAREACATEGORY, label='指数投资领域类别')
        gr_btn_search = gr.Button('搜索')


        # output
        gr_df_result = gr.DataFrame(None,visible=True, label='搜索结果',)
        # conslidate inputs and outputs
        inputs_dict = {
            'name': gr_tb_search_by,
            'indexName': gr_dd_indexName,
            'indexInfo.industry': gr_cbg_indexindustry,
            'fundOrganizationFormCategory': gr_cbg_fundorganizationformcategory,
            'fundAssetalCategory': gr_cbg_fundassetalcategory,

            'fundInvestAreaCategory': gr_cbg_investareacategory,
        }
        inputs = list(inputs_dict.values())
        outputs = [gr_df_result]

        @gr_btn_search.click(inputs=inputs, outputs=outputs)
        def search_by(name, indexName, indexInfo_industry, 
                      fundOrganizationFormCategory, fundAssetalCategory, 
                      fundInvestAreaCategory):
            # got nothing to do
            if not any((name.strip(), indexName, indexInfo_industry, 
                        fundOrganizationFormCategory,
                        fundAssetalCategory, 
                        fundInvestAreaCategory )):
                gr.Warning('请输入代码或名称')
                return None
        
            # everytime we search, we need to use new DataFrame copied from ETF
            # do NOT pollute the original ETF

            from copy import deepcopy
            result = deepcopy(ETF)

            if name:
                name_bool = result['name'].str.contains(name)
                result = result[name_bool]

            for column, _gr in inputs_dict.items():
                # locals() cannot use dot, search_by locals() mapped from inputs_dict 
                column_key = column.replace('.', '_')

                if column == 'name':
                    continue    
                if locals().get(column_key, None):
                    # locals().get must be column_key not column (having dot .)
                    bool = result[column].isin(locals().get(column_key, None))
                    result = result[bool]
            result.sort_values(by=['assetalNet'], ascending=False, inplace=True) 
            result.rename(columns=DATA_HEADER_i18n, inplace=True)
            return result

    # input the index name / ticker, return teh assetalNet sum
    with gr.Tab(label='搜指数') as gr_tab_index:
        gr_tb_search_by = gr.Textbox(label='输入代码或名称', interactive=True)
        gr_df_result = gr.DataFrame(INDEX_GRP_SUM,visible=True, label='搜索结果',)
        # conslidate inputs and outputs
        inputs = [gr_tb_search_by]
        outputs = [gr_df_result]
        
        @gr_tb_search_by.change(inputs=inputs, outputs=outputs)
        def search_by(search_by):
            from copy import deepcopy
            result = deepcopy(ETF)
            if search_by:
                indexTicker_bool = result['indexTicker'].astype(str).str.contains(search_by)
                indexName_bool = result['indexName'].str.contains(search_by)
            
                # output
                result = result[indexTicker_bool | indexName_bool]
                sum = result.groupby(['indexName', 'indexTicker']).sum()
                sum = sum.add_suffix('_sum').reset_index().sort_values(by=['assetalNet_sum'], ascending=False)
                return sum[['indexName', 'indexTicker', 'assetalNet_sum']]

if __name__ == "__main__":
    main.queue()
    main.launch(server_name="0.0.0.0")